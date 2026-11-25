#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters — make.fun entry.

Writes one Wi-Fi network name (at most 32 characters) to
/output/entry.txt (or $WIFI_OUTPUT_DIR/entry.txt).

The chosen name is a whole miniature story: a dad changes the Wi-Fi
password, and the mum walks out over it. Situation, characters and
consequence in 30 characters, no word wasted.

Standard library only. No input, no network, no randomness:
the same bytes on every run.
"""

import os
import sys

# Ten original candidate Wi-Fi names, drafted for this bounty.
# Each is at most 32 characters. None is copied from any other entry.
CANDIDATES = [
    "Dad Changed Password, Mom Left",      # 30 - CHOSEN
    "Divorced But Still On The WiFi",      # 30
    "This WiFi Saw My Search History",      # 31
    "Ex Still Pays, I Still Stream",        # 29
    "My Ex's WiFi, My New Password",        # 29
    "The WiFi Died With My Marriage",       # 30
    "He Proposed, I Said Connect",          # 27
    "The Neighbor's WiFi Since 2019",       # 30
    "Password: My Ex's Birthday",           # 26
    "Rent Due, WiFi Still Free",            # 25
]

# The winner: the joke lands on the first read (a Wi-Fi password ended
# a marriage), the story is complete (dad acts, mum leaves), and the
# wording is fresh and tight at 30 of the 32 allowed characters.
CHOSEN = CANDIDATES[0]

MAX_CHARS = 32


def main() -> int:
    text = CHOSEN
    if not (1 <= len(text) <= MAX_CHARS):
        print(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return 1
    if any(ord(ch) > 127 for ch in text):
        print("entry must be plain ASCII", file=sys.stderr)
        return 1

    out_dir = os.environ.get("WIFI_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    print(f"{text} ({len(text)} characters) -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
