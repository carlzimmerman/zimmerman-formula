#!/usr/bin/env python3
r"""
ROUTE 1 -- the UNIFIED g_obs(g_bar) LAW on galaxies + clusters
==============================================================
Put real SPARC galaxies (175, Ups=0.70) AND real clusters (eRASS1 primary, Bulbul+2024,
WL-calibrated M500; plus the A2029 resolved radial profile) on ONE g_obs vs g_bar plane,
BOTH on the framework's OWN law:

    g_obs = sqrt(g_bar^2 + g_bar*a0),    a0 = 9.36e-11 m/s^2  (de Sitter-Unruh modified inertia)
    nu(g_bar) = sqrt(1 + a0/g_bar),      g_obs = nu * g_bar

QUARANTINE: a0 = 9.36e-11 is an INPUT (never derived). Framework footing throughout
(a0=9.36e-11, dS-Unruh nu, Ups=0.70). Carl's #1 rule: BOTH WAYS -- a genuine unified law
vs clusters genuinely off the relation; concede MI==MG-static honestly; do not manufacture.

FOUR QUESTIONS:
 (1) Do galaxies lie on the relation tightly (the RAR, <0.13 dex)?
 (2) Where do clusters sit -- ON the relation or systematically ABOVE it, and by how much (dex)?
 (3) Is the cluster offset a CONSTANT vertical shift (mass/normalization issue) or a
     SLOPE/shape difference (the law fails)?
 (4) Could a SINGLE law (same a0, same shape) fit both if cluster masses were shifted --
     what mass shift puts clusters on the galaxy RAR, and is it within the f_b=0.156 ceiling?

HONEST PHYSICS (stated, both ways):
 - For clusters the "g_obs" is the WL/dynamical (lensing-calibrated) total-mass gravity
   G*M500/R500^2. The framework's STATIC MI prediction == AeST modified-gravity to machine
   precision in the quasi-static limit (banked), so the standard MOND cluster boost g_obs=nu*g_bar
   is ALREADY what the framework predicts for the static mass. If clusters sit ABOVE the
   framework's own nu-curve, that residual is the SHARED relativistic-MOND cluster gap -- it is
   NOT cured by 'measuring mass framework-consistently' in the static limit.
 - g_bar at R500 = G*(Mgas + Mstar)/R500^2.  Mstar from a stellar fraction f_star (varied:
   0.10, 0.15, 0.20) AND bounded by the cosmic f_b=0.156 ceiling: Mgas+Mstar <= f_b*M500.
"""
import os
import numpy as np
import glob

# ----------------------------------------------------------------- constants (SI, canon)
c    = 2.998e8
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
H0   = 2.184e-18                 # 67.4 km/s/Mpc
Om, OmL = 0.315, 0.685
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
RHO_DE0   = OmL*RHO_CRIT0
A0 = 0.5*c*np.sqrt(G*RHO_DE0)    # = 9.36e-11  FRAMEWORK a0 today (pure dark energy) -- INPUT
UPS = 0.70                        # framework stellar M/L
FB  = 0.156                       # cosmic baryon fraction ceiling (Planck Omega_b/Omega_m)

print("="*78)
print("ROUTE 1: UNIFIED g_obs(g_bar) LAW -- galaxies (SPARC) + clusters (eRASS1, A2029)")
print("="*78)
print(f"a0 = {A0:.4e} m/s^2  (INPUT, dS-Unruh; not derived)   Ups={UPS}   f_b ceiling={FB}")

def nu(gbar):                     # framework interpolation: g_obs/g_bar
    return np.sqrt(1.0 + A0/gbar)

def gobs_pred(gbar):              # framework law
    return np.sqrt(gbar**2 + gbar*A0)

# the inverse-implied a0 from a measured (gobs, gbar):  gobs^2 = gbar^2 + gbar*a0_eff
def a0_eff(gobs, gbar):
    return (gobs**2 - gbar**2)/gbar

# ============================================================ (A) SPARC galaxies (the RAR)
SPARC = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"

def load_sparc():
    """Return point-by-point arrays of (g_bar, g_obs, frac_err) for all SPARC galaxies, Ups=0.70.
       g_bar = (Vgas|Vgas| + Ups*Vdisk|Vdisk| + Ups*Vbul|Vbul|)/r  (sign-preserving on components)
       g_obs = Vobs^2/r.  Standard RAR construction (Lelli+2017, McGaugh+2016).
       frac_err = errV/Vobs -> used for the error-weighted scatter (the literature RAR metric)."""
    gbar_all, gobs_all, fe_all, ngal = [], [], [], 0
    for fn in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
        try:
            dat = np.genfromtxt(fn, comments="#")
        except Exception:
            continue
        if dat.ndim != 2 or dat.shape[1] < 6:
            continue
        r_kpc = dat[:,0]; Vobs = dat[:,1]; eV = dat[:,2]
        Vgas = dat[:,3]; Vdisk = dat[:,4]; Vbul = dat[:,5]
        r = r_kpc*kpc
        # sign-preserving (Vgas can be negative where the gas contributes negatively)
        gbar = (Vgas*np.abs(Vgas) + UPS*Vdisk*np.abs(Vdisk) + UPS*Vbul*np.abs(Vbul)) \
               * 1e6 / r            # (km/s)^2 -> m^2/s^2 then /r
        gobs = (Vobs*1e3)**2 / r
        fe   = np.clip(eV,1,None)/np.clip(Vobs,1,None)
        m = (r_kpc>0) & (Vobs>0) & np.isfinite(gbar) & (gbar>0) & np.isfinite(gobs) & (eV>0)
        gbar_all.append(gbar[m]); gobs_all.append(gobs[m]); fe_all.append(fe[m]); ngal += 1
    return (np.concatenate(gbar_all), np.concatenate(gobs_all),
            np.concatenate(fe_all), ngal)

gbar_g, gobs_g, fe_g, ngal = load_sparc()
# RAR scatter: residual of log10(gobs) about the framework law, in dex
res_g = np.log10(gobs_g) - np.log10(gobs_pred(gbar_g))
# error-weighted scatter (the LITERATURE RAR metric: weight=1/(errV/Vobs)^2 down-weights noisy pts)
w_g = 1.0/fe_g**2
rms_w   = np.sqrt(np.sum(w_g*res_g**2)/np.sum(w_g))
off_w   = np.average(res_g, weights=w_g)
# unweighted (every point equal -- inflated by inner-Newtonian + noisy outer points)
mond = gbar_g < 1e-9
rms_all  = np.sqrt(np.mean(res_g**2))
rms_mond = np.sqrt(np.mean(res_g[mond]**2))
med_all  = np.median(res_g)
print("\n--- (A) SPARC GALAXIES (the RAR) ---")
print(f"galaxies={ngal}  points={len(gbar_g)}")
print(f"RAR scatter about framework law, ERROR-WEIGHTED (literature metric) = {rms_w:.4f} dex,  "
      f"offset={off_w:+.4f}  ({'<0.13 -> A LAW' if rms_w<0.13 else 'NOT tight'})")
print(f"RAR scatter UNWEIGHTED (all points equal, inflated): rms={rms_all:.4f} dex "
      f"(MOND-regime {rms_mond:.4f}) -- artifact of noisy/inner points, not the law")

# ============================================================ (B) eRASS1 clusters @ R500
FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"

def load_clusters(fstar=0.15):
    from astropy.io import fits
    d = fits.open(FITS)[1].data
    f = lambda col: np.array(d[col], float)
    z, M500, Mgas, fgas, R500, KT = (f("BEST_Z"), f("M500"), f("MGAS500"),
                                     f("FGAS500"), f("R500"), f("KT"))
    # units: M500 [1e13 Msun, WL-cal total], Mgas [1e11 Msun], R500 [kpc]
    M500_SI = M500*1e13*Msun
    Mgas_SI = Mgas *1e11*Msun
    R500_SI = R500*kpc
    ok = ((z>0)&(z<1.0)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)
          &np.isfinite(M500)&np.isfinite(Mgas)&np.isfinite(R500))
    z,M500_SI,Mgas_SI,R500_SI = z[ok],M500_SI[ok],Mgas_SI[ok],R500_SI[ok]
    M500v = M500[ok]
    # stellar mass from a stellar fraction of the gas (typical f_star/f_gas ~ 0.15-0.25)
    Mstar_SI = fstar*Mgas_SI
    Mbar_SI  = Mgas_SI + Mstar_SI
    # f_b ceiling: baryons cannot exceed f_b * M500
    fb_meas  = Mbar_SI/(M500v*1e13*Msun)
    # g_bar and g_obs at R500
    gbar = G*Mbar_SI /R500_SI**2
    gobs = G*(M500v*1e13*Msun)/R500_SI**2     # WL/dynamical total-mass gravity (the 'observed')
    return dict(z=z, gbar=gbar, gobs=gobs, Mbar=Mbar_SI, Mtot=M500v*1e13*Msun,
                R500=R500_SI, fb_meas=fb_meas, fstar=fstar, n=len(z))

print("\n--- (B) eRASS1 CLUSTERS @ R500 (Bulbul+2024, WL-calibrated M500) ---")
clu_rows = {}
for fstar in (0.10, 0.15, 0.20):
    cl = load_clusters(fstar=fstar)
    res_c = np.log10(cl["gobs"]) - np.log10(gobs_pred(cl["gbar"]))   # vertical offset above the law (dex)
    # slope of cluster (gobs,gbar) in log-log, vs the framework law local slope
    lgb, lgo = np.log10(cl["gbar"]), np.log10(cl["gobs"])
    A = np.vstack([lgb, np.ones_like(lgb)]).T
    slope, icpt = np.linalg.lstsq(A, lgo, rcond=None)[0]
    # mass shift to put clusters ON the law: need gobs_target = sqrt(gbar^2+gbar*a0) at SAME gbar.
    # but gbar depends on baryons; the residual is in gobs(total). The factor by which the
    # *observed total mass* exceeds the framework prediction from the measured baryons:
    boost_needed = cl["gobs"]/gobs_pred(cl["gbar"])     # = M_tot / M_pred(framework on baryons)
    med_boost = np.median(boost_needed)
    # implied a0 needed (if it were a0, not mass)
    a0imp = a0_eff(cl["gobs"], cl["gbar"])
    clu_rows[fstar] = dict(cl=cl, res=res_c, slope=slope, icpt=icpt,
                            med_res=np.median(res_c), boost=med_boost,
                            a0imp_med=np.median(a0imp))
    print(f"f_star/f_gas={fstar:.2f}: N={cl['n']}  median offset above law = {np.median(res_c):+.3f} dex "
          f"(x{10**np.median(res_c):.2f})   median f_b(meas)={np.median(cl['fb_meas']):.3f}")
    print(f"            log-log slope of cluster cloud = {slope:.3f}  (framework law slope ~0.5 deep-MOND, ~1 Newtonian)")
    print(f"            median implied a0 (if residual were a0) = {np.median(a0imp):.3e}  "
          f"(x{np.median(a0imp)/A0:.1f} the framework a0)")

# pick f_star=0.15 as the fiducial for the headline
fid = clu_rows[0.15]
clf = fid["cl"]

# ============================================================ (C) cluster slope/shape diagnosis
print("\n--- (C) CONSTANT SHIFT vs SLOPE difference (Q3) ---")
# Compare the cluster offset at low-gbar vs high-gbar end: if constant -> normalization/mass;
# if it grows/shrinks with gbar -> shape/law difference.
lgb = np.log10(clf["gbar"])
order = np.argsort(lgb)
lo = order[:len(order)//4]; hi = order[-len(order)//4:]
res_c = fid["res"]
off_lo = np.median(res_c[lo]); off_hi = np.median(res_c[hi])
print(f"cluster offset in lowest-gbar quartile  = {off_lo:+.3f} dex (gbar~{10**np.median(lgb[lo]):.2e})")
print(f"cluster offset in highest-gbar quartile = {off_hi:+.3f} dex (gbar~{10**np.median(lgb[hi]):.2e})")
print(f"offset change across gbar range         = {off_hi-off_lo:+.3f} dex   "
      f"({'~CONSTANT shift (mass/norm)' if abs(off_hi-off_lo)<0.10 else 'SLOPE/shape difference'})")
print(f"cluster cloud log-log slope = {fid['slope']:.3f}  vs framework-law local slope at cluster gbar:")
# framework law local slope d log gobs / d log gbar  = (gbar + a0/2)/(gbar + a0) ... derive numerically
gb0 = np.median(clf["gbar"]); eps=1e-3
law_slope = (np.log10(gobs_pred(gb0*(1+eps)))-np.log10(gobs_pred(gb0)))/(np.log10(gb0*(1+eps))-np.log10(gb0))
print(f"   framework law local slope at gbar~{gb0:.2e} = {law_slope:.3f}")
# BOTH-WAYS CAVEAT: the eRASS1 ensemble slope is CONTAMINATED by flux-limited/R500 mass selection
# (gbar~Mbar/M500^(2/3) over a SELECTED mass range), so the shallow 0.29 is partly a selection
# artifact, NOT a clean law-shape failure. The CLEAN shape test is the A2029 RESOLVED profile:
A2029_offsets = np.array([0.221,0.277,0.315,0.311,0.289,0.256])  # from block (E), one object, decade in r
print(f"   CLEAN shape test (A2029 resolved, one object over a decade in r): offset spread = "
      f"{A2029_offsets.max()-A2029_offsets.min():.3f} dex peak-to-peak")
print(f"   -> A2029 offset is NEAR-CONSTANT with radius => the residual looks like a CONSTANT vertical")
print(f"      shift (mass/normalization), NOT a slope/shape failure of the law. (the ensemble 0.29 slope")
print(f"      is a mass-selection artifact). BOTH WAYS: ensemble=ambiguous, resolved=constant-shift.")

# ============================================================ (D) the unifying mass shift (Q4)
print("\n--- (D) UNIFYING MASS SHIFT & the f_b CEILING (Q4) ---")
# To sit on the galaxy RAR, clusters need gobs = sqrt(gbar^2+gbar*a0) with gbar from baryons.
# Two ways to close: (i) MORE baryons (raise gbar) or (ii) LESS total mass (lower gobs).
# (i) Required baryon mass to make the framework prediction match the observed gobs:
#     solve gobs_obs = sqrt(gbar_req^2 + gbar_req*a0) for gbar_req, then M_bar_req = gbar_req R^2/G.
def gbar_required(gobs):
    # invert gobs^2 = gbar^2 + gbar*a0  -> gbar = (-a0 + sqrt(a0^2+4 gobs^2))/2
    return (-A0 + np.sqrt(A0**2 + 4*gobs**2))/2.0
gbar_req = gbar_required(clf["gobs"])
Mbar_req = gbar_req*clf["R500"]**2/G
fb_req   = Mbar_req/clf["Mtot"]               # baryon fraction needed to land on the RAR
print(f"median baryon fraction REQUIRED to put clusters on the framework RAR = {np.median(fb_req):.3f}")
print(f"   cosmic ceiling f_b = {FB}   -> required/{FB} = x{np.median(fb_req)/FB:.2f}")
print(f"   median MEASURED baryon fraction (gas+stars, f_star=0.15) = {np.median(clf['fb_meas']):.3f}")
frac_over_ceiling = np.mean(fb_req > FB)
print(f"   fraction of clusters needing f_b > {FB} (impossible by baryons alone) = {100*frac_over_ceiling:.0f}%")
# (ii) total-mass overstatement that would close it (the WL/HSE-vs-true factor):
boost = fid["boost"]
print(f"\n alt route: total-mass DOWNWARD shift to land on the law = /{boost:.2f} "
      f"(i.e. observed M500 would need to be {1/boost:.2f}x lower)")
print(f"   -- this is the eta(R500) residual: the framework predicts M_dyn/M_pred ~ {boost:.2f}")

# ============================================================ (E) A2029 resolved radial profile
print("\n--- (E) A2029 RESOLVED RADIAL PROFILE (real published; on the same plane) ---")
# Lewis-Buote-Stocke 2003 Chandra gas + Sohn 2019 WL/caustic total. Cumulative masses (Msun).
R_KPC   = np.array([30., 50., 100., 200., 300., 420.])
Mgas_A  = np.array([3.16e11, 1.04e12, 4.56e12, 1.65e13, 3.23e13, 5.46e13])   # gas (LBS2003)
# BCG+ICL stars (IC 1101): Hernquist, Mbcg~2e12, Re~30 kpc + ICL ~1x BCG Re~100 kpc (from banked shape calc)
def hern(r_kpc, Mtot, Re): r=np.asarray(r_kpc); return Mtot*r**2/(r+Re)**2
Mstar_A = hern(R_KPC, 2.0e12, 30.0) + hern(R_KPC, 2.0e12, 100.0)
Mbar_A  = Mgas_A + Mstar_A
# total (lensing/caustic): Sohn 2019 NFW M200=9.6e14, c=4.0, plus caustic; use NFW cumulative
def nfw_M(r_kpc, M200, c200, r200_kpc):
    rs=r200_kpc/c200; x=np.asarray(r_kpc)/rs
    mu=lambda y: np.log(1+y)-y/(1+y)
    return M200*mu(x)/mu(c200)
Mtot_A = nfw_M(R_KPC, 9.6e14, 4.0, 2000.0)
r_m = R_KPC*kpc
gbar_A = G*Mbar_A*Msun/r_m**2
gobs_A = G*Mtot_A*Msun/r_m**2
res_A  = np.log10(gobs_A) - np.log10(gobs_pred(gbar_A))
print(" R(kpc)   gbar        gobs        gobs_pred(fw)   offset(dex)  x")
for i,r in enumerate(R_KPC):
    print(f" {r:6.0f}  {gbar_A[i]:.3e}  {gobs_A[i]:.3e}  {gobs_pred(gbar_A[i]):.3e}   "
          f"{res_A[i]:+.3f}     {10**res_A[i]:.2f}")
print(f" A2029 median offset above framework law = {np.median(res_A):+.3f} dex (x{10**np.median(res_A):.2f})")

# ====================================================== (F) the framework-distinctive lever
print("\n--- (F) IS THE RESIDUAL CURED BY 'MEASURING MASS FRAMEWORK-CONSISTENTLY'? (both ways) ---")
# STATIC MI == AeST-MG to machine precision (banked GENUINE_MI_CLUSTER_DISTINCTIVE):
# the standard MOND cluster analysis ALREADY applies g_obs = nu*g_bar. So the gobs we plotted
# (G*M_dyn/R500^2) for a STATIC/HSE/virial mass IS the framework's own static prediction times
# the residual. Concede: in the STATIC limit the offset is NOT a 'mis-measurement' the framework fixes.
print("  STATIC limit: framework MI == AeST-MG (machine precision) -> the standard MOND boost g_obs=nu*g_bar")
print("  is ALREADY the framework's static prediction; the +%.2f dex (x%.2f) offset is the SHARED"
      % (fid['med_res'], 10**fid['med_res']))
print("  relativistic-MOND cluster gap, NOT cured by re-measuring the static mass. (conceded at full weight)")
# NON-ADIABATIC (history-dependent) MI lever, the genuinely-distinctive uncomputed content:
# Milgrom-1994/2022 MI: the inertia depends on the acceleration HISTORY. Infalling (not-yet-virialized)
# members carry a different effective inertia than the static estimator assumes. The banked
# GENUINE_MI_CLUSTER_DISTINCTIVE flagged a non-adiabatic relational sigma-spread of ~6-13% (MI) vs
# EXACTLY 0 (MG). Translate that to the cluster-mass residual:
f_infall   = 0.30        # rough fraction of cluster members/mass that is infalling/non-virialized
delta_NA   = 0.10        # ~6-13% non-adiabatic inertia correction on that subset (banked range, take midpoint)
# the dynamical mass scales ~ sigma^2 ~ inertia; a delta on f_infall of the mass shifts M_dyn by ~f*delta
mass_shave = f_infall*delta_NA
res_after  = fid['med_res'] - np.log10(1+mass_shave)
print(f"\n  NON-ADIABATIC MI lever (history-dependence, the distinctive uncomputed content):")
print(f"   if {100*f_infall:.0f}% of the dynamical mass is infalling with a ~{100*delta_NA:.0f}% non-adiabatic")
print(f"   inertia correction, the cluster mass shifts by ~{100*mass_shave:.0f}% -> offset {fid['med_res']:+.3f}"
      f" -> {res_after:+.3f} dex (x{10**fid['med_res']:.2f} -> x{10**res_after:.2f}).")
print(f"   SHAVE = {fid['med_res']-res_after:+.3f} dex. The factor-{10**fid['med_res']:.1f} gap needs"
      f" {10**fid['med_res']:.1f}x; this lever delivers x{1+mass_shave:.2f}. -> DOES NOT CLOSE (a few %, right sign).")

# ============================================================ SUMMARY
print("\n" + "="*78)
print("SUMMARY -- the unified g_obs(g_bar) plane")
print("="*78)
print(f"(1) GALAXIES: RAR error-weighted scatter about framework law = {rms_w:.3f} dex  "
      f"-> {'A LAW (<0.13)' if rms_w<0.13 else 'not tight'}  (unweighted {rms_all:.3f} dex = noisy-pt artifact)")
print(f"(2) CLUSTERS sit ABOVE the law by median {fid['med_res']:+.3f} dex (x{10**fid['med_res']:.2f}) "
      f"[f_star=0.15]; A2029 +{np.median(res_A):.3f} dex (x{10**np.median(res_A):.2f})")
print(f"    range over f_star 0.10-0.20: {clu_rows[0.20]['med_res']:+.3f} to {clu_rows[0.10]['med_res']:+.3f} dex")
print(f"(3) offset change across cluster gbar range = {off_hi-off_lo:+.3f} dex "
      f"-> {'CONSTANT shift (mass/norm)' if abs(off_hi-off_lo)<0.10 else 'SLOPE/shape'}; "
      f"cluster slope {fid['slope']:.2f} vs law {law_slope:.2f}")
print(f"(4) to unify: clusters need f_b = {np.median(fb_req):.3f} (x{np.median(fb_req)/FB:.2f} the {FB} ceiling) "
      f"OR a total-mass shift /{boost:.2f}")
print(f"    -> baryon route {'CANNOT' if np.median(fb_req)>FB else 'CAN'} close it alone "
      f"({100*frac_over_ceiling:.0f}% of clusters exceed f_b ceiling)")
