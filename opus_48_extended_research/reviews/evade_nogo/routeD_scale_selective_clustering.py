#!/usr/bin/env python3
# =============================================================================
# ROUTE D -- THE RECONCILIATION
# Can the framework's AeST ghost-condensate dark sector cluster in CLUSTER cores
# (~Mpc) while staying SMOOTH in GALAXY disks (~kpc), preserving BOTH the CMB
# 3rd-peak fit AND the galaxy RAR?
#
# THE EVASION TO TEST (Carl's candidate loophole the no-go may have missed):
#   A ghost condensate is NOT just cs^2->0. It has a k^4 dispersion
#       omega^2 = (B/M^2) k^4  - A k^2      (ACLM 2004, hep-th/0312099)
#   The k^2 term is the GRAVITATIONAL back-reaction (Jeans), NEGATIVE-signed.
#   This sets a FINITE Jeans wavenumber k_J = sqrt(A M^2 / B) below which the
#   mode is unstable (CLUSTERS) and above which it is stabilized (SMOOTH).
#   IF k_J sits between galaxy (k~few..30 /Mpc) and cluster (k~1 /Mpc) scales,
#   the field orders BY SCALE not by density -> sidesteps "galaxies are denser".
#
# THE CATCH (test honestly, banked Door-A pin DOORA_PIN_REAL_COEFFICIENTS):
#   In the framework's NAMED host (AeST khronon, Blanchet-Skordis 2404.06584
#   Sec 6.2) the propagating-quadratic k^4 coefficient is B = 0 EXACTLY
#   ("there are no higher derivative interaction terms in the action which are
#   also quadratic in the fields"; the dark-matter scalar has dispersion w=0).
#
# This script computes, both ways:
#   (1) The SCALE WINDOW the evasion needs (galaxy vs cluster wavenumbers).
#   (2) The k^4 Jeans scale k_J in the IDEALIZED ghost condensate (B=O(1)) as a
#       function of the GC scale M -- does ANY M put k_J in the window AND keep
#       the wrong-sign side correct (unstable at cluster k, stable at galaxy k)?
#   (3) The DIRECTION test: in AeST/ACLM, k_J = mu (the screening scale).
#       Below k_J the mode is UNSTABLE; above k_J STABLE. Map galaxy & cluster
#       k vs k_J to see which side each lands on.
#   (4) The B=0 host: with B=0 there is NO k^4 stabilization -> the mode is the
#       cs^2->0 khronon. Recompute the threshold the no-go used (rho > mu^2/4piG)
#       and the galaxy-vs-cluster density ordering. Does mu give scale help?
#   (5) The mu screening term: mu^-1 >~ 1 Mpc forced by galaxy MOND. Does the
#       finite screening scale itself give cluster-on/galaxy-off clustering?
#   (6) The CMB constraint: the 3rd-peak fit requires cs^2->0 (GDM-like) at
#       CMB k. Is cs^2->0 forced at ALL sub-horizon k, or only large scales?
#
# Both ways (Carl #1 rule): if a REAL mechanism clusters-in-clusters AND keeps
# galaxies smooth AND keeps the CMB fit -> the no-go OVERTURNS. If it fails
# (B=0, scale out of window, CMB forces cs^2->0 everywhere) -> no-go STANDS.
# Quarantine: a0/Z/kappa/I0 never derived.
# =============================================================================

import numpy as np
import sympy as sp

print("="*78)
print("ROUTE D -- scale-selective clustering: can AeST cluster-clump but galaxy-smooth?")
print("="*78)

# ---------------------------------------------------------------------------
# Physical constants (SI)
# ---------------------------------------------------------------------------
G      = 6.674e-11            # m^3 kg^-1 s^-2
c      = 2.998e8             # m/s
Mpc    = 3.086e22            # m
kpc    = 3.086e19            # m
Msun   = 1.989e30           # kg
hbar   = 1.055e-34
eV     = 1.602e-19          # J
MPl_J  = 2.435e18 * 1e9 * eV # reduced Planck mass in J (2.435e18 GeV)
# rho_crit (h=0.674)
H0 = 67.4 * 1e3 / Mpc        # s^-1
rho_crit = 3*H0**2/(8*np.pi*G)   # kg/m^3
print(f"\nrho_crit = {rho_crit:.3e} kg/m^3   H0 = {H0:.3e} /s")

# ---------------------------------------------------------------------------
# (1) THE SCALE WINDOW the evasion REQUIRES
#     cluster cores ~ a few hundred kpc to ~Mpc ; galaxy disks ~ kpc to tens kpc
#     Convert to comoving-ish wavenumbers k = 2pi / lambda (physical scale here).
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("(1) THE REQUIRED SCALE WINDOW (what 'cluster-clumpy, galaxy-smooth' demands)")
print("-"*78)

# Characteristic physical scales of the structures
R_galaxy_disk   = 10*kpc     # galaxy disk scale where RAR is set
R_galaxy_outer  = 30*kpc     # outer rotation curve
R_cluster_core  = 420*kpc    # the residual radius (banked target, <420 kpc rich)
R_cluster       = 1.0*Mpc    # cluster scale

def k_of_R(R):   # k = 2pi/lambda, lambda ~ 2R (a perturbation spanning the object)
    return np.pi / R          # k = pi/R  (half-wavelength = R); /Mpc below

for name,R in [("galaxy disk (10 kpc)",R_galaxy_disk),
               ("galaxy outer (30 kpc)",R_galaxy_outer),
               ("cluster core (420 kpc)",R_cluster_core),
               ("cluster (1 Mpc)",R_cluster)]:
    k = k_of_R(R)
    print(f"  {name:24s}: k = pi/R = {k*Mpc:8.2f} /Mpc   (lambda~{2*R/Mpc:.3f} Mpc)")

print("""
  REQUIREMENT for the evasion to work:
    CLUSTER scales must CLUSTER  -> need k_cluster  <  k_Jeans  (unstable side)
    GALAXY  scales must be SMOOTH-> need k_galaxy   >  k_Jeans  (stable side)
  Since k ~ 1/R and galaxies are SMALLER than clusters, galaxy k > cluster k.
  ==> The Jeans wavenumber k_J must sit BETWEEN:
        k_cluster(~7.5/Mpc at 420kpc, ~3/Mpc at 1Mpc) < k_J < k_galaxy(~100-300/Mpc)
  i.e. lambda_J BETWEEN ~tens of kpc (galaxy) and ~hundreds of kpc-Mpc (cluster).
  Window center: k_J ~ 10-30 /Mpc, i.e. lambda_J ~ 0.2-0.6 Mpc (200-600 kpc).""")

k_cluster_core = k_of_R(R_cluster_core)*Mpc   # /Mpc
k_cluster_1Mpc = k_of_R(R_cluster)*Mpc
k_galaxy_outer = k_of_R(R_galaxy_outer)*Mpc
k_galaxy_disk  = k_of_R(R_galaxy_disk)*Mpc
print(f"\n  Window (per-Mpc): need {k_cluster_1Mpc:.2f} (1Mpc cluster) < k_J < {k_galaxy_outer:.1f} (30kpc galaxy)")
print(f"                    tightest: {k_cluster_core:.2f} (420kpc core) < k_J < {k_galaxy_disk:.1f} (10kpc disk)")

# ---------------------------------------------------------------------------
# (2) THE k^4 JEANS SCALE in the IDEALIZED ghost condensate (B = O(1))
#     ACLM dispersion (banked verbatim, hep-th/0312099, mixed with gravity):
#        omega^2 = (B/M^2) k^4 - A k^2 ,  A = M^2/(2 MPl^2) * (B units),
#     practically (banked PK_K4_SIGNATURE, sympy-exact):
#        k_J = M^2 / (sqrt(2) MPl)   [the ACLM antigravity / graviton-mass scale]
#     and this k_J = AeST's mu exactly.
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("(2) k^4 JEANS SCALE in the IDEALIZED ghost condensate (B=O(1)): k_J = M^2/(sqrt2 MPl)")
print("-"*78)

MPl_kg = MPl_J / c**2        # reduced Planck mass in kg ... but we want energy units
# Work in energy units: MPl in eV, M in eV, k_J in eV then convert to /Mpc via hbar c.
MPl_eV = 2.435e27            # reduced Planck mass = 2.435e18 GeV = 2.435e27 eV
hbarc_eV_m = 1.973e-7        # hbar*c in eV*m  (197.3 MeV*fm)
def kJ_per_Mpc_from_M(M_eV):
    kJ_eV = M_eV**2 / (np.sqrt(2)*MPl_eV)     # in eV (inverse length in natural units)
    kJ_per_m = kJ_eV / hbarc_eV_m              # /m
    return kJ_per_m * Mpc                      # /Mpc

print("  k_J(M) = M^2/(sqrt2 MPl), self-consistent with mu^-1 = (sqrt2 MPl mu)^... :")
print(f"  {'M [eV]':>10} | {'k_J [/Mpc]':>12} | {'lambda_J = mu^-1 [Mpc]':>22} | in window?")
M_grid = [0.01, 0.04, 0.08, 0.13, 0.148, 0.20, 0.30, 0.50, 1.0]
for M_eV in M_grid:
    kJ = kJ_per_Mpc_from_M(M_eV)
    lamJ = 1.0/kJ if kJ>0 else np.inf
    inwin = (k_cluster_1Mpc < kJ < k_galaxy_outer)
    tag = "YES (in window!)" if inwin else ("k_J too BIG (smooths clusters too)" if kJ>k_galaxy_outer else "k_J too SMALL (clusters galaxies)")
    print(f"  {M_eV:10.3f} | {kJ:12.4f} | {lamJ:22.4f} | {tag}")

print("""
  NOTE: lambda_J = mu^-1 = 1/k_J. The galaxy-MOND constraint mu^-1 >~ 1 Mpc
  (Skordis-Zlosnik 2007.00082, verbatim 'mu^-1 >~ 1 Mpc') FORCES lambda_J >~ 1 Mpc,
  i.e. k_J <~ 1 /Mpc. Compare the window: need k_J between ~3 and ~100 /Mpc.""")

# Solve: what M (and hence mu) would put k_J IN the window? And does it clash with galaxy MOND?
print("\n  Inverting: what k_J does each window edge demand, and is it galaxy-legal?")
for target_kJ, label in [(k_cluster_1Mpc,"cluster-edge (1 Mpc)"),
                         (k_cluster_core,"core-edge (420 kpc)"),
                         (10.0,"window center ~10/Mpc"),
                         (k_galaxy_outer,"galaxy-edge (30 kpc)")]:
    lamJ = 1.0/target_kJ      # Mpc -> this is mu^-1
    # M from k_J = M^2/(sqrt2 MPl):  M = sqrt(sqrt2 MPl k_J)
    kJ_per_m = target_kJ/Mpc
    kJ_eV = kJ_per_m*hbarc_eV_m
    M_eV = np.sqrt(np.sqrt(2)*MPl_eV*kJ_eV)
    galaxy_legal = (lamJ >= 1.0)   # mu^-1 >= 1 Mpc required for galaxy MOND
    print(f"  k_J={target_kJ:6.2f}/Mpc ({label:22s}): mu^-1={lamJ:.4f} Mpc, M={M_eV:.4f} eV"
          f"  -> galaxy-MOND-legal (mu^-1>=1Mpc)? {'YES' if galaxy_legal else 'NO (kills galaxy MOND)'}")

# ---------------------------------------------------------------------------
# (3) THE DIRECTION TEST -- does the unstable side land on CLUSTERS or GALAXIES?
#     ACLM: omega^2 = (B/M^2)k^4 - A k^2.  Below k_J: omega^2 < 0 UNSTABLE (clumps).
#     Above k_J: omega^2 > 0 STABLE (smooth). So:
#       k < k_J  -> clusters/large scales CLUMP   (GOOD: cluster-clumpy)
#       k > k_J  -> galaxies/small scales SMOOTH  (GOOD: galaxy-smooth)
#     The SIGN structure is RIGHT for the evasion. The only question is k_J location.
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("(3) DIRECTION TEST: the SIGN structure of the ghost-condensate Jeans is CORRECT")
print("-"*78)
print("""  ACLM: omega^2 = (B/M^2) k^4 - A k^2,  A = (gravitational back-reaction)>0.
    k < k_J : omega^2<0  UNSTABLE -> CLUMPS   (large scales = clusters)  <-- want this
    k > k_J : omega^2>0  STABLE   -> SMOOTH   (small scales = galaxies)  <-- want this
  ==> The evasion's PREMISE IS PHYSICALLY SOUND: a k^4 ghost condensate orders
      BY SCALE (clumps big, smooths small) -- NOT by density. IF k_J were in the
      window (~3-100 /Mpc), the no-go's 'galaxies are denser so clump more' would
      be SIDESTEPPED. The mechanism is real; everything rides on (a) where k_J is
      and (b) whether B!=0 so the k^4 stabilization EXISTS at all.""")

# But: pin k_J for the galaxy-forced mu.
print("  But k_J = mu, and galaxy MOND forces mu^-1 >~ 1 Mpc  =>  k_J <~ 1 /Mpc:")
for lam_mu in [1.0, 3.0, 10.0, 30.0]:    # mu^-1 in Mpc (galaxy-favored = larger)
    kJ = 1.0/lam_mu
    # which side do galaxy & cluster land?
    gal = "STABLE/smooth (k_gal>k_J GOOD)" if k_galaxy_outer>kJ else "UNSTABLE/clump (BAD)"
    clu_core = "UNSTABLE/clump (k<k_J GOOD)" if k_cluster_core<kJ else "STABLE/smooth (BAD: cluster smoothed too!)"
    clu_1mpc = "UNSTABLE/clump GOOD" if k_cluster_1Mpc<kJ else "STABLE/smooth BAD"
    print(f"  mu^-1={lam_mu:5.1f} Mpc (k_J={kJ:.3f}/Mpc): galaxy(30kpc,k={k_galaxy_outer:.0f})={gal}")
    print(f"        cluster core(420kpc,k={k_cluster_core:.1f}) -> {clu_core}")
    print(f"        cluster (1Mpc,    k={k_cluster_1Mpc:.1f}) -> {clu_1mpc}")

print("""
  VERDICT of the direction test: with the galaxy-forced mu^-1>~1 Mpc (k_J<~1/Mpc),
  BOTH galaxy AND cluster-core scales have k > k_J -> BOTH land on the STABLE side.
  The k^4 mechanism SMOOTHS the field on ALL sub-Mpc scales -- it does NOT clump
  in cluster CORES (420 kpc, k~7.5/Mpc >> k_J~1/Mpc). The Jeans scale is TOO BIG
  (mu^-1 too large): it smooths clusters cores along WITH galaxies.
  The window needs k_J ~ 3-100 /Mpc; AeST gives k_J <~ 1 /Mpc. OUT OF WINDOW by
  one-to-two orders -- and on the WRONG side (cluster cores get smoothed).""")

# ---------------------------------------------------------------------------
# (4) THE B=0 HOST -- with B=0 there is NO k^4 stabilization at all.
#     The no-go's threshold: growth gated by rho > mu^2/(4 pi G) (mass term).
#     Recompute galaxy-vs-cluster density ordering on the framework footing.
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("(4) THE B=0 HOST (Blanchet-Skordis Sec 6.2): NO propagating k^4 -> cs^2->0 khronon")
print("-"*78)

# The no-go threshold rho_thresh = mu^2/(4 pi G), with mu^-1 = 1 Mpc (the SMALLEST
# galaxy-legal screening scale -> the LARGEST mu -> the HIGHEST threshold = most
# favorable to the evasion).
for lam_mu_Mpc in [1.0, 3.0, 10.0]:
    mu = 1.0/(lam_mu_Mpc*Mpc)              # /m
    rho_thresh = mu**2/(4*np.pi*G)          # kg/m^3
    print(f"\n  mu^-1 = {lam_mu_Mpc} Mpc -> rho_thresh = mu^2/(4piG) = {rho_thresh:.3e} kg/m^3 "
          f"= {rho_thresh/rho_crit:.3e} rho_crit")
# densities (banked): galaxy disk ~9.7e13 rho_crit; cluster core ~2.6e13 rho_crit
rho_gal_disk_x   = 9.7e13     # x rho_crit (banked)
rho_clu_core_x   = 2.6e13     # x rho_crit (banked)
print(f"\n  Banked densities: galaxy disk = {rho_gal_disk_x:.2e} rho_crit ; "
      f"cluster core = {rho_clu_core_x:.2e} rho_crit")
print(f"  galaxy/cluster density ratio = {rho_gal_disk_x/rho_clu_core_x:.2f}x  (galaxy DENSER)")
mu1 = 1.0/(1.0*Mpc); rho_thr1 = mu1**2/(4*np.pi*G)/rho_crit
print(f"""
  With B=0 the ONLY gate is the mass term rho > mu^2/4piG = {rho_thr1:.3e} rho_crit
  (at the most-favorable mu^-1=1 Mpc). BOTH galaxy ({rho_gal_disk_x:.1e}) AND cluster
  core ({rho_clu_core_x:.1e}) blow past it by ~13 orders. And the galaxy is {rho_gal_disk_x/rho_clu_core_x:.1f}x
  DENSER -> the field clumps MORE in galaxies. The ordering is BY DENSITY and it is
  BACKWARDS. With B=0 there is no k^4 scale to rescue it. THE NO-GO STANDS.""")

# ---------------------------------------------------------------------------
# (5) DOES THE mu SCREENING ITSELF GIVE SCALE-DEPENDENT HELP?
#     mu screens scales LARGER than mu^-1 (~1 Mpc). i.e. it suppresses the field
#     response at k < mu, NOT at k > mu. That is the OPPOSITE of what we need:
#     it would smooth >Mpc (super-cluster) scales and leave sub-Mpc (cluster core
#     AND galaxy) UNSCREENED. So mu helps neither direction usefully.
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("(5) DOES THE mu SCREENING GIVE SCALE-DEPENDENT CLUSTERING? -- NO (wrong scale)")
print("-"*78)
print(f"""  mu^-1 >~ 1 Mpc screens scales LARGER than ~1 Mpc (k < mu ~ 1/Mpc).
  Cluster cores (420 kpc, k~7.5/Mpc) and galaxy disks (10 kpc, k~100/Mpc) are
  BOTH at k >> mu = UNSCREENED. The mu term changes the >Mpc (supercluster) regime,
  not the cluster-core-vs-galaxy contrast the no-go is about. mu cannot turn
  clustering ON in cluster cores while OFF in galaxies -- both are sub-mu^-1.""")

# ---------------------------------------------------------------------------
# (6) THE CMB CONSTRAINT -- is cs^2->0 forced at ALL sub-horizon k?
#     SZ21 fits the Planck 3rd peak as GDM-like with k-dependent cs^2 (their words).
#     The massive scalar mode omega^2 = cs^2 k^2 + M^2 has cs^2 = O(1) (eq.30) but
#     the COLD DARK MATTER mode (the one doing the 3rd-peak / a^-3 dust job) is the
#     gapless ω=0 khronon with cs^2->0. To fit the 3rd peak it must behave as cold
#     dust (cs^2->0) down to the CMB damping scale k~0.2/Mpc. Check the implication.
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("(6) CMB 3rd-PEAK CONSTRAINT: does it force cs^2->0 at sub-horizon k? -- YES")
print("-"*78)

# The 3rd acoustic peak sits at multipole l~800, k ~ l/D_A ~ 800/14000 Mpc ~ 0.057 /Mpc
k_3rd_peak = 800.0/14000.0   # /Mpc (comoving)
print(f"""  The 3rd acoustic peak: l~800 -> k ~ {k_3rd_peak:.3f} /Mpc (comoving).
  To fit it CDM-like, the dark sector must be cold dust (cs^2->0, no pressure
  support) for k >~ {k_3rd_peak:.3f}/Mpc. That is the SAME 'cs^2->0 sub-horizon'
  property the no-go uses. The k^4/k^2 Jeans scale that could give scale-selection
  is at k_J = mu <~ 1/Mpc -- i.e. it would have to act at k > k_3rd_peak ~ 0.057/Mpc
  to NOT spoil the peak, but it must ALSO be < k_galaxy (~100/Mpc) to smooth galaxies
  AND > k_cluster_core (~7.5/Mpc) to leave cluster cores clumping.
  Required simultaneously: 0.057 < k_J ... but cluster-clump needs k_cluster_core <
  k_J => k_J > 7.5/Mpc AND galaxy-smooth needs k_J < 100/Mpc. So the FULL window is
    7.5/Mpc < k_J < 100/Mpc   (lambda_J between 10 and 130 kpc),
  which is galaxy-ILLEGAL (mu^-1 = 1/k_J < 0.13 Mpc << the required >~1 Mpc).""")

# The fatal clash, quantified:
kJ_needed_lo = k_cluster_core    # must exceed this to leave cluster cores unstable
kJ_needed_hi = k_galaxy_disk     # must be below this to smooth galaxy disks
mu_inv_needed_hi = 1.0/kJ_needed_lo  # mu^-1 must be BELOW this (Mpc)
mu_inv_needed_lo = 1.0/kJ_needed_hi
print(f"\n  THE FATAL CLASH (quantified):")
print(f"    cluster-core-clumpy needs k_J > {kJ_needed_lo:.2f}/Mpc -> mu^-1 < {mu_inv_needed_hi:.3f} Mpc")
print(f"    galaxy-disk-smooth  needs k_J < {kJ_needed_hi:.1f}/Mpc -> mu^-1 > {mu_inv_needed_lo:.4f} Mpc")
print(f"    galaxy MOND         needs mu^-1 > 1.0 Mpc  (Skordis-Zlosnik verbatim)")
print(f"    ==> evasion needs mu^-1 < {mu_inv_needed_hi:.3f} Mpc, galaxy MOND needs mu^-1 > 1.0 Mpc")
print(f"    ==> CONTRADICTION by factor {1.0/mu_inv_needed_hi:.1f}x. NO mu satisfies both.")

# ---------------------------------------------------------------------------
# SUMMARY -- the verdict, both ways, with the decisive numbers
# ---------------------------------------------------------------------------
print("\n" + "="*78)
print("SUMMARY -- ROUTE D VERDICT (both ways)")
print("="*78)

window_lo = k_cluster_core
window_hi = k_galaxy_disk
mu_inv_galaxy = 1.0    # Mpc, the smallest galaxy-legal screening scale
kJ_aest = 1.0/mu_inv_galaxy   # /Mpc, the largest galaxy-legal k_J
print(f"""
THE EVASION'S LOGIC IS SOUND (credit, both-ways): a ghost-condensate k^4 Jeans
scale orders BY SCALE not density -- k<k_J clumps (clusters), k>k_J smooths
(galaxies). The SIGN structure is exactly right to sidestep 'galaxies are denser'.

BUT it FAILS quantitatively on THREE independent, convention-robust legs:

 [A] B = 0 IN THE NAMED HOST. Blanchet-Skordis 2404.06584 Sec 6.2: the AeST khronon
     has NO propagating quadratic k^4 term; the dark-matter scalar has dispersion
     omega=0. With B=0 the k^4 STABILIZATION DOES NOT EXIST -> no scale-selection at
     all -> growth gated only by rho>mu^2/4piG, which BOTH galaxies and clusters
     blow past, galaxies MORE (3.7x denser). The ordering reverts to DENSITY and is
     backwards. (Banked Door-A pin, re-confirmed.)

 [B] EVEN IN THE IDEALIZED GC (B=O(1)), k_J = mu is OUT OF WINDOW. The window needs
     k_J in [{window_lo:.1f}, {window_hi:.0f}] /Mpc (lambda_J 10-130 kpc). AeST's
     galaxy-MOND constraint forces mu^-1 >~ 1 Mpc, i.e. k_J <~ 1 /Mpc -- BELOW the
     window by ~7.5-100x. At that k_J BOTH galaxy and cluster-core scales lie on the
     STABLE side: the field is smoothed in cluster cores TOO. Wrong side.

 [C] THE mu-SCALE CONTRADICTION IS HARD. cluster-core-clumpy needs mu^-1 < {mu_inv_needed_hi:.3f} Mpc;
     galaxy MOND needs mu^-1 > 1.0 Mpc. CONTRADICTION by {1.0/mu_inv_needed_hi:.0f}x. The SAME single
     mu sets BOTH the galaxy MOND scale AND the Jeans scale (k_J = mu identically in
     AeST/ACLM) -- they are NOT independent levers. You cannot pick one for galaxies
     and another for clusters.

 [D] mu SCREENING is the WRONG-SCALE help: it suppresses k < mu (>Mpc supercluster),
     leaving cluster cores AND galaxies (both sub-mu^-1) unscreened -- no contrast.

 [E] CMB 3rd peak forces cs^2->0 (cold dust) for k >~ {k_3rd_peak:.3f}/Mpc; the only
     scale-selection lever (k_J=mu) is pinned <~1/Mpc and galaxy-illegal -- it cannot
     simultaneously preserve the peak, clump cluster cores, and smooth galaxies.

VERDICT: THE NO-GO STANDS. There is NO self-consistent AeST mechanism that clusters
in cluster cores (~420 kpc) while staying smooth in galaxy disks (~kpc) AND keeps
both the CMB 3rd-peak fit and the galaxy RAR. The k^4 Jeans evasion is killed at the
root (B=0) and, even granting B=O(1), the single scale k_J=mu cannot sit in the
required window without violating galaxy MOND by ~7.5x. The field clusters by DENSITY
(galaxies clump more), not by scale -- exactly the no-go's argument.
""")

# Emit machine-readable key numbers
print("KEY_NUMBERS_JSON_START")
import json
out = {
  "window_kJ_per_Mpc_lo_clustercore": round(window_lo,3),
  "window_kJ_per_Mpc_hi_galaxydisk": round(window_hi,2),
  "aest_galaxy_forced_kJ_per_Mpc_max": kJ_aest,
  "aest_out_of_window_factor_low": round(window_lo/kJ_aest,2),
  "B_in_named_host": 0,
  "mu_inv_needed_for_cluster_clump_Mpc_max": round(mu_inv_needed_hi,4),
  "mu_inv_needed_for_galaxy_MOND_Mpc_min": 1.0,
  "mu_contradiction_factor": round(1.0/mu_inv_needed_hi,1),
  "galaxy_over_cluster_density_ratio": round(rho_gal_disk_x/rho_clu_core_x,2),
  "rho_thresh_over_rhocrit_mu1Mpc": float(f"{rho_thr1:.3e}"),
  "k_3rd_peak_per_Mpc": round(k_3rd_peak,4),
  "verdict": "NO-GO STANDS: B=0 kills k^4; k_J=mu out of window by 7.5-100x; mu contradiction 7.5x; CMB forces cs2->0"
}
print(json.dumps(out, indent=2))
print("KEY_NUMBERS_JSON_END")
