#!/usr/bin/env python

"""
Outputs all possible "load balanced" intervals for each input interval
between and including START_INTERVAL and END_INTERVAL.

ivl_range_probst() modified from NEW_adjRevIvl()
Anki load balancer add-on (https://github.com/jakeprobst)
"""

import sys

# Though valid, ivl_range_probst(0) is never called in actual use.
START_INTERVAL = 1
END_INTERVAL = 150

qc = {
      "LBPercentBefore": .1,
      "LBPercentAfter": .1,
      "LBMaxBefore": 6,
      "LBMaxAfter": 4,
      "LBMinBefore": 1,
      "LBMinAfter": 1,
      "LBWorkload": .8,
      "LBDeckScheduling": False
        }


def ivl_range_probst(idealIvl):
    ivlmin = idealIvl - min(qc["LBMaxBefore"], int(idealIvl * qc["LBPercentBefore"]))
    ivlmax = idealIvl + min(qc["LBMaxAfter"], int(idealIvl * qc["LBPercentAfter"]))
    ivlmin = max(min(ivlmin, idealIvl - qc["LBMinBefore"]), 1)
    ivlmax = max(ivlmax, idealIvl + qc["LBMinAfter"])
    return[ivlmin, ivlmax]

for x in range(START_INTERVAL,END_INTERVAL+1):
    out_range = ivl_range_probst(x)
    # sys.stdout.write("# ivl={}\tmin={}\tmax={}\n".format(x, out_range[0], out_range[1]))
    for y in range(out_range[0], out_range[1] + 1):
        sys.stdout.write("{}\t{}\n".format(x, y))