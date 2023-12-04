from argparse import ArgumentParser
from .libb6 import libb6
import time
import csv
from .battbank import *

#Chargers are labelled on board; strings are usb serial numbers.
#For use with Lev's laptop, bottom right USB port only.
A = "1.2"
B = "1-1.3"
C = "1-4"
D = "1-1.4"

#Function devoted to charger tasks.
def charger_main():
    # write code in here as if this is a C++ file int main
    # https://docs.python.org/3/library/argparse.htmlA
	 # look through cfc code to see examples

	###Charger Things###
	devA = libb6.Device(A)
	devB = libb6.Device(B)
	devC = libb6.Device(C)
	devD = libb6.Device(D)
	#None implicitly returned if no return statement	


#Function devoted to labjack tasks.
def labjack_main():

	sense_control_pins = (0, 2, 4, 6)
	charge_control_pins = (7, 5, 3, 1)

	
	blj = BattLabJack(sense_control_pins, charge_control_pins)

	sense_control_pins = (0, 2, 4, 6)
	charge_control_pins = (7, 5, 3, 1)

	blj = BattLabJack(sense_control_pins, charge_control_pins)

	bb = BatteryBank(blj, 3)

	bb.measure()
	print(bb.cellVolts)
	print(bb.cellTemps)
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
	labjack_main()
	
