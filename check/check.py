"""`python3 check/check.py`: which problems the review points at, for the interviewer. Do not edit anything in check/.
Standard library only. It only reads line numbers: the interviewer judges whether each comment is right and useful."""

import hashlib
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API, WEB = "DiscountsController.cs", "ApplyDiscount.jsx"
PROBLEMS = [  # (label, {file: lines})
    ("P1 SQL built by joining the code text", {API: {29, 30}}),
    ("P2 Total taken from the browser", {API: {7, 37}, WEB: {20}}),
    ("P3 Percent / 100 is whole-number division", {API: {38}}),
    ("P4 useEffect with no dependency list", {WEB: {10, 11, 12, 13, 14}}),
    ("P5 Errors not checked after the request", {WEB: {22, 23, 24}}),
    ("P6 Code shown as HTML (script injection)", {WEB: {34}, API: {34, 42}}),
]
PR_FILES = {"pr/api/" + API: "", "pr/web/" + WEB: ""}
REF = re.compile(r"(DiscountsController\.cs|ApplyDiscount\.jsx)\s*:\s*(\d+)(?:\s*[-–]\s*(\d+))?")


def digest(paths):
    h = hashlib.sha256()
    for p in paths:
        with open(os.path.join(ROOT, p), "rb") as f:
            h.update(p.encode() + b"\0" + f.read())
    return h.hexdigest()[:8]


try:
    with open(os.path.join(ROOT, "REVIEW.md"), encoding="utf-8") as f:
        text = f.read()
except OSError:
    text = ""
comments = [l for l in text.splitlines() if REF.search(l)]
pointed = {API: set(), WEB: set()}
for line in comments:
    for name, a, b in REF.findall(line):
        a = int(a)
        b = int(b) if b else a
        if b - a <= 5:  # a wide range does not count as pointing at a line
            pointed[name].update(range(a, b + 1))

found = 0
for label, where in PROBLEMS:
    hit = any(pointed[f] & lines for f, lines in where.items())
    found += hit
    print(f"{label}: {'found' if hit else '-'}")
print(f"Problems found: {found}/6")
print(f"Comments with a file and line: {len(comments)}" + ("  (many: check they are real comments)" if len(comments) > 10 else ""))
print(f"PR files {digest(sorted(PR_FILES))}  Check files {digest(['check/check.py'])}")
