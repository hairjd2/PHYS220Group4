# Usual libraries
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
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Probe.Plot import plot

def createNetlist(r1, r2, device):
    pass

def drawCircuit(values, device):
    if values[2] == "Device":
        r1Label = "R1"
        r2Label = "R2"
    else:
        r1Label = values[0]
        r2Label = values[1]

    deviceLabel = values[2]

    if device == 1:
        circuitDevice = (I1 := elm.SourceV().down().label(deviceLabel, loc='bot'))
    elif device == 2:
        circuitDevice = (I1 := elm.SourceI().down().label(deviceLabel, loc='bot'))
    elif device == 3:
        circuitDevice = (I1 := elm.Resistor().down().label(deviceLabel, loc='bot'))
    elif device == 4:
        circuitDevice = (I1 := elm.Capacitor().down().label(deviceLabel, loc='bot'))
    elif device == 5:
        circuitDevice = (I1 := elm.Inductor().down().label(deviceLabel, loc='bot'))

    with schemdraw.Drawing() as d:
        d.config(unit=5)
        d += (V1 := elm.SourceV().label('5V'))
        d += (R1 := elm.Resistor().right().label(r1Label)).label(['+','$v_{R1}$','-'], loc='bot')
        d += elm.Dot()
        d.push()
        d += (R2 := elm.Resistor().down().label(r2Label, loc='bot')).label(['+','$v_{R2}$','-'])
        d += elm.Dot()
        d.pop()
        d += elm.Switch(action="close")
        # d += (L1 := elm.Line())
        if device == 0 or device == 6:
            elm.style(elm.STYLE_IEC)
            d += (I1 := elm.Resistor().down().label(deviceLabel, loc='bot'))
            elm.style(elm.STYLE_IEEE)
        else:
            d += circuitDevice
        d += (L2 := elm.Line().tox(V1.start))
        d += elm.LoopCurrent([R1,R2,L2,V1], pad=1.25).label('$I_1$')
        d += elm.LoopCurrent([R1,I1,L2,R2], pad=1.25).label('$I_2$')
        d.draw()

def constructCircuit():
    # Displays default device as a placeholder
    print("What device would you like to use where the place holder device is?")
    print("1. Voltage Source")
    print("2. Current Source")
    print("3. Resistor")
    print("4. Capacitor")
    print("5. Inductor")
    print("6. Just wire")
    drawCircuit([-1, -1, "Device"], 0)
    choice = int(input("What device would you like to use?: "))

    r1 = input('Input value with correct units for resistor R1 ("1k" == 1000Ω): ')
    r2 = input('Input value with correct units for resistor R2 ("1k" == 1000Ω): ')
    if choice != 6:
        deviceVal = input('Input value with correct units (for voltage source, you should provide V): ')
        if choice == 3:
            drawCircuit([r1 + "Ω", r2 + "Ω", deviceVal + "Ω"], choice)
        else:
            drawCircuit([r1 + "Ω", r2 + "Ω", deviceVal], choice)
    else:
        drawCircuit([r1, r2, "Wire"], choice)
        deviceVal = 0

    return r1, r2, deviceVal

def drawVoltageDivider():
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
    with schemdraw.Drawing() as d:
        d += elm.Switch()
        d += elm.Resistor().right().label('1kΩ')
        d += elm.Capacitor().down().label('1μF')
        d += elm.Line().left()
        d += elm.Line().left()
        d += elm.SourceV().up().label('5V')
        d.save("figures/RCDrawingOpen.jpg")

    with schemdraw.Drawing() as d:
        d += elm.Switch(action="close")
        d += elm.Resistor().right().label('1kΩ')
        d += elm.Capacitor().down().label('1μF')
        d += elm.Line().left()
        d += elm.Line().left()
        d += elm.SourceV().up().label('5V')
        d.save("figures/RCDrawingClosed.jpg")

def drawRL():
    with schemdraw.Drawing() as d:
        d += elm.Dot().label("in")
        d += elm.Switch()
        d += elm.Dot().label("resistor")
        d += elm.Resistor().right().label('1kΩ')
        d += elm.Dot().label("out")
        d += elm.Inductor().down().label('1H')
        d += elm.Line().left()
        d += elm.Line().left()
        d += elm.SourceV().up().label('5V')
        d.save("figures/RLDrawingOpen.jpg")

    with schemdraw.Drawing() as d:
        d += elm.Dot().label("in")
        d += elm.Switch(action="close")
        d += elm.Dot().label("resistor")
        d += elm.Resistor().right().label('1kΩ')
        d += elm.Dot().label("out")
        d += elm.Inductor().down().label('1H')
        d += elm.Line().left()
        d += elm.Line().left()
        d += elm.SourceV().up().label('5V')
        d.save("figures/RLDrawingClosed.jpg")

def voltageDivider():
# TODO: Add comments
# TODO: Need to make drawing of circuit with schemdraw
    drawVoltageDivider()

    circuit = Circuit('Voltage Divider')

    circuit.V('input', 'in', circuit.gnd, 10@u_V)
    circuit.R(1, 'in', 'out', 2@u_kΩ)
    circuit.R(2, 'out', circuit.gnd, 1@u_kΩ)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()

    for node in analysis.nodes.values():
        print('Node {}: {:5.2f} V'.format(str(node), float(node)))

def RCCircuit():
# TODO: Fix comments
# TODO: Maybe have separate subplots for the current and voltage of the capacitor
# TODO: Try DC source for circuit instead

    drawRC()

    print("Drawing of circuit in figures folder")

    element_type = ('capacitor')

    # for element_type in ('capacitor'):

    circuit = Circuit(element_type.title())
    # Fixme: compute value
    
    source = circuit.PulseVoltageSource('input', 'in', circuit.gnd,
                            initial_value=0@u_V, pulsed_value=5@u_V,
                            pulse_width=10@u_ms, period=20@u_ms)
    circuit.R(1, 'in', 'out', 1@u_kΩ)
    circuit.C(1, 'out', circuit.gnd, 1@u_uF)
    # circuit.R(2, 'out', circuit.gnd, kilo(1)) # for debug

    tau = circuit['R1'].resistance * circuit['C1'].capacitance

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    step_time = 10@u_us
    analysis = simulator.transient(step_time=step_time, end_time=source.period * 0.5)

    # Let define the theoretical output voltage.
    def out_voltage(t, tau):
                # Fixme: TypeError: only length-1 arrays can be converted to Python scalars
        return float(source.pulsed_value) * (1 -  np.exp(-t / tau))
    # Fixme: get step_time from analysis
    # At t = 5 tau, each circuit has nearly reached it steady state.
    i_max = int(5 * tau / float(step_time))
    popt, pcov = curve_fit(out_voltage, analysis.out.abscissa[:i_max], analysis.out[:i_max])
    tau_measured = popt[0]

        # Fixme: use Unit().canonise()
    print('tau {0} = {1}'.format(element_type, tau.canonise().str_space()))
    print('tau measured {0} = {1:.1f} ms'.format(element_type, tau_measured * 1000))

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
# TODO: Fix comments

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
    plt.legend(('Vin [V]', 'Vout [V]', 'I'), loc=(.8, .8))

    plt.tight_layout()
    plt.savefig("figures/RLCircuit.jpg", dpi=600)

def RLCCircuit():
    drawRL()

    print("Drawing of circuit in figures folder")

    element_type = ('inductor')

    # for element_type in ('capacitor'):

    circuit = Circuit(element_type.title())
    # Fixme: compute value
    
    source = circuit.PulseVoltageSource('input', 'in', circuit.gnd,
                            initial_value=0@u_V, pulsed_value=5@u_V,
                            pulse_width=10@u_ms, period=20@u_ms)
    # circuit.R(1, 'in', 'resistor', 1@u_kΩ)
    # circuit.L(1, 'resistor', 'out', 1@u_H)
    # circuit.C(1, 'out', circuit.gnd, 1@u_uF)

    circuit.R(1, 'in', circuit.gnd, 1@u_kΩ)
    circuit.L(1, 'resistor', circuit.gnd, 1@u_H)
    circuit.C(1, 'out', circuit.gnd, 1@u_uF)
    # circuit.R(2, 'out', circuit.gnd, kilo(1)) # for debug

    tau = circuit['L1'].inductance / circuit['R1'].resistance

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    step_time = 10@u_us
    analysis = simulator.transient(step_time=step_time, end_time=source.period)

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

    plt.figure()
    fig, plots = plt.subplots(2, 1)
    plt.suptitle("Inductor: current is constant")
    current_scale = 1000
    plots[0].set_title("Voltage of Inductor")
    plots[0].grid()
    plots[0].plot(analysis['in'])
    plots[0].plot(analysis['out'])
    plots[0].plot(analysis['resistor'])
    # plots[1].set_xlim(0, 1000)
    plots[0].set_ylim(-0.01, 6)
    plots[0].set_xlabel('t (s)')
    plots[0].set_ylabel('V')
    # Fixme: resistor current, scale
    plots[1].set_title("Current")
    plots[1].grid()
    plots[1].plot(analysis['in'])
    plots[1].plot(((analysis['in'] - analysis.out)/circuit['R1'].resistance) * current_scale)
    # plots[1].set_xlim(0, 1000)
    plots[1].set_ylim(-0.01, 6)
    plots[1].set_xlabel('t [s]')
    plots[1].set_ylabel('mA')
    plt.legend(('Vin [V]', 'Vout [V]', 'I'), loc=(.8,.8))

    plt.tight_layout()
    plt.savefig("figures/RLCCircuit.jpg", dpi=600)

def start():
# TODO: Possibly add RLC circuit as well
    choice = 0
    while choice != 6:
        print("What would would you like to do?")
        print("1. Construct main circuit")
        print("2. Simulate voltage divider")
        print("3. Simulate RC circuit")
        print("4. Simulate RL circuit")
        print("5. Simulate RLC")
        print("6. Quit")
        choice = int(input("Choice: "))
        if choice == 1:
            r1, r2, deviceVal = constructCircuit()
            createNetlist(r1, r2, deviceVal)
        elif choice == 2:
            voltageDivider()
        elif choice == 3:
            RCCircuit()
        elif choice == 4:
            RLCircuit()
        elif choice == 5:
            RLCCircuit()
        elif choice == 6:
            break

if __name__ == "__main__":
    start()