#!/usr/bin/env python3
r"""
DOOR C5 -- Bullet Cluster per-halo ghost-condensate (I0) ledger, framework's OWN terms.

FRAMEWORK (Zimmerman de Sitter-Unruh MODIFIED INERTIA):
  a0 = c H_Lambda / Z = 9.36e-11 m/s^2 (canonical, rho_DE footing). Z=sqrt(32pi/3).
  ALT footing a0 = 1.13e-10 (rho_total). Own interpolation:
     g_obs = sqrt(g_bar^2 + g_bar*a0)   (simple form),  nu(y)=sqrt(1+1/y).
  DARK SECTOR = a ghost condensate. Its amount I0 ~ Omega_dm is MEASURED-not-derived.
  A cluster mass "deficit" is read as a per-halo I0 measurement, NOT a kill --
  UNLESS I0 is wildly non-universal across halos/environments.

WHAT C5 TESTS:
  The classic MOND cluster problem: even in MOND, clusters need a residual unseen
  (dark) mass ~2x baryons in the core. In THIS framework that residual is the ghost
  condensate I0. The KILL condition is NOT "residual exists" (that's allowed and even
  expected). The KILL is: the IMPLIED I0/baryon (or I0/M_lens) is WILDLY inconsistent
  ACROSS the three Bullet halos and vs the C2 WINGS ledger -> condensate amount is
  environment-dependent in an uncontrolled way = a genuine two-sector inconsistency.

DATA (all masses 2D-projected, units 1e14 Msun, within projected aperture radius):
  * GR (Newtonian/LCDM) strong-lensing masses  -- Zhang+2026 arXiv:2606.19454 Table I,
    built on Cha+2025 (C25) = arXiv:2503.21870 GR lensing.
  * Baryonic budget (gas + stars + ICL) canonical IMF  -- Zhang+2026 Tables II,III,IV.
  * MOND strong-lensing mass (Mlens,MOND) -- Zhang+2026 Tables II,III,IV
    (this is the mass MOND-style modified gravity REQUIRES from the enclosed baryons via
     the deep-MOND lensing relation; a MODIFIED-INERTIA framework with the SAME a0 and the
     SAME simple interpolation predicts the SAME enclosed-mass -> radial-accel relation for
     a static lens, so we use Mlens,MOND as the framework's predicted enclosed mass).
  * Virial masses (context) -- Kim/An+ 2026 arXiv:2512.03150: main M200c=15.11e14, sub 1.49e14.

  The three cores: southern BCG + northern cD/BCG (both in the MAIN clump) + subclump BCG.
  All quoted with 1-sigma errors. Mgas is X-ray-derived; stars via JWST photometry.
"""
import numpy as np

# ---- constants / footing ----
c = 2.99792458e8
A0_CANON = 9.36e-11     # rho_DE / cH_Lambda footing
A0_ALT   = 1.13e-10     # rho_total / cH0 footing

# ---- DATA: Zhang+2026 (2606.19454), units 1e14 Msun, projected within r_p ----
# aperture radii (kpc)
rp = np.array([80.,100.,150.,250.])

# Table I: GR (Newtonian/LCDM) strong-lensing enclosed mass
M_GR = {
 'south': np.array([0.338,0.475,0.842,1.670]),
 'north': np.array([0.338,0.486,0.898,1.590]),
 'sub'  : np.array([0.311,0.409,0.579,0.870]),
}
M_GR_err = {
 'south': np.array([0.018,0.035,0.086,0.140]),
 'north': np.array([0.012,0.024,0.070,0.140]),
 'sub'  : np.array([0.014,0.025,0.067,0.130]),
}

# Baryonic mass, canonical IMF (gas + galaxies + ICL + faint): Mbar,IMF
M_bar = {
 'south': np.array([0.094,0.127,0.297,0.731]),
 'north': np.array([0.091,0.140,0.297,0.774]),
 'sub'  : np.array([0.052,0.075,0.153,0.399]),
}
M_bar_err = {
 'south': np.array([0.026,0.036,0.089,0.228]),
 'north': np.array([0.027,0.041,0.091,0.238]),
 'sub'  : np.array([0.012,0.019,0.044,0.122]),
}

# gas-only (X-ray), for reference
M_gas = {
 'south': np.array([0.079,0.110,0.270,0.690]),
 'north': np.array([0.080,0.125,0.276,0.721]),
 'sub'  : np.array([0.038,0.059,0.133,0.370]),
}

# MOND strong-lensing enclosed mass (Zhang+ Tables) = framework's static-lens prediction
M_MOND = {
 'south': np.array([0.210,0.288,0.479,0.862]),
 'north': np.array([0.212,0.301,0.541,0.823]),
 'sub'  : np.array([0.203,0.256,0.281,0.400]),
}
M_MOND_err = {
 'south': np.array([0.017,0.033,0.086,0.089]),
 'north': np.array([0.012,0.023,0.070,0.070]),
 'sub'  : np.array([0.014,0.025,0.027,0.030]),
}

cores = ['south','north','sub']
labels = {'south':'Southern BCG (main)','north':'Northern cD (main)','sub':'Subclump BCG (bullet)'}

print("="*82)
print("DOOR C5: Bullet Cluster per-halo ghost-condensate (I0) ledger -- framework's terms")
print("="*82)
print("Data: Zhang+2026 arXiv:2606.19454 (Tables I-IV) on Cha+2025 arXiv:2503.21870 lensing.")
print("All masses 1e14 Msun, 2D-projected within r_p. Three BCG cores.\n")

# --------------------------------------------------------------------------
# STEP 1: The ghost-condensate ledger read TWO ways.
#
# READING A (framework as MODIFIED INERTIA, no literal dark mass):
#   The lensing mass the framework PREDICTS from baryons is M_MOND (same a0, same simple nu,
#   static source -> the MOND lensing relation). The "required extra mass" a NEWTONIAN observer
#   infers is (M_MOND - M_bar). In MI there is NO literal I0; the whole excess is inertial.
#   The consistency test then is: does the enclosed BARYON budget, run through the framework's
#   fixed a0, reproduce the enclosed LENSING mass (M_GR) at every core? i.e. M_MOND ?= M_GR.
#
# READING B (framework as GHOST CONDENSATE / two-sector, literal I0):
#   Dark sector is a real ghost-condensate mass I0. Then the required condensate to match the
#   Newtonian lensing mass is  I0 = M_GR - M_bar  (a literal mass deficit).
#   The per-halo condensate fraction  f_I0 = I0 / M_bar  (or I0/M_GR) must be roughly universal
#   across the three cores AND vs WINGS, else the "amount" is uncontrolled.
# --------------------------------------------------------------------------

print("-"*82)
print("READING A -- pure MODIFIED INERTIA: does baryons@a0 (=M_MOND) reproduce M_GR lensing?")
print("  ratio R = M_MOND / M_GR at each aperture (want ~1 if MI closes the deficit alone)")
print("-"*82)
print(f"{'core':22s} " + " ".join(f"{int(r):>6d}kpc" for r in rp))
for ck in cores:
    R = M_MOND[ck]/M_GR[ck]
    print(f"{labels[ck]:22s} " + " ".join(f"{v:9.2f}" for v in R))
# how far short is MI-alone at 250 kpc?
print("\n  -> M_MOND falls WELL SHORT of M_GR (the classic residual cluster deficit).")
print("     MI with the framework a0 does NOT close the core lensing deficit by itself.")
print("     (This is the known MOND-in-clusters residual; framework reads it as I0.)\n")

print("-"*82)
print("READING B -- literal ghost condensate I0 = M_GR - M_bar (Newtonian deficit).")
print("  Report f_I0 = I0/M_bar and I0/M_GR per core; test cross-core universality.")
print("-"*82)
for aptidx,ap in enumerate(rp):
    print(f"\n  aperture r_p = {int(ap)} kpc:")
    print(f"    {'core':22s} {'M_bar':>7s} {'M_GR':>7s} {'I0':>7s} {'I0/M_bar':>9s} {'I0/M_GR':>8s}")
    vals_fbar=[]; vals_fGR=[]
    for ck in cores:
        Mb=M_bar[ck][aptidx]; Mg=M_GR[ck][aptidx]
        I0=Mg-Mb
        fbar=I0/Mb; fGR=I0/Mg
        vals_fbar.append(fbar); vals_fGR.append(fGR)
        print(f"    {labels[ck]:22s} {Mb:7.3f} {Mg:7.3f} {I0:7.3f} {fbar:9.2f} {fGR:8.2f}")
    vals_fbar=np.array(vals_fbar); vals_fGR=np.array(vals_fGR)
    print(f"    cross-core I0/M_bar: mean={vals_fbar.mean():.2f}  spread(min..max)={vals_fbar.min():.2f}..{vals_fbar.max():.2f}  (max/min={vals_fbar.max()/vals_fbar.min():.2f})")
    print(f"    cross-core I0/M_GR : mean={vals_fGR.mean():.2f}  spread(min..max)={vals_fGR.min():.2f}..{vals_fGR.max():.2f}")

# --------------------------------------------------------------------------
# STEP 2: The DECISIVE cross-core universality test at the anchoring 250 kpc aperture,
#   with error propagation. The KILL is a per-halo I0 spread >> measurement error AND
#   >> the WINGS spread. Use the condensate/baryon ratio, error-propagated.
# --------------------------------------------------------------------------
print("\n"+"="*82)
print("STEP 2: DECISIVE cross-core universality of I0/M_bar at 250 kpc (with errors)")
print("="*82)
apt=3  # 250 kpc
fbar=[]; efbar=[]
for ck in cores:
    Mb=M_bar[ck][apt]; sMb=M_bar_err[ck][apt]
    Mg=M_GR[ck][apt];  sMg=M_GR_err[ck][apt]
    I0=Mg-Mb; sI0=np.hypot(sMg,sMb)
    f=I0/Mb
    sf=abs(f)*np.hypot(sI0/I0, sMb/Mb)
    fbar.append(f); efbar.append(sf)
    print(f"  {labels[ck]:22s} I0={I0:.3f}+/-{sI0:.3f}   I0/M_bar={f:.2f}+/-{sf:.2f}")
fbar=np.array(fbar); efbar=np.array(efbar)
# chi2 against a common value (weighted mean)
w=1/efbar**2
mu=np.sum(w*fbar)/np.sum(w)
chi2=np.sum((fbar-mu)**2/efbar**2)
dof=len(fbar)-1
print(f"\n  weighted-mean I0/M_bar = {mu:.2f}")
print(f"  chi2 vs common value = {chi2:.2f} for dof={dof}  (p~{ 1-__import__('math').erf(np.sqrt(chi2/2)/np.sqrt(2)) if False else '' })")
from scipy import stats
p=1-stats.chi2.cdf(chi2,dof)
print(f"  chi2 = {chi2:.2f}, dof={dof}, p={p:.3f}  ->  {'CONSISTENT (universal)' if p>0.05 else 'INCONSISTENT'} at 5%")

# same on I0/M_GR (deficit fraction, the WINGS-comparable quantity)
print("\n  same test on the DEFICIT FRACTION I0/M_GR (= 1 - M_bar/M_GR), WINGS-comparable:")
fGR=[]; efGR=[]
for ck in cores:
    Mb=M_bar[ck][apt]; sMb=M_bar_err[ck][apt]
    Mg=M_GR[ck][apt];  sMg=M_GR_err[ck][apt]
    f=1-Mb/Mg
    sf=(Mb/Mg)*np.hypot(sMb/Mb,sMg/Mg)
    fGR.append(f); efGR.append(sf)
    print(f"    {labels[ck]:22s} I0/M_GR = {f:.3f}+/-{sf:.3f}  (baryon fraction {Mb/Mg:.3f})")
fGR=np.array(fGR); efGR=np.array(efGR)
w2=1/efGR**2; mu2=np.sum(w2*fGR)/np.sum(w2)
chi22=np.sum((fGR-mu2)**2/efGR**2); p2=1-stats.chi2.cdf(chi22,dof)
print(f"    weighted-mean deficit fraction = {mu2:.3f};  chi2={chi22:.2f} dof={dof} p={p2:.3f} -> {'CONSISTENT' if p2>0.05 else 'INCONSISTENT'}")

# --------------------------------------------------------------------------
# STEP 3: Compare the Bullet per-halo condensate fraction to the C2 WINGS cluster ledger
#   and to the generic MOND-cluster residual (~factor 2 in cores). The framework's own
#   position: I0~Omega_dm; cluster cores generically need M_dyn/M_bar ~ 2 EVEN in MOND.
# --------------------------------------------------------------------------
print("\n"+"="*82)
print("STEP 3: Bullet cores vs the generic MOND-cluster residual and C2/WINGS")
print("="*82)
# global (all baryons, 250 kpc, main+sub summed) dynamical/baryon ratio, GR
for tag,Mset in [('GR lensing',M_GR),('MOND lensing',M_MOND)]:
    tot_dyn=sum(Mset[ck][apt] for ck in cores)
    tot_bar=sum(M_bar[ck][apt] for ck in cores)
    print(f"  summed 3 cores @250kpc:  M_{tag}/M_bar = {tot_dyn/tot_bar:.2f}")
print("  Literature: MOND clusters need residual M_dyn/M_bar ~ 1.8-2.5 in cores (Sanders 2003;")
print("  Angus+2008) -- the SAME residual the framework books as I0. C2/WINGS eta(R500)~1.0-1.3.")
print("  Bullet cores here sit at I0/M_bar ~ 1-2 (GR) -- SAME ballpark, not an outlier.")

# --------------------------------------------------------------------------
# STEP 4: The a0-footing fork -- does the verdict depend on a0(0)?
#   The lensing masses (M_GR, M_MOND) and baryons are DATA; a0 enters only in whether MI
#   closes the deficit (Reading A). Neither footing closes the ~2x core deficit, so the
#   verdict (residual exists, and its cross-core universality) is a0-INDEPENDENT.
# --------------------------------------------------------------------------
print("\n"+"="*82)
print("STEP 4: a0-footing fork (canonical 9.36e-11 vs alt 1.13e-10)")
print("="*82)
print("  M_GR, M_bar, M_MOND are DATA (a0-free). a0 only sets whether MI-alone closes the")
print("  deficit; alt footing is ~21% higher a0 -> M_MOND up by ~sqrt(1.13/0.936)~1.10 in deep-MOND,")
print("  still << the factor ~2 core deficit. Verdict (residual I0 needed; cross-core universality)")
print("  is UNCHANGED under either footing.")
# quantify the deep-MOND lensing-mass scaling factor
scale = np.sqrt(A0_ALT/A0_CANON)
print(f"  deep-MOND M_dyn scales ~sqrt(a0): alt/canon = sqrt({A0_ALT:.3g}/{A0_CANON:.3g}) = {scale:.3f}")

print("\n"+"="*82)
print("VERDICT INPUTS:")
print(f"  - I0/M_bar @250kpc per core: {[f'{v:.2f}' for v in fbar]} -> chi2={chi2:.2f}/{dof}, p={p:.3f}")
print(f"  - deficit fraction I0/M_GR : {[f'{v:.2f}' for v in fGR]} -> chi2={chi22:.2f}/{dof}, p={p2:.3f}")
print(f"  - per-core I0/M_bar spread max/min = {fbar.max()/fbar.min():.2f}")
print("="*82)
