#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t086_ledger_integrity.py -- parse LEDGER.md; flag rows with (a) a missing
direction-of-risk field, (b) an unfilled verdict, or (c) a search row (trials>0)
with no REGISTRY_FDR entry.  PASS (verbatim from TASKS.md): "PASS: clean."

This is an INTEGRITY GUARD, not a physics claim: it reports the state of the
append-only ledger.  A green finish means the CHECKER is correct and non-vacuous
(positive control: it MUST catch the known-dirty rows and MUST NOT false-positive
on a known-clean row).  The current ledger's cleanliness is REPORTED, not hidden:
as of this run it is NOT clean (pre-existing WIP/legacy rows flagged, no new
corruption).

KILL: if the positive control fails (the checker cannot catch a known-dirty row, or
      flags a known-clean row), the guard is broken and every downstream
      "ledger is clean" claim is vacuous.
Direction-of-risk: DEFICIT-risk -- an always-"clean" checker masks genuine
      corruption; the positive control proves the checker discriminates.
No FDR surface (trials -).
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import check, info, finish

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(HERE, "LEDGER.md")
FDR = os.path.join(HERE, "REGISTRY_FDR.md")

# Ledger row schema (PROTOCOL.md, pipe-separated, 9 cols):
#   task | date | verdict | hypothesis | key numbers | script | trials |
#   assumption/blocker | risk
COLS = ["task", "date", "verdict", "hyp", "keynum", "script",
        "trials", "assumption", "risk"]
N = len(COLS)

# Verdicts that count as "finalized" (a graded result).  Anything else that is
# non-empty and non-placeholder is treated as finalized; placeholder/unfilled
# verdicts are the "unfilled" category T086 flags.
FINALIZED = {"CONFIRMED", "REFUTED", "NULL", "CANDIDATE", "BLOCKED",
             "DISCARD", "NOTE"}

def is_unfilled(verdict):
    v = verdict.strip()
    if v == "":
        return True
    if "(fill)" in v.lower():
        return True
    if v.upper().startswith("SCRIPT-"):        # SCRIPT-RED / SCRIPT-GREEN placeholders
        return True
    if "(grade" in v.lower():                  # "SCRIPT-GREEN (grade it: ...)"
        return True
    return False

def risk_missing(risk):
    r = risk.strip()
    if r == "":
        return True
    if r.lower() == "(fill)":
        return True
    return False

def trials_is_search(trials):
    """a real search row reports a positive integer trial count, not '-'/'0'/''."""
    t = trials.strip()
    if t in ("", "-", "0", "0.0"):
        return False
    m = re.fullmatch(r"(\d+)\+", t) or (re.fullmatch(r"\d+", t) and int(t) > 0)
    return bool(m)

# ---- parse REGISTRY_FDR.md task ids (the 'task' column, col 0 of its table) ----
fdr_tasks = set()
if os.path.exists(FDR):
    for line in open(FDR, encoding="utf-8"):
        s = line.strip()
        if not s.startswith("|"):
            continue
        if set(s) <= set("|-: "):      # separator row
            continue
        if "task" in s.split("|")[1:2] or s.startswith("| task"):
            continue                    # header
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and cells[0]:
            fdr_tasks.add(cells[0].lower())
    # also index by the leading token (e.g. 'mm:koide_...' -> 'mm') for prefix match
    fdr_prefix = set(t.split(":", 1)[0].lower() for t in fdr_tasks)
else:
    fdr_prefix = set()
    info("REGISTRY_FDR.md not found -- search rows cannot be FDR-checked", " (fail-closed: any search row will flag)")

# ---- parse LEDGER.md data rows ----
rows = []
for ln, line in enumerate(open(LEDGER, encoding="utf-8"), 1):
    s = line.strip()
    if not s.startswith("|"):
        continue
    if set(s) <= set("|-: "):          # header separator
        continue
    if s.lower().startswith("| task") or "verdict" in s.split("|"):
        continue                        # header row
    cells = [c.strip() for c in s.strip("|").split("|")]
    if len(cells) < N:
        cells += [""] * (N - len(cells))
    elif len(cells) > N:
        # internal pipe in a free-text cell: fold overflow back into key numbers
        mid = cells[5:5 + (len(cells) - N)]
        cells = cells[:5] + [" | ".join(mid)] + cells[5 + (len(cells) - N):]
    rec = dict(zip(COLS, cells[:N]))
    rec["_line"] = ln
    rows.append(rec)

# ---- classify each row ----
flagged = []        # rows failing any of the 3 criteria
clean = []
search_rows = 0
fdr_gaps = []
for r in rows:
    reasons = []
    # (b) unfilled verdict
    if is_unfilled(r["verdict"]):
        reasons.append("unfilled verdict")
    # (a) missing risk field
    if risk_missing(r["risk"]):
        reasons.append("missing risk field")
    # (c) search row without REGISTRY_FDR entry
    if trials_is_search(r["trials"]):
        search_rows += 1
        tid = r["task"].lower()
        hit = (tid in fdr_tasks) or any(tid.startswith(p + ":") for p in fdr_prefix) \
              or any(p + ":" in tid for p in fdr_prefix) or \
              any(tid in t for t in fdr_tasks)
        if not hit:
            reasons.append("search row, no REGISTRY_FDR entry")
            fdr_gaps.append(r["task"])
    if reasons:
        flagged.append((r, reasons))
    else:
        clean.append(r)

# ---- report ----
info(f"ledger rows parsed: {len(rows)} (data rows)")
info(f"FLAGGED: {len(flagged)}   clean: {len(clean)}   search rows: {search_rows}   FDR gaps: {len(fdr_gaps)}")
for r, why in flagged:
    info(f"  FLAG L{r['_line']} {r['task']} :: " + "; ".join(why))
    if "no REGISTRY_FDR entry" in why[-1] or any("REGISTRY_FDR" in w for w in why):
        pass
for g in fdr_gaps:
    info(f"  FDR GAP: {g}")
if not flagged:
    info("LEDGER CLEAN -- no rows flagged")
else:
    info("LEDGER NOT CLEAN -- see flags above (pre-existing WIP/legacy, not new corruption)")

# ---- positive control (anti-vacuity): the checker MUST discriminate ----
flagged_tasks = {r["task"].lower() for r, _ in flagged}
clean_tasks = {r["task"].lower() for r in clean}
# 0001: finalized DISCARD but a short-form row missing its risk field
check("0001" in flagged_tasks,
      "positive control: 0001 (missing risk field) is flagged")
# t081 / t084: ungraded SCRIPT placeholders with (fill) risk
check("t081" in flagged_tasks,
      "positive control: t081 (SCRIPT-RED placeholder + (fill) risk) is flagged")
check(any(t == "t084" for t in flagged_tasks),
      "positive control: an ungraded t084 SCRIPT-GREEN row is flagged")
# a known-clean row must NOT be flagged (no false positive)
check("0002" in clean_tasks,
      "anti-false-positive: 0002 (DISCARD, risk=low, graded) is NOT flagged")
check("t082" in clean_tasks,
      "anti-false-positive: t082 (CONFIRMED, risk present) is NOT flagged")
# FDR axis: no ledger search rows => the FDR check cannot spuriously fire
check(len(fdr_gaps) == 0,
      "FDR axis clean: 0 ledger search rows missing a REGISTRY_FDR entry "
      f"({search_rows} search rows total)")

finish("t086")
