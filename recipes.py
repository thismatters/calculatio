class Recipe:
    inputs = {}
    crafting_time = 0
    made_in = []
    outputs = {}

    def __str__(self):
        return self.__class__.__name__


class ExtractionRecipe(Recipe):
    crafting_time = 1  # ???
    made_in = ["BurnerMiningDrill", "ElectricMiningDrill", "PlayerMiner"]


class SmeltingRecipe(Recipe):
    crafting_time = 3.2
    made_in = ["StoneFurnace", "SteelFurnace", "ElectricFurnace"]


class BasicCraftingRecipe(Recipe):
    made_in = ["PlayerCrafter", "AssemblingMachine1", "AssemblingMachine2", "AssemblingMachine3"]


class LiquidCraftingRecipe(Recipe):
    made_in = ["AssemblingMachine2", "AssemblingMachine3"]


class RefiningRecipe(Recipe):
    made_in = ["OilRefinery"]


class ChemicalRecipe(Recipe):
    made_in = ["ChemicalPlant"]


class WoodExtraction(ExtractionRecipe):
    made_in = ["Axe", "PlayerMiner"]
    outputs = {"Wood": 1}


class IronOreExtraction(ExtractionRecipe):
    outputs = {"IronOre": 1}


class CopperOreExtraction(ExtractionRecipe):
    outputs = {"CopperOre": 1}


class CoalExtraction(ExtractionRecipe):
    outputs = {"Coal": 1}


class StoneExtraction(ExtractionRecipe):
    outputs = {"Stone": 1}


class WaterExtraction(ExtractionRecipe):
    made_in = ["OffshorePump"]
    outputs = {"Water": 1200}


class CrudeOilExtraction(ExtractionRecipe):
    outputs = {"CrudeOil": 1}
    made_in = ["Pumpjack"]


class UraniumOreExtraction(ExtractionRecipe):
    outputs = {"UraniumOre": 1}
    inputs = {"SulfuricAcid": 200}
    made_in = ["ElectricMiningDrill"]


class SulfuricAcidRecipe(ChemicalRecipe):
    crafting_time = 1
    inputs = {"IronPlate": 1, "Sulfur": 5, "Water": 100}
    outputs = {"SulfuricAcid": 50}


class BasicOilRecipe(RefiningRecipe):
    crafting_time = 5
    inputs = {"CrudeOil": 100}
    outputs = {"PetroleumGas": 45}


class AdvancedOilRecipe(RefiningRecipe):
    crafting_time = 5
    inputs = {"CrudeOil": 100, "Water": 50}
    outputs = {"PetroleumGas": 55, "HeavyOil": 25, "LightOil": 45}


class HeavyOilToLightOilCrackingRecipe(ChemicalRecipe):
    crafting_time = 2
    inputs = {"HeavyOil": 40, "Water": 30}
    outputs = {"LightOil": 30}


class LightOilToPetroleumCrackingRecipe(ChemicalRecipe):
    crafting_time = 2
    inputs = {"LightOil": 30, "Water": 30}
    outputs = {"PetroleumGas": 20}


class LightOilToSolidFuelRecipe(ChemicalRecipe):
    crafting_time = 2
    inputs = {"LightOil": 10}
    outputs = {"SolidFuel": 1}


class LubricantRecipe(ChemicalRecipe):
    crafting_time = 1
    inputs = {"HeavyOil": 10}
    outputs = {"Lubricant": 10}


class IronPlateRecipe(SmeltingRecipe):
    inputs = {"IronOre": 1}
    outputs = {"IronPlate": 1}


class CopperPlateRecipe(SmeltingRecipe):
    inputs = {"CopperOre": 1}
    outputs = {"CopperPlate": 1}


class SteelPlateRecipe(SmeltingRecipe):
    inputs = {"IronPlate": 5}
    outputs = {"SteelPlate": 1}


class PlasticBarRecipe(ChemicalRecipe):
    crafting_time = 1
    inputs = {"Coal": 1, "PetroleumGas": 20}
    outputs = {"PlasticBar": 2}


class SulfurRecipe(ChemicalRecipe):
    crafting_time = 1
    inputs = {"Water": 30, "PetroleumGas": 20}
    outputs = {"Sulfur": 2}


class BatteryRecipe(ChemicalRecipe):
    crafting_time = 4
    inputs = {"IronPlate": 1, "CopperPlate": 1, "SulfuricAcid": 20}
    outputs = {"Battery": 1}


class ExplosivesRecipe(ChemicalRecipe):
    crafting_time = 4
    inputs = {"Coal": 1, "Sulfur": 1, "Water": 10}
    outputs = {"Explosives": 2}


class CopperCableRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"CopperPlate": 1}
    outputs = {"CopperCable": 2}


class IronStickRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 1}
    outputs = {"IronStick": 2}


class IronGearWheelRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 2}
    outputs = {"IronGearWheel": 1}


class EmptyBarrelRecipe(BasicCraftingRecipe):
    crafting_time = 1
    inputs = {"SteelPlate": 1}
    outputs = {"EmptyBarrel": 1}


class ElectronicCircuitRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 1, "CopperCable": 3}
    outputs = {"ElectronicCircuit": 1}


class AdvancedCircuitRecipe(BasicCraftingRecipe):
    crafting_time = 6
    inputs = {"PlasticBar": 2, "CopperCable": 4, "ElectronicCircuit": 2}
    outputs = {"AdvancedCircuit": 1}


class ProcessingUnitRecipe(LiquidCraftingRecipe):
    crafting_time = 10
    inputs = {"SulfuricAcid": 2, "ElectronicCircuit": 2, "AdvancedCircuit": 2}
    outputs = {"ProcessingUnit": 1}


class EngineUnitRecipe(BasicCraftingRecipe):
    crafting_time = 10
    inputs = {"SteelPlate": 1, "IronGearWheel": 1, "Pipe": 2}
    outputs = {"EngineUnit": 1}


class ElectricEngineUnitRecipe(LiquidCraftingRecipe):
    crafting_time = 10
    inputs = {"ElectronicCircuit": 2, "EngineUnit": 1, "Lubricant": 15}
    outputs = {"ElectricEngineUnit": 1}


class FlyingRoboticFrameRecipe(BasicCraftingRecipe):
    crafting_time = 20
    inputs = (
        {
            "SteelPlate": 1,
            "Battery": 2,
            "ElectronicCircuit": 3,
            "ElectricEngineUnit": 1,
        },
    )
    outputs = {"FlyingRoboticFrame": 1}


class SatelliteRecipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = (
        {
            "ProcessingUnit": 100,
            "LowDensityStructure": 100,
            "RocketFuel": 50,
            "SolarPanel": 100,
            "Accumulator": 100,
            "Radar": 5,
        },
    )
    outputs = {"Satellite": 1}


class RocketControlUnitRecipe(BasicCraftingRecipe):
    crafting_time = 30
    inputs = ({"ProcessingUnit": 1, "SpeedModule1": 1},)
    outputs = {"RocketControlUnit": 1}


class LowDensityStructureRecipe(BasicCraftingRecipe):
    crafting_time = 20
    inputs = ({"CopperPlate": 20, "SteelPlate": 2, "PlasticBar": 5},)
    outputs = {"LowDensityStructure": 1}


class RocketFuelRecipe(LiquidCraftingRecipe):
    crafting_time = 30
    inputs = {"SolidFuel": 10, "LightOil": 10}
    outputs = {"RocketFuel": 1}


class AutomationSciencePackRecipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"CopperPlate": 1, "IronGearWheel": 1}
    outputs = {"AutomationSciencePack": 1}


class LogisticSciencePackRecipe(BasicCraftingRecipe):
    crafting_time = 6
    inputs = {"TransportBelt": 1, "Inserter": 1}
    outputs = {"LogisticSciencePack": 1}


class MilitarySciencePackRecipe(BasicCraftingRecipe):
    crafting_time = 10
    inputs = {"PiercingRoundsMagazine": 1, "Grenade": 1, "Wall": 2}
    outputs = {"MilitarySciencePack": 2}


class ChemicalSciencePackRecipe(BasicCraftingRecipe):
    crafting_time = 24
    inputs = {"Sulfur": 1, "AdvancedCircuit": 3, "EngineUnit": 2}
    outputs = {"ChemicalSciencePack": 2}


class ProductionSciencePackRecipe(BasicCraftingRecipe):
    crafting_time = 21
    inputs = {"Rail": 30, "ElectricFurnace": 1, "ProductivityModule1": 1}
    outputs = {"ProductionSciencePack": 3}


class UtilitySciencePackRecipe(BasicCraftingRecipe):
    crafting_time = 21
    inputs = {"ProcessingUnit": 2, "FlyingRoboticFrame": 1, "LowDensityStructure": 3}
    outputs = {"UtilitySciencePack": 3}


class RepairPackRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronGearWheel": 2, "ElectronicCircuit": 2}
    outputs = {"RepairPack": 1}


class BoilerRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"Pipe": 4, "StoneFurnace": 1}
    outputs = {"Boiler": 1}


class SteamEngineRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 10, "IronGearWheel": 8, "Pipe": 5}
    outputs = {"SteamEngine": 1}


class SolarPanelRecipe(BasicCraftingRecipe):
    crafting_time = 10
    inputs = {"CopperPlate": 5, "SteelPlate": 5, "ElectronicCircuit": 15}
    outputs = {"SolarPanel": 1}


class AccumulatorRecipe(BasicCraftingRecipe):
    crafting_time = 10
    inputs = {"IronPlate": 2, "Battery": 5}
    outputs = {"Accumulator": 1}


class BurnerMiningDrillRecipe(BasicCraftingRecipe):
    crafting_time = 2
    inputs = {"IronPlate": 3, "IronGearWheel": 3, "StoneFurnace": 1}
    outputs = {"BurnerMiningDrill": 1}


class ElectricMiningDrillRecipe(BasicCraftingRecipe):
    crafting_time = 2
    inputs = {"IronPlate": 10, "IronGearWheel": 5, "ElectronicCircuit": 3}
    outputs = {"ElectricMiningDrill": 1}


class OffshorePumpRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronGearWheel": 1, "ElectronicCircuit": 2, "Pipe": 1}
    outputs = {"OffshorePump": 1}


class PumpjackRecipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"SteelPlate": 5, "IronGearWheel": 10, "ElectronicCircuit": 2, "Pipe": 10}
    outputs = {"Pumpjack": 1}


class StoneFurnaceRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"Stone": 5}
    outputs = {"StoneFurnace": 1}


class SteelFurnaceRecipe(BasicCraftingRecipe):
    crafting_time = 3
    inputs = {"SteelPlate": 6, "StoneBrick": 10}
    outputs = {"SteelFurnace": 1}


class ElectricFurnaceRecipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"SteelPlate": 10, "AdvancedCircuit": 5, "StoneBrick": 10}
    outputs = {"ElectricFurnace": 1}


class AssemblingMachine1Recipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 9, "IronGearWheel": 5, "ElectronicCircuit": 3}
    outputs = {"AssemblingMachine1": 1}


class AssemblingMachine2Recipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {
        "SteelPlate": 2,
        "IronGearWheel": 5,
        "ElectronicCircuit": 3,
        "AssemblingMachine1": 1,
    }
    outputs = {"AssemblingMachine2": 1}


class AssemblingMachine3Recipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"AssemblingMachine2": 2, "SpeedModule1": 4}
    outputs = {"AssemblingMachine3": 1}


class OilRefineryRecipe(BasicCraftingRecipe):
    crafting_time = 8
    inputs = {
        "SteelPlate": 15,
        "IronGearWheel": 10,
        "ElectronicCircuit": 10,
        "Pipe": 10,
        "StoneBrick": 10,
    }
    outputs = {"OilRefinery": 1}


class ChemicalPlantRecipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"SteelPlate": 5, "IronGearWheel": 5, "ElectronicCircuit": 5, "Pipe": 5}
    outputs = {"ChemicalPlant": 1}


class SpeedModule1Recipe(BasicCraftingRecipe):
    crafting_time = 15
    inputs = {"ElectronicCircuit": 5, "AdvancedCircuit": 5}
    outputs = {"SpeedModule1": 1}


class SpeedModule2Recipe(BasicCraftingRecipe):
    crafting_time = 30
    inputs = {"AdvancedCircuit": 5, "ProcessingUnit": 5, "SpeedModule1": 4}
    outputs = {"SpeedModule2": 1}


class SpeedModule3Recipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"AdvancedCircuit": 5, "ProcessingUnit": 5, "SpeedModule2": 5}
    outputs = {"SpeedModule3": 1}


class EfficiencyModule1Recipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"ElectronicCircuit": 5, "AdvancedCircuit": 5}
    outputs = {"EfficiencyModule1": 1}


class EfficiencyModule2Recipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"AdvancedCircuit": 5, "ProcessingUnit": 5, "EfficiencyModule1": 4}
    outputs = {"EfficiencyModule2": 1}


class EfficiencyModule3Recipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"AdvancedCircuit": 5, "ProcessingUnit": 5, "EfficiencyModule2": 5}
    outputs = {"EfficiencyModule3": 1}


class ProductvityModule1Recipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"ElectronicCircuit": 5, "AdvancedCircuit": 5}
    outputs = {"ProductvityModule1": 1}


class ProductvityModule2Recipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"AdvancedCircuit": 5, "ProcessingUnit": 5, "ProductivityModule1": 4}
    outputs = {"ProductvityModule2": 1}


class ProductvityModule3Recipe(BasicCraftingRecipe):
    crafting_time = 5
    inputs = {"AdvancedCircuit": 5, "ProcessingUnit": 5, "ProductivityModule2": 5}
    outputs = {"ProductvityModule3": 1}


class WoodenChestRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"Wood": 2}
    outputs = {"WoodenChest": 1}


class IronChestRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 8}
    outputs = {"IronChest": 1}


class SteelChestRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"SteelPlate": 8}
    outputs = {"SteelChest": 1}


class StorageTankRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 8}
    outputs = {"IronChest": 1}


class TransportBeltRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 1, "IronGearWheel": 1}
    outputs = {"TransportBelt": 1}


class FastTransportBeltRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronGearWheel": 5, "TransportBelt": 1}
    outputs = {"FastTransportBelt": 1}


class ExpressTransportBeltRecipe(LiquidCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronGearWheel": 10, "FastTransportBelt": 1, "Lubricant": 20}
    outputs = {"IronChest": 1}


class UndergroundBeltRecipe(BasicCraftingRecipe):
    crafting_time = 1
    inputs = {"IronPlate": 10, "TransportBelt": 5}
    outputs = {"UndergroundBelt": 2}


class FastUndergroundBeltRecipe(BasicCraftingRecipe):
    crafting_time = 2
    inputs = {"IronGearWheel": 40, "UndergroundBelt": 2}
    outputs = {"FastUndergroundBelt": 2}


class ExpressUndergroundBeltRecipe(LiquidCraftingRecipe):
    crafting_time = 2
    inputs = {"IronGearWheel": 80, "FastUndergroundBelt": 2, "Lubricant": 40}
    outputs = {"ExpressUndergroundBelt": 2}


class SplitterRecipe(BasicCraftingRecipe):
    crafting_time = 1
    inputs = {"IronPlate": 5, "ElectronicCircuit": 5, "TransportBelt": 4}
    outputs = {"Splitter": 1}


class FastSplitterRecipe(BasicCraftingRecipe):
    crafting_time = 2
    inputs = {"IronGearWheel": 10, "ElectronicCircuit": 10, "Splitter": 1}
    outputs = {"FastSplitter": 1}


class ExpressSplitterRecipe(LiquidCraftingRecipe):
    crafting_time = 2
    inputs = {
        "IronGearWheel": 10,
        "AdvancedCircuit": 10,
        "FastSplitter": 1,
        "Lubricant": 80,
    }
    outputs = {"ExpressSplitter": 1}


class BurnerInserterRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 1, "IronGearWheel": 1}
    outputs = {"BurnerInserter": 1}


class InserterRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 1, "IronGearWheel": 1, "ElectronicCircuit": 1}
    outputs = {"Inserter": 1}


class LongHandedInserterRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 1, "IronGearWheel": 1, "Inserter": 1}
    outputs = {"LongHandedInserter": 1}


class FastInserterRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 2, "ElectronicCircuit": 2, "Inserter": 1}
    outputs = {"FastInserter": 1}


class FilterInserterRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"ElectronicCircuit": 4, "FastInserter": 1}
    outputs = {"FilterInserter": 1}


class StackInserterRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {
        "IronGearWheel": 1,
        "ElectronicCircuit": 15,
        "AdvancedCircuit": 1,
        "FastInserter": 1,
    }
    outputs = {"StackInserter": 1}


class StackFilterInserterRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"ElectronicCircuit": 5, "StackInserter": 1}
    outputs = {"StackFilterInserter": 1}


class SmallElectricPoleRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"Wood": 1, "CopperCable": 2}
    outputs = {"SmallElectricPole": 2}


class MediumElectricPoleRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"CopperPlate": 2, "SteelPlate": 2, "IronStick": 4}
    outputs = {"MediumElectricPole": 1}


class BigElectricPoleRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"CopperPlate": 5, "SteelPlate": 5, "IronStick": 8}
    outputs = {"BigElectricPole": 1}


class SubstationRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"CopperPlate": 5, "SteelPlate": 10, "AdvancedCircuit": 5}
    outputs = {"Substation": 1}


class PipeRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 1}
    outputs = {"Pipe": 1}


class PipeToGroundRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"IronPlate": 5, "Pipe": 10}
    outputs = {"PipeToGround": 2}


class PumpRecipe(BasicCraftingRecipe):
    crafting_time = 2
    inputs = {"SteelPlate": 1, "EngineUnit": 1, "Pipe": 1}
    outputs = {"Pump": 1}


class RailRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"Stone": 1, "SteelPlate": 1, "IronStick": 1}
    outputs = {"Rail": 2}


# Ignoring the rest of the train stuff
# Ignoring the robotics stuff
# Ignoring the logic stuff


class StoneBrick(SmeltingRecipe):
    crafting_time = 3.2
    inputs = {"Stone": 2}
    outputs = {"StoneBrick": 1}


class ConcreteRecipe(LiquidCraftingRecipe):
    crafting_time = 10
    inputs = {"IronOre": 1, "StoneBrick": 5, "Water": 100}
    outputs = {"Concrete": 10}


class LandfillRecipe(BasicCraftingRecipe):
    crafting_time = 0.5
    inputs = {"Stone": 20}
    outputs = {"Landfill": 1}


class CliffExplosivesRecipe(BasicCraftingRecipe):
    crafting_time = 8
    inputs = {"Explosives": 10, "EmptyBarrel": 1, "Grenade": 1}
    outputs = {"CliffExplosives": 1}


class GrenadeRecipe(BasicCraftingRecipe):
    crafting_time = 8
    inputs = {"Coal": 10, "IronPlate": 5}
    outputs = {"Grenade": 1}


class SteamEngineGenerationRecipe(Recipe):
    crafting_time = 1
    inputs = {"Steam": 30}
    outputs = {"Electricity": 900}
    made_in = ("SteamEngine",)


class BoilerSteamGeneration(Recipe):
    crafting_time = 1
    inputs = {"Water": 60}
    outputs = {"Steam": 60}
    made_in = ("Boiler",)
