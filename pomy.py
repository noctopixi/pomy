#!/usr/bin/python3

from time import sleep
from datetime import datetime
from sys import argv
import platform
from subprocess import run
from shutil import which
import threading

minute_seconds = 60 if "--test" not in argv else 1
global_cycle_count = 1
set_count = 1
pomodoro_count = 0

pomodoro_duration = 25 * minute_seconds if "--test" not in argv else 1
short_break_duration = 5 * minute_seconds if "--test" not in argv else 1
long_break_duration = 15 * minute_seconds if "--test" not in argv else 1

operating_system = platform.system()
sound_binary = None
pomodoro_sfx = "sfx/pomodoro_sfx.wav"
break_sfx = "sfx/break_sfx.wav"

MAX_TIMER_CHARACTERS = 32

# Text format and colors
if "--no-color" in argv:
    ORANGE = ""
    SKY_BLUE = ""
    YELLOW = ""
else:
    from text_format import Colors

    ORANGE = Colors.ORANGE
    SKY_BLUE = Colors.SKY_BLUE
    YELLOW = Colors.YELLOW

if "--no-format" in argv:
    BOLD = ""
    UNDERLINE = ""
    RESET_FORMAT = ""
else:
    from text_format import Format

    BOLD = Format.BOLD
    UNDERLINE = Format.UNDERLINE
    RESET_FORMAT = Format.RESET


if not any(arg in argv for arg in ["--quiet", "-q"]):
    # Check if a sound binary is present, default to aplay
    if which("aplay"):
        sound_binary = "aplay"
    elif which("play"):
        sound_binary = "play"
    else:
        print(
            "Error: Unable to play sound effects. No supported sound binary found (aplay or play)."
        )

if not any(arg in argv for arg in ["--disable-notifications", "-d"]):
    display_toast = True
else:
    display_toast = False


def play_sfx(sound_effect):
    if operating_system == "Linux":
        run(["aplay", "-q", sound_effect])


def toast(msg):
    if operating_system != "Linux":
        print(
            "Notifications are not yet implemented for your operating system - sorry!"
        )
    elif operating_system == "Linux":
        if which("notify-send"):
            run(["notify-send", "Pomy", msg])
        else:
            print(
                "Unable to display notification toasts. notify-send is not installed on this device."
            )


def set_cycle_type():
    global global_cycle_count
    # Long break every 8th cycle
    if global_cycle_count % 8 == 0:
        is_work = False
        return (
            long_break_duration,
            "You finished a set! Enjoy your well deserved rest!",
            is_work,
        )
    # Short breaks are always even cycles
    elif global_cycle_count % 2 == 0:
        is_work = False
        return (
            short_break_duration,
            "Drink water, breathe deeply and stretch!",
            is_work,
        )
    # Pomodoro cycles are always odd
    elif global_cycle_count % 2 != 0:
        is_work = True
        return (pomodoro_duration, "Work time - Let's do this!", is_work)
    else:
        is_work = True
        return (pomodoro_duration, "Work time - Let's do this!", is_work)


# Functions
def countdown(duration):
    while duration:
        mins, secs = divmod(duration, 60)
        timer = "Timer: {:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        sleep(1)
        duration -= 1


# Messages are only used for pomo/break cycles.
# When completing a set, the message is built in.
def show_progress(count, progress_message=None, is_set=False, is_work=False):
    current_time = str(datetime.now().time())[:5]

    if is_set:
        toast_msg = f"Set {count} at {current_time}"
        terminal_msg = (
            f"{YELLOW}{BOLD}{UNDERLINE}Set {count} at {current_time}{RESET_FORMAT}"
        )
        # Print enough whitespace to delete the Timer: MM:SS line in the terminal
        print(" " * MAX_TIMER_CHARACTERS)

    elif is_work:
        minutes = "25 minutes"
        toast_msg = f"{current_time} - Pomodoro {count}\nDuration: {minutes}\n{progress_message}"
        terminal_msg = f"{ORANGE}{BOLD}[{current_time} - Pomodoro {count}]{RESET_FORMAT}  {progress_message} ({minutes})"

    # Break messages
    else:
        global global_cycle_count
        # Long breaks occur every 8th cycle
        if global_cycle_count % 8 == 0:
            minutes = "15 minutes"
            toast_msg = (
                f"{current_time} - Long break\nDuration: {minutes}\n{progress_message}"
            )
            terminal_msg = f"{SKY_BLUE}{BOLD}[{current_time} - Long break]{RESET_FORMAT}  {progress_message} ({minutes})"

        # Short breaks are always even cycles (cycle count % 2 = 0)
        else:
            minutes = "5 minutes"
            toast_msg = (
                f"{current_time} - Mini break\nDuration: {minutes}\n{progress_message}"
            )
            terminal_msg = f"{SKY_BLUE}{BOLD}[{current_time} - Mini break]{RESET_FORMAT}  {progress_message} ({minutes})"

    if display_toast:
        toast(toast_msg)
    print(terminal_msg)


while True:
    try:
        if pomodoro_count == 0:
            show_progress(set_count, is_set=True)

        next_cycle = set_cycle_type()
        cycle_duration = next_cycle[0]
        cycle_msg = next_cycle[1]
        cycle_is_work = next_cycle[2]

        if cycle_is_work:
            pomodoro_count += 1

        # Display a timestamped progress message
        show_progress(pomodoro_count, progress_message=cycle_msg, is_work=cycle_is_work)

        # Play sound effect in a separate thread so the program does not hang
        if sound_binary:
            if cycle_is_work:
                sound_effect = pomodoro_sfx
            else:
                sound_effect = break_sfx
            sfx_thread = threading.Thread(target=play_sfx, args=(sound_effect,))
            sfx_thread.start()

        countdown(cycle_duration)
        global_cycle_count += 1

        # Congratulate user after completing a set of 8 cycles
        if global_cycle_count % 9 == 0:
            global_cycle_count = 1
            pomodoro_count = 0
            set_count += 1

    except KeyboardInterrupt:
        print("\n\n[Session ended]  Good job!")
        exit()
