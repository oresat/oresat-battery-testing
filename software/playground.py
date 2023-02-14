# from liblabjack import LabJack
from battbank import *
import time

sense_control_pins = (0, 2, 4, 6)
charge_control_pins = (7, 5, 3, 1)

blj = BattLabJack(sense_control_pins, charge_control_pins)

bb = BatteryBank(blj, 3)

bb.measure()
print(bb.cellVolts)
print(bb.cellTemps)