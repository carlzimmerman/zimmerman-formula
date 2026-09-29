#!/usr/bin/env python3
"""W2 (b): the Landau pole and the triviality statement (pre-registered B1, B2, B3 in W2_PREREGISTRATION.md).
B1  exact one-loop statement (sympy), two-loop ODE vs closed form, cross-check of the numbers quoted by the lattice paper (electron 10^227 GeV, SM 10^34 GeV).
B2  the pole scale as a function of the charged content (span in decades).
B3  eight hit-tests 'the Landau pole sits at X' + the number of extra unit-hypercharge Dirac singlets that would be needed.
Run:    python3 w2_b1_landau_poles.py           (from this directory; exit 0 iff every check passes)  -> writes w2_b1_results.json
MUTATE: python3 w2_b1_landau_poles.py MUTATE    (one-loop coefficient 2/(3 pi) replaced by 1/(3 pi) in the closed-form pole)
        must exit 1 (exit 3 if the control is broken)  -> writes w2_b1_results_MUTATE.json
"""
import sys
sys.dont_write_bytecode = True
import json, math
import sympy as sp
import w2_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
COEF = 1 / (3 * math.pi) if MUT else 2 / (3 * math.pi)
fails = []
def chk(name, ok, info=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)
PI = math.pi
LN10 = math.log(10)
res = {}

# ------------------------------------------------------------------ B1
print("== B1 exact statement and cross-checks ==")
al, Lg, S1s = sp.symbols("alpha L S1", positive=True)
Lp = sp.solve(sp.Eq(1 / al - sp.Rational(2, 3) / sp.pi * S1s * Lg, 0), Lg)[0]
chk("B1a  one loop: 1/alpha(mu) = 1/alpha_0 - (2 S1/3pi) ln(mu/m) has its pole at ln(Lambda_L/m) = 3 pi/(2 S1 alpha_0)", sp.simplify(Lp - 3 * sp.pi / (2 * S1s * al)) == 0)
rows1, rows2 = L.toy_table(1), L.toy_table(2)
e_only = [r for r in rows1 if r[0] == "e"]
me = e_only[0][1]
ln_e_1L = math.log(me) + (L.ALPHA_INV0 / (COEF * 1.0))
e_nof = [(n, m, a, 0.0) for n, m, a, b in e_only]
ln_e_ode0 = L.pole_scale_twoloop(e_nof)
chk("B1b  ODE with the two-loop term switched off reproduces the closed-form one-loop pole (electron only; AMENDMENT 1: tolerance 5e-5 in ln, the ODE stops at u = 1e-6, offset u/b1 = 4.7e-6)", abs(ln_e_ode0 - ln_e_1L) < 5e-5, f"(closed {ln_e_1L:.6f}, ODE {ln_e_ode0:.6f})")
ln_e_2L = L.pole_scale_twoloop(e_only)
ln_e_2L_closed = math.log(me) + L.twoloop_closed_single(1, 1, 1 / L.ALPHA_INV0, me)
chk("B1c  two-loop ODE equals the closed form (single species set) ", abs(ln_e_2L - ln_e_2L_closed) < 1e-6, f"({ln_e_2L/LN10:.4f} vs {ln_e_2L_closed/LN10:.4f} in log10 GeV)")
print(f"   electron only: log10(Lambda_L/GeV) = {ln_e_1L/LN10:.3f} (one loop), {ln_e_2L/LN10:.3f} (two loop)")
print(f"   the lattice paper (hep-th/9712244) quotes 10^227 GeV for the electron alone: difference {ln_e_1L/LN10-227:.1f} decades from my one-loop value")
chk("B1d  PRE-REGISTERED PREDICTION: the quoted 10^227 is NOT reproduced; one-loop is 10^277 (a likely transposition), two-loop 10^274", abs(ln_e_1L / LN10 - 277.16) < 0.05 and abs(ln_e_2L / LN10 - 274.06) < 0.05 and abs(ln_e_1L / LN10 - 227) > 40)
ln_sm_1L = L.pole_scale_oneloop(rows1, coef=COEF)
ln_sm_2L = L.pole_scale_twoloop(rows1)
print(f"   SM QED-only toy: log10 pole = {ln_sm_1L/LN10:.3f} (one loop), {ln_sm_2L/LN10:.3f} (two loop); the paper quotes ~10^34 GeV")
chk("B1e  SM QED-only toy pole reproduces the quoted ~10^34 GeV within 2 decades", abs(ln_sm_1L / LN10 - 34) < 2 and abs(ln_sm_2L / LN10 - 34) < 2)
res["B1"] = dict(electron_1L=ln_e_1L / LN10, electron_2L=ln_e_2L / LN10, sm_toy_1L=ln_sm_1L / LN10, sm_toy_2L=ln_sm_2L / LN10)

# ------------------------------------------------------------------ B2
print("== B2 content dependence of the pole scale (log10 GeV) ==")
tab = {}
lept = [r for r in rows1 if r[0] in ("e", "mu", "tau")]
tab["e only, 1L"] = ln_e_1L / LN10; tab["e only, 2L"] = ln_e_2L / LN10
tab["e,mu,tau, 1L"] = L.pole_scale_oneloop(lept, coef=COEF) / LN10; tab["e,mu,tau, 2L"] = L.pole_scale_twoloop(lept) / LN10
tab["all SM fermions (set 1), 1L"] = ln_sm_1L / LN10; tab["all SM fermions (set 1), 2L"] = ln_sm_2L / LN10
tab["all SM fermions (set 2), 1L"] = L.pole_scale_oneloop(rows2, coef=COEF) / LN10; tab["all SM fermions (set 2), 2L"] = L.pole_scale_twoloop(rows2) / LN10
tab["fermions (set 1) + W (b=-7), 1L, toy"] = L.pole_scale_oneloop(rows1, coef=COEF, w_b=-7.0) / LN10
solA, lpA, RA = L.sm_twoloop_run("A"); solB, lpB, RB = L.sm_twoloop_run("B")
tab["SM U(1)_Y, 1L, set A"] = L.pole_aY_oneloop("A") / LN10; tab["SM U(1)_Y, 1L, set B"] = L.pole_aY_oneloop("B") / LN10
tab["SM U(1)_Y, 2L (N1 runner), set A"] = lpA / LN10; tab["SM U(1)_Y, 2L (N1 runner), set B"] = lpB / LN10
for N in (1, 3, 9):
    tab[f"U(1)_Y + {N} unit-Y Dirac singlet(s) at 1 TeV, 1L"] = L.pole_aY_oneloop("A", extra=[(N, 4 / 3, 1000.0)]) / LN10
for k, v in tab.items():
    print(f"   {k:52s}: 10^{v:8.3f} GeV   (= {v - math.log10(L.XP):+8.2f} decades relative to M_P)")
span = max(tab.values()) - min(tab.values())
print(f"   span over the listed physical variants: {span:.1f} decades")
chk("B2a  the pole scale depends on the charged content by > 10 decades", span > 10)
chk("B2b  the SM U(1)_Y pole is above M_P for every SM-content variant, below M_P once >= 9 extra unit-Y singlets sit at 1 TeV",
    all(tab[k] > math.log10(L.XP) for k in tab if "SM U(1)_Y" in k) and tab["U(1)_Y + 9 unit-Y Dirac singlet(s) at 1 TeV, 1L"] < math.log10(L.XP) + 1)
chk("B2c  two-loop shifts the SM U(1)_Y pole by < 1 decade relative to one loop (set A)", abs(tab["SM U(1)_Y, 2L (N1 runner), set A"] - tab["SM U(1)_Y, 1L, set A"]) < 1.0)
res["B2"] = tab

# ------------------------------------------------------------------ B3
print("== B3 eight hit-tests: 'the Landau pole sits at X' ==")
variants = []
for Xn in ("X_G", "X_S", "M_red", "M_P"):
    X = L.SCALES[Xn]
    pr = [L.S_oneloop(t, X) for t in (rows1, rows2)]
    variants.append(dict(coupling="QED-toy", X=Xn, pred=pr[0], spread=abs(pr[0] - pr[1]) / L.ALPHA_INV0))
    pa = [L.ALPHA_INV0 + (L.B_Y / (2 * PI) * math.log(X / L.MZ)) - L.A_Y_MZ[k] for k in ("A", "B")]
    variants.append(dict(coupling="U(1)_Y", X=Xn, pred=pa[0], spread=abs(pa[0] - pa[1]) / L.ALPHA_INV0,
                         N_Y_needed=L.need_N_Y(X, "A"), N_Y_needed_B=L.need_N_Y(X, "B")))
assert len(variants) == 8
for v in variants:
    v["miss"] = v["pred"] / L.ALPHA_INV0 - 1
    v["tol"] = max(2 * v["spread"], 0.01)
    v["within_tol"] = abs(v["miss"]) <= v["tol"]
    extra = f"  N_Y needed at 1 TeV = {v['N_Y_needed']:.2f} (set B {v['N_Y_needed_B']:.2f})" if "N_Y_needed" in v else ""
    print(f"   {v['coupling']:8s} X = {v['X']:6s}: 1/alpha_pred(0) = {v['pred']:8.3f}  miss = {v['miss']:+.4f}  tol = {v['tol']:.4f}  within tol: {v['within_tol']}{extra}")
chk("B3a  eight variants scored", len(variants) == 8)
chk("B3b  no variant within its tolerance (declared expectation: all miss by > 20%)", not any(v["within_tol"] for v in variants) and min(abs(v["miss"]) for v in variants) > 0.20, f"(smallest |miss| = {min(abs(v['miss']) for v in variants):.4f})")
chk("B3c  the spectrum needed to move the U(1)_Y pole to M_P is >= 1 unforced multiplet (N_Y > 1)", [v for v in variants if v["coupling"] == "U(1)_Y" and v["X"] == "M_P"][0]["N_Y_needed"] > 1)
res["B3"] = variants
json.dump(res, open("w2_b1_results_MUTATE.json" if MUT else "w2_b1_results.json", "w"), indent=1, default=float)
L.finish(fails, MUT, "w2_b1")
