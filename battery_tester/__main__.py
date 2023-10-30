from argparse import ArgumentParser
import .libb6

def main():
    # write code in here as if this is a C++ file int main
    # https://docs.python.org/3/library/argparse.htmlA
	 # look through cfc code to see examples
	devA = libb6.Device(1-2)
	devB = libb6.Device(1-1.3)
	devC = libb6.Device(1-4)
	devD = libb6.Device(1-1.4)

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

if __name__ == "__main__":
    main()
