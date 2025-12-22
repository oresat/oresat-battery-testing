from enum import Enum
import math
from dataclasses import dataclass
import u6

"""
In the labjack battery data-getting section, does not interact with chargers at all.
Jobs:
A) Hold data required for labjack commands: PINS, 
	i. Have notes about each of the functions (or at least a mention) of the functions we're using such as getAIN()
B) Hold dataclass for collecting temperature and voltage data: class BankData
C) Hold calculation/conversion functions for getting temps and volts: get_actual_temp(), get_data()
D) A general STOP() function for the labjack
"""

#Labjack Command Pins
MEASURE_PINS = [0, 2, 4, 6]
TEMPERATURE_PINS = [8, 9, 10, 11]
VOLTAGE_NEG_PINS = [18, 17, 16, 15]
CHARGE_BANK_PINS = [7, 5, 3, 1]
VOLTAGE_POS_PINS = [37, 36, 35, 34]

#For storing data on a single battery.
@dataclass
class BankData:
    temperature: float
    voltage: float

#Settings Temp/Voltage Measuring, used in get_data...()
class MeasureProfile: 
  resolution = 0
  gain = 0
  settling = 0
  voltage_measure_diff = True
  temp_measure_diff = False

#Conversion function for use in get_data_from_one_cell, gets value in Celsius
def get_actual_temp(self, num) -> float:
  """
  num is the original measurement of a given battery cell, avgTemps. 
  Convert thermistor value to voltage and then to degrees Celsius.
  """ 
  tempRef = 295.15
  betaValue = 3380
  resInitial = 10000
  voltageDefault = 5
  kelvinToCelsius = 273.15

  resistance = resInitial * ((voltageDefault / num) - 1)
  actualTemp = 1/(1/tempRef + 1/betaValue * math.log(resistance/resInitial))
 
  return actualTemp - 273.15

#Returns readable data about a given battery (AKA cell)
def get_data_from_one_cell(self, mp: MeasureProfile, bank: int, cell: int) -> BankData:
  """ 
  cell is 0: A, 1: B, 2: C, 3: D AND so is the BankData index into which we'll append data
  """
 
  temp_pin = TEMPERATURE_PINS[cell]
  volt_pin = MEASURE_PINS[cell]
  data_list = [] #Might not be needed unless we want to return a list rather than a dataclass
 
  #Ensure all banks are unselected
  for pin in MEASURE_PINS:
    u6.getFeedback(u6.BitStateWrite(pin, False))

  #Set the bank we actually want to measure
  u6.getFeedback(u6.BitStateWrite(MEASURE_PINS[bank], True))
  time.sleep(1) #??
 
  ###TEMPERATURE SECTION
  temp_total = float(0)

  for data_point in range(10):
    temp_total += self.u6.get
    avgTemps += u6.getAIN(mp.temp_pin, mp.resolution, mp.gain, mp.settling, mp.temp_measure_diff)
    time.sleep(0.01)
 
  #Get the temperature.
  cell_temp = get_actual_temp(temp_total/10)

  ###VOLTAGE SECTION
  volts_total = float(0)

  for data_point in range(10):
    volts_total += self.u6.getAIN(volt_pin, mp.resolution, mp.again, mp.settling, mp.voltage_measure_diff)
    time.sleep(0.01)

  cell_voltage = volts_total / 10
 
  return BankData(cell_temp, cell_voltage) #This should work instead of the below three lines

#Put BankData received from get_data...() into csv file, this should be done in scribe_backend
                                #to avoid a double-backend mess
"""
        data = BankData(actualTemp, avgVolts)
        timestamp = scribe.stamper()
        scribe.write_to_csv(timestamp, bank, cell, data.temperature, data.voltage)
"""





