"""
Driver for SkyRC B6 battery chargers.

Mostly a rewrite of https://github.com/maciek134/libb6 in Python

NOTE: This contains a lot of magic values as most of this info was originally found from Wireshark.
"""

import struct
from dataclasses import dataclass
from enum import IntEnum
from typing import ClassVar, List, Union

import serial

_MAX_CELLS = 8


class BatteryType(IntEnum):
    LIPO = 0x0
    LIIO = 0x1
    LIFE = 0x2
    LIHV = 0x3
    NIMH = 0x4
    NICD = 0x5
    PB = 0x5

    @property
    def is_battery_li(self) -> bool:
        return self.type in [self.LIPO, self.LIIO, self.LIFE, self.LIHV]

    @property
    def is_battery_ni(self) -> bool:
        return self.type in [self.LIPO, self.NICD]


class ChargeModeLi(IntEnum):
    """Charge modes for Litium batteries."""

    STANDARD = 0x0
    DISCHARGE = 0x1
    STORAGE = 0x2
    FAST = 0x3
    BALANCE = 0x4


class ChargeModeNi(IntEnum):
    """Charge modes for Nickle batteries."""

    STANDARD = 0x0
    AUTO = 0x1
    DISCHARGE = 0x2
    REPEAK = 0x3
    CYCLE = 0x4


class ChargeModePb(IntEnum):
    """Charge modes for Lead batteries."""

    CHARGE = 0x0
    DISCHARGE = 0x1


ChargeMode = Union[ChargeModeLi, ChargeModeNi, ChargeModePb]


class State(IntEnum):
    """Charge state."""

    CHARGING = 0x1
    ERROR_1 = 0x2
    COMPILE = 0x3
    ERROR_2 = 0x4


class Error(IntEnum):
    """Error code from B6."""

    CONNECTION_BROKEN_1 = 0x000B
    CELL_VOLTAGE_INVALID = 0x000C
    BALANCE_CONNECTION = 0x000D
    NO_BATTERY = 0x000E
    CELL_NUMBER_INCORRECT = 0x000F
    CONNECTION_MAIN_PORT = 0x0010
    BATTERY_FULL = 0x0011
    CHARGE_NOT_NEEDED = 0x0012
    CELL_HIGH_VOLTAGE = 0x0013
    CONNECTION_BROKEN_2 = 0x0014
    CONNECTION_BROKEN_3 = 0x0015
    CONNECTION_BROKEN_4 = 0x0016
    INT_TEMP_TOO_HIGH = 0x0100
    EXT_TEMP_TOO_HIGH = 0x0200
    DC_IN_TOO_LOW = 0x0300
    DC_IN_TOO_HIGH = 0x0400
    OVER_TIME_LIMIT = 0x0500
    OVER_CAPACITY_LIMIT = 0x0600
    REVERSE_POLARITY = 0x0700
    CONTROL_FAIL = 0x0800
    BREAK_DOWN = 0x0900
    INPUT_FAIL = 0x1000
    UNKNOWN = 0xFFFF


@dataclass
class SystemInfo:
    _FMT: ClassVar[str] = "4xB?HBH2BH2xBH"

    cycle_time: int
    time_limit_on: bool
    time_limit: int
    cap_limit_on: bool
    key_buzzer: bool
    system_buzzer: bool
    low_dc_limit: int
    temp_limit: int
    voltage: int
    cells: List[int]

    @classmethod
    def unpack(cls, raw: bytes):
        data = struct.unpack(cls._FMT, raw[:-_MAX_CELLS])
        return SystemInfo(*data[:-_MAX_CELLS], data[-_MAX_CELLS:])


@dataclass
class ChargeInfo:
    _FMT: ClassVar[str] = "4xB3H2BH8H"

    state: State
    temp_ext: int
    temp_int: int
    capacity: int
    time: int
    voltage: int
    current: int
    impendance: int
    cells: List[int]

    @classmethod
    def unpack(cls, raw: bytes):
        data = struct.unpack(cls._FMT, raw[:-_MAX_CELLS])
        state = State[data[0]]
        return ChargeInfo(state, *data[1:-_MAX_CELLS], data[-_MAX_CELLS:])


@dataclass
class ChargeProfile:

    battery_type: BatteryType
    cell_count: int
    r_peak_count: int
    cycle_type: int
    cycle_count: int
    mode: ChargeMode
    charge_current: int
    dischargeCurrent: int
    cell_discharged_voltage: int
    end_voltage: int
    trickle_current: int

    @classmethod
    def default(cls, btype: BatteryType):
        """Make the default charge profile for specific battery type."""

        if btype.is_battery_li:
            mode = ChargeModeLi.STANDARD
        elif btype.is_battery_ni:
            mode = ChargeModeNi.STANDARD
        else:
            mode = ChargeModePb.CHARGE

        trickle_current = 0
        if btype == BatteryType.LIPO:
            cell_discharged_voltage = 3200
            end_voltage = 4200
        elif btype == BatteryType.LIIO:
            cell_discharged_voltage = 3100
            end_voltage = 4200
        elif btype == BatteryType.LIFE:
            cell_discharged_voltage = 2900
            end_voltage = 3700
        elif btype in [BatteryType.LIHV, BatteryType.NIMH]:
            cell_discharged_voltage = 1100
            end_voltage = 4
        elif btype == BatteryType.NICD:
            cell_discharged_voltage = 1800
            end_voltage = 0
            trickle_current = 300
        elif btype == BatteryType.PB:
            end_voltage = 11_000
            trickle_current = 12_000

        return ChargeProfile(
            Battery_type=btype,
            cell_count=1,
            r_peak_count=3,
            cell_count=1,
            cycle_count=1,
            mode=mode,
            charge_current=1500,
            dischargeCurrent=1000,
            trickle_current=trickle_current,
            cellDischargeVoltage=cell_discharged_voltage,
            end_voltage=end_voltage,
        )


class B6:

    def __init__(self, path: str):
        self._ser = serial.Serial(path, timeout=0.2)

        # get device info
        raw = self._send_cmd("\x0f\x03\x57\x00")
        data = struct.unpack("5x6sB?HB3B", raw)
        self.core_type = data[0]
        self.upgrade_type = data[1]
        self.is_encyrpted = data[2]
        self.customer_id = data[3]
        self.language_id = data[4]
        self.sw_version = float(data[5] + data[6]) / 100
        self.hw_version = float(data[7])

    def _send_cmd(self, raw: bytes) -> bytes:

        # add checksum and end of message bytes
        checksum = 0
        for i in raw[2:]:
            checksum += i
        checksum %= 255  # uint8
        raw += checksum + b"\xff\xff"

        self._ser.write(raw)
        return self._ser.read(64)

    def get_sys_info(self) -> SystemInfo:
        raw = self._send_cmd("\x0f\x03\x5a\x00")
        return SystemInfo.unpack(raw)

    def get_charge_info(self) -> ChargeInfo:
        raw = self._send_cmd("\x0f\x03\x55\x00")
        return ChargeInfo.unpack(raw)

    def set_cycle_time(self, value: int):
        if value < 1 or value > 60:
            raise ValueError("invalid input")
        self._send_cmd(b"\x0f\x05\x11\x00\x00")

    def set_time_limit(self, value: int, enabled: bool):
        if value < 1 or value > 720:
            raise ValueError("invalid input")
        raw = b"\x0f\x07\x11\x01\x00"
        raw += struct.pack("BH", enabled, value)
        self._send_cmd(raw)

    def set_capcity_limit(self, value: int, enabled: bool):
        if value < 100 or value > 50_000:
            raise ValueError("invalid input")
        raw = b"\x0f\x07\x11\x02\x00"
        raw += struct.pack("BH", enabled, value)
        self._send_cmd(raw)

    def set_temperature_limit(self, value: int):
        if value < 20 or value > 80:
            raise ValueError("invalid input")
        raw = b"\x0f\x05\x11\x05\x00"
        raw += struct.pack("B", value)
        self._send_cmd(raw)

    def set_buzzers(self, system: bool, key: bool):
        raw = b"\x0f\x06\x11\x03\x00"
        raw += struct.pack("2B", key, system)
        self._send_cmd(raw)

    def stop_charging(self):
        self._send_cmd("\x0f\x03\xfe\x00")

    def start_charging(self, profile):
        res = self._send_cmd("\x0f\x03\5f\x00")
        if res == 4:  # from libb6
            self.stop_charging()

        if profile.mode.is_battery_li:
            mode = ChargeMode.LI
        elif profile.mode.is_battery_ni:
            mode = ChargeMode.LI
        else:
            mode = ChargeMode.PB

        # deal with extra fields for NI batteries
        option_1 = 0
        option_2 = 0
        if profile.mode.is_battery_ni:
            if mode == ChargeModeNi.REPEAK:
                option_1 = profile.r_peak_count
            elif mode == ChargeModeNi.CYCLE:
                option_1 = profile.cycle_type
                option_2 = profile.cycle_count

        raw = b"\x0f\x16\x05\x00"
        raw += struct.pack(
            "3B4H2BH",
            profile.battery_type,
            profile.cell_count,
            profile.mode.value,
            mode,
            profile.charge_current,
            profile.discharge_current,
            profile.cell_discharged_voltage,
            profile.end_voltage,
            option_1,
            option_2,
            profile.trickle_current,
        )
        raw += b"\x00" * 4
        self._send_cmd(raw)


if __name__ == "__main__":
    b6 = B6("/dev/ttyACM0")
    print(b6.core_type)
