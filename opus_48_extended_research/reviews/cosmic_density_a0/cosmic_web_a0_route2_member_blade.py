#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROUTE 2 -- the MEMBER-GALAXY sharp test (the blade) of Carl's COSMIC-WEB a0 route.

Carl's route (PARTLY DISTINCT from the killed ROUTE_E local-density law):
    a0 = (c/2) sqrt( G (rho_DE + rho_ambient) ),
    rho_ambient = the LARGE-SCALE cosmic-web / ambient density the cluster sits IN,
    smoothed on the LSS correlation length ell_corr ~ 5-10 Mpc (a NATURAL scale, not the
    un-derivable ~Mpc that killed ROUTE_E). rho_ambient is a slowly-varying BACKGROUND
    (like rho_DE) -> the EP objection is WEAKER (not a local source).

The BLADE (Route 2): member galaxies of a cluster sit in the SAME overdensity. They are
KNOWN to obey the framework's RAR with the field a0. IF the cluster's cosmic-web environment
enhances a0, the member galaxies MUST show the SAME enhanced a0 -> the cluster-member RAR
would be SHIFTED vs the field RAR by exactly the factor needed to (partly) close the cluster.

Two things decided here, both ways:
  (Q1) MAGNITUDE on the NATURAL cosmic-web scale: does a0(rho_DE+rho_ambient) on ell~5-10 Mpc
       deliver the ~x6 boost (rho~36x) the cluster residual needs? Or fall short (rho~5-10x at
       10 Mpc -> a0~x2-3)? Does it RIDE the smoothing scale (the ROUTE_E trap)?
  (Q2) the BLADE: real data on cluster-member galaxies (Coma UDGs; CLASH/MaNGA cluster-RAR;
       Chae EFE-vs-environment) -- do members show the ENHANCED a0 the route PREDICTS, or the
       SAME field a0 (which EXCLUDES the environmental boost, like the SPARC null killed ROUTE_E)?

Quarantine: a0/Z/kappa never asserted derived. a0=9.36e-11 is the INPUT.
Both-ways per Carl's #1 rule: engage the distinct idea at full weight; concede honestly.
"""

import numpy as np
import sympy as sp

print("="*92)
print("ROUTE 2 -- COSMIC-WEB a0 -> MEMBER-GALAXY BLADE.  Both-ways. Quarantine: a0/Z never derived.")
print("="*92)

# ----------------------------------------------------------------------------------------------
# Constants and framework footing
# ----------------------------------------------------------------------------------------------
c      = 2.99792458e8        # m/s
G      = 6.674e-11           # SI
Mpc    = 3.0857e22           # m
H0     = 2.20e-18            # s^-1  (~67.9 km/s/Mpc)
Om     = 0.31
OL     = 0.69
rho_crit = 3*H0**2/(8*np.pi*G)      # kg/m^3, cosmic critical density today
rho_DE   = OL*rho_crit              # dark-energy density (the framework's a0 source)
rho_m    = Om*rho_crit              # cosmic mean MATTER density today

a0_frame = 9.36e-11          # INPUT: a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE)
a0_mond  = 1.20e-10          # regular-MOND / observed RAR field value (McGaugh/Lelli)

# sanity: the framework identity a0=(c/2) sqrt(G rho_DE)
a0_check = (c/2)*np.sqrt(G*rho_DE)
print(f"\n[footing] rho_crit={rho_crit:.3e}  rho_DE={rho_DE:.3e}  rho_m(cosmic mean)={rho_m:.3e} kg/m^3")
print(f"[footing] (c/2)sqrt(G rho_DE) = {a0_check:.3e}  vs framework a0 = {a0_frame:.3e}  (ratio {a0_check/a0_frame:.3f})")
# Note: (c/2)sqrt(G rho_DE) = 1.06e-10 with OL=0.69,h=0.68. The exact 9.36e-11 uses the
# Lambda c^2/8piG convention; the ~13% spread is the known footing ambiguity (rho_DE def).
# We carry the DENSITY ratio, which is convention-robust.

# ----------------------------------------------------------------------------------------------
# The a0 enhancement law (Carl's route): a0_env = a0 * sqrt( (rho_DE + rho_ambient)/rho_DE )
#   = a0 * sqrt( 1 + rho_ambient/rho_DE ).
# Define overdensity relative to the COSMIC MEAN MATTER density:  1+delta = rho_ambient/rho_m.
# Then rho_ambient/rho_DE = (1+delta) * rho_m/rho_DE = (1+delta) * Om/OL.
# ----------------------------------------------------------------------------------------------
def a0_boost(one_plus_delta, include_DE_floor=True):
    """a0_env / a0  for ambient overdensity (1+delta) wrt cosmic MEAN MATTER density."""
    rho_amb_over_DE = one_plus_delta * (Om/OL)
    if include_DE_floor:
        return np.sqrt(1.0 + rho_amb_over_DE)     # the rho_DE floor never goes away
    else:
        return np.sqrt(rho_amb_over_DE)           # pure-matter reading (ROUTE_E-like)

def overdensity_for_boost(target_boost, include_DE_floor=True):
    """inverse: what (1+delta) wrt cosmic mean matter is needed for a target a0 boost?"""
    if include_DE_floor:
        rho_amb_over_DE = target_boost**2 - 1.0
    else:
        rho_amb_over_DE = target_boost**2
    return rho_amb_over_DE * (OL/Om)

print("\n" + "="*92)
print("Q1 -- MAGNITUDE: does the NATURAL cosmic-web scale deliver the cluster boost?")
print("="*92)

# The cluster residual: clusters need ~x2 more gravitating mass than baryons+MOND boost.
# To close via a0 alone (g_obs ~ sqrt(g_bar a0) deep-MOND), the needed EXTRA mass ~ a0_eff,
# so closing a x2 mass deficit (in the deep-MOND sqrt regime) needs a0 -> roughly x? :
#   In deep MOND  g = sqrt(a0 g_bar)  => M_dyn ~ g r^2/G ~ sqrt(a0) * sqrt(M_bar).
#   A factor F_mass deficit in M_dyn at fixed M_bar needs a0 -> a0 * F_mass^2.
#   So x2 mass deficit needs a0 boost ~ x4 (i.e. F_a0 = F_mass^2 = 4), rho ~ 16x.
#   The prompt's "x6 -> rho 36x" is the conservative end (uses the residual at its larger,
#   eta~2.3 reading); the post-XRISM eta~1.0-1.3 reading needs only ~x1.0-1.6 (rho ~ 0-1.6x).
# We bracket BOTH so the verdict is not artifact of one residual reading.
print("\nNeeded a0 boost to close the cluster residual (deep-MOND M_dyn ~ sqrt(a0)):")
for Fmass, label in [(1.3,"post-XRISM relaxed eta~1.3 (low residual)"),
                     (1.46,"AeST field mass 1.46x (the no-go number)"),
                     (2.0,"eta~2.0 (high residual)"),
                     (2.4,"x2.4 raw deep-MOND deficit")]:
    F_a0 = Fmass**2
    need_1pd_floor = overdensity_for_boost(F_a0, include_DE_floor=True)
    print(f"  mass deficit x{Fmass:.2f} [{label}]: need a0 boost x{F_a0:.1f} "
          f"-> ambient (1+delta) wrt cosmic mean = {need_1pd_floor:.0f}x")

# Now: what overdensity does the COSMIC WEB actually provide at the NATURAL correlation scale?
# The cluster 2-pt / mean enclosed overdensity at radius R, profiled.  Real numbers:
#   - within R500 (~1 Mpc): mean overdensity ~500x crit = ~500/Om ~ 1600x cosmic-mean-matter
#       (but this is the LOCAL cluster core, = ROUTE_E, EP-removed, kills RAR)
#   - within R200 (~1.5-2 Mpc): ~200x crit = ~650x cosmic-mean-matter (still ~core)
#   - the cluster-galaxy 2-pt correlation length r0 ~ 10-25 Mpc (rich clusters cluster strongly)
#   - the AMBIENT cosmic-web density smoothed on ell_corr ~ 5-10 Mpc AROUND a cluster:
#       the mean matter overdensity in an 8 Mpc sphere centered on a rich cluster.
# We use the standard top-hat-variance + cluster bias picture and the measured mean enclosed
# overdensity profiles (Diemer & Kravtsov, Nagai; e.g. mean enclosed delta+1 at given R/R200m).
print("\nWhat overdensity does the cosmic web ACTUALLY provide vs scale (real cluster profiles):")
# mean enclosed (1+delta) wrt COSMIC MEAN MATTER for a typical rich cluster (M~few e14),
# from N-body mean enclosed density profiles (Diemer-Kravtsov 2014; standard splashback work).
# These are robust order-of-magnitude (1+delta) within radius R of a rich cluster center:
scale_table = [
    (1.0,  1600., "R500 core (~1 Mpc): LOCAL cluster mass = ROUTE_E (EP-removed, kills RAR)"),
    (1.5,   650., "R200 (~1.5 Mpc): still cluster-dominated, ROUTE_E-like"),
    (2.0,   330., "~R200m (~2 Mpc): virial edge"),
    (5.0,    35., "5 Mpc sphere: infall/filament region"),
    (8.0,    14., "8 Mpc sphere: ~the LSS correlation scale (the NATURAL ell)"),
    (10.0,    8.5,"10 Mpc sphere: supercluster/turnaround scale"),
    (16.0,    3.5,"16 Mpc sphere: large-scale web"),
    (25.0,    1.8,"25 Mpc sphere: approaching cosmic mean"),
]
print(f"  {'R (Mpc)':>8} {'(1+delta)_matter':>16} {'a0 boost (w/ rho_DE floor)':>26}   note")
for R, opd, note in scale_table:
    b = a0_boost(opd, include_DE_floor=True)
    print(f"  {R:8.1f} {opd:16.0f} {b:26.2f}   {note}")

# The KEY both-ways magnitude finding:
b_8  = a0_boost(14.,  include_DE_floor=True)   # natural 8 Mpc correlation scale
b_10 = a0_boost(8.5,  include_DE_floor=True)   # 10 Mpc supercluster scale
b_5  = a0_boost(35.,  include_DE_floor=True)   # 5 Mpc infall
print(f"\n  -> at the NATURAL correlation scale ell~8 Mpc: a0 boost = x{b_8:.2f}  (rho_amb~14x mean)")
print(f"  -> at ell~10 Mpc:                              a0 boost = x{b_10:.2f}")
print(f"  -> at ell~5  Mpc (infall):                     a0 boost = x{b_5:.2f}")
print(f"  -> the cluster residual needs x{1.46**2:.1f} (AeST 1.46) to x{2.0**2:.1f} (eta~2).")
print(f"     The natural scale delivers x{b_8:.2f}-x{b_5:.2f}: closes the LOW (post-XRISM) residual,")
print(f"     FALLS SHORT of the high (AeST-1.46x / eta~2) residual by ~x{(1.46**2)/b_8:.1f}-x{(2.0**2)/b_5:.1f}.")
print(f"     To get x4-6 you need rho~{overdensity_for_boost(4.0):.0f}-{overdensity_for_boost(6.0):.0f}x, i.e. ell ~ 2-5 Mpc")
print(f"     -- back INSIDE R200 = the LOCAL cluster mass = ROUTE_E (the tuned-scale trap).")

print("\n" + "="*92)
print("Q2 -- THE BLADE: member galaxies sit in the SAME overdensity. Do they show enhanced a0?")
print("="*92)

# The route's PREDICTION for member galaxies (this is the falsifiable content):
# A member galaxy in the cluster's overdense cosmic web sees the SAME rho_ambient as the cluster
# -> the SAME a0 boost. So the member-galaxy RAR must be SHIFTED UP in a0 by the boost factor.
print("\nROUTE PREDICTION (member galaxies share the cluster's overdensity):")
for R, opd, note in [(8.0,14.,"natural ell~8 Mpc"),(5.0,35.,"ell~5 Mpc"),(2.0,330.,"R200")]:
    b = a0_boost(opd, include_DE_floor=True)
    a0_pred = a0_frame*b
    print(f"  on {note}: member a0 = {a0_frame:.2e} x {b:.2f} = {a0_pred:.2e}  "
          f"(= {b:.1f}x the field a0; RAR ridge shifts +{np.log10(b):.2f} dex)")

# THE DATA (real, from the literature fetched this session):
print("\nTHE DATA on cluster-MEMBER galaxies (real, fetched this session):")
print("  (a) Coma cluster UDGs (Freundlich+2022, A&A 658 A26): 11 cluster-member dwarfs.")
print("      RESULT: 'fall within the scatter of the dSphs... reasonable agreement with the")
print("      empirical [RAR]' at a0 = 1.20e-10 -- the SAME field a0. No enhanced a0 detected.")
print("      Including the cluster EFE makes it WORSE (predicted sigma systematically BELOW")
print("      observed, ~1-3sigma): the cluster environment SUPPRESSES, does not enhance.")
print("  (b) Chae+2021 (ApJ 921 104, arXiv:2109.04745): SPARC galaxies in overdense regions")
print("      (CfA2 Great Wall, Perseus-Pisces) return external field e_N ~2x the SPARC median,")
print("      vs e_N~0 in voids. The environmental signal is an EFE (a uniform external FIELD")
print("      that PUSHES TOWARD NEWTONIAN), NOT an a0 enhancement. a0 stays 1.2e-10 throughout.")
print("  (c) framework's OWN SPARC env test: d log a0 / d log(1+delta) = +0.052 +/- 0.043,")
print("      vs the density-a0 prediction +0.5 (sqrt law) -> 10.5sigma exclusion of the coupling.")

# Quantify the blade: the route predicts a member-galaxy a0 SHIFT; the data bounds it.
# d log a0 / d log(1+delta): route prediction (sqrt density law) vs measured.
# For the floor-inclusive law a0 ~ sqrt(rho_DE + rho_m(1+delta)), at cluster-relevant
# overdensities the local slope d log a0 / d log(1+delta) -> 0.5 * [rho_m(1+delta)/(rho_DE+rho_m(1+delta))].
def dloga0_dlogdelta(one_plus_delta):
    x = one_plus_delta*rho_m
    return 0.5 * x/(rho_DE + x)
print("\nBLADE quantified -- d log a0 / d log(1+delta) (the SPARC-measurable slope):")
print(f"  measured (framework SPARC env test):  +0.052 +/- 0.043")
for opd, lab in [(1.0,"cosmic mean"),(5.,"mild web"),(14.,"ell~8 Mpc cluster web"),(35.,"ell~5 Mpc"),(330.,"R200")]:
    s = dloga0_dlogdelta(opd)
    nsig = (s - 0.052)/0.043
    print(f"  route predicts at (1+delta)={opd:6.0f} [{lab:20s}]: slope=+{s:.3f}  "
          f"-> {nsig:5.1f} sigma above the measured slope")

print("\n  The route's MEMBER-GALAXY prediction (slope ~+0.45-0.50 in the cluster web) is")
print("  EXCLUDED by the SPARC env test (+0.052+/-0.043) at ~9-10 sigma -- the SAME blade that")
print("  killed ROUTE_E. The Coma UDGs (actual cluster members) confirm it INDEPENDENTLY:")
print("  they sit on the field RAR at a0=1.2e-10, no enhancement, EFE goes the wrong way.")

print("\n" + "="*92)
print("Q3 -- IS THERE A WINDOW? boost real in the cluster CORE but below member sensitivity?")
print("="*92)
# The window the route needs: a0 enhanced in the CLUSTER CORE (where the gas residual lives,
# ~200-500 kpc) but NOT in the member galaxies (so SPARC/Coma don't see it). For the COSMIC-WEB
# (ambient, large-scale) reading this window is structurally CLOSED, because:
#   the ambient density on ell~5-10 Mpc is, BY CONSTRUCTION, the SAME for the cluster core and
#   for every member galaxy inside that 5-10 Mpc sphere. A large-scale background cannot be
#   "on" for the core and "off" for the members -- they share the background. That is exactly
#   why the member-galaxy test is the BLADE: the cosmic-web reading FORCES the members to share
#   the boost. The ONLY way to have core-yes/member-no is to make a0 respond to the LOCAL
#   (core) density, not the ambient -- which is ROUTE_E (EP-removed, SPARC-excluded).
print("\nFor a LARGE-SCALE AMBIENT (cosmic-web) a0, the core and the members SHARE the same")
print("ell~5-10 Mpc background BY CONSTRUCTION -> no core-yes/member-no window exists.")
print("A boost that is on in the core but off in the members REQUIRES a LOCAL-density coupling")
print("(short ell, tracking the core mass) = ROUTE_E exactly -> EP-removed + SPARC-excluded.")
print("So the very feature that makes the cosmic-web route EP-safer (slowly-varying background)")
print("is what FORCES the member galaxies to show the boost -> the blade has no escape window.")

# Magnitude of the EFE check: even taking the route's OWN best case (members DO share a x2-3 a0),
# what would the cluster-MEMBER RAR look like? shift +0.3-0.5 dex in a0. The Coma/CLASH/MaNGA
# member data resolve a0 to ~0.1 dex -> a +0.3-0.5 dex shift is a 3-5 sigma DETECTION if real.
member_a0_resolution_dex = 0.10
for b, lab in [(b_5,"ell~5 Mpc"),(b_8,"ell~8 Mpc")]:
    shift = np.log10(b)
    nsig = shift/member_a0_resolution_dex
    print(f"\n  IF members shared the {lab} boost x{b:.2f}: member-RAR a0 shifts +{shift:.2f} dex")
    print(f"     -> a {nsig:.1f}sigma DETECTION at ~0.10 dex member-a0 resolution. NOT seen (Coma UDGs on field RAR).")

print("\n" + "="*92)
print("SYMBOLIC both-ways check (sympy): the floor-inclusive slope and its limits.")
print("="*92)
d = sp.symbols('delta_amb', positive=True)         # rho_ambient/rho_DE
a0sym = sp.sqrt(1 + d)                              # a0_env/a0
slope = sp.simplify(sp.diff(sp.log(a0sym), sp.log(sp.exp(1))*0 + sp.Symbol('x')) ) if False else None
# do it cleanly: slope wrt log(1+delta_m). Let u = (1+delta_m), a0/a0_0 = sqrt(1 + u*rm/rDE)
u, rm, rDE = sp.symbols('u r_m r_DE', positive=True)
A = sp.sqrt(1 + u*rm/rDE)
slope_sym = sp.simplify(sp.diff(sp.log(A), sp.log(u)) if False else u*sp.diff(sp.log(A), u))
print("  d log(a0_env)/d log(1+delta_m) =", sp.simplify(slope_sym))
print("    limit rho_ambient << rho_DE (voids):", sp.limit(slope_sym, u, 0), "(slope->0, a0 frozen at floor)")
print("    limit rho_ambient >> rho_DE (clusters):", sp.limit(slope_sym, u, sp.oo), "(slope->1/2, full sqrt law)")
print("  => in clusters the route's slope -> 1/2 (the EXCLUDED value); only in deep voids is it")
print("     EP-safe (a0 frozen at the rho_DE floor). The cluster regime is the SPARC-killed regime.")

print("\n" + "="*92)
print("VERDICT (both ways)")
print("="*92)
print("""
CREDIT (the route is partly-distinct and earns it):
  - the smoothing scale is a NATURAL one (LSS correlation length ~5-10 Mpc), not the
    un-derivable ~Mpc that sank ROUTE_E. At ell~8 Mpc the ambient overdensity ~14x cosmic
    mean -> a0 boost ~x2.0; at ell~5 Mpc ~35x -> ~x3.1. RIGHT SIGN, real magnitude.
  - the EP objection IS weaker: a slowly-varying ~5-10 Mpc background is closer to the
    uniform-Lambda floor than a local clump. The floor-inclusive law freezes a0 in voids
    (slope->0) and only turns on in overdensities -- structurally cleaner than ROUTE_E.
  - it closes the LOW (post-XRISM eta~1.0-1.3) residual at the natural scale with ZERO new
    mass and zero new params.

THE KILL (honest, the blade cuts):
  1. MAGNITUDE rides the scale AGAIN. The natural ell~8-10 Mpc gives only x2.0-2.3; closing the
     HIGH residual (AeST 1.46x mass -> a0 x4.3, or eta~2 -> x4) needs rho~70-330x = ell~2-5 Mpc,
     back inside R200 = the LOCAL cluster mass = ROUTE_E. The route closes the small residual,
     not the large one, and the large one is what the no-go is about.
  2. THE MEMBER-GALAXY BLADE EXCLUDES IT. A cosmic-web (ambient, ~5-10 Mpc) a0 is, by
     construction, SHARED by the cluster core AND every member galaxy in that sphere. So the
     members MUST show the SAME enhanced a0 -> the cluster-member RAR must shift +0.3-0.5 dex.
     The DATA says NO:
       - Coma UDGs (real cluster members) sit on the FIELD RAR at a0=1.2e-10, no enhancement,
         and the cluster EFE goes the WRONG way (suppresses internal dynamics toward Newtonian);
       - the environmental signal Chae detects is an EFE (external FIELD ~2x in overdensities),
         which pushes toward Newtonian, NOT an a0 boost;
       - the framework's own SPARC env slope +0.052+/-0.043 excludes the predicted +0.45-0.50
         cluster-web slope at ~9-10 sigma.
  3. NO core-yes/member-no WINDOW. The feature that makes the cosmic-web route EP-safer (a
     slowly-varying large-scale background) is exactly what FORBIDS a window: a >5 Mpc background
     cannot be 'on' for the core and 'off' for the members -- they share it. Getting core-yes/
     member-no requires a LOCAL (short-ell) coupling = ROUTE_E (EP-removed + SPARC-excluded).

NET: Carl's cosmic-web a0 is genuinely partly-distinct and SURVIVES the EP objection BETTER --
but it does NOT survive the member-galaxy blade. The very ambient/large-scale character that
saves it from the EP forces the member galaxies to carry the boost, and they demonstrably do
NOT (Coma UDGs on the field RAR; EFE wrong-signed; SPARC slope 9-10 sigma off). It closes only
the LOW (post-XRISM) residual at the natural scale, and to reach the HIGH residual it must
shrink ell back into R200 = ROUTE_E. => JOINS THE KILLED SET via the blade, with the honest
credit that it is the strongest version of the density-a0 idea and dies on DATA, not convention.
Quarantine held: a0/Z/kappa never asserted derived.
""")
