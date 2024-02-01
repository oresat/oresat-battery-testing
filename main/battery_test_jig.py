from dataclasses import dataclass
import u6
import time
from libb6 import libb6
from typing import List

#Index is the bank ID.
MEASURE_PINS = [6, 5, 4, 3]
TEMPERATURE_PINS = [33, 14, 32, 13]
VOLTAGE_NEG_PINS = [18, 17, 16, 15]
CHARGE_BANK_PINS = [24, 23, 22, 21]
VOLTAGE_POS_PINS = [37, 36, 35, 34]

CHARGERS = [
#"2.1.4", 
"1.2",
#"2.3",
#"1-2.4"
]

@dataclass
class BankData:
    temperature: float
    voltage: float

class BatteryTestJig:
    def __init__(self, ids: List[str]):
        self.u6 = u6.U6()        
        self.chargers = [libb6.Device(id) for id in ids]
        for charger in self.chargers:    
            chargeProfile = libb6.Device.getDefaultChargeProfile(charger, libb6.BATTERY_TYPE.LIIO)
            print(chargeProfile.batteryType, chargeProfile.cellCount)
            charger.startCharging(chargeProfile)

    def stop(self):
        for pin in CHARGE_BANK_PINS:
            self.u6.getFeedback(u6.BitStateWrite(pin, False))

        for pin in MEASURE_PINS:
            self.u6.getFeedback(u6.BitStateWrite(pin, False))

    def set_charge_bank(self, bank: int):
        if bank < 0 or bank > 3:
            raise ValueError("Bank ID is invalid.")
        for pin in CHARGE_BANK_PINS:
            self.u6.getFeedback(u6.BitStateWrite(pin, False))
        self.u6.getFeedback(u6.BitStateWrite(CHARGE_BANK_PINS[bank], True))

    def get_data(self, bank: int) -> List[BankData]:
        """
        Returns list that contains BankData (temperature and voltage)
        for each cell (which means battery).
        """
        for pin in TEMPERATURE_PINS:
            avgTemps = 0.0 
            for x in range(10):
                avgTemps += self.u6.getAIN(pin, resolution, gain, settling, diff)
                time.sleep(0.01)
            avgTemps = avgTemps / 10
        for pin in VOLTAGE_POS_PINS:
            avgVolts = 0.0
            for x in range(10):
                avgVolts += self.u6.getAIN(pin, resolution, gain , settling, diff)
                time.sleep(0.01)
            avgVolts = avgVolts / 10
            #BankData[pin] = avgVolts #is this a legal line?
            
            """
            Implement this - take four or however many readings back to back and then average them,
            for voltage and temperature.
            for avi in range(avgCount):
                time.sleep(delay)
                av += self.lj.analogRead(cellNum * 2, settling=1, diff=True)
                atv = self.lj.analogRead(cellNum + 8)
                at += atv
            self.cellVolts[cellNum] = av / avgCount
            self.cellTemps[cellNum] = at / avgCount
            """
        return [BankData(avgTemps,avgVolts)]

    
jig = BatteryTestJig(CHARGERS)

jig.set_charge_bank(3)

jig.stop()





