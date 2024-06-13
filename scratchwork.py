from time import sleep
import sys
from alive_progress import alive_bar

def load_bar(current, total, bar_length=20):
    # sys.stdout.flush()
    sys.stdout.write('\r')
    # the exact output you're looking for:
    # bars = how many 5% increments are complete
    bars = int(bar_length * current / total)
    sys.stdout.write("[%-20s] %d%%" % ('=' * bars, 100 / total * current))
    sys.stdout.flush()

    # sys.stdout.flush()
    # sleep(0.25)

for i in range(1, 101):
    load_bar(i, 100)
