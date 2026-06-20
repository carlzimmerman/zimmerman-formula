#!/usr/bin/env python3
r"""
ROUTE C -- Cassini / solar-system bound on the second-scalar fifth force + the bimetric variant.
================================================================================================
The core-filling second scalar needs a UNIVERSAL Yukawa coupling alpha~1 to baryons, range
l_chi >~ 420 kpc.  An UNSCREENED scalar fifth force of that strength and range is wildly excluded
by the solar system.  Quantify against Cassini (the framework's banked MI-vs-MG discriminator).
"""
import numpy as np
G=6.674e-11; c=2.998e8; AU=1.496e11; kpc=3.0857e19

print("="*90)
print("ROUTE C -- Cassini / solar-system bound on the second-scalar fifth force")
print("="*90)
print(r"""
  A scalar chi Yukawa-coupled to baryons with strength alpha and range l_chi gives an extra
  potential  V_chi = -alpha (G M/r) exp(-r/l_chi).  For l_chi >~ 420 kpc >> 1 AU, exp(-r/l)~1,
  so it is an UNSCREENED 1/r fifth force: it simply RESCALES Newton's constant by (1+alpha) on
  ALL scales below l_chi -- the Sun, the planets, binary pulsars, EVERYTHING inside 420 kpc.
""")
# (1) A universal (1+alpha) rescaling of G is NOT directly Cassini-bound (it renormalizes G);
#     the bound is on a COMPOSITION-DEPENDENT or TIME/SPACE-VARYING piece. But the core closure
#     needs chi to track GAS not stars => it must couple DIFFERENTLY to gas vs stars
#     (else it tracks total baryons = stars, not gas-tracking). That composition dependence is
#     exactly what the Eot-Wash / Cassini / LLR bounds forbid.
alpha=0.98
print(f"  (1) If alpha is UNIVERSAL (same coupling to all baryons): it renormalizes G by (1+alpha)={1+alpha:.2f}")
print(f"      -> NOT directly Cassini-bound (absorbed into G_eff) BUT then chi tracks TOTAL baryons")
print(f"      = stars+gas, i.e. it tracks the STELLAR cusp too -> NOT gas-tracking. Contradiction with")
print(f"      the A2029/RXJ1347 gas-tracking shape (M_res/M_star rises 15-30x). FAILS G4 shape.")
print()
print(f"  (2) To be GAS-tracking, chi must couple to GAS more than STARS (e.g. to thermal pressure /")
print(f"      ionized-plasma fraction). That is a COMPOSITION-DEPENDENT fifth force. Bounds:")
# Cassini bound on a composition-dep / scalar fifth force: |gamma-1| < 2.3e-5 (Bertotti+2003).
# A scalar of gravitational strength alpha~1 gives |gamma-1| ~ alpha/(1+alpha) ~ O(0.5) for unscreened.
gamma_cassini = 2.3e-5
alpha_max_unscreened = gamma_cassini/(1-gamma_cassini/2)  # |gamma-1|=2 alpha_chi/(1+alpha_chi) approx -> alpha<~1.15e-5
print(f"      Cassini (Bertotti+2003): |gamma-1| < {gamma_cassini:.1e}. A scalar contributes")
print(f"      |gamma-1| ~ 2 alpha/(1+alpha). For the needed alpha~1: |gamma-1|~1 -> exceeds Cassini by")
print(f"      ~{1/gamma_cassini:.0e}x. The Sun's plasma (kT_core~1 keV, fully ionized) couples to a")
print(f"      gas/plasma-sourced chi -> a HUGE unscreened fifth force at Saturn. EXCLUDED by ~5 orders.")
print()
print(r"""  (3) THE ONLY WAY OUT IS SCREENING (chameleon/Vainshtein) in the solar system. But:
       - chameleon screening is DENSITY-triggered, and (banked Part 3) galaxy/solar cores are
         DENSER than cluster cores -> the screen that hides the Sun ALSO hides the cluster core
         (cluster cores are LESS dense than the Sun by ~10^10). Wrong ordering: you cannot screen
         the Sun and un-screen the cluster core with a single density threshold.
       - Vainshtein screening is MASS/curvature-triggered -> screens INSIDE massive bodies; a
         cluster core has HIGHER enclosed mass than the solar system -> screened EVEN MORE.
      Either screening that passes Cassini ALSO kills the cluster-core enhancement. No window.
""")
print("  CASSINI VERDICT: a gas-tracking second-scalar fifth force is composition-dependent at")
print("  alpha~1 -> exceeds Cassini |gamma-1| by ~5 orders unscreened; any screening that saves")
print("  Cassini (density- or mass-triggered) ALSO screens the cluster core (denser-Sun / heavier-")
print("  cluster ordering). G4-Cassini: FAIL with no consistent screening window.\n")

print("="*90)
print("ROUTE C -- the BIMETRIC / massive-graviton partner variant")
print("="*90)
print(r"""
  Variant: instead of a scalar, add a SECOND metric / massive spin-2 partner (bigravity) whose
  extra polarizations source core mass.  Tested both ways:
   - In bigravity the second metric's effect on matter is again a Yukawa-range modification of the
     gravitational potential, range = graviton Compton wavelength m_g^-1.  To add cluster-core mass
     needs m_g^-1 ~ Mpc.  But a Mpc-range massive graviton:
       (a) is the SAME universal-vs-composition dilemma as the scalar (universal -> tracks stars,
           not gas-tracking; composition-dep -> Cassini-excluded);
       (b) bigravity has a NOTORIOUS Higuchi-ghost / strong-coupling problem in exactly the regime
           (sub-horizon, nonlinear cluster) needed -> instability, not a clean source;
       (c) c_GW=c (GW170817) forces the bigravity branch to the 'minimal model' whose extra force
           is Yukawa-suppressed at exactly Mpc unless m_g is tuned -> a tuned new scale, RELOCATING.
   - And a massive graviton is a NEW spin-2 SPECIES with 5 polarizations -- structurally a NEW
     field with new dof, NOT 'the framework's own ghost-condensate'.  G3: relocates fully (new
     gravitational sector), and it inherits the SAME shape (G4) + Cassini (G4) kills as the scalar.
""")
print("  BIMETRIC VERDICT: same universal-vs-composition / Cassini dilemma as the scalar, PLUS a")
print("  Higuchi-ghost instability in the cluster regime and a new spin-2 species. No advantage;")
print("  G3 relocates fully, G1/G4 inherit the scalar's fails.\n")
