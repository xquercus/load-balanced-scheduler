# Copyright (C) 2018 Jeff Stevens
# This software is licensed under the GNU GPL v3 https://www.gnu.org/licenses/gpl-3.0.html

# LOG_LEVEL = 0  Disables logging.
# LOG_LEVEL = 1  Logs a one line summary each time a card is load balanced.
# LOG_LEVEL = 2  Logs additional detailed information about each step of the load balancing process.
LOG_LEVEL = 0

import sys
import anki
import datetime
from aqt import mw
from anki import version
from anki.sched import Scheduler


def log_info(message):
    if LOG_LEVEL >= 1:
        sys.stdout.write(message)


def log_debug(message):
    if LOG_LEVEL >= 2:
        sys.stdout.write(message)


def load_balanced_ivl(self, ivl):
    """Return the (largest) interval that has the least number of cards and falls within the 'fuzz'"""
    orig_ivl = int(ivl)
    min_ivl, max_ivl = self._fuzzIvlRange(orig_ivl)
    min_num_cards = 18446744073709551616        # Maximum number of rows in an sqlite table?
    best_ivl = 1
    for check_ivl in range(min_ivl, max_ivl + 1):
        num_cards = self.col.db.scalar("""select count() from cards where due = ? and queue = 2""",
                                       self.today + check_ivl)
        if num_cards <= min_num_cards:
            best_ivl = check_ivl
            log_debug("> ")
            min_num_cards = num_cards
        else:
            log_debug("  ")
        log_debug("check_ivl {0:<4} num_cards {1:<4} best_ivl {2:<4}\n".format(check_ivl, num_cards, best_ivl))
    log_info("{0:<28} orig_ivl {1:<4} min_ivl {2:<4} max_ivl {3:<4} best_ivl {4:<4}\n"
             .format(str(datetime.datetime.now()), orig_ivl, min_ivl, max_ivl, best_ivl))
    return best_ivl


# Patch Anki 2.0 and Anki 2.1 default scheduler
anki.sched.Scheduler._fuzzedIvl = load_balanced_ivl


# Patch Anki 2.1 experimental v2 scheduler
if version.startswith("2.1"):
    from anki.schedv2 import Scheduler
    anki.schedv2.Scheduler._fuzzedIvl = load_balanced_ivl
