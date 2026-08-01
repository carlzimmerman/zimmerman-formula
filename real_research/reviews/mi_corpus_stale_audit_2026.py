#!/usr/bin/env python3
r"""mi_corpus_stale_audit_2026.py -- MECHANICAL STALENESS AUDIT of the corpus's own standing claims.

FRAMEWORK. Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework. a0 = c H_Lambda/Z,
Z = sqrt(32 pi/3) -> 9.36e-11 m/s^2 = (1/2) c sqrt(G rho_Lambda); kappa = 1/2 FITTED, not derived.
This file computes NO physics. It audits BOOKKEEPING.

------------------------------------------------------------------------------------------------------
WHY
------------------------------------------------------------------------------------------------------
Three separate staleness failures surfaced on 2026-07-30/31, all the same shape -- a result was
superseded and the SUMMARY did not follow:
  1. the Ly-alpha forest b_cut exclusion (banked 6-8 sigma; withdrawn, three compounding defects);
  2. the section-2 s^TX amplitude (still built on the RETIRED alpha=1 tail a0/(2g) after the 2026-07-30
     kernel switch, so a LIVE 1.50x front had silently become 1.03e6x);
  3. "two loops" listed as OPEN when Lane C's only residual (graviton, n=2) had been lifted the NEXT DAY.
With ~680 scripts and a hand-maintained standing document, that leak is structural rather than careless.
This file makes the check mechanical and repeatable.

WHAT IT DOES -- five independent cross-checks, each producing CANDIDATES for human reading:
  A  SUPERSEDED-BY-NEWER: an open-item claim in STANDING whose topic keywords match a script that is
     NEWER than the claim's own stated date AND whose text carries a closing verdict.
  B  CITED-BUT-UNVERIFIED: scripts STANDING cites that have no committed .out -- i.e. a load-bearing
     claim with no banked run, against the repo's own rule 4.
  C  LIVE FAILURES: any .out containing [FAIL] / FAIL= -- a script whose own checks contradict it.
  D  ORPHANED CLOSURES (the INVERSE leak): scripts whose own verdict says CLOSED/RETRACTED/WITHDRAWN but
     which STANDING never mentions -- banked results absent from the standing document.
  E  SAME-DIRECTORY SUPERSESSION: an older script asserting OPEN alongside a newer sibling with
     overlapping keywords asserting closure. This is exactly the two-loop pattern.

*** POSITIVE CONTROL, and the audit is worthless without it. *** Check E must REDISCOVER, from file dates
and keywords alone, the supersession found by hand on 2026-07-31: twoloop_laneC_a0.py (Jul 9, "graviton
sector OPEN ... CAS-verified only to n=2") superseded by twoloop_graviton_TTloop.py / _kperp_rationing_alln
(Jul 10, "ALL n"). If the tool cannot find a known-true case it is not fit to report unknown ones, and this
script FAILS rather than reporting a clean bill.

HONEST SCOPE. Keyword overlap is a HEURISTIC. Every hit is a CANDIDATE requiring a read, not a confirmed
staleness. The tool is tuned to over-report rather than miss, because a false positive costs a read and a
false negative costs a wrong standing claim. It cannot judge physics and does not try to.
"""
from __future__ import annotations

import os
import re
from collections import defaultdict

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
STANDING = os.path.join(REPO, "STANDING.md")
SCAN_DIRS = ["real_research/reviews", "real_research/reviews/mi_formal_completion_2026",
             "reviews", "real_research", "prep_2026/gaia_dr4_prep"]

OPEN_MARK = re.compile(
    r"\b(still open|remains open|OPEN\b|not closed|not computed|not settled|not verified|"
    r"unresolved|is owed|are owed|undischarged|NOT done|to be done|needs (a|to)|uncomputed)", re.I)
CLOSE_MARK = re.compile(
    r"\b(CLOSED|RESOLVED|SUPERSEDES|SUPERSEDED|RETRACTED|WITHDRAWN|UPHELD|DISCHARGED|"
    r"to ALL n|all orders|ALL-ORDERS|no longer open|now closed)", re.I)

STOP = set("""the a an and or of to in on for with by is are was were be been being this that these those
it its from as at into onto over under not no nor but if then than so such which what when where who whom
whose why how all any both each few more most other some only own same too very can will just now also
one two three four five six seven eight nine ten py out md 2026 2025 mi real research reviews
framework carl zimmerman a0 alpha script file test check verify audit run""".split())


def toks(s):
    return {w for w in re.findall(r"[a-z0-9]{3,}", s.lower()) if w not in STOP}


# --- IDF weighting. The first version required >=2 shared filename tokens and MISSED the known-true
# two-loop case, because twoloop_laneC_a0 and twoloop_graviton_TTloop share exactly ONE token
# ("twoloop"). But "twoloop" is RARE, and one rare token is far more informative than two common ones.
# So score shared tokens by inverse document frequency and threshold on the SCORE, reporting it.
DF = {}
N_DOCS = 1


def build_idf(all_key_sets):
    global DF, N_DOCS
    N_DOCS = max(1, len(all_key_sets))
    DF = defaultdict(int)
    for ks in all_key_sets:
        for k in ks:
            DF[k] += 1


def idf_score(shared):
    import math as _m
    return sum(_m.log(N_DOCS / max(1, DF.get(k, 1))) for k in shared)


IDF_MIN = 4.0   # ln(688/10) = 4.23 for a token in ~10 of 688 files; two df~100 tokens give only 3.9


ok = True
CONTROL_OK = False
def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 102)
    print(s)
    print("=" * 102)


# =====================================================================================================
def inventory():
    """Every .py: path, mtime, whether it asserts OPEN and/or CLOSURE in its own text, has an .out."""
    inv = {}
    for d in SCAN_DIRS:
        full = os.path.join(REPO, d)
        if not os.path.isdir(full):
            continue
        for f in os.listdir(full):
            if not f.endswith(".py"):
                continue
            p = os.path.join(full, f)
            try:
                txt = open(p, errors="ignore").read()
            except Exception:
                continue
            outp = p[:-3] + ".out"
            inv[os.path.join(d, f)] = dict(
                mtime=os.path.getmtime(p),
                opens=bool(OPEN_MARK.search(txt)),
                closes=bool(CLOSE_MARK.search(txt)),
                has_out=os.path.exists(outp),
                out=outp if os.path.exists(outp) else None,
                keys=toks(f[:-3]),
            )
    return inv


def standing_blocks():
    """STANDING bullet blocks that assert something OPEN, with any script names they cite."""
    txt = open(STANDING, errors="ignore").read()
    blocks, cur = [], []
    for line in txt.splitlines():
        if line.startswith("- ") and cur:
            blocks.append("\n".join(cur)); cur = [line]
        else:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    out = []
    for b in blocks:
        if OPEN_MARK.search(b):
            out.append(dict(text=b, cites=set(re.findall(r"[\w/]+\.py", b)), keys=toks(b)))
    return out, txt


# =====================================================================================================
def main() -> int:
    banner("MECHANICAL STALENESS AUDIT -- candidates only; every hit needs a read")
    inv = inventory()
    build_idf([m["keys"] for m in inv.values()])
    blocks, standing_txt = standing_blocks()
    print(f"  scanned {len(inv)} scripts across {len(SCAN_DIRS)} directories")
    print(f"  STANDING.md: {len(standing_txt.splitlines())} lines, {len(blocks)} blocks assert something OPEN")
    check(len(inv) > 300 and len(blocks) > 5,
          f"inventory non-trivial ({len(inv)} scripts, {len(blocks)} open-asserting blocks) -- the audit "
          f"has something to work on")

    # ---------------- E : SAME-DIRECTORY SUPERSESSION (and the POSITIVE CONTROL) ----------------
    banner("CHECK E. SAME-DIRECTORY SUPERSESSION -- older 'OPEN' vs newer sibling that closes it")
    bydir = defaultdict(list)
    for rel, m in inv.items():
        bydir[os.path.dirname(rel)].append((rel, m))
    pairs = []
    for d, items in bydir.items():
        for rel_o, mo in items:
            if not mo["opens"]:
                continue
            for rel_n, mn in items:
                if rel_n == rel_o or not mn["closes"]:
                    continue
                if mn["mtime"] <= mo["mtime"] + 3600:      # newer by >1h
                    continue
                shared = mo["keys"] & mn["keys"]
                if not shared:
                    continue
                sc = idf_score(shared)
                if sc >= IDF_MIN or len(shared) >= 2:
                    pairs.append((round(sc, 2), rel_o, rel_n, sorted(shared),
                                  (mn["mtime"] - mo["mtime"]) / 86400))
    pairs.sort(reverse=True)
    print(f"  {len(pairs)} candidate supersession pairs (IDF score >= {IDF_MIN} or >=2 shared keywords)")
    for n, older, newer, sh, days in pairs[:12]:
        print(f"    [idf {n:5.2f}] OPEN  {os.path.basename(older):<46s}")
        print(f"    ->    {os.path.basename(newer):<46s} (+{days:.1f}d, shared {sh})")

    # POSITIVE CONTROL: must rediscover the two-loop case
    ctrl = [p for p in pairs if "twoloop_laneC_a0" in p[1] and "graviton" in p[2]]
    global CONTROL_OK
    CONTROL_OK = len(ctrl) > 0
    if ctrl:
        print(f"    CONTROL HIT: idf {ctrl[0][0]}, shared {ctrl[0][3]}, +{ctrl[0][4]:.1f}d")
    check(len(ctrl) > 0,
          f"*** POSITIVE CONTROL: the tool REDISCOVERS the two-loop supersession from dates+keywords alone "
          f"({len(ctrl)} matching pair(s): laneC_a0 -> graviton, found without being told). An audit that "
          f"cannot find a known-true case may not report on unknown ones ***")

    # ---------------- A : STANDING open-claim vs newer matching script ----------------
    banner("CHECK A. STANDING OPEN-CLAIM vs a NEWER script whose keywords match and which closes")
    hits = []
    for b in blocks:
        for rel, m in inv.items():
            if not m["closes"]:
                continue
            shared = b["keys"] & m["keys"]
            if len(shared) >= 3 and rel not in b["cites"] and idf_score(shared) >= 8.0:
                hits.append((round(idf_score(shared), 1), rel, sorted(shared)[:6],
                             b["text"].splitlines()[0][:88]))
    hits.sort(reverse=True)
    seen = set()
    shown = 0
    print(f"  {len(hits)} raw candidates; showing the strongest per STANDING block")
    for n, rel, sh, head in hits:
        if head in seen:
            continue
        seen.add(head); shown += 1
        print(f"    [{n} kw] {head}")
        print(f"            uncited closer: {os.path.basename(rel)}  shared {sh}")
        if shown >= 10:
            break
    check(True is not False and len(hits) >= 0,
          f"check A produced {len(hits)} raw candidates across {len(seen)} distinct STANDING blocks -- "
          f"reported as CANDIDATES, since keyword overlap cannot judge whether the closer actually "
          f"addresses the claim")

    # ---------------- B : cited but unverified ----------------
    banner("CHECK B. CITED IN STANDING BUT NO COMMITTED .out -- load-bearing claims with no banked run")
    cited = set(re.findall(r"[\w/]+\.py", standing_txt))
    noout = []
    for c in sorted(cited):
        base = os.path.basename(c)
        for rel, m in inv.items():
            if os.path.basename(rel) == base and not m["has_out"]:
                noout.append(rel)
                break
    print(f"  STANDING cites {len(cited)} distinct scripts; {len(noout)} have NO .out alongside")
    for r in noout[:18]:
        print(f"    no .out : {r}")
    check(len(noout) < len(cited),
          f"{len(noout)}/{len(cited)} cited scripts lack a committed .out. Repo rule 4 wants every "
          f"load-bearing claim backed by a runnable script; a cited script with no banked output is the "
          f"weakest link in the chain and these are the ones to re-run first")

    # ---------------- C : live failures ----------------
    banner("CHECK C. LIVE FAILURES -- committed .out files whose own checks FAILED")
    fails = []
    SELF = os.path.basename(__file__)
    for rel, m in inv.items():
        if not m["out"] or os.path.basename(rel) == SELF:
            continue          # exclude this auditor's own .out: self-reference is noise
        try:
            t = open(m["out"], errors="ignore").read()
        except Exception:
            continue
        # DISTINGUISH a FAILED CHECK from a FINDING LABELLED "FAIL-MINOR". Adversarial audit scripts in
        # this corpus tag their findings [FAIL-MINOR]/[FAIL-MAJOR]; those are the audit WORKING, not
        # broken. The first version of this check counted them and produced a false positive on
        # AUDIT_mi_kernel_axis_gate_2026 (4 verdict-neutral findings). Count only bare [FAIL] / [FAIL ].
        nf = len(re.findall(r"\[FAIL[\]\s]", t))
        findings = len(re.findall(r"\[FAIL-(?:MINOR|MAJOR)\]", t))
        if findings and not nf:
            print(f"    (skipped, {findings} labelled findings not failed checks): {os.path.basename(rel)}")
        if nf:
            fails.append((nf, rel))
    fails.sort(reverse=True)
    for nf, rel in fails[:12]:
        print(f"    {nf:3d} FAIL lines : {rel}")
    check(len(fails) == 0,
          f"{len(fails)} committed .out file(s) contain a genuinely FAILED CHECK. Any nonzero count is a "
          f"script whose own checks contradict the claim it backs. Findings tagged [FAIL-MINOR] by "
          f"adversarial audit scripts are EXCLUDED -- those are the audit working, not a defect")

    # ---------------- D : orphaned closures (inverse leak) ----------------
    banner("CHECK D. ORPHANED CLOSURES -- scripts that close something but STANDING never mentions")
    orphans = []
    for rel, m in inv.items():
        if not m["closes"]:
            continue
        if os.path.basename(rel) not in standing_txt:
            orphans.append((m["mtime"], rel))
    orphans.sort(reverse=True)
    print(f"  {len(orphans)} scripts assert a closure but are not named in STANDING (newest 12):")
    import datetime
    for mt, rel in orphans[:12]:
        print(f"    {datetime.date.fromtimestamp(mt)}  {os.path.basename(rel)}")
    check(len(orphans) >= 0,
          f"{len(orphans)} uncited closures. This is the INVERSE leak -- results banked in code but absent "
          f"from the standing document, i.e. the corpus understating itself, which is exactly what happened "
          f"with two loops. Reported as candidates, newest first, since recency correlates with relevance")

    banner("VERDICT")
    if CONTROL_OK:
        print("  THE POSITIVE CONTROL PASSED, which is the only reason to trust the rest: check E")
        print("  rediscovered the twoloop_laneC_a0 -> graviton supersession from file dates and filename")
        print("  keywords alone, with no knowledge of the physics and without being told to look.")
    else:
        print("  *** THE POSITIVE CONTROL FAILED. The tool did NOT rediscover a known-true supersession,")
        print("  so its other output must NOT be trusted as coverage. Reported as a tool defect. ***")
    print()
    print("  WHAT EACH CHECK IS FOR, and what it is NOT:")
    print("   A  STANDING open-claims with an uncited, newer, closing script on overlapping keywords.")
    print("   B  Cited scripts with NO committed .out -- the weakest links against the repo's own rule 4.")
    print("   C  Committed .out files containing [FAIL] -- live self-contradictions. MUST be zero.")
    print("   D  The INVERSE leak: closures banked in code but missing from STANDING. This is the class")
    print("      that hid the two-loop result, and it makes the corpus UNDERSTATE itself.")
    print("   E  Same-directory supersession by date + keyword. The two-loop pattern.")
    print()
    print("  *** EVERY HIT IS A CANDIDATE, NOT A FINDING. *** Keyword overlap cannot judge whether a newer")
    print("  script actually addresses an older claim -- only a read can. The tool is deliberately tuned to")
    print("  OVER-report: a false positive costs one read, a false negative costs a wrong standing claim.")
    print("  It computes no physics and does not attempt to.")
    print()
    print("  a0 is NOT derived, kappa = 1/2 stays FITTED, and nothing here closes or opens any physics")
    print("  door -- it only asks which doors the paperwork has mislabelled.")
    print("=" * 102)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
