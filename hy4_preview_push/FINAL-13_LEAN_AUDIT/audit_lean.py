#!/usr/bin/env python3
"""FINAL-13 LEAN-AUDIT harness.

For each NEW .lean file produced by lanes FINAL-9..12:
  1. recompile with the working recipe (`lake env lean <file>` from the lake project root)
  2. record exit code
  3. record the full `#print axioms` output line for every headline theorem
     (headline theorem = one the file itself asks Lean to print axioms for)
  4. proof-term `sorry` scan, backtick-aware, with per-match classification
  5. confirm no `sorryAx` appears in any axioms line

Emits JSON to stdout (and to <out>) plus a human-readable text block.
"""

import json
import os
import re
import subprocess
import sys

LAKE_ROOT = "/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026"
STD_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
SORRY_RE = re.compile(r"(^|[^`])sorry([^`]|$)")
AX_LINE_RE = re.compile(r"^'(?P<name>[^']+)' depends on axioms: \[(?P<ax>[^\]]*)\]")
PRINT_RE = re.compile(r"^\s*#print\s+axioms\s+(?P<name>\S+)\s*$")


def run_lean(rel_path, timeout=1800):
    """Compile rel_path with the working recipe. Returns (exit_code, combined_output)."""
    cmd = ["lake", "env", "lean", rel_path]
    try:
        p = subprocess.run(
            cmd, cwd=LAKE_ROOT, capture_output=True, text=True, timeout=timeout
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ss" % timeout


def headline_theorems(path):
    """The names the file asks Lean to `#print axioms` for, in order."""
    names = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = PRINT_RE.match(line)
            if m:
                names.append(m.group("name"))
    return names


def axiom_lines(out):
    """{theorem_name: raw 'depends on axioms' line} from the compiler output."""
    got = {}
    for line in out.splitlines():
        m = AX_LINE_RE.match(line.strip())
        if m:
            got[m.group("name")] = line.strip()
    return got


def _strip_state(path):
    """Return the file text with comments/docstrings blanked, char-preserving.

    Blanking (not deleting) keeps every offset valid so the sorry scan can look at
    the original line for context.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    out = list(src)
    i, n = 0, len(src)

    def blank(a, b):
        for k in range(a, min(b, n)):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        c = src[i]
        if c == '"':  # string literal
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == '"':
                    break
                j += 1
            blank(i, j + 1)
            i = j + 1
        elif src.startswith("/--", i):  # doc comment (may nest on /-)
            depth, j = 1, i + 3
            while j < n and depth > 0:
                if src.startswith("/-", j):
                    depth += 1
                    j += 2
                elif src.startswith("-/", j):
                    depth -= 1
                    j += 2
                else:
                    j += 1
            blank(i, j)
            i = j
        elif src.startswith("/-", i) and not src.startswith("/--", i):  # block comment
            depth, j = 1, i + 2
            while j < n and depth > 0:
                if src.startswith("/-", j):
                    depth += 1
                    j += 2
                elif src.startswith("-/", j):
                    depth -= 1
                    j += 2
                else:
                    j += 1
            blank(i, j)
            i = j
        elif src.startswith("--", i):  # line comment (but not an arrow '-->' token)
            if src.startswith("-->", i):
                out[i] = " "
                i += 1
                continue
            j = src.find("\n", i)
            j = n if j < 0 else j
            blank(i, j)
            i = j
        else:
            i += 1
    return "".join(out)


def sorry_scan(path):
    """Backtick-aware sorry census.

    Returns:
      count_regex : int  -- literal `grep -cE '(^|[^`])sorry([^`]|$)'` count
      in_code     : list -- (lineno, line) where sorry survives comment stripping
      in_comment  : list -- (lineno, line) where sorry is only inside a comment/docstring
    """
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw_lines = fh.read().splitlines()
    stripped = _strip_state(path).splitlines()

    count_regex = 0
    in_code, in_comment = [], []
    for idx, raw in enumerate(raw_lines):
        if SORRY_RE.search(raw):
            count_regex += 1
        s = stripped[idx] if idx < len(stripped) else ""
        if "sorry" in s.lower() or "sorry" in raw.lower():
            # classification: does a *bare* sorry survive outside comments?
            if "sorry" in s.lower():
                in_code.append((idx + 1, raw.strip()))
            else:
                in_comment.append((idx + 1, raw.strip()))
    return count_regex, in_code, in_comment


def audit(rel_path):
    full = os.path.join(LAKE_ROOT, rel_path)
    rec = {"file": rel_path, "exists": os.path.isfile(full)}
    if not rec["exists"]:
        rec["verdict"] = "MISSING"
        return rec

    with open(full, "r", encoding="utf-8", errors="replace") as fh:
        rec["bytes"] = len(fh.read())

    want = headline_theorems(full)
    rec["headline_theorems"] = want

    rc, out = run_lean(rel_path)
    rec["exit_code"] = rc

    got = axiom_lines(out)
    rec["axioms_printed"] = got
    # A `#print axioms X` written inside `namespace N` is printed back as `N.X`,
    # so match on the qualified suffix rather than exact string equality.
    rec["axiom_lines_missing"] = [
        t for t in want
        if not any(n == t or n.endswith("." + t) for n in got)
    ]

    # non-standard axiom check + sorryAx check
    nonstd, sorryax = [], []
    for name, line in got.items():
        m = AX_LINE_RE.match(line)
        assert m is not None
        raw_ax = m.group("ax") or ""
        axs = [a.strip() for a in raw_ax.split(",") if a.strip()]
        for a in axs:
            if a not in STD_AXIOMS:
                nonstd.append((name, a))
            if "sorry" in a.lower():
                sorryax.append((name, a))
    rec["nonstandard_axioms"] = nonstd
    rec["sorryax_in_axioms"] = sorryax

    cnt, in_code, in_comment = sorry_scan(full)
    rec["proof_term_sorry_count"] = cnt
    rec["sorry_in_code"] = in_code
    rec["sorry_in_comment"] = in_comment
    rec["error_lines"] = [l for l in out.splitlines() if "error:" in l][:20]
    rec["warning_lines"] = [l for l in out.splitlines() if "warning:" in l][:20]

    ok = (
        rc == 0
        and not rec["axiom_lines_missing"]
        and not nonstd
        and not sorryax
        and not in_code
        and not rec["error_lines"]
    )
    rec["verdict"] = "PASS" if ok else "FAIL"
    rec["raw_output"] = out
    return rec


def main():
    targets = [a for a in sys.argv[1:] if not a.startswith("--")]
    outpath = None
    for a in sys.argv[1:]:
        if a.startswith("--out="):
            outpath = a.split("=", 1)[1]
    results = [audit(t) for t in targets]
    if outpath:
        with open(outpath, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=2)
    # human-readable
    for r in results:
        print("=" * 78)
        print("FILE     : %s" % r.get("file"))
        print("verdict  : %s   exit=%s  bytes=%s" % (r.get("verdict"), r.get("exit_code"), r.get("bytes")))
        print("theorems : %d headline (%d printed, %d missing)"
              % (len(r.get("headline_theorems", [])), len(r.get("axioms_printed", {})),
                 len(r.get("axiom_lines_missing", []))))
        for t in r.get("headline_theorems", []):
            print("   %-46s %s" % (t, r.get("axioms_printed", {}).get(t, "<NO AXIOM LINE>")))
        print("proof-term sorry count : %s" % r.get("proof_term_sorry_count"))
        if r.get("sorry_in_code"):
            print("  !! IN CODE:")
            for ln, l in r["sorry_in_code"]:
                print("     %d: %s" % (ln, l))
        if r.get("sorry_in_comment"):
            print("  (comment/docstring only):")
            for ln, l in r["sorry_in_comment"]:
                print("     %d: %s" % (ln, l))
        print("sorryAx in axioms lines: %s" % (r.get("sorryax_in_axioms") or "none"))
        print("non-standard axioms    : %s" % (r.get("nonstandard_axioms") or "none"))
        if r.get("error_lines"):
            print("ERRORS:")
            for l in r["error_lines"]:
                print("   " + l)


if __name__ == "__main__":
    main()
