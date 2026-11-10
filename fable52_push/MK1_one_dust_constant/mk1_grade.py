#!/usr/bin/env python3
"""MK1 label (criteria b1fbded1e2 section 3): intersect the rows' mu_K sets per footing; NO VERDICT if any known answer failed.
Reads mk1_rows.json, mk1_sparc.json, mk1_kids.json (and their MUTATE files for the 'moves' check). Writes mk1_grade.json / .out.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
J = {k: json.load(open(os.path.join(HERE, f"mk1_{k}.json"))) for k in ("rows", "sparc", "kids")}
M = {k: json.load(open(os.path.join(HERE, f"mk1_{k}_MUTATE.json"))) for k in ("rows", "sparc", "kids")}
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
INF = float("inf")
ka = {}
for k in J: ka.update({f"{k}: {kk}": v["ok"] for kk, v in J[k]["KA"].items()})
ka_ok = all(ka.values())
P(f"MK1 grade. Known answers: {sum(ka.values())} of {len(ka)} PASS" + ("" if ka_ok else f" -> FAILED: {[k for k, v in ka.items() if not v]}"))

def rows_for(f, capped=True):
    R = {}
    r1 = J["rows"]["rows"]["1 CMB and background"][f]; R["1 CMB and background (KD1 B1a)"] = (r1["interval"][0], INF, "KD1 B1a; QX17 FRW", r1["quality"])
    r2 = J["rows"]["rows"]["2 clustering scale"][f]; R["2 clustering scale (KD1 G9a Jeans line)"] = (r2["interval"][0], INF, "KD1 G9a on QX3 iter2", r2["quality"])
    r3 = J["rows"]["rows"]["3 X-COP"][f"exact zero 3 R200 {f}"]
    R["3 X-COP (G-X)"] = ((r3["interval"][0], r3["interval"][1]) if r3["interval"] else (None, None)) + ("QX2 iter 5 + QX6 back-reaction, action-exact", f"grid 1e-3..1e4; min rms {r3['min_rms']:.3f} at {r3['mu_min_rms']:.3g}")
    r4 = J["rows"]["rows"]["4 groups"][f"exact {f}"]
    R["4 groups (Lovisari)"] = ((r4["interval"][0], r4["interval"][1]) if r4["interval"] else (None, None)) + ("QX5 group gate, action-exact", "power-law M_HSE potential")
    key5 = f"capped {f}" if capped else f"uncapped {f}"; r5 = J["sparc"]["rows"][key5]
    ub5 = r5["upper_bound"] if r5["upper_bound"] is not None else 0.0
    R["5 SPARC (QX8 line)"] = (0.0, ub5, "QX8", f"first fail {r5['first_fail']}; {'capped' if capped else 'uncapped, coarse grid'}")
    key6 = f"primary {f}" if capped else f"uncapped {f}"; r6 = J["kids"]["rows"][key6]
    pas = [float(k) for k, v in r6["points"].items() if v["status"] == "PASS"]
    note6 = f"first fail {r6['first_fail']}; passing grid points {pas}; {'capped, neighbours' if capped else 'uncapped, own halo, no neighbours, coarse grid'}"
    if r6["points"]["0"]["status"] != "PASS" and not pas:
        R["6 KiDS host-free (ONE1 gate, 1.6 R_h)"] = (None, None, "ONE1", "no grid value passes (mu_K = 0 fails); " + note6)
    else:
        R["6 KiDS host-free (ONE1 gate, 1.6 R_h)"] = (0.0, r6["upper_bound"] if r6["upper_bound"] is not None else 0.0, "ONE1", note6)
    r7 = J["rows"]["rows"]["7 Solar System"][f]; R["7 Solar System (Saturn line)"] = (0.0, r7["interval"][1], "EW2 iter4", "closed form")
    return R

def label(R):
    empty = [k for k, v in R.items() if v[0] is None]
    lo = max((v[0], k) for k, v in R.items() if v[0] is not None); hi = min((v[1], k) for k, v in R.items() if v[0] is not None)
    if empty:
        return "NO VALUE", lo, hi, empty
    if lo[0] <= hi[0]:
        return "ONE VALUE EXISTS", lo, hi, []
    return "NO VALUE", lo, hi, []

RES = dict(lane="MK1", criteria="b1fbded1e2 (A1 916f4e0e22)", KA_all_pass=ka_ok, footings={}, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
for f in ("canonical", "alt"):
    R = rows_for(f, True); lab, lo, hi, empty = label(R)
    if not ka_ok: lab = "NO VERDICT"
    Ru = rows_for(f, False); labu, lou, hiu, emptyu = label(Ru)
    P(f"\n=== {f}: {lab}")
    for k, (a, b, src, q) in R.items():
        P(f"  {k}: " + ("EMPTY (no mu_K passes)" if a is None else f"[{a:.4g}, {'inf' if b == INF else f'{b:.4g}'}]") + f"   <- {src}; {q}")
    fac = lo[0] / hi[0] if hi[0] > 0 else INF
    P(f"  largest lower end {lo[0]:.4g} ({lo[1]}); smallest upper end {hi[0]:.4g} ({hi[1]}); factor {fac:.3g}" + (f"; empty rows: {empty}" if empty else ""))
    # factor between the CMB rows and each galaxy / cluster upper end
    pairs = {}
    for kl in ("1 CMB and background (KD1 B1a)", "2 clustering scale (KD1 G9a Jeans line)"):
        for ku in ("5 SPARC (QX8 line)", "6 KiDS host-free (ONE1 gate, 1.6 R_h)", "7 Solar System (Saturn line)"):
            pairs[f"{kl} vs {ku}"] = R[kl][0] / R[ku][1] if R[ku][1] > 0 else INF
    for k, v in pairs.items(): P(f"    {k}: factor {v:.3g}")
    P(f"  uncapped (rows 5, 6 on their uncapped readings): {labu}; lower {lou[0]:.4g} ({lou[1]}), upper {hiu[0]:.4g} ({hiu[1]}) -> "
      + ("the label does NOT turn on the cap" if labu == lab or (lab == 'NO VERDICT') else "the label TURNS ON THE CAP"))
    RES["footings"][f] = dict(label=lab, rows={k: dict(lo=v[0], hi=(None if v[1] == INF else v[1]), source=v[2], note=v[3]) for k, v in R.items()},
                              L=lo, U=hi, factor=fac, empty_rows=empty, pair_factors=pairs,
                              uncapped=dict(label=labu, L=lou, U=hiu, rows={k: dict(lo=v[0], hi=(None if v[1] == INF else v[1])) for k, v in Ru.items()}),
                              turns_on_cap=bool(labu != lab and lab != "NO VERDICT"))

# MUTATE moves (criteria section 5)
P("\nMUTATE: does each arm move an interval?")
mv = {}
for f in ("canonical", "alt"):
    c6 = J["kids"]["rows"][f"primary {f}"]["upper_bound"]; u6 = J["kids"]["rows"][f"uncapped {f}"]["upper_bound"]
    c5 = J["sparc"]["rows"][f"capped {f}"]["upper_bound"]; u5 = M["sparc"]["arms"][f"M-NOCAP {f}"]["upper_bound"]
    mv[f"M-NOCAP row 6 {f}"] = (c6, u6); mv[f"M-NOCAP row 5 {f}"] = (c5, u5)
    mv[f"M-2X row 6 {f} (own halo only, both)"] = (str(M["kids"]["arms"][f"M-2X {f}"]["primary_own_passing"]), str(M["kids"]["arms"][f"M-2X {f}"]["passing"])); mv[f"M-2X row 5 {f}"] = (c5, M["sparc"]["arms"][f"M-2X {f}"]["upper_bound"])
    mv[f"M-SIGN row 6 {f}"] = (c6, M["kids"]["arms"][f"M-SIGN {f}"]["upper_bound"]); mv[f"M-SIGN row 5 {f}"] = (c5, M["sparc"]["arms"][f"M-SIGN {f}"]["upper_bound"])
    i3p = J["rows"]["rows"]["3 X-COP"][f"exact zero 3 R200 {f}"]["interval"]; i3m = M["rows"]["arms"][f"M-SIGN row 3 {f}"]["interval"]
    mv[f"M-SIGN row 3 {f} (interval, frozen definition)"] = (i3p, i3m)
    mv[f"M-SIGN row 3 {f} (closest miss, reported)"] = (f"min rms {J['rows']['rows']['3 X-COP'][f'exact zero 3 R200 {f}']['min_rms']:.3f}", f"min rms {M['rows']['arms'][f'M-SIGN row 3 {f}']['min_rms']:.3f}")
    mv[f"M-SIGN row 4 {f}"] = (J["rows"]["rows"]["4 groups"][f"exact {f}"]["interval"], M["rows"]["arms"][f"M-SIGN row 4 {f}"]["interval"])
for k, (a, b) in mv.items():
    moved = (a != b)
    if "frozen definition" in k: moved = not (a is None and b is None) and a != b
    P(f"  {k}: primary {a} -> mutated {b}: {'MOVES' if moved else 'DOES NOT MOVE'}")
RES["mutate_moves"] = {k: dict(primary=a, mutated=b, moves=bool(a != b)) for k, (a, b) in mv.items()}
json.dump(RES, open(os.path.join(HERE, "mk1_grade.json"), "w"), indent=1, default=lambda o: None if o == INF else o)
open(os.path.join(HERE, "mk1_grade.out"), "w").write("\n".join(OUT + ["kappa = 1/2 FITTED; not theory closed. Adopts nothing."]) + "\n")
