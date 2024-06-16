import usb

busses = usb.busses()
"""
for bus in busses:

    devices = bus.devices

    for dev in devices:

        if dev.idVendor == 0x0000 and dev.idProduct == 0x0001:

            print("Device:", dev.address)
"""
x = usb.core.show_devices(verbose = True, idVendor = 0, idProduct = 1)

print(x)
