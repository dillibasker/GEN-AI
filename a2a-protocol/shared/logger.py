"""Shared pretty logger for A2A demo."""
import time
from datetime import datetime


COLORS = {
    "reset":  "\033[0m",
    "bold":   "\033[1m",
    "cyan":   "\033[96m",
    "green":  "\033[92m",
    "yellow": "\033[93m",
    "red":    "\033[91m",
    "magenta":"\033[95m",
    "blue":   "\033[94m",
    "white":  "\033[97m",
    "gray":   "\033[90m",
}

def _ts():
    return datetime.now().strftime("%H:%M:%S")

def _fmt(color: str, prefix: str, msg: str) -> str:
    c = COLORS.get(color, "")
    r = COLORS["reset"]
    b = COLORS["bold"]
    return f"{COLORS['gray']}[{_ts()}]{r} {c}{b}{prefix}{r} {msg}"

def info(prefix: str, msg: str):
    print(_fmt("cyan", prefix, msg))

def success(prefix: str, msg: str):
    print(_fmt("green", prefix, msg))

def warn(prefix: str, msg: str):
    print(_fmt("yellow", prefix, msg))

def error(prefix: str, msg: str):
    print(_fmt("red", prefix, msg))

def step(prefix: str, msg: str):
    print(_fmt("magenta", prefix, msg))

def protocol(msg: str):
    print(_fmt("blue", "📡 [A2A]", msg))

def divider(title: str = ""):
    line = "─" * 60
    if title:
        pad = (58 - len(title)) // 2
        print(f"\n{COLORS['gray']}┌{line}┐")
        print(f"│{' '*pad}{COLORS['bold']}{COLORS['white']}{title}{COLORS['reset']}{COLORS['gray']}{' '*(58-pad-len(title))}│")
        print(f"└{line}┘{COLORS['reset']}\n")
    else:
        print(f"{COLORS['gray']}{line}{COLORS['reset']}")
