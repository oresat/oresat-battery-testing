import libb6


x = libb6.BATTERY_TYPE.LIPO
print(x);
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
