import schemdraw
import schemdraw.elements as elm

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

def start():
    choice = 0
    while choice != 2:
        print("What would would you like to do?")
        print("1. Construct circuit")
        print("2. Quit")
        choice = int(input("Choice: "))
        if choice == 2:
            break
        r1, r2, deviceVal = constructCircuit()
        createNetlist(r1, r2, deviceVal)

if __name__ == "__main__":
    start()