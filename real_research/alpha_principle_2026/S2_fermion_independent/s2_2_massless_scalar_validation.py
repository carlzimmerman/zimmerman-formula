#!/usr/bin/env python3
"""S2-2 -- ROUTE B' (method validation): the SAME massless-limit method (flat on-shell vacuum polarization + retarded response + Weyl anomaly) applied to the
conformally coupled massless charged SCALAR in dS_4, whose target comes from a different lane's direct mode sums (Q2/q3: 'C' rows, five points to 1.1e-7, and AH4's
Kobayashi-Afshordi closed form).  If the method reproduces that number the anomaly coefficient and the scheme identification are validated on a second field.

Pre-registered in S2_PREREGISTRATION.md (before this script was run).  Units H = 1, tau = -T, evaluation at T = 1.  f := 4 pi^2 J_par/(e H^3), lambda = eE/H^2, small lambda.
Prediction of the method (evaluated below from numerical ingredients): f/lambda = (1/3) (ln M + c_S),  c_S = c_an/4 - kappa_s,  kappa_s = 1/6 - gamma_E (analytic), c_an = 2 (units alpha/(12 pi)).
Target: f = f_0(lambda, sqrt 2) + (lambda/3) ln(M/sqrt 2)  (Q2), f_0 = K&A/AH4 closed form, imported READ-ONLY from Q1_ds4_fermions/q1_lib.py (scalar_closed_f).
Helper functions (vacuum-polarization integrals, spectral response, anomaly algebra) are imported from s2_1_massless_fermion.py (same lane).

Run:     python3 s2_2_massless_scalar_validation.py            (real run; exit 0 iff every check passes)
         python3 s2_2_massless_scalar_validation.py --mutate   (control: the FERMION anomaly coefficient in scalar units, 8 instead of 2, is used; S2b and S3 must both FAIL;
                                                                 exit 1 if both fail = the control works, exit 3 if either passes)
Only the literal argument --mutate triggers the control.  Set PYTHONDONTWRITEBYTECODE=1.
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import numpy as np
import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "Q1_ds4_fermions"))
import s2_1_massless_fermion as F1
from q1_lib import scalar_closed_f

MUTATE = "--mutate" in sys.argv
CHECKS = {}


def check(tag, ok, detail=""):
    CHECKS[tag.split()[0]] = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def s0_vacuum_polarization():
    print("\nS0. scalar one-loop vacuum polarization, on-shell scheme (recalled; verified here)")
    x = sp.symbols("x", positive=True)
    val = sp.integrate((1 - 2 * x) ** 2 * sp.log(x * (1 - x)), (x, 0, 1))
    check("S0a Int (1-2x)^2 ln(x(1-x)) = -8/9 exactly (sympy)", sp.simplify(val + sp.Rational(8, 9)) == 0, f"({val})")
    mp.mp.dps = 30
    Q2 = mp.mpf(10) ** 8
    lhs = F1.feynman_pi(Q2, "s")
    rhs = -(mp.log(Q2) - mp.mpf(8) / 3) / 12
    check("S0b m -> 0 form: -(1/4) Int (1-2x)^2 ln(1 + x(1-x)Q2/m2) = -(1/12)[ln(Q2/m2) - 8/3] (units alpha/pi) at Q2/m2 = 1e8, to 1e-6", abs(lhs - rhs) < 1e-6, f"(diff {float(lhs - rhs):.2e})")
    lo = F1.feynman_pi(mp.mpf(10) ** -6, "s") / mp.mpf(10) ** -6
    check("S0c small-Q2 slope = -1/120 (units alpha/pi per Q2/m2) to 1e-5", abs(lo + mp.mpf(1) / 120) < 1e-5 * (mp.mpf(1) / 120), f"(slope {float(lo):.9f} vs {-1/120:.9f})")
    worst = max(abs(F1.feynman_pi(q, "s") - F1.disp_pi(q, "s")) for q in (0.5, 3.0, 40.0))
    check("S0d spectral representation -(1/12) Q2 Int ds (1-4m2/s)^{3/2}/(s(s+Q2)) equals the Feynman-parameter integral at Q2/m2 = 0.5, 3, 40 (1e-8)", worst < 1e-8, f"(worst {float(worst):.2e})")


def main():
    print("=" * 118)
    print(f"S2-2 method validation on the conformal massless scalar -- mode: {'MUTATE CONTROL (fermion anomaly coefficient used)' if MUTATE else 'REAL RUN'}")
    print("=" * 118)
    s0_vacuum_polarization()
    kappa_s = mp.mpf(1) / 6 - mp.euler
    errs, mono, kap = F1.w2_spectral_response("s", kappa_s)
    check("S1 spectral response -> kappa_s = 1/6 - gamma_E: error at m = 1e-3 <= 1e-4 and monotone decreasing", errs[-1] <= 1e-4 and mono, f"(errors {[f'{float(e):.1e}' for e in errs]})")
    # plus-distribution constant (same integral as the fermion; only the scheme constant 8/3 and the prefactor differ)
    Flim3 = mp.mpf(3)        # lim [Int_eps D(tau-u)/u du + D ln eps] at T = 1, E = 1 (verified symbolically and numerically in s2_1 W3b, W3c)
    D = -2
    lnD = -mp.euler * D - Flim3
    bracket_const = 2 * lnD - mp.mpf(8) / 3 * D
    kappa_num = -bracket_const / 4
    check("S1b plus-distribution constant kappa_s = 1/6 - gamma_E (1e-12, uses the exact limit 3)", abs(kappa_num - kappa_s) < 1e-12, f"(kappa_s = {float(kappa_num):.12f})")
    c_an = 8 if MUTATE else 2
    print("\nS2. Weyl-anomaly coefficient (units alpha/(12 pi); pole algebra and dS invariance are identical in form to the fermion's, P -> P_s)")
    # log coefficient of the scalar Pi_hat: -1/12 (units alpha/pi): read off numerically from the m -> 0 form checked in S0b (slope of Pi_hat vs ln Q2)
    q1, q2 = mp.mpf(10) ** 9, mp.mpf(10) ** 11          # Amendment 3: the first run used 1e6, 1e8, where the O(ln Q2/Q2) correction is 1.6e-5 relative
    slope = (F1.feynman_pi(q2, "s") - F1.feynman_pi(q1, "s")) / (mp.log(q2) - mp.log(q1))
    check("S2a the ln Q2 coefficient of Pi_hat_s is -1/12 (units alpha/pi) = -P_s, so the pole is 2 P_s/eps and the anomaly term is 2 P_s ln a", abs(slope + mp.mpf(1) / 12) < 1e-6, f"(slope {float(slope):.9f})")
    Jphys = F1.w4_anomaly(c_an)
    # rename the checks from w4_anomaly: they are stored in F1.CHECKS
    okb = F1.CHECKS["W4b'"]
    CHECKS["S2b"] = okb
    print(f"  [{'PASS' if okb else 'FAIL'}] S2b dS invariance: the anomaly coefficient used ({c_an} in units P_s) makes the physical current T-independent")
    # assembly
    print("\nS3. prediction vs Q2/AH4 closed form")
    c_S = mp.mpf(c_an) / 4 - kappa_num
    print(f"     route B' constant: f/lambda = (1/3)(ln M + c_S),  c_S = c_an/4 - kappa_s = {float(c_S):.12f}   [gamma_E + 1/3 = {float(mp.euler + mp.mpf(1)/3):.12f}]")
    lams = [0.05, 0.03, 0.02, 0.01]
    vals = []
    for l in lams:
        f0 = scalar_closed_f(l, math.sqrt(2.0))
        vals.append(f0 / l)
        print(f"     lambda = {l:5.3f}   f_0(lambda, sqrt 2)/lambda = {f0/l:+.12f}")
    A = np.array([[1.0, l ** 2, l ** 4] for l in lams[1:]])
    coef = np.linalg.solve(A, np.array(vals[1:]))
    A4 = np.array([[1.0, l ** 2, l ** 4, l ** 6] for l in lams])
    coef4 = np.linalg.solve(A4, np.array(vals))
    a0 = coef[0]
    print(f"     extrapolation lambda -> 0: quadratic-in-lambda^2 fit (3 pts) a0 = {a0:.12f};  cubic fit (4 pts) a0 = {coef4[0]:.12f}")
    cQ2 = 3 * a0 - math.log(math.sqrt(2.0))          # 3 f/lambda - ln M = 3 f_0/lambda - ln sqrt 2
    print(f"     Q2/AH4 constant  c_S(Q2) = 3 f_0(sqrt 2)/lambda - ln sqrt 2 = {cQ2:.12f}")
    rel = abs(float(c_S) - cQ2) / abs(cQ2)
    print(f"     relative difference |c_S(route) - c_S(Q2)|/|c_S(Q2)| = {rel:.3e}")
    check("S3 route B' reproduces the Q2/AH4 conformal-scalar constant to 1e-6 (relative)", rel <= 1e-6, f"(rel {rel:.2e})")
    ing = all(CHECKS[k] for k in ("S0a", "S0b", "S0c", "S0d", "S1", "S1b", "S2a", "S2b"))
    verdict = "VALIDATED" if (ing and CHECKS["S3"]) else "NOT VALIDATED"
    print(f"\nroute B' method validation verdict: {verdict}")
    print("=" * 118)
    n_ok = sum(CHECKS.values())
    print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
    print("Scope: conformally coupled massless charged scalar, on-shell(m) scheme, linear in E; the comparator's own validity: Q2 direct sums at lambda = 0.3-0.8 (five points, worst 1.1e-7) and AH4/K&A closed form.")
    if MUTATE:
        if (not CHECKS["S2b"]) and (not CHECKS["S3"]):
            print("\nMUTATE CONTROL: the fermion anomaly coefficient was used for the scalar; S2b and S3 FAILED as required -- the control works")
            sys.exit(1)
        print("\nMUTATE CONTROL: a targeted check did NOT fail -- the control has no power")
        sys.exit(3)
    sys.exit(0 if n_ok == len(CHECKS) else 2)


if __name__ == "__main__":
    main()
