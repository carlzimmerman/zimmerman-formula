#!/usr/bin/env python3
"""SRH1 grader (FROZEN_CRITERIA.md 5ed8a37ec6, section 3): window W(footing) = grid f passing G1-G4; labels ONE HISTORY PASSES /
WINDOW EMPTY / NO VERDICT; qualifiers (G4 does not test the history; amplitude). Reads srh1_forest_<foot>.json, srh1_rc.json,
srh1_lens.json, srh1_hm.json.   python3 srh1_grade.py -> srh1_grade.json / .out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); J = lambda n: json.load(open(os.path.join(HERE, n)))
RC, LE, HM = J("srh1_rc.json"), J("srh1_lens.json"), J("srh1_hm.json"); FO = {f: J(f"srh1_forest_{f}.json") for f in ("canonical", "alt")}
GRID = HM["f_grid"]; K = lambda f: f"{f:.2f}"; OUT = []; RES = dict(lane="SRH1", criteria="5ed8a37ec6", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", foot={})
def P(s=""): print(s); OUT.append(s)
P("SRH1 grade. kappa = 1/2 FITTED; not theory closed. Footings never pooled.")
ka_lens = all(v["pass_"] for v in LE["KA"].values())
for ft in ("canonical", "alt"):
    fo, rc = FO[ft], RC["foot"][ft]
    g1 = {K(f): fo["cases"][f"f{K(f)}"]["dchi2"] <= 4 for f in GRID}
    g2 = {K(f): rc["G2_pass"][K(f)] for f in GRID}; g3 = {K(f): rc["G3_pass"][K(f)] for f in GRID}
    st4 = {K(f): LE["cfg"][f"{ft}|f{K(f)}"]["gate"]["status"] for f in GRID}; g4 = {k: v == "PASS" for k, v in st4.items()}
    W = [f for f in GRID if g1[K(f)] and g2[K(f)] and g3[K(f)] and g4[K(f)]]
    ka = fo["KA_ok"] and rc["KA_G2"]["pass_"] and rc["KA_G3"]["pass_"] and RC["KA_G3b"][ft]["pass_"] and ka_lens
    mu = fo["MUTATE"]["MU1"]["bites"] and fo["MUTATE"]["MU3a_hm"]["bites"] and rc["MU2_bites"] and rc["G2"]["MU3b_bites"] and LE["MU4"]["bites"]
    notev = [K(f) for f in GRID if st4[K(f)] == "NOT EVALUABLE"]
    # edges (reported): G1 upper by log-linear interpolation of Delta chi^2 = 4; G2 lower exact
    d = [(f, fo["cases"][f"f{K(f)}"]["dchi2"]) for f in GRID]; up = None
    for (fa, da), (fb, db) in zip(d[:-1], d[1:]):
        if da <= 4 < db: up = fa + (fb - fa) * (math.log(4) - math.log(max(da, 1e-12))) / (math.log(db) - math.log(max(da, 1e-12))); break
    lo = rc["G2"]["f_min_2p2Re"]
    if not ka or not mu: lab = "NO VERDICT (known answer or MUTATE)"
    elif notev: lab = f"NO VERDICT (G4 not evaluable at f {notev})"
    elif W:
        gaps = [f for f in GRID if min(W) <= f <= max(W) and f not in W]
        lab = f"ONE HISTORY PASSES, f {min(W):.2f} to {max(W):.2f} on the grid" + (f" with a gap at {gaps}" if gaps else "")
    else:
        sets = {"G1": g1, "G2": g2, "G3": g3, "G4": g4}; dead = [n for n, s in sets.items() if not any(s.values())]
        if dead: lab = "WINDOW EMPTY: " + ", ".join(dead) + " fails at every grid f"
        else:
            pairs = [(a, b) for a in sets for b in sets if a < b and not any(sets[a][k] and sets[b][k] for k in sets[a])]
            lab = "WINDOW EMPTY: " + "; ".join(f"{a} and {b} exclude each other" for a, b in pairs)
    allsame = len(set(st4.values()) | {LE["cfg"][f"{ft}|f0"]["gate"]["status"], LE["cfg"][f"{ft}|finf"]["gate"]["status"]}) == 1
    q = []
    if allsame: q.append(f"G4 DOES NOT TEST THE HISTORY (G4 {st4[K(GRID[0])]} at every grid f and at f 0 and f inf)")
    if W and all(not rc["family"][K(f)]["line"] for f in W): q.append("AMPLITUDE: the family-layout SPARC reading fails at every f in W")
    RES["foot"][ft] = dict(label=lab, qualifiers=q, window=W, G1=g1, G2=g2, G3=g3, G4=st4, G1_upper_interp=up, G2_lower_exact=lo, G3a_lower_exact=rc["G3a"]["f_min"],
                           KA_ok=bool(ka), MUTATE_ok=bool(mu))
    P(f"\n[{ft}] LABEL: {lab}" + ("".join(f"; {x}" for x in q)))
    P(f"[{ft}] edges (reported): G1 upper (Delta chi^2 = 4, interpolated) {up}; G2 lower {lo:.4f} (4 R_e: {rc['G2']['f_min_4Re']:.4f}); G3(a) coverage {rc['G3a']['f_min']:.4f} (G3 passes by its line (b) below it)")
    P(f"[{ft}] f    | G1 dchi2      | G2  | G3  | G4 (z all/late/early, chi2)              | family SPARC rms | z=0 R_tot k1/k3")
    for f in GRID:
        c = LE["cfg"][f"{ft}|f{K(f)}"]; l = c["gate"]["lines"]; zt = HM["z0_table"][f"{ft}|f{K(f)}"]["R_tot_at_k1_3"]
        g4s = (" / ".join(f"{l[f'G-K1 {s}']['z']:+.2f}" for s in ("all", "late", "early")) + f", {l['G-K2 all profile']['chi2']:.2f}") if l else "-"
        P(f"[{ft}] {f:.2f} | {fo['cases'][f'f{K(f)}']['dchi2']:9.2f} {'P' if g1[K(f)] else 'F'}   | {'P' if g2[K(f)] else 'F'}   | {'P' if g3[K(f)] else 'F'}   | {st4[K(f)]:4s} {g4s:34s} | {rc['family'][K(f)]['all']['rms']:.4f} {'P' if rc['family'][K(f)]['line'] else 'F'}  | {zt[0]:.4f} / {zt[1]:.4f}")
    P(f"[{ft}] KA all pass {ka}; MUTATE all bite {mu}")
    # tilt (reported)
    tl = []
    for beta in (-1.0, -0.5, 0.5):
        for f0 in (0.5, 0.75, 1.0):
            dc = fo["cases"][f"tilt_b{beta:+.1f}_f{f0:.2f}"]["dchi2"]; t = rc["tilt"][f"{beta:+.1f}"]
            ok = dc <= 4 and f0 >= t["f0_min_G2"] and (f0 >= t["f0_min_G3a"] or True)
            tl.append(dict(beta=beta, f0=f0, dchi2=dc, G1=dc <= 4, G2=f0 >= t["f0_min_G2"], G3a=f0 >= t["f0_min_G3a"]))
    RES["foot"][ft]["tilt"] = tl
    P(f"[{ft}] tilt (reported; G4 for the tilt is in srh1_tilt.out): " + "; ".join(f"beta {x['beta']:+.1f} f0 {x['f0']:.2f}: dchi2 {x['dchi2']:.2f} G1 {'P' if x['G1'] else 'F'} G2 {'P' if x['G2'] else 'F'} G3a {'P' if x['G3a'] else 'F'}" for x in tl))
json.dump(RES, open(os.path.join(HERE, "srh1_grade.json"), "w"), indent=1)
open(os.path.join(HERE, "srh1_grade.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
