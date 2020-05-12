import logging
logging.basicConfig(level=logging.DEBUG)

from factories import SpeedRunProgression


logging.debug("here")

if __name__ == "__main__":
    prog = f.SpeedRunProgression()
    with open("busses_by_phase.html", "w") as _file:
        _file.write("<html>")
        _file.write("<head><style>table, th, td {border: 1px solid black;}</style></head>")
        _file.write("<h2>Busses by Phase</h2>")
        _file.write(prog.busses_to_html())
        _file.write("<h2>Production by Phase</h2>")
        _file.write("<h2>Total Resource Use</h2>")
        _file.write("<h2>Production by Phase</h2>")
        _file.write("</html>")
    final_factory = prog.factory_steps[-1]
    rocket_factory = prog.rocket_factory
    print("\n".join([str(l) for l in final_factory.product_production_lines]))
    print(final_factory.crafting_item_counts)
    print(final_factory.base_resources)

    print("\n".join([str(l) for l in rocket_factory.product_production_lines]))
    print(rocket_factory.base_resources)

"""
TODO:

[*] account for inserter power use
[*] Incorporate modules
[*] sub-bus production
[*] calculate BOM for creating infrastructure (miners, smelters, assembly machines, power gen, etc.)
* account for inserters (approx) in BOM
* Better data view
"""


# {'IronOre': 30579.4, 'Stone': 4705.0, 'Water': 18692.222222222223, 'CopperOre': 6670.5, 'CrudeOil': 37377.77777777778, 'Coal': 495.0}
# {'IronOre': 30889.8, 'Stone': 4705.0, 'Water': 19984.444444444445, 'CopperOre': 7325.5, 'CrudeOil': 44088.88888888889, 'Coal': 590.0}