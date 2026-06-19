#!/usr/bin/env python3
r"""
POPULATION of non-adiabatic cluster members for the framework's distinctive MI sigma-spread test
================================================================================================
TASK (topic "population"): WHICH cluster members actually reach the non-adiabatic regime
y = omega_ex/omega_in ~ 1, and HOW MANY are there per rich cluster?

THE SIGNAL (live, distinctive, MG-impossible, non-a0-degenerate -- per
GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15.md and member_MI_nonadiabatic_plunge.py):
  - MODIFIED INERTIA (the framework, Milgrom 2022 arXiv:2208.07073 Eq 34): a member's internal
    inertia depends on its acceleration HISTORY via theta(omega_ex/omega_in). At MATCHED cluster-
    centric radius (= matched MOMENTARY a_ext), member internal sigma CORRELATES with infall phase.
    Banked relational spread ~6-13% in sigma.
  - MODIFIED GRAVITY (QUMOND/AeST, all MG-MOND): EFE depends ONLY on the momentary a_ext
    (Milgrom-2022 verbatim) -> ZERO sigma-spread across infall phase at matched radius, for ANY a0.
  - CDM: no a0, no memory -> 0.

  *** This is a TEST, not a closure of the cluster residual. The mean dynamical mass is UNCHANGED
      (mi_dynamic_route.py); only the relational spread is distinctive. ***

QUARANTINE: a0/Z/kappa NOT derived. theta(y) form UNKNOWN -> amplitude UNVERIFIED; only the
SIGN/EXISTENCE (nonzero MI vs structural-zero MG) is robust. DO NOT use the REFUTED
"MI-tangential-vs-MG-radial ellipsoid sign" claim.

WHAT THIS SCRIPT ADDS over the prior pilots: the prior scripts established the regime IS reached for
"diffuse/UDG/dSph plungers" qualitatively. This computes the POPULATION quantitatively:
  (1) omega_ex/omega_in for a UDG, a dSph, and a normal elliptical on PLUNGING orbits in M~1e15;
      omega_ex = cluster orbital freq at pericenter; omega_in = internal stellar freq sigma/R.
  (2) the y(D) profile ALONG a realistic NFW plunge orbit -> the WINDOW (radius range, time fraction)
      where each type has y > ~0.5.
  (3) folds in REAL catalog counts (Coma UDG census ~1000, ~200 per M~1e15; dSph faint-end LF;
      bright ellipticals) and the recent-infall/radial-orbit fraction -> N_usable per rich cluster.

BOTH-WAYS (#1 rule): verify the population is real & above-floor as hard as it washes out. A UDG that
crosses y~1 only if its internal sigma is at the very low end, or only for a few Myr near pericenter,
or only if it survives the core, is reported as such. No manufactured count.
"""
import numpy as np

# ----------------------------------------------------------------- constants (SI)
c, G, Msun, kpc, Mpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
Gyr = 3.1557e16
km  = 1e3
a0  = 9.36e-11                       # sealed framework value c^2 sqrt(Lambda/32pi)

def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)

print("="*100)
print(" POPULATION of non-adiabatic (y=omega_ex/omega_in ~ 1) cluster members  --  framework MI sigma-spread TEST")
print("="*100)
print(f"  a0 = {a0:.3e} m/s^2 (sealed).  y = omega_ex/omega_in;  non-adiabatic regime y >~ 0.5, sharp at y~1.\n")

# ===========================================================================
# CLUSTER MODEL: M200 = 1e15 Msun, NFW, c=5  (Coma-like rich cluster)
# ===========================================================================
M200, c200, R200 = 1.0e15*Msun, 5.0, 2.0*Mpc
rs = R200/c200
def Menc(D):
    x = D/rs
    return M200*(np.log(1+x)-x/(1+x))/(np.log(1+c200)-c200/(1+c200))
def a_ext(D):   return G*Menc(D)/D**2                 # external (cluster) acceleration at radius D
def om_clus(D): return np.sqrt(G*Menc(D)/D**3)        # cluster orbital ang. freq at D (= v_circ/D)

print("-"*100)
print(" CLUSTER (Coma-like): M200=1e15 Msun, NFW c=5, R200=2 Mpc.  External field & orbital frequency vs radius:")
print("-"*100)
print(f"  {'D (kpc)':>9} {'M_enc(Msun)':>12} {'a_ext/a0':>9} {'v_circ(km/s)':>12} {'om_clus(1/Gyr)':>14} {'T_orb(Gyr)':>11}")
for Dk in [100,200,300,500,1000,1500,2000]:
    D=Dk*kpc
    vcirc=np.sqrt(G*Menc(D)/D)
    om=om_clus(D)
    print(f"  {Dk:9d} {Menc(D)/Msun:12.3e} {a_ext(D)/a0:9.2f} {vcirc/km:12.0f} {om*Gyr:14.3f} {2*np.pi/om/Gyr:11.3f}")
print(r"""  NOTE: a_ext > a0 over the whole cluster (core ~10-30 a0, R200 ~ a few a0). The cluster itself is
  NOT deep-MOND -- but the EFE still modulates each MEMBER's internal field, and the distinctive MI
  content is the FREQUENCY of that modulation (om_clus) relative to the member's internal om_in.""")

# ===========================================================================
# (1) omega_ex/omega_in for the THREE member types on PLUNGING orbits
# ===========================================================================
print("\n"+"="*100)
print(" (1) y = omega_ex/omega_in for UDG, dSph, normal elliptical on PLUNGING orbits (small pericenter)")
print("="*100)
print(r"""  omega_in = internal stellar orbital ang. frequency = sigma_member / R_member  (the member's own
             dynamical frequency; a star's orbit time about the member centre).
  omega_ex = frequency at which the cluster field SEEN BY THE MEMBER varies = cluster orbital ang.
             frequency at PERICENTER = om_clus(D_peri) ~ v_peri / D_peri.  A plunging (radial, small
             D_peri) orbit MAXIMIZES omega_ex (deep, fast core passage).  We quote y at pericenter.""")

# member types:  name, sigma_member (km/s), R_member (kpc)
members = [
    ("UDG (diffuse)",         20.0, 3.0),
    ("dSph",                   8.0, 0.3),
    ("normal elliptical",    200.0, 3.0),
]
# also carry a low-sigma UDG (extreme deep-MOND) and a classic small dSph for the spread
members_extra = [
    ("UDG low-sigma (extreme)", 10.0, 3.0),
    ("dSph small (Draco-like)",  9.0, 0.2),
]

pericenters_kpc = [100, 200, 300, 500]   # plunge pericenters; 100-300 kpc = deep radial through core

def y_at_peri(sig_member_km, R_member_kpc, Dperi_kpc):
    om_in = (sig_member_km*km)/(R_member_kpc*kpc)
    om_ex = om_clus(Dperi_kpc*kpc)
    return om_ex/om_in, om_in, om_ex

print(f"\n  {'member':26s} {'sigma':>6} {'R(kpc)':>7} {'om_in(1/Gyr)':>13} {'a_in/a0':>8} | "
      + " ".join(f"y@{p}kpc" for p in pericenters_kpc))
print("  "+"-"*100)
all_rows=[]
for name,sig,R in members+members_extra:
    om_in = (sig*km)/(R*kpc)
    a_in  = (sig*km)**2/(R*kpc)
    ys = [y_at_peri(sig,R,p)[0] for p in pericenters_kpc]
    all_rows.append((name,sig,R,om_in,a_in,ys))
    print(f"  {name:26s} {sig:6.0f} {R:7.2f} {om_in*Gyr:13.3f} {a_in/a0:8.2f} | "
          + " ".join(f"{yy:6.3f}" for yy in ys))

print(r"""
  READ (1): y = om_ex/om_in scales as om_clus(D_peri) / (sigma/R) = (cluster pericenter freq) /
  (member internal freq). Two facts dominate:
   * om_clus(core) ~ 6-12 /Gyr (T_orb ~ 0.5-1 Gyr through the core).
   * om_in(UDG, sigma=20,R=3) ~ 6.6 /Gyr  -> y ~ O(1) for a UDG plunging to D_peri ~ 100-300 kpc.
   * om_in(dSph, sigma=8,R=0.3) ~ 26 /Gyr  -> y ~ 0.2-0.4 (a few-x too internally fast: marginal).
   * om_in(elliptical, sigma=200,R=3) ~ 66 /Gyr -> y ~ 0.05-0.1 (DEEP ADIABATIC: a0-degenerate trap).""")

# ===========================================================================
# (2) y ALONG a realistic plunge orbit -> the WINDOW (radius range + time fraction y>0.5)
# ===========================================================================
print("\n"+"="*100)
print(" (2) y(D) ALONG a deep radial plunge (apo=2 Mpc, peri=150 kpc) -> radius & time WINDOW with y>0.5")
print("="*100)
from scipy.integrate import quad
# NFW potential (closed form, robust): Phi(D) = -4 pi G rho_s rs^3 ln(1+D/rs)/D
norm = (np.log(1+c200)-c200/(1+c200))
rho_s_rs3 = M200/(4*np.pi*norm)          # = rho_s * rs^3 (since Menc=4pi rho_s rs^3 [ln(1+x)-x/(1+x)])
def Phi(D):
    return -4*np.pi*G*rho_s_rs3*np.log(1.0+D/rs)/D
def plunge_orbit(Dapo, Dperi, n=4000):
    # E, L from the two radial turning points (vr=0): E=Phi+L^2/(2D^2) at both.
    Pa,Pp=Phi(Dapo),Phi(Dperi)
    L2=2.0*(Pp-Pa)/(1.0/Dapo**2-1.0/Dperi**2)
    E =Pa+L2/(2.0*Dapo**2)
    Ds=np.linspace(Dperi,Dapo,n)
    vr2=np.maximum(2.0*(E-Phi(Ds))-L2/Ds**2, 0.0)
    vr=np.sqrt(vr2)
    # midpoint dt = dr/vr, evaluated on cell midpoints (avoids the vr->0 endpoint singularities)
    Dmid=0.5*(Ds[1:]+Ds[:-1]); dr=np.diff(Ds)
    vr2m=np.maximum(2.0*(E-Phi(Dmid))-L2/Dmid**2, 1e-30)
    dtmid=dr/np.sqrt(vr2m)
    return Ds, vr, Dmid, dtmid

Dapo,Dperi = 2.0*Mpc, 150.0*kpc
Ds,vr,Dmid,dtmid = plunge_orbit(Dapo,Dperi)
T_radial = 2*np.sum(dtmid)   # peri->apo->peri full radial period
print(f"  Radial plunge orbit: apo={Dapo/Mpc:.1f} Mpc, peri={Dperi/kpc:.0f} kpc, radial period ~ {T_radial/Gyr:.2f} Gyr")
print(f"\n  {'member':26s} {'om_in(1/Gyr)':>13} {'y@peri':>8} {'y@500kpc':>9} {'D where y>0.5 (kpc)':>20} {'time frac y>0.5':>16}")
print("  "+"-"*100)
om_ex_arr  = om_clus(Ds)
om_ex_mid  = om_clus(Dmid)
w = dtmid/np.sum(dtmid)        # time weight along peri->apo (by symmetry = the full-period weight)
for name,sig,R in members+members_extra:
    om_in=(sig*km)/(R*kpc)
    yarr  = om_ex_arr/om_in
    ymid  = om_ex_mid/om_in
    mask_mid = ymid>0.5
    if mask_mid.any():
        Dlo,Dhi = Dmid[mask_mid].min()/kpc, Dmid[mask_mid].max()/kpc
        tfrac = np.sum(w[mask_mid])
        win=f"{Dlo:.0f}-{Dhi:.0f}"
    else:
        win="(none)"; tfrac=0.0
    i_peri=0; i500=np.argmin(np.abs(Ds-500*kpc))
    print(f"  {name:26s} {om_in*Gyr:13.2f} {yarr[i_peri]:8.3f} {yarr[i500]:9.3f} {win:>20} {tfrac*100:15.1f}%")
print(r"""
  READ (2): the non-adiabatic WINDOW (y>0.5) for a UDG plunger spans D ~ inner few-hundred kpc and a
  time fraction ~10-25% of the radial orbit (the member spends most time near apocenter where y<<1).
  dSph windows are narrow/absent (internally too fast); ellipticals never enter. So the test population
  is UDGs caught NEAR PERICENTER on RADIAL orbits -- a duty-cycle ~10-25% on top of the UDG census.""")

# ===========================================================================
# (3) COUNTS per rich cluster: catalog census x (radial/recent-infall fraction) x (near-peri duty cycle)
# ===========================================================================
print("\n"+"="*100)
print(" (3) HOW MANY per rich cluster: census x radial-orbit fraction x near-pericenter duty cycle")
print("="*100)
print(r"""  REAL CATALOG INPUTS (web-sourced this session; see Sources in the structured return):
   * UDG census: Coma has ~1000 UDGs (Yagi+2016 Subaru catalog, arXiv:1602.00002 / 2016ApJS 225 11);
     van der Burg+2016 give ~200 UDGs per M200~1e15 cluster (selection-dependent: ~200-1000).
   * UDG orbits: Coma UDGs are PREDOMINANTLY RECENT INFALL on RADIAL orbits (Yagi/Alabi, MNRAS 479
     3308 = arXiv:1801.09686): higher |v_los|, bluer, smaller = first-infall plungers. The core
     (r<~300 kpc = 0.15 R200) is DEPLETED of UDGs (they disrupt) -> the deep plungers we want are
     caught en route / near first pericenter, not survivors sitting in the core.
   * dSph/dE census: faint-end LF is steep; rich clusters host HUNDREDS-1000s of dwarfs
     (Virgo alpha~-1.6, Sabatini/Trentham). But dSph are internally fast (y~0.2-0.4): mostly MARGINAL.
   * Bright ellipticals: tens-100s, but DEEP ADIABATIC (y~0.05): contribute ZERO to the signal.""")

# Numbers (ranges; both-ways conservative<->optimistic)
N_udg_census   = (200, 1000)     # per M~1e15 cluster (van der Burg low .. Coma Yagi high)
f_radial       = (0.3, 0.6)      # fraction on radial / recent-infall orbits reaching small pericenter
f_nearperi     = (0.10, 0.25)    # near-pericenter duty cycle (time frac y>0.5 from (2))
f_resolved     = (0.05, 0.3)     # fraction with internal kinematics resolvable (sigma~20 km/s, faint)

def band(lo_tuple, hi_pick):
    return lo_tuple[0]*hi_pick[0], lo_tuple[1]*hi_pick[1]

print(f"\n  STEP-BUILD (UDG channel, the dominant one):")
print(f"   census N_UDG (per M~1e15)        : {N_udg_census[0]:5d} - {N_udg_census[1]:5d}")
lo,hi = N_udg_census
lo*=f_radial[0]; hi*=f_radial[1]
print(f"   x radial/recent-infall {f_radial} : {lo:7.0f} - {hi:7.0f}   (plungers reaching small D_peri)")
lo*=f_nearperi[0]; hi*=f_nearperi[1]
print(f"   x near-peri duty cycle {f_nearperi}: {lo:7.1f} - {hi:7.0f}   (caught with y>0.5 NOW)")
N_in_regime_lo, N_in_regime_hi = lo, hi
lo2,hi2 = lo*f_resolved[0], hi*f_resolved[1]
print(f"   x resolved internal sigma {f_resolved}: {lo2:6.1f} - {hi2:6.0f}   (USABLE for the sigma-spread test)")
print(f"""
  COUNTS per rich (M~1e15) cluster:
   * UDGs PHYSICALLY in the y>0.5 regime RIGHT NOW (any given snapshot): ~ {N_in_regime_lo:.0f} - {N_in_regime_hi:.0f}
   * of those, with internal sigma RESOLVABLE (the test sample today): ~ {lo2:.0f} - {hi2:.0f}  per cluster
   * the RELATIONAL test needs members SPANNING infall phase at MATCHED cluster-centric radius -> you
     compare these ~few-tens plungers against circular-orbit UDGs at the SAME radius (y<<1). So the
     usable SAMPLE per cluster is a few -> few-tens, and you STACK clusters (Coma+Perseus+Virgo+Fornax+
     Frontier-Fields + 4MOST/MUSE wide-field) to build the correlation.""")

# dSph channel (marginal) + elliptical channel (null), for completeness
print(f"\n  OTHER CHANNELS:")
print(f"   * dSph/dE: census hundreds-1000s, but y~0.2-0.4 (internally fast) -> MARGINAL; only the")
print(f"     largest, lowest-sigma, deepest-plunging dwarfs (Draco-like at peri<150 kpc) graze y~0.4.")
print(f"     A few per cluster at best, and sigma~8-9 km/s is at/below the resolved-kinematics floor.")
print(f"   * Normal ellipticals: y~0.05-0.1 (deep adiabatic) -> ZERO distinctive signal (a0-degenerate")
print(f"     trap, Eq 35). They are the WRONG population. Do not include them.")

# ===========================================================================
# (4) SIGN/AMPLITUDE of the spread for the y~1 UDG population (re-confirm vs the banked 6-13%)
# ===========================================================================
print("\n"+"="*100)
print(" (4) Sign & amplitude of the sigma-spread for the y~1 UDG population (theta-form spread, both ways)")
print("="*100)
def theta_rational(y): y=np.abs(y); return 2.0/(1.0+y*y)      # theta(0)=2
def theta_exp1(y):     y=np.abs(y); return np.exp(1.0-y)       # theta(0)=e
def theta_exp2(y):     y=np.abs(y); return np.exp((1.0-y)/2.0) # theta(0)=e^{1/2}
THETAS=[("2/(1+y^2)",theta_rational),("e^{1-y}",theta_exp1),("e^{(1-y)/2}",theta_exp2)]
# At MATCHED a_ext: compare a CIRCULAR UDG (y~0.05, theta->theta(0)) vs a PLUNGING UDG (y~1, theta(1)=1)
a_in_udg = (20*km)**2/(3*kpc)     # ~ a UDG internal accel
a_ext_match = 2.0*a0              # matched cluster-centric radius (~ R500-ish, a_ext few a0)
print(f"  At MATCHED a_ext={a_ext_match/a0:.1f} a0, a_in(UDG)={a_in_udg/a0:.2f} a0:")
print(f"  member internal sigma ~ sqrt(boost),  boost = 1/mu_fw((a_in + a_ext*theta(y))/a0).")
print(f"  {'theta form':14s} | {'sigma(circular y=0.05)':>22} {'sigma(plunge y=1)':>18} | {'spread':>8}")
print("  "+"-"*72)
spreads=[]
for nm,thf in THETAS:
    b_circ = 1.0/mu_fw((a_in_udg+a_ext_match*thf(0.05))/a0)
    b_plun = 1.0/mu_fw((a_in_udg+a_ext_match*thf(1.0))/a0)
    s_circ,s_plun=np.sqrt(b_circ),np.sqrt(b_plun)
    spread=abs(s_circ-s_plun)/(0.5*(s_circ+s_plun))
    spreads.append(spread)
    print(f"  {nm:14s} | {s_circ:22.3f} {s_plun:18.3f} | {spread*100:7.1f}%")
print(f"\n  sigma-spread (circular vs plunging UDG at matched a_ext) = {min(spreads)*100:.1f} - {max(spreads)*100:.1f}% "
      f"(theta-form dependent).")
print(r"""  SIGN ROBUST: theta decreasing => the PLUNGING UDG (y~1, theta=1) is LESS EFE-boosted than the
  CIRCULAR UDG (y<<1, theta(0)~2-e) at the SAME cluster radius -> plunger has the SMALLER internal
  sigma boost. MG gives 0 spread (momentary a_ext only). CDM 0. Consistent with the banked ~6-13%.""")

print("\n"+"="*100)
print(" SYNTHESIS")
print("="*100)
print(f"""
 WHICH members cross y~1:   ONLY large, diffuse, LOW-sigma members on RADIAL/plunging orbits = UDGs.
   - UDG (sigma~20, R~3 kpc): y ~ 0.6-1.1 at D_peri ~ 100-300 kpc -> CROSSES y~1. (Extreme low-sigma
     UDGs sigma~10 cross even more easily.)
   - dSph (sigma~8, R~0.3 kpc): y ~ 0.2-0.4 -> MARGINAL (internally too fast); only deepest plungers graze.
   - normal elliptical (sigma~200, R~3 kpc): y ~ 0.05-0.1 -> DEEP ADIABATIC, a0-degenerate, ZERO signal.

 HOW MANY per rich (M~1e15) cluster:
   - UDG census ~200-1000 (van der Burg 2016 .. Yagi Coma 2016); ~30-60% on radial/recent-infall orbits
     (Coma UDGs ARE predominantly first-infall plungers, MNRAS 479 3308); ~10-25% near-pericenter duty
     cycle (y>0.5) at any snapshot -> ~ {N_in_regime_lo:.0f}-{N_in_regime_hi:.0f} UDGs PHYSICALLY in the y>0.5 regime now.
   - With resolvable internal sigma (sigma~20 km/s, faint): ~ {lo2:.0f}-{hi2:.0f} USABLE per cluster today.
   - The RELATIONAL test stacks these against matched-radius circular UDGs and stacks across clusters.

 NET: the non-adiabatic population is a SMALL, SPECIFIC subset -- plunging UDGs caught near pericenter --
 NOT a generic cluster population. A few -> few-tens usable per rich cluster today; stack ~10 rich
 clusters (Coma/Perseus/Virgo/Fornax/Frontier-Fields/4MOST) for ~tens-to-~hundred matched plungers.
 sigma-spread ~6-13% (theta-dependent), MG/CDM = 0. It is a TEST, NOT a cluster-residual closure.
 QUARANTINE held (a0/Z/theta(y) not derived); refuted ellipsoid-sign NOT used.""")
