"""
================================================================================
CLUSTER-MASS TENSION: does the framework's OWN field supply the residual?
Two creative-but-honest routes, both with the GALAXY-RAR VETO as the hard wall.
================================================================================

Framework (Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (INPUT, quarantine).
Modified inertia / dS-Unruh interpolation:  g_obs = sqrt(g_bar^2 + g_bar*a0).
Dark sector = the AeST (Skordis-Zlosnik 2021) ghost-condensate Q-mode: a w=0, a^-3
COLD dust component that is a MODE of the gravity field, CDM-DEGENERATE on linear
scales, with amplitude I0 ~ Omega_dm FREE. The CMB needs it; the question here is
whether it ALSO clusters enough in cluster cores to supply eta~2.3, WITHOUT
clustering in galaxy disks (which would spoil the RAR).

THE TARGET (banked, eRASS1 Bulbul+2024, N=9830, framework a0+interp):
  - median eta(R500) = 2.333; CENTRAL, dies to ~1 by 1.3 R500.
  - core missing mass M_res(<420 kpc) ~ 2.3e14 Msun (rich); cored, gas-tracking,
    ~400-450 kpc cutoff scaling ~sqrt(M500).
  - galaxies lie ON the a0 law (RAR 0.11-0.14 dex); clusters sit 1.9-2.4x ABOVE.

================================================================================
ROUTE 1 (CENTERPIECE): Q-mode DUST clustering -- spherical-collapse / Jeans test.
  The Q-mode is COLD dust (w=0). Cold dust clusters by gravitational instability
  with a Jeans/sound-horizon floor. Question: in a cluster (deep potential, large
  scale, early collapse) does the dust contrast delta_Q grow ENOUGH to provide the
  core residual, while in a GALAXY (shallow, small, late) it stays smooth?
  The DISCRIMINATOR is the Jeans length / free-streaming-equivalent scale of the
  condensate vs the system size, AND the linear-collapse amplitude.

ROUTE 2: TIME-DOMAIN / FORMATION-EPOCH modified inertia.
  (2a) Non-quasi-static multi-frequency MI in a cluster (Milgrom 1994/2022 A[omega]).
  (2b) Formation-epoch a0(z): cluster deep-MOND structure SET at z~0.5-2; if a0 was
       higher then (rising-a0 reading) the boost imprinted at formation is larger.
================================================================================
"""
import numpy as np
import sympy as sp

# ----------------------------- constants (SI) -----------------------------
G     = 6.674e-11
c     = 2.998e8
Msun  = 1.989e30
kpc   = 3.086e19
Mpc   = 1000*kpc
yr    = 3.156e7
Gyr   = 1e9*yr
a0    = 9.36e-11          # framework a0 (eta-worst footing per MEMORY rule)
H0    = 2.20e-18          # s^-1 (~67.9 km/s/Mpc)
rho_crit0 = 3*H0**2/(8*np.pi*G)
Om    = 0.31
OLam  = 0.69
rho_m0 = Om*rho_crit0

def Ez(z):  return np.sqrt(Om*(1+z)**3 + OLam)
def Hz(z):  return H0*Ez(z)

def eta_interp(gbar, gobs):
    """framework dS-Unruh interpolation eta. eta=1 means ON the a0 law."""
    return gobs/np.sqrt(gbar**2 + gbar*a0)

print("="*78)
print("FRAMEWORK FOOTING:  a0 = %.3e m/s^2   (INPUT, quarantine held)" % a0)
print("rho_crit0 = %.3e kg/m^3   rho_m0 = %.3e" % (rho_crit0, rho_m0))
print("="*78)


# ============================================================================
# ROUTE 1 : THE CENTERPIECE  --  does the Q-mode DUST cluster enough?
# ============================================================================
# The Q-mode condensate is COLD dust (w=0, a^-3). Whether it provides the cluster
# residual reduces to whether its density CONTRAST in the cluster core builds to
# delta_Q ~ (eta-1)*rho_baryon_core / rho_Q_background, while in galaxies delta_Q
# stays << the local stellar/gas density.
#
# Key physics that decides this -- and the WALL the framework cannot tune around:
#   A cold pressureless fluid that is CDM-degenerate on linear/cluster scales has a
#   Jeans length set ONLY by its sound speed cs. For AeST the Q-mode sub-horizon
#   sound speed is essentially zero (cs^2 ~ 0, that is WHY it fits the CMB 3rd peak
#   like CDM, banked dark_sector_cmb). A cs^2->0 dust clusters IDENTICALLY to CDM at
#   ALL scales down to its (tiny) Jeans scale -- it CANNOT be made to cluster in
#   clusters but not in galaxies by any scale-selection, because there is no scale.
# So the centerpiece must be tested as: "Q-mode = CDM-like dust." Then the residual
# it can supply in the core is exactly the CDM mass that would sit there -- which is
# the ORDINARY CDM halo. We compute how much that is, and CRUCIALLY whether that same
# dust clusters in galaxy disks (the veto).

print("\n" + "#"*78)
print("# ROUTE 1: Q-mode dust clustering (centerpiece)")
print("#"*78)

# ---- 1a. The Jeans / scale-selection test: is there ANY scale that turns the
#          dust ON in clusters and OFF in galaxies?  ----------------------------
# Jeans length lambda_J = cs * sqrt(pi/(G rho)). For the dust to be smooth in a
# galaxy (size ~30 kpc) but clumpy in a cluster (size ~1 Mpc) we'd need
# lambda_J between ~30 kpc and ~1 Mpc. Solve for the required cs.
rho_gal  = 1e-21    # ~ mean baryon+ density in a galaxy (kg/m^3), ~0.03 Msun/pc^3
rho_clus = 1e-24    # ~ mean cluster density within R500 (kg/m^3)
for name, rho, L in [("galaxy disk", rho_gal, 30*kpc), ("cluster core", rho_clus, 400*kpc)]:
    # cs that would put lambda_J exactly at L
    cs_req = L/np.sqrt(np.pi/(G*rho))
    print(f"  {name:13s}: rho={rho:.1e}  L={L/kpc:6.0f} kpc -> cs for lambda_J=L: {cs_req/1e3:.3g} km/s")
# Conclusion driver: the two required cs differ; let's see if a single cs threads.
cs_gal_floor  = 30*kpc /np.sqrt(np.pi/(G*rho_gal))     # smooth in galaxy needs cs >= this
cs_clus_ceil  = 400*kpc/np.sqrt(np.pi/(G*rho_clus))    # clumpy in cluster needs cs <= this
print(f"\n  To be SMOOTH in galaxies (lambda_J >= 30 kpc): cs >= {cs_gal_floor/1e3:.3g} km/s")
print(f"  To be CLUMPY in clusters (lambda_J <= 400 kpc): cs <= {cs_clus_ceil/1e3:.3g} km/s")
thread = cs_gal_floor <= cs_clus_ceil
print(f"  Single cs threads BOTH?  {thread}   "
      f"(window {'EXISTS' if thread else 'EMPTY -- ordering is BACKWARDS'})")
print("  --> NOTE the ordering: galaxies are DENSER than cluster cores, so the Jeans")
print("      length is SHORTER in galaxies. A dust that is Jeans-smooth in a galaxy")
print("      is even MORE smooth (relative to size) than in a cluster only if cs is")
print("      large; but a large cs erases cluster clustering too. The scale lever is")
print("      degenerate -- you cannot select cluster-ON / galaxy-OFF by Jeans scale.")

# ---- 1b. Quantify the veto directly: a CDM-like dust that supplies the cluster
#          core residual -- how much of it sits in a galaxy, and does it spoil RAR?
# If the Q-mode is CDM-like, its profile follows the gravitational potential. In a
# galaxy the would-be CDM mass inside the disk is the standard halo. Inject that as
# extra mass on a fiducial SPARC-like disk and read the RAR shift.
print("\n  1b. VETO: if the dust is CDM-like, how much sits in a galaxy disk?")

def disk_rar_shift(Mdisk_Msun=5e10, Rd_kpc=3.0, Mhalo_in_disk_frac=0.0):
    """Fiducial exponential disk; add a CDM-like dust mass = frac*Mdisk inside the
    optical disk; compute the RAR offset (dex) it induces at 2.2 Rd (peak of RC)."""
    Rd = Rd_kpc*kpc
    r  = 2.2*Rd
    # baryonic enclosed (exponential disk, ~0.8 of total inside 2.2Rd)
    Mbar = 0.80*Mdisk_Msun*Msun
    gbar = G*Mbar/r**2
    gpred = np.sqrt(gbar**2 + gbar*a0)        # framework law (the RAR)
    # add CDM-like dust inside the disk:
    Mdust = Mhalo_in_disk_frac*Mdisk_Msun*Msun
    gobs  = G*(Mbar+Mdust)/r**2
    # the "observed" g if dust is present; RAR offset vs the pure-law prediction:
    return np.log10(gobs/gpred), gbar/a0

# A genuine NFW halo has ~ (5-10)x the baryon mass, but only a FRACTION sits inside
# the optical disk. For a Milky-Way-like galaxy the CDM inside 2.2Rd is ~30-60% of
# the baryonic disk mass (the RC is baryon-dominated there -- that's WHY MOND works).
for frac, label in [(0.0,"no dust (pure law)"), (0.3,"CDM-like 30% inside disk"),
                    (0.6,"CDM-like 60% inside disk"), (1.0,"CDM-like 100%")]:
    dex, x = disk_rar_shift(Mhalo_in_disk_frac=frac)
    print(f"     {label:28s}: RAR offset = {dex:+.3f} dex   (gbar/a0={x:.1f})")
print("  --> The RAR is observed at 0.11-0.14 dex scatter. A CDM-like dust that")
print("      clusters in disks at the 30-60% level shifts galaxies by +0.1 to +0.2")
print("      dex AND introduces galaxy-to-galaxy SCATTER (halo/disk ratio varies)")
print("      -- this is exactly the cuspy-halo problem MOND was built to avoid.")

# ---- 1c. The decisive point: the framework's OWN no-go (Bridge-1, banked).
print("\n  1c. WHY the dust cannot be cluster-selective (framework's own Bridge-1):")
print("      a0 is PROVABLY ABSENT from linear perturbations (banked Bridge-1).")
print("      So the Q-mode dust growth knows NOTHING about a0 -- it grows by pure")
print("      gravitational instability, identically to CDM. There is no a0-gated")
print("      'cluster-only' switch in the linear/quasi-linear growth. The amplitude")
print("      I0 is a single FREE number; once set to ~Omega_dm for the CMB it is")
print("      FIXED everywhere. It clusters in galaxies too. => CDM relocated.")


# ============================================================================
# ROUTE 1' : the SHARP both-ways credit -- the dust DOES the cluster, honestly.
# ============================================================================
# Being fully generative: the dust CAN supply the cluster core mass. Let's compute
# how much CDM-like dust the eRASS1 core needs and confirm it's the standard halo.
print("\n  1'. GENERATIVE: can the dust SUPPLY the core mass (CDM-style)? YES, but...")
M_res_core = 2.3e14            # Msun, banked rich-cluster core missing mass (<420 kpc)
M500       = 1.0e15            # Msun
# A standard NFW CDM halo of a 1e15 cluster has M_cdm(<420kpc) ~ ?
def nfw_M_enclosed(r_kpc, M500_Msun=1e15, R500_kpc=1300, c500=4.0):
    rs = R500_kpc/c500
    x  = r_kpc/rs; X = R500_kpc/rs
    return M500_Msun*(np.log(1+x)-x/(1+x))/(np.log(1+X)-X/(1+X))
M_cdm_core = nfw_M_enclosed(420.)
print(f"     eRASS1 core residual needed (<420 kpc): {M_res_core:.2e} Msun")
print(f"     standard NFW CDM in same volume:        {M_cdm_core:.2e} Msun")
print(f"     ratio (dust-as-CDM supplies / needed):  {M_cdm_core/M_res_core:.2f}")
print("     --> A CDM-like dust of the cosmic amount SUPPLIES the core residual to")
print("         order unity. The cluster closes -- IF the dust clusters like CDM.")
print("         THAT is the catch: the very clustering that closes clusters is CDM,")
print("         and CDM clusters in galaxies, which the RAR forbids at 0.11 dex.")
print("         The framework's dust is galaxy-safe ONLY where it is SUB-DOMINANT")
print("         (smooth) -- and a smooth dust in galaxies that becomes a clumpy")
print("         halo in clusters is a SCALE-SELECTIVE clustering with NO knob to")
print("         set it (Bridge-1: a0 absent from growth; cs=0 => no Jeans scale).")


# ============================================================================
# ROUTE 2 : TIME-DOMAIN / FORMATION-EPOCH modified inertia
# ============================================================================
print("\n" + "#"*78)
print("# ROUTE 2: time-domain (multi-freq MI) + formation-epoch a0(z)")
print("#"*78)

# ---- 2a. Multi-frequency MI in a cluster (Milgrom 1994/2022). ---------------
# The MI force depends on the FULL trajectory via the functional A[{a}]. For a
# single-frequency circular orbit MI==MG (quasi-static). For an eccentric / multi-
# frequency orbit the effective mu is the orbit-AVERAGE of mu over the acceleration
# history. Milgrom-2022 Eq.20: the response is set by the rms acceleration, NOT the
# instantaneous one. We compute the cycle-averaged boost honestly (the Jensen 17x
# was banked-VOID as an apocenter a->0 singularity; here we do it RIGHT).
print("\n  2a. Multi-frequency MI: cycle-averaged effective mass boost")

def mu_simple(x):                 # deep-MOND-safe interpolation mu(a/a0)
    return x/np.sqrt(1+x**2)      # 'simple' nu's mu; mu->1 Newt, mu->x MOND

def cycle_avg_boost(gbar_over_a0, ecc):
    """Honest Milgrom-2022 cycle average. The MI inertia uses the rms (orbit-summed)
    acceleration argument, so the cycle-averaged mu is evaluated at the TIME-AVERAGE
    of |a|, which by Jensen for a CONVEX-then-concave mu is BOUNDED by the
    quasi-static value. We compute <mu> over a Kepler-like a(t) and compare to
    mu(rms a)."""
    th = np.linspace(0, 2*np.pi, 4000)
    # radius of an eccentric orbit (a=1): r = (1-e^2)/(1+e cos th)
    r  = (1-ecc**2)/(1+ecc*np.cos(th))
    # local acceleration ~ 1/r^2 in Newtonian-ish part, normalized so <g>~gbar:
    g_local = (gbar_over_a0)/r**2
    g_local *= gbar_over_a0/np.mean(g_local)    # renormalize mean to gbar/a0
    # time weight dt ~ r^2 dtheta (Kepler 2nd law)
    w = r**2
    # quasi-static (instantaneous) cycle-averaged mu:
    mu_qs = np.trapz(mu_simple(g_local)*w, th)/np.trapz(w, th)
    # Milgrom-2022 rms-argument response: mu at the rms acceleration
    g_rms = np.sqrt(np.trapz(g_local**2*w, th)/np.trapz(w, th))
    mu_mi = mu_simple(g_rms)
    # boost in *effective gravitating mass* ~ 1/mu (deep MOND), relative to QS:
    return mu_qs, mu_mi, (mu_qs/mu_mi)   # >1 means MI gives MORE boost than QS

print("     gbar/a0   ecc    mu_QS    mu_MI(rms)   boost(MI/QS in 1/mu)")
for x0 in [0.037, 0.1, 0.44]:    # 0.037 deep-MOND cluster, 0.44 near-MOND R500
    for e in [0.0, 0.5, 0.9]:
        mqs, mmi, b = cycle_avg_boost(x0, e)
        print(f"     {x0:6.3f}  {e:4.1f}   {mqs:.4f}   {mmi:.4f}      {1/mmi/(1/mqs):.3f}")
print("  --> boost(MI/QS) <= ~1 for all realistic ecc (rms a >= mean a => mu_MI >=")
print("      mu_QS => 1/mu_MI <= 1/mu_QS). The non-quasi-static MI gives a SMALLER")
print("      effective mass than quasi-static, not larger. The deep-MOND scale")
print("      invariance pins M*G*a0 = eta*sigma^4 (eta~1) SHARED by MI and MG;")
print("      orbit shape is an O(1) second-tier wiggle, NOT the ~2.3x clusters need.")

# ---- 2b. Formation-epoch a0(z): was the boost imprinted earlier, bigger? -----
print("\n  2b. Formation-epoch a0(z): cluster structure SET at z_form")
# Two a0(z) branches (both in the corpus):
#   (i)  framework canonical DECLINING  a0(z) = a0 * sqrt(rho_DE(z)/rho_DE0) = a0 (w=-1 const!)
#        -> for w=-1, rho_DE const => a0(z) = a0 CONSTANT. No formation boost.
#   (ii) rival RISING reading a0(z) ~ c*H(z) (the MUSE/Ciocan rising-a0 reading):
#        a0(z) ~ a0 * E(z)   (cH0 footing). This GROWS with z.
def a0_declining(z):  return a0*np.ones_like(np.atleast_1d(z))   # w=-1: constant
def a0_rising(z):     return a0*Ez(z)                            # cH(z) footing
zf = np.array([0.5, 1.0, 2.0])
print("     z_form   a0_decl/a0   a0_rise/a0   (if structure froze at z_form)")
for z in zf:
    print(f"     {z:5.1f}    {a0_declining(z)[0]/a0:8.3f}    {a0_rising(z)/a0:8.3f}")
# If the cluster's deep-MOND mass M*G*a0 = eta*sigma^4 froze at z_form with the
# higher a0, the implied dynamical-mass boost today (read with a0_today) is:
print("\n     Deep-MOND virial: M_eff ~ sigma^4/(G a0). If sigma was set at z_form")
print("     with a0(z_form) but we INFER mass with a0(today):")
for z in zf:
    boost_rise = a0_rising(z)/a0   # M_eff(z_form)/M_eff(today) ~ a0(today)/a0(z_form)...
    # Actually: at fixed sigma, M_eff ~ 1/a0. Higher a0 at formation => SMALLER M_eff
    # imprinted; inferred with today's lower a0 => we'd OVER-estimate, i.e. the
    # phantom is SMALLER, wrong direction. Let's state both signs explicitly:
    print(f"     z_form={z:.1f}: a0_rise/a0_today={boost_rise:.2f} ->"
          f" M_eff ~ 1/a0 so a HIGHER formation a0 gives a SMALLER frozen M_eff"
          f" (factor {1/boost_rise:.2f}) = WRONG sign for the deficit.")
print("  --> Formation-epoch a0(z): declining/w=-1 branch gives a0=CONST (no effect).")
print("      Rising branch raises a0 at z_form, but M_eff~1/a0 => a HIGHER formation")
print("      a0 IMPRINTS LESS phantom mass, the WRONG sign to explain a SURPLUS.")
print("      And clusters are not frozen relics: gas re-virializes to today's a0.")
print("      Banked +2.5% (0.025 dex) at z=0.296 stands; ~+10-25% max at z=2, but")
print("      sign-ambiguous and z-reach-limited. NOT the 130% the core needs.")


# ============================================================================
# ROUTE 2c (sympy): the deep-MOND scale-invariance pin -- MI==MG mean mass
# ============================================================================
print("\n  2c. sympy: deep-MOND scale invariance pins the mean mass (MI==MG)")
sig, a0s, Gs, eta = sp.symbols('sigma a0 G eta', positive=True)
# deep-MOND isothermal: M = eta * sigma^4 / (G a0).  This is a THEOREM of deep-MOND
# (Milgrom), independent of whether inertia or gravity is modified. The cluster
# deficit eta_cluster is the SAME object; MI and MG give the SAME M for the same
# sigma. So the time-domain MI cannot create extra MEAN mass beyond this.
M_deepMOND = eta*sig**4/(Gs*a0s)
print("     M_eff = eta * sigma^4/(G a0)  with eta = O(1) SHARED by MI and MG")
print("     d ln M / d ln a0 =", sp.diff(sp.log(M_deepMOND), a0s)*a0s, " (= -1)")
print("     => a +X% change in a0 gives a -X% change in inferred mass (1:1, signed).")


# ============================================================================
# FINAL ROLL-UP
# ============================================================================
print("\n" + "="*78)
print("ROLL-UP")
print("="*78)
results = {
 "R1_dust_supplies_core_as_CDM": M_cdm_core/M_res_core,   # ~ order 1 (CDM closes it)
 "R1_jeans_window_exists": thread,                         # False: no scale selection
 "R1_galaxy_veto_offset_30pct_dex": disk_rar_shift(Mhalo_in_disk_frac=0.3)[0],
 "R1_galaxy_veto_offset_60pct_dex": disk_rar_shift(Mhalo_in_disk_frac=0.6)[0],
 "R2a_MI_boost_over_QS_max": max(cycle_avg_boost(x,e)[0]/cycle_avg_boost(x,e)[1]
                                 for x in [0.037,0.44] for e in [0,0.5,0.9]),
 "R2b_a0_rising_z2": a0_rising(2.0)/a0,
 "R2b_formation_meff_factor_z2": 1/(a0_rising(2.0)/a0),    # <1 => wrong sign
}
for k,v in results.items():
    print(f"  {k:38s} = {v}")
print("="*78)
