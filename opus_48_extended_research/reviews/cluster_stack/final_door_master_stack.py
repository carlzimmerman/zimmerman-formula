"""
FINAL-DOOR MASTER STACK: assemble the honest best-case no-new-particle stack
(Route B AeST Y-Q field boost + IGIMF remnants + known baryons), apply the four
FINAL-DOOR candidate ingredients (i-iv), and report the best-case CORE coverage % in
BOTH shape scenarios (gas-tracking vs galaxy-tracking) WITHOUT double-counting, with the
residual gap conceded at full weight.

ANTI-DOUBLE-COUNT RULES enforced here:
  - ICL (candidate iii) is INSIDE the IGIMF stellar budget -> NOT added separately.
  - Route A's IGIMF-BCG and Route D's IGIMF-remnants are the SAME M/L boost on the SAME
    stellar mass -> counted ONCE (the BCG is the central part of the stellar budget).
  - Candidate (i) lensing-vs-dynamics slip caps at the 3% two-probe data slack -> applied
    as a target reduction, NOT a mass add.
  - Candidates (ii) non-equilibrium and (iv) EFE are wrong-signed/negligible -> 0 added.
  - Route B (~17-20% AeST field boost) is on the MOND PHANTOM (the field), IGIMF is on
    BARYONS, baryon-census gas is the ICM -> three DISJOINT channels, no overlap.

BOTH WAYS: best-case generous in each channel, but no channel double-counted; the
remaining residual gap is reported at full weight under both shape readings.
"""
import numpy as np

Msun = 1.989e30

print("="*94)
print(" FINAL-DOOR MASTER STACK -- honest best-case no-new-particle core coverage (both ways)")
print("="*94)

# ---------------- the banked CORE target (rich M500=1e15, <420 kpc) ----------------
M_target_lens = 1.357e14     # CLASH lensing residual (banked, routeA-reproduced)
M_phantom_MI  = 3.508e13     # framework MI phantom (bare, dynamical=lensing)
M_bar_core    = 2.549e13     # baryons in core (gas 2.46e13 + 1e12 BCG), banked routeA
M_gas_core    = 2.460e13     # core gas
core_gap_bare = M_target_lens - M_phantom_MI
print("\n[CORE, <420 kpc] target=%.3e  bare MI phantom=%.3e  baryons=%.3e  bare gap=%.3e (x%.2f)"
      % (M_target_lens, M_phantom_MI, M_bar_core, core_gap_bare, M_target_lens/M_phantom_MI))

# ====================================================================================
# CHANNEL 1 (Route B): the AeST Y-Q FIELD boost on the MOND phantom: +17-20%
# ====================================================================================
yq_boost = 0.20    # best-case +20% over the bare phantom (Route B verdict, viable 1/mu)
M_phantom_B = M_phantom_MI*(1.0+yq_boost)
dM_B = M_phantom_B - M_phantom_MI
print("\n CHANNEL 1 (Route B AeST Y-Q field, +%.0f%%): phantom %.3e -> %.3e  (+%.3e)"
      % (100*yq_boost, M_phantom_MI, M_phantom_B, dM_B))

# ====================================================================================
# CHANNEL 2 (Route D): IGIMF stellar remnants in the core. SHAPE-dependent.
#   gas-tracking (FPS) vs galaxy-tracking (Bullet 2605.10022) -> two coverage numbers.
# ====================================================================================
# Stellar budget (canonical IMF, whole cluster), IGIMF M/L boost, fraction in core.
M_star_canon = 1.5e13     # generous canonical total cluster stars (between 1.3 and 2.0e13)
ML_boost     = 8.0        # generous IGIMF M/L (Kroupa headline 6x; 8x = generous ceiling)
M_extra_igimf = (ML_boost-1.0)*M_star_canon   # extra remnant mass, whole cluster

# fraction landing inside 420 kpc, and the SHAPE penalty:
#   - galaxy-tracking: remnants follow the galaxy/ICL distribution -> ~60% in core (generous)
#   - gas-tracking demand: the residual must be a FLAT gas-tracking ~10 shell; star-tracking
#     remnants over-fill the center and UNDER-fill the 100-420 kpc shell -> an EFFECTIVE
#     shape-usable fraction lower than the raw enclosed fraction. We apply a shape-efficiency.
f_in_core      = 0.60     # generous: 60% of remnant mass inside 420 kpc
shape_eff_gal  = 1.00     # galaxy-tracking: remnants ARE the right shape -> full credit
shape_eff_gas  = 0.55     # gas-tracking: star-spike mismatches flat shell -> ~55% usable

M_igimf_core_gal = f_in_core*M_extra_igimf*shape_eff_gal
M_igimf_core_gas = f_in_core*M_extra_igimf*shape_eff_gas
print("\n CHANNEL 2 (Route D IGIMF remnants): canonical stars %.2e, ML=%.0fx -> extra %.3e"
      % (M_star_canon, ML_boost, M_extra_igimf))
print("   galaxy-tracking core mass (60%% in core, full shape) = %.3e" % M_igimf_core_gal)
print("   gas-tracking   core mass (60%% in core, 55%% shape-eff)= %.3e" % M_igimf_core_gas)
print("   [ICL is INSIDE this stellar budget -> candidate (iii) adds 0, no double-count]")

# ====================================================================================
# CHANNEL 3 (Route A baryons): known-physics core baryons NOT in the stellar budget.
#   = missing warm-hot gas inside core (generous +15%) + min-nu (negligible).
#   (the IGIMF-BCG piece is in CHANNEL 2, not re-added here -> no double-count)
# ====================================================================================
M_gas_extra = 0.15*M_gas_core    # +15% undetected core gas (generous; banked realistic ceiling)
M_nu_core   = 4.5e8              # min-nu in core (Tremaine-Gunn ceiling, negligible)
M_baryon_extra = M_gas_extra + M_nu_core
print("\n CHANNEL 3 (Route A baryons): +15%% core gas %.3e + min-nu %.2e = %.3e"
      % (M_gas_extra, M_nu_core, M_baryon_extra))

# ====================================================================================
# CANDIDATE (i): lensing-vs-dynamics slip -> reduce the DYNAMICAL target by the 3% slack.
#   (applied as a target reduction, capped at the two-probe data ceiling)
# ====================================================================================
slip = 1.03
M_target_dyn = M_target_lens/slip   # the dynamical residual a no-DM theory must source
print("\n CANDIDATE (i) lensing-vs-dyn slip (cap 1.03): dynamical target %.3e (lensing %.3e)"
      % (M_target_dyn, M_target_lens))
print(" CANDIDATE (ii) non-equilibrium: WRONG SIGN (HSE biases low) -> 0 deflation applied.")
print(" CANDIDATE (iii) ICL/2nd remnant: SUBSUMED by IGIMF -> 0 added (anti-double-count).")
print(" CANDIDATE (iv) EFE: negligible/wrong-signed -> 0 added.")

# ====================================================================================
# THE HONEST BEST-CASE STACK (no double-count) under BOTH shape readings
# ====================================================================================
def coverage(M_igimf_core, target, label):
    supplied = M_phantom_B + M_igimf_core + M_baryon_extra
    # 'no-particle CORE coverage %': supplied / target (the bare baryons are part of the
    # cluster; the TARGET is the missing collisionless mass, so we compare the no-particle
    # SOURCES (phantom field + remnants + extra gas) against the missing-mass target).
    cov = 100.0*supplied/target
    residual = target - supplied
    print("\n  --- %s (target %.3e) ---" % (label, target))
    print("    Route B phantom (field)      = %.3e" % M_phantom_B)
    print("    Route D IGIMF remnants (core)= %.3e" % M_igimf_core)
    print("    Route A extra baryons (core) = %.3e" % M_baryon_extra)
    print("    -------------------------------------------")
    print("    TOTAL no-particle supplied   = %.3e" % supplied)
    print("    CORE coverage                = %.1f%%" % cov)
    print("    residual gap (full weight)   = %.3e Msun  (%.1f%% of target uncovered)"
          % (residual, 100*residual/target))
    return cov, residual

print("\n" + "="*94)
print(" HONEST BEST-CASE CORE COVERAGE (no double-count), BOTH shape readings + (i) slip")
print("="*94)

cov_gas, res_gas = coverage(M_igimf_core_gas, M_target_dyn, "GAS-TRACKING (FPS), dyn target")
cov_gal, res_gal = coverage(M_igimf_core_gal, M_target_dyn, "GALAXY-TRACKING (Bullet), dyn target")

# also report vs the raw LENSING target (no slip) for the conservative read:
print("\n  [conservative, NO slip -- vs raw lensing target %.3e]" % M_target_lens)
cov_gas_L = 100*(M_phantom_B+M_igimf_core_gas+M_baryon_extra)/M_target_lens
cov_gal_L = 100*(M_phantom_B+M_igimf_core_gal+M_baryon_extra)/M_target_lens
print("    gas-tracking coverage   = %.1f%%   galaxy-tracking coverage = %.1f%%" % (cov_gas_L, cov_gal_L))

# ====================================================================================
# THE CEILING TEST: is (B+IGIMF+baryons) the ceiling? Did any candidate add a 3rd channel?
# ====================================================================================
print("\n" + "="*94)
print(" CEILING TEST -- did any FINAL-DOOR candidate add a genuine THIRD channel?")
print("="*94)
print("  (i)   lensing-vs-dyn slip : target -3%% (data cap). NOT a mass channel; ~4%% gap-shrink.")
print("  (ii)  non-equilibrium     : WRONG SIGN (+15%% target if anything). 0 added.")
print("  (iii) ICL / 2nd remnants  : SUBSUMED by IGIMF (anti-double-count). 0 fresh mass.")
print("  (iv)  EFE on the core     : negligible/wrong-signed. 0 added.")
print("  ==> NO candidate adds a genuine third no-particle channel. The stack")
print("      (B field + IGIMF remnants + known baryons) IS THE CEILING.")
print()
print("  Best-case coverage: %.0f%% (gas-tracking) to %.0f%% (galaxy-tracking) of the core."
      % (cov_gas, cov_gal))
print("  Residual gap conceded at full weight: %.0f%% (galaxy) to %.0f%% (gas) of the core"
      % (100*res_gal/M_target_dyn, 100*res_gas/M_target_dyn))
print("  stays UNCOVERED by any no-new-particle ingredient. The core remains the shared")
print("  relativistic-MOND open soft-spot. No manufactured closure; no reflexive dismissal.")
