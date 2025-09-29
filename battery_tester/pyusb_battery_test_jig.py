import u6

from dataclasses import dataclass
from enum import Enum
import usb.core
import usb.util
import sys

#Index is the bank ID
MEASURE_PINS = [0, 2, 4, 6]
TEMPERATURE_PINS = [8, 9, 10, 11]
VOLTAGE_NEG_PINS = [18, 17, 16, 15]
CHARGE_BANK_PINS = [7, 5, 3, 1]
VOLTAGE_POS_PINS = [37, 36, 35, 34]

#Boolean?
class ChargeMode(Enum):
    CHARGE = 0
    DISCHARGE = 1

#Also note that I don't think these USB paths are correct in the slightest.
#Note that charger X corresponds to Battery Slot/Cell X.
CHARGERS = [
    "1-1.4",#A
    "1-2",#B
    "1-3",#C
    "1-4" #D
]

class BatteryTester:

  def __init__(self, ids: list[str]):
    print(f'{ids=}')
    # preconditions : ids must be valid usb paths, tested in libb6
    # postconditions: 
    self.u6 = u6.U6()
    #self.chargers = [libb6.Device(id) for id in ids]
    self.chargers = []
    for id in ids:
      print(id)
      self.chargers.append(id)#This assumes that we automatically found the correct
                              #serial paths - it does not call the custom constructor

  def setup(self, chargeFlag = False, dischargeFlag = False):
    print(f'{chargeFlag=} {dischargeFlag=}')
    for charger in self.chargers:
      #How to write this in Python
      chargeProfile = libb6.Device.getDefaultChargeProfile(charger, libb6.BATTERY_TYPE.LIIO)
      print(chargeProfile.batteryType, chargeProfile.cellCount)
      
      if chargeFlag == True:
          print("\nFlag == 1. Charging.\n")
          charger.startCharging(chargeProfile)
      else:
          print("\nFlag != 1. Not charging.\n")

      if dischargeFlag == True:
          print("\nCommencing discharge...\n")
          chargeProfile.mode = ChargeMode.DISCHARGE.value
          charger.startCharging(chargeProfile)
      else:
          print("\nNot discharging.\n")

  def stop(self):
    for pin in CHARGE_BANK_PINS:
      self.u6.setDOState(pin, 0)
    for pin in MEASURE_PINS:
      self.u6.setDOState(pin, 0)
    print("\nSTOPPED\n")

BTJ = BatteryTester(CHARGERS)
BTJ.setup(True, False)
BTJ.stop()
