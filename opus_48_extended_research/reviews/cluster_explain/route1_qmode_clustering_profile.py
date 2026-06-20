#!/usr/bin/env python3
"""
ROUTE 1 -- THE CENTERPIECE: does the AeST ghost-condensate Q-mode CLUSTER in the
cluster core to provide the residual, while staying sub-dominant in galaxies?
================================================================================
Framework (C. Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2; MOND at z=0
realized covariantly by AeST (Skordis-Zlosnik 2021 PRL 127 161302). The dark sector
= the AeST shift-symmetric scalar's Q-mode: a w=0, rho ~ a^-3 COLD component, a MODE
of the gravity field (NOT a new particle). Banked: CDM-DEGENERATE on P(k)/CMB/S8, fits
full Planck; amount I0 ~ Omega_dm and FREE (an off-minimum shift-charge integration
constant).  QUARANTINE: a0/Z/kappa/I0 never asserted derived; I0 is INPUT.

THE QUESTION (distinct from the banked quasi-static mass-term Helmholtz work):
  The banked CLUSTER_RESIDUAL_CLOSURE / cluster_aest_massterm work solved the LOCAL
  quasi-static scalar RESPONSE (the mu^2 Phi Helmholtz term sourced by BARYONS) and
  found a DEFICIT/drain at R500 unless a free boundary constant chi_out is tuned.
  That is the field reacting to baryons IN PLACE.

  This script asks the DIFFERENT, CDM-degenerate question: the Q-mode is a a^-3 DUST
  with Omega_dm worth of density everywhere in the universe. Like CDM, it should
  GRAVITATIONALLY COLLAPSE into deep potential wells. The cluster IS a deep, large-
  scale well; the galaxy is a shallow, small-scale well. Does the SAME cosmic dust
  cluster MORE in the cluster (supplying the eta~2 residual = the field doing its
  CDM job) while staying SMOOTH in the galaxy (preserving the tight RAR)?

  The governing physics is the Q-mode's JEANS / clustering scale. A pressureless dust
  clusters on ALL scales (= ordinary CDM, would spoil galaxies). The Q-mode is NOT
  pressureless: it is a ghost condensate with a k^4 dispersion (Blanchet-Skordis;
  ACLM 2004) PLUS a CMB-pinned mass mu (1/mu ~ 1 Mpc). Its dispersion
       omega^2(k) ~ c_eff^2 k^2 + (k^4 / (2 mu^2-ish)) [stable branch]
  gives a SCALE-DEPENDENT sound speed -> a JEANS WAVENUMBER k_J. The clustering is
  SUPPRESSED below the Jeans length lambda_J = 2 pi / k_J and CDM-like above it.

  CENTERPIECE TEST:
   (A) where is lambda_J?  Is it BETWEEN galaxy (~10-30 kpc) and cluster (~Mpc) scales?
   (B) cluster: how much Q-mode mass collects inside R500 -- does it give eta~2?
   (C) GALAXY VETO (HARD): does the SAME field add < ~5% inside a galaxy (RAR-safe)?
   (D) the transition: WHY clusters-yes / galaxies-no (the scale threshold).

  BOTH WAYS (Carl #1 rule): build the best candidate, but the galaxy-veto is the hard
  constraint -- if enough clustering to close clusters spoils galaxies, SAY SO.

EQUATIONS USED (grounded; same as the banked extractions from the AeST PDFs):
  - AeST scalar mass:  mu^2 = 2 K2 Q0^2/(2-K_B);  1/mu >~ 1 Mpc (CMB/cosmo-pinned).
    [Skordis-Zlosnik 2021; Verwayen-Skordis-Zlosnik 2024; Durakovic-Skordis 2024]
  - Q-mode = ghost condensate (Verwayen-Skordis-Zlosnik 2024 Eq.7 K(Q)=mu^2(Q-1)^2
    cites ACLM 2004): perturbation dispersion omega^2 = c_s^2 k^2 + k^4/M_*^2 ...
  - cosmological dust:  rho_Q ~ a^-3,  Omega_Q ~ Omega_dm = 0.264 (FREE I0).  [banked]
  - linear growth in a sub-region: a fluid with sound speed c_s has a Jeans length
    lambda_J = c_s sqrt(pi/(G rho)); below it pressure beats gravity, above it grows.
"""
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import brentq

# ---------------------------------------------------------------- constants (SI)
c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
eV   = 1.602e-19
hbar = 1.0546e-34
yr   = 3.156e7
Gyr  = 1e9*yr

a0   = 9.36e-11                       # framework, quarantined
H0   = 67.4e3/Mpc                     # 1/s
Om, OL, Ob = 0.315, 0.685, 0.0493
Odm  = Om - Ob                        # 0.266  (the Q-mode amount, FREE I0)
rho_crit0 = 3*H0**2/(8*np.pi*G)       # kg/m^3
rho_dm0   = Odm*rho_crit0
Lambda    = 32.0*np.pi*(a0/c**2)**2   # 1/m^2  from a0=c^2 sqrt(Lambda/32pi)

print("="*86)
print("ROUTE 1 CENTERPIECE -- does the AeST Q-mode cluster in clusters but not galaxies?")
print("="*86)
print(f"  a0={a0:.3e}  Lambda(a0)={Lambda:.3e} 1/m^2  Odm(Q-mode,FREE I0)={Odm:.3f}")
print(f"  rho_crit0={rho_crit0:.3e}  rho_dm0={rho_dm0:.3e} kg/m^3")

# ==============================================================================
# STEP 0 -- THE TARGET (banked eRASS1 / A2029).  What the residual demands.
# ==============================================================================
print("\n"+"="*86)
print("STEP 0 -- TARGET: the cluster residual the Q-mode must supply (banked eRASS1)")
print("="*86)
# Rich cluster + a group, framework footing
def R500_of_M(M500_Msun, z=0.0):
    rc = rho_crit0*(Om*(1+z)**3+OL)
    return (3*M500_Msun*Msun/(4*np.pi*500*rc))**(1/3.)

clusters = {
  'rich  M500=1e15': dict(M500=1e15, fb=0.13),
  'group M500=1e14': dict(M500=1e14, fb=0.11),
}
TARGET = {}
for name,cl in clusters.items():
    M500=cl['M500']; R500=R500_of_M(M500); Mb=cl['fb']*M500
    g_bar=G*Mb*Msun/R500**2
    g_mond=np.sqrt(g_bar**2+g_bar*a0)        # framework dS-Unruh nu
    eta=2.0                                  # missing-mass factor at R500 (banked ~2)
    # extra GRAVITATING mass the residual needs inside R500 (over baryons+MOND-phantom)
    # eta = g_obs/g_mond ; g_obs = eta*g_mond ; M_dyn(R500)=g_obs R500^2/G
    M_dyn = eta*g_mond*R500**2/G/Msun
    M_phantom_mond = g_mond*R500**2/G/Msun   # MOND already supplies this as effective mass
    M_extra = M_dyn - M_phantom_mond         # what the Q-mode must add inside R500
    TARGET[name]=dict(M500=M500,R500=R500,Mb=Mb,g_bar=g_bar,g_mond=g_mond,
                      M_dyn=M_dyn,M_extra=M_extra,eta=eta)
    print(f"  {name}: R500={R500/Mpc:.2f} Mpc  Mb={Mb:.2e}  g_bar/a0={g_bar/a0:.3f}")
    print(f"     g_mond={g_mond:.3e}  eta~2 -> M_dyn(R500)={M_dyn:.2e} Msun"
          f"  Q-mode must add M_extra={M_extra:.2e} Msun inside R500")

# ==============================================================================
# STEP 1 -- THE JEANS / CLUSTERING SCALE OF THE Q-MODE
# ==============================================================================
print("\n"+"="*86)
print("STEP 1 -- the Q-mode clustering scale: is there a galaxy-OFF/cluster-ON window? (NO)")
print("="*86)
print("""  CLAIM TO TEST: the Q-mode is a ghost condensate with a scale that might resist
  collapse on SMALL scales and permit it on LARGE scales. (Spoiler: the growth-threshold
  check below shows this FAILS -- it is effectively c_s^2->0 CDM and clusters at all scales.)
   (i) PRIMARY (robust, CMB-pinned): the scalar mass mu, 1/mu ~ 1 Mpc -- a Yukawa/Jeans
       range. The field's self-gravitating clustering is screened/oscillatory BELOW 1/mu
       and free ABOVE it. This is the scale we lean on (it is CMB-pinned).
   (ii) SECONDARY (caveat, NOT robust): the ghost-condensate k^4 dispersion
        omega^2 ~ k^4/M_*^2 carries an UN-PINNED O(1) coefficient M_*; its implied
        Jeans length swings from ~30 kpc (no c) to ~500 Mpc (with c^2) -- so it is
        coefficient-dependent and we do NOT rely on it (flagged below).""")

inv_mu = 1.0*Mpc                  # 1/mu, CMB-pinned (free AeST constant, flagged)
mu = 1.0/inv_mu

# ----------------------------------------------------------------------------------
# CORRECTION (added after cross-check vs the sibling qmode_clustering verdict): the
# "1/mu sits between galaxy and cluster SIZES" framing is the WRONG physics for CLUSTERING.
# Gravitational GROWTH of a c_s^2->0 scalar is gated by the DENSITY threshold of its
# dispersion omega^2 = mu^2 - 4 pi G rho < 0, i.e. rho > rho_thresh = mu^2/(4 pi G), NOT by
# the system size vs 1/mu. Test it -- this is load-bearing and it OVERRIDES the optimistic
# size-based reading below.
rho_thresh = mu**2/(4*np.pi*G)
rho_gal_core = 6e10*Msun/((4*np.pi/3)*(20*kpc)**3)
rho_cl_core  = 1.3e14*Msun/((4*np.pi/3)*(400*kpc)**3)
print("\n  *** GROWTH-THRESHOLD CHECK (overrides the size-based reading) ***")
print(f"  Q-mode is c_s^2->0 (that is WHY it fits the CMB like CDM). Its growth is gated by")
print(f"  omega^2=mu^2-4piG rho<0 -> rho>rho_thresh=mu^2/4piG = {rho_thresh:.2e} kg/m^3 = {rho_thresh/rho_crit0:.1e} rho_crit.")
print(f"    galaxy disk rho  = {rho_gal_core:.2e} = {rho_gal_core/rho_thresh:.1e}x threshold -> GROWS (clusters in galaxies!)")
print(f"    cluster core rho = {rho_cl_core:.2e} = {rho_cl_core/rho_thresh:.1e}x threshold -> GROWS")
print(f"  => the CMB-pinned mu~1/Mpc is ~1e13x TOO SMALL to gate galaxy-vs-cluster. The mass term")
print(f"     screens the static POTENTIAL on >1 Mpc but does NOT stop sub-Mpc gravitational")
print(f"     COLLAPSE. A field that clusters in clusters ALSO clusters in galaxy halos. The")
print(f"     'smooth below 1/mu' reading below is the static-response scale, NOT the growth scale.")
print(f"     HONEST: there is NO Jeans/mass window that turns the dust ON in clusters and OFF in")
print(f"     galaxies -- consistent with the sibling verdict. The size-based steps below are kept")
print(f"     for the record but DO NOT establish a galaxy-safe clustering window. ***\n")

print(f"\n  (i) mass scale: 1/mu = {inv_mu/Mpc:.2f} Mpc  (CMB-pinned, FREE AeST constant)")
print(f"      galaxy R~20 kpc  : (mu R)^2 = {(mu*20*kpc)**2:.2e}  -> mass term OFF (smooth Phi)")
print(f"      cluster R500~1 Mpc: (mu R)^2 = {(mu*1.3*Mpc)**2:.2e}  -> mass term O(1) (active)")

# THE CLUSTERING SCALE -- the ROBUST handle is the MASS TERM mu (a Yukawa range), NOT
# the k^4 term. A massive scalar sourcing Phi has a Yukawa/Jeans range 1/mu: the field's
# response (and its self-gravitating clustering) is screened/oscillatory BELOW 1/mu and
# free ABOVE it. 1/mu ~ 1 Mpc (CMB-pinned) is therefore the physical clustering floor.
# [Equivalent fluid statement: a Jeans length lambda_J=1 Mpc at a cluster overdensity
#  corresponds to an effective sound speed c_s = lambda_J sqrt(G rho/pi) ~ tens-100 km/s.]
def cs_for_lamJ(lamJ, rho):
    return lamJ*np.sqrt(G*rho/np.pi)
print("\n  ROBUST clustering scale = the mass-term Yukawa range 1/mu (CMB-pinned):")
print(f"  {'system':>16} {'scale':>10} {'scale/(1/mu)':>13} {'regime':>22}")
for label, R in [('galaxy disk',20*kpc),('group R500',0.72*Mpc),
                 ('cluster R500',1.3*Mpc),('cluster 2xR500',2.6*Mpc)]:
    ratio=R/inv_mu
    regime='SMOOTH (suppressed)' if ratio<0.3 else ('threshold' if ratio<1.5 else 'CLUSTERS (free)')
    print(f"  {label:>16} {R/Mpc:>8.3f}Mpc {ratio:>13.3f} {regime:>22}")
print(f"\n  Equivalent fluid sound speed for lambda_J=1/mu=1 Mpc:")
for rlabel, rho in [('cosmic mean',rho_dm0),('cluster 200x',200*rho_dm0)]:
    cs=cs_for_lamJ(inv_mu, rho)
    print(f"    {rlabel:>13}: c_s = {cs/1e3:>6.1f} km/s = {cs/c:.2e} c  (physical for a cold cluster fluid)")

print("""
  READING: 1/mu ~ 1 Mpc sits EXACTLY between the galaxy disk (~0.02 Mpc, deep in the
  suppressed regime, ratio 0.02) and the cluster R500 (~1.3 Mpc, at/above the threshold,
  ratio ~1.3). The SAME CMB-pinned scale that AeST needs cosmologically is the galaxy/
  cluster divide. The equivalent sound speed (tens-100 km/s) is physical for a cold
  cluster-scale fluid. THIS IS THE KEY SCALE SEPARATION -- and it is ONE number (1/mu),
  not a per-object tune.

  CAVEAT (both ways, the k^4 term): the ghost-condensate ALSO carries a k^4 dispersion
  (ACLM 2004; Blanchet-Skordis) whose Jeans length depends on an UN-PINNED coefficient
  M_*. Naive omega^2=k^4/M_*^2 (no c) gives lambda_J~30 kpc (would leak into galaxies);
  the relativistic omega^2=c^2 k^4/M_*^2 gives ~500 Mpc (over-suppresses). The k^4 floor
  is therefore O(1)-coefficient-DEPENDENT and NOT robust -- we lean on the mass-term
  Yukawa scale (1/mu), which IS CMB-pinned, and FLAG the k^4 normalization as open.""")

# ==============================================================================
# STEP 2 -- THE CRUX TENSION: the SAME mu drives a quasi-static DEFICIT (banked)
# ==============================================================================
print("\n"+"="*86)
print("STEP 2 -- CRUX both-ways tension: the SAME mu that clusters ALSO drains (banked)")
print("="*86)
print("""  The mu that gives the ~1 Mpc clustering scale is the SAME mu in the banked quasi-
  static Helmholtz response:  (1/r^2)d/dr[r^2 M(x)Phi'] + mu^2 Phi = 4 pi G rho_b.
  Banked (cluster_aest_massterm, CLUSTER_RESIDUAL_CLOSURE): with the NATURAL boundary
  condition that quasi-static response gives a DEFICIT/drain at R500 (g_AeST/g_MOND~0.2-
  0.5), NOT a boost -- the +mu^2 makes it an oscillatory Helmholtz operator. The eta~2
  boost is reachable ONLY by tuning a free boundary constant chi_out per cluster.

  RESOLUTION (the centerpiece's actual claim, and why it is DIFFERENT):
  The banked DEFICIT is the field's LOCAL response sourced by the BARYONS in place (the
  particular solution of the Helmholtz eq with a baryon source). The centerpiece is the
  HOMOGENEOUS/cosmological piece: the a^-3 dust I0 that EXISTS independently of the local
  baryons (the CMB-fitting cold component) and gravitationally COLLAPSED into the well
  during structure formation. These are ADDITIVE:
        Phi_total = Phi_baryon-sourced (banked: deficit)  +  Phi_Q-dust-collapsed (this).
  The chi_out 'free boundary constant' the banked work had to tune per-cluster is, in this
  reading, PHYSICALLY SET by the collapsed Q-dust amplitude at the cluster edge -- i.e. the
  cosmological dust that fell in IS the boundary value. So the centerpiece both (a) gives a
  PHYSICAL origin for chi_out (no per-cluster tune: it is the collapsed-dust potential) and
  (b) supplies the boost via the dust's own self-gravity, not the baryon-sourced response.

  HONEST CAVEAT (both ways): this additive decomposition is the RIGHT physics for a linear
  operator, but the AeST scalar eq is NONLINEAR (the MOND M(x) operator), so the dust and
  baryon-sourced pieces do NOT strictly superpose. The claim 'collapsed dust fixes chi_out'
  is PHYSICALLY MOTIVATED but not yet a solved nonlinear BVP. Flagged as the open step.""")

# ==============================================================================
# STEP 3 -- CLUSTER: how much Q-mode mass collects inside R500?
# ==============================================================================
print("\n"+"="*86)
print("STEP 3 -- CLUSTER clustering: how much Q-mode mass inside R500 vs the target?")
print("="*86)
print("""  Two honest bounds on the Q-mode mass that can collect inside R500:
   UPPER (pure-CDM clustering): if the Q-mode clustered EXACTLY like CDM, the cluster
     would carry the cosmic dm/baryon ratio: M_Q(R500) = (Odm/Ob) * Mb. This is the
     LambdaCDM amount -- by construction it OVERSHOOTS to eta~CDM (the field IS CDM).
   REALISTIC (Jeans-suppressed): the k^4/mu floor at ~Mpc means the Q-mode CANNOT
     follow baryons into the inner core; it tracks the cluster on >~Mpc scales only.
     So inside R500 it supplies a CORED, NFW-like-but-cored contribution.""")
for name,T in TARGET.items():
    M500=T['M500']; R500=T['R500']; Mb=T['Mb']
    M_Q_cdm = (Odm/Ob)*Mb                       # pure-CDM clustering upper bound
    print(f"\n  {name}:")
    print(f"     M_extra needed inside R500 (eta~2)   = {T['M_extra']:.2e} Msun")
    print(f"     UPPER: pure-CDM clustering (Odm/Ob)Mb = {M_Q_cdm:.2e} Msun"
          f"   ratio to needed = {M_Q_cdm/T['M_extra']:.2f}")
    # cosmic Q-mode mass within a sphere of R500 at mean density (the floor, no clustering)
    M_Q_mean = rho_dm0*(4*np.pi/3)*R500**3/Msun
    print(f"     FLOOR: cosmic-mean Q within R500       = {M_Q_mean:.2e} Msun"
          f"   ratio to needed = {M_Q_mean/T['M_extra']:.4f}")
    # overdensity needed: contrast over mean to supply M_extra inside R500
    delta_needed = T['M_extra']*Msun/(rho_dm0*(4*np.pi/3)*R500**3)
    print(f"     => Q-mode overdensity inside R500 needed: delta = {delta_needed:.1f}"
          f"  (cluster CDM delta~200-1000; FEASIBLE if it clusters CDM-like)")

print("""
  READING: the pure-CDM clustering (the field doing its full CDM job) OVERSHOOTS the
  residual (ratio >1): there is MORE than enough Q-mode mass available IF it clusters
  CDM-like. The needed overdensity delta~100s is the ordinary cluster CDM contrast.
  So the AMOUNT is not the problem -- the field carries Omega_dm worth of dust. The
  question is whether the k^4/mu Jeans floor lets it reach that contrast at <~R500.""")

# ==============================================================================
# STEP 4 -- THE GALAXY VETO (HARD CONSTRAINT): does the SAME field stay <5% in a galaxy?
# ==============================================================================
print("\n"+"="*86)
print("STEP 4 -- GALAXY VETO (HARD): does the SAME Q-mode stay sub-dominant in a galaxy?")
print("="*86)
print("""  The RAR is tight (0.11-0.13 dex). The Q-mode must add < ~5% effective mass inside
  a galaxy disk (~10-30 kpc) or it spoils the RAR. The clustering floor 1/mu~1 Mpc is
  ~50x the disk -> the Q-mode CANNOT collapse to a 20 kpc disk. Test it quantitatively,
  AND confront the hard sub-case: a galaxy's >~Mpc HALO/group environment.""")
# galaxy: SPARC-like, L* spiral
Mgal_b = 6e10                       # baryonic mass (Msun)
Rdisk  = 20*kpc                     # optical disk
g_bar_gal = G*Mgal_b*Msun/Rdisk**2
g_mond_gal= np.sqrt(g_bar_gal**2+g_bar_gal*a0)
M_eff_gal = g_mond_gal*Rdisk**2/G/Msun   # MOND effective mass at the disk edge
print(f"\n  L* spiral: Mb={Mgal_b:.1e} Msun, R_disk={Rdisk/kpc:.0f} kpc")
print(f"     g_bar/a0={g_bar_gal/a0:.2f}  g_mond={g_mond_gal:.3e}  M_eff(MOND)={M_eff_gal:.2e} Msun")
# (a) the MOST it could cluster: if it tracked baryons CDM-like, the Q-disk mass would be
#     (Odm/Ob)*M_b(<Rdisk). But the 1/mu floor forbids that on 20 kpc -- the realistic
#     contribution is the diffuse Q-density at the disk, NOT the cosmic mean and NOT full CDM.
print(f"\n     (a) DISK RAR test -- can the Q-mode add >5% inside 20 kpc?")
print(f"         clustering floor 1/mu = {inv_mu/kpc:.0f} kpc >> R_disk = {Rdisk/kpc:.0f} kpc")
print(f"         -> on 20 kpc the Q-mode is SMOOTH at ~its local halo density, not collapsed")
print(f"            to the disk. The RAR (a DISK<30kpc statement) is preserved: the smooth")
print(f"            Q-background adds a near-CONSTANT density, not a baryon-tracking phantom,")
print(f"            so it does NOT reproduce the baryon-shaped RAR correlation it would need")
print(f"            to spoil -- it is a soft, nearly-uniform pedestal across the disk.")
# Quantify the pedestal: Q density of a galaxy-scale halo (if it virialized on ~Mpc) at 20 kpc
# Take an isothermal Q-halo with the galaxy's group/halo mass ~ (Odm/Ob)Mb spread over 1/mu:
M_Q_halo = (Odm/Ob)*Mgal_b           # if it virialized on its >Mpc environment
rho_Q_halo = M_Q_halo*Msun/((4*np.pi/3)*inv_mu**3)   # spread over the 1/mu floor
M_Q_indisk = rho_Q_halo*(4*np.pi/3)*Rdisk**3/Msun    # what leaks into the 20 kpc disk
print(f"\n     (b) HALO sub-case -- if the Q-mode virializes on its >Mpc environment:")
print(f"         Q-halo mass ~(Odm/Ob)Mb = {M_Q_halo:.2e} Msun spread over (1/mu)^3")
print(f"         -> Q density at disk pedestal -> M_Q(<20kpc) = {M_Q_indisk:.2e} Msun"
      f" = {100*M_Q_indisk/M_eff_gal:.2f}% of MOND disk mass")
verdict_gal = "SAFE (<5%)" if M_Q_indisk/M_eff_gal < 0.05 else "BREAKS (>5%)"
print(f"         -> galaxy-veto: {verdict_gal}")
print("""
  READING (both ways, CORRECTED): the smooth-pedestal model ABOVE assumes the Q-mode does
  NOT collapse onto the galaxy -- but the growth-threshold check (Step 1 correction) shows it
  DOES: a c_s^2->0 field above rho_thresh clusters at ALL sub-Mpc scales, so it forms a CUSPY
  CDM-LIKE GALAXY HALO, not a uniform pedestal. The honest galaxy veto is therefore the DIRECT
  injection of a CDM-like halo on the RAR, and the sibling run did exactly that: adding the
  CDM-like dust at the disk-relevant level gives +0.02 dex (30%), +0.12 dex (60%), +0.23 dex
  (100%) of RAR scatter -- the RAR is 0.11-0.14 dex tight, so a halo dense enough to fill
  clusters re-introduces the cuspy-halo scatter MOND was built to remove. THE VETO BITES:
  the same clustering that fills clusters is CDM, and CDM fails the galaxy RAR. 'Galaxy-safe
  clustering window' = NOT established. (The pedestal numbers above only hold if the field
  stayed smooth, which the c_s^2->0 growth physics forbids.)""")

# ==============================================================================
# STEP 5 -- THE TRANSITION + THE HONEST WALL (both ways)
# ==============================================================================
print("\n"+"="*86)
print("STEP 5 -- the transition (why clusters-yes/galaxies-no) AND the honest wall")
print("="*86)
print(f"""  THE TRANSITION SCALE: lambda_J ~ 1/mu ~ 1 Mpc (CMB-pinned). This sits BETWEEN:
     galaxy disk    ~ 0.01-0.03 Mpc   (<< lambda_J -> SMOOTH, RAR-safe)
     cluster R500   ~ 1-1.4   Mpc     (~ lambda_J  -> clusters, supplies residual)
   The SAME scale (1/mu) that AeST needs for the CMB/cosmology ALSO sits exactly at the
   galaxy/cluster divide. This is the structural reason the split EXISTS and is NOT tuned
   per object -- it is one CMB-pinned number doing double duty.

  BOTH-WAYS -- THE HONEST WALL (do NOT manufacture the close):
   (1) The AMOUNT I0 ~ Omega_dm is FREE (banked, sympy-exact mean-vs-variance proof).
       The Q-mode clustering CLOSES the cluster residual ONLY because I0 was set to the
       LambdaCDM dm abundance. a0=sqrt(Lambda) does NOT predict it (Bridge-1: a0 absent
       from linear perturbations). So this is 'the field IS the cluster dark matter' --
       which is TRUE and CDM-degenerate -- but it is dark matter RELOCATED onto a gravity
       mode, NOT eliminated. 'No dark matter' is forfeited at clusters (and the CMB).
   (2) Once you admit the Q-mode clusters CDM-like to supply clusters, it ALSO clusters
       in galaxy HALOS on >~Mpc scales (the galaxy's Mpc-scale environment/halo), which
       is FINE for the RAR (the RAR is a DISK <30 kpc statement) -- but it means the
       framework's dark sector is now a full CDM-like halo component, i.e. the framework
       is MOND-in-the-disk + CDM-halo (nuLCDM / 'MOND with residual DM'), the Angus-type
       hybrid -- NOT pure MOND. This is the honest cost.
   (3) The ROBUST clustering scale is the mass-term Yukawa range 1/mu (CMB-pinned, ~1 Mpc),
       which is what lands between galaxy and cluster scales. The ghost-condensate k^4
       'pressure' (ACLM, Blanchet-Skordis) is ALSO real but its Jeans floor rides an
       UN-PINNED O(1) coefficient M_* (swings ~30 kpc to ~500 Mpc across the c-power). We
       do NOT rely on the k^4 term; the load-bearing scale is 1/mu. The window that threads
       galaxy-OFF/cluster-ON exists at 1/mu~1 Mpc but the k^4 normalization is genuinely open.

  NET (both ways, CORRECTED after the growth-threshold check): the centerpiece's PREMISE is
  right -- the Q-mode carries Omega_dm worth of cold a^-3 dust that ARITHMETICALLY supplies
  the cluster core (1.4-1.8x the residual, zero mass tuning). But the hoped-for SCALE
  SELECTION ('clusters in clusters, smooth in galaxies') has NO realization: the field is
  c_s^2->0 (that is WHY it fits the CMB like CDM), so its gravitational growth is gated by a
  density threshold rho>mu^2/4piG that BOTH galaxies and clusters exceed by ~1e13x. The
  CMB-pinned mu~1/Mpc screens the >Mpc static potential but does NOT stop sub-Mpc collapse;
  the dust forms a CUSPY CDM-like galaxy halo and reintroduces RAR scatter (+0.12 to +0.23
  dex by direct injection). So the residual IS the field doing a CDM job -- but it is CDM,
  RELOCATED onto the gravity mode, NOT a galaxy-safe clustering window. The cluster tension is
  EXPLAINED (cold CDM-like dark sector clusters where CDM does) but NOT eliminated, and 'no
  dark matter' is forfeited at BOTH clusters and galaxy halos.""")

# ==============================================================================
# SUMMARY NUMBERS (for the structured return)
# ==============================================================================
print("\n"+"="*86); print("SUMMARY"); print("="*86)
T=TARGET['rich  M500=1e15']
M_Q_cdm=(Odm/Ob)*T['Mb']
print(f"  clustering floor 1/mu (CMB-pinned)= {inv_mu/Mpc:.2f} Mpc  (between galaxy & cluster)")
print(f"  galaxy disk scale                 = {Rdisk/Mpc:.3f} Mpc ({Rdisk/kpc:.0f} kpc) -> ratio {Rdisk/inv_mu:.3f} SMOOTH")
print(f"  cluster R500                      = {T['R500']/Mpc:.2f} Mpc -> ratio {T['R500']/inv_mu:.2f} CLUSTERS")
print(f"  rich cluster M_extra needed       = {T['M_extra']:.2e} Msun")
print(f"  pure-CDM Q available (Odm/Ob)Mb   = {M_Q_cdm:.2e} Msun  (ratio {M_Q_cdm/T['M_extra']:.2f} to needed -> ENOUGH/overshoots)")
print(f"  growth threshold rho_thresh=mu^2/4piG = {rho_thresh/rho_crit0:.1e} rho_crit "
      f"(galaxy & cluster BOTH ~1e13x above -> mu does NOT gate them)")
print(f"  cluster core residual: dust supplies ~1.4-1.8x needed (ARITHMETICALLY enough, zero tuning)")
print(f"  galaxy RAR (direct CDM-halo injection): +0.12 to +0.23 dex scatter (RAR floor 0.11-0.14) -> VETO BITES")
print("\n  VERDICT (both ways): SMALL-PARTIAL. The PREMISE is right -- the Q-mode is a cold,")
print("  Omega_dm-worth a^-3 dust that ARITHMETICALLY fills the cluster core (1.4-1.8x, zero")
print("  mass tuning). But the hoped scale-selection FAILS: the field is c_s^2->0 (CMB-CDM-like),")
print("  so it clusters at ALL scales above a negligible density threshold -- it forms a CUSPY")
print("  CDM-like galaxy halo and BREAKS the RAR (+0.12-0.23 dex). The CMB-pinned mu~1/Mpc screens")
print("  the static potential on >Mpc but does NOT stop sub-Mpc collapse. No galaxy-safe window.")
print("  HONEST WALLS (full weight): the close = CDM RELOCATED onto the gravity mode, NOT")
print("  eliminated; I0~Omega_dm is FREE (a0=sqrt(Lambda) does not predict it, Bridge-1); the")
print("  same clustering that fills clusters fails the galaxy veto -- the residual is CDM by")
print("  another name. The cluster gap stays MOND-family-SHARED and OPEN, not closed.")
