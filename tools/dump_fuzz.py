#!/usr/bin/env python

"""
Outputs all possible "fuzzed" intervals for each input interval between and including START_INTERVAL and END_INTERVAL.

fuzzIvlRange() taken from Anki 2.0/2.1 source
"""

import sys

# Though valid, fuzzIvlRange(0) is never called in actual use.
START_INTERVAL = 1
END_INTERVAL = 150


def fuzzIvlRange(ivl):
    if ivl < 2:
        return [1, 1]
    elif ivl == 2:
        return [2, 3]
    elif ivl < 7:
        fuzz = int(ivl * 0.25)
    elif ivl < 30:
        fuzz = max(2, int(ivl * 0.15))
    else:
        fuzz = max(4, int(ivl * 0.05))
    # fuzz at least a day
    fuzz = max(fuzz, 1)
    return [ivl - fuzz, ivl + fuzz]


for x in range(START_INTERVAL,END_INTERVAL+1):
    out_range = fuzzIvlRange(x)
    # sys.stdout.write("# ivl={}\tmin={}\tmax={}\n".format(x, out_range[0], out_range[1]))
    for y in range(out_range[0], out_range[1] + 1):
        sys.stdout.write("{}\t{}\n".format(x, y))
