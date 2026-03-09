from enum import Enum, unique
import usb.core
import usb.util
import sys
"""
  /**
   * Custom constructor that takes in a port number and then checks each device
   * plugged in via USB until it finds the one that matches said argument port
   * number. Then it opens that one.
   */
  Device::Device(const std::string & location) {
    int loc_i{0};                   // tracker for location index
    int path_i{0};                  // tracker for path index
    libusb_device *b6dev = nullptr; // check if we've b6dev the correct charger
    libusb_device *dev = nullptr;   /* changed this to nullptr */
    libusb_device **devs;
    int i = 0;
    uint8_t path[8];     // the device we're on
    uint8_t loc_path[8]; // the device we want

    // Put string nums into path array.
    while (location[loc_i]) {
      if (location[loc_i] != '.' && location[loc_i] != '-') {
        int to_add = location[loc_i] - '0';
        loc_path[path_i] = to_add;
        ++loc_i;
         ++path_i;
      } else {
        ++loc_i;
      }
    }
"""

from dataclasses import dataclass

# Kosher commands to write to the chargers, taken from Libb6 Enum.hh
@unique
class Command(Enum):
    GET_DEV_INFO = 0x57,
    GET_SYS_INFO = 0x5A,
    GET_CHARGE_INFO = 0x55,
    UNK1 = 0x5F,
    STOP_CHARGING = 0xFE

# Lithium ion batteries only. Values copied from Device.cc in /archive/libb6
@dataclass
class ChargeProfile:
    battery_type = "lithium_ion"
    cell_count = 1
    r_peak_count = 3
    cycle_type = 1
    cycle_count = 1
    charge_current = 1500
    discharge_current = 1000
    trickle_current = 0
    cell_discharge_voltage = 3200
    end_voltage = 4200

# This is how we access the chargers. These need to be filled each time by finding the
# correct paths. These are the correct paths when plugged into the USB port on my computer right.


@dataclass
class ChargerSerialPaths:
    A = str("1-1.1.4")
    B = str("1-1.1.2")
    C = str("1-1.1.3")
    D = str("1-1.4")
    # Give this function the correct serial ports for the chargers that you find manually.
    """
    def __init__(self, paths: list[str]):
        print(f'{paths}')
        self.A = paths[0]
        self.B = paths[1]
        self.C = paths[2]
        self.D = paths[3]
        

    def convert_from_string(self, paths: list[str]):


    def path_to_tuple(path):
        return tuple(int(x) for x in path.split("-")[1].split("."))
    """
    """
    while True:
      for x in range(4):
        charger = str(input("\nEnter the serial port exactly for charger: "))
        flag = input((f"Does this look correct?\n{charger}\nY/n: "))
        if flag == 'y' or flag == 'Y':
          self.A = charger
          break
    print(f"Charger A:\n{self.A}\nCharger B:\n{
          self.B}\nCharger C:\n{self.C}\nCharger D:\n{self.D}")

    flag = input((f"Does this look correct? Y/n: "))
    if flag == 'y' or flag == 'Y':
      break
  """

def path_to_tuple(path: str):
    return tuple(int(x) for x in path.split("-")[1].split("."))

# Note that this merely tells the chargers to "do something". By default they will charge.
# To discharge, you will still call this function but you will first set the chargemode to discharge.
########Use lambda to iterate through chargers and find the right path that is entered by user
def start_charging(profile: ChargeProfile, CH1: str) -> bool:#Manually know which charger you are calling
    # This is where pyusb comes into play
    # Realizing that we run into the same problem, no matter what we need to identify which device
    # Once we do that, then we can call this function --> this function should probably
    # be in a class with everything else, but hold that thought
    # Let's assume that we have already located the correct charger device

    # ids are placeholders
    charger1 = usb.core.find(custom_match=lambda d: d.port_numbers == path_to_tuple(CH1))
    #Make sure that usb is not being used for something else
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    print(f"charger1 path is {charger1}")
    """
    devices = usb.core.find(find_all=True)
    for dev in devices:
        # Format: bus-port1.port2.port3...
        path = f"{dev.bus}-{'.'.join(map(str, dev.port_numbers))}"
    if path == "1-1.1.4":
        print("Found device:", dev)
    """
    if charger1 is None:
        raise ValueError("Charger 1 not found!")

    charger1.set_configuration()  # Assumes that there is only 1

    charger1_config = charger1.get_active_configuration()

    charger1_interface = charger1_config[(0, 0)]

    charger1_endpoint = usb.util.find_descriptor(charger1_interface, custom_match=lambda endp:
        usb.util.endpoint_direction(endp.bEndpointAddress) == usb.util.ENDPOINT_OUT)

    # UNK1 appears to be a test where if it is 4, we must stop charging. It is checking if the data
    # is 4 bytes would be my guess
    if charger1_endpoint is not None:
        charger1_endpoint.write(Command.UNK1)  # For now, we're gonna assume that the charger
                                               # corrects for this, we'll test later
        # if (buffer is at 4 (uint8s) so if buffer is at one byte then stop charging)
        # stop charging under certain conditions, might be a safety check
        # might not work if charger needs specific
        charger1_endpoint.write(ChargeProfile.battery_type)  # data type, we'll see
        charger1_endpoint.write(ChargeProfile.cell_count)
        # Not sure what mode is - except that it is tied to battery type, but we only have one type
        charger1_endpoint.write(ChargeProfile.battery_type)
        charger1_endpoint.write(ChargeProfile.charge_current)
        charger1_endpoint.write(ChargeProfile.discharge_current)
        charger1_endpoint.write(ChargeProfile.cell_discharge_voltage)
        charger1_endpoint.write(ChargeProfile.end_voltage)
        charger1_endpoint.write(ChargeProfile.trickle_current)
        # UA? Checksum? See below.
        charger1_endpoint.write([0, 0, 0, 0])  # Figure out what this is for, UA
    else:
        print("The endpoint is null. Something might be disconnected.")


"""
C Code reference
  bool Device::startCharging(ChargeProfile profile) {
    Packet res = m_sendCommand(CMD::UNK1);
    if (res.readU8() == 4) {
      stopCharging();
    }

    Packet cmd({ 0x0f, 0x16, 0x05, 0x00 });
    cmd.writeU8(static_cast<uint8_t>(profile.batteryType));
    cmd.writeU8(profile.cellCount);
    if (isBatteryLi(profile.batteryType)) {
      cmd.writeU8(static_cast<uint8_t>(profile.mode.li));
    } else if (isBatteryNi(profile.batteryType)) {
      cmd.writeU8(static_cast<uint8_t>(profile.mode.ni));
    } else {
      cmd.writeU8(static_cast<uint8_t>(profile.mode.pb));
    }
    cmd.writeU16(profile.chargeCurrent);
    cmd.writeU16(profile.dischargeCurrent);
    cmd.writeU16(profile.cellDischargeVoltage);
    cmd.writeU16(profile.endVoltage);
    if (isBatteryNi(profile.batteryType) && profile.mode.ni >= CHARGING_MODE_NI::REPEAK) {
      if (profile.mode.ni == CHARGING_MODE_NI::REPEAK) {
        cmd.writeU8(profile.rPeakCount);
        cmd.writeU8(0x00);
      } else if (profile.mode.ni == CHARGING_MODE_NI::CYCLE) {
        cmd.writeU8(profile.cycleType);
        cmd.writeU8(profile.cycleCount);
      }
    } else {
      cmd.writeUA({ 0x00, 0x00 });
    }
    cmd.writeU16(profile.trickleCurrent);
    cmd.writeUA({ 0x00, 0x00, 0x00, 0x00 });
    cmd.writeChecksum();

    m_write(cmd);
    m_read(); // TODO: handle return value

    return true;
  }
"""
