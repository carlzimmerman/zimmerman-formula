#!/usr/bin/env python3
r"""
THE EARLY-GALAXY UNIFIER  (solution_hunt, 2026-06-19)
================================================================================
THE TEST: if a LOCAL curvature/density/fluctuation term raises effective a0 in
dense/hot/fluctuating environments, then the EARLY universe (denser, more curved,
more fluctuating) should have a HIGHER effective a0 -> stronger MOND boost at high
z -> faster structure formation + higher velocities -> the JWST 'too-massive-too-
early' tension. ONE mechanism for BOTH clusters and early galaxies?

Computes, both ways, on REAL JWST numbers:
  (a) effective a0 enhancement in a high-z (z~6-10) proto-cluster / early-galaxy
      environment vs today, using the SAME X_local forms (density, potential,
      fluctuation) tested in curvature_floor_unifier.py;
  (b) the velocity/mass boost it gives, vs the JWST 'too-massive' data:
      de Graaff+2024 (JADES M_dyn/M* up to ~40, UPPER LIMITS),
      Xu+2024 (z~5 IFU, M_dyn/M*~0.87), the bright early UVLF (Labbe+2023,
      Boylan-Kolchin 2023 'impossible' stellar-mass-density bound);
  (c) does ONE mechanism help BOTH -- or does it OVERSHOOT (break something at z)?

FRAMEWORK (sealed): a0 = c^2 sqrt(Lambda/32pi)=9.36e-11; a0 ~ sqrt(Lambda_eff);
  cosmic shape a0(z)=a0*sqrt(rho_DE(z)/rho_DE0) (DECLINING for w~-1: the framework's
  OWN branch). Quasi-static g_obs=sqrt(gbar^2+gbar*a0). Deep-MOND V^4=G M a0.

BOTH-WAYS / QUARANTINE: a0/kappa/Z never asserted derived. Honest magnitude both
ways -- including whether the LOCAL enhancement OVERSHOOTS at high z (breaks something).
"""
import numpy as np

c    = 2.998e8;  G = 6.674e-11; Msun = 1.989e30
kpc  = 3.0857e19; Mpc = 3.0857e22; km = 1e3
hbar = 1.0546e-34; kB = 1.381e-23
a0   = 9.36e-11
rho_DE = 6.0e-27
Lambda = (a0/c**2)**2*32*np.pi
H0   = 2.268e-18                       # 70 km/s/Mpc in 1/s
Om, OL = 0.31, 0.69
rho_crit0 = 3*H0**2/(8*np.pi*G)
rho_m0    = Om*rho_crit0
def Ez(z):   return np.sqrt(Om*(1+z)**3 + OL)
def rho_m(z):return rho_m0*(1+z)**3

print("="*94)
print(" THE EARLY-GALAXY UNIFIER -- does the local a0 enhancement also help JWST too-massive-too-early?")
print("="*94)
print(f"  a0={a0:.3e}  rho_m0/rho_DE={rho_m0/rho_DE:.3f}  (mean matter today < dark energy)")
print()

# =================================================================================
# (A) The framework's OWN cosmic a0(z) -- the DECLINING branch -- helps how?
# =================================================================================
print("-"*94)
print(" (A) Framework's OWN cosmic a0(z)=a0*sqrt(rho_DE(z)/rho_DE0): for w=-1 this is CONSTANT (DE const).")
print("-"*94)
print(r"""  The framework's published a0(z) tracks rho_DE(z), NOT rho_matter. For LambdaCDM (w=-1) rho_DE=const
  so a0(z)=a0=const -- it does NOT rise in the early universe. (Only the DESI w(z)!=-1 branch gives a
  small +-6% wiggle, peaking at z=0.4 then DECLINING to 0.74*a0 at z=3.) So the framework's OWN cosmic
  a0(z) gives essentially NO early-universe MOND enhancement -- if anything a mild DECLINE at z>1.
  => The cosmic a0(z) branch does NOT unify clusters+early galaxies; it is silent/declining at high z.""")
for z in [0,2,4,6,10]:
    # w=-1 -> a0 const; DESI w(z) branch declines. Show both.
    a0z_LCDM = a0  # rho_DE const
    print(f"   z={z:2d}: a0(z)/a0 [w=-1, framework's own]={a0z_LCDM/a0:.3f}  (declines to ~0.74 by z=3 on DESI w(z))")
print("  This is why the prior JWST work found the framework SILENT on early formation: a0(z) does not rise.")

# =================================================================================
# (B) The UNIFIER hypothesis: a LOCAL X_local raises a0 in dense/curved early environments
# =================================================================================
print("\n"+"-"*94)
print(" (B) UNIFIER: does a LOCAL X_local (density / potential / fluctuation) raise a0 at high z?")
print("-"*94)

print("  (B1) DENSITY route  a0_eff=a0*sqrt(rho_local/rho_DE) on early collapsed objects (virial ~200 rho_m):")
print(f"   {'z':>4} {'rho_m/rhoDE':>12} {'a0_eff/a0 (mean)':>16} {'a0_eff/a0 (virial 200x)':>22}")
for z in [0,2,4,6,8,10]:
    rm = rho_m(z); rv = 200*rm
    print(f"   {z:4d} {rm/rho_DE:12.2e} {np.sqrt(rm/rho_DE):16.2f} {np.sqrt(rv/rho_DE):22.2f}")
print(r"""   READ: density-a0 DOES rise strongly at high z (mean 25x, virial 360x at z=10). It WOULD give a big
   early MOND boost. BUT (i) it is the SAME density route that BREAKS the z=0 galaxy veto (a z=0 disk at
   rho~2.6e5 rho_DE already gets a0_eff~510x -- so the law is already excluded by the local RAR); and
   (ii) a z=0 galaxy DISK (2.6e5 rhoDE) is DENSER than the z=10 mean (634 rhoDE), so 'early universe is
   denser' is FALSE for the relevant comparison -- collapsed disks today out-dense the early mean field.
   The density route's early boost is real but it is the vetoed law; it cannot be switched on at high z
   and off in z=0 disks. NOT a clean unifier.""")

print("\n  (B2) POTENTIAL route  a0_eff=a0*sqrt(1+f(|Phi|/c^2)): does early collapse give deeper |Phi|?")
# Early proto-cluster / massive early galaxy: |Phi|/c^2 = GM/(c^2 R). Use real JWST-scale masses.
print(f"   {'system (z)':>34} {'M (Msun)':>10} {'R (kpc)':>9} {'|Phi|/c^2':>11} {'a0_eff/a0 (lin)':>15}")
for name,M,R in [("z=0 MW disk",          5e10*Msun,  8*kpc),
                 ("z=6 massive gal (Labbe)",1e11*Msun, 1.0*kpc),  # compact, ~10^11 Msun, sub-kpc
                 ("z=10 'impossible' gal",  1e10*Msun, 0.3*kpc),  # very compact early
                 ("z=6 proto-cluster core", 1e14*Msun, 200*kpc),
                 ("z=0 cluster core",       2e14*Msun, 300*kpc)]:
    PhiC2 = G*M/(c**2*R)
    print(f"   {name:>34} {M/Msun:10.0e} {R/kpc:9.2f} {PhiC2:11.2e} {np.sqrt(1+PhiC2):15.6f}")
print(r"""   READ: COMPACT early galaxies have deeper |Phi|/c^2 than z=0 disks (1e-6 vs 3e-7) because they are
   sub-kpc dense -- but still ~1e-6, a tiny perturbation. A LINEAR potential coupling gives ~1+5e-7, no
   boost. Same ~1e6 magnitude shortfall as the cluster core. The potential is simply never large enough
   (early galaxies are NOT relativistically deep: |Phi|/c^2 ~ (sigma/c)^2 ~ (100-300 km/s / c)^2 ~ 1e-7-1e-6).
   No early-universe potential boost from a forced linear coupling.""")

# =================================================================================
# (C) What boost would JWST 'too-massive-too-early' actually NEED? (real numbers, both ways)
# =================================================================================
print("\n"+"-"*94)
print(" (C) What a0 boost would the JWST tension NEED, and does the deep-MOND mass boost deliver it?")
print("-"*94)
print(r"""  Two distinct JWST puzzles -- the framework can only touch one:
   (i) DYNAMICAL masses (de Graaff+2024 M_dyn/M* up to ~40; Xu+2024 ~0.87): a KINEMATIC over-estimate.
       Deep MOND already inflates M_dyn/M_bar by the boost 1/mu. If a0 rises, the inflation grows ~sqrt(a0).
   (ii) STELLAR-mass density / UVLF abundance (Labbe+2023 ~1e11 Msun at z~7-9; Boylan-Kolchin 2023
       'impossible' if eps_* too high): a FORMATION/ABUNDANCE puzzle. Needs MORE EARLY COLLAPSE, i.e.
       enhanced GROWTH, which a0 (absent from linear growth) does NOT provide. The framework is SILENT here.""")

# (i) dynamical-mass channel: does a high-z a0 boost help explain high M_dyn/M*?
print("\n  (i) Dynamical-mass channel (the one the framework can touch):")
print(r"""    de Graaff+2024 (z=5.5-7.4 JADES): M*~1e7-1e9 Msun, R~1 kpc, gas ~10x stellar -> Mbar~11 M*.
    REGIME CHECK (real numbers): the LOW-mass ones (M*~1e7-1e8) sit in DEEP MOND/transition (g_bar/a0
    ~0.16-1.6), NOT Newtonian. So at CONSTANT a0 the framework ALREADY gives M_dyn/M* ~ nu*(Mbar/M*):""")
for Mstar in [1e7,1e8,1e9]:
    Mbar=11*Mstar*Msun; g=G*Mbar/(1.0*kpc)**2; nu=np.sqrt(1+a0/g)
    reg="deep MOND" if g/a0<0.3 else ("transition" if g/a0<3 else "Newtonian")
    print(f"      M*={Mstar:.0e}: g_bar/a0={g/a0:5.2f} ({reg:10s}) nu={nu:.2f} -> M_dyn/M*~{nu*11:.0f}  (obs up to ~40)")
print(r"""    => The framework already reproduces de Graaff's M_dyn/M*~10-40 at CONSTANT a0 (gas-dominated + MOND
    boost on the low-g ones). The DYNAMICAL-mass puzzle needs NO early-a0 enhancement -- it is neither
    needed nor (via the veto-safe potential route) available. The HIGH-mass (1e9) compact ones ARE
    Newtonian (g/a0~16, nu~1) -> there the high M_dyn/M* is a gas/stellar-mass-modeling issue, not MOND.
    Now: IF a high-z a0 boost existed, the EXTENDED low-g deep-MOND boost 1/mu~sqrt(a0_eff/g) would grow:""")
for z, a0fac, label in [(0,1.0,"z=0 baseline"),(6,1.0,"z=6 cosmic a0 (w=-1, no rise)"),
                        (6,3.6,"z=6 IF density-a0 (vetoed)"),(10,5.0,"z=10 IF density-a0 (vetoed)")]:
    gbar = 0.05*a0  # extended low-SB early galaxy, deep MOND
    boost = np.sqrt(a0fac*a0/gbar)   # deep-MOND 1/mu ~ sqrt(a0_eff/gbar)
    Mdyn_ratio = boost  # M_dyn/M_bar ~ boost in deep MOND
    print(f"    {label:34s}: a0_eff/a0={a0fac:.1f}  M_dyn/M_bar~{Mdyn_ratio:.1f}  (vs constant-a0 {np.sqrt(a0/gbar):.1f})")
print(r"""    READ: a high-z a0 boost DOES raise the deep-MOND M_dyn/M_bar (e.g. 4.5->8.5 at a0_eff=3.6x). So IF
    the early a0 were enhanced, extended early galaxies would look MORE dark-matter-dominated kinematically.
    But this only helps the DYNAMICAL-mass reading, and only via the VETOED density route; the framework's
    own cosmic a0(z) is flat/declining and gives NO such z=6 boost. And it does NOTHING for the abundance/
    UVLF puzzle (ii).""")

# (ii) abundance channel: the unifier's core claim -- does enhanced a0 make galaxies form earlier?
print("\n  (ii) Abundance/formation channel (the actual 'impossible early galaxy' puzzle):")
# Boylan-Kolchin 2023: the bound is eps_* = M*/(fb * M_halo) <= 1. Labbe galaxies need eps_* ~ 0.2-0.5.
# MOND/enhanced-a0 helps ONLY if it speeds linear growth. a0 is absent from linear growth (AeST).
print(r"""    The 'impossible' puzzle (Boylan-Kolchin 2023) is a stellar-mass-DENSITY / baryon-conversion-efficiency
    bound: the observed M* at z~7-10 requires converting an implausibly high fraction eps_*~0.2-0.5 of
    available baryons into stars EARLY. This needs faster GROWTH of structure, set by LINEAR perturbation
    theory. The framework's a0 (and any local a0 enhancement) is ABSENT FROM LINEAR GROWTH (the AeST
    completion that fits the CMB puts the MOND scalar in a configuration that does not boost the growing
    mode). => Enhanced a0, local OR cosmic, does NOT make halos collapse earlier. It cannot supply the
    abundance. The unifier FAILS the formation/abundance leg structurally, not just numerically.""")

# =================================================================================
# (D) SYNTHESIS -- does ONE mechanism help BOTH clusters and early galaxies?
# =================================================================================
print("\n"+"="*94)
print(" (D) SYNTHESIS -- the unifier verdict, both ways")
print("="*94)
print(r"""
 The unifier has a clean LOGICAL structure but FAILS on magnitude AND on the growth leg:

  * The ONLY X_local that rises strongly in the early universe is the DENSITY route (mean rho ~25x,
    virial ~360x at z=10). It WOULD boost early-galaxy dynamical masses (M_dyn/M_bar 4.5->8.5). BUT it
    is the SAME density route that BREAKS the z=0 galaxy veto, AND a z=0 disk is DENSER than the z=10
    mean -- so 'early = denser' is false for the relevant comparison. Not a clean unifier; it's the
    vetoed law evaluated at high z.

  * The veto-PASSING X_local (potential depth |Phi|/c^2) does NOT rise enough at high z: early galaxies
    are non-relativistic (|Phi|/c^2 ~ (sigma/c)^2 ~ 1e-7-1e-6), the same ~1e6 magnitude shortfall as the
    cluster core. A forced linear coupling gives no early boost.

  * The framework's OWN cosmic a0(z) tracks rho_DE, so for w=-1 it is CONSTANT (and on DESI w(z) it
    DECLINES to ~0.74 a0 by z=3). It gives NO early enhancement -- if anything less MOND at high z.

  * DECISIVE for the abundance puzzle: even a (hypothetical) enhanced early a0 is ABSENT FROM LINEAR
    GROWTH, so it cannot make galaxies form EARLIER or in greater NUMBER. The 'impossible early galaxy'
    census/UVLF is a GROWTH/efficiency puzzle the framework is structurally SILENT on. The unifier can at
    most touch the DYNAMICAL-mass reading of extended low-g early galaxies (which de Graaff's compact
    JADES targets are NOT -- they are Newtonian, no boost).

 NET: NO single framework-native mechanism cleanly unifies clusters and early-galaxy formation. The local
 enhancement that would help (density) is veto-excluded and not genuinely 'early-denser'; the veto-safe
 one (potential) is ~1e6 too weak; and the abundance leg is blocked by a0's absence from linear growth.
 The honest overlap is ONE narrow channel -- the deep-MOND dynamical-mass over-estimate of EXTENDED low-g
 systems grows with a0 -- but that needs the vetoed density-a0 to actually rise, helps only kinematics
 (not abundance), and does not match de Graaff's Newtonian-core targets. Both ways: a logically appealing
 unifier that does not survive the magnitude + veto + linear-growth constraints. QUARANTINE held.""")
