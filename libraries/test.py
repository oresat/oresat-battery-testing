import libb6

dev = libb6.Device("1-1.1")#this keeps seg-faulting meaning that there is
								 #probably an error in the logic in Device.cc (comparing port numbers)
								 #such that even if we have the correct port number
								 #the computer thinks we don't and thus does not open a device

info = dev.getSysInfo()

print(info)

#Disambiguate chargers via USB slot

"""
c = b6mini.Charger([1,2]) #pass in array of port numbers
print(c)
print()

s = c.getSysInfo()
print(s)
print()

ci = c.getChargeInfo()
print(ci)
print()
print("TESTESTEST")

cp = c.getDefaultChargeProfile("LiPo")
print(cp.getTypeString())
print(cp)
cp.chargeCurrent = 128
print(cp)

c.startCharging(cp);

#each charger only charges one cell at a time
"""
