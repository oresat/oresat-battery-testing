jmport time
import math
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

CHARGERS = [
    # "2.1.4",
    "1.2",
    # "2.3",
    # "1-2.4"
]

"""
Battery bank 3 and 2 work with this code. There is a problem with battery bank 3 where I only get
two resistance readings and one is a very negative value which makes no sense.
Possible hardware problem. 

"""

@dataclass
class BankData:
    temperature: float
    voltage: float


class BatteryTestJig:
    def __init__(self, ids: List[str], flag):
        self.u6 = u6.U6()
        self.chargers = [libb6.Device(id) for id in ids]
        for charger in self.chargers:
            chargeProfile = libb6.Device.getDefaultChargeProfile(charger, libb6.BATTERY_TYPE.LIIO)
            print(chargeProfile.batteryType, chargeProfile.cellCount)

            charger.setBuzzers(False, False)
            
            if flag == True:
                charger.startCharging(chargeProfile)
                print("\nFlag == 1. Charging.\n")
            else:
                print("\nFlag != 1. Not charging.\n")

    def stop(self):
        """
        Stop charging and measuring.
        """
        for pin in CHARGE_BANK_PINS:
            self.u6.setDOState(pin, 0)

        for pin in MEASURE_PINS:
            self.u6.setDOState(pin, 0)

    def set_charge_bank(self, bank: int):
        """
        Selects the bank to charge.
        """
        if bank < 0 or bank > 3:
            raise ValueError("Bank ID is invalid.")
        for pin in CHARGE_BANK_PINS:
            self.u6.getFeedback(u6.BitStateWrite(pin, False))
        self.u6.getFeedback(u6.BitStateWrite(CHARGE_BANK_PINS[bank], True))
    
    def get_actual_temp(self, num):
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
        print(f"Resistance (R) = {resistance}")
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
            actualTemp = jig.get_actual_temp(avgTemps)

            avgVolts = 0.0
            for x in range(10):
                avgVolts += self.u6.getAIN(volt_pin, resolution, gain, settling, voltage_measure_diff)
                time.sleep(0.01)
            avgVolts = avgVolts / 10
             
            data = BankData(actualTemp, avgVolts)
            data_list.append(data)

        return data_list


# Scaffolding GUI for testing purposes.
flag = int(input("Do you want to begin charging batteries?\n0: No.\n1: Yes\nInput: "))

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

jig = BatteryTestJig(CHARGERS, flag)

jig.set_charge_bank(chargeChoice)

data = jig.get_data(senseChoice)
for i in data:
    print(f"Temperature: {i.temperature}")
    print(f"Voltage: {i.voltage}")
    print()

time.sleep(sleepTimeChoice)
jig.stop()
