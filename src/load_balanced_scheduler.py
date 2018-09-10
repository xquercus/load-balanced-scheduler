import sys
import anki
from anki.sched import Scheduler
from anki.schedv2 import Scheduler


_debug_lvl = 2


def dbg(message, level):
    if _debug_lvl >= level:
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
            dbg("> ", 2)
            min_num_cards = num_cards
        else:
            dbg("  ", 2)
        dbg("check_ivl {0:<4} num_cards {1:<4} best_ivl {2:<4}\n".format(check_ivl, num_cards, best_ivl), 2)
    dbg("* orig_ivl {0:<4} min_ivl {1:<4} max_ivl {2:<4} best_ivl {3:<4} ****\n".format(orig_ivl, min_ivl, max_ivl, best_ivl), 1)
    return best_ivl


anki.sched.Scheduler._fuzzedIvl = load_balanced_ivl


anki.schedv2.Scheduler._fuzzedIvl = load_balanced_ivl
