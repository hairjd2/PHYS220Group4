import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary

#Need to add schemdraw for the circuit

circuit = Circuit('2R2C Circuit')

Vin = circuit.SinusoidalVoltageSource('Vin', 'in', circuit.gnd, amplitude=5@u_V)

circuit.R(1, 'in', 'out1', 1@u_kOhm)
circuit.R(2, 'out1', 'out2', 2@u_kOhm)
circuit.C(1, 'out1', circuit.gnd, 1@u_uF)
circuit.C(2, 'out2', circuit.gnd, 2@u_uF)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
step_time = 10@u_us
end_time = 20@u_ms

analysis = simulator.transient(step_time=step_time, end_time=end_time)

# Defining output voltage as a function of time:
def vout(t, tau1, tau2):
    return float(Vin.amplitude) * (1 - np.exp(-t / tau1)) * np.exp(-t / tau2)
    
# Max number of time steps based on resistors and capacitors
i_max = int(5 * 1@u_kOhm * 1@u_uF / float(step_time))
popt, pcov = curve_fit(vout, analysis.time[:i_max], analysis.out2[:i_max], bounds=([0, 0], np.inf))

tau1 = popt[0]
tau2 = popt[1]

print('Tau1 = {:.2f} μs, Tau2 = {:.2f} μs'.format(tau1 / u_μs, tau2 / u_μs))

fig, plots = plt.subplots(2, 1)
plt.suptitle('2R2C Circuit')
plots[0].set_title('Output Voltage')
plots[0].plot(analysis.time, analysis.inp)
plots[0].plot(analysis.time, analysis.out2)
plots[0].set_xlabel('Time [μs]')
plots[0].set_ylabel('Voltage [V]')
plots[0].legend(('Vin [V]', 'Vout [V]'))

plots[1].set_title('Current')
plots[1].plot(analysis.time, Vin._currents[1])
plots[1].plot(analysis.time, (analysis['out1'] - analysis['out2']) / R2)
plots[1].set_xlabel('Time [μs]')
plots[1].set_ylabel('Current [mA]')
plots[1].legend(('Vin [mA]', 'I [mA]'))

plt.tight_layout()
plt.savefig('2R2C Circuit.png', dpi=300)
plt.show()