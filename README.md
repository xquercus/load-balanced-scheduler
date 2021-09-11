# Load Balanced Scheduler

*Load Balanced Scheduler* is an Anki add-on which helps maintain a consistent number of reviews from one day to another.  Intervals are chosen from the same range as stock Anki so as not to affect the SRS algorithm. It is compatible with:
* Anki v2.0
* Anki v2.1 with the original scheduler
* Anki v2.1 with the [v2 scheduler](https://faqs.ankiweb.net/the-anki-2.1-scheduler.html)

## Installation

To install follow the instructions on the AnkiWeb [add-ons page](https://ankiweb.net/shared/info/208879074).

## Configuration

No configuration is required however logging can be enabled.  This is done by setting `LOG_LEVEL` at the top of `load_balanced_scheduler.py`.  The following options are available:

* `LOG_LEVEL = 0`: Disables logging.
* `LOG_LEVEL = 1`: Logs a one line summary each time a card is load balanced.
* `LOG_LEVEL = 2`: Logs additional detailed information about each step of the load balancing process.

Logs are sent to `stdout`.  On Windows, the logs can be viewed by running `anki-console.exe`, located in Anki's main directory (usually `C:\Program Files\Anki`).  This works as of Anki 2.1.6.  For Anki 2.0, you can manually download and install [Le Petit Debugger](https://github.com/lovac42/Le_Petit_Debugger) to view the log output.

## Details

After a card is reviewed, Anki assigns it the interval shown on the ease button selected by the user.  This new interval is further modified as described in the Anki [manual](https://docs.ankiweb.net/studying.html#due-counts-and-fuzz-factor):

> Anki additionally adds a small amount of random variation ("fuzz") to the next due times, in order to prevent cards that were introduced together and always rated the same from always staying next to each other.

![Image](https://raw.githubusercontent.com/xquercus/load-balanced-scheduler/master/tools/plot120.png)
![Image](https://raw.githubusercontent.com/xquercus/load-balanced-scheduler/master/tools/plot15.png)

The above plots show the possible "fuzzed" intervals Anki may assign given a particular interval.  Looking at the second plot as an example, if the users selects an ease button with an interval of 10 days, Anki will randomly assign a "fuzzed" interval between 8 and 12 days.  *Load Balanced Scheduler* uses this same range of between 8 and 12 but, instead of selecting at random, will choose an interval with the least number of cards due.

Cards with small intervals will be load balanced over a narrow range.  For example, cards with an interval of 3 will be load balanced over days 2-4.  This range expands as the interval increases.  Cards with an interval of 15 will be balanced over days 13-17 and cards with an interval of 30 will be balanced over days 26-34.  Again, these are the same ranges stock Anki uses when randomly assigning intervals.  The exact ranges can be seen [here](https://github.com/ankitects/anki/blob/9f0929db32aaa9b589af20d7c8abb1a433e76cff/pylib/anki/scheduler/v2.py#L931-L944) in the Anki source.

## Bugs and Support

If you encounter a bug or need support   please see the official [README](https://github.com/xquercus/load-balanced-scheduler). Please report bugs through [github](https://github.com/xquercus/load-balanced-scheduler/issues).  Please don't use the review section of the AnkiWeb add-on page for support as I won't receive a notification and there is no way for me to respond.

## Known Issues

### Failed cards aren't getting load balanced.

This is expected behavior.  *Load Balanced Scheduler* balances cards that stock Anki would "fuzz".  Anki doesn't "fuzz" failed cards when they move back into the review queue so they are not load balanced. Additionally, while this would be easy to add, it would patch core parts of the v2 scheduler which is still in development.  It's not worth putting scheduling at risk if there is a silent failure.  The "fuzz" function itself has been very stable over time.

### Under the v2 scheduler, logs show multiple intervals being calculated for the same card.

This is expected behavior. Anki calculates intervals before checking which ease button the user actually pressed.  See [this function](https://github.com/ankitects/anki/blob/9f0929db32aaa9b589af20d7c8abb1a433e76cff/pylib/anki/scheduler/v2.py#L904-L925) in `scheduler/v2.py` if you want to explore more.  The end result is that for a NORMAL card the log will show calculated intervals for HARD and NORMAL.  For an EASY cards the log will show calculated intervals for HARD, NORMAL and EASY. In the end, the last interval shown in the log is the one Anki assigns to the card.

## Credits
    
Thank you to Jake Probst for the *Load Balancer* add-on. I used and abused that thing for a long time. 

## Revision History

* Version 1.1.1 -- 10/04/2018
  * Backport to Anki 2.0
  * Move configuration to `load_balanced_scheduler.py`.


* Version 1.0.0 -- 09/21/2018
  * Initial Release