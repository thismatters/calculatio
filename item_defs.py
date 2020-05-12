class BaseItem:
    inserter_count = 0
    inserter_consumption = 20.11  # long inserter
    module_selection = None
    effect_slots = 0  # ea


class Crafter(BaseItem):
    base_speed = 1  # per second
    base_productivity = 0
    pollution = 0  # per minute
    max_consumption = 0  # kW
    min_consumption = 0  # kW
    consumes = "electricity"

    def _modifier(self, attr):
        if self.module_selection is None:
            return 1
        return (
            1 + getattr(self.module_selection, f"{attr}_increase") * self.effect_slots
        )

    @property
    def speed(self):
        return self.base_speed * self._modifier("speed")

    @property
    def productivity(self):
        modifier = 0
        return self.base_productivity * self._modifier("productivity")

    @property
    def consumption(self):
        modifier = 0
        return self.max_consumption * max(self._modifier("consumption"), 0.2)


class Smelter(Crafter):
    pass


class Miner(Crafter):
    base_productivity = 0


class Burnable:
    fuel_value = 0  # MJ


class Fissionable:
    fuel_value = 0  # MJ


class BoilerItem(Crafter):
    water_consumption = 6.0  # per second
    consumes = "burnable"
    max_consumption = 1800  # kW
    steam_output = 60  # per second


class SteamEngineItem(Crafter):
    steam_input = 30
    power_output = 900  # kW


class PumpingItem(BaseItem):
    speed = 1200
    consumption = 0
    productivity = 0
    consumes = None


class LabItem(BaseItem):
    max_consumption = 60


class Module:
    consumption_increase = 0
    speed_increase = 0
    productivity_increase = 0
    pollution_increase = 0


item_defs = [
    ("Axe", (Miner,), {}),
    ("IronOre", (), {"is_base_resource": True}),
    ("CopperOre", (), {"is_base_resource": True}),
    ("Coal", (Burnable,), {"is_base_resource": True, "fuel_value": 4}),
    ("Stone", (), {"is_base_resource": True}),
    ("Wood", (), {"is_base_resource": True}),
    ("UraniumOre", (), {"is_base_resource": True}),
    ("CrudeOil", (), {"state": "liquid", "is_base_resource": True}),
    ("Water", (), {"state": "liquid", "is_base_resource": True}),
    ("SulfuricAcid", (), {"state": "liquid"}),
    ("PetroleumGas", (), {"state": "liquid"}),
    ("HeavyOil", (), {"state": "liquid"}),
    ("LightOil", (), {"state": "liquid"}),
    ("Lubricant", (), {"state": "liquid"}),
    ("IronPlate", (), {}),
    ("CopperPlate", (), {}),
    ("SteelPlate", (), {}),
    ("PlasticBar", (), {}),
    ("Sulfur", (), {}),
    ("Battery", (), {}),
    ("Explosives", (), {}),
    ("CopperCable", (), {}),
    ("IronStick", (), {}),
    ("IronGearWheel", (), {}),
    ("EmptyBarrel", (), {}),
    ("ElectronicCircuit", (), {}),
    ("AdvancedCircuit", (), {}),
    ("ProcessingUnit", (), {}),
    ("EngineUnit", (), {}),
    ("ElectricEngineUnit", (), {}),
    ("FlyingRoboticFrame", (), {}),
    ("Satellite", (), {}),
    ("RocketControlUnit", (), {}),
    ("LowDensityStructure", (), {}),
    ("RocketSilo", (Crafter,), {}),
    ("RocketPart", (), {}),
    ("SolidFuel", (Burnable,), {"fuel_value": 100000}),
    ("RocketFuel", (Burnable,), {"fuel_value": 100}),
    ("NuclearFuel", (Burnable,), {"fuel_value": 1210}),
    ("UraniumFuelCell", (Fissionable,), {"fuel_value": 8000}),
    ("AutomationSciencePack", (), {}),  # red
    ("LogisticSciencePack", (), {}),  # green
    ("MilitarySciencePack", (), {}),  # grey
    ("ChemicalSciencePack", (), {}),  # blue
    ("ProductionSciencePack", (), {}),  # purple
    ("UtilitySciencePack", (), {}),  # yellow
    ("RepairPack", (), {}),
    ("Boiler", (BoilerItem,), {}),
    ("SteamEngine", (SteamEngineItem,), {}),
    ("Electricity", (), {}),
    ("Steam", (), {}),
    # ("SolarPanel", (), {}),
    # ("Accumulator", (), {}),
    # ("NuclearReactor", (), {}),
    # ("HeatPipe", (), {}),
    # ("HeatExchanger", (), {}),
    # ("SteamTurbine", (), {}),
    (
        "BurnerMiningDrill",
        (Miner,),
        {
            "base_speed": 0.25,
            "pollution": 12,
            "max_consumption": 150,
            "consumes": "burnable",
        },
    ),
    (
        "ElectricMiningDrill",
        (Miner,),
        {"base_speed": 0.5, "pollution": 10, "max_consumption": 90, "effect_slots": 3},
    ),
    ("OffshorePump", (PumpingItem,), {"speed": 1},),
    ("Pumpjack", (Miner,), {"base_speed": 1, "pollution": 10, "max_consumption": 90,}),
    ("PlayerCrafter", (Crafter,), {}),
    ("PlayerMiner", (Crafter,), {}),
    (
        "StoneFurnace",
        (Smelter,),
        {
            "base_speed": 1,
            "pollution": 2,
            "max_consumption": 90,
            "consumes": "burnable",
            "inserter_count": 3,
        },
    ),
    (
        "SteelFurnace",
        (Smelter,),
        {
            "base_speed": 2,
            "pollution": 4,
            "max_consumption": 90,
            "consumes": "burnable",
            "inserter_count": 3,
        },
    ),
    (
        "ElectricFurnace",
        (Smelter,),
        {
            "base_speed": 2,
            "pollution": 1,
            "max_consumption": 186,
            "min_consumption": 6,
            "inserter_count": 2,
            "effect_slots": 2,
        },
    ),
    (
        "AssemblingMachine1",
        (Crafter,),
        {
            "base_speed": 0.5,
            "pollution": 4,
            "min_consumption": 2.5,
            "max_consumption": 77.5,
            "inserter_count": 5,
        },
    ),
    (
        "AssemblingMachine2",
        (Crafter,),
        {
            "base_speed": 0.75,
            "pollution": 3,
            "min_consumption": 5,
            "max_consumption": 155,
            "inserter_count": 5,
            "effect_slots": 2,
        },
    ),
    (
        "AssemblingMachine3",
        (Crafter,),
        {
            "base_speed": 1.25,
            "pollution": 2,
            "min_consumption": 12.5,
            "max_consumption": 388,
            "inserter_count": 5,
            "effect_slots": 4,
        },
    ),
    (
        "OilRefinery",
        (Crafter,),
        {
            "base_speed": 1,
            "pollution": 6,
            "min_consumption": 14,
            "max_consumption": 434,
            "effect_slots": 3,
        },
    ),
    (
        "ChemicalPlant",
        (Crafter,),
        {
            "base_speed": 1,
            "pollution": 4,
            "min_consumption": 7,
            "max_consumption": 217,
            "inserter_count": 5,
            "effect_slots": 3,
        },
    ),
    (
        "Centrifuge",
        (Crafter,),
        {
            "base_speed": 1,
            "pollution": 4,
            "min_consumption": 11.67,
            "max_consumption": 362,
        },
    ),
    ("Lab", (LabItem,), {"inserter_count": 2}),
    # ("Beacon", (), {}),
    ("SpeedModule1", (Module,), {"consumption_increase": 0.5, "speed_increase": 0.2},),
    ("SpeedModule2", (Module,), {"consumption_increase": 0.6, "speed_increase": 0.3},),
    ("SpeedModule3", (Module,), {"consumption_increase": 0.7, "speed_increase": 0.5},),
    ("EfficiencyModule1", (Module,), {"consumption_increase": -0.3}),
    ("EfficiencyModule2", (Module,), {"consumption_increase": -0.4}),
    ("EfficiencyModule3", (Module,), {"consumption_increase": -0.5}),
    (
        "ProductivityModule1",
        (Module,),
        {
            "consumption_increase": 0.4,
            "speed_increase": -0.15,
            "pollution_increase": 0.05,
            "productivity_increase": 0.04,
        },
    ),
    (
        "ProductivityModule2",
        (Module,),
        {
            "consumption_increase": 0.6,
            "speed_increase": -0.15,
            "pollution_increase": 0.07,
            "productivity_increase": 0.06,
        },
    ),
    (
        "ProductivityModule3",
        (Module,),
        {
            "consumption_increase": 0.8,
            "speed_increase": -0.15,
            "pollution_increase": 0.1,
            "productivity_increase": 0.1,
        },
    ),
    ("WoodenChest", (), {}),
    ("IronChest", (), {}),
    ("SteelChest", (), {}),
    ("StorageTank", (), {}),
    ("TransportBelt", (), {}),
    ("FastTransportBelt", (), {}),
    ("ExpressTransportBelt", (), {}),
    ("UndergroundBelt", (), {}),
    ("FastUndergroundBelt", (), {}),
    ("ExpressUndergroundBelt", (), {}),
    ("Splitter", (), {}),
    ("FastSplitter", (), {}),
    ("ExpressSplitter", (), {}),
    ("BurnerInserter", (), {}),
    ("Inserter", (), {}),
    ("LongHandedInserter", (), {}),
    ("FastInserter", (), {}),
    ("FilterInserter", (), {}),
    ("StackInserter", (), {}),
    ("StackFilterInserter", (), {}),
    ("SmallElectricPole", (), {}),
    ("MediumElectricPole", (), {}),
    ("BigElectricPole", (), {}),
    ("Substation", (), {}),
    ("Pipe", (), {}),
    ("PipeToGround", (), {}),
    ("Pump", (PumpingItem,), {"speed": 12000, "max_consumption": 30}),
    ("Rail", (), {}),
    # don't care about train stuff broadly
    # don't care about robot stuff broadly
    # don't care about logic stuff broadly
    ("StoneBrick", (), {}),
    ("Concrete", (), {}),
    ("Landfill", (), {}),
    ("CliffExplosives", (), {}),
    ("Grenade", (), {}),
    # don't care about military stuff broadly
]
