#!/usr/bin/env python3
"""
ROUTE C -- the BROADER scale-dependent-DM-clustering literature, tested HARD and BOTH-WAYS.

QUESTION (Carl's evasion goal): is there a KNOWN mechanism by which a dark sector clusters in
CLUSTER cores (~Mpc) but stays SMOOTH in GALAXY disks (~kpc), and can the AeST ghost-condensate
Q-mode REALIZE that scale?  If yes -> the cluster no-go is OVERTURNED (clusters explained galaxy-safe).
If no -> the no-go STANDS.

THE DIRECTIONALITY TRAP (the crux the prompt names):
  - The familiar "small-scale-suppression" DM (warm/fuzzy/SIDM) suppresses clustering BELOW some scale.
    To keep GALAXIES smooth you'd suppress BELOW ~kpc-Mpc.  But galaxies (kpc) are SMALLER scale than
    cluster cores (Mpc).  So a small-scale cutoff that smooths galaxies ALSO smooths the cluster core
    (the cluster core is INSIDE the cutoff too, or only marginally outside).
  - WORSE: density-wise galaxy disks are ~3.7x DENSER than cluster cores (banked).  Any density-gated
    collapse clusters MORE in galaxies.  So "cluster-clumpy + galaxy-smooth" needs a mechanism that is
    SCALE-selective in the RIGHT window AND survives the density-ordering.  We test both.

We quantify each literature mechanism's characteristic scale, its DIRECTION, and whether AeST can host it.

QUARANTINE: a0=9.36e-11, Z, kappa, I0 NEVER derived. All AeST shape params (K_B, K_2, mu, lambda_s, I0)
are FREE/quarantined; we only ask whether ANY choice realizes the split.
BOTH-WAYS: we hunt the evasion hard (try to MAKE the window open) AND report honestly if it cannot.
"""
import numpy as np
import sympy as sp

# ----------------------------------------------------------------------------------------------------
# Physical constants (SI)
# ----------------------------------------------------------------------------------------------------
G     = 6.674e-11          # m^3 kg^-1 s^-2
c     = 2.998e8            # m/s
hbar  = 1.0546e-34         # J s
eV    = 1.602e-19          # J
Mpc   = 3.086e22           # m
kpc   = 3.086e19           # m
Msun  = 1.989e30           # kg
H0    = 67.4 * 1e3 / Mpc   # s^-1  (67.4 km/s/Mpc)
rho_crit = 3*H0**2/(8*np.pi*G)   # kg/m^3
Lambda = 1.0909e-52        # m^-2 (banked)
a0     = 9.3624e-11        # m/s^2 (FRAMEWORK INPUT, quarantined)

print("="*92)
print("ROUTE C: scale-dependent-DM clustering -- can a dark sector be galaxy-smooth AND cluster-clumpy?")
print("="*92)
print(f"rho_crit = {rho_crit:.3e} kg/m^3,  H0 = {H0:.3e} 1/s,  Hubble radius c/H0 = {c/H0/Mpc:.1f} Mpc")

# ----------------------------------------------------------------------------------------------------
# (0) The density landscape (banked numbers, restated so the directionality is explicit)
# ----------------------------------------------------------------------------------------------------
# Galaxy disk mean density (SPARC-ish, inside optical radius) vs cluster core mean density.
# Banked: galaxy disk ~9.7e13 x rho_crit; cluster core ~2.6e13 x rho_crit; galaxy disk 3.7x DENSER.
rho_galaxy_disk = 9.7e13 * rho_crit
rho_cluster_core = 2.6e13 * rho_crit
print("\n(0) DENSITY LANDSCAPE (the ordering that defeats density-gated clustering)")
print(f"    galaxy disk  rho ~ {rho_galaxy_disk/rho_crit:.2e} rho_crit")
print(f"    cluster core rho ~ {rho_cluster_core/rho_crit:.2e} rho_crit")
print(f"    galaxy/cluster density ratio = {rho_galaxy_disk/rho_cluster_core:.2f}x  (galaxies DENSER)")
print("    => ANY density-gated collapse clusters MORE in galaxies.  Need a SCALE selector, not density.")

# Characteristic LENGTH scales we must separate:
L_galaxy = 3.0 * kpc      # galaxy disk / inner halo scale where RAR is measured
L_cluster_core = 420.0 * kpc   # banked cluster-core radius (~0.42 Mpc)
print(f"\n    L_galaxy ~ {L_galaxy/kpc:.0f} kpc   L_cluster_core ~ {L_cluster_core/kpc:.0f} kpc = {L_cluster_core/Mpc:.2f} Mpc")
print(f"    => For 'cluster-clumpy, galaxy-smooth' a cutoff scale must sit BETWEEN {L_galaxy/kpc:.0f} kpc and {L_cluster_core/kpc:.0f} kpc,")
print( "       AND smooth the SMALLER scale while letting the LARGER cluster scale collapse.")
print("    KEY: galaxies are the SMALLER scale.  A small-scale cutoff smooths galaxies, GOOD --")
print("         but it ALSO smooths everything below the cutoff INCLUDING cluster sub-structure;")
print("         the cluster core can only stay clumpy if the cutoff is BELOW ~Mpc but ABOVE ~kpc.")

# ----------------------------------------------------------------------------------------------------
# (1) WARM DARK MATTER -- free-streaming cutoff
# ----------------------------------------------------------------------------------------------------
# WDM free-streaming (half-mode) length scales with thermal relic mass m_X.
# Empirical (Schneider/Viel): half-mode mass M_hm ~ 1e10 Msun for m_X~3 keV; lambda_hm ~ few x 100 kpc..Mpc.
# lambda_fs (comoving) ~ 0.049 (m_X/keV)^-1.11 (Omega_X/0.25)^0.11 (h/0.7)^1.22  Mpc  (Bode-Ostriker-Turok-ish)
print("\n" + "-"*92)
print("(1) WARM DARK MATTER -- free-streaming cutoff (suppresses BELOW lambda_fs)")
print("-"*92)
def wdm_lambda_fs_Mpc(m_keV, OmegaX=0.25, h=0.674):
    # Bode-Ostriker-Turok / Viel scaling, comoving Mpc/h -> convert
    lam_hMpc = 0.049 * (m_keV)**-1.11 * (OmegaX/0.25)**0.11 * (h/0.7)**1.22
    return lam_hMpc / h
for m_keV in [0.3, 1.0, 3.0, 5.4, 10.0]:
    lam = wdm_lambda_fs_Mpc(m_keV)
    # half-mode is ~10-20x lambda_fs for the *scale where power is cut*; report both
    print(f"    m_X={m_keV:5.1f} keV : lambda_fs ~ {lam*1e3:7.1f} kpc  (cutoff scale)  -> half-mode ~ {lam*1e3*14:7.0f} kpc")
print("    DIRECTION: cutoff suppresses BELOW lambda_fs.  To smooth GALAXIES (~3 kpc) need lambda_fs >~ kpc,")
print("               which needs m_X <~ few keV.  But then lambda_fs is at most ~100s kpc << cluster core 420 kpc?")
print("    VERDICT(WDM): the free-streaming cutoff that smooths galaxies (kpc) sits at <~ few-100 kpc.")
print("               The cluster CORE (420 kpc) is at/above the cutoff so it could still collapse --")
print("               BUT to smooth a 3-kpc galaxy you need a cutoff ~kpc, which leaves ALL of >kpc clumpy,")
print("               i.e. galaxies are NOT smoothed (only sub-kpc is).  To actually smooth the whole")
print("               galaxy halo you need lambda_fs ~ tens of kpc -> m_X ~ 0.1-0.3 keV = HOT, already ruled")
print("               out by Lyman-alpha (m_X > 5.3 keV, Villasenor 2023 / Irsic).  And a cutoff big enough")
print("               to erase the galaxy halo (~tens kpc) ALSO erases cluster sub-structure but NOT the")
print("               420-kpc core mean -- so WDM gives 'smooth galaxies' ONLY in the hot, excluded regime,")
print("               and even there the CORE still gets its smooth-but-present mean density (no extra clumping).")
print("    => WDM is the WRONG TOOL: it removes a HALO, it does not ADD cluster-core mass. NULL for the no-go.")

# ----------------------------------------------------------------------------------------------------
# (2) FUZZY / ULTRALIGHT DM -- quantum-pressure Jeans scale (THE most relevant analog)
# ----------------------------------------------------------------------------------------------------
# Jeans wavenumber for a wave-DM / ghost-condensate-like quantum pressure: omega^2 = -4 pi G rho + (hbar k^2/2m)^2
# k_J = (16 pi G rho m^2 / hbar^2)^(1/4);  lambda_J = 2 pi / k_J.  lambda_J DECREASES with rho (denser -> smaller Jeans).
print("\n" + "-"*92)
print("(2) FUZZY / ULTRALIGHT DM -- quantum-pressure Jeans scale  lambda_J ~ rho^{-1/4} (de Broglie)")
print("-"*92)
def fdm_lambdaJ(m_eV, rho):
    m = m_eV*eV/c**2  # kg
    kJ = (16*np.pi*G*rho*m**2/hbar**2)**0.25
    return 2*np.pi/kJ
print("    The Jeans scale is DENSITY-dependent: lambda_J ~ rho^{-1/4}.  Denser -> SMALLER Jeans -> clumps MORE.")
print("    Since galaxies are 3.7x DENSER, their Jeans length is (3.7)^{-1/4}=0.72x SMALLER -> galaxies clump MORE.")
print(f"    {'m [eV]':>10} | {'lamJ(gal)':>12} | {'lamJ(clus)':>12} | direction")
for m_eV in [1e-24, 1e-23, 1e-22, 1e-21]:
    lg = fdm_lambdaJ(m_eV, rho_galaxy_disk)
    lc = fdm_lambdaJ(m_eV, rho_cluster_core)
    print(f"    {m_eV:10.1e} | {lg/kpc:9.2f} kpc | {lc/kpc:9.2f} kpc | gal Jeans SMALLER by {lc/lg:.2f}x")
print("    DIRECTION: density-gated AGAIN -> galaxies (denser) have the SMALLER Jeans length and clump MORE.")
print("    To smooth a 3-kpc galaxy you need lambda_J(gal) >~ 3 kpc -> m ~ 1e-22 eV (canonical FDM).")
print("    But at THAT mass lambda_J(cluster core) is even SMALLER (denser core? no -- core is LESS dense),")
print("    so cluster core Jeans is LARGER -> core is MORE suppressed than the galaxy.  WRONG WAY for clusters.")
print("    => FDM smooths the LESS-dense cluster core MORE than the denser galaxy.  It is the OPPOSITE of needed.")
print("    (This is why FDM is invoked to make galaxy CORES, not to ADD cluster-core mass.) NULL for the no-go.")

# ----------------------------------------------------------------------------------------------------
# (3) SELF-INTERACTING DM -- cores in clusters via velocity-dependent cross section
# ----------------------------------------------------------------------------------------------------
print("\n" + "-"*92)
print("(3) SELF-INTERACTING DM -- velocity-dependent sigma/m makes CORES (REMOVES central mass)")
print("-"*92)
print("    SIDM with velocity-dependent sigma/m can be strong in galaxies (low v) and weak in clusters (high v).")
print("    But its effect is to FLATTEN cusps = REDUCE central density (make cores), NOT to ADD cluster-core mass.")
print("    Direction is wrong twice: (a) it removes mass where you need to add it; (b) the cluster no-go needs")
print("    EXTRA clumping in cluster cores, SIDM gives LESS.  NULL for the no-go.")

# ----------------------------------------------------------------------------------------------------
# (4) THE AeST Q-MODE: what scale does IT actually have?  (the host test)
# ----------------------------------------------------------------------------------------------------
print("\n" + "="*92)
print("(4) CAN THE AeST GHOST-CONDENSATE Q-MODE REALIZE ANY OF THESE SCALES?")
print("="*92)

# (4a) The k^4 ghost-condensate Jeans scale -- IF B != 0 (the candidate loophole)
# Ghost condensate dispersion: omega^2 = cs^2 k^2 + (B/M^2) k^4 (Arkani-Hamed et al).  With cs^2->0 sub-horizon,
# omega^2 ~ (B/M^2) k^4 - 4 pi G rho.  Jeans: k_J^4 = 4 pi G rho M^2 / B.  lambda_J = 2 pi / k_J.
print("\n(4a) THE CANDIDATE LOOPHOLE: ghost-condensate k^4 Jeans scale (IF a real B>0 k^4 tail exists)")
print("     omega^2 = cs^2 k^2 + (B/M^2) k^4 ;  with cs^2->0: Jeans k_J = (4 pi G rho M^2 / B)^{1/4}, lamJ ~ rho^{-1/4}")
def gc_lambdaJ(M_invlen_per_Mpc, rho, B=1.0):
    # M is a mass scale with 1/M^2 the k^4 coefficient; parameterize by length L_M = 1/M
    L_M = M_invlen_per_Mpc*Mpc   # treat input as L_M in Mpc
    Msc = 1.0/L_M
    kJ = (4*np.pi*G*rho*Msc**2/B)**0.25
    return 2*np.pi/kJ
print("     Even granting B>0, the k^4 Jeans is STILL rho^{-1/4} -> SAME density-ordering defeat as FDM:")
for L_M_Mpc in [0.1, 1.0, 10.0]:
    lg = gc_lambdaJ(L_M_Mpc, rho_galaxy_disk)
    lc = gc_lambdaJ(L_M_Mpc, rho_cluster_core)
    print(f"     L_M={L_M_Mpc:5.1f} Mpc : lamJ(gal)={lg/kpc:8.2f} kpc, lamJ(clus)={lc/kpc:8.2f} kpc -> gal SMALLER by {lc/lg:.2f}x (clumps MORE)")
print("     => the k^4 Jeans length is DENSITY-dependent ~rho^{-1/4}; galaxies being denser get the SMALLER")
print("        Jeans -> clump MORE.  A scale-only selector it is NOT.  Same backwards ordering.")

# (4b) THE DECISIVE HOST FACT (banked Door-A + primary sources, verified this session):
print("\n(4b) THE DECISIVE HOST FACT (primary-source verified this session):")
print("     Blanchet-Skordis 2024 (arXiv:2404.06584) ABSTRACT, verbatim: the propagating scalar dof has")
print("     'dispersion relation omega=0'.  Skordis-Zlosnik 2021 (arXiv:2007.00082): cs^2->0 sub-horizon.")
print("     Door-A pin (banked, wxe4q0b5x): the k^4 coefficient B = 0 EXACTLY in the AeST khronon host --")
print("     the single k^4 in the action is the NON-DYNAMICAL constraint momentum P_nu, gauge-fixed to zero.")
print("     => There is NO propagating quadratic k^4 tail in the host.  The candidate loophole's premise")
print("        (a finite k^4 Jeans scale between kpc and Mpc) DOES NOT EXIST in AeST.  B=0 holds.")

# (4c) The mu mass term: what length scale, and does it help?
print("\n(4c) THE mu MASS TERM: K(Q)=mu^2(Q-1)^2.  Does it give a helpful scale-dependent clustering?")
# Growth gated only by rho > mu^2/(4 pi G) (banked).  mu^-1 ~ Mpc (BS Fig.1 ~22 Mpc at K_B=0.5).
# The critical density threshold:
mu_inv_Mpc = 22.3   # banked from BS Fig 1
mu = 1.0/(mu_inv_Mpc*Mpc)   # 1/m
rho_thresh = mu**2/(4*np.pi*G)
print(f"     mu^-1 ~ {mu_inv_Mpc} Mpc (BS Fig.1).  Growth threshold rho > mu^2/(4 pi G) = {rho_thresh/rho_crit:.2e} rho_crit.")
print(f"     Galaxy disk ({rho_galaxy_disk/rho_crit:.1e}) and cluster core ({rho_cluster_core/rho_crit:.1e}) BOTH >> threshold {rho_thresh/rho_crit:.1e}.")
print(f"     ratio galaxy/threshold = {rho_galaxy_disk/rho_thresh:.2e},  cluster/threshold = {rho_cluster_core/rho_thresh:.2e}")
print("     => The mu term screens only >mu^-1 ~ 22 Mpc (SUPER-cluster scale).  It does NOTHING to stop")
print("        sub-Mpc collapse.  BOTH galaxies and clusters are FAR above the density threshold -> BOTH clump.")
print("        And the mu screening scale (~22 Mpc) is ABOVE the cluster core (0.42 Mpc), so it cannot keep")
print("        the cluster clumpy while smoothing the galaxy -- it smooths NEITHER (both are sub-22-Mpc).")
print("     Direction check: mu screening kills LARGE scales (>22 Mpc), keeps SMALL scales clumpy. That is")
print("     EXACTLY BACKWARDS -- it would smooth the LARGEST scales, but galaxies are the smallest. NULL.")

# (4d) The omega=0 stability wavenumber from BS: convert ~10^-31 eV to a length
print("\n(4d) The BS 'Hamiltonian bounded below for k > ~10^-31 eV' stability wavenumber -- what length?")
k_eV = 1e-31
# k in 1/m: k[1/m] = k[eV]*eV/(hbar c)
k_per_m = k_eV*eV/(hbar*c)
L_stab = 2*np.pi/k_per_m
print(f"     k ~ 1e-31 eV  ->  k = {k_per_m:.3e} 1/m  ->  lambda = 2pi/k = {L_stab/Mpc:.3e} Mpc = {L_stab/(c/H0):.2f} x Hubble radius")
print(f"     (Hubble radius c/H0 = {c/H0/Mpc:.0f} Mpc.)  => the ONLY scale in the linear AeST scalar problem is")
print( "     HORIZON-sized.  There is NO sub-Mpc dynamical scale in the propagating sector -- consistent with")
print( "     omega=0 (no dispersion) and B=0 (no k^4).  The mode behaves as scale-free CDM-dust below the horizon.")

# ----------------------------------------------------------------------------------------------------
# (5) SYNTHESIS TABLE -- direction of each mechanism
# ----------------------------------------------------------------------------------------------------
print("\n" + "="*92)
print("(5) SYNTHESIS: does any mechanism give galaxy-SMOOTH + cluster-CLUMPY, and can AeST host it?")
print("="*92)
rows = [
 ("Warm DM (free-stream)", "suppress < lambda_fs", "smooths SMALL (sub-kpc) only in allowed range; removes halos, adds no core mass", "NO"),
 ("Fuzzy/ULDM (quantum J)", "lambda_J ~ rho^{-1/4}", "DENSITY-gated: denser galaxies clump MORE; smooths the LESS-dense cluster core MORE", "NO"),
 ("SIDM (vel-dep sigma)",   "cores via scattering", "REMOVES central mass (makes cores); wrong sign twice", "NO"),
 ("GC k^4 Jeans (IF B>0)",  "lambda_J ~ rho^{-1/4}", "same density-ordering defeat as FDM; AND B=0 in AeST so it does not exist", "NO (B=0)"),
 ("AeST mu mass term",      "screen > mu^-1~22 Mpc", "kills LARGE scales not small; both gal+clus far above threshold -> both clump", "NO"),
]
print(f"  {'mechanism':<24}{'char scale':<24}{'why it fails the split':<62}{'AeST?':<8}")
for r in rows:
    print(f"  {r[0]:<24}{r[1]:<24}{r[2]:<62}{r[3]:<8}")

print("\n" + "="*92)
print("VERDICT")
print("="*92)
print("""
The broader scale-dependent-DM literature offers THREE families that smooth small scales:
warm DM (free-streaming), fuzzy/ultralight DM (quantum-pressure Jeans), and SIDM (scattering cores).
ALL THREE fail the 'galaxy-smooth + cluster-clumpy' split, for a reason that is structural, not
incidental:

  * They suppress clustering BELOW a scale or BELOW a density.  Galaxies are the SMALLER and the
    DENSER environment.  So every one of these mechanisms, tuned to smooth galaxies, either (a) smooths
    the cluster core EVEN MORE (FDM/GC: lambda_J ~ rho^{-1/4}, the less-dense core has the LARGER Jeans
    length, more suppression), or (b) merely REMOVES a halo / makes a core (WDM/SIDM), adding NO mass to
    the cluster center -- which is exactly the deficit the no-go needs filled.

  * The one mechanism with the RIGHT topology (a finite k^4 Jeans scale SET BY SCALE not density,
    sitting between kpc and Mpc) is the ghost-condensate k^4 tail -- and (i) even it is rho^{-1/4}
    density-gated once you write omega^2 = cs^2 k^2 + (B/M^2)k^4, and (ii) in the framework's named host
    the coefficient is B = 0 EXACTLY (Door-A pin; corroborated by the primary-source fact that the AeST
    scalar dof has dispersion omega=0).  No k^4 tail -> no finite Jeans scale -> the loophole's premise
    is absent.

  * The AeST mu mass term screens only ABOVE mu^-1 ~ 22 Mpc (super-cluster scale) -- the WRONG direction
    (it kills the LARGEST scales, but galaxies are the smallest), and both galaxies and cluster cores sit
    far above its density threshold, so it stops neither from collapsing.

CONCLUSION: NO known scale-dependent-clustering mechanism realizes the galaxy-safe/cluster-clumpy split
in the direction the no-go requires, and the AeST Q-mode cannot embody one -- B=0 kills the k^4 Jeans
scale, the mu term is the wrong direction, and the quantum/free-streaming analogs are all rho^{-1/4} or
mass-removing.  The no-go STANDS.  (Both-ways: we tried hard to open the window -- granting B>0, scanning
masses and scales -- and it does not open.  No manufactured loophole.)
""")
print("DONE.")
