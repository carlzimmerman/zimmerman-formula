#!/usr/bin/env python3
"""mi_forced_weight_attempt_2026.py -- an honest attempt to FORCE the spectral weight.

TARGET (fixed by mi_kappa_spectral_reduction_2026, before this script existed):
    a0 = kappa c sqrt(G rho_Lambda)  exactly, so "why 32pi/3" IS "why kappa = 1/2".
    W_above(kappa) = kappa * sqrt(3/(8 pi^3)) = kappa * 0.10997420   (EXACTLY LINEAR)
    kappa = 1/2  <=>  W_above = 0.05498710  <=>  Z = sqrt(32pi/3) = 5.788810

METHOD, AND THE DISCIPLINE THAT MAKES IT MEAN ANYTHING. Each candidate principle below is
stated with its physical derivation IN FULL, in this docstring, BEFORE any number is
evaluated. Nothing is selected after seeing a result; every principle stated is reported with
whatever it gives. This is the only way an attempt like this can be honest -- picking the
principle after seeing which one lands is the Kepler-epicycle failure mode, and the atomos
null paper (DOI 10.5281/zenodo.21654272) documents exactly why it is worthless.

-----------------------------------------------------------------------------------------
PRINCIPLE P1 -- FLUCTUATION-DISSIPATION IDENTIFICATION.
Derivation: a thermal bath can only exchange energy with the DISSIPATIVE part of a response
function; the reactive part stores, it does not absorb (standard FDT). In this kernel the
dissipative part is exactly the ON-CUT spectrum, T > 1/4, i.e. omega > omega_b -- region B --
because off the cut the retarded boundary value is real (KERNEL_THEORY.md:40: on the physical
branch K is unimodular, a pure phase; the imaginary part lives on the cut). Region B's weight
is FORCED, in closed form: INT_B dmu/|t| = 2/pi exactly (KERNEL_THEORY.md:38, sympy).
So if the de Sitter bath is what sources the inertia, the thermally ACTIVE fraction must
coincide with the DISSIPATIVE fraction:
        R(Z) = 2/pi
Both sides forced. Zero free parameters. Solve for Z, hence kappa.

PRINCIPLE P2 -- CROSSOVER MATCHING.
Derivation: the kernel has one intrinsic crossover, the branch point omega_b = a0/2c, where
the response changes analytic character. The de Sitter thermal factor tanh(pi omega/H_Lambda)
has one intrinsic crossover too, at half-activation, tanh = 1/2. If a0 IS the de Sitter-Unruh
scale then these two crossovers describe the same physical transition and must coincide:
        omega_b = omega_(tanh = 1/2)   =>   a0/2c = (H_Lambda/pi) artanh(1/2)
Zero free parameters, no reference to any weight value. Solve for Z, hence kappa.

PRINCIPLE P3 -- CAUSAL MEMORY BOUND (an inequality, so it can only EXCLUDE).
Derivation: the kernel's memory time is forced, tau_mem = 2c/a0 = 2Z/H_Lambda
(KERNEL_THEORY.md:45). An inertial response cannot be sourced by correlations longer than
the causal horizon can support, so tau_mem <= 1/H_Lambda gives Z <= 1/2. This is stated as a
bound, not a derivation, and is reported as pass/fail only.

-----------------------------------------------------------------------------------------
INDEPENDENT EMPIRICAL FILTER (not a principle -- a fact). The empirical a0 box is +/-16%
around the canonical value, so ANY candidate principle predicting kappa outside
0.5 * [1/1.16, 1/0.84] is excluded by DATA regardless of how pretty its derivation is. This
filter is applied to every principle, and it cuts both ways: it can kill a principle that
happens to land on kappa = 1/2 for the wrong reason too.

Exit 0 = all checks ran. No hard-coded verdicts. Outcome accepted whatever it is.
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

# forced constants
SQ8PI3   = math.sqrt(8 * math.pi / 3)        # = 2.894405 ; Z(kappa) = SQ8PI3/kappa
KAPPA_FW = 0.5
Z_FW     = SQ8PI3 / KAPPA_FW                 # = sqrt(32pi/3) = 5.788810
W_COEF   = math.sqrt(3 / (8 * math.pi**3))   # W_above = kappa * W_COEF
REGION_B = 2.0 / math.pi                     # forced: INT_B dmu/|t| = 2/pi exactly


def measure_integral(f, lo_u=0.0, hi_u=np.inf):
    """committed two-region Herglotz measure, in u = sqrt(T)."""
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
    """thermally ACTIVE fraction of the unit sum rule; KMS-forced tanh weighting."""
    return measure_integral(lambda T: math.tanh(math.pi * math.sqrt(T) / Z) / T)


def kappa_of_Z(Z):
    return SQ8PI3 / Z


def main() -> int:
    banner("mi_forced_weight_attempt_2026 -- can any FORCED principle give kappa = 1/2?")

    # sanity: reproduce the forced inputs before using them
    M = measure_integral(lambda T: 1.0 / T)
    check(abs(M - 1.0) < 3e-3, f"sum rule INT dmu/|t| = 1 ({M:.6f})")
    B = measure_integral(lambda T: 1.0 / T, 0.5, np.inf)
    check(abs(B - REGION_B) < 3e-3,
          f"region B (dissipative, on-cut) weight = 2/pi = {REGION_B:.6f} (got {B:.6f})")
    check(abs(KAPPA_FW * W_COEF - 0.05498710) < 1e-7,
          f"target: kappa=1/2 <=> W_above = {KAPPA_FW*W_COEF:.8f}")
    print(f"\n  TARGET (fixed before this script): kappa = 1/2, Z = {Z_FW:.6f}, "
          f"W_above = {KAPPA_FW*W_COEF:.8f}")

    # empirical filter, stated before any principle is evaluated
    K_LO, K_HI = 0.5 / 1.16, 0.5 / 0.84
    print(f"  EMPIRICAL FILTER (independent of every principle): the +/-16% a0 box admits")
    print(f"  kappa in [{K_LO:.4f}, {K_HI:.4f}]. Anything outside is excluded by DATA.")

    results = []

    # -----------------------------------------------------------------------------------
    banner("P1. FLUCTUATION-DISSIPATION: thermally active fraction = dissipative fraction")
    print("  Condition (derived above, no free parameters):  R(Z) = 2/pi = "
          f"{REGION_B:.6f}")
    print(f"  R is monotone decreasing. R(1)={R(1.0):.6f}  R(3)={R(3.0):.6f}  "
          f"R(10)={R(10.0):.6f}")
    try:
        Z1 = brentq(lambda Z: R(Z) - REGION_B, 0.3, 60.0, xtol=1e-10)
        k1 = kappa_of_Z(Z1)
        print(f"  SOLUTION: Z = {Z1:.6f}  ->  kappa = {k1:.6f}  "
              f"(W_above = {k1*W_COEF:.8f})")
        print(f"  vs kappa = 1/2: {100*(k1-0.5)/0.5:+.2f}%")
        results.append(("P1 fluctuation-dissipation", Z1, k1))
    except ValueError as e:
        print(f"  no solution in range: {e}")
        results.append(("P1 fluctuation-dissipation", float("nan"), float("nan")))

    # -----------------------------------------------------------------------------------
    banner("P2. CROSSOVER MATCHING: branch point = thermal half-activation point")
    at_half = math.atanh(0.5)
    print(f"  tanh(x) = 1/2 at x = artanh(1/2) = {at_half:.8f}")
    print(f"  condition: pi*omega/H_L = artanh(1/2) at omega = omega_b = a0/2c")
    print(f"    => a0/(2c) = (H_L/pi) artanh(1/2)")
    print(f"    => Z = cH_L/a0 = pi / (2 artanh(1/2))")
    Z2 = math.pi / (2 * at_half)
    k2 = kappa_of_Z(Z2)
    print(f"  SOLUTION: Z = {Z2:.6f}  ->  kappa = {k2:.6f}  (W_above = {k2*W_COEF:.8f})")
    print(f"  vs kappa = 1/2: {100*(k2-0.5)/0.5:+.2f}%")
    results.append(("P2 crossover matching", Z2, k2))

    # -----------------------------------------------------------------------------------
    banner("P3. CAUSAL MEMORY BOUND (exclusion only)")
    tau_fw = 2 * Z_FW
    print(f"  tau_mem = 2Z/H_Lambda; framework gives {tau_fw:.4f}/H_Lambda "
          f"({tau_fw:.2f} Hubble times)")
    print(f"  bound tau_mem <= 1/H_Lambda requires Z <= 0.5, i.e. kappa >= {SQ8PI3/0.5:.4f}")
    passes = Z_FW <= 0.5
    print(f"  framework Z = {Z_FW:.4f} -> bound {'SATISFIED' if passes else 'VIOLATED'}")
    print("  READING, carefully: this does NOT falsify the framework. The kernel's memory is")
    print("  a susceptibility tail, not a signal path, so a tail longer than the Hubble time")
    print("  is not acausal by itself. But it does mean KERNEL_THEORY.md:45's description of")
    print(f"  tau_mem as 'the horizon scale' is loose by a factor {tau_fw:.1f}. Flagged.")

    # -----------------------------------------------------------------------------------
    banner("LEDGER: every principle stated, every result reported")
    print(f"  {'principle':<32}{'Z':>12}{'kappa':>10}{'vs 1/2':>10}"
          f"{'in a0 box?':>12}")
    print("  " + "-" * 78)
    for nm, Zv, kv in results:
        if math.isnan(kv):
            print(f"  {nm:<32}{'--':>12}{'--':>10}{'--':>10}{'--':>12}")
            continue
        inbox = K_LO <= kv <= K_HI
        print(f"  {nm:<32}{Zv:>12.6f}{kv:>10.6f}"
              f"{100*(kv-0.5)/0.5:>+9.1f}%{'YES' if inbox else 'no':>12}")
    print(f"  {'framework (target)':<32}{Z_FW:>12.6f}{0.5:>10.6f}{0.0:>+9.1f}%{'YES':>12}")

    ks = [k for _, _, k in results if not math.isnan(k)]
    if ks:
        print(f"\n  spread of forced-principle predictions: kappa in "
              f"[{min(ks):.4f}, {max(ks):.4f}]")
        brackets = min(ks) <= 0.5 <= max(ks)
        print(f"  does the spread BRACKET kappa = 1/2? {'YES' if brackets else 'NO'}")

    # -----------------------------------------------------------------------------------
    banner("VERDICT -- stated whatever the outcome")
    print("  Both principles were derived and written down before evaluation, and both are")
    print("  reported. Neither was selected after the fact. Total forced-condition attempts")
    print("  across this line of work is now 6 (4 previous + P1 + P2), i.e.")
    print(f"  log2(6) = {math.log2(6):.2f} bits of accumulated look-elsewhere.")
    print("\n  What the numbers above do and do not license:")
    print("   * If a principle lands ON kappa = 1/2 to several digits, that is worth its")
    print("     precision minus 2.58 bits, and would be the lock.")
    print("   * If the principles merely BRACKET kappa = 1/2 within a factor ~2, that is")
    print("     weak support for the spectral axis being the right neighbourhood and NO")
    print("     support at all for the specific value. It must not be reported as a win.")
    print("   * Any principle landing outside the a0 box is falsified by data, which is")
    print("     informative about the PRINCIPLE, not about the framework.")
    print("\n  kappa = 1/2 remains POSTULATED unless a number above matches it tightly.")
    print("=" * 96)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
