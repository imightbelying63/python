"""adding functionality for CLI args"""

import argparse

parser = argparse.ArgumentParser(description="Iterates over all possible cPanel update blockers, and informs when one is present")
parser.add_argument("--skip-rpm-check", help="RPM check adds wait time, if you're positive RPM is working, skip this to increase the speed at which this script runs", action="store_true")
parser.add_argument("--raw", help="Doesn't attempt to fill the customer reply in, simply delivers the output of any given blocker")
parsrer.add_argument('--report-only-fail', help="terse output, only notify of failures", action="store_true")

args = parser.parse_args()
