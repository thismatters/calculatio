import pprint
import factories as f
import logging

logging.basicConfig(level=logging.DEBUG)

pp = pprint.PrettyPrinter()


if __name__ == "__main__":
    prog = f.SpeedRunProgression()
    with open("busses_by_phase.html", "w") as f:
        f.write("<html>")
        f.write("<head><style>table, th, td {border: 1px solid black;}</style></head>")
        f.write("<h2>Busses by Phase</h2>")
        f.write(prog.busses_to_html())
        f.write("<h2>Production by Phase</h2>")
        f.write("<h2>Total Resource Use</h2>")
        f.write("<h2>Production by Phase</h2>")
        f.write("</html>")

"""
TODO:

[*] account for inserter power use
[*] Incorporate modules
[*] sub-bus production
[*] calculate BOM for creating infrastructure (miners, smelters, assembly machines, power gen, etc.)
* account for inserters (approx) in BOM
* Better data view
"""
