import serial
import serial.tools.list_ports

VENDOR_ID = 0x2e8a
PRODUCT_ID = 0x0005

for i in serial.tools.list_ports.comports():
    if i.vid != VENDOR_ID or i.pid != PRODUCT_ID:
        continue

    print(f'/dev/{i.name} {i.location.split(":")[0]}\n')
    print(f"{i.device_path}")
