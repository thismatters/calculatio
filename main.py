import pprint
from factories import PreFactory
import logging

logging.basicConfig(level=logging.INFO)

pp = pprint.PrettyPrinter()


if __name__ == "__main__":
    factory = PreFactory()
    print("\n".join([str(l) for l in factory.product_production_lines]))
    print("\n".join([str(l) for l in factory.electricity_production_lines]))
    print("\n".join([str(l) for l in factory.burnable_production_lines]))
    print("\n".join([str(l) for l in factory.bus_production_lines]))
