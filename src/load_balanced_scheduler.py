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
from anki.consts import *


def log_info(message):
    if LOG_LEVEL >= 1:
        sys.stdout.write(message)


def log_debug(message):
    if LOG_LEVEL >= 2:
        sys.stdout.write(message)


def _fixedNextRevIvl(self, card, ease, fuzz):
    "Next review interval for CARD, given EASE."
    delay = self._daysLate(card)
    conf = self._revConf(card)
    fct = card.factor / 1000
    hardFactor = conf.get("hardFactor", 1.2)
    if hardFactor > 1:
        hardMin = card.ivl
    else:
        hardMin = 0

    ivl2 = self._constrainedIvl(card.ivl * hardFactor, conf, hardMin, fuzz)
    if ease == BUTTON_TWO:
        if fuzz:
            ivl2 = self._fuzzedIvl(ivl2)

        log_debug(f"\nHard button pressed. Setting card interval to: {ivl2} days\n")
        return ivl2

    ivl3 = self._constrainedIvl((card.ivl + delay // 2) * fct, conf, ivl2, fuzz)
    if ease == BUTTON_THREE:
        if fuzz:
            ivl3 = self._fuzzedIvl(ivl3)

        log_debug(f"\nGood button pressed. Setting card interval to: {ivl3} days\n")
        return ivl3

    ivl4 = self._constrainedIvl(
        (card.ivl + delay) * fct * conf["ease4"], conf, ivl3, fuzz
    )
    if fuzz:
        ivl4 = self._fuzzedIvl(ivl4)

    log_debug(f"\nEasy button pressed. Setting card interval to: {ivl4} days\n")
    return ivl4


# Note, we cannot remove the fuzz parameter despite it not being needed because
# _earlyReviewIvl calls it with
# ivl = self._constrainedIvl(ivl, conf, prev=0, fuzz=False)
def _fixedConstrainedIvl(self, ivl, conf, prev, fuzz):
    ivl = int(ivl * conf.get("ivlFct", 1))
    ivl = max(ivl, prev + 1, 1)
    ivl = min(ivl, conf["maxIvl"])
    return int(ivl)


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


# Patch Anki v1 scheduler
# Note: We do not need to patch _nextRevIvl or _constrainedIvl because there is
# no bug in the v1 scheduler
anki.sched.Scheduler._fuzzedIvl = load_balanced_ivl


# Patch Anki v2 scheduler
if version.startswith("2.1"):
    from anki.schedv2 import Scheduler

    # We need to patch _nextRevIvl and _constrainedIvl because there is a bug
    # with the v2 scheduler
    # See: https://github.com/ankitects/anki/issues/1416
    #
    # TODO: Once the above anki issue has been resolved, we shouldn't need to
    # patch these functions anymore.
    #
    # However, to ensure backwards compatibility for this addon, we will need to
    # check the anki PATCH version (MAJOR.MINOR.PATCH, ie: the 48 in v2.1.48)
    # and still apply these patches to all anki clients below that version
    anki.schedv2.Scheduler._nextRevIvl = _fixedNextRevIvl
    anki.schedv2.Scheduler._constrainedIvl = _fixedConstrainedIvl

    anki.schedv2.Scheduler._fuzzedIvl = load_balanced_ivl
