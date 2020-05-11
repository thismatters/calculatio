import pprint
import factories as f
import logging

logging.basicConfig(level=logging.DEBUG)

pp = pprint.PrettyPrinter()


if __name__ == "__main__":
    # factory = f.RedBottles()
    # factory = f.GreenBottles()
    # factory = f.BlueBottles()
    factory = f.PurpleBottles()
    # factory = f.YellowBottles()
    print("\n".join([str(l) for l in factory.product_production_lines]))
    print("\n".join([str(l) for l in factory.electricity_production_lines]))
    print("\n".join([str(l) for l in factory.burnable_production_lines]))
    print("\n".join([str(l) for l in factory.bus_production_lines]))


"""
TODO:

[*] account for inserters
* calculate BOM for creating infrastructure (miners, smelters, assembly machines, power gen, etc.)
* start at the bottom of the stack when removing bus items
* Incorporate modules
"""