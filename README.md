# Load Balanced Scheduler

*Load Balanced Scheduler* is an Anki add-on which helps maintain a consistent number of reviews from one day to another.  Intervals are chosen from the same range as stock Anki so as not to affect the SRS algorithm.  It is compatible with Anki 2.1 using both the default and v2 scheduler.

## Installation

To manually install this add-on copy the `src` directory and it's contents to your Anki add-on directory.  To find the Anki add-on directory first go go to *Tools -> Add-ons*, un-select any currently highlighted add-ons, and click *Show Files*.  It is generally a good idea to rename the `src` directory.  Anki will use this folder name as the name of the plugin.  After restarting Anki the add-on will appear in the add-on window.

## Configuration

Logging can be configured by setting the value of `LogLevel`.  `"LogLevel": 1` will cause a one line summary to be sent to `stdout` each time a card is load balanced.  `"LogLevel": 2` will add detailed information about the load balancing process.  `"LogLevel": 0` will disable logging.  Logs are written to `stdout`.

## Details

After a card is reviewed, Anki assigns it the interval shown on the ease button selected by the user.  This new interval is further modified as described in the Anki [manual](https://apps.ankiweb.net/docs/manual.html#what-spaced-repetition-algorithm-does-anki-use):  

> After you select an ease button, Anki also applies a small amount of random “fuzz” to prevent cards that were introduced at the same time and given the same ratings from sticking together and always coming up for review on the same day. This fuzz does not appear on the interval buttons, so if you’re noticing a slight discrepancy between what you select and the intervals your cards actually get, this is probably the cause.

![Image](https://raw.githubusercontent.com/xquercus/load-balanced-scheduler/master/tools/plot120.png)
![Image](https://raw.githubusercontent.com/xquercus/load-balanced-scheduler/master/tools/plot15.png)

The above plots show the possible "fuzzed" intervals Anki may assign given a particular interval.  Looking at the second plot as an example, if the users selects an ease button with an interval of 10 days, Anki will randomly assign a "fuzzed" interval between 8 and 12 days.  *Load Balanced Scheduler* uses this same range of between 8 and 12 but, instead of selecting at random, will choose an interval with the least number of cards due.

Cards with small intervals will be load balanced over a narrow range.  For example, cards with an interval of 3 will be load balanced over days 2-4.  This range expands as the interval increases.  Cards with an interval of 15 will be balanced over days 13-17 and cards with an interval of 30 will be balanced over days 26-34.  Again, these are the same ranges stock Anki uses when randomly assigning intervals.  The exact ranges can be seen [here](https://github.com/dae/anki/blob/b5785f7ec8b3f95f88ba63cc43f9ee7ce829241a/anki/schedv2.py#L921-L934) in the Anki source.

## Known Issues

### Failed cards aren't getting load balanced.

This is expected behavior.  *Load Balanced Scheduler* balances cards that stock Anki would "fuzz".  Anki doesn't "fuzz" failed cards when they move back into the review queue so they are not load balanced. Additionally, while this would be easy to add, it would patch core parts of the v2 scheduler which is still in development.  It's not worth putting scheduling at risk if there is a silent failure.  The "fuzz" function itself has been very stable over time.

### Under the v2 scheduler logs show multiple intervals being calculated for the same card.

This is expected behavior. Under the v2 scheduler, logs may show the card being scheduled multiple times.  Anki calculates intervals before checking which ease button the user actually pressed.  It's not clear why this is done but see [this function](https://github.com/dae/anki/blob/b5785f7ec8b3f95f88ba63cc43f9ee7ce829241a/anki/schedv2.py#L895-L915) in `schedv2.py` if you want to explore more.  The end result is that for a NORMAL card the log will show calculated intervals for HARD and NORMAL.  For an EASY cards the log will show calculated intervals for HARD, NORMAL and EASY. In the end, the last interval shown in the log is the one Anki assigns to the card.   

## Credits
    
Thank you to Jake Probst for the *Load Balancer* add-on. I used and abused that thing for a long time. 

