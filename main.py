#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters — make.fun entry.

Writes one Wi-Fi network name (at most 32 characters) to
/output/entry.txt (or $WIFI_OUTPUT_DIR/entry.txt).

The chosen name is a whole miniature story: a dad changes the Wi-Fi
password, and the mum walks out over it. Situation, characters and
consequence in 30 characters, no word wasted.

Run with --check to validate the chosen name without writing a file.

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


def validate(text: str) -> list:
    """Check one candidate Wi-Fi name against the bounty rules.

    Returns a list of problems (empty means the name is valid):
    length 1-32 characters, not only whitespace, no leading or
    trailing whitespace, and printable ASCII only (0x20-0x7E).
    Control characters and DEL are rejected too: the old gate only
    rejected ord(ch) > 127, so a tab or bell would have slipped
    through into a network name nobody can type or read.
    """
    problems = []
    if not (1 <= len(text) <= MAX_CHARS):
        problems.append(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        problems.append("entry must not be only whitespace")
    if text != text.strip():
        problems.append("entry must not start or end with whitespace")
    bad = sorted({ch for ch in text if not (0x20 <= ord(ch) <= 0x7E)})
    if bad:
        problems.append(
            "entry must be printable ASCII, found: "
            + ", ".join(repr(ch) for ch in bad))
    return problems


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv == ["--check"]:
        # Validate the chosen name without writing anything.
        problems = validate(CHOSEN)
        if problems:
            for problem in problems:
                print(f"invalid: {problem}", file=sys.stderr)
            return 1
        print(f"OK: {CHOSEN!r} ({len(CHOSEN)} characters)")
        return 0
    if argv:
        print(f"usage: {sys.argv[0]} [--check]", file=sys.stderr)
        return 2

    problems = validate(CHOSEN)
    if problems:
        for problem in problems:
            print(f"invalid: {problem}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("WIFI_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(CHOSEN)
    print(f"{CHOSEN} ({len(CHOSEN)} characters) -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
