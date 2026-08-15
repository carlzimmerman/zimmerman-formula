#!/usr/bin/env python3
"""t083_donotcite_linter.py -- DO-NOT-CITE linter (R8 retracted/withdrawn phrases).

Grep-based linter over qwen_38_experiment/ for the eight R8 retracted claims
(PROTOCOL.md, R8, lines 58-63). It guards against re-citing any claim the corpus
has formally retracted/withdrawn.

PASS criterion (T083): a clean run on the current folder.

Wired into harness.py to run before EVERY LEDGER.md append (fail-closed: a
retracted citation blocks the row). The escape hatch for a legitimate need is
ESCALATE.md (R10) -- never silently edit PROTOCOL.md/RETRACTIONS.md.

Modes
  python t083_donotcite_linter.py                  # scan the whole folder (CI/regression)
  python t083_donotcite_linter.py --check TEXT     # lint one snippet (pre-append guard)
  python t083_donotcite_linter.py --check -        # read the snippet from stdin
Exit 0 = clean; exit 1 = a retracted phrase was found; exit 2 = grep error.

The patterns are the *retracted claims*, written precisely enough not to flag
legitimate uses -- e.g. "MUSE" in T071's title, or the [A9: 1.2139] supersession
tags in t085_kernel_regression.py (which correctly track the retraction, they do
not re-cite it).
"""
import os
import re
import subprocess
import sys

# The eight R8 retracted claims, each as one or more case-insensitive regexes.
# Faithful to PROTOCOL.md R8, in order.
RETRACTED = [
    ("fine-structure/Omega_Lambda Z-numerology",
     [r"z-numerology",
      r"fine-structure[/-]omega_lambda"]),
    ("'no dark matter in galaxies' as a result",
     [r"no dark matter in galaxies"]),
    ("AeST lambda_J=2.7 Mpc prediction",
     [r"lambda_j\s*=\s*2\.7"]),
    ("'clusters at 21.6 a0 at R500'",
     [r"21\.6\s*a0"]),
    ("Cell 3 transport as VIABLE (demoted CONDITIONAL-DEAD, stage63)",
     [r"cell 3 transport"]),
    ("the a0-rising MUSE confirmation",
     [r"a0-rising muse",
      r"muse confirmation"]),
    ("the Ly-alpha 6-8 sigma exclusion",
     [r"ly-alpha\s+6[-\s]8"]),
    ("gamma_v = 1.2139/1.2592 as settled (superseded by Amendment 10)",
     [r"gamma_v\s*=\s*1\.2139",
      r"gamma_v\s*=\s*1\.2592",
      r"1\.2139\s*/\s*1\.2592",
      r"1\.2592\s*/\s*1\.2139"]),
]

SELF = os.path.basename(__file__)
# Files that legitimately *define* the phrases -- they must never be flagged.
EXCLUDE_NAMES = {"PROTOCOL.md", SELF}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def flatten_patterns():
    out = []
    for _, pats in RETRACTED:
        out.extend(pats)
    return out


def gather_files(root):
    files = []
    for dirpath, _dirnames, filenames in os.walk(root):
        if "__pycache__" in dirpath.split(os.sep):
            continue
        for fn in filenames:
            if fn in EXCLUDE_NAMES:
                continue
            if fn.endswith((".md", ".py", ".txt")):
                files.append(os.path.join(dirpath, fn))
    return files


def grep_lines(text, patterns):
    """Return list of (lineno, matched_line) for `text` via grep -E (grep-based)."""
    args = ["grep", "-niE"]
    for p in patterns:
        args += ["-e", p]
    r = subprocess.run(args, input=text, capture_output=True, text=True)
    if r.returncode == 2:   # grep error (bad regex, etc.)
        raise RuntimeError("grep failed: " + (r.stderr or "").strip())
    hits = []
    for raw in (r.stdout or "").splitlines():
        m = re.match(r"^(\d+):(.*)$", raw)
        if m:
            hits.append((int(m.group(1)), m.group(2).strip()))
    return hits


def lint_folder():
    """Return list of (relpath, lineno, line) for the whole folder."""
    pats = flatten_patterns()
    problems = []
    for f in gather_files(ROOT):
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        for lineno, line in grep_lines(text, pats):
            problems.append((os.path.relpath(f, ROOT), lineno, line))
    return problems


def lint_text(text):
    return grep_lines(text, flatten_patterns())


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        if len(sys.argv) > 2 and sys.argv[2] != "-":
            text = sys.argv[2]
        else:
            text = sys.stdin.read()
        problems = [("<snippet>", n, ln) for (n, ln) in lint_text(text)]
        label = "snippet"
    else:
        problems = lint_folder()
        label = "folder"

    if not problems:
        if label == "folder":
            print(f"DO-NOT-CITE linter: CLEAN -- 0 R8 retracted phrases in {ROOT}")
        else:
            print("DO-NOT-CITE linter: CLEAN -- snippet carries no R8 retracted phrase")
        return 0

    print(f"DO-NOT-CITE linter: {len(problems)} R8 RETRACTED-PHRASE HIT(S) -- fix or ESCALATE (R10):")
    for (f, n, ln) in problems:
        print(f"    {f}:{n}: {ln}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
