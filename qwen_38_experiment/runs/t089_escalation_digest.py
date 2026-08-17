#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t089_escalation_digest.py -- T089 Escalation digest.

PASS (verbatim from TASKS.md): "Script that formats ESCALATE.md into a one-page
digest for Carl with dates and blocking tasks. PASS: the digest."

CONSOLIDATION/INFRASTRUCTURE task, not a physics claim: build the machine that
reduces the append-only ESCALATE.md (Carl's decision log) to a one-page digest --
every escalation with its DATE, STATUS (OPEN / RESOLVED), the DECISION-FOR-CARL
ask, and the BLOCKING TASKS the loop cannot advance past.  A green finish means
the builder is correct and non-vacuous: a positive control proves it MUST parse a
synthetic OPEN entry and a synthetic RESOLVED entry, extract their dates, surface
a blocking task, and CLEAR it when a RESOLVED note supersedes it -- even though
the real ESCALATE.md's single escalation is already RESOLVED.

APPEND-ONLY SEMANTICS (the crux): ESCALATE.md is a log Carl appends to; a
RESOLVED bullet supersedes EVERYTHING at and before it, including its own
section's OPEN lines.  In the real file the 2026-08-15 re-occurrence section
carries its OWN "STUCK / cannot advance / PENDING" complaint lines AND the
trailing "- RESOLVED (frontier model ...)" bullet in the same ## block; that
bullet resolves the whole section.  So a blocking line is OPEN only if NO RESOLVED
bullet appears at or after its section.  The honest current state is therefore
"0 open blocking tasks -- the loop is unblocked", and the digest must say so,
not print a stale OPEN count.
Direction-of-risk: WIN-risk -- a parser that cannot detect RESOLVED would keep
Carl re-acting on a bug that is already fixed; the positive control proves the
parser discriminates OPEN vs RESOLVED and clears a block on resolution.
No FDR surface (trials -).
"""
import sys, os, re, datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import check, info, finish

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESC = os.path.join(HERE, "ESCALATE.md")
OUT = os.path.join(HERE, "ESCALATION_DIGEST.md")

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
HDR_RE = re.compile(r"^##\s+(.*)$")
RESOLVED_TOKEN = "RESOLVED"
DECISION_TOKEN = "DECISION FOR CARL"
# a "blocking task" bullet: the loop is stuck / cannot advance / waiting on a fix
BLOCK_RE = re.compile(r"\b(STUCK|block|cannot advance|PENDING|until the|re-?dispatch|"
                      r"re-?issue)\b", re.I)


def bullets_of(lines):
    """Join ESCALATE.md continuation lines into logical bullets: a top-level
    '- ' line starts a bullet; indented / code continuation lines extend it."""
    out, buf = [], ""
    for ln in lines:
        if ln.lstrip().startswith("- "):
            if buf:
                out.append(buf.strip())
            buf = ln
        else:
            buf = (buf + " " + ln) if buf else ln
    if buf.strip():
        out.append(buf.strip())
    return [b for b in out if b.strip()]


def bullet_resolved(b):
    return b.lstrip("- ").lstrip().upper().startswith(RESOLVED_TOKEN)


def decision_of(bullets):
    for b in bullets:
        m = re.search(r"DECISION FOR CARL[:\-]\s*(.*)", b, re.I)
        if m:
            return m.group(1).strip()
    return ""


def parse_sections(text):
    """Split ESCALATE.md into ## sections; decorate each with date, title,
    status, decision-for-carl, and its blocking bullets.  The leading single-#
    title line stays outside any section."""
    lines = text.splitlines()
    sections, cur = [], None
    for ln in lines:
        m = HDR_RE.match(ln)
        if m:
            if cur is not None:
                sections.append(cur)
            cur = {"raw": m.group(1).strip(), "lines": []}
        elif cur is not None:
            cur["lines"].append(ln)
    if cur is not None:
        sections.append(cur)

    for s in sections:
        raw = s["raw"]
        dm = DATE_RE.search(raw)
        s["date"] = dm.group(1) if dm else "(no date)"
        s["title"] = (raw[dm.end():].lstrip(" -—:") if dm else raw).strip()
        blts = bullets_of(s["lines"])
        s["bullets"] = blts
        # RESOLVED if the header carries the token or ANY bullet resolves the section
        s["status"] = "RESOLVED" if (RESOLVED_TOKEN in raw.upper()
                                     or any(bullet_resolved(b) for b in blts)) else "OPEN"
        s["decision"] = decision_of(blts)
        s["blocking"] = [b for b in blts if BLOCK_RE.search(b)]
    return sections


def open_blocks(sections):
    """Append-only: a blocking bullet is CLEARED if its section -- or any later
    section -- carries a RESOLVED status.  OPEN only if NO RESOLVED bullet appears
    at or after the block's own section."""
    n = len(sections)
    future_resolved = [False] * n
    running = False
    for i in range(n - 1, -1, -1):
        if sections[i]["status"] == "RESOLVED":
            running = True
        future_resolved[i] = running
    open_b, cleared = [], []
    for i, s in enumerate(sections):
        for b in s["blocking"]:
            rec = (s["date"], b)
            (cleared if future_resolved[i] else open_b).append(rec)
    return open_b, cleared


def write_digest(path, sections, open_b, cleared):
    n_open = len([s for s in sections if s["status"] == "OPEN"])
    n_res = len([s for s in sections if s["status"] == "RESOLVED"])
    L = []
    L.append("# ESCALATION DIGEST -- one page for Carl")
    L.append("")
    L.append(f"Generated by t089_escalation_digest.py at "
             f"{datetime.datetime.now().isoformat(timespec='seconds')}Z.")
    L.append("")
    L.append(f"Escalations: {len(sections)} total -- {n_open} OPEN, "
             f"{n_res} RESOLVED.  Blocking tasks: {len(open_b)} OPEN, "
             f"{len(cleared)} cleared by a RESOLVED note.")
    L.append("")
    # ---- per-escalation table (date | status | title | decision-for-carl) ----
    L.append("## Escalations (date · status · ask)")
    L.append("")
    L.append("| date | status | title | decision for Carl |")
    L.append("| --- | --- | --- | --- |")
    for s in sections:
        dec = s["decision"] or "—"
        dec = (dec[:160] + "…") if len(dec) > 160 else dec
        L.append(f"| {s['date']} | {s['status']} | {s['title']} | {dec} |")
    L.append("")
    # ---- blocking tasks: OPEN vs cleared ----
    L.append("## Blocking tasks")
    L.append("")
    if open_b:
        L.append("### OPEN (loop cannot advance past these)")
        for d, b in open_b:
            L.append(f"- ({d}) {b}")
    else:
        L.append("### OPEN -- none")
        L.append("")
        L.append("0 blocking tasks are open: every logged block is superseded by a "
                  "RESOLVED note (append-only semantics). The loop is unblocked.")
    if cleared:
        L.append("")
        L.append("### CLEARED (superseded by a RESOLVED note)")
        for d, b in cleared:
            L.append(f"- ({d}) {b}")
    L.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


# ---- positive control (anti-vacuity): the builder MUST discriminate ----
syn = (
    "# ESCALATE -- decisions that belong to Carl\n"
    "\n"
    "## 2026-01-01 -- bogus PROMOTE S0001 re-dispatched\n"
    "- the loop is STUCK on this re-issued duty; it cannot advance to T101-T120\n"
    "- DECISION FOR CARL: fix the pursued-filter to key off the GRADE field\n"
    "- until the filter is fixed, S0001 re-dispatches every session\n"
    "\n"
    "## RESOLVED (frontier model, 2026-01-02): the filter was patched\n"
    "- the worker's refusal was correct; the bug is fixed\n"
)
s_syn = parse_sections(syn)
check(len(s_syn) == 2, "control: two ## sections parsed")
check(s_syn[0]["status"] == "OPEN" and s_syn[1]["status"] == "RESOLVED",
      "control: first section OPEN, second RESOLVED (parser discriminates)")
check(s_syn[0]["date"] == "2026-01-01" and s_syn[1]["date"] == "2026-01-02",
      "control: dates extracted from both section headers")
check("fix the pursued-filter" in s_syn[0]["decision"],
      "control: DECISION-FOR-CARL clause extracted from the OPEN section")
ob, cl = open_blocks(s_syn)
check(any("STUCK" in b[1].upper() for b in cl) and len(ob) == 0,
      "control: a RESOLVED note supersedes the earlier OPEN block, 0 remain open")
# a fresh OPEN escalation with NO resolution must surface as open
syn2 = ("## 2026-03-03 -- new open escalation\n"
        "- the loop cannot advance until X exists\n"
        "- DECISION FOR CARL: choose X now\n")
s2 = parse_sections(syn2)
ob2, _ = open_blocks(s2)
check(len(ob2) >= 1 and s2[0]["status"] == "OPEN",
      "control: a lone OPEN escalation surfaces an open block (no false clear)")
ctrl = os.path.join(HERE, "runs", "t089_control_tmp.md")
write_digest(ctrl, s_syn, ob, cl)
back = open(ctrl, encoding="utf-8").read()
check("## Escalations" in back and "### CLEARED" in back,
      "control: digest writer emits the escalation table and a CLEARED section")
os.remove(ctrl)

# ---- the real digest ----
sections = parse_sections(open(ESC, encoding="utf-8").read())
check(len(sections) >= 1, "real: at least one escalation section parsed")
n_res = len([s for s in sections if s["status"] == "RESOLVED"])
check(n_res >= 1, "real: a RESOLVED note is detected in ESCALATE.md")
open_b, cleared = open_blocks(sections)
write_digest(OUT, sections, open_b, cleared)

# ---- structural invariants (always true, non-vacuous, re-runnable) ----
check(all(s["status"] in ("OPEN", "RESOLVED") for s in sections),
      "invariant: every section carries a binary OPEN/RESOLVED status")
check(os.path.exists(OUT), "PASS: ESCALATION_DIGEST.md written")
out_txt = open(OUT, encoding="utf-8").read()
check("ESCALATION DIGEST" in out_txt and "## Blocking tasks" in out_txt,
      "digest carries its title and a blocking-tasks section")
check(f"{len(open_b)} OPEN" in out_txt, "digest states the honest open-block count")
label = out_txt.split("### OPEN")[1][:10] if "### OPEN" in out_txt else ""
check((len(open_b) == 0) == ("none" in label),
      "digest OPEN/cleared label agrees with the computed open-block count")

# ---- honest current state (dynamic; cannot contradict the computed count) ----
info(f"sections parsed: {len(sections)} "
     f"({len([s for s in sections if s['status']=='OPEN'])} OPEN, {n_res} RESOLVED)")
info(f"blocking tasks: {len(open_b)} OPEN, {len(cleared)} cleared by a RESOLVED note")
if open_b:
    info(f"HONEST STATE: {len(open_b)} OPEN blocking task(s) in ESCALATE.md as of this run "
         "(the loop is still blocked -- see the digest).")
else:
    info("HONEST STATE: ESCALATE.md's escalation family is RESOLVED "
          "(2026-08-15 frontier note); 0 open blocking tasks -- the loop is unblocked.")
finish("t089")
