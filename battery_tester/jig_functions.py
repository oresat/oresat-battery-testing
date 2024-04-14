def charge_one_battery(BTJ, bank: int, cell: int):
    BTJ.set_charge_bank(BTJ, bank)


def charge_one_bank(BTJ, bank: int):
    """
    Charges all batteries in one bank.
    """
    BTJ.set_charge_bank(BTJ, bank)
    BTJ.setup(BTJ, True)


def discharge_one_bank(BTJ, bank: int):
    """
    Discharges all batteries in one bank.
    """
    BTJ.set_charge_bank(BTJ, bank)
    BTJ.setup(BTJ, False, True)


def output_measurements(BTJ, bank: int):
    """
    Measures and prints voltage/temps of each cell in one bank.
    """
    data = BTJ.get_data(BTJ, bank)
    print(f"Bank {bank} data:\n")
    for i in data:
        print(f"Cell {i+1}: ")
        print(f"Temperature: {i.temperature}")
        print(f"Voltage: {i.voltage}")
        print()


# Write bankdata to CSV file.
