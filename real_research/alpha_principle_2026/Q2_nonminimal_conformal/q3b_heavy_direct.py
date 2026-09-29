#!/usr/bin/env python3
"""Q2/q3b -- supplementary (Amendment 5): direct mode sums at heavy mass (mu = 6, 10), xi = 0 and xi = 1/6, lam = 0.3, against
f_0(lam, mu_eff) + (lam/3) ln(mu/mu_eff)  (AH4 closed form, transcribed; Delta from q3).  Uses q3's functions (imported, not modified).

Run:    python3 q3b_heavy_direct.py            (real run; exit 0 iff the comparison passes at 2e-3)
        python3 q3b_heavy_direct.py --mutate   (control: s = -2 used for the xi = 1/6 points; must FAIL;
                                               exit 1 = "control fails as required", exit 3 = control did NOT fail)
"""
import sys
import math
sys.path.insert(0, ".")
import q3_current_conformal as q3

MUTATE = "--mutate" in sys.argv
if __name__ == "__main__":
    XI = 1 / 6
    pts = [(0.3, 6.0, 0.0), (0.3, 10.0, 0.0), (0.3, 6.0, XI), (0.3, 10.0, XI)]
    specs = [(lam, mu, xi, mu, (-2.0 if (MUTATE and xi != 0) else 12 * xi - 2)) for lam, mu, xi in pts]
    res = []
    for sp_, (lam, mu, xi) in zip(specs, pts):
        res.append(q3.direct_f([sp_], K=40.0 * mu)[0])      # Amendment 5b: K = 40 mu
    worst = 0.0
    print("     lambda  mu     xi      direct f          f_0 + (lam/3) ln(mu/mu_eff)   ratio       tail c2")
    for (lam, mu, xi), (fd, c2) in zip(pts, res):
        fc = float(q3.f_formula(lam, mu, xi, mu, 12 * xi - 2))
        worst = max(worst, abs(fd / fc - 1))
        print(f"     {lam:5.2f}  {mu:5.1f}  {xi:5.3f}  {fd:+.10f}   {fc:+.10f}          {fd / fc:+.6f}   {c2:+.1e}")
    ok = worst <= 2e-3
    print(f"  [{'PASS' if ok else 'FAIL'}] q3b direct sum = closed form at heavy mass (worst |ratio - 1| = {worst:.1e}; threshold 2e-3)")
    if MUTATE:
        if not ok:
            print("MUTATE CONTROL: the comparison FAILED as required -- CONTROL FAILS AS REQUIRED")
            sys.exit(1)
        print("MUTATE CONTROL: the comparison did NOT fail -- CONTROL DID NOT FAIL")
        sys.exit(3)
    sys.exit(0 if ok else 1)
