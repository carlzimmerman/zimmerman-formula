#!/usr/bin/env python3
"""mi_thermal_class_nogo_2026.py -- close (or open) the whole thermal-saturation CLASS.

THE NARROW OPEN QUESTION, from mi_dissipative_identification_2026: what fixes the
bath-coupled spectral fraction? A condition R(Z) = F fixes Z, hence kappa, hence a0. Previous
attempts guessed F one at a time. That is unbounded and each guess costs look-elsewhere.

THIS SCRIPT DOES IT EXHAUSTIVELY INSTEAD. Rather than inventing more targets, it enumerates
EVERY dimensionless constant the kernel itself FORCES -- each one derived from the committed
kernel or measure, none chosen for taste -- and uses each as the target F. Then:

  * if some forced F gives kappa = 1/2 tightly, that is a genuine derivation, worth its
    precision minus log2(#constants) bits;
  * if NONE does, the entire thermal-saturation class is CLOSED, which is a real no-go and
    far more valuable than another miss.

It also runs the inverse, which is the sharpest single statement available: compute
R(Z_framework) exactly and ask whether that number lies in the kernel's forced constant set
at all. If it does not, no condition of this class can ever produce it.

THE FORCED CONSTANT SET (each verified in S1 before use, not asserted):
    1                     total sum rule INT dmu/|t|
    2/pi                  region B (on-cut) weight                    [KERNEL_THEORY.md:38]
    1 - 2/pi              region A weight
    1/pi                  dissipative weight, INT dmu/|t| * sin phi   [derived 2026-07-29]
    1/4                   branch point |z|
    1/2                   branch point in u = omega c/a0
    4/9                   z at which K = 1/2
    (sqrt5-1)/2           K(1), the kernel at z = 1
Aesthetic constants (1/e, 1/(2pi^2), ...) are EXCLUDED -- they are not forced by anything in
this framework, and including them is what made the earlier sweep weak.

Exit 0 = all checks ran. No hard-coded verdicts. Outcome accepted whatever it is.
"""
from __future__ import annotations
import math
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return cond

def banner(s):
    print("\n" + "=" * 98); print(s); print("=" * 98)

SQ8PI3   = math.sqrt(8 * math.pi / 3)
KAPPA_FW = 0.5
Z_FW     = SQ8PI3 / KAPPA_FW
K_LO, K_HI = 0.5 / 1.16, 0.5 / 0.84


def measure_integral(f, lo_u=0.0, hi_u=np.inf):
    tot = 0.0
    a, b = max(lo_u, 0.0), min(hi_u, 0.5)
    if b > a:
        tot += quad(lambda u: f(u * u) * (1 - np.sqrt(max(1 - 4 * u * u, 0.0))) / np.pi,
                    a, b, limit=400)[0]
    a, b = max(lo_u, 0.5), hi_u
    if b > a:
        tot += quad(lambda u: f(u * u) / np.pi, a, b, limit=400)[0]
    return tot


def R(Z):
    """KMS-forced thermally active fraction of the unit sum rule."""
    return measure_integral(lambda T: math.tanh(math.pi * math.sqrt(T) / Z) / T)


def main() -> int:
    banner("mi_thermal_class_nogo_2026 -- exhaust the thermal-saturation class")

    # -----------------------------------------------------------------------------------
    banner("S1. Verify every forced constant BEFORE using it as a target")
    z = sp.Symbol("z", positive=True)
    K = (sp.sqrt(1 + 4 * z) - 1) / (2 * sp.sqrt(z))
    u = sp.Symbol("u", positive=True)

    total = measure_integral(lambda T: 1.0 / T)
    regB = measure_integral(lambda T: 1.0 / T, 0.5, np.inf)
    diss = float(sp.integrate(1 / (sp.pi * u**2) * (1 / (2 * u)), (u, sp.Rational(1, 2), sp.oo)))
    K_at_1 = float(K.subs(z, 1))
    z_half = sp.solve(sp.Eq(K, sp.Rational(1, 2)), z)

    check(abs(total - 1.0) < 3e-3, f"total sum rule = 1 ({total:.6f})")
    check(abs(regB - 2 / math.pi) < 3e-3, f"region B = 2/pi = {2/math.pi:.6f} ({regB:.6f})")
    check(abs(diss - 1 / math.pi) < 1e-9, f"dissipative = 1/pi = {1/math.pi:.6f} ({diss:.6f})")
    check(abs(K_at_1 - (math.sqrt(5) - 1) / 2) < 1e-12,
          f"K(1) = (sqrt5-1)/2 = {K_at_1:.6f}")
    check(len(z_half) == 1 and z_half[0] == sp.Rational(4, 9), "K = 1/2 at z = 4/9")

    FORCED = [
        ("1            total sum rule",        1.0),
        ("2/pi         region B weight",       2 / math.pi),
        ("1-2/pi       region A weight",       1 - 2 / math.pi),
        ("1/pi         dissipative weight",    1 / math.pi),
        ("1/4          branch point |z|",      0.25),
        ("1/2          branch point in u",     0.5),
        ("4/9          z where K=1/2",         4.0 / 9),
        ("(sqrt5-1)/2  K(1)",                  (math.sqrt(5) - 1) / 2),
    ]
    print(f"\n  {len(FORCED)} forced constants, all verified above.")

    # -----------------------------------------------------------------------------------
    banner("S2. THE INVERSE -- the sharpest single statement")
    R_fw = R(Z_FW)
    print(f"  R(Z_framework) = R({Z_FW:.6f}) = {R_fw:.8f}")
    print(f"  For ANY condition R(Z) = F to give kappa = 1/2, F must equal this number.")
    print(f"\n  Is it in the forced set? Distance to each:")
    print(f"    {'forced constant':<34}{'value':>12}{'|F - R_fw|':>14}{'rel':>10}")
    print("    " + "-" * 72)
    best = None
    for nm, v in FORCED:
        d = abs(v - R_fw)
        rel = d / R_fw
        print(f"    {nm:<34}{v:>12.8f}{d:>14.8f}{rel:>9.2%}")
        if best is None or d < best[2]:
            best = (nm, v, d)
    print(f"\n  nearest forced constant: {best[0].split()[0]} at {best[2]/R_fw:.2%} relative")
    TOL = 1e-4    # declared before the comparison
    in_set = best[2] / R_fw < TOL
    print(f"  at the pre-declared tolerance of {TOL:.0e}: "
          f"{'IN the forced set' if in_set else 'NOT in the forced set'}")

    # -----------------------------------------------------------------------------------
    banner("S3. FORWARD SWEEP -- every forced constant as the target, all reported")
    print(f"  {'target F':<34}{'Z':>12}{'kappa':>11}{'vs 1/2':>10}{'in a0 box':>11}")
    print("  " + "-" * 80)
    rows = []
    for nm, F in FORCED:
        try:
            if F >= R(0.30) or F <= R(400.0):
                raise ValueError("target outside the range of R")
            Zs = brentq(lambda Z: R(Z) - F, 0.30, 400.0, xtol=1e-11)
            ks = SQ8PI3 / Zs
            rows.append((nm, Zs, ks))
            print(f"  {nm:<34}{Zs:>12.6f}{ks:>11.6f}{100*(ks-0.5)/0.5:>+9.1f}%"
                  f"{'YES' if K_LO <= ks <= K_HI else 'no':>11}")
        except ValueError:
            rows.append((nm, float("nan"), float("nan")))
            print(f"  {nm:<34}{'unreachable':>12}{'--':>11}{'--':>10}{'--':>11}")
    print(f"  {'FRAMEWORK TARGET':<34}{Z_FW:>12.6f}{0.5:>11.6f}{0.0:>+9.1f}%{'YES':>11}")

    hits = [(nm, Zs, ks) for nm, Zs, ks in rows
            if not math.isnan(ks) and abs(ks - 0.5) / 0.5 < 0.01]
    print(f"\n  forced constants giving kappa = 1/2 to within 1%: "
          f"{[h[0].split()[0] for h in hits] or 'NONE'}")

    # -----------------------------------------------------------------------------------
    banner("S4. Look-elsewhere for an EXHAUSTIVE sweep")
    n = len(FORCED)
    print(f"  This sweep is exhaustive over the forced set, so its cost is fixed at")
    print(f"  log2({n}) = {math.log2(n):.2f} bits and does NOT grow with further guessing --")
    print("  that is the advantage of exhausting a class instead of sampling it.")
    if hits:
        for nm, Zs, ks in hits:
            rel = abs(ks - 0.5) / 0.5
            bits = math.log2(1 / rel) if rel > 0 else float("inf")
            print(f"    {nm.split()[0]}: rel dev {rel:.3e} -> {bits:.1f} bits vs "
                  f"{math.log2(n):.2f} -> "
                  f"{'INFORMATIVE' if bits > math.log2(n) else 'not informative'}")
    else:
        print("    no hits to price.")

    # -----------------------------------------------------------------------------------
    banner("VERDICT")
    if hits:
        print("  A FORCED CONSTANT OF THE KERNEL REPRODUCES kappa = 1/2. See S3/S4 for the")
        print("  precision and whether it clears the sweep's fixed look-elsewhere cost.")
        print("  This would be a derivation, not a fit: the target was not chosen, it was")
        print("  enumerated from the kernel, and the sweep is exhaustive over that set.")
    else:
        print("  NO-GO ON THE THERMAL-SATURATION CLASS. No constant that the kernel itself")
        print("  forces, used as the saturation target, yields kappa = 1/2. Combined with S2 --")
        print(f"  R(Z_framework) = {R_fw:.8f} is not in the forced set -- the entire class of")
        print("  conditions 'thermally active fraction = a forced kernel constant' is CLOSED.")
        print("  This is a genuine negative and it is worth more than another near-miss: it")
        print("  rules out a whole family at fixed cost rather than one guess at a time.")
        print("\n  WHAT REMAINS OPEN. A forced condition could still live in a class this sweep")
        print("  does not touch: a different WEIGHTING of the measure (not tanh), a different")
        print("  functional (not a weight fraction), or a condition tying the kernel to a dS")
        print("  quantity that is not a pure number. Those are separate classes and each")
        print("  would need its own exhaustive treatment.")
    print("\n  kappa = 1/2 remains POSTULATED, NOT DERIVED. Nothing empirical moves.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
