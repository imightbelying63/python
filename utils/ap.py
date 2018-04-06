import sys
import argparse as ap
p = ap.ArgumentParser()
p.add_argument("-v", "--verbose", help="increase output", action="store_true")
p.add_argument("-V", "--version", help="print version and exit", action="store_true")

args = p.parse_args()

if args.version:
    print("version 0.63")
    sys.exit(0)

if args.verbose:
    print("you did it")
