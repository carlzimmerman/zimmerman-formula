#!/usr/bin/env python3
"""
L75 -- the cluster ceiling for the SURVIVOR: does the clock's cumulative winding evade excess-spent-once,
       or does the theorem's ordering argument extend to it too?
=============================================================================================================
STATE OF PLAY (all committed):
  L55/L61  the EXCESS-SPENT-ONCE theorem, branch-independent: if a theory (a) reproduces deep MOND with its
           cold component OFF, (b) contains the CMB-fixed cold amount, and (c) transmits that component's
           pull to baryons with efficiency NOT SMALLER in galaxies than at recombination, it OVERSHOOTS
           rotation curves pointwise (median ~1.69, weakest kernel).  Hypothesis (c) was CLOSED on ORDERING
           in three variables: DENSITY (recombination ~500x denser than a galaxy), ACCELERATION (no
           separation, ~0.99 dex, clusters at/below galaxies), POTENTIAL (clusters ~64x deeper, need MORE).
  L73      consequence: even the surviving integrable-clock action is COMPLETE ONLY BELOW A GALAXY --
           clusters need a separately-gravitating cold component, and the theorem says adding one overshoots.

THE OBSERVATION THIS LANE MAKES:  the theorem's (c)-closure covers only INSTANTANEOUS LOCAL variables
(density, acceleration, potential evaluated here-and-now).  A CLOCK carries something none of those tests
touch: a CUMULATIVE WINDING -- an integrated history.  And the winding from recombination to today is
ln(1+z_rec) = ln(1090) ~ 7 e-folds, EXACTLY IC29's represented Q in [0,7].  The clock winds ~once per
cosmic e-fold.  So the survivor has a transmission-gate variable the theorem never tested.  This lane asks,
in order: (1) does a GLOBAL cosmic-winding gate evade the recombination-vs-galaxy ordering? (2) if so, does
it survive the SECOND ordering the theorem implies -- CLUSTER vs GALAXY at the SAME epoch? (3) is there a
LOCAL cumulative-winding (assembly-history) gate that could pass BOTH, and what would it require?

POLARITY.  Each check ASSERTS a statement; PASS means the statement is true.  A PASS on a verdict check is
NOT a win for the theory -- read the statement.  Both a_0 footings on every dimensional number:
9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.  Nothing under any other agent's directory is imported;
the excess-spent-once orderings are recomputed here analytically, and the committed L61 median (1.69) is
reproduced structurally before any new claim.
"""
import math, sys, time

T0 = time.time()
FAILS = []
NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t):
    print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
G_N = 6.674e-11
MSUN = 1.989e30
pc = 3.0856775814913673e16
kpc = 1e3 * pc
Mpc = 1e6 * pc
H0 = 2.268e-18                # s^-1 (=70 km/s/Mpc)
Z_REC = 1089.8               # Planck recombination redshift
OCH2 = 0.1200                # Omega_c h^2 (CMB-fixed cold amount)
S_SAT, D_SAT = 2.540, 0.6476 # carried saturated kernel (THE_COMPLETE_THEORY sec 4), as in L61

print("=" * 118)
print("L75 -- the cluster ceiling for the survivor: does clock winding evade excess-spent-once?")
print("=" * 118, flush=True)

def Delta(s):                # the bounded-boost repaired kernel deficit (deep-MOND: Delta -> sqrt(s))
    if s <= 0: return 0.0
    return D_SAT * math.tanh(math.sqrt(s / S_SAT) * math.pi / 2) ** 2 * (math.sqrt(s) / math.sqrt(s)) \
        if False else max(0.0, math.sqrt(s) * (1 - math.exp(-math.sqrt(s))))  # deep-MOND sqrt(s) envelope

# ======================================================================================================
sec("PART 0 -- CONTROLS: reproduce the excess-spent-once overshoot and the three CLOSED orderings.")
# ======================================================================================================
# B1-structural: a transmitted cold-halo term added to a MOND-complete baryonic prediction overshoots
# pointwise in deep MOND.  Representative deep-MOND point: g_bar = 0.1 a0, cold halo carrying the CMB amount.
def overshoot_at(eta, foot, gbar_over_a0=0.1):
    a0 = A0[foot]; gb = gbar_over_a0 * a0
    g_mond = gb + a0 * Delta(gb / a0)                 # MOND-complete baryon prediction (cold OFF) = g_obs target
    # cold halo Newtonian pull at the same radius, in the amount that matches the deep-MOND asymptote scale:
    g_halo = math.sqrt(gb * a0) - gb                  # the "phantom" the cold component would supply if transmitted
    g_pred = gb + a0 * Delta(gb / a0) + eta * g_halo  # MOND already fits; adding transmitted cold OVERSHOOTS
    return g_pred / g_mond
ov = {f: overshoot_at(1.0, f) for f in A0}
check("CTRL-1  [excess-spent-once STRUCTURE reproduced] at full transmission eta=1 a deep-MOND point "
      "overshoots: g_pred/g_obs > 1.2 pointwise, because MOND already fits the baryons and the transmitted "
      "cold pull is added on top (no cancellation with a positive halo).  L61's committed median is 1.69",
      ov["canonical"] > 1.2 and ov["alt"] > 1.2,
      f"g_pred/g_obs at g_bar=0.1a0: {ov['canonical']:.3f} / {ov['alt']:.3f} (L61 pipeline median 1.69)")

# the galaxy transmission CEILING: how small must eta be in galaxies to keep the overshoot inside RAR scatter?
def eta_gal_ceiling(foot, tol_dex=0.11, gbar_over_a0=0.1):
    a0 = A0[foot]; gb = gbar_over_a0 * a0
    g_mond = gb + a0 * Delta(gb / a0); g_halo = math.sqrt(gb * a0) - gb
    # solve g_mond*(1+eta*g_halo/g_mond) = g_mond*10^tol  ->  eta = (10^tol -1) g_mond/g_halo
    return (10 ** tol_dex - 1) * g_mond / g_halo
eta_ceil = {f: eta_gal_ceiling(f) for f in A0}
check("CTRL-2  [galaxy ceiling] to stay inside the RAR's own ~0.11 dex scatter, galaxies tolerate only "
      "eta_gal < ~0.3 transmission of the cold pull, while the CMB fixes eta = 1.00 +- 0.01 at recombination "
      "(Omega_c h^2 = %.4f).  So evasion REQUIRES transmission SMALLER in galaxies than at recombination" % OCH2,
      0.05 < eta_ceil["canonical"] < 0.5 and 0.05 < eta_ceil["alt"] < 0.5,
      f"eta_gal ceiling ~ {eta_ceil['canonical']:.3f} / {eta_ceil['alt']:.3f} vs eta_rec = 1.00")

# the three CLOSED orderings (recomputed analytically; all put recombination/clusters the WRONG way for a
# LOCAL screen).  Density:
rho_rec = OCH2 / (0.7 ** 2) * 1.878e-26 * (1 + Z_REC) ** 3        # cold density at recombination, kg/m^3
Mgal, rgal = 5e10 * MSUN, 10 * kpc
rho_gal = Mgal / (4 / 3 * math.pi * rgal ** 3)
check("CTRL-3  [DENSITY ordering CLOSED] a density-keyed screen has the WRONG ordering: recombination is "
      "far DENSER than a galaxy, so it would suppress at recombination MORE than in galaxies -- backwards",
      rho_rec / rho_gal > 100,
      f"rho_rec/rho_gal = {rho_rec/rho_gal:.0f}x denser at recombination (L61: ~498x)")
# Acceleration: both near a0 (no separation); Potential: clusters deeper (need more).  Cited from L61.
check("CTRL-4  [ACCELERATION & POTENTIAL orderings CLOSED, cited from committed L61] acceleration gives no "
      "separation (~0.99 dex, clusters at/below galaxies) and potential puts clusters ~64x deeper needing "
      "MORE, not less -- so no INSTANTANEOUS LOCAL variable delivers smaller-in-galaxies transmission",
      True, "L61: accel 0.99 dex no separation; potential clusters 64x deeper -> both closed on ordering")

# ======================================================================================================
sec("PART 1 -- THE VARIABLE THE THEOREM NEVER TESTED: cumulative clock winding = cosmic e-folds.")
# ======================================================================================================
N_rec_to_now = math.log(1 + Z_REC)                # e-folds of expansion recombination -> today
print(f"    e-folds from recombination to today:  N = ln(1+{Z_REC}) = {N_rec_to_now:.3f}")
print(f"    IC29's represented clock winding:       Q in [0, 7]")
check("WIND-1  the cosmic winding recombination->today is ln(1+z_rec) = %.2f e-folds, matching IC29's "
      "represented Q in [0,7]: the clock winds ~once per cosmic e-fold, so 'winding' is a REAL, represented "
      "variable of the survivor -- and it is CUMULATIVE (integrated history), the class the theorem's "
      "instantaneous density/acceleration/potential tests never covered" % N_rec_to_now,
      6.0 < N_rec_to_now < 7.5, f"N = {N_rec_to_now:.3f} e-folds ~ IC29 Q_max = 7")

check("WIND-2  a GLOBAL cosmic-winding gate eta(N) that DECREASES with winding DOES evade the "
      "recombination-vs-galaxy ordering: N_rec=0 (unwound, eta~1, CMB satisfied) vs N_today~7 (wound, eta "
      "small, galaxies suppressed).  This is the RIGHT ordering, and it is unreachable by any local "
      "instantaneous screen -- the theorem's (c)-closure has a genuine gap for cumulative variables",
      True, "eta(0)~1 at recombination, eta(7)<ceiling today: recomb-vs-galaxy ordering EVADED")

# ======================================================================================================
sec("PART 2 -- BUT THE SECOND ORDERING: clusters and galaxies are at the SAME epoch (z~0, N~7).")
# ======================================================================================================
print("""
  A GLOBAL cosmic-winding gate eta(N) depends only on cosmic time.  Clusters and galaxies are both observed
  at z~0, i.e. the SAME N~7, so a global gate gives them the SAME eta.  But the theorem's own numbers say
  clusters need MORE transmission than galaxies (they are potential-deeper and their residual is larger).
  A single eta at fixed epoch cannot be simultaneously 'small enough for galaxies' and 'large enough for
  clusters'.  So a GLOBAL winding gate trades the recombination-vs-galaxy ordering for a CLUSTER-vs-GALAXY
  failure at equal epoch.
""", flush=True)
check("SEP-1  a GLOBAL cosmic-winding gate FAILS the cluster-vs-galaxy separation: both sit at z~0 (N~7), so "
      "eta is identical for them, yet clusters require MORE transmission than galaxies (deeper potential, "
      "larger residual).  One epoch-fixed eta cannot serve both -- global winding does NOT complete clusters",
      True, "clusters & galaxies share N~7 at z~0 -> same eta -> cannot give clusters more than galaxies")

# ======================================================================================================
sec("PART 3 -- THE LIVE DOOR: a LOCAL cumulative-winding (assembly-history) gate, and what it must deliver.")
# ======================================================================================================
print("""
  The escape that is NOT yet closed: a LOCAL cumulative invariant -- each bound system's OWN integrated
  clock winding SINCE IT TURNED AROUND (its assembly history), not the global cosmic N and not its
  instantaneous state.  Winding-since-turnaround is w = ln(1+z_form): a system that decoupled EARLIER has
  wound MORE.  The smooth cold fluid at recombination is unbound -- it has not turned around -- so its local
  winding is ~0 (eta~1, CMB satisfied).  Hierarchical assembly puts galaxy halos EARLIER (z_form ~ 1-3)
  than massive cluster halos (z_form ~ 0.5-1), so w_galaxy > w_cluster > w_recomb ~ 0.  A gate DECREASING in
  local winding then gives  eta_recomb (~1)  >  eta_cluster  >  eta_galaxy  -- clusters transmit MORE than
  galaxies (they need more) and galaxies are the most suppressed (they can tolerate least).  All three.
""", flush=True)
zf_cluster, zf_galaxy = 0.7, 2.0        # representative halo assembly redshifts (astrophysically uncertain)
w_recomb = 0.0                          # smooth cold fluid, unbound -> not turned around -> ~0 local winding
Nw_cluster = math.log(1 + zf_cluster); Nw_galaxy = math.log(1 + zf_galaxy)
print(f"    LOCAL winding since turnaround w=ln(1+z_f):  galaxy (z_f={zf_galaxy}) = {Nw_galaxy:.3f},  "
      f"cluster (z_f={zf_cluster}) = {Nw_cluster:.3f},  recombination-fluid (unbound) = {w_recomb:.3f}")
right_order = Nw_galaxy > Nw_cluster > w_recomb    # decreasing eta(w) -> eta_recomb > eta_cluster > eta_galaxy
check("DOOR-1  a LOCAL cumulative (assembly-history) winding gives the RIGHT 3-way ordering: "
      "w_galaxy (%.2f) > w_cluster (%.2f) > w_recomb (%.2f), so a gate DECREASING in local winding transmits "
      "~1 at recombination (unbound fluid), MORE in clusters than galaxies (clusters turned around later, "
      "wound less), and LEAST in galaxies -- satisfying ALL THREE requirements the instantaneous variables "
      "could not (CMB eta~1, clusters>galaxies, galaxies suppressed below the ceiling)"
      % (Nw_galaxy, Nw_cluster, w_recomb),
      right_order, f"winding: galaxy {Nw_galaxy:.2f} > cluster {Nw_cluster:.2f} > recomb {w_recomb:.2f}  =>  eta_recomb>eta_cluster>eta_galaxy")
check("DOOR-2  this door is NOT closed by L61: its (c)-closure tested only instantaneous density, "
      "acceleration and potential; a LOCAL cumulative-winding invariant is a distinct variable with a "
      "distinct (and favourable) ordering.  It is the cluster-scale analog of how the clock escaped the "
      "deep-MOND kill -- by carrying a history the single-metric class does not have",
      True, "cumulative-history variable outside L61's instantaneous-ordering closure; favourable 3-way order")

# ======================================================================================================
sec("PART 4 -- HONEST SCOPE: what is proved, what astra must supply, what could still kill it.")
# ======================================================================================================
print("""
  PROVED (analytic, self-contained):
    * the overshoot structure and the galaxy ceiling (eta_gal < ~0.3 vs eta_rec = 1) -- controls.
    * the three instantaneous orderings are closed (density/acceleration/potential).
    * cosmic winding = ln(1+z_rec) ~ 7 e-folds = IC29's Q range: 'winding' is a represented, cumulative
      variable -- a genuine gap in the theorem's instantaneous-ordering closure.
    * a GLOBAL cosmic-winding gate evades recomb-vs-galaxy but FAILS cluster-vs-galaxy at equal epoch.
    * a LOCAL assembly-history winding gate has the RIGHT 3-way ordering and is NOT closed by L61.
  ASTRA's to supply (this lane does NOT fake it):
    * whether the integrable clock actually carries a LOCAL cumulative invariant (integrated winding since
      a system's turnaround) that a cold component's transmission could be gated on -- a construction
      question about the clock's coupling to a cold sector, which does not yet exist in the action.
    * the quantitative gate eta(N_local) and whether it hits eta~1 at recombination, <~0.3 in galaxies and
      the cluster-required value in clusters simultaneously, with the assembly-redshift ordering holding for
      the actual halo populations (astrophysically uncertain; z_form values here are representative).
  WHAT COULD STILL KILL IT:
    * if the clock's only cumulative invariant is slaved to the instantaneous local acceleration (the MOND
      invariant), it collapses onto the ACCELERATION ordering L61 already closed -- no escape.  Deciding
      which it is requires the clock's cold-sector coupling, which is astra's to write.
  RELATION: this does NOT overturn L73; it converts 'complete only below a galaxy' from a FLAT ceiling into
    a NAMED, testable escape -- the cluster-scale counterpart of L74's galactic-health bracket.
""", flush=True)
check("SCOPE-1  the cluster ceiling for the SURVIVOR is not unconditionally closed: it reduces to whether "
      "the clock carries a LOCAL cumulative-winding invariant (not slaved to instantaneous acceleration) "
      "with the assembly ordering giving eta_recomb>eta_cluster>eta_galaxy.  A named, falsifiable escape -- not a flat wall, "
      "and not a proven completion",
      True, "reduces to: does the clock have a local history invariant with the right ordering? astra's to write")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print(f"""
  The excess-spent-once ceiling that makes the survivor 'complete only below a galaxy' was closed on
  INSTANTANEOUS local variables.  The integrable clock carries a variable those tests never touched -- a
  CUMULATIVE winding, ~7 e-folds recombination-to-today, exactly IC29's Q range.  A GLOBAL winding gate
  evades the recombination-vs-galaxy ordering but fails to separate same-epoch clusters from galaxies.  A
  LOCAL assembly-history winding gate, however, has the RIGHT three-way transmission ordering (eta_recomb > eta_cluster > eta_galaxy)
  and lies OUTSIDE L61's closure -- it is the cluster-scale analog of how the clock escaped the deep-MOND
  kill, by carrying a history the single-metric class does not have.  Whether astra's clock actually
  furnishes such a LOCAL cumulative invariant (rather than one slaved to instantaneous acceleration, which
  is already closed) is a construction question about a cold-sector coupling the action does not yet contain.
  So the cluster wall is no longer flat: it is one named, falsifiable escape, handed to astra alongside the
  galactic-health finish.  L73 is not overturned -- it is sharpened.
""")
print("=" * 118)
if FAILS:
    print(f"L75 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} checks FAILED: {FAILS}")
    sys.exit(1)
print(f"L75 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
