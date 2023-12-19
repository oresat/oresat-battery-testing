from battery_tester.libb6 import libb6
from battery_tester.battbank import BattLabJack, BatteryBank

###############################################################
#Function devoted to labjack tasks.
#Measure voltage and temperature of each battery.
#Write voltage/temperature/battery_id to csv file.

def battery_bank_from_pack_number(battery_pack_num: int) -> BatteryBank:
	"""
	Measure voltage and temperature of each battery.
	"""
	assert battery_pack_num in range(4), "Unexpected and invalid battery pack number."
	sense_control_pins = (0, 2, 4, 6)
	charge_control_pins = (7, 5, 3, 1)

	blj = BattLabJack(sense_control_pins, charge_control_pins)
	
	return BatteryBank(blj, battery_pack_num) #should be 0,1,2, or 3
