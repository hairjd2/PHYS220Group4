import schemdraw
import schemdraw.elements as elm

def drawCircuit(values, device):
    if device == 1:
        circuitDevice = (I1 := elm.Capacitor().down().label('Device', loc='bot'))

    with schemdraw.Drawing() as d:
        d.config(unit=5)
        d += (V1 := elm.SourceV().label('5V'))
        d += (R1 := elm.Resistor().right().label('R1')).label(['+','$v_{R1}$','-'], loc='bot')
        d += elm.Dot()
        d.push()
        d += (R2 := elm.Resistor().down().label('R2', loc='bot', rotate=True)).label(['+','$v_{R2}$','-'])
        d += elm.Dot()
        d.pop()
        d += elm.Switch(action="close")
        # d += (L1 := elm.Line())
        if device == 0:
            elm.style(elm.STYLE_IEC)
            d += (I1 := elm.Resistor().down().label('Device', loc='bot'))
            elm.style(elm.STYLE_IEEE)
        else:
            d += circuitDevice
        d += (L2 := elm.Line().tox(V1.start))
        d += elm.LoopCurrent([R1,R2,L2,V1], pad=1.25).label('$I_1$')
        d += elm.LoopCurrent([R1,I1,L2,R2], pad=1.25).label('$I_2$')
        d.draw()

def constructCircuit():
    drawCircuit([1, 2], 0)
    drawCircuit([1, 2], 1)
    print("What device would you like to use?")

def start():
    choice = 0
    while choice != 2:
        print("What would would you like to do?")
        print("1. Construct circuit")
        print("2. Quit")
        choice = int(input("Choice: "))
        if choice == 2:
            break
        constructCircuit()

if __name__ == "__main__":
    start()