from libb6 import libb6
import battery_bank_library
from battery_bank_library import BattLabJack
from battery_bank_library import BatteryBank
import labjack_library

#Code pertains to the chargers below this line.
class Battery:
	"""
	Holds chargeProfile of battery hardcoded, for now.
	"""

class Charger:
	"""
	Holds serial numbers of each charger hardcoded.	
	"""
	A = "2.1.4"
	B = "1.2"
	C = "2.3"
	D = "1-2.4"
		
def access(charger_id):
	"""
	Access a charger or return failure.
	Note that the error message is sent by Device.cc in libb6.	
	"""
	dev = libb6.Device(charger_id);
	return dev

def activate_charger():
	"""
	Function will be split up later, likely.
	Catch the device number, then send it to get a profile for the battery in question,
	then print type of battery (should be lio) and cell count (??). Then start charging
	the battery.	
	"""
	catch_dev = access(Charger.B)
	chargeProfile = libb6.Device.getDefaultChargeProfile(catch_dev, libb6.BATTERY_TYPE.LIIO)
	print(chargeProfile.batteryType, chargeProfile.cellCount)
	catch_dev.startCharging(chargeProfile)

#Code pertains to the Labjack below this line.
class LCPs:
	"""
	Holds Labjack control pins.
	"""	
	find = (0, 2, 4, 6)
	charge = (7, 5, 3, 1)

labjack_obj = BattLabJack(LCPs.find, LCPs.charge)	
batterybank_obj = BatteryBank(labjack_obj, 3)

def measure_volts_temp(obj):
	"""
	Measure the volts and temperature of each battery in a given board. Arg is battery_bank_obj.
	"""
	obj.measure()
	print(obj.cellVolts)
	print(obj.cellTemps)

measure_volts_temp(batterybank_obj)


#Rambly (and partially useless) notes below this line.
"""
#.def("startCharging", & b6::Device::startCharging, py::arg("profile"))
#  1. (self: libb6.libb6.Device, profile: libb6.libb6.ChargeProfile) -> bool

.def("getDefaultChargeProfile", [](b6::Device & d, b6::BATTERY_TYPE t) {
	return d.getDefaultChargeProfile(t);
		})

 1. (self: libb6.libb6.Device, arg0: libb6.libb6.BATTERY_TYPE) -> libb6.libb6.ChargeProfile


Rambly NOTES:
Access touches the charger and returns it, send that into startCharging, and then error
because startCharging needs not only dev (returned from Access) but also a "charge profile"

found a function that gets "defaultChargeProfile" and hopefully that's the right one
but for it to work, it needs a parameter called BATTERY_TYPE and BATTERY_TYPE is a class, but
not sure if it wants the whole class or simply something in the class, or the literal type of battery that charger is going to be charging.

Qs: 
Is getDefaultChargeProfile the correct function to get the chargeProfile argument for the startCharging function?

Probably but you should let user change profile settings, and for now you can save it in chargeProfile
liio is correct battery type

Udev rules are updated, and charger B works, but A does not, nor does C 
B is the only one that works, but if everything except for B is unplugged and I run with Charger.D then B works, and it also works with Charger.B

This thing works with Charger B, so I'm just gonna use that one charger for now.
"""




