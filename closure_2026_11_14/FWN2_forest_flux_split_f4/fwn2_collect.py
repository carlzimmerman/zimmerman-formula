#!/usr/bin/env python3
"""FWN2 collector (FROZEN_CRITERIA.md 26cb002843, section 4): reads this lane's two grade files and the committed grade
files of FRZ6, FWN1 (build A) and FRZ6R, FWN1R (build B), and prints, per footing, the table of f against both builds, the
frozen read-across word at f = 4, and each build's ceiling interpolation. It computes no statistic of its own: every D, SE
and label is copied from a grade file. Written before any graded number of this lane existed.
Usage: python3 -I -B fwn2_collect.py -> fwn2_collect.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
C13 = os.path.join(REPO, "closure_2026_11_13"); C14 = os.path.join(REPO, "closure_2026_11_14")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def J(*p): return json.load(open(os.path.join(*p)))
def word(lab):
    return "HOLDS" if lab.startswith("FOREST ROW HOLDS") else "FAILS" if lab.startswith("FOREST ROW FAILS") else "NO VERDICT"
B_new = J(HERE, "fwn2b_grade.json"); B_r6 = J(C13, "FRZ6R_blind_forest_flux_candidate", "frz6r_grade.json"); B_r1 = J(C14, "FWN1R_blind_split_f_ceiling", "fwn1r_grade.json")
for ft in ("canonical", "alt"):
    A_new = J(HERE, f"fwn2a_grade_{ft}.json"); A_6 = J(C13, "FRZ6_forest_flux_candidate_graded", f"frz6_grade_{ft}.json")
    A_1 = J(C13, "FWN1_forest_flux_split_f_ceiling", f"fwn1_grade_{ft}.json")
    rowsA = {}
    for g, lane, keys in ((A_6, "FRZ6", (("S2.00", 2.0), ("S3.00", 3.0))), (A_new, "FWN2", (("S4.00", 4.0),)), (A_1, "FWN1", (("S5.00", 5.0), ("S10.00", 10.0), ("Sinf", math.inf)))):
        for k, f in keys:
            if g["rows"].get(k) is None: rowsA[f] = (lane, None, None, g["labels"][k]); continue
            rowsA[f] = (lane, g["rows"][k]["flux"], g["known_answers"]["e"][k]["SE"], g["labels"][k])
    rowsB = {}
    for g, lane, keys in ((B_r6, "FRZ6R", (("J2", 2.0), ("J3", 3.0))), (B_new, "FWN2", (("J3.5", 3.5), ("J4", 4.0), ("J4.5", 4.5))), (B_r1, "FWN1R", (("J5", 5.0), ("J10", 10.0), ("Jinf", math.inf)))):
        L = g["footings"][ft]["labels"]
        for k, f in keys: rowsB[f] = (lane, L[k]["D"], L[k]["SE"], L[k]["label"])
    P(f"[{ft}] f | build A: lane, D (SE), D + 2 SE, D - 2 SE, label | build B: lane, D (SE), D + 2 SE, D - 2 SE, label")
    def cell(r):
        if r is None: return "not run"
        lane, D, SE, lab = r
        if D is None: return f"{lane}: {lab}"
        return f"{lane}: {D:.4g} ({SE:.3g}), {D + 2 * SE:.4g}, {D - 2 * SE:.4g}, {lab}"
    for f in sorted(set(rowsA) | set(rowsB)):
        P(f"[{ft}] f {f:g} | {cell(rowsA.get(f))} | {cell(rowsB.get(f))}")
    wa, wb = word(rowsA[4.0][3]), word(rowsB[4.0][3])
    if wa == "HOLDS" and wb == "HOLDS": ra = "f = 4 HOLDS IN BOTH BUILDS"
    elif wa == "FAILS" and wb == "FAILS": ra = "f = 4 FAILS IN BOTH BUILDS"
    elif {wa, wb} == {"HOLDS", "FAILS"}: ra = "THE BUILDS DISAGREE AT f = 4"
    else: ra = "f = 4 NOT RESOLVED"
    frag = [n for n, r in (("A", rowsA[4.0]), ("B", rowsB[4.0])) if "FRAGILE" in r[3]]
    P(f"[{ft}] READ ACROSS (section 4; reported, never a label on the theory): {ra}" + (f" (FRAGILE in build {' and '.join(frag)})" if frag and ra.startswith("f = 4 HOLDS") else "")
      + f"; build A S4: {rowsA[4.0][3]}; build B J4: {rowsB[4.0][3]}")
    both = sorted(set(rowsA) & set(rowsB))
    hold = [f for f in both if word(rowsA[f][3]) == "HOLDS" and word(rowsB[f][3]) == "HOLDS"]
    fail = [f for f in both if word(rowsA[f][3]) == "FAILS" and word(rowsB[f][3]) == "FAILS"]
    P(f"[{ft}] f run in both builds: {[f'{f:g}' for f in both]}; largest f that HOLDS as a label in both: {max(hold) if hold else 'none'}; smallest f that FAILS as a label in both: {min(fail) if fail else 'none'}")
    P(f"[{ft}] words by f, build A / build B: " + "; ".join(f"{f:g}: {word(rowsA[f][3]) if f in rowsA else 'not run'} / {word(rowsB[f][3]) if f in rowsB else 'not run'}" for f in sorted(set(rowsA) | set(rowsB))))
    ce = A_new["ceiling"]; cb = B_new["footings"][ft]["ceiling"]
    P(f"[{ft}] ceiling, build A (log-linear between adjacent run points): D + 2 SE = 4 at {ce['hi']['text']}; D = 4 at {ce['D']['text']}; D - 2 SE = 4 at {ce['lo']['text']}")
    fmt = lambda v: f"{v:.2f}" if isinstance(v, float) else str(v)
    P(f"[{ft}] ceiling, build B (log-linear between adjacent run points): D + 2 SE = 4 at f {fmt(cb['D+2SE'])}; D = 4 at f {fmt(cb['D'])}; D - 2 SE = 4 at f {fmt(cb['D-2SE'])}")
    rep = B_new["footings"][ft]["reported_boundary_removed_f4"]
    P(f"[{ft}] reported, not a gate, build B: boundary removed at f = 4, D(U4) {rep['D_U4']:.4g} against D(J4) {rep['D_J4']:.4g}, ratio {rep['ratio']:.3g}; FWN1R's rule {'would bite' if rep['rule_would_bite'] else 'would not bite'}")
open(os.path.join(HERE, "fwn2_collect.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
