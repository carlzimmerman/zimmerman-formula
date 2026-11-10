#!/usr/bin/env python3
"""MK2 label (criteria 3b4f515ff8 section 5; A1-A3): intersect the graded rows' c_s sets per footing. Reads mk2_rows.json, mk2_sparc.json,
mk2_kids.json, mk2_cmb.json (if present) and the MUTATE files. Writes mk2_grade.json / .out.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
def load(n):
    p = os.path.join(HERE, n); return json.load(open(p)) if os.path.exists(p) else None
R, S, K, C = load("mk2_rows.json"), load("mk2_sparc.json"), load("mk2_kids.json"), load("mk2_cmb.json")
RM, SM = load("mk2_rows_MUTATE.json"), load("mk2_sparc_MUTATE.json")
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
CSG = sorted(R["cs_grid"])
ka = {}
for name, J in (("rows", R), ("sparc", S), ("kids", K)):
    if J: ka.update({f"{name}: {k}": v["ok"] for k, v in J["KA"].items()})
frozen_fail = [k for k, v in R["KA"].items() if "groups no dust" in k and not v.get("frozen_reading_ok", True)]
cmb_ka = {}
if C:
    for f, r in C["footings"].items(): cmb_ka[f] = bool(r["KA_C1"]["ok"] and r["KA_C2"]["ok"])
ka_ok = all(ka.values())
P(f"MK2 grade. Known answers (A3 reading): {sum(ka.values())} of {len(ka)} PASS. Frozen KA4 groups reading fails on: {frozen_fail or 'none'}. CMB machinery KAs: {cmb_ka or 'not run'}")
RES = dict(lane="MK2", footings={}, KA_all_pass=ka_ok, frozen_reading_KA_fail=frozen_fail, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
for f in ("canonical", "alt"):
    rows = {}
    a1 = R["rows"]["a1"]["cs_max_kms"]; rows["a1 CMB background (KD1 B1a)"] = (min(CSG), a1)
    if C and cmb_ka.get(f):
        cr = C["footings"][f]; rows["a2 primary CMB likelihood (F1A)"] = (min(CSG), cr["cs_max"]) if cr.get("cs_max") else (None, None)
    rc = R["rows"][f"c {f}"]["interval"]; rows["c X-COP"] = tuple(rc) if rc else (None, None)
    rd = R["rows"][f"d {f}"]["interval"]; rows["d groups"] = tuple(rd) if rd else (None, None)
    if S:
        se = S["rows"][f"e {f}"]["lower_bound"]; rows["e SPARC"] = (se, max(CSG)) if se else (None, None)
    if K:
        sk = K["rows"][f"f {f}"]["lower_bound"]; rows["f KiDS"] = (sk, max(CSG)) if sk else (None, None)
    gg = R["rows"][f"g {f}"]["cs_min"]; rows["g Solar System"] = (gg, max(CSG)) if gg else (None, None)
    hh = R["rows"]["h"][f]["interval"]; rows["h SCS1 stability"] = tuple(hh) if hh else (None, None)
    empty = [k for k, v in rows.items() if v[0] is None]
    lo = max((v[0], k) for k, v in rows.items() if v[0] is not None); hi = min((v[1], k) for k, v in rows.items() if v[0] is not None)
    if not ka_ok: lab = "NO VERDICT"
    elif empty or lo[0] > hi[0]: lab = "NO VALUE"
    else: lab = "A VALUE EXISTS ON THE GRADED ROWS"
    P(f"\n=== {f}: {lab}" + (f"  (as frozen: NO VERDICT, KA4 groups leg {frozen_fail})" if any(f in x for x in frozen_fail) else ""))
    for k, (a, b) in rows.items():
        P(f"  {k}: " + ("EMPTY" if a is None else f"[{a:.4g}, {b:.4g}] km/s"))
    P(f"  largest lower end {lo[0]:.4g} ({lo[1]}); smallest upper end {hi[0]:.4g} ({hi[1]})" + (f"; empty rows {empty}" if empty else ""))
    closest = R["rows"][f"c {f}"]["closest"]
    if closest: P(f"  X-COP closest miss: rms {closest['rms']:.3f} (mean {closest['mean']:+.3f}) at c_s {closest['cs']:.0f} km/s; static states fold below that")
    RES["footings"][f] = dict(label=lab, rows={k: dict(lo=a, hi=b) for k, (a, b) in rows.items()}, empty=empty, L=lo, U=hi,
                              frozen_label=("NO VERDICT" if any(f in x for x in frozen_fail) else lab))
ST = load("mk2_static.json")
if ST:
    P("\nRow i (A4, reported beside the frozen label): " + "; ".join(f"{f}: {ST['footings'][f]['label']}" for f in ("canonical", "alt")))
    RES["row_i"] = {f: ST["footings"][f]["label"] for f in ("canonical", "alt")}
P("\nNot carried (named, not graded): the three lines of row b (CMB-lensing Jeans line, growth, forest) and the forest / growth / CMB-lensing rows.")
P("\nMUTATE: does each arm move an interval? (frozen definition: an endpoint moves by a grid step, or a row turns empty / non-empty)")
mv = {}
if RM:
    for k, v in RM["arms"].items():
        mv[f"{k} row c"] = (v["primary_c"], v["c_interval"], (v["primary_c_closest"] or {}).get("rms"), (v["c_closest"] or {}).get("rms"))
        mv[f"{k} row d"] = (v["primary_d"], v["d_interval"], None, None)
if SM:
    for k, v in SM["arms"].items(): mv[f"{k} row e"] = (v["primary"], v["lower_bound"], None, None)
for k, (a, b, ra, rb) in mv.items():
    moves = a != b
    P(f"  {k}: primary {a} -> mutated {b}: {'MOVES' if moves else 'DOES NOT MOVE'}" + ("" if ra is None else f" (closest miss rms {ra:.3f} -> {rb if rb is None else round(rb, 3)})"))
RES["mutate"] = {k: dict(primary=a, mutated=b, moves=bool(a != b), closest=(ra, rb)) for k, (a, b, ra, rb) in mv.items()}
json.dump(RES, open(os.path.join(HERE, "mk2_grade.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, "mk2_grade.out"), "w").write("\n".join(OUT + ["kappa = 1/2 FITTED; not theory closed. Adopts nothing."]) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
