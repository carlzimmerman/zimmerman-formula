#!/usr/bin/env python3
"""
ROUTE 1 -- companion: the Q-mode DENSITY PROFILE in a cluster vs a galaxy, computed
with a Jeans-filtered (1/mu) clustering transfer function.
================================================================================
Goal: turn the integrated-mass argument (route1_qmode_clustering_profile.py) into an
actual rho_Q(r) and eta_Q(r) for a cluster and a galaxy, using the SAME CMB-pinned
1/mu~1 Mpc clustering floor as a Jeans filter on CDM-like collapse.

PHYSICS (both ways, honest):
  A pressureless CDM tracks the potential and forms an NFW profile. The Q-mode has a
  Jeans/Yukawa floor 1/mu: density perturbations with wavelength < 1/mu are SUPPRESSED.
  We model this as a CDM-like NFW collapse CONVOLVED with a smoothing of scale ~1/mu
  (a fuzzy-DM-like core). Concretely we take the Q-mode profile = NFW(M_Q, c) but with a
  CORE radius r_core ~ 1/mu, i.e. a cored-NFW / Burkert-like profile (the generic outcome
  of a Jeans floor: a soliton/core of size ~the de Broglie/Jeans length).

  In a CLUSTER (R500~1.3 Mpc >~ 1/mu): the core (~1 Mpc) is COMPARABLE to R500, so the
  Q-mode is cored but still delivers most of its mass within R500 -> fills the residual.
  In a GALAXY (R_disk~20 kpc << 1/mu): the core (~1 Mpc) is ~50x the disk, so the Q-mode
  is nearly UNIFORM across the disk (a soft pedestal) -> negligible, baryon-uncorrelated.

  This is the SAME mechanism fuzzy DM uses to make cores in dwarfs; here the floor is at
  ~Mpc (1/mu) instead of ~kpc, which is what separates clusters from galaxies.
QUARANTINE: a0/Z/I0 never asserted derived; I0~Omega_dm is INPUT; mu free, CMB-pinned.
"""
import numpy as np
from scipy.integrate import quad

c=2.99792458e8; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
a0=9.36e-11; H0=67.4e3/Mpc
Om,OL,Ob=0.315,0.685,0.0493; Odm=Om-Ob
rho_crit0=3*H0**2/(8*np.pi*G)
inv_mu=1.0*Mpc; mu=1.0/inv_mu

def nu_dS(g_bar):  # framework dS-Unruh interpolation
    return np.sqrt(g_bar**2+g_bar*a0)

# cored-NFW (Jeans-floored) Q-mode profile: rho = rho_s / [(1+r/rc)(1+(r/rc)^2 ... )]
# Use a Burkert profile (flat core of size rc, NFW-like outskirt) -- the canonical
# Jeans-floored DM profile. rho_B(r)= rho0 rc^3 / [(r+rc)(r^2+rc^2)].
def burkert_rho(r, rho0, rc):
    return rho0*rc**3/((r+rc)*(r**2+rc**2))
def burkert_Menc(r, rho0, rc):
    # analytic enclosed mass of Burkert
    x=r/rc
    return np.pi*rho0*rc**3*( np.log(1+x**2) + 2*np.log(1+x) - 2*np.arctan(x) )

print("="*84)
print("ROUTE 1 companion -- Q-mode density profile (Jeans-floored, rc~1/mu) cluster vs galaxy")
print("="*84)
print(f"  clustering floor rc = 1/mu = {inv_mu/Mpc:.2f} Mpc (CMB-pinned). Burkert (cored-NFW) Q-profile.")

# ----------------------------------------------------------------- CLUSTER
print("\n"+"-"*84); print("CLUSTER  M500=1e15, R500~1.56 Mpc"); print("-"*84)
M500=1e15*Msun; R500=(3*M500/(4*np.pi*500*rho_crit0*Om* ( (1)**3) +0))**(1/3.)
R500=(3*M500/(4*np.pi*500*rho_crit0*(Om+OL)))**(1/3.)
fb=0.13; Mb=fb*M500
# total Q-mode mass available if CDM-like: (Odm/Ob)*Mb, clustered into the cluster
M_Q_tot=(Odm/Ob)*Mb
# Jeans core in the cluster: the floor 1/mu is the COSMIC-MEAN value; in the overdense
# cluster the Jeans/de-Broglie core shrinks ~rho^-1/4. At a ~200x mean cluster overdensity
# rc -> (1/mu)/200^0.25 ~ 0.27 Mpc. We report BOTH the cosmic-mean core (1 Mpc, conservative
# under-fill) and the density-shrunk core (0.27 Mpc, the physical cluster value).
rc_cl=inv_mu/(200.0**0.25)       # Jeans core shrunk in the cluster overdensity
# normalize Burkert so M_Q(<3 R500) = M_Q_tot (most of the field collected in the cluster)
Rnorm=3*R500
rho0_cl = M_Q_tot/burkert_Menc(Rnorm,1.0,rc_cl)
print(f"  Mb={Mb/Msun:.2e}  M_Q_tot (CDM-like, Odm/Ob*Mb)={M_Q_tot/Msun:.2e} Msun")
print(f"  Jeans core: cosmic-mean 1/mu={inv_mu/Mpc:.2f} Mpc -> shrunk in 200x overdensity to rc={rc_cl/Mpc:.2f} Mpc")
print(f"\n  {'r/R500':>7} {'r[Mpc]':>7} {'M_Q(<r)[Msun]':>13} {'g_bar':>10} {'g_mond':>10} {'g_with_Q':>10} {'eta_Q':>7}")
for frac in [0.1,0.3,0.5,1.0,1.3,2.0]:
    r=frac*R500
    MQ=burkert_Menc(r,rho0_cl,rc_cl)
    # baryon enclosed: assume beta-model-ish; approximate Mb(<r)=Mb*(r/R500)^1.2 capped
    Mb_r=Mb*min(1.0,(r/R500)**1.2)
    g_bar=G*Mb_r/r**2
    g_mond=nu_dS(g_bar)
    g_with=np.sqrt((g_bar+G*MQ/r**2)**2+(g_bar+G*MQ/r**2)*a0)  # Q adds to the baryon source
    # simpler/honest: total dynamical g = g_mond(from baryons) + Newtonian g from Q-mass
    g_tot = g_mond + G*MQ/r**2
    eta = g_tot/g_mond
    print(f"  {frac:>7.2f} {r/Mpc:>7.2f} {MQ/Msun:>13.2e} {g_bar:>10.2e} {g_mond:>10.2e} {g_tot:>10.2e} {eta:>7.2f}")
print("  => eta_Q(R500) is the Q-mode boost over MOND. Target eRASS1 ~2.0. Read the R500 row.")

# ----------------------------------------------------------------- GALAXY
print("\n"+"-"*84); print("GALAXY  L* spiral Mb=6e10, R_disk~20 kpc"); print("-"*84)
print("  *** NOTE: this section IMPOSES a 1 Mpc core in the galaxy too, giving eta_gal~1.")
print("      That core is NOT physical for a c_s^2->0 field (it clusters to a ~kpc cuspy halo).")
print("      The eta_gal~1.0000 below is therefore an ARTIFACT, NOT a real galaxy-veto pass.")
print("      The honest galaxy veto is the direct CDM-halo injection: +0.12 to +0.23 dex. ***")
Mgal_b=6e10*Msun; Rdisk=20*kpc
# Q-mode in the galaxy: its >Mpc-scale halo, SAME Burkert core rc=1/mu, normalized to the
# galaxy's CDM-like halo mass (Odm/Ob)*Mgal_b collected over its ~Mpc environment.
M_Q_gal=(Odm/Ob)*Mgal_b
rho0_gal=M_Q_gal/burkert_Menc(2*Mpc,1.0,inv_mu)   # spread over ~2 Mpc environment
print(f"  Mb={Mgal_b/Msun:.2e}  M_Q_halo (CDM-like)={M_Q_gal/Msun:.2e} Msun  core rc={inv_mu/Mpc:.2f} Mpc")
print(f"\n  {'r[kpc]':>7} {'M_Q(<r)[Msun]':>13} {'M_b(<r)':>10} {'g_bar':>10} {'g_mond':>10} {'g+Q':>10} {'eta_Q':>7}")
for rk in [5,10,20,30,50]:
    r=rk*kpc
    MQ=burkert_Menc(r,rho0_gal,inv_mu)
    Mb_r=Mgal_b*(1-(1+r/(3*kpc))*np.exp(-r/(3*kpc)))  # exp disk
    g_bar=G*Mb_r/r**2; g_mond=nu_dS(g_bar)
    g_tot=g_mond+G*MQ/r**2; eta=g_tot/g_mond
    print(f"  {rk:>7} {MQ/Msun:>13.2e} {Mb_r/Msun:>10.2e} {g_bar:>10.2e} {g_mond:>10.2e} {g_tot:>10.2e} {eta:>7.4f}")
print("  => eta_Q in the disk = the Q-mode's RAR contamination. RAR-safe needs eta_Q-1 < few%.")

# ----------------------------------------------------------------- VERDICT
print("\n"+"="*84)
r=R500; MQ=burkert_Menc(r,rho0_cl,rc_cl); Mb_r=Mb
g_bar=G*Mb_r/r**2; g_mond=nu_dS(g_bar); eta_cl=(g_mond+G*MQ/r**2)/g_mond
r=30*kpc; MQg=burkert_Menc(r,rho0_gal,inv_mu)
Mb_r=Mgal_b*(1-(1+r/(3*kpc))*np.exp(-r/(3*kpc)))
g_bar=G*Mb_r/r**2; g_mond=nu_dS(g_bar); eta_gal=(g_mond+G*MQg/r**2)/g_mond
# also report the conservative cosmic-mean-core cluster eta
rho0_cl_1Mpc=M_Q_tot/burkert_Menc(Rnorm,1.0,inv_mu)
MQ_1Mpc=burkert_Menc(R500,rho0_cl_1Mpc,inv_mu)
g_bar=G*Mb/R500**2; g_mond=nu_dS(g_bar); eta_cl_1Mpc=(g_mond+G*MQ_1Mpc/R500**2)/g_mond
print(f"  CLUSTER eta_Q(R500) = {eta_cl:.2f}  (shrunk core rc={rc_cl/Mpc:.2f} Mpc) | {eta_cl_1Mpc:.2f} (cosmic-mean core 1 Mpc) | target ~2.0")
print(f"  GALAXY  eta_Q(30kpc)= {eta_gal:.4f}  (RAR-safe needs ~1.00-1.05)")
print(f"  galaxy/cluster boost ratio = {(eta_gal-1)/(eta_cl-1):.1e}  (the field discriminates by ~{(eta_cl-1)/(eta_gal-1):.0f}x)")
print(f"""
  READING (both ways, with the HARD CAVEAT): the cored Burkert Q-profile at the CDM-like
  abundance (Odm/Ob*Mb, NO mass tuning) delivers eta_Q(R500) = {eta_cl_1Mpc:.2f} (1 Mpc core)
  to {eta_cl:.2f} (shrunk 0.27 Mpc core) -- it ARITHMETICALLY supplies MOST of the eta~2
  residual. The disk eta_gal~1.0000 HERE IS AN ARTIFACT of the IMPOSED 1 Mpc core (this
  script assumed the Q-mode stays cored at 1/mu in the galaxy). That assumption is WRONG:
  the companion growth-threshold check (route1_qmode_clustering_profile.py Step 1) shows the
  c_s^2->0 Q-mode clusters at ALL scales above a negligible density threshold, so in a galaxy
  it forms a CUSPY CDM-like halo (core ~kpc, not Mpc), NOT a 1 Mpc pedestal. With a realistic
  ~kpc galaxy-halo core the disk eta is NOT ~1 -- the direct-injection veto gives +0.12 to
  +0.23 dex RAR scatter (sibling run), which BREAKS the 0.11-0.14 dex RAR. So the apparent
  ~{(eta_cl-1)/(eta_gal-1):.0f}x cluster/galaxy discrimination here is an ARTIFACT of imposing the Mpc core on
  the galaxy; the field does NOT actually self-select. WALLS (full weight): the abundance
  I0~Omega_dm is FREE; the cored-Burkert is an ANSATZ; and crucially there is NO physical
  mechanism that cores the field at Mpc in galaxies (the c_s^2->0 growth forbids it). NET:
  the dust ARITHMETICALLY covers the cluster core, but it does so by being CDM, which fails
  the galaxy RAR -- dark matter RELOCATED onto the gravity mode, NOT galaxy-safe-selected.
  The cluster tension is EXPLAINED (cold CDM-like dark sector), NOT closed galaxy-safely.""")
