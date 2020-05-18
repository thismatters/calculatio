import logging

logging.basicConfig(level=logging.DEBUG)

from factories import SpeedRunProgression, LateFactory


logging.debug("here")

if __name__ == "__main__":
    # prog = SpeedRunProgression()
    # with open("busses_by_phase.html", "w") as _file:
    #     _file.write("<html>")
    #     _file.write("<head><style>table, th, td {border: 1px solid black;}</style></head>")
    #     _file.write("<h2>Busses by Phase</h2>")
    #     _file.write(prog.busses_to_html())
    #     _file.write("<h2>Production by Phase</h2>")
    #     _file.write("<h2>Total Resource Use</h2>")
    #     _file.write("<h2>Production by Phase</h2>")
    #     _file.write("</html>")
    # final_factory = prog.factory_steps[-1]
    # rocket_factory = prog.rocket_factory
    # print("\n".join([str(l) for l in final_factory.product_production_lines]))
    # print(final_factory.crafting_item_counts)
    # print(final_factory.base_resources)

    # print("\n".join([str(l) for l in rocket_factory.product_production_lines]))
    # print(rocket_factory.base_resources)
    d = LateFactory(
        desired_production_rates={"Satellite": 0.01,}, module="SpeedModule1",
    )
    print("\n".join([str(l) for l in d.product_production_lines]))
"""
TODO:

[*] account for inserter power use
[*] Incorporate modules
[*] sub-bus production
[*] calculate BOM for creating infrastructure (miners, smelters, assembly machines, power gen, etc.)
* better accounting for advanced oil processing (cracking etc.)
* account for inserters (approx) in BOM
* Better data view
* add speed module line to the blue bottle stage
* add support for assembly machine balancing, e.g. use a slower machine in order 
   to keep the number of machines consistent (copper wire in electric circuits)
* power discrepancy...
* revise plan
"""
