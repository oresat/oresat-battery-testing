import b6mini

c = b6mini.Charger()
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
