from battery_test_jig import CHARGERS, BatteryTestJig

BTJ = BatteryTestJig(CHARGERS)

#Charge one battery until it reaches 3.6V.
#Measure voltage/temperature every second.
#Once voltage >= 3.6, stop charging, then begin discharging. Measure every second.
#Display completion message.

def full_test_one_battery(bank: int, cell: int):
    #Begin charging.
    BTJ.setup_one_charger(bank, chargeFlag = True, dischargeFlag = False)
    BTJ.set_charge_bank(bank)
    while True:
        """
        Loop breaks once the battery reaches 4.2V.
        """ 
        data = BTJ.get_data_from_one_cell(bank, cell)
        if data.voltage >= 4.2:
            BTJ.stop()
            print("Charge complete.\n")
            break

    #Begin discharging. 
    BTJ.setup_one_charger(bank, chargeFlag = False, dischargeFlag = True)
    BTJ.set_charge_bank(bank)
    print("Begin discharging.\n")
    while True:
        """
        Loop breaks once battery reaches 3.0V.
        """
        data = BTJ.get_data_from_one_cell(bank, cell)
        if data.voltage <= 3.0:
            BTJ.stop()
            break

print("Full test one battery. Enter bank (0 to 3). Enter cell.\n")
bankInput = int(input("Bank ID: "))
print()
cellInput = int(input("Cell ID: "))
print()
print("FULL POWER TO THE TESTING BAY! LESGO!\n")

try:
    full_test_one_battery(bankInput, cellInput)  
finally:
    BTJ.stop()
    print("Stop successful.\n")
