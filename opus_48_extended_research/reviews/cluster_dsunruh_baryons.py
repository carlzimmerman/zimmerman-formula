#!/usr/bin/env python3
r"""
ROUTE cluster_dsunruh_baryons -- FIRST PRINCIPLES
=================================================
DERIVE whether the framework's OWN de Sitter-Unruh interpolation
   mu(a) = [sqrt(a^2 + (cH)^2) - cH]/a   <=>   g_obs = sqrt(g_bar^2 + g_bar*a0)
changes the cluster deficit relative to standard MOND nu functions, and how much of the
canonical ~2x cluster missing-mass is an honest baryon-accounting effect.

The dS-Unruh form is the "simple" nu family:  nu(y) = sqrt(1 + 1/y),  y = g_bar/a0.
Compare head-to-head against:
   - standard "simple"  mu = x/(1+x)  ->  nu = 1/2 (1 + sqrt(1+4/y))
   - McGaugh RAR        nu = 1/(1 - exp(-sqrt(y)))
all at the FRAMEWORK a0=9.36e-11 AND the regular-MOND a0=1.2e-10 (both ways, per the working rule).
"""
import numpy as np

# ---- constants / cosmology (framework canon) -------------------------------------------
c, G, Msun, kpc, Mpc = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
H0   = 2.184e-18                      # 67.4 km/s/Mpc
Om, OmL = 0.315, 0.685
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
RHO_DE0   = OmL*RHO_CRIT0

A0_FRAME = 0.5*c*np.sqrt(G*RHO_DE0)   # framework pure-Lambda a0
A0_MOND  = 1.2e-10                     # regular MOND

print("="*92)
print("(0) THE INTERPOLATION FORMS and a0 values")
print("="*92)
print(f"  a0_FRAME (pure dark energy)  = {A0_FRAME:.4e} m/s^2  [canon 9.36e-11]")
print(f"  a0_MOND  (regular MOND)      = {A0_MOND:.4e} m/s^2")
print(f"  ratio a0_MOND/a0_FRAME       = {A0_MOND/A0_FRAME:.4f}  (=> deep-MOND boost ~sqrt of this = {np.sqrt(A0_MOND/A0_FRAME):.4f})")

# ---- the three nu functions (g_obs / g_bar as a function of y = g_bar/a0) ---------------
def nu_dSU(y):      # de Sitter-Unruh = framework's OWN form: g_obs=sqrt(gb^2+gb a0)
    return np.sqrt(1.0 + 1.0/y)
def nu_simple(y):   # standard "simple" mu = x/(1+x)
    return 0.5*(1.0 + np.sqrt(1.0 + 4.0/y))
def nu_mcgaugh(y):  # McGaugh 2016 RAR
    return 1.0/(1.0 - np.exp(-np.sqrt(y)))

print()
print("="*92)
print("(1) THE MILD-MOND CLUSTER REGIME: nu(y) for y=g_bar/a0 ~ 0.5-2  (the crux)")
print("="*92)
print(f"  {'y=gb/a0':>9}{'nu_dSU':>10}{'nu_simple':>11}{'nu_McGaugh':>12}   <- boost g_obs/g_bar")
for y in (0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0):
    print(f"  {y:>9.2f}{nu_dSU(y):>10.4f}{nu_simple(y):>11.4f}{nu_mcgaugh(y):>12.4f}")
print("""
  READING: in mild MOND (y~0.5-2) the three nu's DIFFER. dS-Unruh (sqrt) is the WEAKEST boost
  of the three at fixed a0 -- it has the gentlest transition. So at FIXED a0 the dS-Unruh form
  gives the SMALLEST g_obs => predicts the LEAST dynamical mass => LARGEST cluster deficit.
  This is the framework's own interpolation working AGAINST it in the cluster regime.""")

print()
print("="*92)
print("(2) ETA = g_obs_needed / (nu * g_bar) ON REAL eRASS1 CLUSTERS  (the deficit factor)")
print("="*92)
import os
from astropy.io import fits
FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"
d = fits.open(FITS)[1].data
def col(name):
    return np.array([float(v) if str(v).strip() not in ("","--") else np.nan for v in d[name]], float)
z, M500, Mgas, fgas, R500, KT = col("BEST_Z"), col("M500"), col("MGAS500"), col("FGAS500"), col("R500"), col("KT")
fstar = 0.20  # stellar/gas baseline (gas+stars baryons)
ok = (z>0)&(z<1)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>0.01)&(fgas<0.30)
M500_kg = M500[ok]*1e13*Msun
Mbar_kg = (1+fstar)*Mgas[ok]*1e11*Msun
R_m = R500[ok]*kpc
gobs = G*M500_kg/R_m**2            # = G M_dyn(500)/R500^2  (the "needed" gravity)
gbar = G*Mbar_kg/R_m**2
N = ok.sum()
print(f"  N = {N} clean eRASS1 clusters; z_med={np.median(z[ok]):.3f}")
print(f"  at R500: g_bar/a0_FRAME median = {np.median(gbar)/A0_FRAME:.3f}  (mild-to-deep MOND boundary)")
print(f"           g_bar/a0_FRAME quartiles = {np.percentile(gbar/A0_FRAME,[25,50,75]).round(3)}")
print(f"  fraction with y=g_bar/a0 in [0.5,2] (mild MOND): {100*((gbar/A0_FRAME>0.5)&(gbar/A0_FRAME<2)).mean():.0f}%")
print(f"  fraction with y<0.5 (deeper):                    {100*(gbar/A0_FRAME<0.5).mean():.0f}%")

# eta = g_obs / (nu * g_bar) = M_dyn / M_pred  -- the residual deficit (1 = perfect)
def eta_of(nu_func, a0):
    y = gbar/a0
    gpred = nu_func(y)*gbar
    return gobs/gpred

print(f"\n  ETA = M_dyn/M_pred (median; quartiles) -- residual missing-mass factor at R500:")
print(f"  {'interpolation':>16}{'a0=9.36e-11 (FRAME)':>26}{'a0=1.2e-10 (MOND)':>24}")
for name, nu in [("dS-Unruh", nu_dSU), ("simple", nu_simple), ("McGaugh", nu_mcgaugh)]:
    eF = eta_of(nu, A0_FRAME); eM = eta_of(nu, A0_MOND)
    print(f"  {name:>16}{np.median(eF):>12.3f} {str(np.percentile(eF,[25,75]).round(2)):>13}"
          f"{np.median(eM):>12.3f} {str(np.percentile(eM,[25,75]).round(2)):>11}")

print()
print("="*92)
print("(2b) WHERE is the mild-MOND regime? -- radial profile, NFW-like baryon distribution")
print("="*92)
# At R500, integrated g_bar/a0 ~ 0.037 (DEEP MOND). The mild-MOND regime y~0.5-2 lives at
# SMALLER radii where the baryon surface density is high (cluster core). The A&A 2024 paper's
# worst residual (M_mm/M_bar ~ 1-5) is at R~200-300 kpc (inner). Let's locate y~1 for a typical
# cluster. Take a typical M500=2e14 Msun cluster, gas ~ beta-model, find r where g_bar=a0.
M500_typ = 2e14*Msun
R500_typ = 1300*kpc  # typical
# beta-model gas: rho_g ~ (1+(r/rc)^2)^(-3beta/2), beta=2/3, rc~150 kpc; enclosed gas mass profile.
# Simplify: assume g_bar(r) = G M_bar(<r)/r^2. Use the eRASS1 median to anchor g_bar(R500).
gbar_R500 = np.median(gbar)
print(f"  Typical cluster: g_bar(R500) ~ {gbar_R500:.2e} = {gbar_R500/A0_FRAME:.3f} a0_FRAME (deep MOND at R500).")
# g_bar peaks in the core. For a beta-model the enclosed mass M(<r) ~ r^3/(rc^3) inner, ~r outer.
# g_bar = GM/r^2 peaks near rc. Crudely, g_bar(rc) can be ~10-30x g_bar(R500). Let's bracket.
for fac in (1,5,10,20,30):
    g = gbar_R500*fac
    print(f"    if g_bar(core) ~ {fac:>2d}x g_bar(R500): y=g/a0_FRAME = {g/A0_FRAME:.2f}"
          f"   -> {'MILD MOND (y~0.5-2)' if 0.3<g/A0_FRAME<3 else ('Newtonian-ish' if g/A0_FRAME>3 else 'still deep')}")
print("""  => The mild-MOND y~0.5-2 regime the brief names lives in the cluster CORE (r~100-400 kpc),
  NOT at the integrated R500 radius (which is DEEP MOND, y~0.04). The eRASS1 R500 test above
  therefore probes DEEP MOND, where all three nu's converge and the deficit is ~2.0-2.3x.
  The mild-MOND core is exactly where MOND's residual is WORST (A&A2024: M_mm/M_bar ~ 1-5).""")

print()
print("="*92)
print("(3) THE a0(z) LEVER at the cluster formation epoch z~0.3")
print("="*92)
W0, WA = -0.752, -0.86
def rho_DE_ratio(zz): return (1+zz)**(3*(1+W0+WA))*np.exp(-3*WA*zz/(1+zz))
def a0_frame_z(zz): return A0_FRAME*np.sqrt(rho_DE_ratio(zz))
for zz in (0.0, 0.1, 0.3, 0.5):
    # deep-MOND deficit scales as eta ~ 1/sqrt(a0), so the help from a0(z) is sqrt(a0(z)/a0(0))
    ratio = a0_frame_z(zz)/A0_FRAME
    help_dex = 0.5*np.log10(ratio)  # eta ~ 1/sqrt(a0) => log eta shifts by -0.5 log(a0 ratio)
    print(f"  z={zz:.2f}: a0(z)/a0(0)={ratio:.4f}  => deep-MOND deficit helped by {0.5*np.log10(ratio):+.4f} dex"
          f" (need +0.66 dex to close 2x->parity... wait, 2x=0.30 dex)")
need_dex = np.log10(2.0)
zz=0.3
help_dex = 0.5*np.log10(a0_frame_z(zz)/A0_FRAME)
print(f"\n  To close a 2x deficit needs {need_dex:.3f} dex of help (NOT 0.66 -- 0.66 dex would be 4.6x).")
print(f"  a0(z) at z=0.3 supplies {help_dex:+.4f} dex (={(a0_frame_z(0.3)/A0_FRAME):.3f}x in a0, {np.sqrt(a0_frame_z(0.3)/A0_FRAME):.3f}x in deficit).")
print(f"  => the a0(z) lever supplies ~{help_dex:+.3f} dex vs the {need_dex:.2f} dex needed: NEGLIGIBLE ({100*help_dex/need_dex:.0f}% of the gap), and it has the WRONG SIGN early (a0 rises => deficit slightly WORSE at z~0.3).")

print()
print("="*92)
print("(4) THE BARYON BUDGET: how much of the ~2x can honest baryon accounting supply?")
print("="*92)
# In DEEP MOND, g_obs = sqrt(g_bar * a0), so M_pred ~ sqrt(M_bar). A boost in baryons M_bar by
# factor B reduces the deficit eta = M_dyn/M_pred by sqrt(B):  eta_new = eta_old / sqrt(B).
# (Because g_pred ~ sqrt(g_bar) => boosting g_bar by B raises g_pred by sqrt(B).)
eta0_frame = 2.334   # dS-Unruh, framework a0, R500 (from part 2)
eta0_mond  = 2.073   # dS-Unruh, regular MOND a0
print("  In DEEP MOND g_pred ~ sqrt(g_bar), so a baryon boost B shrinks eta by sqrt(B):")
print(f"  starting deficit (dS-Unruh): eta(a0_FRAME)={eta0_frame:.2f}, eta(a0_MOND)={eta0_mond:.2f}\n")
print(f"  {'baryon source':>42}{'boost B':>9}{'eta_FRAME':>11}{'eta_MOND':>10}")
budget = [
  ("baseline (gas + stars, fstar=0.2)",                1.00),
  ("+ ICL/BCG undercount (~25% of stellar)",           1.05),
  ("+ missing baryons to R500 (~18% below cosmic)",    1.18),
  ("+ IGIMF stellar+remnant doubling (Kroupa 2026)",   2.00),
  ("ALL stacked (ICL + missing + IGIMF)",              2.0*1.05*1.18/1.0),  # but IGIMF only boosts STELLAR
]
for name, B in budget:
    print(f"  {name:>42}{B:>9.2f}{eta0_frame/np.sqrt(B):>11.2f}{eta0_mond/np.sqrt(B):>10.2f}")
print("""
  KEY SUBTLETY (honest): the IGIMF 'doubling' is a doubling of the STELLAR+remnant mass, NOT the
  total baryon mass. In clusters HOT GAS dominates (gas ~ 5-7x stellar within R500). So doubling
  stars raises TOTAL baryons by only ~(1 + f_star_extra), not 2x. Let f_star/f_gas ~ 0.15-0.20:""")
# Honest total-baryon boost from doubling stars: M_bar = M_gas + M_star; double M_star.
# B_total = (M_gas + 2 M_star)/(M_gas + M_star) = 1 + M_star/(M_gas+M_star)
for fstar_frac in (0.10, 0.15, 0.20, 0.30):  # M_star/(M_gas+M_star)
    B_total = 1 + fstar_frac
    print(f"    f_star={fstar_frac:.2f} of baryons: doubling stars -> total baryon boost B={B_total:.2f}"
          f" -> eta_FRAME {eta0_frame:.2f}->{eta0_frame/np.sqrt(B_total):.2f}, eta_MOND {eta0_mond:.2f}->{eta0_mond/np.sqrt(B_total):.2f}")
print("""
  => The Kroupa/IGIMF '2x heavier => matches MOND' claim works because THEIR baryon accounting
  finds clusters are 2x heavier in TOTAL (they include large ICL + remnant + revised gas), AND
  they use a0=1.2e-10 with a different nu. With the FRAMEWORK's LOWER a0 and the WEAKER dS-Unruh
  nu, the SAME honest +18-25% baryon gain only takes eta from ~2.33 to ~2.1 -- it does NOT close.""")

print()
print("="*92)
print("(5) HONEST RECONCILIATION with the IGIMF '88% of dynamical mass' claim")
print("="*92)
# IGIMF paper: M_bar reaches 88% of M_dyn(MOND) at a0=1.2e-10. That is eta = 1/0.88 = 1.14 deficit.
# Their TOTAL baryon boost vs our baseline: eta went 2.07 -> 1.14 at a0_MOND => B = (2.07/1.14)^2.
B_igimf = (eta0_mond/1.14)**2
print(f"  IGIMF result: M_bar = 88% of M_dyn at a0=1.2e-10 => eta_IGIMF = 1/0.88 = 1.14.")
print(f"  To go from our baseline eta_MOND={eta0_mond:.2f} to 1.14 needs B = (2.07/1.14)^2 = {B_igimf:.2f}x baryons.")
print(f"  That is a {B_igimf:.1f}x TOTAL baryon increase -- consistent with their 'clusters 2x heavier' headline.")
print(f"  Apply that SAME {B_igimf:.1f}x boost at the FRAMEWORK a0 with dS-Unruh nu:")
eta_frame_igimf = eta0_frame/np.sqrt(B_igimf)
print(f"     eta_FRAME = {eta0_frame:.2f}/sqrt({B_igimf:.2f}) = {eta_frame_igimf:.2f}  (residual {100*(eta_frame_igimf-1):.0f}% over parity)")
print(f"  => EVEN WITH the full contested IGIMF 2x-baryon boost, the FRAMEWORK's lower a0 + weaker")
print(f"     dS-Unruh nu leaves eta ~ {eta_frame_igimf:.2f}: a ~{100*(eta_frame_igimf-1):.0f}% residual that does NOT close.")
print(f"     The framework is sqrt(1.2e-10/9.36e-11) = {np.sqrt(A0_MOND/A0_FRAME):.3f}x WORSE than the MOND value the")
print(f"     IGIMF paper used to claim closure. The baryon fix closes MOND-at-1.2e-10, not the framework.")

print()
print("="*92)
print("(6) ROBUSTNESS: what survives convention choice? (the working-rule both-ways check)")
print("="*92)
# The deep-MOND limit: all three nu -> 1/sqrt(y), so eta is IDENTICAL across nu's at R500 (y~0.04).
y_deep = 0.037
print(f"  At y=g_bar/a0={y_deep} (eRASS1 R500): nu_dSU={nu_dSU(y_deep):.3f}, nu_simple={nu_simple(y_deep):.3f}, nu_McGaugh={nu_mcgaugh(y_deep):.3f}")
print(f"  => in DEEP MOND the three nu's agree to {100*abs(nu_dSU(y_deep)-nu_simple(y_deep))/nu_dSU(y_deep):.1f}%. The interpolation CHOICE is moot at R500.")
print(f"     The dS-Unruh form only HURTS (weakest boost) in the MILD-MOND CORE (y~0.5-2), {100*(1-nu_dSU(1.0)/nu_simple(1.0)):.0f}% weaker at y=1.\n")

# The ONLY robust, convention-free statement: framework a0 < MOND a0 => deeper deficit by sqrt(ratio).
print(f"  CONVENTION-ROBUST deficit ratio (framework vs regular MOND), deep-MOND, ANY nu:")
print(f"     eta_FRAME/eta_MOND = sqrt(a0_MOND/a0_FRAME) = sqrt({A0_MOND/A0_FRAME:.3f}) = {np.sqrt(A0_MOND/A0_FRAME):.4f}")
print(f"     => the framework is robustly ~13% WORSE on clusters than regular MOND, independent of nu and baryon budget.")
print(f"     This is EXACT ALGEBRA (g_pred ~ sqrt(g_bar a0)), not a convention artifact.\n")

# Both-ways: is the deficit itself an artifact of integrated R500 hydrostatic masses?
print(f"  BOTH WAYS -- is the 2x itself robust, or a hydrostatic-mass artifact?")
print(f"   * eRASS1 M500 are WL-calibrated (Bulbul 2024), so NOT pure-hydrostatic-biased; the 2x is real-ish.")
print(f"   * A&A2024 (hydrostatic) + arXiv2410.02612 (LENSING, bias-free) BOTH find ~2x residual at cluster scale")
print(f"     => the deficit survives the lensing cross-check; it is NOT only a hydrostatic-bias artifact.")
print(f"   * BUT absolute eta carries ~30-50% baryon-budget systematic (fstar, gas profile, ICL). The DIRECTION")
print(f"     (lower a0 => bigger deficit) is exact; the MAGNITUDE 2.0-2.3 is uncertain at the ~tens-of-percent level.")

print()
print("="*92)
print("FINAL SYNTHESIS -- ROUTE cluster_dsunruh_baryons")
print("="*92)
print(f"""  (1) dS-Unruh nu vs standard: the framework's OWN interpolation is the WEAKEST boost in mild
      MOND => at fixed a0 it gives the LARGEST core deficit (dS-Unruh nu(1)={nu_dSU(1.0):.3f} vs simple {nu_simple(1.0):.3f}).
      At R500 (deep MOND, y~0.04) all nu's converge: dS-Unruh does NOT help, and the lower a0 HURTS.
      eRASS1 deficit (dS-Unruh, a0_FRAME): eta = 2.33 [IQR 2.16-2.74]; regular MOND: 2.07.
  (2) baryon budget: honest non-IGIMF accounting (ICL ~+5%, missing-to-R500 ~+18%) supplies only
      ~+18-25% baryons => eta 2.33 -> ~2.1 (deep MOND eta ~ 1/sqrt(B)). The CONTESTED IGIMF 'clusters
      2x heavier' fix closes MOND-at-1.2e-10 (88% of M_dyn) but at the framework a0 leaves eta ~ 1.28.
  (3) a0(z) lever at z~0.3: a0 rises +5.8% (declining-DE law has a small early bump) => deficit
      WORSE by +0.012 dex, vs the 0.30 dex needed for 2x. Negligible AND wrong-signed. Confirmed.
  ROBUST RESIDUAL: the framework is sqrt(a0_MOND/a0_FRAME)={np.sqrt(A0_MOND/A0_FRAME):.3f}x WORSE than regular MOND on
      clusters (exact algebra). After the most generous HONEST (non-IGIMF) baryon budget, a ~1.9-2.1x
      deficit survives at the framework a0. The IGIMF route can in principle reach ~1.3x but (i) is
      contested, (ii) was tuned at a0=1.2e-10, and (iii) still leaves a residual at the lower framework a0.""")
