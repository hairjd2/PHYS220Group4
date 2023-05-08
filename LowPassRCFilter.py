import math
import numpy as np
import matplotlib.pyplot as plt


import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from scipy.optimize import curve_fit

circuit = Circuit('Low Pass RC Filter')
source = circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, 
                                         amplitude=5@u_V)

circuit.R(1, 'in', 'out', 1@u_kΩ)
circuit.C(1, 'out', circuit.gnd, 1@u_uF)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.ac(start_frequency=10@u_Hz, stop_frequency=1@u_MHz, number_of_points=100,  variation='dec')

# Theoretical tau
tau = circuit['R1'].resistance * circuit['C1'].capacitance
def out_voltage(t, tau):
    return float(source.amplitude) * (1 - np.exp(-t / tau))

print('Theoretical tau =', tau)

break_frequency = 1/ (2*math.pi*float(circuit['R1'].resistance * circuit['C1'].capacitance))
print("Break frequency = {:.1f} Hz".format(break_frequency))

# Bode-Diagram plots
figure, axes = plt.subplots(2, figsize=(20,10))
plt.title("Bode Diagram of a Low-Pass RC Filter")
bode_diagram(axes=axes,
             frequency= analysis.frequency,
             gain=20*np.log10(np.absolute(analysis.out)),
             phase = np.angle(analysis.out, deg=False),
             marker='.',
             color='blue',
             linestyle='-',
             )
for ax in axes:
    ax.axvline(x=break_frequency, color='red')
    
plt.tight_layout()
plt.show()
plt.savefig("downloads/BodeDiagramLowPassRCCircuit.jpg", dpi=600)

# Current and Voltage over time

step_time = 10@u_us
analysis2 = simulator.transient(step_time= step_time, end_time=source.period)

plt.figure()
fig, plots = plt.subplots(2, 1)
plt.suptitle("Capacitor: Voltage is constant")
current_scale = 1000
plots[0].set_title("Voltage of Capacitor")
plots[0].grid()
plots[0].plot(analysis2['in'])
plots[0].plot(analysis2['out'])
plots[0].set_xlim(0, 1100)
plots[0].set_ylim(-0.01, 5.5)
plots[0].set_xlabel('t [μs]')
plots[0].set_ylabel('V')
plots[0].legend(('Vin [V]', 'Vout [V]'), loc="upper right")

ax1 = plots[1].twinx()
plots[1].set_title("Current")
plots[1].grid()
plots[1].plot(analysis2['in'])
plots[1].plot(((analysis2['in'] - analysis2.out)/circuit['R1'].resistance) * current_scale)
plots[1].set_xlim(0, 1100)
plots[1].set_ylim(-0.01, 5.5)
plots[1].set_xlabel('t [μs]')
plots[1].set_ylabel('Voltage [V]')
ax1.set_ylabel('Current [mA]')
plots[1].legend(('Vin [V]', 'I [mA]'), loc="upper right")

plt.tight_layout()
plt.savefig("downloads/LowPassRCCircuit.jpg", dpi=600)