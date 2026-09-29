#!/usr/bin/env python3
"""W2 verdicts: collects the hit-tests of w2_a1 (12) and w2_b1 (8), calls lane D's bar on every one, applies the rules declared in W2_PREREGISTRATION.md, prints the per-sub-question verdicts.
Needs the JSON files written by w2_a1_ladder_critical.py, w2_b1_landau_poles.py, w2_c1_quasi_fixed.py, w2_d1_large_nf.py, w2_e1_ward_z3.py (run those first).
Run:    python3 w2_f_verdicts.py           (from this directory; exit 0 iff the gates pass, the bar's positive control clears, and no hit-test is a LEAD)  -> writes w2_f_verdicts.json
MUTATE: python3 w2_f_verdicts.py MUTATE    (the bar's positive control is run with fitted_reals = 1)  must exit 1 (exit 3 if the control is broken)  -> writes w2_f_verdicts_MUTATE.json
"""
import sys
sys.dont_write_bytecode = True
import json, math
import w2_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(name, ok, info=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)

# gates
rows1 = L.toy_table(1)
S_MP = L.S_oneloop(rows1, L.XP)
chk("G1  toy S(M_P) reproduces lane I's 77.2304 (quark set A) to 1e-4 relative", abs(S_MP / 77.2304 - 1) < 1e-4, f"({S_MP:.4f})")
aY_MP = L.aY_oneloop(L.XP, "A")
chk("G2  one-loop 1/alpha_Y(M_P) reproduces lane B/U3's 55.48 to 1e-3", abs(aY_MP / 55.48 - 1) < 1e-3, f"({aY_MP:.3f})")
r = L.bar(1e-12, predicted_precision=0.0)          # AMENDMENT 6: control uses no predicted-precision floor (see the FIRSTRUN output)
chk("G3  the bar's positive control (miss 1e-12, no fitted reals, 20-trial family) clears", r["clears"])
if MUT:
    import alpha_bar_checker as ABC, math as _m
    r2 = ABC.assess(delta=1e-12, log2size=_m.log2(20), n_targets=1, predicted_precision=0.0, fitted_reals=1, scale_stated=True, verbose=False)
    chk("G3m MUTATE: the same positive control with one fitted real must still clear (it must NOT)", r2["clears"])

A = json.load(open("w2_a1_results.json"))["A3"]
B = json.load(open("w2_b1_results.json"))["B3"]
hits = []
for v in A:
    hits.append(dict(lane="A3", label=f"{v['coupling']} X={v['X']} alpha_c={v['alpha_c']}", miss=v["miss"], tol=v["tol"], within_tol=v["within_tol"]))
for v in B:
    hits.append(dict(lane="B3", label=f"{v['coupling']} pole at X={v['X']}", miss=v["miss"], tol=v["tol"], within_tol=v["within_tol"]))
chk("V0  twenty hit-tests collected (12 + 8)", len(hits) == 20)
print("== the bar (lane D) for every hit-test ==")
leads = []
for h in hits:
    a = L.bar(h["miss"])
    h["bar_clears"] = bool(a["clears"]); h["P"] = float(a["p"]); h["c2_precision"] = bool(a["c2_precision"])
    verdict = "LEAD-CANDIDATE" if (h["within_tol"] and h["bar_clears"]) else "DEAD"
    h["verdict"] = verdict
    if verdict != "DEAD":
        leads.append(h)
    print(f"   {h['lane']}  {h['label']:42s} miss {h['miss']:+.4f} (tol {h['tol']:.3f})  bar: P = {h['P']:.3g}, precision ok: {h['c2_precision']}, clears: {h['bar_clears']}  -> {verdict}")
chk("V1  no hit-test is a LEAD (none within tolerance AND clearing the bar)", not leads)
chk("V2  the closest hit-test misses by more than 20% (expected outcome, stated in advance)", min(abs(h["miss"]) for h in hits) > 0.20, f"(closest: {min(abs(h['miss']) for h in hits):.4f})")

print("== joint test (lane U3 scorer) ==")
print("   Every rule above constrains ONE abelian coupling (alpha_em toy or alpha_Y). SU(2) and SU(3) are asymptotically free: no Landau pole, no near-critical value below M_P (A2: R_SU2 = 0.015, R_SU3 = 0.024 at M_P).")
print("   Lane U3's T-IND requires >= 3 absolute constraints including alpha_Y AND alpha_2; none of these rules can satisfy it, so none can be a LEAD regardless of the numerical miss.")

verdicts = [
    ("(a) critical coupling / chiral breaking", "DEAD", "alpha_c ~ 1 (pi/3 derived; 0.933667 unverified); SM abelian R <= 0.017 below M_P; control (QCD) fires at ~0.35 GeV; 12/12 variants miss by > 39%"),
    ("(b) Landau pole / triviality", "DEAD", "the exact statement is 'pole scale = f(a_Y(m_Z), charged spectrum)'; content moves it over 260 decades; pole at any Planckian X misses by > 40% and needs >= 7 unforced multiplets; 8/8 miss"),
    ("(c) compositeness / quasi-fixed points", "DEAD", "no IR focusing of gauge couplings (elasticity 0.56, additive in 1/alpha); Z3 = 0 is the pole equation; Yukawa QFP is real (control) but says nothing about an abelian coupling"),
    ("(d) large-N_f QED", "UNDECIDED (existence of a UV zero) / DEAD (as a selector)", "F_1 reproduced; zeros within e^(-15 pi^2 N/7) of A = 15/2 (scheme dependent, 1/N-truncated); any UV fixed point trades alpha_0 for ln(Lambda_*/m)"),
    ("(e) Ward identity Z1 = Z2, Z3", "DEAD", "identity e_R = sqrt(Z3) e_0, inequality Z3 <= 1 (bound), exact charge RATIOS; the bare coupling, cutoff and spectrum stay free"),
]
print("== verdicts ==")
for a, b, c in verdicts:
    print(f"   {a:42s} {b:48s} {c}")
json.dump(dict(hits=hits, leads=leads, verdicts=verdicts), open("w2_f_verdicts_MUTATE.json" if MUT else "w2_f_verdicts.json", "w"), indent=1, default=float)
L.finish(fails, MUT, "w2_f")
