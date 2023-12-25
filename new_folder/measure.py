from libb6 import libb6
import battery_bank_library
import labjack_library

######################################################################
#Serial numbers for each battery charger (titled on board A, B, C, D):  
#A is 1.2                                                            
#B is 1-1.3                                                          
#C is 1-4                                                            
#D is 1-1.4                                                          
######################################################################

class Charger:
	"""
	Holds serial numbers hardcoded.	
	"""
	A = "1.2"
	B = "1-1.3"
	C = "1-4"
	D = "1-1.4"
		
def access(charger_id):
	"""
	Access a charger or return failure.
	Note that the error message is sent by Device.cc in libb6.	
	"""
	dev = libb6.Device(charger_id);
	return dev


catch_dev = access(Charger.A)


chargeProfile = libb6.Device.getDefaultChargeProfile(catch_dev, libb6.BATTERY_TYPE)
#libb6.Device.startCharging(access(Charger.A), """charge profile""")

#.def("startCharging", & b6::Device::startCharging, py::arg("profile"))
#  1. (self: libb6.libb6.Device, profile: libb6.libb6.ChargeProfile) -> bool

"""
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

If so, what/where do I get the BATTERY_TYPE argument from?
"""


