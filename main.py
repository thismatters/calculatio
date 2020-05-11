import pprint
import factories as f
import logging

logging.basicConfig(level=logging.INFO)

pp = pprint.PrettyPrinter()


if __name__ == "__main__":
    # factory = f.RedBottles()
    # factory = f.GreenBottles()
    # factory = f.BlueBottles()
    # factory = f.PurpleBottles()
    factory = f.YellowBottles()
    print("\n".join([str(l) for l in factory.product_production_lines]))
    print("\n".join([str(l) for l in factory.electricity_production_lines]))
    print("\n".join([str(l) for l in factory.burnable_production_lines]))
    print("\n".join([str(l) for l in factory.bus_production_lines]))
    print(factory.crafting_item_counts)
    print(factory.base_resources)

"""
TODO:

[*] account for inserter power use
[*] Incorporate modules
[*] sub-bus production
[*] calculate BOM for creating infrastructure (miners, smelters, assembly machines, power gen, etc.)
* Better data view
"""