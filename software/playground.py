# from liblabjack import LabJack
from battbank import *
import time

sense_control_pins = (0, 2, 4, 6)
charge_control_pins = (7, 5, 3, 1)

blj = BattLabJack(sense_control_pins, charge_control_pins)

bb = BatteryBank(blj, 3)

bb.measure()
print(bb.cellVolts)
print(bb.cellTemps)

#blame Lev below this line
from datetime import datetime
import csv

#function takes in timestamp and voltage, writes values to csv file, "a" appends whereas "w" clears file first
def write_to_csv(date, voltage):
    with open("timestamps.csv", "a", newline = "") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([date, voltage])
        #writer.writerow("\n")

#function clears csv file, just scaffolding for now, "w+" truncates the file
def clear_csv(): 
    with open("timestamps.csv", "w+", newline = "") as csv_file:
        pass

#function makes a timestamp
def stamper():
    dt = datetime.now()
    iso_date = dt.isoformat()
    return iso_date

check = input("Do you want to clear the csv file, good sir? \nY/n: ")
if (check.upper == 'Y'):
    clear_csv()

for x in range(5):
    #time.sleep(1)
    voltage = bb.cellVolts 
    date = stamper()
    print(str(voltage))
    print(str(date))
    write_to_csv(date, voltage)
    #/home/lev/oresat-battery-testing/timestamps.csv