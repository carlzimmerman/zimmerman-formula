#!/usr/bin/env python3
"""mi_three_classes_2026.py -- exhaust the three classes left open by mi_thermal_class_nogo_2026.

STATE OF PLAY. a0 = kappa c sqrt(G rho_Lambda) exactly, so the whole of "32pi/3" is the single
number kappa = 1/2. The spectral weight above the dS frequency is exactly linear in it,
W_above(kappa) = kappa sqrt(3/(8 pi^3)), so any forced spectral condition gives kappa in one
step. Three classes are already closed: local kernel conditions (all scale-invariant),
aesthetic saturation targets, and forced-kernel-constant saturation. Three remain, and each is
exhausted here with a PRE-REGISTERED enumeration so its look-elsewhere cost is fixed rather
than growing with each guess.

  CLASS A -- a different WEIGHTING than tanh. The standard thermal weightings are a closed
      list (each is a textbook factor with a definite physical meaning, not a taste). Applied
      with the ONE forced target established today: the FDT statement that the bath-coupled
      fraction equals the dissipative weight D = 1/pi.

  CLASS B -- a different FUNCTIONAL than a weight fraction. Standard location statistics of
      the inertia-generating measure dmu/|t|: median, geometric mean, arithmetic centroid.
      These need NO target at all -- "the dS frequency IS the median/mean of the spectrum" is
      a zero-parameter statement, which makes them the strongest candidates in the whole
      programme.

  CLASS C -- a condition tying the kernel to a DIMENSIONFUL dS quantity or to the dS entropy.
      Closed by inspection, with the numbers shown: such conditions import S_dS ~ 1e122 or the
      Planck length, and for kappa to be O(1) that dependence must cancel exactly, returning
      to a pure-number condition -- already closed. (The CKN degrees-of-freedom bridge was
      independently closed earlier.)

DISCIPLINE. Every enumeration is fixed in source before evaluation; every member is reported
with whatever it gives; nothing is selected afterward. Near-misses are labelled as near-misses.
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
    print("\n" + "=" * 98); print(s); print("=" * 98)

SQ8PI3     = math.sqrt(8 * math.pi / 3)
KAPPA_FW   = 0.5
Z_FW       = SQ8PI3 / KAPPA_FW                 # 5.788810
K_LO, K_HI = 0.5 / 1.16, 0.5 / 0.84            # +/-16% a0 box in kappa
D_DISS     = 1.0 / math.pi                     # forced dissipative weight (derived 2026-07-29)


def measure_integral(f, lo_u=0.0, hi_u=np.inf):
    """INT f(T) dmu(T) in the committed two-region convention, T = u^2."""
    tot = 0.0
    a, b = max(lo_u, 0.0), min(hi_u, 0.5)
    if b > a:
        tot += quad(lambda u: f(u * u) * (1 - np.sqrt(max(1 - 4 * u * u, 0.0))) / np.pi,
                    a, b, limit=400)[0]
    a, b = max(lo_u, 0.5), hi_u
    if b > a:
        tot += quad(lambda u: f(u * u) / np.pi, a, b, limit=400)[0]
    return tot


def kap(Z):
    return SQ8PI3 / Z


def report_row(nm, Z, extra=""):
    if Z is None or (isinstance(Z, float) and (math.isnan(Z) or Z <= 0)):
        print(f"  {nm:<40}{'--':>12}{'--':>11}{'--':>10}{'--':>10}   {extra}")
        return None
    k = kap(Z)
    inbox = K_LO <= k <= K_HI
    print(f"  {nm:<40}{Z:>12.6f}{k:>11.6f}{100*(k-0.5)/0.5:>+9.1f}%"
          f"{'YES' if inbox else 'no':>10}   {extra}")
    return k


def main() -> int:
    banner("mi_three_classes_2026 -- exhausting the last three classes")
    tot = measure_integral(lambda T: 1.0 / T)
    check(abs(tot - 1.0) < 3e-3, f"committed sum rule INT dmu/|t| = 1 ({tot:.6f})")
    print(f"  target: kappa = 1/2  <=>  Z = {Z_FW:.6f};  a0 box admits kappa in "
          f"[{K_LO:.4f}, {K_HI:.4f}]")

    all_kappas = []

    # ==================================================================================
    banner("CLASS A -- different thermal WEIGHTINGS, one forced target (FDT: = 1/pi)")
    print("  x = hbar omega / k_B T_dS = 2 pi omega / H_Lambda = 2 pi u / Z")
    print("  Condition for every member: weighted fraction of the unit sum rule = D = 1/pi")
    print(f"  (D = {D_DISS:.8f}, the dissipative weight, closed form, derived 2026-07-29)\n")

    WEIGHTS = [
        ("tanh(x/2)  symmetrized KMS",     lambda x: math.tanh(x / 2)),
        ("tanh(x)    variant",             lambda x: math.tanh(x)),
        ("1-exp(-x)  absorption",          lambda x: 1.0 - math.exp(-x)),
        ("exp(-x)    Boltzmann",           lambda x: math.exp(-x)),
        ("x/(e^x-1)  Planck/Debye",        lambda x: 1.0 if x < 1e-12 else x / math.expm1(x)),
        ("x/(e^x+1)  Fermi-like",          lambda x: x / (math.exp(x) + 1.0)),
        ("coth(x/2)  FDT fluctuation",     lambda x: 1.0 / math.tanh(x / 2)),
        ("1/(e^x-1)  Bose occupation",     lambda x: 1.0 / math.expm1(x)),
    ]
    print(f"  {'weighting':<40}{'Z':>12}{'kappa':>11}{'vs 1/2':>10}{'in box':>10}   note")
    print("  " + "-" * 96)
    for nm, w in WEIGHTS:
        def Rw(Z, w=w):
            return measure_integral(lambda T: w(2 * math.pi * math.sqrt(T) / Z) / T)
        # detect divergence at the IR end (u -> 0) by probing a shrinking cutoff
        try:
            probe = [measure_integral(lambda T, w=w: w(2 * math.pi * math.sqrt(T) / 3.0) / T,
                                      lo_u=eps) for eps in (1e-3, 1e-5, 1e-7)]
            diverges = (abs(probe[2]) > 3 * abs(probe[0]) + 1.0) or not np.isfinite(probe[2])
        except Exception:
            diverges = True
        if diverges:
            report_row(nm, None, extra="IR DIVERGENT -> not a valid condition")
            continue
        # bracket and solve Rw(Z) = D
        try:
            lo, hi = 0.30, 400.0
            f_lo, f_hi = Rw(lo) - D_DISS, Rw(hi) - D_DISS
            if f_lo * f_hi > 0:
                report_row(nm, None, extra=f"no root (R spans "
                                           f"[{min(Rw(lo),Rw(hi)):.3f},{max(Rw(lo),Rw(hi)):.3f}])")
                continue
            Zs = brentq(lambda Z: Rw(Z) - D_DISS, lo, hi, xtol=1e-10)
            k = report_row(nm, Zs)
            if k is not None:
                all_kappas.append((f"A: {nm}", k))
        except Exception as e:
            report_row(nm, None, extra=f"failed: {type(e).__name__}")

    # ==================================================================================
    banner("CLASS B -- different FUNCTIONALS: location statistics, ZERO target needed")
    print("  Statement: the de Sitter frequency IS the median / mean of the")
    print("  inertia-generating spectral weight dmu/|t|. No target, no parameters.")
    print("  At omega = H_Lambda the axis coordinate is u = Z, so each statistic's")
    print("  location in u IS the predicted Z.\n")

    # B1 MEDIAN -- solve INT_0^{u_m} dmu/|t| = 1/2, then closed form
    A_weight = measure_integral(lambda T: 1.0 / T, 0.0, 0.5)
    print(f"  region A weight = 1 - 2/pi = {A_weight:.8f} < 1/2, so the median lies in region B")
    um = brentq(lambda U: measure_integral(lambda T: 1.0 / T, 0.0, U) - 0.5, 0.5, 50.0,
                xtol=1e-12)
    print(f"  median location  u_m = {um:.10f}")
    # closed form: (1/pi)(2 - 1/u_m) = 1/2 - (1 - 2/pi)  =>  u_m = 2/pi
    u_sym = sp.Symbol("u_m", positive=True)
    sol = sp.solve(sp.Eq((1 / sp.pi) * (2 - 1 / u_sym), sp.Rational(1, 2) - (1 - 2 / sp.pi)),
                   u_sym)
    print(f"  closed form: u_m = {sol[0]} = {float(sol[0]):.10f}")
    check(abs(um - float(sol[0])) < 1e-8 and sp.simplify(sol[0] - 2 / sp.pi) == 0,
          "median of dmu/|t| sits at u = 2/pi EXACTLY")

    # B2 GEOMETRIC MEAN
    ln_mean = measure_integral(lambda T: math.log(math.sqrt(T)) / T)
    ug = math.exp(ln_mean)
    print(f"  geometric mean   u_g = exp(INT ln(u) dmu/|t|) = {ug:.10f}")

    # B3 ARITHMETIC CENTROID -- check convergence first
    c_probe = [measure_integral(lambda T: math.sqrt(T) / T, 0.0, U) for U in (10, 1e3, 1e5)]
    cent_div = c_probe[2] > 3 * c_probe[0]
    print(f"  arithmetic centroid INT u dmu/|t|: partial sums at u<10, 1e3, 1e5 = "
          f"{c_probe[0]:.4f}, {c_probe[1]:.4f}, {c_probe[2]:.4f}")
    print(f"    -> {'LOG DIVERGENT, not a valid statistic' if cent_div else 'converges'}")

    print(f"\n  {'functional':<40}{'Z':>12}{'kappa':>11}{'vs 1/2':>10}{'in box':>10}   note")
    print("  " + "-" * 96)
    k = report_row("B1 median = dS frequency (u=2/pi exact)", um)
    if k is not None:
        all_kappas.append(("B1 median", k))
    k = report_row("B2 geometric mean = dS frequency", ug)
    if k is not None:
        all_kappas.append(("B2 geometric mean", k))
    report_row("B3 arithmetic centroid = dS frequency", None,
               extra="LOG DIVERGENT" if cent_div else "")

    # ==================================================================================
    banner("CLASS C -- dimensionful / entropic dS quantities: closed by inspection")
    # numbers, so the argument is not hand-waving
    H_L = 1.09e-18          # s^-1, Lambda-only Hubble rate (canonical footing)
    c_l = 2.99792458e8
    G_N = 6.674e-11
    hbar = 1.054571817e-34
    L_p = math.sqrt(hbar * G_N / c_l**3)
    r_H = c_l / H_L
    S_dS = math.pi * (r_H / L_p) ** 2          # A/4L_p^2 with A = 4 pi r_H^2
    print(f"  dS horizon radius r_H = c/H_L      = {r_H:.4e} m")
    print(f"  Planck length      L_p             = {L_p:.4e} m")
    print(f"  dS entropy         S = pi (r_H/L_p)^2 = {S_dS:.4e}")
    print(f"  dS temperature     T_dS            = {hbar*H_L/(2*math.pi*1.380649e-23):.4e} K")
    print("\n  Any condition of the form kappa = F(S_dS) or F(L_p/r_H) imports a number of")
    print(f"  order {S_dS:.0e} or {L_p/r_H:.0e}. For kappa to come out O(1) that dependence must")
    print("  cancel EXACTLY, which returns the condition to a pure-number statement about the")
    print("  kernel -- and that family is already closed (local conditions scale-invariant,")
    print("  aesthetic targets missed, forced-constant saturation NO-GO). If it does NOT")
    print("  cancel, kappa is off by astronomical factors and is excluded by the a0 box at")
    print("  once. Either branch closes the class.")
    print("  Independently: the CKN degrees-of-freedom bridge was already closed -- 0.5878 =")
    print("  (3/8pi)^(1/4) is the g*=1 geometric limit, with no microscopic fix available.")
    check(S_dS > 1e100, f"S_dS is astronomically large ({S_dS:.2e}), as the argument requires")

    # ==================================================================================
    banner("LEDGER -- every member of every enumerated class")
    print(f"  {'member':<44}{'kappa':>11}{'vs 1/2':>11}{'in a0 box':>12}")
    print("  " + "-" * 80)
    for nm, k in all_kappas:
        print(f"  {nm:<44}{k:>11.6f}{100*(k-0.5)/0.5:>+10.1f}%"
              f"{'YES' if K_LO <= k <= K_HI else 'no':>12}")
    print(f"  {'FRAMEWORK TARGET':<44}{0.5:>11.6f}{0.0:>+10.1f}%{'YES':>12}")

    TOL_PCT = 1.0     # declared before inspecting
    hits = [(nm, k) for nm, k in all_kappas if abs(100 * (k - 0.5) / 0.5) < TOL_PCT]
    n_tests = len(all_kappas)
    print(f"\n  members giving kappa = 1/2 to within {TOL_PCT}%: "
          f"{[nm for nm, _ in hits] or 'NONE'}")
    if n_tests:
        print(f"  exhaustive cost of these classes: log2({n_tests}) = "
              f"{math.log2(n_tests):.2f} bits, FIXED")
    for nm, k in hits:
        rel = abs(k - 0.5) / 0.5
        bits = math.log2(1 / rel) if rel > 0 else float("inf")
        print(f"    {nm}: {bits:.1f} bits vs {math.log2(max(n_tests,1)):.2f} -> "
              f"{'INFORMATIVE' if bits > math.log2(max(n_tests,1)) else 'not informative'}")

    banner("VERDICT")
    if hits:
        print("  A member of an exhausted class reproduces kappa = 1/2. See the bits line")
        print("  above for whether it clears the fixed cost of its class.")
    else:
        print("  ALL THREE REMAINING CLASSES CLOSED.")
        print("   * CLASS A: no standard thermal weighting, with the forced FDT target, gives")
        print("     kappa = 1/2. Divergent members are flagged as invalid, not silently")
        print("     dropped.")
        print("   * CLASS B: the strongest candidates in the whole programme, because they")
        print("     need NO target -- and the median of the inertia-generating measure sits")
        print("     at u = 2/pi EXACTLY, a clean closed-form result. It is simply not Z.")
        print("   * CLASS C: closed by inspection either way -- exact cancellation returns to")
        print("     an already-closed pure-number condition; no cancellation puts kappa off")
        print("     by ~1e60.")
        print("\n  Taken with the earlier three closures, the spectral programme is now")
        print("  EXHAUSTED at the level of forced O(1) conditions on the committed kernel.")
        print("  kappa = 1/2 is not derivable from the kernel's spectral structure alone.")
        print("  A derivation must come from OUTSIDE it -- new dynamics, not a new reading")
        print("  of the measure. That is a substantive negative result about where to look,")
        print("  and it is the honest end of this line.")
    print("\n  kappa = 1/2 remains POSTULATED, NOT DERIVED. Nothing empirical moves; a0's")
    print("  value was always postulated and every empirical front is untouched.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
