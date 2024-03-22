#!/usr/bin/python3

from time import sleep
from datetime import datetime
from sys import argv
import platform
from subprocess import run
from shutil import which

minute_seconds = 60 if "--test" not in argv else 1
cycle_number = 1
completed_series = 0

pomodoro_duration = 25 * minute_seconds
short_break_duration = 5 * minute_seconds
long_break_duration = 15 * minute_seconds

operating_system = platform.system()
sound_binary = None
pomodoro_sfx = "sfx/pomodoro_sfx.wav"
break_sfx = "sfx/break_sfx.wav"

if not any(arg in argv for arg in ["--quiet", "-q"]):
    # Check if a sound binary is present, default to aplay
    if which("aplay"):
        sound_binary = "aplay"
    elif which("play"):
        sound_binary = "play"


def play_sfx(sound_effect):
    if operating_system == "Linux":
        run(["aplay", "-q", sound_effect])


# Text Format
BOLD = "\033[1m"
RESET_FORMAT = "\033[0m"


def set_cycle_type(cycle_number: int):
    # Long break every 8th cycle
    if cycle_number % 8 == 0:
        is_work = False
        return (long_break_duration, "Long break - You deserve it! (15m)", is_work)
    # Short breaks are always even
    elif cycle_number % 2 == 0:
        is_work = False
        return (
            short_break_duration,
            "Short break - Drink water and stretch! (5m)",
            is_work,
        )
    # Pomodoro cycles are always odd
    elif cycle_number % 2 != 0:
        is_work = True
        return (pomodoro_duration, "Work time - Let's do this! (25m)", is_work)
    else:
        is_work = True
        return (pomodoro_duration, "Work time - Let's do this! (25m)", is_work)


# Functions
def countdown(duration):
    while duration:
        mins, secs = divmod(duration, 60)
        timer = "Timer: {:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        sleep(1)
        duration -= 1


def show_progress(count, message=None, is_series=False):
    current_time = str(datetime.now().time())[:5]
    if not is_series:
        print(f"{BOLD}[Cycle {count:02d} at {current_time}]{RESET_FORMAT}  {message}")
    else:
        print(
            f"{BOLD}[Series {count} at {current_time}]{RESET_FORMAT}  Congratulations, you completed a set!"
        )


while True:
    try:
        next_cycle = set_cycle_type(cycle_number)
        cycle_duration = next_cycle[0]
        cycle_msg = next_cycle[1]
        cycle_is_work = next_cycle[2]
        show_progress(cycle_number, message=cycle_msg)
        if sound_binary:
            if cycle_is_work:
                play_sfx(pomodoro_sfx)
            else:
                play_sfx(break_sfx)
        countdown(cycle_duration)
        cycle_number += 1

        # Congratulate user after completing a set of 8 cycles
        if cycle_number % 9 == 0:
            completed_series += 1
            show_progress(completed_series, is_series=True)
    except KeyboardInterrupt:
        print("\n\n[Session ended]  Good job!")
        exit()
