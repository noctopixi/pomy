# Pomy 🍅⭐

Welcome to Pomy, the minimalist Pomodoro timer!

## About Pomy

Pomy is a simple Pomodoro timer written in Python. It helps you stay focused, stay productive, and take well-deserved breaks.

## Features

- **Gentle sound effects:** Enjoy soothing wind chimes to signal work and break intervals.
- **Minimal dependencies:** To keep Pomy lightweight, it only uses Python's built-in libraries.
- **Useful notifications with time stamps:** Pomy features colored, easy to read output when a new Pomodoro, break, or set starts. Desktop notifications are enabled by default.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/noctopixi/pomy.git
   ```
2. Navigate to the Pomy directory:
   ```bash
   cd pomy
   ```
3. Run Pomy:
   ```bash
   python3 pomy.py
   ```

## Usage

1. Start Pomy to begin your Pomodoro session.
2. Focus during work intervals and avoid distractions.
3. During breaks, get off your chair, hydrate and move around.
4. You will get a long 15-minute break every 4 work cycles.

## Options

- `--quiet` or `-q` disables sound output.
- `--disable-notifications` or `-d` disables desktop notifications.
- `--no-color` disables color output and only displays Pomy's messages in your terminal's default color.
- `--no-format` disables bold and underline formatting. Using this option might reduce readability.
- `--test` makes each cycle last 1 second only. Mostly useful for development purposes.
