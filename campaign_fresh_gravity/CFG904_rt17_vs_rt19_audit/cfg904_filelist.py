#!/usr/bin/env python3
r"""CFG904 file list: tracked files that still present 0.4607 (the Z = 2 pi value) as coefficient-free / derived.

Criteria: FROZEN_CRITERIA.md §7. Tracked files only, read at a pinned commit (git grep <commit>, git show <commit>:path);
no working-tree or untracked search. Text types only; _external_data excluded; files > 2 MB skipped.

  python3 cfg904_filelist.py extract   -> cfg904_filelist_candidates.csv (every kappa-context hit, CLAIM/CAVEAT flags,
                                          the seeded 40-line miss-rate sample)
  python3 cfg904_filelist.py merge     -> reads cfg904_manual_review.csv (hand classes A/B/C), writes
                                          cfg904_filelist_A.csv and prints the summary (stdout -> cfg904_filelist.out)
Read-only for every listed file.
"""
from __future__ import annotations

import csv
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True,
                      check=True).stdout.strip()
PIN = "15f9ba56f"            # the FROZEN_CRITERIA commit: the record as it stood at registration
MAXSIZE = 2_000_000
GLOBS = ["*.md", "*.py", "*.tex", "*.txt", "*.json", "*.out", "*.lean"]
EXCLUDE = [":(exclude)_external_data/*", ":(exclude)campaign_fresh_gravity/CFG904_rt17_vs_rt19_audit/*"]

PATTERNS = {
    "0.4607": r"0\.4607",
    "0.46066": r"0\.46066",
    "0.461": r"0\.461([^0-9]|$)",
    "sqrt(2/(3": r"sqrt[({]2/\(3",
    "frac{2}{3pi}": r"\\frac\{2\}\{3\\pi\}",
    "cH_L/2pi": r"H_(Lambda|Λ|\\Lambda|\{\\Lambda\}|L) ?/ ?\(?2 ?\*? ?\\?(pi|π)",
    "c^2/(2pi L_dS)": r"c\^?2 ?/ ?\(2 ?\\?(pi|π) ?L",
    "dS tie": r"dS tie",
}
CTX_I = re.compile(r"kappa|κ|2 ?pi|2π|2\\pi|horizon|de ?sitter|thermal|KMS|unruh|gibbons|milgrom|coefficient|"
                   r"Z ?= ?2|H_?Lambda|H_Λ|H_\\Lambda", re.I)
CTX_S = re.compile(r"\bdS\b")
CLAIM = re.compile(r"coefficient[- ]free|deriv|forced|predict|first[- ]principles?|no data|parameter[- ]free|"
                   r"closed[- ]form|principle[- ]shaped|un-?excluded|the only|dS tie gives|de Sitter gives|"
                   r"thermality gives|natural", re.I)
CAVEAT = re.compile(r"withdr[ae]w|menu|RT-19|4 ?π error|4 ?pi error|conflict|not derived|never cite|do not cite|"
                    r"not a derivation|posit|conditional", re.I)
COPY = re.compile(r"source_snapshots/|raw_output\.json$|_MUTATE\.out$")


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=False).stdout


def extract():
    hits = {}
    for tag, pat in PATTERNS.items():
        out = git("grep", "-n", "-I", "-E", pat, PIN, "--", *GLOBS, *EXCLUDE)
        for line in out.splitlines():
            m = re.match(rf"^{PIN}:(.+?):(\d+):(.*)$", line)
            if not m:
                continue
            key = (m.group(1), int(m.group(2)))
            hits.setdefault(key, dict(text=m.group(3), pats=set()))["pats"].add(tag)
    cache = {}
    rows = []
    for (path, ln), h in sorted(hits.items()):
        if path not in cache:
            size = git("cat-file", "-s", f"{PIN}:{path}").strip()
            cache[path] = None if (not size.isdigit() or int(size) > MAXSIZE) else \
                git("show", f"{PIN}:{path}").splitlines()
        lines = cache[path]
        if lines is None:
            continue
        win = "\n".join(lines[max(0, ln - 3):ln + 2])
        txt = h["text"]
        direct = bool(h["pats"] - {"0.4607", "0.46066", "0.461"})   # closed forms / cH/2pi / dS tie are kappa-context
        ctx = direct or bool(CTX_I.search(txt) or CTX_S.search(txt))
        rows.append(dict(id=f"{path}:{ln}", path=path, line=ln, patterns="|".join(sorted(h["pats"])),
                         ctx=int(ctx), claim=int(bool(CLAIM.search(win))), caveat=int(bool(CAVEAT.search(win))),
                         copy=int(bool(COPY.search(path))), sample=0, text=txt.strip()[:300]))
    pool = [r for r in rows if r["ctx"] and not r["claim"]]
    rng = random.Random(904)
    for r in rng.sample(pool, min(40, len(pool))):
        r["sample"] = 1
    with open(os.path.join(HERE, "cfg904_filelist_candidates.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    n_ctx = sum(r["ctx"] for r in rows)
    n_claim = sum(1 for r in rows if r["ctx"] and r["claim"])
    print(f"pinned commit {PIN}; raw hits {len(rows)} lines in {len({r['path'] for r in rows})} files; "
          f"kappa-context {n_ctx}; CLAIM-flagged {n_claim} (with CAVEAT {sum(1 for r in rows if r['ctx'] and r['claim'] and r['caveat'])}); "
          f"miss-rate sample {sum(r['sample'] for r in rows)}")


def merge():
    cand = {r["id"]: r for r in csv.DictReader(open(os.path.join(HERE, "cfg904_filelist_candidates.csv")))}
    rev = {r["id"]: r for r in csv.DictReader(open(os.path.join(HERE, "cfg904_manual_review.csv")))}
    need = [i for i, r in cand.items() if r["ctx"] == "1" and (r["claim"] == "1" or r["sample"] == "1")]
    missing = [i for i in need if i not in rev]
    if missing:
        print(f"UNREVIEWED: {len(missing)} required rows lack a hand class, e.g. {missing[:5]}")
        sys.exit(2)
    stray = [i for i in rev if i not in cand]
    if stray:
        print(f"REVIEW ROWS NOT IN CANDIDATES: {stray[:5]}")
        sys.exit(2)
    A = []
    for i in need:
        if rev[i]["class"] == "A":
            r = dict(cand[i], cls="A", note=rev[i]["note"])
            r["copy"] = "1" if (cand[i]["copy"] == "1" or rev[i].get("copy") == "1") else "0"   # hand flag for
            A.append(r)                                                                       # generated quotes
    cls_claim = {}
    for i in need:
        if cand[i]["claim"] == "1":
            cls_claim[rev[i]["class"]] = cls_claim.get(rev[i]["class"], 0) + 1
    samp = [i for i in need if cand[i]["sample"] == "1"]
    samp_A = [i for i in samp if rev[i]["class"] == "A"]
    with open(os.path.join(HERE, "cfg904_filelist_A.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "path", "line", "copy", "note", "text"])
        w.writeheader()
        for r in A:
            w.writerow({k: r[k] for k in ["id", "path", "line", "copy", "note", "text"]})
    print(f"CFG904 file list (pinned commit {PIN}; tracked text files only; FROZEN_CRITERIA §7)")
    print(f"  candidates: {len(cand)} lines; kappa-context {sum(r['ctx'] == '1' for r in cand.values())}; "
          f"hand-reviewed {len(need)} (CLAIM-flagged {sum(cand[i]['claim'] == '1' for i in need)} + sample "
          f"{len(samp)})")
    print(f"  CLAIM-flagged classes: " + ", ".join(f"{k} {v}" for k, v in sorted(cls_claim.items())))
    print(f"  miss-rate sample (non-CLAIM context hits): {len(samp_A)}/{len(samp)} found to be class A"
          + (f" -> {', '.join(samp_A)}" if samp_A else ""))
    files = sorted({r["path"] for r in A})
    print(f"  CLASS A (correction candidates): {len(A)} lines in {len(files)} files "
          f"({sum(r['copy'] == '1' for r in A)} lines are snapshot/generated copies)\n")
    for r in A:
        print(f"  {r['path']}:{r['line']}{'  [copy]' if r['copy'] == '1' else ''}\n      {r['note']}")


if __name__ == "__main__":
    {"extract": extract, "merge": merge}[sys.argv[1] if len(sys.argv) > 1 else "extract"]()
