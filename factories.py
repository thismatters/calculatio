import logging

from items import items, BusLine
from utils import AdditiveUpdateDict


class Factory:
    crafting_items_available = (
        "AssemblingMachine1",
        "BurnerMiningDrill",
        # "ElectricMiningDrill",
        "StoneFurnace",
        "Boiler",
        "SteamEngine",
        "OffshorePump",
    )
    desired_production_rates = {
        "AutomationSciencePack": 5,
        "LogisticSciencePack": 5,
    }
    bus_items = [
        "IronPlate",
        "CopperPlate",
        "Stone",
        "StoneBrick",
        "SteelPlate",
        "PetroleumGas",
        "PlasticBar",
        "SulfuricAcid",
        "Lubricant",
        "EngineUnit",
        "ElectronicCircuit",
        "AdvancedCircuit",
        "ProcessingUnit",
    ]
    crafted_item_counts = {}
    module = None

    def __init__(
        self,
        crafting_items_available=None,
        desired_production_rates=None,
        module=None,
        bus_items=None,
        crafted_item_counts=None,
    ):
        if crafting_items_available:
            self.crafting_items_available = crafting_items_available
        if desired_production_rates:
            self.desired_production_rates = desired_production_rates
        if module:
            self.module = module
        if bus_items:
            self.bus_items = bus_items
        if crafted_item_counts:
            self.crafted_item_counts = crafted_item_counts
        self.burnable_fuels = AdditiveUpdateDict()
        self.product_production_lines = []
        self.bus_production_lines = []
        self.electricity_production_lines = []
        self.burnable_production_lines = []
        self.product_electricity_demand = 0
        self.electricity_production = 0
        self.crafting_item_counts = AdditiveUpdateDict()
        self.miner_placements = AdditiveUpdateDict()
        self.base_resources = AdditiveUpdateDict()
        self._module = None
        if self.module is not None:
            self._module = getattr(items, self.module)
        self.satisfy_production_requirements()
        self.reconcile_electricity_usage()
        self.split_bus_production()
        self.tally_equipment()
        self.tally_base_resources()

    @property
    def totals(self):
        total_fields = (
            "burnable_fuels",
            "electricity_demand",
            "crafting_item_counts",
            "miner_placements",
            "items_produced",
            "production_targets",
        )
        return {f: getattr(self, f) for f in total_fields}

    @property
    def lines(self):
        return (
            self.product_production_lines
            + self.bus_production_lines
            + self.electricity_production_lines
            + self.burnable_production_lines
        )

    def satisfy_production_requirements(self):
        for _item, production_rate in self.desired_production_rates.items():
            production_line = getattr(items, _item).creation_pipeline(
                desired_output_rate=production_rate,
                crafting_items_available=self.crafting_items_available,
                module=self._module,
            )
            self.product_production_lines.append(production_line)

    def tally_equipment(self):
        for line in self.lines:
            self.crafting_item_counts.update(line.all_crafters)

    def tally_base_resources(self):
        to_craft = AdditiveUpdateDict()
        to_craft.update(self.crafting_item_counts)
        to_craft.update(self.crafted_item_counts)
        for _item, qty in to_craft.items():
            item = getattr(items, _item)
            self.base_resources.update(item.base_resource_requirements(qty=qty))

    @property
    def items_produced(self):
        produced = AdditiveUpdateDict()
        for line in self.product_production_lines + self.burnable_production_lines:
            produced.update(line.all_items_produced)
        return produced

    @property
    def production_targets(self):
        target = AdditiveUpdateDict()
        for line in self.product_production_lines + self.burnable_production_lines:
            target.update(line.all_items_target)
        return target

    @property
    def electricity_demand(self):
        demand = self.product_electricity_demand
        for line in self.burnable_production_lines + self.electricity_production_lines:
            demand += line.total_electricity_demand
        return demand

    def _electic_production(self):
        production = 0
        for line in self.electricity_production_lines:
            production = line.total_electricity_production
        return production

    def _electric_deficit(self):
        return self.electricity_demand - self._electic_production()

    def _satisfy_electricity_requirements(self):
        deficit = self._electric_deficit()
        count = 0
        while deficit > 0:
            self.electricity_production_lines.append(
                getattr(items, "Electricity").creation_pipeline(
                    desired_output_rate=deficit,
                    crafting_items_available=self.crafting_items_available,
                    module=self._module,
                )
            )
            deficit = self._electric_deficit()

    def _burnable_demand(self, *, burnable_fuel):
        try:
            base = self.burnable_fuels[burnable_fuel]
        except KeyError:
            base = 0
        supplimental_burnables = AdditiveUpdateDict()
        for line in self.burnable_production_lines + self.electricity_production_lines:
            supplimental_burnables.update(line.total_burnables)
        try:
            supplimental = supplimental_burnables[burnable_fuel]
        except KeyError:
            supplimental = 0
        return base + supplimental

    def _burnable_production(self, *, burnable_fuel):
        production = 0
        for line in self.burnable_production_lines:
            if line.item == burnable_fuel:
                production += line.output_rate
        return production

    def _burnable_deficit(self, **kwargs):
        return self._burnable_demand(**kwargs) - self._burnable_production(**kwargs)

    def _satisfy_burnable_requirements(self):
        # iterate on burnable lines until they satisfy the burnable_fuels
        #  requirements as well as their own secondary requirements
        for burnable_fuel in self.burnable_fuels:
            deficit = self._burnable_deficit(burnable_fuel=burnable_fuel)
            while deficit > 0:
                self.burnable_production_lines.append(
                    getattr(items, burnable_fuel).creation_pipeline(
                        desired_output_rate=deficit,
                        crafting_items_available=self.crafting_items_available,
                        module=self._module,
                    )
                )
                deficit = self._burnable_deficit(burnable_fuel=burnable_fuel)

    def _consolidate_electricity_production(self):
        if len(self.electricity_production_lines) > 1:
            self.electricity_production_lines = [
                getattr(items, "Electricity").creation_pipeline(
                    desired_output_rate=self.electricity_demand,
                    crafting_items_available=self.crafting_items_available,
                    module=self._module,
                )
            ]

    def _consolidate_burnable_production(self):
        if len(self.burnable_production_lines) > 1:
            burnables = set()
            for line in self.burnable_production_lines:
                burnables.add(line.item)
            for item in burnables:
                self.burnable_production_lines = [
                    getattr(items, item).creation_pipeline(
                        desired_output_rate=self._burnable_demand(burnable_fuel=item),
                        crafting_items_available=self.crafting_items_available,
                        module=self._module,
                    )
                ]

    def reconcile_electricity_usage(self):
        """Determine electricity consumption and generation lines"""
        for line in self.product_production_lines + self.bus_production_lines:
            self.product_electricity_demand += line.total_electricity_demand
            self.burnable_fuels.update(line.total_burnables)

        last_count = -1
        count = len(self.burnable_production_lines) + len(
            self.electricity_production_lines
        )

        while last_count < count:
            # calculate power reqs
            self._satisfy_electricity_requirements()
            # calculate burnables to provide power
            self._satisfy_burnable_requirements()
            last_count = count
            count = len(self.burnable_production_lines) + len(
                self.electricity_production_lines
            )
            # repeat if necessary
        # flatten the burnable and elecricity production lines
        self._consolidate_electricity_production()
        self._consolidate_burnable_production()

    def split_bus_production(self):
        """Relegate bus item production to bus lines"""
        self.bus_production_lines = [
            l for l in self.product_production_lines if l.item in self.bus_items
        ]
        self.product_production_lines = [
            l for l in self.product_production_lines if l.item not in self.bus_items
        ]
        for bus_item in self.bus_items:
            # logging.debug(f"trying to remove bus item {bus_item}")
            for line in self.product_production_lines:
                # logging.debug(f">> checking line {line.item}")
                # logging.debug(f">> line has items {line.all_items_produced}")
                if bus_item in line.all_items_produced:
                    # logging.debug(f">>>> here")
                    removed = line.remove_source(bus_item)
                    if removed:
                        self.bus_production_lines.extend(removed)
        self.consolidate_bus_lines()

    def consolidate_bus_lines(self):
        """make singular lines for each bus item"""
        busses = {i: 0 for i in self.bus_items}
        for line in self.bus_production_lines:
            busses[line.item] += line.target_output_rate
        new_bus_production_lines = []
        for item, target in busses.items():
            if target == 0:
                continue
            new_bus_line = getattr(items, item).creation_pipeline(
                desired_output_rate=target,
                crafting_items_available=self.crafting_items_available,
                module=self._module,
            )
            for bus_item in self.bus_items:
                if bus_item in new_bus_line.all_items_produced:
                    new_bus_line.remove_source(bus_item)
            new_bus_production_lines.append(new_bus_line)
        self.bus_production_lines = new_bus_production_lines


class Progression:
    bus_ordering = [
        "Electricity",
        "Coal",
        "IronPlate",
        "CopperPlate",
        "ElectronicCircuit",
        "SteelPlate",
        "PetroleumGas",
        "PlasticBar",
        "AdvancedCircuit",
        "EngineUnit",
        "Stone",
        "StoneBrick",
        "SulfuricAcid",
        "Lubricant",
        "ProcessingUnit",
    ]

    def __init__(self):
        self.busses = {}
        self._bus_ordering = self.bus_ordering.copy()
        # busses = {
        #     "Electricity": {
        #         ("OffshorePump", "WaterExtraction"): {0: 1, 1: 1, 2: 4},
        #         ("Boiler", "BoilerSteamGeneration"): {0: 1, 1: 1, 2: 4},
        #         ...
        #     },
        #     "IronPlate": {
        #         ("ElectricMiningDrill", "IronOre"): {0: 16, ...}
        #     },
        # }
        self._process()

    def _process_bus_sources(self, *, sources, top_level_line, factory_idx):
        for source in sources:
            if isinstance(source, (BusLine,)):
                continue
            self.busses[top_level_line.item].setdefault(
                (source.crafter_item, str(source.recipe)), {}
            ).update({factory_idx: source.crafter_count})
            self._process_bus_sources(
                sources=source.sources,
                top_level_line=top_level_line,
                factory_idx=factory_idx,
            )

    def _process_busses(self, *, factory_idx, factory):
        lines = (
            factory.bus_production_lines
            + factory.electricity_production_lines
            + factory.burnable_production_lines
        )
        for line in lines:
            logging.debug(f"examining line {line.item}")
            if line.item not in self._bus_ordering:
                self._bus_ordering.append(line.item)
            self.busses.setdefault(line.item, {})
            self.busses[line.item].setdefault(
                (line.crafter_item, str(line.recipe)), {}
            ).update({factory_idx: line.crafter_count})
            self._process_bus_sources(
                sources=line.sources, top_level_line=line, factory_idx=factory_idx
            )

    def _process_production(self, *, factory_idx, factory):
        pass

    def _process(self):
        for idx, factory in enumerate(self.factory_steps):
            self._process_busses(factory_idx=idx, factory=factory)
            self._process_production(factory_idx=idx, factory=factory)

    def busses_to_html(self):
        # return self.busses
        table = "<table>\n"
        table += "  <tr><th>Bus</th><th>Equipment</th><th>Recipe</th>"
        for idx, factory in enumerate(self.factory_steps, 1):
            table += f"<th>Stage {idx}</th>"
        table += "</tr>\n"
        for bus_item in self._bus_ordering:
            if bus_item in self.busses:
                first = True
                _bus = self.busses[bus_item]
                _len = len(_bus.keys())
                for equipment, spread in _bus.items():
                    table += "  <tr>"
                    if first:
                        first = False
                        table += f"<td rowspan={_len}>{bus_item}</td>"
                    table += f"<td>{equipment[0]}</td><td>{equipment[1]}</td>"
                    for idx in range(len(self.factory_steps)):
                        table += f"<td>"
                        if idx in spread:
                            table += f"{spread[idx]}"
                        table += f"</td>"
                    table += "</tr>\n"
        table += "</table>"
        return table

    def production_to_html(self):
        pass


class PreFactory(Factory):
    crafting_items_available = (
        "PlayerCrafter",
        "PlayerMiner",
        "StoneFurnace",
    )
    desired_production_rates = {
        "AutomationSciencePack": 10,
        "BurnerMiningDrill": 16,
        "StoneFurnace": 8,
    }


class EarlyFactory(Factory):
    crafting_items_available = (
        "StoneFurnace",
        "ElectricMiningDrill",
        "AssemblingMachine1",
        "Boiler",
        "SteamEngine",
        "OffshorePump",
    )


class MiddleFactory(Factory):
    crafting_items_available = (
        "SteelFurnace",
        "ElectricMiningDrill",
        "AssemblingMachine2",
        "Pumpjack",
        "ChemicalPlant",
        "OilRefinery",
        "Boiler",
        "SteamEngine",
        "OffshorePump",
    )


class SpeedRunProgression(Progression):
    factory_steps = [
        EarlyFactory(  # Red Bottles
            desired_production_rates={"AutomationSciencePack": 1,}
        ),
        EarlyFactory(  # +Green Bottles
            desired_production_rates={
                "AutomationSciencePack": 1,
                "LogisticSciencePack": 1,
            }
        ),
        MiddleFactory(  # +Blue Bottles
            desired_production_rates={
                "AutomationSciencePack": 2,
                "LogisticSciencePack": 2,
                "ChemicalSciencePack": 2,
            }
        ),
        MiddleFactory(  # +Purple Bottles
            desired_production_rates={
                "AutomationSciencePack": 3,
                "LogisticSciencePack": 3,
                "ChemicalSciencePack": 3,
                "ProductionSciencePack": 3,
            },
            module="SpeedModule1",
        ),
        MiddleFactory(  # +Yellow Bottles
            desired_production_rates={
                "AutomationSciencePack": 3,
                "LogisticSciencePack": 3,
                "ChemicalSciencePack": 3,
                "ProductionSciencePack": 3,
                "UtilitySciencePack": 3,
            },
            crafted_item_counts={
                "AutomationSciencePack": 6300,
                "LogisticSciencePack": 6115,
                "ChemicalSciencePack": 4050,
                "ProductionSciencePack": 2100,
                "UtilitySciencePack": 1300,
                "TransportBelt": 10000,
                "SmallElectricPole": 5000,
            },
        ),
    ]
