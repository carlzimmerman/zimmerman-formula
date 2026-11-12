#!/usr/bin/env python3
"""EW1 answers Q1-Q3 from matrix.tsv (criteria FROZEN_CRITERIA.md section 2).
    python3 ew1_matrix.py           -> ew1_matrix.json / .out
    python3 ew1_matrix.py --mutate  -> ew1_matrix_MUTATE.json / .out (planted all-pass row; Bullet column emptied)
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = "--mutate" in sys.argv; OUT = []
def P(s=""): print(s); OUT.append(s)
lines = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "matrix.tsv"))]
hdr, rows = lines[0], lines[1:]
TOK = {"PASS", "FAIL", "SPLIT", "MIXED", "NO_VERDICT", "OPEN", "UNGRADED", "N/A", "PASS_SCOPED", "TENSION", "DERIVED", "BY_HAND", "ABSENT"}
def tok(c): return c.split(":")[0].strip()
assert len(hdr) == 18 and len(rows) == 23, (len(hdr), len(rows))
for r in rows:
    assert len(r) == 18, r[0]
    for c in r[1:]: assert c.strip() and tok(c) in TOK, (r[0], c)
COLS = hdr[1:]; STATUS = "C05 wide binaries (status)"; TIE = "C17 a0 tie"
M = {r[0]: dict(zip(COLS, (tok(c) for c in r[1:]))) for r in rows}
if MUT:
    M["PLANTED all-pass"] = {c: ("DERIVED" if c == TIE else "PASS") for c in COLS}
    for k in M:
        if M[k]["C09 Bullet"] == "PASS" and k != "PLANTED all-pass": M[k]["C09 Bullet"] = "FAIL"
LCDM = [k for k in M if k.startswith("R23")]
GRADED = [c for c in COLS if c != STATUS]
def passes(k, c, relax=False):
    t = M[k][c]
    if c == TIE: return t == "DERIVED" or (relax and t == "BY_HAND")
    return t == "PASS"
RES = dict(tag="ew1_matrix_MUTATE" if MUT else "ew1_matrix", note="kappa = 1/2 FITTED; not theory closed")
q1 = {lab: [k for k in M if k not in LCDM and all(passes(k, c, relax) for c in GRADED)] for lab, relax in (("strict", False), ("tie_by_hand_ok", True))}
q1["LCDM_comparison_strict"] = [k for k in LCDM if all(passes(k, c) for c in GRADED)]
q1["LCDM_failing_cols"] = {k: [c for c in GRADED if not passes(k, c)] for k in LCDM}
RES["Q1"] = q1
P(f"Q1 strict (C17 must be DERIVED): {q1['strict'] or 'NO ROW'}")
P(f"Q1 with C17 BY_HAND allowed: {q1['tie_by_hand_ok'] or 'NO ROW'}")
P(f"   LCDM (comparison only) non-pass columns: {q1['LCDM_failing_cols']}")
nonpass = {k: [c for c in GRADED if not passes(k, c, True)] for k in M if k not in LCDM}
RES["nonpass_per_row"] = nonpass
for k in sorted(nonpass, key=lambda k: len(nonpass[k])):
    P(f"   {k}: {len(nonpass[k])} non-pass columns (C17 by hand allowed)")
def cover(pool, relax):
    cov = {c for c in GRADED if any(passes(k, c, relax) for k in pool)}; unc = [c for c in GRADED if c not in cov]
    for n in range(1, len(pool) + 1):
        sols = [s for s in itertools.combinations(pool, n) if all(any(passes(k, c, relax) for k in s) for c in cov)]
        if sols: return dict(size=n, sets=[list(s) for s in sols], uncovered=unc)
    return dict(size=0, sets=[], uncovered=unc)
FW = [k for k in M if k not in LCDM]
RES["Q2"] = {"framework_strict": cover(FW, False), "framework_tie_by_hand": cover(FW, True), "with_LCDM_strict": cover(list(M), False)}
for lab, v in RES["Q2"].items():
    P(f"Q2 {lab}: minimal cover size {v['size']}, {len(v['sets'])} minimal sets; uncovered: {v['uncovered']}")
    for s in v["sets"][:40]: P("     " + " + ".join(x.split()[0] for x in s))
# Q3: open cells that could change an answer
opencells = {"UNGRADED", "NO_VERDICT", "OPEN", "PASS_SCOPED", "SPLIT", "MIXED"}
q3 = []
for k in FW:
    np_ = nonpass[k]
    if np_ and all(M[k][c] in opencells for c in np_): q3.append(dict(row=k, kind="Q1 flip: every non-pass cell is open", cells={c: M[k][c] for c in np_}))
base = RES["Q2"]["framework_strict"]
for c in base["uncovered"]:
    cand = [k for k in FW if M[k][c] in opencells]
    q3.append(dict(column=c, kind="uncovered column: open cells that could cover it", rows={k: M[k][c] for k in cand}))
RES["Q3"] = q3
for q in q3: P(f"Q3 {q}")
if MUT:
    ok1 = q1["strict"] == ["PLANTED all-pass"]; ok2 = RES["Q2"]["framework_strict"]["size"] == 1
    ok3 = "C09 Bullet" not in {c for c in GRADED if any(passes(k, c) for k in M if k not in ("PLANTED all-pass",) and k not in LCDM)}
    RES["MUTATE"] = dict(planted_Q1=ok1, planted_Q2_size1=ok2, bullet_uncovered_without_plant=ok3, bites=bool(ok1 and ok2 and ok3))
    P(f"MUTATE: planted row Q1 YES {ok1}, Q2 size 1 {ok2}, Bullet uncovered without it {ok3} -> {'BITES' if RES['MUTATE']['bites'] else 'NO BITE'}")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, RES["tag"] + ".json"), "w"), indent=1)
open(os.path.join(HERE, RES["tag"] + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (not MUT or RES["MUTATE"]["bites"]) else 1)
