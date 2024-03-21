#!/usr/bin/python3

from time import sleep
from datetime import datetime
from sys import argv

minute_seconds = 60 if "--test" not in argv else 1
cycle_number = 1
completed_series = 0

pomodoro_duration = 25 * minute_seconds
short_break_duration = 5 * minute_seconds
long_break_duration = 15 * minute_seconds


def set_cycle_type(cycle_number: int):
    # Long break every 8th cycle
    if cycle_number % 8 == 0:
        return (long_break_duration, "Long break - You deserve it! (15m)")
    # Short breaks are always even
    elif cycle_number % 2 == 0:
        return (short_break_duration, "Short break - Drink water and stretch! (5m)")
    # Pomodoro cycles are always odd
    elif cycle_number % 2 != 0:
        return (pomodoro_duration, "Work time - Let's do this! (25m)")
    else:
        return (pomodoro_duration, "Work time - Let's do this! (25m)")


# Functions
def countdown(duration, cycle_msg):
    start_time = str(datetime.now().time())[:5]
    print(f"[Cycle {cycle_number:02d} at {start_time}]  {cycle_msg}")
    while duration:
        mins, secs = divmod(duration, 60)
        timer = "Timer: {:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        sleep(1)
        duration -= 1


while True:
    try:
        next_cycle = set_cycle_type(cycle_number)
        cycle_duration = next_cycle[0]
        cycle_msg = next_cycle[1]
        countdown(cycle_duration, cycle_msg)
        cycle_number += 1
        # Congratulate user after completing a set of 8 cycles
        if cycle_number % 9 == 0:
            completed_series += 1
            series_completion_time = str(datetime.now().time())[:5]
            print(
                f"[Series {completed_series} at {series_completion_time}]  Congratulations, you completed a set!"
            )
    except KeyboardInterrupt:
        print("\n\n[Session ended]  Goodbye!")
        exit()
