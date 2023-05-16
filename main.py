# Usual libraries
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Schemdraw
import schemdraw
import schemdraw.elements as elm

# PySpice Logging
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

# Needed for circuit netlists
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from scipy.optimize import curve_fit

def drawVoltageDivider():
# Drawing of simple voltage divider circuit
    with schemdraw.Drawing() as d:
        d += elm.Ground()
        d += elm.SourceV().up().label('5V')
        d += elm.Dot().label('in')
        d += elm.Resistor().right().label('2kΩ')
        d.push()
        d += elm.Line().right()
        d += elm.Dot(open=True).label('out')
        d.pop()
        d += elm.Resistor().down().label('1kΩ')
        d += elm.Line().left()
        d.save("figures/VoltageDivider.jpg")

def drawRC():
# Drawing of RC circuit
# Drawing with the switch closed
    with schemdraw.Drawing() as d:
        d += elm.Dot().label("in")
        d += elm.Switch()
        d += elm.Resistor().right().label('1kΩ')
        d += elm.Dot().label("out")
        d += elm.Capacitor().down().label('1μF')
        d += elm.Line().left()
        d += elm.Line().left()
        d += elm.SourceV().up().label('5V')
        d.save("figures/RCDrawingOpen.jpg")

# Drawing with the switch closed
    with schemdraw.Drawing() as d:
        d += elm.Dot().label("in")
        d += elm.Switch(action="close")
        d += elm.Resistor().right().label('1kΩ')
        d += elm.Dot().label("out")
        d += elm.Capacitor().down().label('1μF')
        d += elm.Line().left()
        d += elm.Line().left()
        d += elm.SourceV().up().label('5V')
        d.save("figures/RCDrawingClosed.jpg")

def drawRL():
# Drawing of RL circuit
# Drawing with the switch open
    with schemdraw.Drawing() as d:
        d += elm.Dot().label("in")
        d += elm.Switch()
        d += elm.Resistor().right().label('1kΩ')
        d += elm.Dot().label("out")
        d += elm.Inductor().down().label('1H')
        d += elm.Line().left()
        d += elm.Line().left()
        d += elm.SourceV().up().label('5V')
        d.save("figures/RLDrawingOpen.jpg")

# Drawing with the switch closed
    with schemdraw.Drawing() as d:
        d += elm.Dot().label("in")
        d += elm.Switch(action="close")
        d += elm.Resistor().right().label('1kΩ')
        d += elm.Dot().label("out")
        d += elm.Inductor().down().label('1H')
        d += elm.Line().left()
        d += elm.Line().left()
        d += elm.SourceV().up().label('5V')
        d.save("figures/RLDrawingClosed.jpg")

def drawBandpass():
# Drawing of Bandpass filter circuit
    with schemdraw.Drawing() as d:
        d += elm.Dot().label("in")
        d += elm.Resistor().right().label('1kΩ')
        d += elm.Dot().label("resistor")
        d += elm.Inductor().right().label('1H')
        d += elm.Dot().label("out")
        d += elm.Capacitor().down().label('1μF')
        d += elm.Line().left()
        d += elm.Line().left()
        d += elm.SourceSin().up().label(r'1sin($\omega$t)')
        d.save("figures/BandpassDrawing.jpg")

def voltageDivider():
# Runs SchemDraw figure function
    drawVoltageDivider()

# Create circuit object
    circuit = Circuit('Voltage Divider')

# Generate netlist
    circuit.V('input', 'in', circuit.gnd, 5@u_V)
    circuit.R(1, 'in', 'out', 2@u_kΩ)
    circuit.R(2, 'out', circuit.gnd, 1@u_kΩ)

# Perform basic operating point analysis
# Note: using default temperature parameters provided by library docs
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()

# For loops through all defined nodes and outputs the voltage values
    for node in analysis.nodes.values():
        print('Node {}: {:5.2f} V'.format(str(node), float(node)))

def RCCircuit():
# Runs SchemDraw figure function
    drawRC()

    print("Drawing of circuit in figures folder")

    element_type = ('capacitor')

    circuit = Circuit(element_type.title())
    
# Use pulse voltage source and create netlist
    source = circuit.PulseVoltageSource('input', 'in', circuit.gnd,
                            initial_value=0@u_V, pulsed_value=5@u_V,
                            pulse_width=10@u_ms, period=20@u_ms)
    circuit.R(1, 'in', 'out', 1@u_kΩ)
    circuit.C(1, 'out', circuit.gnd, 1@u_uF)

    tau = circuit['R1'].resistance * circuit['C1'].capacitance

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    step_time = 10@u_us
    analysis = simulator.transient(step_time=step_time, end_time=source.period * 0.5)

    # defines the theoretical output voltage.
    def out_voltage(t, tau):
                # Fixme: TypeError: only length-1 arrays can be converted to Python scalars
        return float(source.pulsed_value) * (1 -  np.exp(-t / tau))
    # Fixme: get step_time from analysis
    # At t = 5 tau, each circuit has nearly reached it steady state.
    i_max = int(5 * tau / float(step_time))
    popt, pcov = curve_fit(out_voltage, analysis.out.abscissa[:i_max], analysis.out[:i_max])
    tau_measured = popt[0]

    print('tau {0} = {1}'.format(element_type, tau.canonise().str_space()))
    print('tau measured {0} = {1:.1f} ms'.format(element_type, tau_measured * 1000))

# Plot of voltage of the capacitor over time
    plt.figure()
    fig, plots = plt.subplots(2, 1)
    plt.suptitle("Capacitor: voltage is constant")
    current_scale = 1000
    plots[0].set_title("Voltage of Capacitor")
    plots[0].grid()
    plots[0].plot(analysis['in'])
    plots[0].plot(analysis['out'])
    plots[0].set_xlim(0, 1000)
    plots[0].set_ylim(-0.01, 5.1)
    plots[0].set_xlabel('t [μs]')
    plots[0].set_ylabel('V')
    plots[0].legend(('Vin [V]', 'Vout [V]'), loc="best")

# Plot of the current around the loop
    ax1 = plots[1].twinx()
    plots[1].set_title("Current")
    plots[1].grid()
    plots[1].plot(analysis['in'])
    plots[1].plot(((analysis['in'] - analysis.out)/circuit['R1'].resistance) * current_scale)
    plots[1].set_xlim(0, 1000)
    plots[1].set_ylim(-0.01, 5.1)
    plots[1].set_xlabel('t [μs]')
    plots[1].set_ylabel('Voltage [V]')
    ax1.set_ylabel('Current [mA]')
    plots[1].legend(('Vin [V]', 'I [mA]'), loc="best")

    plt.tight_layout()
    plt.savefig("figures/RCCircuit.jpg", dpi=600)

def RLCircuit():
# Runs SchemDraw figure function
    drawRL()

    print("Drawing of circuit in figures folder")

    element_type = ('inductor')

    circuit = Circuit(element_type.title())
    # Fixme: compute value
    
    source = circuit.PulseVoltageSource('input', 'in', circuit.gnd,
                            initial_value=0@u_V, pulsed_value=5@u_V,
                            pulse_width=10@u_ms, period=20@u_ms)
    circuit.R(1, 'in', 'out', 1@u_kΩ)
    circuit.L(1, 'out', circuit.gnd, 1@u_H)
    # circuit.R(2, 'out', circuit.gnd, kilo(1)) # for debug

    tau = circuit['L1'].inductance / circuit['R1'].resistance

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    step_time = 10@u_us
    analysis = simulator.transient(step_time=step_time, end_time=source.period * 0.5)

    # Let define the theoretical output voltage.
    def out_voltage(t, tau):
        return float(source.pulsed_value) * np.exp(-t / tau)
    # Fixme: get step_time from analysis
    # At t = 5 tau, each circuit has nearly reached it steady state.
    i_max = int(5 * tau / float(step_time))
    popt, pcov = curve_fit(out_voltage, analysis.out.abscissa[:i_max], analysis.out[:i_max])
    tau_measured = popt[0]

    print('tau {0} = {1}'.format(element_type, tau.canonise().str_space()))
    print('tau measured {0} = {1:.1f} ms'.format(element_type, tau_measured * 1000))

# Plot of voltage of the inductor over time
    plt.figure()
    fig, plots = plt.subplots(2, 1)
    plt.suptitle("Inductor: current is constant")
    current_scale = 1000
    plots[0].set_title("Voltage of Inductor")
    plots[0].grid()
    plots[0].plot(analysis['in'])
    plots[0].plot(analysis['out'])
    plots[1].set_xlim(0, 1000)
    plots[0].set_ylim(-0.01, 5.1)
    plots[0].set_xlabel('t (μs)')
    plots[0].set_ylabel('V')
    plots[0].legend(('Vin [V]', 'Vout [V]'), loc="best")

# Plot of the current around the loop
    ax1 = plots[1].twinx()
    plots[1].set_title("Current")
    plots[1].grid()
    plots[1].plot(analysis['in'])
    plots[1].plot(((analysis['in'] - analysis.out)/circuit['R1'].resistance) * current_scale)
    plots[1].set_xlim(0, 1000)
    plots[1].set_ylim(-0.01, 5.1)
    plots[1].set_xlabel('t [μs]')
    plots[1].set_ylabel('Voltage [V]')
    ax1.set_ylabel('Current [mA]')
    plots[1].legend(('Vin [V]', 'I [mA]'), loc="best")

    plt.tight_layout()
    plt.savefig("figures/RLCircuit.jpg", dpi=600)

def BandPass():
    drawBandpass()

    circuit = Circuit('Band Pass RLC Filter') 
    source = circuit.SinusoidalVoltageSource('input', 'in', 
                                            circuit.gnd, 
                                            amplitude=1@u_V)
    circuit.L(1, 'in', 2, 10@u_mH)
    circuit.C(1, 2, 'out', 1@u_uF)
    circuit.R(1, 'out', circuit.gnd, 25@u_Ω)
    
    tau = circuit['L1'].inductance / circuit['R1'].resistance

# Use AC simulation for analysis instead of usual DC methods. 
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

# Calculate resonance frequency and quality factor
    resonant_frequency = 1 / (2 * math.pi * math.sqrt(inductance * capacitance))
    quality_factor = 1 / circuit['R1'].resistance * math.sqrt(inductance / capacitance)

    print("Resonant frequency = {:.1f} Hz".format(resonant_frequency))
    print("Factor of quality = {:.1f}".format(quality_factor))

    # Bode-Diagram plots
    plt.figure()
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
    plt.savefig('figures/BandpassBodeplot.jpg', dpi=600)

def start():
# Provided menu for user to simulate the circuit of their choice
    choice = 0
    while choice != 5:
        print("What would would you like to do?")
        print("1. Simulate voltage divider")
        print("2. Simulate RC circuit")
        print("3. Simulate RL circuit")
        print("4. Simulate BandPass Filter Circuit")
        print("5. Quit")
        choice = int(input("Choice: "))
        if choice == 1:
            voltageDivider()
        elif choice == 2:
            RCCircuit()
        elif choice == 3:
            RLCircuit()
        elif choice == 4:
            BandPass()
        elif choice == 5:
            break

if __name__ == "__main__":
    start()