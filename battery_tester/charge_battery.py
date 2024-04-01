import battery_test_jig
from libb6 import libb6

"""
set charge bank
choose batteries to charge
set charge time - need to stop at a certain voltage
"""

BTJ = battery_test_jig.BatteryTestJig

def charge_one_battery(bank: int, cell: int):
   BTJ.set_charge_bank(BTJ, bank)

def charge_one_bank(bank: int, voltage: int, chargeMode):
    BTJ.set_charge_bank(BTJ, bank)
    #set voltage to charge to via:
    #profile.cellDischargeVoltage = 3100;
    #profile.endVoltage = 4200;
    #Device.cc line 448
