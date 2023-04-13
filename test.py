def battery():
    
    print("Now...which direction is the new battery (B2) pointing with respect to the original battery (B1)?")
    print("")
    print("As if our new battery was in series, use the menu to decide the direction.")
    print("")
    print("MENU--1: same direction; 2: opposite direction.")
    
#def capacitor():
#def inductor():
def resistor():
    
    Vb = float(input("What is the voltage of B1 in Volts: "))
    strength_1 = float(input("What is the resistance of R1 in Ohms: "))
    strength_2 = float(input("What is the resistance of R2 in Ohms: "))
    i_R1 = float(Vb/strength_1)
    print("")
    print("Although R2 is",strength_2,"Ohms, it has no impact on the current through R1 (i_R1), because the resistors are in parallel.")
    print("")
    print("Kirchoff's Voltage Rule demands the voltage of the battery (Vb) must equal the sum of voltage drops across any path of current.")
    print("")
    print("We ONLY have two objects in this circuit, and they are in parallel, so the voltage drop across each equals Vb.")
    print("")
    return i_R1

if __name__ == '__main__':
    
    print("There is a simple circuit with one battery (B1) and two items in parallel. There is nothing else outside the parallel.")
    print("")
    print("Occupying one route is a resistor (R1). Using the menu, you get to choose the item across the resistor!")
    print("")
    print("Then the program will calculate the current flowing through the resistor as a function of time.")
    print("")
    print("As you can imagine, depending on what you choose...the current will behave differently.")
    print("")
    print("MENU--1: Battery; 2: Capacitor; 3: Inductor; 4: Resistor; 5: Just Wire")
    
    item_block = int(input("Enter a number on the menu: "))
    
    #if item_block == 1:
        
    #if item_block == 2:
    
    #if item_block == 3:
        
    if item_block == 4:
        print("The current across R1 is",resistor(),"Amperes.")
        print("")
        print("Current is a dependent variable with respect to voltage and resistance.")
        print("")
        print("To change i_R1, either change R1, add a resistor in series with R1, or change Vb.")
        
    if item_block == 5:
        print("")
        print("The current across R1 is 0 Amperes.")
        print("")
        print("Kirchoff's Junction Rule demands the current that enters a parallel must be equal to the current that exits it.")
        print("")
        print("This means the sum of the currents through each loop of the parallel equals the total current of the circuit.")
        print("")
        print("However, when encountering a parallel, the majority of the current will feed through the loop with the least resistance.")
        print("")
        print("Ultimately, both loops will have current flow (reduced with respect to the total circuit current) unless...")
        print("")
        print("One of the paths has NO resistance, so ALL of the current will feed through that loop, leaving i_R1 = 0.")
        
    else:
        print("Invalid input. Rerun the program.")