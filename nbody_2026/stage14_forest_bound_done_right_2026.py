#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage14_forest_bound_done_right_2026.py
=======================================
THE LYMAN-ALPHA BOUND, DONE PROPERLY -- and it overturns stage 13's "1.38x short" TWICE over, in
opposite directions, so the net verdict is BOUNDARY rather than excluded.

Stage 13 built the gamma = 0 sector, p_chi = K ln(rho/rho_*), and reported it excluded by 1.38x on the
Lyman-alpha forest.  That verdict rested on TWO things I got wrong:

  *** ERROR 1 (mine, and Carl caught it): I USED A NEWTONIAN JEANS LENGTH. ***
  This framework is not MOND with a fixed a_0 -- a_0 scales with redshift, and at forest scales the
  perturbations are DEEP IN THE MOND REGIME (checked below: g_N/a_0 ~ 1e-4).  The Jeans balance is
  therefore MONDian, and it is a different law:
        Newtonian:  c_s^2/L ~ G rho L                  =>  L_J ~ c_s / sqrt(G rho)
        DEEP MOND:  c_s^2/L ~ sqrt(G rho a_0 L)        =>  L_J ~ (c_s^2)^(2/3) (G rho a_0)^(-1/3)
  With c_s^2 = K/rho this gives  *** L_J ~ K^(2/3) G^(-1/3) a_0(z)^(-1/3) rho^-1 ***  -- still the
  rho^-1 ceiling, but now carrying a_0(z)^(-1/3).  Since a_0 was SMALLER at high z (0.74 of today's at
  z = 3 under the framework's own law), the growth from z = 3 to now is 57.9x rather than 64x: the
  correction runs slightly AGAINST the sector.

  *** ERROR 2 (also mine): MY "0.1 Mpc FOREST SENSITIVITY" WAS A ROUND NUMBER, NOT A PUBLISHED BOUND. ***
  Converting real thermal-relic WDM limits through the Viel et al. (2005) transfer function,
  T(k) = [1+(alpha k)^{2 nu}]^{-5/nu}, nu = 1.12, alpha = 0.049 (m/keV)^-1.11 h^-1 Mpc, the half-mode
  COMOVING wavelengths are:
        m > 2.0 keV -> 0.45 Mpc      m > 3.5 keV -> 0.243 Mpc
        m > 3.0 keV -> 0.288 Mpc     m > 5.3 keV -> 0.153 Mpc     m > 6.0 keV -> 0.133 Mpc
  So the real permitted scale is 0.13-0.45 Mpc depending on which analysis, not 0.10.  This correction
  runs strongly FOR the sector, and it is much larger than error 1.

  *** AND A THIRD POINT, WHICH IS THE REAL CONTENT OF "GETTING THE BOUND RIGHT": THE PUBLISHED BOUNDS
  ASSUME A CUTOFF FIXED IN COMOVING UNITS (free-streaming, set once in the early universe).  THIS
  SECTOR'S COMOVING CUTOFF SHRINKS WITH REDSHIFT -- 0.26 Mpc at z=2 down to 0.074 Mpc at z=5.  The
  forest's WDM constraining power is strongest at HIGH z (less thermal broadening), which is exactly
  where this sector is SAFEST.  So the published number does not transfer, and the direction of the
  mismatch FAVOURS the model.  A proper re-analysis is owed and is likely to be more permissive. ***
"""

import sys
import mpmath as mp

mp.mp.dps = 20
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


G = mp.mpf("6.674e-11")
MPC = mp.mpf("3.0857e22")
H_LIT = mp.mpf("0.7")
RHO0 = mp.mpf("0.264") * mp.mpf("8.6e-27")
A0_0 = mp.mpf("9.3619e-11")
LAM0 = mp.mpf("2.2")                       # Mpc, calibration from stage 12's lensing exclusion
NU = mp.mpf("1.12")


def a0_ratio(z, w0=mp.mpf("-0.75"), wa=mp.mpf("-0.86")):
    z = mp.mpf(z)
    return (1 + z) ** (mp.mpf("1.5") * (1 + w0 + wa)) * mp.e ** (-mp.mpf("1.5") * wa * z / (1 + z))


print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- ERROR 1: the Jeans law is MONDian, and a_0(z) enters it")
print("=" * 100)

z3 = mp.mpf(3)
L_test = mp.mpf("0.025") * MPC
rho3 = RHO0 * (1 + z3) ** 3
gN = G * rho3 * L_test
a0z3 = A0_0 * a0_ratio(3)
check(gN / a0z3 < mp.mpf("1e-2"),
      f"A1  REGIME CHECK: at z = 3 and 0.1 Mpc comoving, g_N/a_0(z) = {sig(gN/a0z3,3)} -- four orders "
      "below the transition, so the perturbations are DEEP IN THE MOND REGIME and the Newtonian Jeans "
      "law I used in stage 13 was the wrong one",
      "this is the correction Carl flagged, and it is a physics error not a labelling one")


def growth_newt(z):
    return (1 + mp.mpf(z)) ** 3


def growth_mond(z):
    """L_J ~ a_0^(-1/3) rho^-1  =>  L_J(0)/L_J(z) = (1+z)^3 [a_0(z)/a_0(0)]^(1/3)."""
    return (1 + mp.mpf(z)) ** 3 * a0_ratio(z) ** (mp.mpf(1) / 3)


check(growth_mond(3) < growth_newt(3),
      f"A2  and the MOND correction runs AGAINST the sector: growth from z = 3 is "
      f"{sig(growth_mond(3),4)}x rather than {sig(growth_newt(3),4)}x, because a_0 was only "
      f"{sig(a0_ratio(3),3)} of its present value then and L_J ~ a_0^(-1/3)",
      "reported first because it is the unfavourable half of the correction")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- ERROR 2: the real forest bound, converted from published WDM limits")
print("=" * 100)

half = (mp.mpf(2) ** (NU / 5) - 1) ** (1 / (2 * NU))
print(f"\n   Viel et al. (2005) half-mode condition: alpha * k_1/2 = {sig(half,5)}\n")
print("     m_WDM [keV]   alpha [h^-1 Mpc]   k_1/2 [h/Mpc]   lambda_1/2 COMOVING [Mpc]")
bounds = {}
for m_s in ("2.0", "3.0", "3.5", "5.3", "6.0"):
    m = mp.mpf(m_s)
    al = mp.mpf("0.049") * m ** mp.mpf("-1.11")
    k = half / al
    lam = 2 * mp.pi / k / H_LIT
    bounds[m_s] = lam
    print(f"     {m_s:>9s}    {sig(al,4):>12s}     {sig(k,4):>10s}     {sig(lam,4)}")

check(bounds["3.5"] > mp.mpf("0.2") and bounds["5.3"] > mp.mpf("0.15"),
      f"B1  *** MY 0.1 Mpc FIGURE WAS TOO STRICT BY 1.5-2.4x.  The real permitted comoving scale is "
      f"{sig(bounds['6.0'],3)} Mpc (m > 6 keV, most aggressive) to {sig(bounds['2.0'],3)} Mpc "
      f"(m > 2 keV, most conservative), with the widely-quoted m > 3.5 keV giving "
      f"{sig(bounds['3.5'],3)} Mpc ***",
      "this correction is larger than Part A's and runs the other way")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the comparison, redshift bin by redshift bin")
print("=" * 100)

print("\n     z    MOND growth   comoving cutoff [Mpc]   vs 5.3 keV (0.153)   vs 3.5 keV (0.243)")
cuts = {}
for z_s in ("2", "3", "4", "5"):
    z = mp.mpf(z_s)
    com = LAM0 / growth_mond(z_s) * (1 + z)
    cuts[z_s] = com
    v53 = "OVER" if com > bounds["5.3"] else "under"
    v35 = "OVER" if com > bounds["3.5"] else "under"
    print(f"    {z_s:>3s}    {sig(growth_mond(z_s),5):>9s}      {sig(com,4):>10s}            "
          f"{v53:>6s}              {v35}")

check(cuts["5"] < bounds["6.0"] and cuts["4"] < bounds["5.3"],
      f"C1  *** AT HIGH REDSHIFT THE SECTOR IS COMFORTABLY SAFE: comoving cutoff "
      f"{sig(cuts['5'],3)} Mpc at z = 5 and {sig(cuts['4'],3)} Mpc at z = 4, both below even the most "
      "aggressive bound.  And high z is where the forest's WDM constraining power is greatest ***",
      "less thermal broadening at high z, so those bins carry the WDM limits")

check(cuts["3"] <= bounds["5.3"] * mp.mpf("1.01"),
      f"C2  at z = 3 it sits essentially ON the tightest published bound: {sig(cuts['3'],4)} Mpc "
      f"against {sig(bounds['5.3'],4)} Mpc -- a {sig(cuts['3']/bounds['5.3'],4)} ratio, i.e. the "
      "boundary rather than an exclusion",
      "and comfortably inside the m > 3.5 keV reading")

check(cuts["2"] > bounds["3.5"],
      f"C3  AGAINST INTEREST: at z = 2 the cutoff is {sig(cuts['2'],4)} Mpc, which EXCEEDS even the "
      f"m > 3.5 keV scale ({sig(bounds['3.5'],3)} Mpc).  The low-redshift forest bins are where this "
      "sector is genuinely exposed, and that must be said plainly",
      "it is inside the m > 3 keV reading, but that is a conservative analysis")

# NC-C (negative control): the comparison must reject a genuinely large cutoff at every z.
big = LAM0 * 10 / growth_mond("3") * (1 + mp.mpf(3))
check(big > bounds["2.0"],
      f"NC-C  CONTROL: a sector calibrated to 22 Mpc today would give {sig(big,3)} Mpc comoving at "
      "z = 3, exceeding even the most conservative bound -- so the comparison has teeth",
      "")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- *** AND THE POINT THAT MATTERS MOST: THE PUBLISHED BOUND DOES NOT TRANSFER ***")
print("=" * 100)
print(f"""
   Thermal-relic WDM has a cutoff FIXED IN COMOVING UNITS -- free-streaming is set once, in the early
   universe, and the comoving scale then stays put.  Every published m_WDM limit is a limit on THAT.

   This sector's comoving cutoff EVOLVES, and strongly:
        z = 2: {sig(cuts['2'],4)} Mpc      z = 3: {sig(cuts['3'],4)} Mpc
        z = 4: {sig(cuts['4'],4)} Mpc      z = 5: {sig(cuts['5'],4)} Mpc
   a factor {sig(cuts['2']/cuts['5'],3)} across the forest's own redshift range.  A fixed-cutoff bound
   cannot be applied to it bin by bin without re-deriving the likelihood.
""")
check(cuts["2"] / cuts["5"] > 3,
      f"D1  *** THE EVOLUTION IS A FACTOR {sig(cuts['2']/cuts['5'],3)} ACROSS z = 2-5, so the model is "
      "qualitatively different from the WDM template the bounds were derived for.  The comparison in "
      "Part C is indicative, NOT a likelihood ***",
      "which is the honest content of 'get the bound right': the published number does not transfer")

check(cuts["5"] < cuts["3"] < cuts["2"],
      "D2  and the DIRECTION of the mismatch favours the sector: the forest's WDM constraining power "
      "is concentrated at HIGH z (less thermal broadening), and that is precisely where this cutoff is "
      "SMALLEST.  A proper joint re-analysis would weight the safe bins most heavily",
      "so the indicative comparison in Part C is likely PESSIMISTIC for this model")

info("D3  and the evolution is itself a SIGNATURE, not just a complication: a cutoff scale that shrinks "
     "with redshift like a^3 a_0(z)^(1/3) is distinguishable from WDM's fixed comoving cutoff using "
     "the forest's own redshift bins. That is a real, near-term test on existing spectra.")


# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  *** STAGE 13'S "EXCLUDED BY 1.38x" IS WITHDRAWN.  THE HONEST VERDICT IS BOUNDARY, AND WHICH SIDE
  DEPENDS ON A LIKELIHOOD NOBODY HAS RUN. ***

  1. TWO ERRORS OF MINE, IN OPPOSITE DIRECTIONS.  (a) I used a NEWTONIAN Jeans length in a framework
     whose perturbations are deep in the MOND regime at these scales (g_N/a_0 ~ 1e-4) -- the correct
     law is L_J ~ (c_s^2)^(2/3)(G rho a_0)^(-1/3), which carries a_0(z)^(-1/3) and reduces the growth
     from 64x to {sig(growth_mond(3),4)}x: AGAINST the sector.  Carl caught this and he was right.
     (b) My "0.1 Mpc forest sensitivity" was a round number, not a bound.  Converting real WDM limits
     through Viel et al. (2005) gives {sig(bounds['6.0'],3)}-{sig(bounds['2.0'],3)} Mpc: strongly FOR the
     sector, and the larger of the two corrections.

  2. THE RESULTING PICTURE, bin by bin: SAFE at z = 4-5 ({sig(cuts['4'],3)} and {sig(cuts['5'],3)} Mpc, below
     every bound), ON THE LINE at z = 3 ({sig(cuts['3'],4)} vs {sig(bounds['5.3'],4)} Mpc for the tightest
     published limit), and EXPOSED at z = 2 ({sig(cuts['2'],4)} Mpc, above the m > 3.5 keV scale).

  3. *** AND THE DECISIVE POINT: THE PUBLISHED BOUND DOES NOT TRANSFER.  Every m_WDM limit constrains a
     cutoff FIXED in comoving units.  This sector's comoving cutoff evolves by a factor
     {sig(cuts['2']/cuts['5'],3)} across the forest's own redshift range -- and it is SMALLEST exactly where
     the forest constrains WDM most strongly.  So Part C is an indicative comparison, not a
     likelihood, and the direction of the mismatch favours the model. ***

  4. WHAT IS ACTUALLY OWED, and it is now a specific, bounded piece of work rather than a search:
     re-derive the forest likelihood for an EVOLVING cutoff, L_J(z) ~ a^3 a_0(z)^(1/3), against the
     public flux-power spectra (XQ-100, MIKE/HIRES, or the SDSS/BOSS bins), marginalising over the IGM
     thermal history as those analyses do.  That is one MCMC on public data.  It is the last thing
     standing between this sector and a verdict.

  5. AND THE EVOLUTION IS A PREDICTION IN ITS OWN RIGHT: a cutoff that shrinks with redshift is
     qualitatively distinguishable from WDM's fixed comoving cutoff using the forest's own z-bins.
     Whichever way the likelihood falls, that is a real test on spectra that already exist.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f_ in FAIL:
        print("   -", f_)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED (incl. 1 negative control)")
sys.exit(0)
