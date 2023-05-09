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

circuit = Circuit('Band Pass RLC Filter') 
source = circuit.SinusoidalVoltageSource('input', 'in', 
                                         circuit.gnd, 
                                         amplitude=1@u_V)
circuit.L(1, 'in', 2, 10@u_mH)
circuit.C(1, 2, 'out', 1@u_uF)
circuit.R(1, 'out', circuit.gnd, 25@u_Ω)
  
tau = circuit['L1'].inductance / circuit['R1'].resistance

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.ac(start_frequency=100@u_Hz, 
                          stop_frequency=10@u_kHz, 
                          number_of_points=100,  
                          variation='dec')

def out_voltage(t, tau):
    return float(source.amplitude) * (1 - np.exp(-t / tau))

print('Theoretical tau =', tau)

inductance = 10@u_mH
capacitance = 1@u_uF

resonant_frequency = 1 / (2 * math.pi * math.sqrt(inductance * capacitance))
quality_factor = 1 / circuit['R1'].resistance * math.sqrt(inductance / capacitance)

print("Resonant frequency = {:.1f} Hz".format(resonant_frequency))
print("Factor of quality = {:.1f}".format(quality_factor))

# Bode-Diagram plots
figure, axes = plt.subplots(2, figsize=(20,10))
plt.title("Bode Diagram of a Band-Pass RLC Filter")
bode_diagram(axes=axes,
             frequency=analysis.frequency,
             gain=20*np.log10(np.absolute(analysis.out)),
             phase=np.angle(analysis.out, deg=False),
             marker='.',
             color='magenta',
             linestyle='-',
            )
for ax in axes:
    ax.axvline(x=resonant_frequency, color='red')
    
plt.tight_layout()
plt.show()

# Current and Voltage over time

step_time = 6@u_us
analysis2 = simulator.transient(step_time= step_time, end_time=source.period)

plt.figure()
fig, plots = plt.subplots(2, 1)
plt.suptitle("RLC Circuit")
current_scale = 1000
plots[0].set_title("Voltage of each node")
plots[0].grid()
plots[0].plot(analysis2['in'])
plots[0].plot(analysis2['out'])
plots[0].set_ylim(-0.01, 6)
plots[0].set_xlabel('t (s)')
plots[0].set_ylim(-0.01, 2)
plots[0].set_xlabel('t [μs]')
plots[0].set_ylabel('V')
    # Fixme: resistor current, scale
plots[0].legend(('Vin [V]', '$V_R$ [V]', 'Vout [V]'), loc="best")

ax1 = plots[1].twinx()
plots[1].set_title("Current")
plots[1].grid()
plots[1].plot(analysis2['in'])
plots[1].plot(((analysis2['in'] - analysis2.out)/circuit['R1'].resistance) * current_scale)
plots[1].set_ylim(-0.01, 6)
plots[1].set_xlabel('t [s]')
plots[1].set_ylabel('mA')
plt.legend(('Vin [V]', 'Vout [V]', 'I'), loc=(.8,.8))
plots[1].set_xlim(0, 1750)
plots[1].set_ylim(-0.01, 50)
plots[1].set_xlabel('t [μs]')
plots[1].set_ylabel('Voltage [V]')
ax1.set_ylabel('Current [mA]')
plots[1].legend(('Vin [V]', 'I [mA]'), loc="best")
plt.tight_layout()
