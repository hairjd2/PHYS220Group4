import numpy as np
import matplotlib.pyplot as plt
import sys

import PySpice
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

if __name__ == "__main__":
    logger = Logging.setup_logging()

    circuit = Circuit("Voltage Divider")
    circuit.V("input", "in", circuit.gnd, 10@u_V)
    circuit.R(1, "in", "out", 9@u_kOhm)
    circuit.R(2, "out", circuit.gnd, 1@u_kOhm)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    print("The circuit/Netlist:\n\n", circuit)
    
    analysis = simulator.operating_point()

    print(analysis.nodes['in'])
    print(str(analysis.nodes['in']))
    print(float(analysis.nodes['in']))
    print(float(analysis.nodes['out']))

    exit()