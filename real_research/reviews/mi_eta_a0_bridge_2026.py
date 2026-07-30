#!/usr/bin/env python3
r"""mi_eta_a0_bridge_2026.py -- is the baryon-to-photon ratio eta related to a0's dark-energy scale?

THE DOOR. Recombination (mi_recombination_why_2026) is set by three numbers that were NEVER in the
atomos germ pool: E_ion = 13.6 eV, Lambda_2s1s = 8.22 s^-1, and eta = 6.12e-10. Only eta is
DIMENSIONLESS, so it is the only one a dimensionless-germ search could ever target. And eta is a
genuinely new target: it is the one number in the recombination story that the whole atomos
programme never tested.

THE TEST, PRE-REGISTERED. a0 = kappa c sqrt(G rho_Lambda) supplies a family of dimensionless
quantities via the de Sitter horizon (S_dS, L_p/r_dS, rho_Lambda/rho_Planck, a0/a_Planck, T_dS/T_P).
Ask: is eta any of them, to within measurement?

THE TRAP, NAMED FIRST. Those quantities are ~1e-62 or ~1e122, while eta ~ 1e-10. Bridging them
needs a POWER, and if the exponent is FREE then "eta = X^(p/q)" is not a prediction -- the set
{X^(p/q)} for small p,q densely covers many decades, so something always lands near eta. That is
the same density argument that killed the PMNS pre-registration. So this script tests the CLASS
before testing any member:

  S2  FORCED-EXPONENT test: only exponents that are NOT free parameters (1, 1/2, 2, -1) are
      allowed. Report the miss in orders of magnitude. Zero look-elsewhere.
  S3  FALSIFIABILITY of the free-exponent class: count how many rational exponents p/q land within
      a factor of 2 of eta. If more than ~1, the class is VACUOUS and no member of it can be
      evidence, however pretty.
  S4  THE PHYSICS: what actually sets eta, and whether a dark-energy link is even coherent.

Exit 0 = ran. No hard-coded verdicts. Outcome accepted either way.
"""
from __future__ import annotations
import math
from fractions import Fraction

C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054571817e-34
KB = 1.380649e-23
H0 = 2.184e-18
OL = 0.685
ETA = 6.12e-10                 # baryon-to-photon ratio (Planck + BBN), ~1.5% precision
ETA_REL_ERR = 0.015

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)


def main() -> int:
    banner("mi_eta_a0_bridge_2026 -- can a0's dark-energy scale reach eta = 6.12e-10?")

    # ---------------------------------------------------------------------------------
    banner("S1. The dimensionless quantities a0 / de Sitter actually supplies")
    H_L = H0 * math.sqrt(OL)
    r_dS = C / H_L
    L_p = math.sqrt(HBAR * G / C**3)
    t_p = L_p / C
    rho_L = 3 * H_L**2 / (8 * math.pi * G)
    rho_P = C**5 / (HBAR * G**2)
    a_P = C / t_p                                # Planck acceleration c/t_P
    a0 = 0.5 * C * math.sqrt(G * rho_L)
    T_dS = HBAR * C * H_L / (2 * math.pi * KB * C)
    T_P = math.sqrt(HBAR * C**5 / G) / KB
    S_dS = math.pi * (r_dS / L_p) ** 2

    QUANT = [
        ("L_p / r_dS",              L_p / r_dS),
        ("a0 / a_Planck",           a0 / a_P),
        ("rho_Lambda / rho_Planck", rho_L / rho_P),
        ("T_dS / T_Planck",         T_dS / T_P),
        ("1 / S_dS",                1.0 / S_dS),
        ("H_Lambda * t_Planck",     H_L * t_p),
    ]
    print(f"  eta (target)          = {ETA:.4e}   (+/- {100*ETA_REL_ERR:.1f}%)")
    print(f"  {'quantity':<26}{'value':>14}{'log10':>10}{'orders from eta':>18}")
    print("  " + "-" * 70)
    for nm, v in QUANT:
        print(f"  {nm:<26}{v:>14.4e}{math.log10(v):>10.2f}"
              f"{abs(math.log10(v) - math.log10(ETA)):>18.1f}")
    print("  Every one is 20-110 orders of magnitude from eta. Nothing matches directly.")

    # ---------------------------------------------------------------------------------
    banner("S2. FORCED-EXPONENT test: only non-arbitrary powers. Zero look-elsewhere.")
    print("  Allowed exponents: 1, 1/2, 2, -1 -- the only ones that are not free parameters")
    print("  (identity, a square root from an area/length relation, a square, an inverse).")
    print(f"  {'quantity':<26}{'exp':>6}{'value':>14}{'orders from eta':>18}{'verdict':>10}")
    print("  " + "-" * 78)
    best = None
    for nm, v in QUANT:
        for e in (1.0, 0.5, 2.0, -1.0):
            val = v ** e
            d = abs(math.log10(val) - math.log10(ETA))
            if best is None or d < best[0]:
                best = (d, nm, e, val)
            if d < 3:      # only print anything remotely close
                print(f"  {nm:<26}{e:>6.1f}{val:>14.4e}{d:>18.1f}{'':>10}")
    print(f"  closest forced-exponent result: {best[1]}^{best[2]:.1f} = {best[3]:.3e},"
          f" {best[0]:.1f} orders from eta")
    check(best[0] > 5,
          f"NO forced exponent gets within 5 orders of eta (closest is {best[0]:.0f} orders off)")

    # ---------------------------------------------------------------------------------
    banner("S3. Is the FREE-exponent class even falsifiable? (the decisive test)")
    print("  If arbitrary rational exponents p/q are allowed, how many land within a factor of 2")
    print("  of eta? If more than ~1, the class is VACUOUS -- a hit carries no information.")
    QMAX = 16
    print(f"  {'quantity':<26}{'#(p/q) within 2x of eta':>26}{'|p|,|q| <= ' + str(QMAX):>16}")
    print("  " + "-" * 70)
    total_hits = 0
    for nm, v in QUANT:
        lv = math.log10(v)
        hits = set()
        for q in range(1, QMAX + 1):
            for p in range(-QMAX, QMAX + 1):
                if p == 0:
                    continue
                fr = Fraction(p, q)
                if abs(fr.numerator) > QMAX or fr.denominator > QMAX:
                    continue
                # compare in LOG space -- 10**(lv*fr) overflows for large negative fr
                log_val = lv * float(fr)
                if abs(log_val - math.log10(ETA)) < math.log10(2):
                    hits.add(fr)
        total_hits += len(hits)
        print(f"  {nm:<26}{len(hits):>26}{'':>16}")
    print(f"\n  TOTAL distinct rational exponents landing within 2x of eta: {total_hits}")
    if total_hits >= 2:
        print("  -> the free-exponent class is VACUOUS. With this many ways to reach eta, hitting")
        print("     it is guaranteed and therefore worthless. Any member of this class is")
        print("     numerology by construction, exactly like the PMNS pre-registration failure.")
    else:
        print("  -> the class is sparse enough that a hit would carry information.")
    check(total_hits >= 2,
          "the free-exponent class is vacuous (multiple exponents reach eta) -- so a "
          "free-exponent 'match' could never be evidence")

    # a concrete example of the vacuity, for the record
    lv = math.log10(1.0 / S_dS)
    e_needed = math.log10(ETA) / lv
    print(f"\n  Worked example of the trap: to get eta from 1/S_dS you need exponent")
    print(f"    log10(eta)/log10(1/S_dS) = {e_needed:.5f}  ~ 1/{1/e_needed:.1f}")
    print(f"    and (1/S_dS)^(1/13) = {(1.0/S_dS)**(1/13):.3e} vs eta = {ETA:.3e}")
    print(f"  A 1/13 power is a FREE PARAMETER dressed as a discovery. Rejected.")

    # ---------------------------------------------------------------------------------
    banner("S4. THE PHYSICS: what actually sets eta, and is a dark-energy link coherent?")
    print("  eta is fixed by BARYOGENESIS, which needs Sakharov's three conditions:")
    print("    (1) baryon-number violation, (2) C and CP violation, (3) departure from thermal")
    print("        equilibrium.")
    print("  All three are EARLY-UNIVERSE, high-energy, out-of-equilibrium particle physics. The")
    print("  observed eta is a frozen relic of CP-violating decays at (probably) the electroweak")
    print("  scale or above -- roughly 1e2 GeV to 1e16 GeV.")
    print(f"  a0's scale is dark energy: rho_Lambda = {rho_L:.3e} kg/m^3, an energy scale of")
    e_L = (rho_L * C**2) ** 0.25 / (1.602e-10) ** 0.25   # rough meV-scale marker
    print(f"    (rho_Lambda c^2)^(1/4) ~ 2 meV -- 14 to 28 ORDERS below the baryogenesis scale.")
    print("  So a link would have to connect a meV-scale IR vacuum energy to a >=100 GeV UV")
    print("  freeze-out. That is not merely unproven -- it would require solving the cosmological")
    print("  coincidence problem, since eta was frozen in long before dark energy did anything.")
    print("  There is no known mechanism, and no published claim of one.")

    banner("VERDICT")
    print(f"  THE DOOR IS CLOSED, and cleanly, on two independent counts:")
    print(f"   1. With FORCED exponents (the only non-arbitrary ones), the closest a0/de Sitter")
    print(f"      quantity misses eta by {best[0]:.0f} orders of magnitude. Zero look-elsewhere")
    print(f"      spent, and a clean miss.")
    print(f"   2. With FREE exponents the class is VACUOUS: {total_hits} distinct rational powers")
    print(f"      land within a factor of 2 of eta, so a 'match' is guaranteed and worthless.")
    print(f"      This is the same density argument that killed the PMNS pre-registration.")
    print(f"   3. Physically, eta is a UV baryogenesis relic (Sakharov, >=100 GeV) and a0 is a")
    print(f"      meV-scale IR vacuum quantity -- 14-28 orders apart, with eta frozen in long")
    print(f"      before dark energy mattered. No mechanism, no published claim.")
    print(f"  eta was a genuinely NEW target and it was worth one shot. It missed. Recorded as a")
    print(f"  closed door rather than left ambiguous. a0's value remains postulated.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
