from battery_test_jig import CHARGERS, BatteryTestJig

"""
One bank at a time, measure all batteries, charge all batteries, then measure all batteries, then discharge all batteries, then measure all batteries.
"""

BTJ = BatteryTestJig(CHARGERS)

def charge_one_bank(bank: int):
    """
    Charges all batteries in one bank.
    """
    BTJ.set_charge_bank(bank)
    BTJ.setup(chargeFlag = True, dischargeFlag = False)

def discharge_one_bank(bank: int):
    """
    Discharges all batteries in one bank.
    """
    BTJ.set_charge_bank(bank)
    BTJ.setup(chargeFlag = False, dischargeFlag = True)

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

#Write bankdata to CSV file.

for x in range(4):
    output_measurements(x) 
    print()
    print("Charging...")
    print()
    charge_one_bank(x)
    print()
    print("Charging complete.")
    print()
    output_measurements(x) 
    print()
    print("Discharging...")
    print()
    discharge_one_bank(x)
    print()
    print("Discharging complete.")
    print()
    output_measurements(x) 
    print()
