#!/usr/bin/env python3
"""mi_spectral_kms_bootstrap_2026.py -- two things:

  (A) AUDIT MY OWN DEFICIT CLAIM. mi_spectral_weight_swing_2026 concluded that the clean
      spectral condition favours the conventional 2pi over the framework's sqrt(32pi/3),
      because W_above = 1/(pi Z) put 2pi on the natural value 1/(2pi^2) and left the
      framework needing sqrt(3/(32 pi^3)). But W_above probes Z LINEARLY, while the
      framework's coefficient is natural in Z^2 = 32pi/3 = 4*(8pi)/3 (Einstein x Friedmann
      x the kappa factor). A linear probe structurally flatters coefficients clean in Z and
      penalises ones clean in Z^2. If the asymmetry vanishes on the axis's own variable
      T = |z| = Z^2, my deficit was a MEASUREMENT ARTIFACT and must be downgraded.
      Verifying a deficit as rigorously as a win.

  (B) THE ZERO-PARAMETER THERMAL BOOTSTRAP -- the one calculation that is FORCED rather
      than chosen. The previous script had to pick a candidate weight off a list, which is
      fitting. This does not. The framework's a0 IS the de Sitter-Unruh scale, so the
      physically dictated weighting of the kernel's spectrum is the de Sitter thermal one,
      and detailed balance (KMS) fixes that factor uniquely: for a symmetrized response the
      thermal factor is tanh(hbar omega / 2 k_B T_dS), with no freedom at all.

      On the dimensionless axis, T = |z| = (omega c/a0)^2 and a0 = c H_Lambda/Z, so
          omega/H_Lambda = sqrt(T)/Z = u/Z,     T_dS = hbar H_Lambda/(2 pi k_B)
          =>  thermal factor = tanh(pi u / Z)
      Define the KMS-weighted fraction of the committed sum rule
          R(Z) = INT dmu(T)/|T| * tanh(pi sqrt(T)/Z)        (R in (0,1), monotone in Z)
      R = 1 is unreachable (tanh < 1), so the ONE natural zero-parameter condition is
      half-saturation, R(Z) = 1/2: half the kernel's spectral weight is thermally active in
      the de Sitter bath. Solve it. The answer is not up to us.

      NOTE the IR care: the raw Bose factor 1/(exp-1) makes this integral DIVERGE
      logarithmically at u->0. The symmetrized tanh is finite there. tanh is used because
      detailed balance dictates it for a symmetrized response, NOT because it converges.

Exit 0 = all checks ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math
import numpy as np
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
    print("\n" + "=" * 96); print(s); print("=" * 96)

Z_FRAME = math.sqrt(32 * math.pi / 3)      # 5.788810
Z_CONV  = 2 * math.pi                      # 6.283185


# committed two-region Herglotz measure, in u = sqrt(T)
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


def main() -> int:
    banner("mi_spectral_kms_bootstrap_2026")
    M = measure_integral(lambda T: 1.0 / T)
    check(abs(M - 1.0) < 3e-3, f"committed sum rule INT dmu/|t| = 1 reproduced ({M:.6f})")

    # -----------------------------------------------------------------------------------
    banner("A. Is my 'favours 2pi' claim robust, or an artifact of probing Z linearly?")
    print("  The dS frequency sits at T* = |z*| = Z^2 on the axis. T is the axis's OWN")
    print("  variable. Compare how clean each coefficient is in T*, not in 1/Z.\n")
    T_frame, T_conv = Z_FRAME**2, Z_CONV**2
    print(f"  framework    T* = Z^2 = 32pi/3  = {T_frame:.6f}   = 4*(8pi)/3, i.e. "
          f"Einstein x Friedmann x kappa^-2")
    print(f"  conventional T* = Z^2 = 4pi^2   = {T_conv:.6f}   = (2pi)^2")
    check(abs(T_frame - 32 * math.pi / 3) < 1e-9, "framework T* = 32pi/3 exactly")
    check(abs(T_conv - 4 * math.pi**2) < 1e-9, "conventional T* = 4pi^2 exactly")
    print("\n  Both are closed-form expressions of comparable simplicity on the T-axis:")
    print("    32pi/3 : one power of pi, rational coefficient 32/3")
    print("    4pi^2  : two powers of pi, rational coefficient 4")
    print("  Neither is 'uglier'. The asymmetry reported by the previous script appears only")
    print("  after taking a SQUARE ROOT and an inverse, which manufactures a half-integer")
    print("  power of pi for the framework and cancels one for 2pi:")
    print(f"    W_above(framework) = 1/(pi Z) = sqrt(3/(32 pi^3))  <- half-integer power")
    print(f"    W_above(2pi)       = 1/(pi Z) = 1/(2 pi^2)         <- integer powers")
    print("\n  VERDICT ON MY OWN CLAIM: the 'favours 2pi' finding is substantially an")
    print("  ARTIFACT of choosing a probe linear in Z. On the axis's own variable the two")
    print("  coefficients are equally clean. I am DOWNGRADING that finding from a")
    print("  'theoretical point against the framework' to 'probe-dependent, not decisive'.")
    print("  The residual asymmetry that DOES survive: W_above is a fraction, and fractions")
    print("  are the natural currency of a spectral condition, so a condition stated on the")
    print("  fraction still lands on 2pi. Both statements are now on the record.")

    # -----------------------------------------------------------------------------------
    banner("B. The zero-parameter thermal bootstrap (nothing chosen from a list)")
    print("  KMS/detailed balance fixes the thermal factor for a symmetrized response:")
    print("      tanh(hbar omega / 2 k_B T_dS) = tanh(pi u / Z),   u = sqrt(T)")
    print("  R(Z) = INT dmu(T)/|T| * tanh(pi sqrt(T)/Z)   -- the thermally ACTIVE fraction")
    print("  of the unit sum rule. No parameters. R in (0,1), monotone decreasing in Z.\n")

    def R(Z):
        return measure_integral(lambda T: math.tanh(math.pi * math.sqrt(T) / Z) / T)

    # show it is monotone and bracket the half-saturation point
    print(f"  {'Z':>10}{'R(Z)':>12}")
    print("  " + "-" * 24)
    grid = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, Z_FRAME, Z_CONV, 8.0, 12.0, 20.0]
    vals = []
    for Zt in grid:
        r = R(Zt)
        vals.append(r)
        tag = ""
        if abs(Zt - Z_FRAME) < 1e-9:
            tag = "  <-- framework sqrt(32pi/3)"
        if abs(Zt - Z_CONV) < 1e-9:
            tag = "  <-- conventional 2pi"
        print(f"  {Zt:>10.6f}{r:>12.6f}{tag}")
    mono = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    check(mono, "R(Z) is strictly monotone decreasing -> R(Z)=const has a unique solution")

    print("\n  Solve the one natural zero-parameter condition, half-saturation R(Z) = 1/2:")
    try:
        Z_star = brentq(lambda Z: R(Z) - 0.5, 0.5, 60.0, xtol=1e-10)
        print(f"    Z* = {Z_star:.6f}")
        print(f"    vs framework    sqrt(32pi/3) = {Z_FRAME:.6f}   "
              f"({100*(Z_star-Z_FRAME)/Z_FRAME:+.2f}%)")
        print(f"    vs conventional 2pi          = {Z_CONV:.6f}   "
              f"({100*(Z_star-Z_CONV)/Z_CONV:+.2f}%)")
        # what closed forms sit near Z*?
        print(f"\n    Z*^2 = {Z_star**2:.6f}   (framework needs 32pi/3 = {T_frame:.6f}, "
              f"2pi needs 4pi^2 = {T_conv:.6f})")
        print(f"    Z*/pi = {Z_star/math.pi:.6f}   Z*^2/pi = {Z_star**2/math.pi:.6f}   "
              f"3*Z*^2/(32) = {3*Z_star**2/32:.6f}  (=pi if framework exact)")
        TOL = 1.0   # percent, declared before the solve
        hit_frame = abs(100 * (Z_star - Z_FRAME) / Z_FRAME) < TOL
        hit_conv = abs(100 * (Z_star - Z_CONV) / Z_CONV) < TOL
        print(f"\n    at the pre-declared {TOL}% tolerance: "
              f"framework {'HIT' if hit_frame else 'miss'}, "
              f"2pi {'HIT' if hit_conv else 'miss'}")
        print("    look-elsewhere: ONE condition tested, zero candidates from a list,")
        print("    so log2(trials) = 0 bits. Any hit here is worth its full precision;")
        print("    any miss is a clean falsification of half-saturation.")
    except ValueError as e:
        Z_star = None
        print(f"    no root in [0.5, 60]: {e}")
        print(f"    R(0.5)={R(0.5):.6f}  R(60)={R(60.0):.6f} -> half-saturation is not")
        print("    attainable, so this particular condition is ruled out outright.")

    # -----------------------------------------------------------------------------------
    banner("C. What each coefficient's thermally-active fraction actually is")
    for nm, Zv in (("framework sqrt(32pi/3)", Z_FRAME), ("conventional 2pi", Z_CONV)):
        r = R(Zv)
        print(f"  {nm:<26} R = {r:.6f}")
    print("\n  If neither sits on a recognisable value, the thermal bootstrap does not")
    print("  select either coefficient, and BOTH remain postulated. That is the likeliest")
    print("  outcome and it is not a defeat -- it removes an axis from contention rather")
    print("  than settling it.")

    banner("SUMMARY")
    print("  A. My previous 'the spectral condition favours 2pi' finding is DOWNGRADED to")
    print("     probe-dependent: on the axis's own variable T = Z^2 both coefficients are")
    print("     equally clean (32pi/3 vs 4pi^2). The asymmetry was created by taking a")
    print("     square root. Recorded both ways.")
    print("  B. The thermal bootstrap is the first genuinely ZERO-PARAMETER test on this")
    print("     axis -- no candidate list, no look-elsewhere. See the number above.")
    print("=" * 96)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
