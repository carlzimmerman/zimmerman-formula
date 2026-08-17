#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t087_refutation_tracker.py -- Refutation-duty tracker.

TASKS.md T087: "Script listing every CONFIRMED ledger row without a linked
refutation attempt.  PASS: the list (the adversarial loop's memory)."

WHAT IT DOES
  Parses LEDGER.md, collects every row whose verdict is exactly CONFIRMED, and
  for each checks whether a *separate* ledger row is a refutation attempt that
  LINKS to it.  Per PROTOCOL.md line 30-31 a refutation attempt is "its own run"
  -- a distinct ledger row that (a) is refutation-flavoured (names the act of
  re-checking / refuting / adversarially testing something) AND (b) names the
  target CONFIRMED task id in its free text.  A CONFIRMED row with NO such
  linker is "refutation duty owed" and is the tracker's output.

This is a TRACKER / integrity guard, NOT a physics claim (guard precedent:
t082/t083/t084/t085/t086).  Grading CONFIRMED means the tracker is built and its
positive control proves it discriminates -- it is neither always-empty (would
mask owed duties) nor always-full (would ignore successful refutations).  The
*current* state -- which CONFIRMED rows still owe a refutation -- is REPORTED in
the key-numbers, not hidden.

KILL: if the positive control fails (a synthetic refutation attempt does NOT drop
      its target off the un-refuted list, OR a self-reference falsely counts as a
      refutation) the linker is vacuous and "no duties owed" would be untrustworthy.
Direction-of-risk: DEFICIT-risk -- an always-empty list hides adversarial debt;
      the positive/negative controls prove the list reflects real state.
No FDR surface (trials -).
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import check, info, finish

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(HERE, "LEDGER.md")
OUT = os.path.join(HERE, "REFUTATION_DUTY.md")

# Ledger row schema (PROTOCOL.md, pipe-separated, 9 cols):
COLS = ["task", "date", "verdict", "hyp", "keynum", "script",
        "trials", "assumption", "risk"]
N = len(COLS)

# A refutation attempt must be refutation-FLAVOURED.  Deliberately narrow so a
# grade-it placeholder that merely lists verdicts ("CONFIRMED/REFUTED/NULL") does
# not itself read as an attempt -- linking also requires naming a DIFFERENT
# CONFIRMED id, which such a placeholder never does.
REFUT_KW = ["refut", "adversar", "re-check", "recheck", "re-check",
            "re-exam", "reexam", "retest", "re-test", "survive"]
REFUT_SFX = ("ref", "advers", "recheck", "retest")   # task-id suffix signals

# finalized verdicts that may constitute a completed refutation run
REFUTED_VERDICTS = {"REFUTED", "NULL", "CANDIDATE", "DISCARD", "NOTE"}


def token_hit(tid, text):
    """Does `tid` appear as a standalone token in `text` (word-bounded)?
    't081' must NOT match inside 't081b'; '0002' must NOT match '0001'."""
    pat = r"(?<![\w])" + re.escape(tid) + r"(?![\w])"
    return re.search(pat, text) is not None


def is_refut_flavoured(r):
    blob = " ".join([r.get("task", ""), r.get("hyp", ""), r.get("keynum", ""),
                     r.get("assumption", ""), r.get("risk", "")]).lower()
    if any(k in blob for k in REFUT_KW):
        return True
    # task-id suffix signal, e.g. 't082ref', 't083-adversarial'
    tid = r.get("task", "").lower()
    if any(tid.endswith(s) for s in REFUT_SFX):
        return True
    return False


def links_to(target_tid, r):
    """A distinct row r links to CONFIRMED target iff refutation-flavoured AND
    names the target id AND is not the target row itself."""
    if r["_task"].lower() == target_tid.lower():
        return False                       # self-reference is not a refutation
    # T090 consolidation fix: the target must be named in the attempt's OWN
    # hypothesis (its declared subject).  As the ledger grew, newer CONFIRMED
    # guard rows (t088/t089) enumerated the guard family in the assumption column
    # ("...matching the t082/t083/.../t087 guard precedent") while being
    # refutation-flavoured, and the old hyp+keynum+assumption blob let those
    # enumerations falsely count as attempts -- dropping t083/t086 from the owed
    # list and firing the positive control.  Restricting the name search to the
    # hypothesis keeps a genuine attempt (t082ref, whose hyp names its target)
    # while rejecting a passing guard-family enumeration.
    hyp = r.get("hyp", "")
    return is_refut_flavoured(r) and token_hit(target_tid, hyp)


def parse_rows(path):
    rows = []
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        if set(s) <= set("|-: "):               # separator row
            continue
        if s.lower().startswith("| task") or "verdict" in s.split("|"):
            continue                             # header row
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < N:
            cells += [""] * (N - len(cells))
        elif len(cells) > N:                     # internal pipe: fold into keynum
            extra = len(cells) - N
            mid = cells[5:5 + extra]
            cells = cells[:5] + [" | ".join(mid)] + cells[5 + extra:]
        rec = dict(zip(COLS, cells[:N]))
        rec["_line"] = ln
        rec["_task"] = rec["task"]
        rows.append(rec)
    return rows


def confirmed_targets(rows):
    return [r for r in rows if r["verdict"].strip().upper() == "CONFIRMED"]


def un_refuted(rows, extra_attempts=()):
    """Return CONFIRMED rows with no linked refutation attempt, given the ledger
    rows plus any synthetic attempt rows (for the positive control)."""
    all_rows = list(rows) + list(extra_attempts)
    targets = confirmed_targets(rows)             # targets come from the ledger
    out = []
    for t in targets:
        tid = t["_task"]
        has_attempt = any(links_to(tid, r) for r in all_rows
                          if r is not t and r.get("_task", "") != tid or
                          links_to(tid, r) and r is not t)
        # simpler, unambiguous: a linker that is not the target row itself
        has_attempt = any(links_to(tid, r) for r in all_rows if r is not t)
        if not has_attempt:
            out.append(t)
    return out


# ---- run ----
rows = parse_rows(LEDGER)
targets = confirmed_targets(rows)
owed = un_refuted(rows)

info(f"ledger data rows parsed: {len(rows)}")
info(f"CONFIRMED rows: {len(targets)}  -> "
     f"{[t['_task'] for t in targets]}")
info(f"refutation duty OWED (CONFIRMED, no linked attempt): {len(owed)}  -> "
     f"{[t['_task'] for t in owed]}")

# ---- write the durable memory artifact ----
with open(OUT, "w", encoding="utf-8") as f:
    f.write("# REFUTATION_DUTY -- CONFIRMED rows awaiting an adversarial re-check\n")
    f.write("# Generated by runs/t087_refutation_tracker.py (adversarial-loop memory).\n")
    f.write("# A row is 'owed' when NO separate ledger row is a refutation attempt\n")
    f.write("# that names its task id.  Clear the list by writing the re-check runs.\n")
    f.write(f"# CONFIRMED total: {len(targets)}  |  owed: {len(owed)}\n\n")
    if owed:
        for t in owed:
            f.write(f"- {t['task']} (L{t['_line']}) :: {t['hyp'][:90]}\n")
    else:
        f.write("(none -- every CONFIRMED row has survived an adversarial re-check)\n")
info(f"wrote {os.path.relpath(OUT, HERE)} ({len(owed)} owed)")

# ---- positive control (anti-vacuity): a real attempt MUST drop its target ----
# The current ledger has zero refutation attempts, so 'owed' == all CONFIRMED.
# Synthesize one adversarial re-check naming a real CONFIRMED target and confirm
# that target leaves the owed list while the others stay.
synthetic = dict(task="t082ref", date="2026-08-15",
                 verdict="REFUTED",
                 hyp="adversarial re-check of t082 frozen-guard",
                 keynum="injected synthetic attempt",
                 script="control", trials="-",
                 assumption="positive control", risk="control")
synthetic["_line"] = 0
synthetic["_task"] = "t082ref"
owed_after = un_refuted(rows, extra_attempts=[synthetic])
owed_ids_after = {t["_task"].lower() for t in owed_after}

check(all(t["_task"].lower() != "t082" for t in owed_after),
      "positive control: a synthetic refutation attempt referencing t082 drops "
      "t082 off the owed list")
check(any(t["_task"].lower() == "t083" for t in owed_after),
      "positive control: t083 (no attempt) REMAINS owed -- the list is not "
      "always-empty")
check(any(t["_task"].lower() == "t086" for t in owed_after),
      "positive control: t086 (no attempt) REMAINS owed -- the list is not "
      "always-empty")

# ---- negative control: a self-reference must NOT count as a refutation ----
# A CONFIRMED row that merely mentions its own id + refut-wording is NOT a
# linker for itself (links_to excludes the target row itself).
check(not any(links_to(t["_task"], t) for t in targets),
      "negative control: no CONFIRMED row is its own refutation attempt "
      "(self-reference excluded)")

# ---- the honest current state ----
# Guard built + both controls pass => the tracker is non-vacuous.  The owed list
# being non-empty is the *reported* truth (duties are owed), not a failure.
check(owed_ids_after != {t["_task"].lower() for t in targets},
      "discrimination: owed-set changes under a real attempt (neither "
      "always-full nor always-empty)")

info("tracker built; positive + negative controls pass; owed list reported "
     "honestly above")
finish("t087")
