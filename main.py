#!/usr/bin/env python3
"""Write the Funniest Cat Voicemail Greeting entry to entry.txt.

Writes exactly 105 bytes (UTF-8, no trailing newline) to
<MAKEFUN_OUTPUT_DIR>/entry.txt (defaults to /output).
Standard library only; no network access.
"""

import os
import sys

ENTRY = "Can't come to the phone. Coughing up a hairball the size of a second cat. Call back when the rug's clean."


def verify(path):
    """Read entry.txt back from disk and check it against ENTRY.

    Exits non-zero with a clear error if any check fails.
    """
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError as exc:
        print(f"error: cannot read back {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"error: {path} is not valid UTF-8: {exc}", file=sys.stderr)
        sys.exit(1)
    if text != ENTRY:
        print(f"error: {path} content does not match ENTRY", file=sys.stderr)
        sys.exit(1)
    if not 1 <= len(text) <= 120:
        print(f"error: {path} length {len(text)} outside 1-120 chars", file=sys.stderr)
        sys.exit(1)
    if "\n" in text or "\r" in text:
        print(f"error: {path} contains a newline", file=sys.stderr)
        sys.exit(1)
    expected_bytes = len(ENTRY.encode("utf-8"))
    if len(raw) != expected_bytes:
        print(
            f"error: {path} is {len(raw)} bytes, expected {expected_bytes}",
            file=sys.stderr,
        )
        sys.exit(1)
    for ch in text:
        if ord(ch) < 0x20 and ch not in ("\t",):
            print(
                f"error: {path} contains control character U+{ord(ch):04X}",
                file=sys.stderr,
            )
            sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    verify(path)


if __name__ == "__main__":
    main()
