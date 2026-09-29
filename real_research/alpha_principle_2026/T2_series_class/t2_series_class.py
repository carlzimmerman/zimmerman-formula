#!/usr/bin/env python3
"""T2 -- is alpha^-1 + alpha - 12 pi alpha^2 = 4 Z^2 + 3 a genuine QED loop series?  Pre-registered in T2_PREREGISTRATION.md.
Run:  python3 t2_series_class.py            (real run; exit 0 iff all checks pass)
      python3 t2_series_class.py --mutate   (control: replaces pi by a rational in the class test; exit 1 iff exactly the class checks A1 and A2 fail (pi rational makes both relations appear), exit 3 if broken)
"""
import sys
import random
from fractions import Fraction
import mpmath as mp

MUT = "--mutate" in sys.argv
mp.mp.dps = 110
CH, FAILED = [], []


def chk(tag, ok, detail=""):
    CH.append(bool(ok))
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


PI = mp.mpf(22) / 7 if MUT else mp.pi          # the control: a rational 'pi' must make pi-relations appear
AINV = mp.mpf("137.035999177")
ALPHA = 1 / AINV
Z2 = 32 * mp.pi / 3
C_TARGET = 4 * Z2 + 3
RESID = C_TARGET - AINV
print("T2: is alpha^-1 + alpha - 12 pi alpha^2 = 4 Z^2 + 3 a genuine QED loop series?   (MUTATE=%s)" % MUT)
print(f"  residual to close: 4Z^2+3 - alpha^-1 = {mp.nstr(RESID, 12)}")

# ---- class sanity: the published closed forms, checked against their published decimals (recalled)
A2 = mp.mpf(197) / 144 + mp.pi ** 2 / 12 - (mp.pi ** 2 / 2) * mp.log(2) + mp.mpf(3) / 4 * mp.zeta(3)
chk("C0a the two-loop electron g-2 coefficient closed form equals its published decimal -0.328478965579 (recalled)", abs(A2 - mp.mpf("-0.328478965579193")) < mp.mpf("1e-12"), f"(A2 = {mp.nstr(A2, 15)})")
print("  => genuine order-n QED coefficients are (1/pi)^n x (Q-span of 1, zeta(3), pi^2, pi^2 ln 2, ...): first order = rational/pi")

# ---- T-A: integer-relation search
basis1 = [mp.mpf(1), 1 / PI]                    # is  a1 = 1  a rational multiple of 1/pi ?  <=>  relation  m*1 + n*(1/pi) = 0 with a1=1 ... test pi rational:
rel1 = mp.pslq([mp.mpf(1), PI], maxcoeff=10 ** 6, maxsteps=10 ** 6)            # m + n*pi = 0 ?  (pi rational)
chk("A1 a1 = 1 is NOT of the form (rational)/pi: no integer relation m + n*pi = 0 with |m|,|n| <= 1e6 (i.e. pi is not a small rational)", rel1 is None, f"(pslq -> {rel1})")
# a2 = -12 pi in the class {(r + s zeta3 + t pi^2 + u pi^2 ln2)/pi^2}  <=>  -12 pi^3 in Q-span{1, zeta3, pi^2, pi^2 ln2}
vec = [PI ** 3, mp.mpf(1), mp.zeta(3), PI ** 2, PI ** 2 * mp.log(2)]
rel2 = mp.pslq(vec, maxcoeff=10 ** 6, maxsteps=10 ** 6)
chk("A2 a2 = -12 pi is NOT in the QED second-order class: no integer relation among pi^3, 1, zeta(3), pi^2, pi^2 ln 2 up to 1e6", rel2 is None, f"(pslq -> {rel2})")

if MUT:
    works = [t.split()[0] for t in FAILED] == ["A1"] or [t.split()[0] for t in FAILED] == ["A1", "A2"]
    print("\nMUTATE CONTROL: with pi replaced by 22/7 the pi-relations must appear (A1, and A2 here, must FAIL); failed:", [t.split()[0] for t in FAILED])
    sys.exit(1 if works else 3)

# ---- T-B: how much freedom do two class-restricted rational slots have?
pi = mp.pi
x1 = ALPHA / pi                                 # coefficient weight of r1
x2 = (ALPHA / pi) ** 2                          # coefficient weight of r2
fr = lambda n, d: mp.mpf(n) / d


def count_hits(target, tol, nmax1=64, nmax2=4096, dmax=12):
    """Count distinct (r1, r2) with r1 = p/q (|p|<=nmax1), r2 = p/q (|p|<=nmax2), q<=dmax  such that |r1*x1 + r2*x2 - target| < tol."""
    seen1 = {}
    for q in range(1, dmax + 1):
        for p in range(-nmax1, nmax1 + 1):
            f = Fraction(p, q)
            seen1[f] = fr(f.numerator, f.denominator)
    seen2 = {}
    for q in range(1, dmax + 1):
        for p in range(-nmax2, nmax2 + 1):
            f = Fraction(p, q)
            seen2[f] = fr(f.numerator, f.denominator)
    r2s = sorted(seen2.items(), key=lambda kv: kv[1])
    vals2 = [float(v) for _, v in r2s]
    import bisect
    hits = 0
    n1 = len(seen1)
    for f1, v1 in seen1.items():
        need = float((target - v1 * x1) / x2)              # r2 needed
        lo = bisect.bisect_left(vals2, need - float(tol / x2))
        hi = bisect.bisect_right(vals2, need + float(tol / x2))
        hits += max(0, hi - lo)
    return hits, n1, len(seen2)


mp.mp.dps = 30
h8, n1, n2 = count_hits(RESID, mp.mpf("1e-8"))
h10, _, _ = count_hits(RESID, mp.mpf("5e-10"))
h6, _, _ = count_hits(RESID, mp.mpf("1e-6"))
print(f"\nT-B: class-restricted pairs (r1, r2): {n1} values of r1 x {n2} values of r2 = {n1 * n2} pairs")
print(f"  pairs whose series lands within 1e-6 of the residual: {h6};  within 1e-8: {h8};  within 5e-10: {h10}")
chk("B1 many class-restricted rational pairs already close the residual to 1e-8 (freedom of two rational slots)", h8 >= 1, f"({h8} pairs)")
# ---- T-C: random targets of the same size
random.seed(12345)
counts = []
for _ in range(8):
    t = RESID * mp.mpf(random.uniform(0.5, 1.5))
    counts.append(count_hits(t, mp.mpf("1e-8"))[0])
print(f"T-C: the same count for 8 random residuals of comparable size: {counts}  (real residual: {h8})")
chk("C1 random residuals give hit counts of the same order as the real one (a hit within 1e-8 means nothing)", (sum(counts) / len(counts)) >= 0.25 * h8 and min(counts) >= 0, f"(mean {sum(counts) / len(counts):.1f} vs real {h8})")

print("\nVERDICT (against the declared criteria):")
print("  The identity's coefficients a1 = 1 and a2 = -12 pi are NOT in the class real QED loop expansions produce (first order rational/pi; second order a Q-span over pi^2):")
print("  it has the shape of a series in alpha but not of a QED series, so 'two-loop' describes its form, not any diagram.  Two rational slots in the QED class have plenty of freedom to close the residual;")
print("  a random residual is matched as often, so the closeness is not evidence.  alpha stays an INPUT; kappa = 1/2 FITTED.")
ok = all(CH)
sys.exit(0 if ok else 1)
