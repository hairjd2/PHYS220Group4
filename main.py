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

def voltageDivider():
    circuit = Circuit('Voltage Divider')

    circuit.V('input', 1, circuit.gnd, 10@u_V)
    circuit.R(1, 1, 2, 2@u_kΩ)
    circuit.R(2, 2, circuit.gnd, 1@u_kΩ)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()

    for node in analysis.nodes.values():
        print('Node {}: {:5.2f} V'.format(str(node), float(node)))

def RCCircuit():
    figure, (ax1, ax2) = plt.subplots(2, figsize=(20, 10))

    element_types = ('capacitor')

    for element_type in ('capacitor'):

        circuit = Circuit(element_type.title())
        # Fixme: compute value
        source = circuit.PulseVoltageSource('input', 'in', circuit.gnd,
                            initial_value=0@u_V, pulsed_value=10@u_V,
                            pulse_width=10@u_ms, period=20@u_ms)
        circuit.R(1, 'in', 'out', 1@u_kΩ)
        if element_type == 'capacitor':
            element = circuit.C
            value = 1@u_uF
            # tau = RC = 1 ms
        else:
            element = circuit.L
            # Fixme: force component value to an Unit instance ?
            value = 1@u_H
            # tau = L/R = 1 ms
        element(1, 'out', circuit.gnd, value)
        # circuit.R(2, 'out', circuit.gnd, kilo(1)) # for debug

        if element_type == 'capacitor':
            tau = circuit['R1'].resistance * circuit['C1'].capacitance
        else:
            tau = circuit['L1'].inductance / circuit['R1'].resistance

        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        step_time = 10@u_us
        analysis = simulator.transient(step_time=step_time, end_time=source.period*3)

        # Let define the theoretical output voltage.
        if element_type == 'capacitor':
            def out_voltage(t, tau):
                # Fixme: TypeError: only length-1 arrays can be converted to Python scalars
                return float(source.pulsed_value) * (1 -  np.exp(-t / tau))
        else:
            def out_voltage(t, tau):
                return float(source.pulsed_value) * np.exp(-t / tau)
        # Fixme: get step_time from analysis
        # At t = 5 tau, each circuit has nearly reached it steady state.
        i_max = int(5 * tau / float(step_time))
        popt, pcov = curve_fit(out_voltage, analysis.out.abscissa[:i_max], analysis.out[:i_max])
        tau_measured = popt[0]

        # Fixme: use Unit().canonise()
        print('tau {0} = {1}'.format(element_type, tau.canonise().str_space()))
        print('tau measured {0} = {1:.1f} ms'.format(element_type, tau_measured * 1000))

        if element_type == 'capacitor':
            ax = ax1
            title = "Capacitor: voltage is constant"
        else:
            ax = ax2
            title = "Inductor: current is constant"
        ax.set_title(title)
        ax.grid()
        current_scale = 1000
        ax.plot(analysis['in'])
        ax.plot(analysis['out'])
        # Fixme: resistor current, scale
        ax.plot(((analysis['in'] - analysis.out)/circuit['R1'].resistance) * current_scale)
        ax.axvline(x=float(tau), color='red')
        ax.set_ylim(-11, 11)
        ax.set_xlabel('t [s]')
        ax.set_ylabel('[V]')
        ax.legend(('Vin [V]', 'Vout [V]', 'I'), loc=(.8,.8))

    plt.tight_layout()
    plt.show()

def RLCircuit():
    pass

def start():
    choice = 0
    while choice != 5:
        print("What would would you like to do?")
        print("1. Construct main circuit")
        print("2. Simulate voltage divider")
        print("3. Simulate RC circuit")
        print("4. Simulate RL circuit")
        print("5. Quit")
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
            break

if __name__ == "__main__":
    start()