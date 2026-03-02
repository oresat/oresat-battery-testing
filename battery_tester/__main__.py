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
