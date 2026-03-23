from enum import Enum, unique
import struct
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
    GET_DEV_INFO = 0x57
    GET_SYS_INFO = 0x5A
    GET_CHARGE_INFO = 0x55
    UNK1 = 0x5F
    STOP_CHARGING = 0xFE

# Lithium ion batteries only. Values copied from Device.cc in /archive/libb6
@dataclass
class ChargeProfile:
    battery_type: int = 0x01 #This is the enum value for lithium ion batteries in libb6
    cell_count: int = 1
    r_peak_count: int = 3
    cycle_type: int = 1
    cycle_count: int = 1
    charge_current: int = 1500
    discharge_current: int = 1000
    trickle_current: int = 0
    cell_discharge_voltage: int = 3200
    end_voltage: int = 4200
# This is how we access the chargers. These need to be filled each time by finding the
# correct paths. These are the correct paths when plugged into the USB port on my computer right.

@dataclass
class ChargerSerialPaths:
    A: str = "1-1.1.4"
    B: str = "1-1.1.2"
    C: str = "1-1.1.3"
    D: str = "1-1.4"
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

def send_command(endpoint_out, endpoint_in, cmd):
    packet = bytearray([0x0f, 0x03, cmd.value, 0x00])
    checksum = sum(packet[2:]) & 0xFF
    packet += bytes([checksum, 0xFF, 0xFF])
    endpoint_out.write(packet)
    return endpoint_in.read(64)

def build_start_charging_packet(profile: ChargeProfile) -> bytearray:
    def u16(val):
        return bytes([(val >> 8) & 0xFF, val & 0xFF])

    packet = bytearray([0x0f, 0x16, 0x05, 0x00])
    packet += bytes([profile.battery_type])
    packet += bytes([profile.cell_count])
    packet += bytes([0x00]) #Standard charge mode
    packet += u16(profile.charge_current)
    packet += u16(profile.discharge_current)
    packet += u16(profile.cell_discharge_voltage)
    packet += u16(profile.end_voltage)
    packet += bytes([0x00, 0x00]) #writeua
    packet += u16(profile.trickle_current)
    packet += bytes([0x00, 0x00, 0x00, 0x00])#writeUA
    checksum = sum(packet[2:]) & 0xFF
    packet += bytes([checksum, 0xFF, 0xFF])
    return packet

def start_charging(profile: ChargeProfile, CH1: str) -> bool:
    charger1 = usb.core.find(custom_match=lambda d: d.port_numbers == path_to_tuple(CH1))

    if charger1 is None:
        raise ValueError("Charger 1 not found!")

    if charger1.is_kernel_driver_active(0):
        charger1.detach_kernel_driver(0)

    charger1.set_configuration()#There is only one config for now

    charger1_config = charger1.get_active_configuration()
    charger1_interface = charger1_config[(0, 0)]

    charger1_endpoint = usb.util.find_descriptor(charger1_interface, custom_match=lambda endp:
        usb.util.endpoint_direction(endp.bEndpointAddress) == usb.util.ENDPOINT_OUT)

    charger1_endpoint_in = usb.util.find_descriptor(charger1_interface, custom_match=lambda endp:
        usb.util.endpoint_direction(endp.bEndpointAddress) == usb.util.ENDPOINT_IN)

    if charger1_endpoint is None or charger1_endpoint_in is None:
        print("An endpoint is NULL. Something might be disconnected.")
        return False

    res = send_command(charger1_endpoint, charger1_endpoint_in, Command.UNK1)
    if res[4] == 4:
        send_command(charger1_endpoint, charger1_endpoint_in, Command.STOP_CHARGING)

    cmd = build_start_charging_packet(profile)
    charger1_endpoint.write(cmd)
    charger1_endpoint_in.read(64)

    return True

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
