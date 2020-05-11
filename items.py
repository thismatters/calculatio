from math import ceil
import logging

from item_defs import item_defs
import recipes as _recipes
from utils import AdditiveUpdateDict

_item_objects = {}


class Stringified:
    def stringify(self, indent_depth=0):
        _sources = []
        main_item = (
            " " * indent_depth * 2 + self._stringify_template()
        )
        _sources.append(main_item)
        for source in self.sources:
            _source = source.stringify(indent_depth=indent_depth + 1)
            # print(f"source {_source}")
            _sources.append(_source)
        return "\n".join(_sources)


class BusLine(Stringified):
    def __init__(self, **kwargs):
        props = (
            "item",
            "input_rate",
        )
        for prop in props:
            setattr(self, prop, None)
        self.sources = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _stringify_template(self):
        return (f">>> From bus '{self.item}', Input Rate: {self.input_rate}")


class Line(Stringified):
    def __init__(self, **kwargs):
        props = (
            "burnable_fuel",
            "crafter_count",
            "crafter_item",
            "electricity_consumption",
            "fuel_burn_rate",
            "inserter_count",
            "item",
            "output_rate",
            "target_output_rate",
            "recipe",
        )
        for prop in props:
            setattr(self, prop, None)
        self.sources = kwargs.pop("sources", [])
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _stringify_template(self):
        return (
            f"Item: {self.item}, Output Rate: {self.output_rate}/{self.target_output_rate}, "
            f"{self.crafter_item}: {self.crafter_count}, Recipe: {str(self.recipe)}"
        )

    def __str__(self):
        return self.stringify() + "\n"

    def add_source(self, source):
        self.sources.append(source)

    def remove_source(self, source_item):
        """When consolidating the production of an item the source can be removed"""
        # check self
        if self.item == source_item:
            return
        # check subsources
        source_item_lines = []
        remove_idx = None
        for idx, source in enumerate(self.sources):
            if not isinstance(source, (Line, )):
                continue
            if source.item == source_item:
                remove_idx = idx
            else:
                source_item_lines.extend(source.remove_source(source_item))
        if remove_idx is not None:
            removed = self.sources.pop(remove_idx)
            replacement = BusLine(item=removed.item, input_rate=removed.target_output_rate)
            self.sources.insert(remove_idx, replacement)
            source_item_lines.append(removed)

        return source_item_lines

    def _crafters(self, *, crafters=None):
        crafters = crafters or AdditiveUpdateDict()
        crafters.update({self.crafter_item: self.crafter_count})
        for source in self.sources:
            if not isinstance(source, (Line, )):
                continue
            crafters = source._crafters(crafters=crafters)
        return crafters

    @property
    def all_crafters(self):
        return self._crafters()

    @property
    def total_electricity_demand(self):
        demand = 0
        if self.electricity_consumption is not None:
            demand = self.electricity_consumption
        for source in self.sources:
            if not isinstance(source, (Line, )):
                continue
            demand += source.total_electricity_demand
        return demand

    @property
    def total_electricity_production(self):
        production = 0
        if self.item == "Electricity":
            production += self.output_rate
        for source in self.sources:
            if not isinstance(source, (Line, )):
                continue
            production += source.total_electricity_production
        return production

    def _burnables(self, *, burnables=None):
        burnables = burnables or AdditiveUpdateDict()
        if self.burnable_fuel is not None:
            burnables.update({self.burnable_fuel: self.fuel_burn_rate})
        for source in self.sources:
            if not isinstance(source, (Line, )):
                continue
            burnables = source._burnables(burnables=burnables)
        return burnables

    @property
    def total_burnables(self):
        return self._burnables()

    def _all_items(self, *, target=False):
        attr = "output_rate"
        if target:
            attr = "target_output_rate"
        items = AdditiveUpdateDict({self.item: getattr(self, attr)})
        for source in self.sources:
            if not isinstance(source, (Line, )):
                continue
            items.update(source._all_items(target=target))
        return items

    @property
    def all_items_produced(self):
        return self._all_items()

    @property
    def all_items_target(self):
        return self._all_items(target=True)

    @property
    def miner_placements(self):
        """
        {"miner": {"ore": count, "other_ore": count}, "otherminer": {"ore": count}}
        """
        pass


class Item:
    state = "solid"  # solid, liquid
    is_base_resource = False
    produced_by_recipes = []

    def __str__(self):
        return self.__class__.__name__

    def creation_pipeline(
        self,
        desired_output_rate=1,
        crafting_items_available=(
            "AssemblingMachine1",
            "BurnerMiningDrill",
            "StoneFurnace",
        ),
        burnable_fuel="Coal",
    ):
        """Specifies the numbers of equipment needed to produce the
        `desired_output_rate` (per second) from base resources
        """
        # if desired_output_item is None:
        #     desired_output_item = self.outputs.keys()[0]
        # logging.debug(f"creation_pipeline of {self}")
        recipe = self.produced_by_recipes[0]
        # logging.debug(f">> using recipe {recipe}")
        # _creation_pipeline = []
        # how am I made?
        selected_crafter = None
        for _crafter in recipe.made_in:
            if _crafter not in crafting_items_available:
                continue
            crafter = _item_objects[_crafter]
            if selected_crafter is None:
                selected_crafter = crafter
                continue
            if crafter.base_speed > selected_crafter.base_speed:
                selected_crafter = crafter
        crafter = selected_crafter
        if crafter is None:
            logging.error(f"No crafter found for item {self}")
        # logging.debug(f">> crafter selected {crafter}")
        pipeline_element = {
            "item": str(self),
            "target_output_rate": desired_output_rate,
            "crafter_item": str(crafter),
            "recipe": recipe,
            "sources": [],
        }
        unit_craft_time = recipe.crafting_time / crafter.speed  # seconds / item
        craft_quantity = recipe.outputs[str(self)]
        craft_rate = (craft_quantity / unit_craft_time) * (1 + crafter.productivity)
        logging.debug(f"item {str(self)} :: unit craft rate {1/unit_craft_time} :: {str(crafter)}")
        crafters_required = ceil(desired_output_rate / craft_rate)
        actual_output_rate = crafters_required * craft_rate
        pipeline_element.update(
            {"crafter_count": crafters_required, "output_rate": actual_output_rate,}
        )
        power_consumption = crafters_required * crafter.consumption
        # 1000 kW = 1 MJ / s
        if crafter.consumes == "burnable":
            fuel_item = _item_objects[burnable_fuel]
            fuel_value = fuel_item.fuel_value  # MJ
            pipeline_element.update(
                {
                    "burnable_fuel": str(fuel_item),
                    "fuel_burn_rate": power_consumption / (1000 * fuel_value),
                }
            )
        else:
            pipeline_element.update(
                {"electricity_consumption": power_consumption,}
            )
        # deal with inserters
        inserter_consumption = crafters_required * crafter.inserter_count * crafter.inserter_consumption
        pipeline_element.update({"electricity_consumption": inserter_consumption})

        assert selected_crafter, f"No appropriate crafter available for {recipe}"
        for _input, qty in recipe.inputs.items():
            # find (best) recipe for each input
            input_item = _item_objects[_input]
            needed_rate = desired_output_rate / craft_quantity * qty
            pipeline_element["sources"].append(
                input_item.creation_pipeline(
                    desired_output_rate=needed_rate,
                    crafting_items_available=crafting_items_available,
                )
            )
        line = Line(**pipeline_element)

        return line


recipes = dict(
    [(name, cls()) for name, cls in _recipes.__dict__.items() if isinstance(cls, type)]
)

recipes_by_item_produced = {}
for name, recipe in recipes.items():
    for item_produced in recipe.outputs.keys():
        recipes_by_item_produced.setdefault(item_produced, []).append(recipe)

for name, extra_bases, _item in item_defs:
    _item.update({"produced_by_recipes": recipes_by_item_produced.get(name, [])})
    # [Item].append('something')
    _item_objects[name] = type(name, (Item, *extra_bases), _item)()


class Items:
    def __getattr__(self, attr):
        try:
            return _item_objects[attr]
        except KeyError:
            raise KeyError(f"There is no item called {attr!r}")


items = Items()

if __name__ == "__main__":
    # print("\n".join(items.keys()))

    red_pack = items.AutomationSciencePack.creation_pipeline(desired_output_rate=5)
    print(red_pack)
    print(red_pack.all_crafters)
    print(red_pack.total_electricity_demand)
    print(red_pack.total_burnables)
    ce = items.CliffExplosives.creation_pipeline(
        desired_output_rate=0.75,
        crafting_items_available=(
            "AssemblingMachine2",
            "SteelFurnace",
            "ElectricMiningDrill",
            "ChemicalPlant",
            "OilRefinery",
            "Pumpjack",
            "OffshorePump",
        ),
    )
    print(ce)
    print(ce.all_items_target)
    print(ce.all_items_produced)
    electric_pole = items.SmallElectricPole.creation_pipeline(
        desired_output_rate=1,
        crafting_items_available=(
            "AssemblingMachine2",
            "SteelFurnace",
            "ElectricMiningDrill",
            "Axe",
        ),
    )
    print(electric_pole)
    # removed = electric_pole.remove_source("Wood")
    # print(removed)
    # print(electric_pole)
    print(
        items.Electricity.creation_pipeline(
            desired_output_rate=1210000,
            crafting_items_available=("SteamEngine", "Boiler", "OffshorePump"),
        )
    )
