from battery_test_jig import CHARGERS, BatteryTestJig

"""
One bank at a time, measure all batteries, charge all batteries, then measure all batteries, then discharge all batteries, then measure all batteries.
"""

BTJ = BatteryTestJig(CHARGERS)


def charge_one_battery_get_data(bank: int, time: float, cell: int):
    """
    Select a bank, then select a charger, then charge associated cell, then output cell's data.
    Cell is 0: A, 1: B, 2: C, 3: D
    """
    BTJ.set_charge_bank(bank)
    BTJ.setup(chargeFlag=True, dischargeFlag=False)
    time.sleep(time)
    BTJ.get_data(bank)


def charge_one_bank(bank: int):
    """
    Charges all batteries in one bank.
    """
    BTJ.set_charge_bank(bank)
    BTJ.setup(chargeFlag=True, dischargeFlag=False)


def discharge_one_bank(bank: int):
    """
    Discharges all batteries in one bank.
    """
    BTJ.set_charge_bank(bank)
    BTJ.setup(chargeFlag=False, dischargeFlag=True)


def output_measurements(bank: int):
    """
    Measures and prints voltage/temps of each cell in one bank.
    """
    data = BTJ.get_data(bank)
    print(f"Bank {bank} data:\n")
    for i, val in enumerate(data):
        print(f"Cell {i+1}: ")
        print(f"Temperature: {val.temperature}")
        print(f"Voltage: {val.voltage}")
        print()


# Write bankdata to CSV file.
