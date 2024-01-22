from dataclasses import dataclass
import u6
from libb6 import libb6
from typing import List

class Pin(Enum):
    """
    A = Pin.MEASURE_3.value (for example)
    """
    MEASURE_3 = 3 
    MEASURE_2 = 4
    MEASURE_1 = 5
    MEASURE_0 = 6  

    TEMPERATURE_3 = 13
    TEMPERATURE_1 = 14

    VOLTAGE_NEG_3 = 15
    VOLTAGE_NEG_2 = 16
    VOLTAGE_NEG_1 = 17
    VOLTAGE_NEG_0 = 18  

    CHARGE_BANK_3 = 21
    CHARGE_BANK_2 = 22
    CHARGE_BANK_1 = 23
    CHARGE_BANK_0 = 24

    TEMPERATURE_2 = 32
    TEMPERATURE_0 = 33

    VOLTAGE_POS_3 = 34
    VOLTAGE_POS_2 = 35
    VOLTAGE_POS_1 = 36
    VOLTAGE_POS_0 = 37

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

    def set_charge_bank(self, bank: int):
        pass
    
    def get_data(self, bank: int) -> List[BankData]:
        """
        Returns list that contains BankData (temperature and voltage)
        for each cell (which means battery).
        """
        return [BankData(0,0)]
    
jig = BatteryTestJig(CHARGERS)
