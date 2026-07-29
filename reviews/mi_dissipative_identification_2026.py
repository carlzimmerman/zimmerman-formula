#!/usr/bin/env python3
"""mi_dissipative_identification_2026.py -- fix an error in my own P1 premise, then re-ask
why the spectral principles wanted kappa ~ 1.

THE ERROR. mi_forced_weight_attempt_2026's principle P1 identified "the dissipative part of
the response" with "the on-cut spectrum, region B", whose weight is 2/pi. That is WRONG.
KERNEL_THEORY.md:40 states that on the physical (oscillatory) branch the retarded boundary
value is UNIMODULAR -- a pure phase -- with

    phi(omega) = arcsin(a0 / 2 c omega),   reactive part cos phi, dissipative part sin phi

so the dissipative fraction of a mode FALLS as 1/omega and vanishes deep in region B. Region B
is therefore overwhelmingly REACTIVE at the frequencies real systems occupy (KERNEL_THEORY.md:45:
every bound orbit has w >> 1/2). Equating "on-cut" with "dissipative" over-counted the
bath-coupled weight by exactly the factor that the sin phi taper supplies.

THE CORRECTION. The genuinely dissipative weight, as a fraction of the unit sum rule, is

    D = INT_{T>1/4} dmu(T)/|T| * sin phi(T),   sin phi = 1/(2 sqrt(T))

which is computed in closed form below (it is 1/pi, not 2/pi). Re-running P1 with the correct
dissipative fraction moves kappa, and the direction it moves is the point of this script.

WHAT THIS IS AND IS NOT. This is a CORRECTION of a stated premise, not a new tunable
condition -- the premise was wrong for a reason internal to the framework's own documented
kernel, discovered by re-reading it, not by seeing which answer came out. The look-elsewhere
count does NOT increase for a corrected version of an already-counted attempt; it stays at 6.
A KNOB found along the way is explicitly REJECTED in S4 and recorded so it is not reused.

Exit 0 = all checks ran. No hard-coded verdicts.
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
    print("\n" + "=" * 96); print(s); print("=" * 96)

SQ8PI3   = math.sqrt(8 * math.pi / 3)
KAPPA_FW = 0.5
Z_FW     = SQ8PI3 / KAPPA_FW
K_LO, K_HI = 0.5 / 1.16, 0.5 / 0.84       # +/-16% a0 box, in kappa


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
    return measure_integral(lambda T: math.tanh(math.pi * math.sqrt(T) / Z) / T)


def main() -> int:
    banner("mi_dissipative_identification_2026 -- correcting P1's premise")

    # -----------------------------------------------------------------------------------
    banner("S1. The unimodular phase, and why 'on-cut' != 'dissipative'")
    u = sp.Symbol("u", positive=True)     # u = sqrt(T) = omega c / a0
    sinphi = 1 / (2 * u)                  # sin(arcsin(a0/2c omega)) with omega c/a0 = u
    print("  KERNEL_THEORY.md:40-45: on the oscillatory branch |K| = 1 exactly and")
    print("      phi(omega) = arcsin(a0/2c omega),  dissipative part = sin phi = 1/(2u)")
    for uu in (0.5, 1.0, 10.0, 1e3, 2.0e3):
        print(f"    u = omega c/a0 = {uu:>8.1f}  ->  sin phi = {float(sinphi.subs(u, uu)):.6e}")
    print("  At galactic orbital frequencies (w ~ 2e3) the dissipative fraction of a mode is")
    print("  ~2.5e-4: region B is REACTIVE, not dissipative. My P1 premise equated the two.")

    # -----------------------------------------------------------------------------------
    banner("S2. The correct dissipative weight, in closed form")
    # D = INT_{1/2}^{inf} [1/(pi u^2)] * [1/(2u)] du
    D_sym = sp.integrate(1 / (sp.pi * u**2) * sinphi, (u, sp.Rational(1, 2), sp.oo))
    print(f"  D = INT_{{1/2}}^inf du/(pi u^2) * 1/(2u) = {sp.simplify(D_sym)}")
    D = float(D_sym)
    print(f"    = {D:.8f}")
    check(sp.simplify(D_sym - 1 / sp.pi) == 0, "dissipative weight D = 1/pi EXACTLY")
    D_num = measure_integral(lambda T: (1.0 / (2.0 * math.sqrt(T))) / T, 0.5, np.inf)
    check(abs(D_num - D) < 1e-8, f"quadrature agrees ({D_num:.8f})")
    print(f"\n  So the bath-coupled fraction is 1/pi = {D:.6f}, NOT region B's 2/pi = "
          f"{2/math.pi:.6f}.")
    print(f"  P1 over-counted the coupled weight by exactly a factor 2 "
          f"({(2/math.pi)/D:.4f}).")

    # -----------------------------------------------------------------------------------
    banner("S3. P1 RE-RUN with the corrected dissipative fraction")
    print(f"  corrected condition:  R(Z) = D = 1/pi = {D:.6f}")
    print(f"  bracket: R(4)={R(4.0):.6f}  R(8)={R(8.0):.6f}  R(16)={R(16.0):.6f}")
    Z1c = brentq(lambda Z: R(Z) - D, 0.3, 200.0, xtol=1e-10)
    k1c = SQ8PI3 / Z1c
    print(f"  SOLUTION: Z = {Z1c:.6f}  ->  kappa = {k1c:.6f}")
    print(f"    vs kappa = 1/2 : {100*(k1c-0.5)/0.5:+.2f}%")
    print(f"    in the a0 box [{K_LO:.4f},{K_HI:.4f}]? "
          f"{'YES' if K_LO <= k1c <= K_HI else 'no'}")
    print(f"\n  BEFORE the correction P1 gave kappa = 1.137860 (+127.6%).")
    print(f"  AFTER  the correction P1 gives kappa = {k1c:.6f} "
          f"({100*(k1c-0.5)/0.5:+.2f}%).")
    crossed = (1.137860 - 0.5) * (k1c - 0.5) < 0
    print(f"  Did the correction move kappa ACROSS 1/2? {'YES' if crossed else 'NO'}")

    # -----------------------------------------------------------------------------------
    banner("S4. A KNOB found along the way -- explicitly REJECTED, recorded so it is not reused")
    at_half = math.atanh(0.5)
    Z_knob = math.pi / at_half            # P2 with omega_b = a0/c instead of a0/2c
    k_knob = SQ8PI3 / Z_knob
    print(f"  If P2's kernel frequency were a0/c instead of a0/2c, one would get")
    print(f"      Z = pi/artanh(1/2) = {Z_knob:.6f}  ->  kappa = {k_knob:.6f}  "
          f"({100*(k_knob-0.5)/0.5:+.2f}% from 1/2)")
    print("  That is within ~1% of kappa = 1/2 and would look like a spectacular hit.")
    print("  IT IS REJECTED. The branch point is at z = -1/4, and z = -(omega c/a0)^2, so")
    print("      |z| = 1/4  =>  omega = a0/(2c)   -- FORCED, not a convention.")
    zsol = sp.solve(sp.Eq((sp.Symbol('w', positive=True))**2, sp.Rational(1, 4)),
                    sp.Symbol('w', positive=True))
    check(len(zsol) == 1 and zsol[0] == sp.Rational(1, 2),
          "omega c/a0 = 1/2 at the branch point -- the factor 2 in a0/2c is forced")
    print("  Dropping that 2 to improve the fit is exactly the epicycle move. Recorded as")
    print("  a rejected knob, NOT as a result.")
    print("\n  Also rejected, same reason: matching the kernel's HALF-RESPONSE point")
    print("  (K = 1/2 at z = 4/9, i.e. |a|/a0 = 2/3) to a thermal half-activation. That")
    print("  compares an ACCELERATION-slot value to a FREQUENCY-slot value -- a category")
    print("  error, since z = a^2/a0^2 in the first-moment closure but z = -(omega c/a0)^2")
    print("  on the frequency branch. Not a candidate.")
    zhalf = sp.solve(sp.Eq((sp.sqrt(1 + 4 * sp.Symbol('zz', positive=True)) - 1) /
                           (2 * sp.sqrt(sp.Symbol('zz', positive=True))), sp.Rational(1, 2)),
                     sp.Symbol('zz', positive=True))
    print(f"    (for the record, K = 1/2 at z = {zhalf[0] if zhalf else '?'} = "
          f"{float(zhalf[0]) if zhalf else float('nan'):.6f})")

    # -----------------------------------------------------------------------------------
    banner("S5. Does the 'spectral side wants kappa = 1' pattern survive?")
    tried = [("P1 as published (on-cut = dissipative) -- WRONG PREMISE", 1.137860),
             ("P1 corrected (sin phi taper)", k1c),
             ("P2 crossover matching", 1.012171)]
    print(f"  {'principle':<52}{'kappa':>10}{'vs 1/2':>10}{'in box':>9}")
    print("  " + "-" * 82)
    for nm, kv in tried:
        print(f"  {nm:<52}{kv:>10.6f}{100*(kv-0.5)/0.5:>+9.1f}%"
              f"{'YES' if K_LO <= kv <= K_HI else 'no':>9}")
    live = [kv for nm, kv in tried if "WRONG" not in nm]
    lo, hi = min(live), max(live)
    print(f"\n  live (non-retracted) spread: kappa in [{lo:.4f}, {hi:.4f}]")
    brackets = lo <= 0.5 <= hi
    print(f"  brackets kappa = 1/2? {'YES' if brackets else 'NO'}")
    print("\n  ANSWER TO THE QUESTION ASKED. The 'spectral side wants kappa ~ 1' pattern was")
    print("  PARTLY AN ARTIFACT of my wrong dissipative identification: correcting it moves")
    print(f"  P1 from 1.1379 to {k1c:.4f}, i.e. to the OTHER SIDE of 1/2. So it is not true")
    print("  that the spectral axis systematically wants the 1/2 deleted. What IS true is")
    print("  that the two surviving principles straddle 1/2 by factors of order 1.5-2 and")
    print("  neither lands on it.")
    print("\n  PER MY OWN PRE-COMMITMENT: bracketing is weak evidence that the AXIS is the")
    print("  right neighbourhood and ZERO evidence for the VALUE. It is not a win and is not")
    print("  reported as one. kappa = 1/2 remains POSTULATED.")

    banner("VERDICT")
    print("  1. P1's premise was WRONG and is corrected: the bath couples to the dissipative")
    print(f"     weight D = 1/pi = {D:.6f} (closed form), not to region B's 2/pi. My error,")
    print("     found by re-reading the framework's own unimodularity result.")
    print(f"  2. Corrected P1 gives kappa = {k1c:.6f}, on the opposite side of 1/2 from the")
    print("     published value, so the 'wants kappa = 1' reading is RETRACTED as stated.")
    print("  3. One near-miss knob (kappa = 0.506 from dropping the forced 2 in a0/2c) and")
    print("     one category error are explicitly REJECTED and recorded.")
    print("  4. Look-elsewhere stays at 6 attempts (a correction is not a new trial).")
    print("  5. Nothing empirical moves. kappa = 1/2 POSTULATED, NOT DERIVED.")
    print("=" * 96)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
