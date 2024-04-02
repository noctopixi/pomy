# pomy 🍅⭐

Welcome to pomy, the minimalist Pomodoro timer!

## About pomy

pomy is a simple Pomodoro timer written in Python. It helps you stay focused, stay productive, and take well-deserved breaks.

## Features

- **Gentle sound effects:** Enjoy soothing wind chimes to signal work and break intervals.
- **Minimal dependencies:** To keep pomy lightweight, it only uses Python's built-in libraries.
- **Useful time stamps:** pomy displays a timestamp whenever a new Pomodoro, break, or series starts.
- **Easy to read messages:** pomy features colored, well structured terminal output to make it easier to read.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/noctopixi/pomy.git
   ```
2. Navigate to the pomy directory:
   ```bash
   cd pomy
   ```
3. Run pomy:
   ```bash
   python3 pomy.py
   ```

## Usage

1. Start pomy to begin your Pomodoro session.
2. Focus during work intervals and avoid distractions.
3. During breaks, get off your chair, hydrate and move around.
4. You will get a long 15-minute break every 4 work cycles.

## Options

- `--quiet` or `-q` disables sound output.
- `--no-color` disables color output and only displays pomy's messages in your terminal's default color.
- `--no-format` disables bold and underline formatting. Using this option might reduce readability.
- `--test` makes each cycle last 1 second only. Mostly useful for development purposes.
