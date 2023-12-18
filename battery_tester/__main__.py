from argparse import ArgumentParser
from .libb6 import libb6
import time
import csv
from .battbank import BattLabJack, BatteryBank

#Chargers are labelled on board; strings are usb serial numbers.
#For use with Lev's laptop, bottom right USB port only.
A = "1.2"
B = "1-1.3"
C = "1-4"
D = "1-1.4"


def write_to_csv(date, voltage):
    """
    function takes in timestamp and voltage,
    writes values to csv file,
    "a" appends whereas "w" clears file first
    """
    with open("timestamps.csv", "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([date, voltage])

def clear_csv():
    """
    function clears csv file,
    just scaffolding for now, "w+" truncates the file
    """
    with open("timestamps.csv", "w+", newline="") as csv_file:
        pass


def stamper():
    # function makes a timestamp
    dt = datetime.now()
    iso_date = dt.isoformat()
    return iso_date

###############################################################
#Function devoted to charger tasks.
def charger_main():
    # write code in here as if this is a C++ file int main
    # https://docs.python.org/3/library/argparse.htmlA
	 # look through cfc code to see examples
	print("\nChargers charge things!\n")
	###Charger Things###
	devA = libb6.Device(A)
	devB = libb6.Device(B)
	devC = libb6.Device(C)
	devD = libb6.Device(D)
	#"None" implicitly returned if no return statement	

###############################################################


def measure_volts_temp(battery_pack_num):
	sense_control_pins = (0, 2, 4, 6)
	charge_control_pins = (7, 5, 3, 1)

	blj = BattLabJack(sense_control_pins, charge_control_pins)
	
	bb = BatteryBank(blj, battery_pack_num) #should be 0,1,2, or 3

	bb.measure()
	print(bb.cellVolts)
	print(bb.cellTemps)
	

def labjack_main():
	sense_control_pins = (0, 2, 4, 6)
	charge_control_pins = (7, 5, 3, 1)

	blj = BattLabJack(sense_control_pins, charge_control_pins)

	bb = BatteryBank(blj, 3)

	bb.measure()
	print(bb.cellVolts)
	print(bb.cellTemps)

###############################################################
	
"""
    parser = ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "integers", metavar="N", type=int, nargs="+", help="an integer for the accumulator"
    )
    parser.add_argument(
        "--sum",
        dest="accumulate",
        action="store_const",
        const=sum,
        default=max,
        help="sum the integers (default: find the max)",
    )

    args = parser.parse_args()
    print(args.accumulate(args.integers))
    print("hello world")
"""
#if this module is not from an import statement (thus making it the top level module),
#then run it - importantly, any code not in this document (top level module) will not run
if __name__ == "__main__":
	charger_main()
	while (True):	
		check = int(input("0--> Oops, didn't mean to run this. Please exit.\n1--> Run chargers.\n2--> Run labjack.\n3--> Run both.\nUp to you, good sir: "))
		if check == 0:
			break;
		if check == 1:
			charger_main()
			break
		elif check == 2:
			labjack_main()
			break	
		elif check == 3:
			charger_main()
			labjack_main()
			break
		else:
			print("Error, read the instructions again.\n") 
		
		



	
