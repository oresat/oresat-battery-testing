import battery_test_jig
import jig_functions as jF

"""
One bank at a time, measure all batteries, charge all batteries, then measure all batteries, then discharge all batteries, then measure all batteries.
"""

BTJ = battery_test_jig.BatteryTestJig

for bank in range(4):
    jF.output_measurements(BTJ, bank) 
    print()
    print("Charging...")
    print()
    jF.charge_one_bank(BTJ, bank)
    print()
    print("Charging complete.")
    print()
    jF.output_measurements(BTJ, bank) 
    print()
    print("Discharging...")
    print()
    jF.discharge_one_bank(BTJ, bank)
    print()
    print("Discharging complete.")
    print()
    jF.output_measurements(BTJ, bank) 
    print()
