#!/usr/bin/env python3
r"""
ROUTE E (ADVERSARIAL / null_steelman) -- does the dS-Unruh FOUNDATION itself license
ANY local-matter-density / local-curvature dependence of a0, and if so what SCALE does
it PICK OUT?  Steelman the NEGATIVE: NO framework-native scale threads the cluster-core
window (~300-450 kpc) WITHOUT smearing the 0.13-dex SPARC RAR; density-a0 is a CLOSED
FALSIFIER.

This is a DERIVATION question (what does the foundation FORCE), not a candidate-ell scan
(banked: 1/mu=1Mpc, r_DE, r_AH=Gpc all NULL).

FOUNDATION (the spine, taken verbatim):
    T_eff = (hbar/2 pi c kB) sqrt(a^2 + (cH)^2)
    a0 emerges where a^2 = (cH)^2 = the de Sitter / horizon floor.
    a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = cH_Lambda/Z = 9.36e-11.

THE LOAD-BEARING STRUCTURAL QUESTION:
  In T_eff the SECOND argument under the root is (cH)^2 -- a CURVATURE / horizon-acceleration
  scale, NOT a matter density. The density reading a0=(c/2)sqrt(G rho) arises ONLY by the
  Friedmann substitution H^2 = (8pi G/3) rho. So the foundation references a LOCAL scale
  ONLY through whatever "H" (or curvature) is felt locally. Route E asks: what is the
  PHYSICALLY CORRECT local H/curvature a test particle in a cluster core feels -- and what
  length does that pick out?

We enumerate EVERY length the framework derives, compute it at galaxy-disk, cluster-core,
and cosmic densities, and check: (i) does it land in 300-450 kpc, (ii) is rho_disk boosted
(must NOT be) while rho_cluster-core IS (must be), (iii) is it DERIVED or a new tuned input.

Pure numpy/sympy. Quarantine: a0/Z never asserted derived.
"""
import numpy as np
import sympy as sp

# ---------------------------------------------------------------- constants
c    = 2.99792458e8
G    = 6.674e-11
hbar = 1.054571817e-34
kB   = 1.380649e-23
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
Gyr  = 3.1557e16
H0   = 2.184e-18                 # 67.4 km/s/Mpc
Om, OmL = 0.315, 0.685
rho_crit0 = 3*H0**2/(8*np.pi*G)
rho_DE    = OmL*rho_crit0
a0_frame  = 0.5*c*np.sqrt(G*rho_DE)
cH_Lambda = c*H0*np.sqrt(OmL)
Z         = cH_Lambda/a0_frame

print("="*94)
print("(0) THE FOUNDATION AND ITS ONE LOCAL HOOK")
print("="*94)
print(f"  a0 (framework)   = {a0_frame:.4e} m/s^2")
print(f"  cH_Lambda (floor)= {cH_Lambda:.4e} m/s^2 = {Z:.3f} a0")
print(f"  rho_DE           = {rho_DE:.4e} kg/m^3")
print(f"  rho_crit0        = {rho_crit0:.4e} kg/m^3")
print("""
  T_eff = (hbar/2 pi c kB) sqrt(a^2 + (cH)^2).  The SECOND term is a CURVATURE/horizon
  acceleration (cH)^2, NOT a matter density. a0 <-> Lambda is a property of the VACUUM
  (the cosmological constant), uniform in space. The ONLY way a LOCAL matter scale enters
  is if the "H" felt by a local test particle is a LOCAL Friedmann rate H_local^2 =
  (8pi G/3) rho_local -- i.e. if the floor responds to local density. Route E tests
  whether the foundation FORCES that, and at what smoothing length.
""")

# representative densities -- MATTER ONLY (the formula adds the rho_DE floor uniformly below).
# NB: the cosmic-mean and DE-floor rows store the MATTER component, NOT the total, so that the
# uniform "+rho_DE" recovers the correct total (rho_m + rho_DE):
#   cosmic mean : rho_m = Om*rho_crit  ->  rho_m + rho_DE = rho_crit (total) -> a0=0.5c sqrt(G rho_crit)=1.13e-10 (1.21x)
#   DE floor    : rho_m = 0            ->  0     + rho_DE = rho_DE          -> a0=a0_frame (1.00x)
# (Storing rho_crit / rho_DE here directly would double-count DE, since rho_crit already includes it.)
rho_disk      = 1e5 * rho_DE       # galaxy disk local gas+stars ~1e5-1e6 rho_DE
rho_disk_hi   = 1e6 * rho_DE
rho_clcore    = 730 * rho_DE       # cluster-core gas mean ~ R500 overdensity (banked: 500 rho_crit ~ 725-1000 rho_DE)
rho_cl_mpc    = 30  * rho_DE       # cluster smoothed over ~Mpc-ambient (the tuned target)
densities = {
    "galaxy disk (local)  rho_m=1e5 rho_DE": rho_disk,
    "galaxy disk (local hi)rho_m=1e6 rho_DE": rho_disk_hi,
    "cluster core (local)  rho_m=730 rho_DE": rho_clcore,
    "cluster Mpc-ambient   rho_m=30  rho_DE": rho_cl_mpc,
    "cosmic mean  rho_m=Om rho_crit(tot rho_crit)": Om*rho_crit0,
    "dark-energy floor  rho_m=0 (tot rho_DE)"     : 0.0,
}

# ============================================================================
# (1) ENUMERATE EVERY FRAMEWORK-DERIVED LENGTH; where does each land?
# ============================================================================
print("="*94)
print("(1) EVERY FRAMEWORK-NATIVE LENGTH SCALE -- value & whether it lands in 300-450 kpc")
print("="*94)
print("  Target window: 300-450 kpc (cluster-core), must NOT register galaxy disk (~10 kpc).\n")

WINDOW = (300*kpc, 450*kpc)
def flag(L):
    if WINDOW[0] <= L <= WINDOW[1]:
        return "  <-- IN WINDOW"
    if L < 50*kpc:   return "  (galaxy-scale: would boost disks -> breaks RAR)"
    if L > 3*Mpc:    return "  (>>Mpc: washes to cosmic -> no differential boost)"
    return ""

scales = []

# 1. dS-Unruh apparent horizon at the floor: r = c/H_local, self-consistent
print("  --- A. the de Sitter / apparent-horizon radius r_AH = c/H_local (the BATH coherence scale) ---")
for label, rho in densities.items():
    Hloc = np.sqrt((8*np.pi*G/3)*(rho + rho_DE))   # local Friedmann incl. DE floor
    r_AH = c/Hloc
    print(f"    {label:38s}: r_AH = {r_AH/Mpc:10.4g} Mpc = {r_AH/kpc:11.4g} kpc{flag(r_AH)}")
scales.append(("r_AH=c/H_local", "Gpc-to-100Mpc; never <199 Mpc even at R500", "cosmological"))

# 2. The free-fall length R* = c * t_dyn (the framework's own R* in a0=c^2/2R*)
print("\n  --- B. the framework free-fall length R* = c^2/(2 a0) = c/(Z H_local) ---")
for label, rho in densities.items():
    Hloc = np.sqrt((8*np.pi*G/3)*(rho + rho_DE))
    a0_loc = 0.5*c*np.sqrt(G*(rho+rho_DE))
    Rstar = c**2/(2*a0_loc)
    print(f"    {label:38s}: R* = {Rstar/Mpc:10.4g} Mpc{flag(Rstar)}")
scales.append(("R*=c^2/2a0", "Gpc cosmic; shrinks only at huge rho", "cosmological"))

# 3. AeST scalar Compton wavelength 1/mu ~ 1 Mpc (CMB-pinned) -- FIXED, not density-dependent
print("\n  --- C. AeST scalar Compton wavelength 1/mu ~ 1 Mpc (CMB-pinned, FIXED) ---")
inv_mu = 1.0*Mpc
print(f"    1/mu = {inv_mu/Mpc:.3f} Mpc = {inv_mu/kpc:.0f} kpc{flag(inv_mu)}")
print(f"      (banked NULL: at 1 Mpc breaks RAR +34% AND over-closes clusters to eta~0.47)")
scales.append(("1/mu (AeST Compton)", "1 Mpc fixed, CMB-pinned", "fixed-Mpc, banked NULL"))

# 4. r_DE level-set radius (galaxy ~275 kpc, cluster 7-26 Mpc) -- self-normalizes
print("\n  --- D. r_DE level-set (rho_bar(<r)=rho_DE): galaxy 275 kpc, cluster 7-26 Mpc ---")
print(f"    galaxy r_DE ~ 275 kpc{flag(275*kpc)}  -- BUT self-normalizes to rho_eff=2 rho_DE (banked NULL)")
print(f"    cluster r_DE ~ 7-26 Mpc{flag(15*Mpc)} -- dilutes overdensity to 2 rho_DE (banked NULL)")
scales.append(("r_DE level-set", "galaxy 275kpc/cluster 7-26Mpc; self-normalizes to 2rho_DE", "DERIVED but zero differential boost"))

# 5. Z-geometry / compactification scales (the (T^2)^3 modulus) -- dimensionless, no length
print("\n  --- E. Z-geometry / compactification modulus (32pi/3) -- DIMENSIONLESS ---")
print(f"    Z^2 = 32pi/3 = {32*np.pi/3:.4f} is a pure number (a coupling), sets NO length scale.")
scales.append(("Z-geometry modulus", "dimensionless coupling, no length", "no length scale"))

# 6. The MOND radius r_M = sqrt(GM/a0) -- tracks the SYSTEM
print("\n  --- F. MOND radius r_M = sqrt(GM/a0) (tracks the system) ---")
for label, M in [("galaxy M=6e10 Msun", 6e10*Msun), ("cluster M=5e14 Msun", 5e14*Msun)]:
    r_M = np.sqrt(G*M/a0_frame)
    print(f"    {label:24s}: r_M = {r_M/kpc:10.4g} kpc{flag(r_M)}")
print(f"      (banked NULL: r_M smooths each galaxy over its OWN disk -> a0 ~300x too big -> kills RAR)")
scales.append(("r_M=sqrt(GM/a0)", "galaxy ~14kpc/cluster ~550kpc; tracks system -> local clumpy reading", "banked NULL"))

# 7. AeST kinetic / k-essence scale -- the J(Y) free-function scale; tied to a0 (galaxy)
print("\n  --- G. AeST kinetic scale (the free function J's scale ~ a0) -> galaxy-internal ---")
print(f"    The AeST kinetic free-function turns on at g ~ a0; its length on a galaxy is r_M itself")
print(f"    (~10-30 kpc). It is the GALAXY-INTERNAL transition, NOT a cluster-core 300-450 kpc scale.")
scales.append(("AeST kinetic scale", "~r_M, galaxy-internal (10-30 kpc)", "galaxy-internal, not 300-450kpc"))

# ============================================================================
# (2) THE STRUCTURAL GAP: cosmological/CMB scales vs the cluster-core window
# ============================================================================
print()
print("="*94)
print("(2) THE STRUCTURAL SCALE GAP -- every derived scale is COSMOLOGICAL or CMB-pinned or SYSTEM-tracking")
print("="*94)
print(f"""
  Cluster-core window:        300-450 kpc  = 0.30-0.45 Mpc
  Smallest DERIVED COSMIC:    1/mu = 1 Mpc (CMB-pinned)   -> 2.2-3.3x TOO BIG
  Next derived cosmic:        r_AH >= 199 Mpc (R500)      -> ~440-660x TOO BIG
  r_DE (galaxy):              275 kpc -- IN range numerically, BUT self-normalizes (no boost)
  System-tracking (r_M):      galaxy 14 kpc / cluster 550 kpc -- WRONG: boosts disks, kills RAR

  There is a 2.2-3.3x GAP between the smallest cosmic/CMB-pinned framework scale (1 Mpc) and
  the top of the cluster-core window (450 kpc), and a ~660x gap to the horizon scale. The ONLY
  framework scales that fall NEAR 300-450 kpc are SYSTEM-TRACKING (r_M, r_DE), and those either
  smooth a galaxy over its own disk (r_M -> kills RAR) or self-normalize away the boost (r_DE).
""")

# ============================================================================
# (3) THE DEEPER POINT: does the FLOOR even respond to LOCAL MATTER? (sympy)
# ============================================================================
print("="*94)
print("(3) DOES THE dS-UNRUH FLOOR RESPOND TO LOCAL MATTER AT ALL? -- the foundational sign check")
print("="*94)
print("""
  The foundation's floor is (cH)^2. Two readings of "H":
    (i)  H = H_Lambda = the COSMOLOGICAL constant rate (vacuum, uniform)  -> a0 uniform, NO local dep.
    (ii) H_local^2 = (8pi G/3) rho_local  -> a0 = (c/2) sqrt(G rho_local) -> local dep (density-a0).
  Reading (ii) is the density-a0 superset. But what is the CORRECT local curvature a particle feels?
""")
# The covariant content: the floor is set by the BACKGROUND de Sitter curvature R = 12 H_Lambda^2/c^2
# (a property of Lambda). A LOCAL matter overdensity sources NEWTONIAN/tidal curvature, not an
# isotropic de Sitter (cosmological-constant) curvature. Compute the Kretschmann/Ricci comparison.
print("  Covariant test: the dS-Unruh floor is the ISOTROPIC de Sitter curvature from Lambda.")
print("  A local matter clump sources a TIDAL (Weyl/Newtonian) field, NOT an isotropic dS bath.\n")
# de Sitter (cosmological-constant) Ricci scalar:  R_dS = 4 Lambda = 12 H_Lambda^2/c^2
Lambda = 3*OmL*H0**2/c**2
R_dS = 4*Lambda
# Local matter Ricci scalar (trace of Einstein eq):  R_matter = 8 pi G rho / c^2  (kappa rho)
print(f"  {'environment':38s}{'R_matter=8piG rho/c^2':>22}{'R_dS=4Lambda':>16}{'ratio R_m/R_dS':>16}")
for label, rho in densities.items():
    R_matter = 8*np.pi*G*rho/c**2
    print(f"  {label:38s}{R_matter:>22.3e}{R_dS:>16.3e}{R_matter/R_dS:>16.3e}")
print("""
  READING (the both-ways crux): at the COSMIC mean, R_matter ~ R_dS (order unity) -- the
  Friedmann substitution H^2=(8piG/3)rho is then legitimate and gives a0=(c/2)sqrt(G rho_crit)
  ~ 1.13e-10 (the rho_total footing). But IN A CLUSTER CORE R_matter/R_dS ~ 700, and IN A
  GALAXY DISK ~ 1e5-1e6: the LOCAL curvature is matter-tidal, ANISOTROPIC, and DWARFS the
  isotropic dS floor. The foundation's floor (cH_Lambda)^2 is the curvature of the VACUUM
  (Lambda) -- it does NOT pick up local matter curvature UNLESS you re-interpret "H" as a
  local Friedmann rate, which (a) requires a smoothing volume (the ell problem), and (b) is
  the WRONG curvature character (tidal/anisotropic, not isotropic-dS).
""")

# ============================================================================
# (4) THE EQUIVALENCE-PRINCIPLE / FREE-FALL OBSTRUCTION (the deepest negative)
# ============================================================================
print("="*94)
print("(4) THE FREE-FALL OBSTRUCTION -- why a LOCAL density cannot set the inertial floor")
print("="*94)
print("""
  The dS-Unruh temperature is felt by an ACCELERATED particle relative to the cosmic vacuum.
  A test star in a galaxy/cluster is in FREE FALL in the local gravitational field -- by the
  equivalence principle it feels NO local Unruh heat from the local matter's Newtonian field
  (a freely-falling frame is locally inertial). The ONLY irreducible bath it cannot fall out
  of is the COSMOLOGICAL de Sitter horizon (Lambda) -- you cannot free-fall away from the
  cosmological constant. THIS is precisely why a0 <-> Lambda and NOT a0 <-> rho_local:

    * local matter curvature is REMOVABLE by going to the free-fall frame (EP) -> no floor shift
    * the dS/Lambda curvature is IRREDUCIBLE (global, no frame removes it) -> sets the universal floor

  => the foundation STRUCTURALLY forbids a local-matter floor. The density-a0 reading
     a0=(c/2)sqrt(G rho_local) is NOT licensed by the dS-Unruh derivation; it is an
     EXTRAPOLATION (the Friedmann substitution applied to a local volume) that the EP
     specifically blocks at the sub-horizon scale.
""")

# ============================================================================
# (5) THE SIGN CHECK ON ANY DERIVED LOCAL SCALE THAT *DOES* EXIST
# ============================================================================
print("="*94)
print("(5) SIGN CHECK -- IF the floor did respond to local curvature, which way?")
print("="*94)
print("""
  Suppose (Route C, apparent-horizon) the LOCAL apparent horizon shrinks in an overdensity:
  a bound overdense region has a SMALLER apparent horizon -> LARGER c/r_AH -> LARGER floor
  cH_local -> LARGER a0. Sign: BOOSTS a0 in clusters. RIGHT sign for the cluster fix.
  BUT (banked Route C 'wrong-sign apparent horizon'): the collapsed/bound region's relevant
  causal scale is set by its TURNAROUND, and the matter-era apparent horizon c/H(z) GROWS in
  the past and the bound-region correction goes the OTHER way for the inferred a0(z) at fixed
  comoving scale. The net banked result: the apparent-horizon local correction is wrong-signed
  or null for the cluster fix. We re-verify the magnitude is in any case far too small:
""")
# magnitude: even at R500 (730 rho_DE), the apparent horizon is 199 Mpc -- the floor barely moves
for label, rho in [("cluster R500 (730 rho_DE)", rho_clcore), ("galaxy disk (1e5 rho_DE)", rho_disk)]:
    Hloc = np.sqrt((8*np.pi*G/3)*(rho+rho_DE))
    a0_loc = 0.5*c*np.sqrt(G*(rho+rho_DE))
    r_AH = c/Hloc
    print(f"    {label:30s}: r_AH={r_AH/Mpc:8.3g} Mpc, a0_local/a0_frame = {a0_loc/a0_frame:8.2f}x")
print("""
  At the LOCAL density the a0 boost IS large (27x cluster core, 316x galaxy disk) -- but that
  is the LOCAL/clumpy reading that the SPARC null (d log a0/d log(1+delta)=+0.052 vs +0.5,
  10.5 sigma) ALREADY excludes for galaxies. The boost is right-signed for clusters ONLY if
  you can smooth so the galaxy disk does NOT see it -- and no derived smoothing scale does that.
""")

# ============================================================================
# (6) THE EMPIRICAL NAIL
# ============================================================================
print("="*94)
print("(6) THE EMPIRICAL NAIL -- the framework's OWN SPARC environment null")
print("="*94)
slope_obs = 0.052; slope_err = 0.043; slope_pred = 0.5
nsig = (slope_pred - slope_obs)/slope_err
print(f"  d log a0 / d log(1+delta) = {slope_obs:+.3f} +- {slope_err:.3f}  (framework SPARC env test)")
print(f"  density-a0 (a0 ~ sqrt(rho_local)) predicts +0.5")
print(f"  => {nsig:.1f} sigma EXCLUSION of the per-galaxy density coupling.")
print(f"  Corroborated: Li et al. (SPARC) + 2026 A&A 'no credible variation in a0'; Bilek 2026;")
print(f"  Route C wrong-sign apparent horizon. The per-galaxy local-density floor is DEAD.")

# ============================================================================
# (7) VERDICT TABLE
# ============================================================================
print()
print("="*94)
print("(7) VERDICT -- every framework-native scale vs the cluster-core window")
print("="*94)
print(f"  {'scale':24s}{'value':44s}{'status'}")
for name, val, status in scales:
    print(f"  {name:24s}{val:44s}{status}")
print(f"""
  NONE lands in 300-450 kpc as a DERIVED scale that boosts cluster cores WITHOUT boosting
  galaxy disks. The cosmic/CMB scales (r_AH, 1/mu) are 2.2-660x too big; the system-tracking
  scales (r_M, r_DE) either kill the RAR or self-normalize. The foundation's floor is the
  IRREDUCIBLE dS/Lambda curvature, which the equivalence principle forbids from responding to
  local matter. CONCLUSION: density-a0 is a CLOSED FALSIFIER -- a real, distinctive, falsifiable
  signature that the framework's OWN foundation does NOT license and the SPARC data (10.5 sigma)
  already disfavors.
""")
