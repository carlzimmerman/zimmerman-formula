#!/usr/bin/env python3
"""u2_4 -- run the U2 winding-charge model's alpha values through lane D's calibration bar (alpha_bar_checker.assess).  Pre-registered in U2_PREREGISTRATION.md.

Members scored: the primary member (quantum-limited core, w = pi): alpha_c = 2 pi; and the closest of the declared 45 members, the post-observation geometric-mean member
alpha_c = 3 kappa^2/(32 pi) = 1/134.04.  Declared family size N_eff = 45, n_targets = 1, fitted reals = 0, scale stated (core scale).
Predicted precision (a-priori): the official reading is 1.0 (the model fixes alpha only to the O(1)-to-1e3 spread of its own xi_cap sub-family); sensitivities with 0.3 and N = 1 are printed.

Run:      PYTHONDONTWRITEBYTECODE=1 python3 u2_4_bar.py            (exit 0 iff the checks pass; the checks assert the checker REJECTS the model and ACCEPTS the positive control)
Control:  PYTHONDONTWRITEBYTECODE=1 python3 u2_4_bar.py --mutate   (feeds the closest member a fake miss of 1e-11; 'the model does not clear' must FAIL; exit 1)
"""
import os
import sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "D_calibration_bar"))
import math
import io
import contextlib
import mpmath as mp
import alpha_bar_checker as ck

MUT = "--mutate" in sys.argv
mp.mp.dps = 30
CH = []


def chk(tag, ok, detail=""):
    CH.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


T = mp.mpf("137.035999177")
kappa = mp.mpf(1) / 2
a_primary = 2 * mp.pi
a_gm = 3 * kappa ** 2 / (32 * mp.pi)
miss_primary = float(abs((1 / a_primary) / T - 1))
miss_gm = float(abs((1 / a_gm) / T - 1))
if MUT:
    miss_gm = 1e-11
print("U2 / u2_4: lane D's bar applied to the U2 model" + ("   [MUTATED: closest member given a fake miss of 1e-11]" if MUT else ""))
print(f"primary member: alpha_c = 2 pi, 1/alpha_c = {mp.nstr(1 / a_primary, 8)}, miss = {miss_primary:.6g}")
print(f"closest member (geometric mean, post-observation): alpha_c = 3 kappa^2/(32 pi), 1/alpha_c = {mp.nstr(1 / a_gm, 10)}, miss = {miss_gm:.6g}")
print(f"checker density rho = {ck.RHO_DEFAULT:.4f}; bar: P < {ck.B.BAR_P:g}, miss <= {ck.B.BAR_DELTA:g} (or within 2x own predicted precision), 0 fitted reals, scale stated")
lam_chance = 45 * ck.RHO_DEFAULT * 2 * 1e-3
print(f"expected chance hits in the 45-member family at tolerance 1e-3: {lam_chance:.4g}")


def run(label, **kw):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = ck.assess(verbose=False, **kw)
    print(f"  {label:78s} lam = {r['lam']:.4g}  P = {r['p']:.4g}  c1 {str(r['c1_lookelsewhere']):5s} c2 {str(r['c2_precision']):5s}  -> {'CLEARS' if r['clears'] else 'does not clear'}")
    return r


print("\nscoring (official reading first):")
r1 = run("primary, N=45, predicted precision 1.0 (official)", delta=miss_primary, size=45, n_targets=1, predicted_precision=1.0, fitted_reals=0)
r1b = run("primary, N=45, claims exactness (predicted precision 0)", delta=miss_primary, size=45, n_targets=1, predicted_precision=0.0, fitted_reals=0)
r2 = run("closest member, N=45, predicted precision 1.0 (official)", delta=miss_gm, size=45, n_targets=1, predicted_precision=1.0, fitted_reals=0)
r2b = run("closest member, N=45, predicted precision 0.3 (kappa's fit spread, generous)", delta=miss_gm, size=45, n_targets=1, predicted_precision=0.3, fitted_reals=0)
r2c = run("closest member alone, N=1, predicted precision 0.3 (most generous reading)", delta=miss_gm, size=1, n_targets=1, predicted_precision=0.3, fitted_reals=0)
r2d = run("closest member alone, N=1, predicted precision 0.0219 (= its own miss; not a-priori)", delta=miss_gm, size=1, n_targets=1, predicted_precision=0.0219, fitted_reals=0)
r2e = run("closest member, N=45, claims exactness (predicted precision 0)", delta=miss_gm, size=45, n_targets=1, predicted_precision=0.0, fitted_reals=0)
rpos = run("POSITIVE CONTROL: a 1e-12 match in a 2^6 family", delta=1e-12, log2size=6, n_targets=1, fitted_reals=0)
rfit = run("control: the same 1e-12 match with one fitted real (the xi-relabelled model)", delta=1e-12, log2size=6, n_targets=1, fitted_reals=1)

print()
chk("D1 the primary member (alpha_c = 2 pi) does not clear the bar under either reading", (not r1["clears"]) and (not r1b["clears"]))
chk("D2 the closest member does not clear the bar (official, generous, N=1 and exactness readings)", not any(r["clears"] for r in (r2, r2b, r2c, r2e)))
chk("D3 even the most generous non-a-priori reading (N=1, predicted precision = own miss) has P above the 1e-3 threshold or fails the fixed-precision rule",
    (not r2d["clears"]) or MUT)
chk("D4 positive control: the checker accepts a 1e-12 match in a 2^6 family (so the rejections are not a broken checker)", rpos["clears"])
chk("D5 the xi-relabelled model (alpha traded for one fitted length) fails on 'zero fitted reals'", not rfit["clears"])
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = ck.selftest(False)
chk("D6 the checker's own selftest exits 0", rc == 0)

n_fail = CH.count(False)
print(f"\nchecks: {len(CH) - n_fail}/{len(CH)} pass")
print("\nVERDICT (against the pre-registered criteria):")
print("  Neither the primary member (misses by a factor 861) nor the closest member (2.2% off) clears the bar. Even the most generous reading (the closest member alone, N=1, predicted precision set equal to its own 2.19% miss, which is not a-priori) gives P = 1.09e-3, just above the 1e-3 threshold, and the model's real a-priori precision is O(1).")
print("  The model reaches the target in NO reading. The O(1)-to-fourth-power structure means the nearest member is a near coincidence of the kind lane D's bar is built to discount (it reproduces 4 Z^2, the part of the old formula that lane D scored as chance).")
if MUT:
    print("\nMUTATE CONTROL: the closest member was given a fake miss of 1e-11; D2 (the model does not clear) must FAIL.")
    ok = not CH[1]
    print("  " + ("FAILED as required -- the control works (exit 1)" if ok else "DID NOT FAIL -- the control is broken"))
    sys.exit(1 if ok else 0)
sys.exit(0 if n_fail == 0 else 1)
