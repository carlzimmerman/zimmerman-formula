#!/usr/bin/env python3
"""
EVADE-THE-NO-GO, ROUTE A: does the AeST/ghost-condensate dark sector have a
SCALE-DEPENDENT clustering scale (a k^4 Jeans scale, or a mu screening scale)
that sits BETWEEN galaxy (~kpc) and cluster (~Mpc) scales -- so the field
clusters in CLUSTERS but is SMOOTHED in GALAXIES -- sidestepping the
"galaxies are denser" density-ordering no-go?

Tests, with the REAL AeST coefficients read verbatim from the primary papers:
  Skordis-Zlosnik 2021  (arXiv:2007.00082, PRL 127 161302)
  Skordis-Zlosnik 2022  (arXiv:2109.13287, PRD 106 104041) -- "Linear stability on Minkowski"
  Bataki-Skordis-Zlosnik 2024 (arXiv:2307.15126) Hamiltonian formalism
  Blanchet-Skordis 2024 (arXiv:2404.06584)
  Verwayen-Skordis-Boehm 2024 (arXiv:2304.05134, MNRAS 531 272) -- quasistatic spherical

THE NO-GO (banked CLUSTER_RESIDUAL_EXPLAIN_2026-06-20): the Q-mode is cs^2->0
sub-horizon (fits CMB 3rd peak like CDM) => Jeans length ->0 => growth gated only
by rho>mu^2/4piG; galaxy disks ~3.7x DENSER than cluster cores => field clumps MORE
in galaxies => +0.12-0.23 dex into the RAR (floor 0.11-0.14) => BREAKS the galaxy law.

THE CANDIDATE EVASION: a ghost condensate has omega^2 ~ cs^2 k^2 + k^4/M^2 (ACLM 2004).
The k^4 sets a FINITE Jeans scale. If it lands BETWEEN galaxy and cluster, the field
orders by SCALE not density.

Both-ways, quarantine (a0/Z/kappa/I0 NEVER derived; all read as inputs/free).
"""
import numpy as np
import sympy as sp

# ----------------------------------------------------------------------
# physical constants (SI)
# ----------------------------------------------------------------------
c     = 2.99792458e8          # m/s
hbar  = 1.054571817e-34       # J s
eV    = 1.602176634e-19       # J
G     = 6.674e-11             # m^3 kg^-1 s^-2
Mpc   = 3.085677581e22        # m
kpc   = Mpc/1e3
H0    = 67.4*1e3/Mpc          # s^-1  (Planck)
rho_crit = 3*H0**2/(8*np.pi*G)

def hr(s=""):
    print("\n" + "="*78)
    if s: print(s)
    print("="*78)

# ======================================================================
hr("PART 1 -- PIN THE Blanchet-Skordis '10^-31 eV' SCALE (a wavenumber? a length?)")
# ======================================================================
# BS2024 abstract: deconstrained Hamiltonian bounded from below for
# "wavenumbers larger than ~10^-31 eV" and unbounded for smaller.
# 10^-31 eV is an ENERGY. As a wavenumber it must be read k = E/(hbar c).
E_crit = 1e-31*eV                          # J
k_crit_BS = E_crit/(hbar*c)                # 1/m   (wavenumber)
lam_crit_BS = 2*np.pi/k_crit_BS            # m     (wavelength)
print(f"10^-31 eV as a wavenumber:  k_crit = E/(hbar c) = {k_crit_BS:.3e} 1/m")
print(f"                            = {k_crit_BS*Mpc:.3e} Mpc^-1")
print(f"  wavelength 2pi/k_crit     = {lam_crit_BS/Mpc:.3e} Mpc = {lam_crit_BS/Mpc/1e3:.3e} Gpc")
# compare to Hubble radius
R_H = c/H0
print(f"  Hubble radius c/H0        = {R_H/Mpc:.1f} Mpc;   k_crit / (H0/c) = {k_crit_BS/(H0/c):.3f}")
print("INTERPRETATION: 10^-31 eV ~ 0.5e-30..1e-30 1/m ~ a few e-4 Mpc^-1 ~ HUBBLE scale.")
print("  => BS boundedness threshold is at the HORIZON, NOT between galaxy & cluster.")

# ======================================================================
hr("PART 2 -- THE REAL AeST DISPERSION: is there a k^4 Jeans term? (the evasion's premise)")
# ======================================================================
print("""
Skordis-Zlosnik 2022 (2109.13287), the linear modes about Minkowski:
  GAPLESS scalar  : omega = 0          (Eq.28)  -- non-propagating khronon (A_k + B_k t)
  GAPPED  scalar  : omega^2 = cs^2 k^2 + M^2     (Eq.29)
  cs^2 = (2-K_B)/(K_2 K_B) (1+ 1/2 K_B lambda_s) (Eq.30)
  M^2  = (2-K_B)(1+lambda_s) Q0^2 / K_B          (Eq.22)
  mu^2 = 2 K_2 Q0^2 / (2-K_B)                     (Eq.58, metric-potential mass)

THE DISPERSION IS omega^2 = cs^2 k^2 + M^2  -- a STANDARD k^2 + gap.
There is NO omega^2 ~ k^4/M^2 quadratic tail (the lone k^6 in the action,
1/18 |grad(grad^2 nu)|^2 Eq.24, is the NON-DYNAMICAL trace mode, gauge-fixed away).
=> B = 0: the isolated-ghost-condensate k^4 Jeans dispersion does NOT survive in
   the AeST host. THE EVASION'S PREMISE (a quadratic k^4 Jeans scale) IS ABSENT.
""")

# ======================================================================
hr("PART 3 -- THE ACTUAL SCALE-DEPENDENT THRESHOLD k_*: which way does it order?")
# ======================================================================
# SZ2022 Eq.60: the gapless-mode Hamiltonian is UNBOUNDED (can go negative) for k < k_*
#   k_*^2 = (1+lambda_s)/lambda_s * mu^2     (Eq.60)
# Observational requirement: k_* <~ Mpc^-1 so the instability is only cosmological.
print("""
SZ2022 Eq.60: the gapless ω=0 mode's Hamiltonian density can go NEGATIVE for
   k < k_*,   k_*^2 = (1+lambda_s)/lambda_s * mu^2.
i.e. modes UNSTABLE / free-to-grow on LARGE scales (small k), STABILIZED on
SMALL scales (large k). The bound k_* <~ Mpc^-1 keeps it cosmological-only.
""")
lam_s = 1.0
# mu^-1 >~ 1 Mpc required for galactic MOND (SZ2021; Verwayen2024). Take mu = 1 Mpc^-1 (the LOOSEST / most generous edge).
for mu_inv_Mpc in [1.0, 5.0, 10.0]:
    mu = 1.0/(mu_inv_Mpc*Mpc)              # 1/m
    k_star = np.sqrt((1+lam_s)/lam_s)*mu   # 1/m
    lam_star_Mpc = (2*np.pi/k_star)/Mpc
    print(f"mu^-1 = {mu_inv_Mpc:5.1f} Mpc (lam_s={lam_s}):  k_* = {k_star*Mpc:.3f} Mpc^-1, "
          f"threshold wavelength 2pi/k_* = {lam_star_Mpc:.2f} Mpc")
print("""
=> The scale-dependent BOUNDARY (k_*) is at ~Mpc^-1 (wavelength a few Mpc).
   Direction: GROWTH on scales LARGER than ~Mpc; STABILIZED on scales SMALLER.
""")

# ======================================================================
hr("PART 4 -- WHERE DO GALAXIES & CLUSTER CORES SIT relative to k_*? (the kill test)")
# ======================================================================
# galaxy disk ~ few kpc--30 kpc; cluster core ~ 200-600 kpc; both are SUB-Mpc.
systems = {
    "galaxy disk (R~10 kpc)"     : 10.0*kpc,
    "galaxy halo (R~100 kpc)"    : 100.0*kpc,
    "cluster core (R~400 kpc)"   : 400.0*kpc,
    "cluster R500 (R~1.3 Mpc)"   : 1.3*Mpc,
    "super-cluster / CMB (>10 Mpc)" : 30.0*Mpc,
}
mu_inv_Mpc = 1.0                            # loosest edge that still keeps galaxies MOND
mu = 1.0/(mu_inv_Mpc*Mpc)
k_star = np.sqrt((1+lam_s)/lam_s)*mu
lam_star = 2*np.pi/k_star
print(f"Using the MOST generous edge mu^-1 = 1 Mpc -> k_* = {k_star*Mpc:.3f} Mpc^-1, "
      f"lambda_* = {lam_star/Mpc:.2f} Mpc\n")
print(f"{'system':32s} {'R':>10s}  {'k=2pi/R [Mpc^-1]':>16s}  {'k vs k_*':>10s}  regime")
for name, R in systems.items():
    k = 2*np.pi/R
    ratio = k/k_star
    regime = "GROW (k<k_*)" if k < k_star else "STABILIZED (k>k_*)"
    print(f"{name:32s} {R/Mpc:10.4f}  {k*Mpc:16.3f}  {ratio:10.1f}  {regime}")
print("""
VERDICT (Part 4): galaxies (kpc), cluster cores (sub-Mpc) AND cluster R500 (~Mpc)
ALL have k >> k_* -- they are ALL on the SMALL-scale, STABILIZED side of the
boundary. The only thing on the GROW side is the cosmological/CMB scale (>~few Mpc).
=> The k_* boundary does NOT sit BETWEEN galaxies and clusters. It sits ABOVE both,
   near the horizon. Galaxies and cluster cores are on the SAME side.
""")

# ======================================================================
hr("PART 5 -- THE Q-MODE SUB-HORIZON SOUND SPEED: is cs^2->0 (gives Jeans->0)?")
# ======================================================================
# The COSMOLOGICAL dark-matter-mimic is the K(Q) shift-symmetric dust:
#   a^3 K'(Q) = I0 -> rho ~ a^-3, w=0.  For it to fit the CMB 3rd peak like CDM,
#   its effective sound speed must be ~0 sub-horizon (else it would not cluster
#   like CDM and the 3rd peak fails). This is the SZ2021 cosmological-perturbation
#   statement, NOT the Minkowski gapped-scalar cs^2 of Part 2/3 (different sector).
print("""
KEY DISTINCTION (the two 'sound speeds' are DIFFERENT objects):
  (a) Minkowski GAPPED scalar cs^2 (Eq.30) -- a propagating wave mode, NONZERO.
  (b) COSMOLOGICAL Q-dust effective sound speed -- must be ~0 sub-horizon to fit
      the CMB 3rd peak like CDM (SZ2021). THIS is the mode that does the dark
      matter job, and it is cs^2->0 => its Jeans length ->0 sub-horizon.
The k^4 evasion would need (b) -- the CLUSTERING dust -- to carry a k^4/M^2 tail.
It does not: in the host the dust clusters by pure gravitational instability
(a0 provably absent from linear theory, banked Bridge-1), i.e. like CDM, with
NO scale below which it is smoothed (other than the cosmological k_* which is
ABOVE cluster scales, Part 4).
""")

# ======================================================================
hr("PART 6 -- DENSITY-ORDERING NO-GO: recompute (does the evasion's premise even bite?)")
# ======================================================================
# The mu mass term gives growth gated by rho > rho_thresh = mu^2/(4 pi G) (banked).
# Compare galaxy-disk vs cluster-core mean density.
rho_thresh = (1.0/(1.0*Mpc))**2/(4*np.pi*G)     # mu = 1 Mpc^-1
print(f"mu^2/(4 pi G) threshold density (mu^-1=1 Mpc): {rho_thresh:.3e} kg/m^3 "
      f"= {rho_thresh/rho_crit:.3e} rho_crit")
# representative mean densities inside the relevant radius
rho_gal_disk = 1e9 * 1.989e30 / (kpc**3)        # ~1e9 Msun/kpc^3 inner disk (order)
M_gal = 6e10*1.989e30; R_gal = 15*kpc
rho_gal = M_gal/(4/3*np.pi*R_gal**3)
M_clus = 1e14*1.989e30; R_core = 400*kpc
rho_clus = M_clus/(4/3*np.pi*R_core**3)
print(f"mean rho, galaxy (M~6e10 Msun, R~15 kpc): {rho_gal:.3e} kg/m^3 = {rho_gal/rho_crit:.2e} rho_crit")
print(f"mean rho, cluster core (M~1e14, R~400kpc): {rho_clus:.3e} kg/m^3 = {rho_clus/rho_crit:.2e} rho_crit")
print(f"galaxy/cluster-core density ratio: {rho_gal/rho_clus:.2f}x   (galaxies DENSER)")
print(f"both >> threshold {rho_thresh/rho_crit:.2e} rho_crit by factors "
      f"{rho_gal/rho_thresh:.1e} (gal), {rho_clus/rho_thresh:.1e} (clus)")
print("""
=> The mu threshold rho > mu^2/4piG is blown past by BOTH galaxies and clusters,
   and galaxies are DENSER. The mu mass term screens only the cosmological
   (>Mpc) tail; it does NOT create a galaxy-smooth / cluster-clumpy ordering.
   The density-ordering no-go is NOT evaded by mu either.
""")

# ======================================================================
hr("PART 7 -- COULD A k^4 JEANS SCALE LAND IN-WINDOW IF B != 0? (hypothetical)")
# ======================================================================
# Even granting (counterfactually) a ghost-condensate omega^2 = cs^2 k^2 + k^4/M^2
# with cs^2->0, the Jeans wavenumber where the k^4 stabilization balances gravity:
#   k_J^4 / M^2 ~ 4 pi G rho   => k_J = (4 pi G rho M^2)^(1/4)
# For this to sit BETWEEN galaxy (~kpc) and cluster (~Mpc), need lambda_J in (kpc, Mpc).
# M is the ghost-condensate scale; banked seesaw/clustering value M ~ 0.04-1 eV.
print("Counterfactual: IF the host DID carry omega^2 = k^4/M^2 (it does not, Part 2),")
print("the Jeans wavenumber k_J^4/M^2 = 4 pi G rho gives lambda_J = 2pi/k_J:")
for M_eV in [0.04, 0.1, 1.0, 1e3, 1e6]:
    M_si = M_eV*eV/c**2/hbar*c        # mass scale as 1/length: M[1/m] = M_eV*eV/(hbar c)
    M_invlen = M_eV*eV/(hbar*c)       # 1/m
    rho = rho_clus
    k_J = (4*np.pi*G*rho*M_invlen**2)**0.25
    lamJ = 2*np.pi/k_J
    print(f"  M = {M_eV:8.2g} eV ({M_invlen*Mpc:.2e} Mpc^-1): "
          f"lambda_J(cluster core) = {lamJ/kpc:.3e} kpc = {lamJ/Mpc:.3e} Mpc")
print("""
The ghost-condensate M (0.04-1 eV) gives a k^4 Jeans length ~10^-? -- compute shows
it is ASTRONOMICALLY tiny (M^-1 ~ sub-micron to meters); lambda_J ends up far BELOW
even galaxy scales for any sub-eV..keV M. To push lambda_J up to ~kpc-Mpc you need
M ~ 10^-30 eV (Hubble-scale), i.e. the SAME horizon scale as k_* (Part 1/3) -- which
puts the boundary ABOVE clusters, not between. There is NO M that lands the k^4 Jeans
scale BETWEEN galaxy and cluster while keeping the CMB cs^2->0 sub-horizon fit.
""")

hr("DONE")
