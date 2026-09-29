#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG172D_verdict -- reads the JSON results of A1..A5 and prints the gate table per arm.  No physics; every cell cites its script.
Run:  ZF_REPO=<repo> python3 CFG172D_verdict.py     (after A1, A3, A2, A4, A5)
"""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG172D_common as C

R = C.Report("CFG172D_verdict")
P = R.P
P(__doc__.strip()); P(f"\n  repo: {C.rel(C.REPO)}")


def load(name):
    p = os.path.join(C.HERE, name + "_results.json")
    return json.load(open(p)) if os.path.exists(p) else None


A1 = load("CFG172D_A1_theta_equation"); A2 = load("CFG172D_A2_static_solve"); A3 = load("CFG172D_A3_obstruction")
A4 = load("CFG172D_A4_gates_G2_G5_G6_G7"); A5 = load("CFG172D_A5_stress_energy")
missing = [n for n, a in (("A1", A1), ("A2", A2), ("A3", A3), ("A4", A4), ("A5", A5)) if a is None]
if missing:
    P(f"  MISSING RESULTS: {missing}"); sys.exit(1)

ARMS = ["d1", "d1_alt", "d2_lin_even", "d2_sat_even", "d2_lin_mono", "d2_sat_mono"]
LAB = {"d1": "d1 (frozen: continuation branch)", "d1_alt": "d1-alt (sensitivity: upper S-curve branch)", "d2_lin_even": "d2 lin (frozen 'even' gate)",
       "d2_sat_even": "d2 sat (frozen 'even' gate)", "d2_lin_mono": "d2 lin, monotone gate (sensitivity)", "d2_sat_mono": "d2 sat, monotone gate (sensitivity)"}
T = {}
a1c = {c["name"].split()[0] + " " + c["name"].split()[1]: c["ok"] for c in A1["checks"]}
o3_ok = all(c["ok"] for c in A1["checks"] if c["name"].startswith(("O3a", "O3b", "O3c")))
S3 = A3["numbers"]; S2 = A2["numbers"]; S4 = A4["verdicts"]; S5 = A5["checks"]
for arm in ARMS:
    t = {}
    t["O3 (A1)"] = "PASS" if o3_ok else "FAIL"
    # O2 and G1 from A2
    sm = S2.get(f"summary_{arm}")
    if sm:
        rows = S2["G1_rows"][arm]; nr = len(rows)
        n3 = sum(r_["f3rM"] >= 0.99 for r_ in rows); nw = sum(r_["f_web_max"] <= 0.01 for r_ in rows); nfull = sum(r_["f_min_on_grid"] >= 0.99 for r_ in rows)
        t["O2 region-selective (A2)"] = ("PASS" if sm["o2_all"] else "FAIL") + f" (f(3 r_M) >= 0.99 in {n3}/{nr} solves; web off {nw}/{nr}; f >= 0.99 on the whole G1 grid {nfull}/{nr})"
        t["G1 strict, P2 / nu_mono (A2)"] = f"{'PASS' if sm['g1_strict_P2'] else 'FAIL'} / {'PASS' if sm['g1_strict_mono'] else 'FAIL'}"
        t["G1 edge (x <= x_ta), P2 / nu_mono (A2)"] = f"{'PASS' if sm['g1_edge_P2'] else 'FAIL'} / {'PASS' if sm['g1_edge_mono'] else 'FAIL'}"
    else:
        t["O2 region-selective (A2)"] = "NOT ADDRESSED"; t["G1 strict, P2 / nu_mono (A2)"] = "NOT ADDRESSED"; t["G1 edge (x <= x_ta), P2 / nu_mono (A2)"] = "NOT ADDRESSED"
    t["G1 mechanism"] = "FAIL as mechanism (kernel declared, gate shape declared: at best M1 'P-declared'; no pass to re-derive)"
    # O1 and obstruction verdict from A3
    if arm == "d1":
        t["O1 stable (A3)"] = "PASS (blind: c_eff = 0 on the continuation branch)"
        t["obstruction (A3)"] = "MOVED (blind): stable because the gate is never on"
    elif arm == "d1_alt":
        t["O1 stable (A3)"] = "NOT ADDRESSED (the alternative branch's c_eff was not computed; hypothetical fold ratio in A3)"
        t["obstruction (A3)"] = "NOT ADDRESSED beyond O2 (gate ON only at y >~ 0.3, A3/A2)"
    else:
        kind, var = arm.split("_")[1], arm.split("_")[2]
        sm3 = S3.get(f"summary_{kind}_{var}")
        v3 = S3.get("verdicts", {}).get(arm)
        if sm3:
            t["O1 stable (A3)"] = (f"FAIL: c_eff at each cell's zeta_min: median {sm3['ceff_at_zmin_median']:.3g} km/s (line 37); ratio zeta_min/zeta_max median {sm3['ratio_median']:.3g}"
                                  if sm3["ceff_at_zmin_median"] is not None and sm3["ceff_at_zmin_median"] > 37 else
                                  f"c_eff at zeta_min median {sm3['ceff_at_zmin_median']}")
            t["obstruction (A3)"] = v3["verdict"] if v3 else "n/a"
            t["added reach test (A3, not frozen)"] = f"gate ON to 30 r_M for some zeta in {sm3['n_reach']}/{sm3['n_cells']} cells; together with O1: {sm3['n_both_reach']}/{sm3['n_cells']}"
    # G2..G7
    G2 = S4.get(f"G2_{arm}") or (S4.get("G2_d1") if arm.startswith("d1") else None)
    t["G2 (A4)"] = (G2["status"] + " -- " + G2["why"]) if G2 else "NOT ADDRESSED"
    g3 = S2.get("G3", {}).get(arm)
    if arm.startswith("d1"):
        t["G3 (A2)"] = "PASS trivially (gate never on / no coupling)" if arm == "d1" else "NOT ADDRESSED"
    elif g3:
        t["G3 (A2)"] = (f"FAIL: reaction (gate) {g3['reaction_gate']:.3g}, (contact) {g3['reaction_contact']:.3g} x g_law (line 0.10); "
                        f"energy {g3['energy_over_orbital']['r_ta']:.3g} x orbital (line 1)")
    else:
        t["G3 (A2)"] = "NOT ADDRESSED"
    t["G4 constants (A5 ledger; criteria 1.5)"] = "FAIL strict (inherited V0 constants); new constants: " + ("0" if arm.startswith("d1") else "1 (zeta)" + (" + h shape" if "sat" in arm else ""))
    if arm.startswith("d1"):
        t["G5 (A4)"] = "Q2: gate off => 0 (d1); ghost PASS; criterion B, filtered remainder, MW tide NOT ADDRESSED"
        t["G6 (A4)"] = S4["G6_d1"]["status"]
        t["G7 (A4)"] = S4["G7_d1"]["status"]
    else:
        gs = S2.get(f"summary_{arm}")
        t["G5 (A4)"] = f"O1 as above; Q2 (isolated Sun, unfiltered) per gate-at-Sun (A4); criterion B / filtered / MW tide NOT ADDRESSED; ghost PASS"
        t["G6 (A4)"] = S4["G6_d2"]["status"]
        t["G7 (A4)"] = S4["G7_d2"]["status"]
    t["S2 owner's picture (A5)"] = "PASS: no flow mass, Q = 0, functional of baryons; d2 = matter-flow coupling (labelled)" if all(c["ok"] for c in S5) else "see A5"
    T[arm] = t

for arm in ARMS:
    P(f"\n  === {LAB[arm]} ===")
    for k, v in T[arm].items():
        P(f"    {k:44s}: {v}")
R.num("table", T)
nf = R.write()
