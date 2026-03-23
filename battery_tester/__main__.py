import labjack_backend as LBJ
import chargers_backend as CHR
import time

if __name__ == "__main__":
    var = 1
    if (var):
        print("TEST SCRIPT ACTIVATE. PUT BATTERIES IN BANK 3.\n\n")
        TestData = LBJ.BankData
        # def get_data_from_one_cell(mp: MeasureProfile, bank: int, cell: int) -> BankData:
        for cell in range(4):
            TestData = LBJ.get_data_from_one_cell(LBJ.MeasureProfile, 3, cell)
            print(f"Temperature of Bank 3, Cell {cell} is: {TestData.temperature}\n")
            print(f"Voltage of Bank 3, Cell {cell} is: {TestData.voltage}\n")

    print("NOW FOR ACTUALLY CHARGING...\n\n\n") 
    DEFAULT_CHARGER_PATHS = CHR.ChargerSerialPaths()
    paths = []#This stores four addresses such as "1-1.1.4", one address per charger
    NUM_CHARGERS = int(4)
    #Let the user enter the serial port addresses.
    menu = int(input("Are you using Lev's Thinkpad? Plug board on right side. Yes? Type 1. No? Type 0 to enter your own ports.\n"))
    print(f"menu is EQUAL TO {menu}\n\n\n")
    if menu == 0:
        for device in range(NUM_CHARGERS):
            paths.append(input("Enter the serial path for charger 1 exactly: "))
            print(f"You entered the following path:\n{paths[device]}\nIf this is wrong, restart.\n")
    #Supply the paths for Lev's Thinkpad, with the board plugged into rightside
    elif menu == 1:
        paths.append(DEFAULT_CHARGER_PATHS.A)
        paths.append(DEFAULT_CHARGER_PATHS.B)
        paths.append(DEFAULT_CHARGER_PATHS.C)
        paths.append(DEFAULT_CHARGER_PATHS.D)
    else:
        print("Input error. Restart and enter a 1 or 0.\n")
        exit()

    charger_choice = input("Enter the charger you want to charge with: A, B, C, or D:\n")
    print(f"THE CHARGER CHOICE IS {charger_choice}\n\n")
    if charger_choice.upper() == 'A':
        CHR.start_charging(CHR.ChargeProfile(), paths[0])
    elif charger_choice.upper() == 'B':
        CHR.start_charging(CHR.ChargeProfile(), paths[1])
    elif charger_choice.upper() == 'C':
        CHR.start_charging(CHR.ChargeProfile(), paths[2])
    elif charger_choice.upper() == 'D':
        CHR.start_charging(CHR.ChargeProfile(), paths[3])
    else:
        print("Input error. Restart.\n")
        exit()

    time.sleep(600)
    for cell in range(4):
        TestData = LBJ.get_data_from_one_cell(LBJ.MeasureProfile, 3, cell)
        print(f"Temperature of Bank 3, Cell {cell} is: {TestData.temperature}\n")
        print(f"Voltage of Bank 3, Cell {cell} is: {TestData.voltage}\n")




