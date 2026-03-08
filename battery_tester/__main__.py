import labjack_backend as LBJ
import chargers_backend as CHR

if __name__ == "__main__":
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
    menu = 0;
    #Let the user enter the serial port addresses.
    menu = input("Are you using Lev's Thinkpad? Plug board on right side. Yes? Type 1. No? Type 0 to enter your own ports.")
    if menu = 1:
        for device in range(NUM_CHARGERS):
            paths.append(input("Enter the serial path for charger 1 exactly: "))
            print(f"You entered the following path:\n{paths[device]}\nIf this is wrong, restart.\n")
    else if menu = 0:#Supply the paths for Lev's Thinkpad, with the board plugged into rightside
        paths.append(DEFAULT_CHARGER_PATHS.A)
        paths.append(DEFAULT_CHARGER_PATHS.B)
        paths.append(DEFAULT_CHARGER_PATHS.C)
        paths.append(DEFAULT_CHARGER_PATHS.D)
    else print("Input error. Restart and enter a 1 or 0.\n")
    

    CHR.start_charging(CHR.ChargeProfile)
