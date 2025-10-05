#Include things like ChargingProfile (a dataclass makes sense for this)
#You will need a number of features from Device.hh/cc to work for you - you can write them
  #in Python pretty easily. Then use em in conjunction with either pyusb->chargers or 
                                                                  #u6->labjack
  #You basically have two somewhat separate control tracks


from dataclasses import dataclass

#Lithium ion batteries only. Values copied from Device.cc in /archive/libb6
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

def start_charging(profile: ChargeProfile) -> bool:
  #This is where pyusb comes into player
  #Realizing that we run into the same problem, no matter what we need to identify which device
  #Once we do that, then we can call this function --> this function should probably
  #be in a class with everything else, but hold that thought
  #Let's assume that we have already located the correct charger device

  #ids are placeholders
  charger1 = usb.core.find(idVendor = 0x0000, idProduct = 0x0000)
  
  if charger1 is None:
    raise ValueError("Charger 1 not found!")
  
  charger1.set_configuration()#Assumes that there is only 1

  charger1_config = charger1.get_active_configuration()

  charger1_interface = charger1_config[(0,0)] 

  charger1_endpoint = usb.util.find_descriptor(charger1_interface, custom_match = lambda endp:
                                            usb.util.endpoint_direction(endp.bEndpointAddress)
                                            == usb.util.ENDPOINT_OUT)

  if charger1_endpoint is not None:
    charger1_endpoint.write("Some command to start charging.")
    charger1_endpoint.write(ChargeProfile.battery_type)#might not work if charger needs specific
                                                       #data type, we'll see
    charger1_endpoint.write(ChargeProfile.cell_count)
    #Not sure what mode is - except that it is tied to battery type, but we only have one type
    charger1_endpoint.write(ChargeProfile.battery_type)
    charger1_endpoint.write(ChargeProfile.charge_current)
    charger1_endpoint.write(ChargeProfile.discharge_current)
    charger1_endpoint.write(ChargeProfile.cell_discharge_voltage)
    charger1_endpoint.write(ChargeProfile.end_voltage)
    charger1_endpoint.write(ChargeProfile.trickle_current)
    #UA? Checksum? See below.
    charger1_endpoint.write([0,0,0,0])#Figure out what this is for, UA
  else:
    print("The endpoint is null.")

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
