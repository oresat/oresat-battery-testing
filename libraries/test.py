import b6mini
#Disambiguate chargers via USB slot
"""
import serial
import serial.tools.list_ports

def __init__(self, name: str):
    '''construct object, pass in usb device name. ttyA/ttyB/ttyC/ttyD'''
    serial_port = None
    for i in serial.tools.list_ports.comports():
        if i.name == name:
            serial_port = i.device
            break
        if serial_port is None:
            raise Exception(f'Could not find device with id of {name}')

        self.ser = serial.Serial(
                port=serial_port,
                baudrate = self.BAUDRATE,
                parity = self.PARITY,
                stopbits = self.STOPBITS,
                bytesize = self.BYTESIZE,
                timeout = self.TIMEOUT,
                )
"""
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

#each charger only charges one cell at a time
