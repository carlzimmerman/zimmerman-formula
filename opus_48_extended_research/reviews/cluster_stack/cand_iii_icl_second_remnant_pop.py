"""
FINAL-DOOR candidate (iii): a SECOND stellar/remnant population or INTRACLUSTER LIGHT (ICL)
mass NOT already in the BCG count.

QUESTION (both ways): Route D (IGIMF remnants) re-weights the cluster STELLAR mass by a
top-heavy IMF M/L boost. Route A's BCG piece is a single ~1e12 Msun BCG. Is there a
SEPARATE, not-double-counted mass reservoir in the core from the INTRACLUSTER LIGHT (ICL)
-- the diffuse stellar halo between galaxies -- or a second remnant population (e.g. old
halo white dwarfs / faint ICL remnants) that the BCG-only count misses?

THE CRITICAL DOUBLE-COUNTING QUESTION (the whole point):
  Route D's IGIMF boost is applied to the TOTAL cluster stellar mass (~1.3e13 Msun for a
  rich cluster), which ALREADY INCLUDES the BCG + ICL + satellite light. If we now add ICL
  as a "new" reservoir, we double-count. The honest question is: how much of the core
  stellar budget is ICL that is NOT in Route A's 1e12 BCG AND NOT already inside Route D's
  1.3e13 total? Answer: the ICL is INSIDE Route D's total. So as a fresh ingredient ON TOP
  OF Route D, ICL adds ~0. As a fresh ingredient on top of Route A's BCG-only stack, it
  adds the ICL mass -- but that is exactly what Route D already monetizes.

THE PHYSICS (literature, both ways):
  - Total cluster stellar mass (BCG+ICL+satellites), rich M500~1e15: M*_tot ~ 1-2e13 Msun
    (Kravtsov+2018; Gonzalez+2013). ICL is ~30-50% of that -> M_ICL ~ 4-8e12 Msun.
  - BCG+ICL within 100 kpc: luminosity 1.2-3.5e12 Lsun (Kluge/Zhang ICL studies); with a
    massive-elliptical M/L ~ 3-7 (Salpeter-ish) -> M_(BCG+ICL,<100kpc) ~ 0.4-2.4e13 Msun.
  - ICL is centrally concentrated but more extended than the BCG (NFW-like, traces the
    cluster potential), so a good fraction lands in the 100-420 kpc core shell.

CONCLUSION (both ways): ICL is REAL core mass, but it is ALREADY in Route D's stellar
budget. The ONLY non-double-counted increment is whatever ICL the Route-D budget UNDER-
counted. We quantify that honestly and refuse to stack ICL on top of the IGIMF boost.
"""
import numpy as np

Msun = 1.989e30
kpc  = 3.086e19

print("="*94)
print(" FINAL-DOOR candidate (iii): ICL / second stellar-remnant population (anti-double-count)")
print("="*94)

# banked core numbers
M_target_lens = 1.357e14
M_phantom_MI  = 3.508e13
core_gap      = M_target_lens - M_phantom_MI
print("\n[banked core, <420 kpc] target %.3e, MI phantom %.3e, gap %.3e (x%.2f)"
      % (M_target_lens, M_phantom_MI, core_gap, M_target_lens/M_phantom_MI))

# =====================================================================
# 1. THE TOTAL CLUSTER STELLAR BUDGET (what Route D already boosts)
# =====================================================================
print("\n" + "-"*94)
print(" 1. The total cluster stellar budget (BCG+ICL+satellites) -- already in Route D")
print("-"*94)
M_star_tot   = 1.3e13   # Msun, canonical-IMF total cluster stars (Route D banked, Kravtsov+2018)
f_ICL        = 0.40     # ICL share of total cluster stars (Kluge+2021, Zhang+2024: 30-50%)
f_BCG        = 0.20     # BCG share
f_sat        = 0.40     # satellites
M_ICL_canon  = f_ICL*M_star_tot
M_BCG_canon  = f_BCG*M_star_tot
print("  Canonical total cluster stellar mass (BCG+ICL+sats) = %.3e Msun" % M_star_tot)
print("    ICL share (~40%%)        = %.3e Msun" % M_ICL_canon)
print("    BCG share (~20%%)        = %.3e Msun  (Route A used a single 1e12 BCG)" % M_BCG_canon)
print("    satellites (~40%%)       = %.3e Msun" % (f_sat*M_star_tot))
print("  ==> Route D's IGIMF M/L boost (~6x) is applied to THIS WHOLE 1.3e13, which")
print("      ALREADY INCLUDES the ICL. So ICL is NOT a fresh reservoir on top of Route D.")

# =====================================================================
# 2. ICL mass in the core, and what FRACTION Route A's BCG-only count missed
# =====================================================================
print("\n" + "-"*94)
print(" 2. ICL mass landing in the <420 kpc core (NFW-like, more extended than BCG)")
print("-"*94)
# ICL traces the cluster potential ~ NFW(c~4-6); enclosed-mass fraction inside 420 kpc.
def frac_nfw(R_kpc, rs):
    x = R_kpc/rs; m = np.log(1+x) - x/(1+x)
    xt = 1400.0/rs; mt = np.log(1+xt) - xt/(1+xt)
    return m/mt
rs_icl = 250.0   # kpc, ICL scale (between BCG ~50 and cluster ~350)
f_core_icl = frac_nfw(420.0, rs_icl)
M_ICL_core = f_core_icl*M_ICL_canon
print("  ICL enclosed fraction inside 420 kpc (NFW rs=250 kpc) = %.2f" % f_core_icl)
print("  ICL mass inside core (canonical IMF)                  = %.3e Msun" % M_ICL_core)
# Route A counted only a 1e12 BCG; the ICL it MISSED (canonical IMF) inside core:
M_BCG_routeA = 1.0e12
ICL_missed_by_routeA = M_ICL_core   # ICL was entirely outside Route A's BCG-only count
print("  Route A counted a single %.1e BCG -> it MISSED the ICL entirely." % M_BCG_routeA)
print("  ICL the BCG-only Route A missed (canonical) inside core = %.3e Msun (%.1f%% of gap)"
      % (ICL_missed_by_routeA, 100*ICL_missed_by_routeA/core_gap))

# =====================================================================
# 3. THE ANTI-DOUBLE-COUNT RULE: ICL is inside Route D's IGIMF budget
# =====================================================================
print("\n" + "-"*94)
print(" 3. ANTI-DOUBLE-COUNT: is ICL a FRESH increment on top of the (B+IGIMF+baryons) stack?")
print("-"*94)
print("  Route D applies a ~6x M/L (IGIMF) boost to the TOTAL 1.3e13 stellar mass, which")
print("  INCLUDES the %.3e ICL. So the IGIMF-boosted ICL is ALREADY counted in Route D's" % M_ICL_canon)
print("  extra-remnant budget. Adding ICL again = DOUBLE COUNT. The honest increment of")
print("  candidate (iii) ON TOP OF the existing stack is ~0 (ICL subsumed by IGIMF).")
print()
# The ONLY non-double-counted increment: if the canonical M*_tot=1.3e13 itself under-counted
# ICL (some ICL studies find more diffuse light). Even a generous +50% ICL upward revision:
M_star_revised = M_star_tot*1.25   # +25% total stars from a higher ICL census (generous)
extra_star_canon = (M_star_revised - M_star_tot)
extra_star_core  = f_core_icl*extra_star_canon
print("  Most-generous non-double-count increment: revise total stars UP +25%% (higher ICL census):")
print("    extra canonical stars = %.3e, inside core = %.3e (%.1f%% of gap)"
      % (extra_star_canon, extra_star_core, 100*extra_star_core/core_gap))
print("    BUT under Route D this gets the SAME 6x IGIMF boost -> it inflates Route D's")
print("    number, NOT a separate channel. Reported as part of Route D's budget, not added.")

# =====================================================================
# 4. SECOND REMNANT POPULATION beyond IGIMF? (white dwarfs / MACHOs / faint remnants)
# =====================================================================
print("\n" + "-"*94)
print(" 4. A SECOND remnant population beyond the IGIMF neutron-stars/BHs?")
print("-"*94)
print("  IGIMF (Route D) already monetizes the remnant census from a top-heavy IMF")
print("  (neutron stars + stellar BHs). A SEPARATE population would be:")
print("   - Halo white dwarfs / faint old remnants: MACHO/EROS microlensing caps the")
print("     compact-baryon halo fraction at <~few %% (f_MACHO < 0.1) -> sub-dominant, and")
print("     these ARE the low-mass tail of the SAME IMF -> double-count with IGIMF.")
print("   - Primordial black holes: NOT baryons formed from stars; if invoked as the dark")
print("     mass they ARE a new (non-baryonic) species -> G3 FAILS (relocates the sector).")
print("   - Cold molecular gas clouds (FPS's own 'collisionless cold clouds'): a real")
print("     no-particle BARYON route, but it is the SAME baryon budget as piece (ii) gas;")
print("     BBN caps total baryons at f_b cosmic -> already in the baryon census.")
print("  => No genuinely-separate, non-double-counted, BBN-safe remnant population exists")
print("     beyond what Route D + the baryon census already hold.")

# =====================================================================
# 5. GATES
# =====================================================================
print("\n" + "="*94)
print(" GATES for candidate (iii) [ICL / second remnant population]")
print("="*94)
print("  G1 SUFFICIENCY : FAILS as a FRESH ingredient -- ICL is REAL core mass (~%.0e in core)"
      % M_ICL_core)
print("                   but it is ALREADY inside Route D's IGIMF-boosted stellar budget.")
print("                   The non-double-counted increment on top of (B+IGIMF) is ~0.")
print("  G2 GALAXY-VETO : PASS (stellar mass, no galaxy-disk effect).")
print("  G3 NO-PARTICLE : PASS for ICL/remnants (real baryons); FAILS for PBHs (new species).")
print("  G4 DATA        : ICL masses are real (Kluge/Zhang); but the data already folds ICL")
print("                   into the total stellar census Route D boosts.")
print("\n  VERDICT (iii): NOT a fresh third ingredient. ICL is real but SUBSUMED by Route D's")
print("  IGIMF boost (anti-double-count). No separate BBN-safe remnant population beyond")
print("  IGIMF + the baryon census. Both ways: refuse to stack ICL on top of IGIMF.")
