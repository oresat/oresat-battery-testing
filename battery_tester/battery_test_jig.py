import time
from enum import Enum
import math
import data_to_csv_functions as scribe
from dataclasses import dataclass
from typing import List

import u6
from libb6 import libb6

# Index is the bank ID.
MEASURE_PINS = [0, 2, 4, 6]
TEMPERATURE_PINS = [8, 9, 10, 11]
VOLTAGE_NEG_PINS = [18, 17, 16, 15]
CHARGE_BANK_PINS = [7, 5, 3, 1]
VOLTAGE_POS_PINS = [37, 36, 35, 34]

class ChargeMode(Enum):
    CHARGE = 0
    DISCHARGE = 1

#Note that charger X corresponds to Battery Slot/Cell X.
CHARGERS = [
    "1-1.4",#A
    "1-2",#B
    "1-3",#C
    "1-4" #D
]

@dataclass
class BankData:
    temperature: float
    voltage: float

class BatteryTestJig:
    def __init__(self, ids: List[str]):
        print(f'{ids=}')
        # preconditions : ids must be valid usb paths, tested in libb6
        # postconditions: 
        self.u6 = u6.U6()
        #self.chargers = [libb6.Device(id) for id in ids]
        self.chargers = []
        for id in ids:
            print(id)
            self.chargers.append(libb6.Device(id))
        """Turn off beeps.""" 

        for charger in self.chargers:
            charger.setBuzzers(False, False)
        print("\n\n\nINIT COMPLETE\n\n\n")
    
    def setup(self, chargeFlag = False, dischargeFlag = False):
        # preconditions: none
        # postconditions: 
        print(f'{chargeFlag=} {dischargeFlag=}')
        for charger in self.chargers:
            chargeProfile = libb6.Device.getDefaultChargeProfile(charger, libb6.BATTERY_TYPE.LIIO)
            print(chargeProfile.batteryType, chargeProfile.cellCount)
            
            if chargeFlag == True:
                print("\nFlag == 1. Charging.\n")
                charger.startCharging(chargeProfile)
            else:
                print("\nFlag != 1. Not charging.\n")

            if dischargeFlag == True:
                print("\nCommencing discharge...\n")
                breakpoint()
                chargeProfile.mode = ChargeMode.DISCHARGE.value
                charger.startCharging(chargeProfile)
            else:
                print("\nNot discharging.\n")
    
    def setup_one_charger(self, choice: int, chargeFlag = False, dischargeFlag = False):
        
        print(f'{chargeFlag=} {dischargeFlag=}')
        """
        As setup() but for only one charger, choice is charger:
        Charger is 0: A, 1: B, 2: C, 3: D
        """ 
        chosen_charger = self.chargers[choice]

        chargeProfile = libb6.Device.getDefaultChargeProfile(chosen_charger, libb6.BATTERY_TYPE.LIIO) 
        print(f"Selected Charger {choice} which charges cell {choice}.")

        if chargeFlag == True:
            print("\nFlag == 1. Charging.\n")
            chosen_charger.startCharging(chargeProfile)
        else:
            print("\nFlag != 1. Not charging.\n")

        if dischargeFlag == True:
            print("\nCommencing discharge...\n")
            breakpoint()
            chargeProfile.mode = ChargeMode.DISCHARGE.value
            chosen_charger.startCharging(chargeProfile)
        else:
            print("\nNot discharging.\n")

    def stop(self):
        """
        Stop charging and measuring.
        """
        for pin in CHARGE_BANK_PINS:
            self.u6.setDOState(pin, 0)

        for pin in MEASURE_PINS:
            self.u6.setDOState(pin, 0)
        print("\nSTOPPED.\n")

    def set_charge_bank(self, bank: int):
        """
        Selects the bank to charge.
        """
        if bank < 0 or bank > 3:
            raise ValueError("Bank ID is invalid.")
        for pin in CHARGE_BANK_PINS:
            self.u6.getFeedback(u6.BitStateWrite(pin, False))
        self.u6.getFeedback(u6.BitStateWrite(CHARGE_BANK_PINS[bank], True))

    def get_actual_temp(self, num) -> float:
        """
        num is the original measurement of a given battery cell, avgTemps. 
        Convert thermistor value to voltage and then to degrees Celsius.
        """ 
        tempRef = 295.15
        betaValue = 3380
        resInitial = 10000
        voltageDefault = 5
        kelvinToCelsius = 273.15

        resistance = resInitial * ((voltageDefault / num) - 1)
        actualTemp = 1/(1/tempRef + 1/betaValue * math.log(resistance/resInitial))
       
        return actualTemp - 273.15
    
    def get_data(self, bank: int) -> List[BankData]:
        """
        Returns list that contains BankData (temperature and voltage)
        for each cell (which means battery).
        """
        data_list = []
        resolution = 0
        gain = 0
        settling = 0
        voltage_measure_diff = True
        temperature_measure_diff = False

        for pin in MEASURE_PINS:
            self.u6.getFeedback(u6.BitStateWrite(pin, False))
        self.u6.getFeedback(u6.BitStateWrite(MEASURE_PINS[bank], True))
        time.sleep(1)

        for temp_pin, volt_pin in zip(TEMPERATURE_PINS, MEASURE_PINS):
            avgTemps = 0.0
            for x in range(10):
                avgTemps += self.u6.getAIN(temp_pin, resolution, gain, settling, temperature_measure_diff)
                time.sleep(0.01)
            avgTemps = avgTemps / 10
            actualTemp = self.get_actual_temp(avgTemps)

            avgVolts = 0.0
            for x in range(10):
                avgVolts += self.u6.getAIN(volt_pin, resolution, gain, settling, voltage_measure_diff)
                time.sleep(0.01)
            avgVolts = avgVolts / 10
             
            data = BankData(actualTemp, avgVolts)
            data_list.append(data)

        return data_list
    
    def get_data_from_one_cell(self, bank: int, cell: int) -> BankData:
        """ 
        As get_data() but for only one battery cell:
        cell is 0: A, 1: B, 2: C, 3: D AND so is the BankData index into which we'll append data
        """
         
        data_list = []
        resolution = 0
        gain = 0
        settling = 0
        voltage_measure_diff = True
        temperature_measure_diff = False

        temp_pin = TEMPERATURE_PINS[cell]
        volt_pin = MEASURE_PINS[cell]

        for pin in MEASURE_PINS: 
            self.u6.getFeedback(u6.BitStateWrite(pin, False))
        self.u6.getFeedback(u6.BitStateWrite(MEASURE_PINS[bank], True))
        time.sleep(1)

        avgTemps = 0.0 
        for x in range(10):
            avgTemps += self.u6.getAIN(temp_pin, resolution, gain, settling, temperature_measure_diff)
            time.sleep(0.01)
        avgTemps = avgTemps / 10
        actualTemp = self.get_actual_temp(avgTemps)

        avgVolts = 0.0
        for x in range(10):
            avgVolts += self.u6.getAIN(volt_pin, resolution, gain, settling, voltage_measure_diff)
            time.sleep(0.01)
        avgVolts = avgVolts / 10
        
        data = BankData(actualTemp, avgVolts)
        timestamp = scribe.stamper()
        scribe.write_to_csv(timestamp, bank, cell, data.temperature, data.voltage)

        return data
    
    #Write test_script functions here, they can call other BTJ functions. 
    def ryan(self):
        self.get_data(3)

# Scaffolding GUI for testing purposes.
if __name__  == "__main__":
    dischargeFlag = 0
    chargeFlag = int(input("Do you want to begin charging batteries?\n0: No.\n1: Yes\nInput: "))
    if chargeFlag == False:
        dischargeFlag = int(input("Would you like to discharge?\n0: No.\n1: Yes\nInput:  "))
        if dischargeFlag == True:
            print("\nCommencing discharge...\n")
        else:
            print("\nAye, will not discharge.\n")

    chargeChoice = int(-1)
    while chargeChoice != 0 and chargeChoice != 1 and chargeChoice != 2 and chargeChoice != 3:
        chargeChoice = int(input("\nSet bank to charge (0, 1, 2, or 3).\nInput: "))
        if chargeChoice != 0 and chargeChoice != 1 and chargeChoice != 2 and chargeChoice != 3:
            print("Bank out of bounds. Choose 0, 1, 2, or 3. It ain't that difficult!\n")

    senseChoice = int(-1)
    while senseChoice != 0 and senseChoice != 1 and senseChoice != 2 and senseChoice != 3:
        senseChoice = int(input("\nSet bank to read temp/volts from (0, 1, 2, or 3).\nInput: "))
        if senseChoice != 0 and senseChoice != 1 and senseChoice != 2 and senseChoice != 3:
            print("Bank out of bounds. Choose 0, 1, 2, or 3. It ain't that difficult!\n")

    sleepTimeChoice = float(input("\nNumber of seconds before program terminates.\nInput: "))

    jig = BatteryTestJig(CHARGERS)
    
    jig.setup(chargeFlag, dischargeFlag)

    jig.set_charge_bank(chargeChoice)

    data = jig.get_data(senseChoice)
    for i in data:
        print(f"Temperature: {i.temperature}")
        print(f"Voltage: {i.voltage}")
        print()

    time.sleep(sleepTimeChoice)
    jig.stop()
"""
scribe.clear_csv()
jig = BatteryTestJig(CHARGERS)
jig.setup_one_charger(3, False, False)
data = jig.get_data_from_one_cell(3, 3)
print(f"Temperature: {data.temperature}\nVoltage: {data.voltage}\n")
jig.stop
"""

