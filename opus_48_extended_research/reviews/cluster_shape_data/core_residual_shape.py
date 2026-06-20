#!/usr/bin/env python3
"""
CORE RESIDUAL SHAPE — first-pass data confrontation of the framework's
modified-inertia MOND on two CLASH cluster cores.

Question (the decisive, contested observable):  is the core mass the framework
must SOURCE beyond the deep-MOND baryon prediction
    M_res(r) = M_lens(r) - M_MOND(r)
GAS-TRACKING (M_res/M_gas ~ flat/cored, FPS shape -> smooth ~10x-gas component,
the irreducible shared MOND gap) or GALAXY-TRACKING (M_res rises inward / tracks
the BCG stellar light, Bullet shape -> consistent with IGIMF stellar remnants ->
the framework + remnants reach ~half the core with NO new particle)?

Framework footing (quarantine: a0/Z/kappa NEVER asserted derived):
    a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2  (dS-Unruh value, used throughout)
    modified-INERTIA interpolation  g_obs = sqrt(g_bar^2 + g_bar*a0)
    -> phantom (MOND-sourced) mass  M_MOND(r) defined by g_obs(r) = G M_MOND / r^2

REAL published profiles (cite paper + table):
  M_lens(r): Umetsu+2016 ApJ 821,116 (arXiv:1507.04385) joint SL+WL+mag NFW
             RXJ1347 M200c=34.2e14 Msun(phys), c=3.09 ; A383 M200c=7.97e14, c=5.61
  M_gas(r):  RXJ1347 Gitti+2007 XMM double-beta n_e + deprojected T (calibrated to
             published Mgas(<729)=1.15e14) ; A2029 Lewis-Buote-Stocke 2003 Chandra
             (relaxed X-ray comparison).  Tabulated M_gas(<r) supplied by upstream pull.
  M_star(r): BCG deprojected stellar mass, Hernquist approx to de Vaucouleurs
             (r_h = 0.551 R_e ; Tian+2020 CLASH-RAR / Cooke+2016).
             M_star,BCG: RXJ1347 = 5.11e11, A383 = 1.78e11 Msun (Tian+2020 Table 1,
             Salpeter/Cooke).  R_e scanned (cD typical 20-40 kpc) for sensitivity.

BOTH-WAYS rule: report the shape the REAL data shows; do NOT force galaxy-tracking,
do NOT reflexively call gas-tracking.  Full systematic budget at the end.
"""

import numpy as np

# ----------------------------------------------------------------------------- constants
G      = 6.674e-11          # m^3 kg^-1 s^-2
Msun   = 1.989e30           # kg
kpc    = 3.0857e19          # m
a0     = 9.36e-11           # m/s^2  framework dS-Unruh value (NOT 1.2e-10)

R_KPC  = np.array([30., 50., 100., 200., 300., 420.])   # core radii (kpc)

# ============================================================================= LENSING
# Umetsu+2016 spherical-NFW deprojected M(<r), PHYSICAL Msun (unit-trap verified upstream:
# 34.2e14 reproduces Table-3 overdensity masses ONLY as physical Msun w/ c=3.09).
def nfw_M_of_r(r_kpc, M200c, c200, r200_kpc):
    """NFW cumulative mass M(<r). M200c in Msun, r200 in kpc."""
    rs = r200_kpc / c200
    m  = lambda x: np.log(1.0 + x) - x/(1.0 + x)
    x  = np.asarray(r_kpc) / rs
    return M200c * m(x) / m(c200)

# RXJ1347 (merger): M200c=34.2e14, c=3.09, r200=2680 kpc
M_lens_RXJ = nfw_M_of_r(R_KPC, 34.2e14, 3.09, 2680.0)
# A383 (relaxed): M200c=7.97e14, c=5.61, r200=1810 kpc
M_lens_A383 = nfw_M_of_r(R_KPC, 7.97e14, 5.61, 1810.0)

# ============================================================================= GAS
# Tabulated cumulative gas mass M_gas(<r) [Msun] from the upstream X-ray pull.
# RXJ1347: Gitti+2007 XMM double-beta + deprojected T.
# A2029  : Lewis-Buote-Stocke 2003 Chandra (relaxed comparison; note A2029 != A383,
#          but it is the relaxed X-ray control that has a fully published gas profile).
# radii:        30      50      100     200     300     420   (kpc)
Mgas_RXJ  = np.array([4.51e10, 1.89e11, 1.31e12, 8.61e12, 2.31e13, 4.69e13])
Mgas_A2029= np.array([3.16e11, 1.04e12, 4.56e12, 1.65e13, 3.23e13, 5.46e13])  # 420 from table tail

# A383 has CLASH lensing but the supplied X-ray relaxed control is A2029. For the
# A383 baryon budget we ALSO build a scaled gas estimate from A2029 normalized to
# A383's mass (A383 is ~0.65x A2029 in M500); we carry both reads explicitly.
# A383 X-ray (Allen+2008 / Newman+2013): f_gas(<r) rises ~0.05->0.13 across core.
# We use the A2029 shape scaled by the lensing-mass ratio as a transparent proxy and
# FLAG it as a proxy (not a native A383 deprojection).
scale_A383 = float(M_lens_A383[-1] / M_lens_RXJ[-1])  # rough mass scaling at 420 kpc
# better: scale by M500 ratio ~ (7.97/34.2 NFW) but gas tracks the relaxed A2029 core
Mgas_A383_proxy = Mgas_A2029 * (M_lens_A383[-1]/ (nfw_M_of_r(420., 8.0e14,5.6,1810.)))  # ~1 (A2029~A383 in core mass)
# keep it simple & honest: A383 gas ~ A2029 gas (both relaxed, similar core M); proxy=1.0
Mgas_A383 = Mgas_A2029.copy()

# ============================================================================= STARS
# Hernquist deprojection of de Vaucouleurs:  M(<r) = M_tot * r^2 / (r + a)^2 ,  a = r_h.
# r_h = 0.551 * R_e  (Tian+2020 / Hernquist 1990).  M_tot = total BCG stellar mass.
def hernquist_M_of_r(r_kpc, Mtot, Re_kpc):
    a = 0.551 * Re_kpc
    r = np.asarray(r_kpc)
    return Mtot * r**2 / (r + a)**2

# Tian+2020 Table 1 (Cooke+2016 multiwavelength, Salpeter-ish):
Mstar_BCG_RXJ  = 5.11e11   # Msun
Mstar_BCG_A383 = 1.78e11   # Msun
# Cooke+2015 mag_auto BCG-only (Salpeter): RXJ1347 3.68e11, A383 1.51e11 (lower bound).
# R_e for massive cD BCGs: scan 20/30/40 kpc; headline Re=30 kpc.
Re_headline = 30.0
# ICL: CLASH BCG+ICL ~ 1.5-2x BCG-only at large r; we add an ICL component as a
# second, more extended Hernquist (Re_ICL ~ 100 kpc) at 1.0x the BCG mass = a
# galaxy-FAVORABLE upper estimate of the total tracked stellar light. Carry BOTH
# (BCG-only headline, BCG+ICL favorable).
def Mstar_profile(r_kpc, Mbcg, Re_bcg, include_icl=False):
    M = hernquist_M_of_r(r_kpc, Mbcg, Re_bcg)
    if include_icl:
        M = M + hernquist_M_of_r(r_kpc, 1.0*Mbcg, 100.0)  # ICL = 1x BCG, Re=100 kpc
    return M

# ============================================================================= MOND
def M_mond_of_r(Mbar_of_r_func, r_kpc):
    """
    Modified-inertia MOND phantom mass:
       g_bar = G M_bar(<r) / r^2
       g_obs = sqrt(g_bar^2 + g_bar*a0)         (framework dS-Unruh nu)
       M_MOND(<r) = g_obs r^2 / G               (the TOTAL dynamical/lensing mass MOND predicts)
    Returns M_MOND in Msun.  Mbar_of_r_func(r_kpc) returns baryon mass in Msun.
    """
    r_m   = np.asarray(r_kpc) * kpc
    Mbar  = np.asarray(Mbar_of_r_func(r_kpc)) * Msun
    g_bar = G * Mbar / r_m**2
    g_obs = np.sqrt(g_bar**2 + g_bar*a0)
    M_mond= g_obs * r_m**2 / G
    return M_mond / Msun

# ============================================================================= ASSEMBLE per cluster
def run_cluster(name, M_lens, Mgas, Mbcg, Re_bcg, include_icl, relaxed):
    Mstar = Mstar_profile(R_KPC, Mbcg, Re_bcg, include_icl=include_icl)
    Mbar  = Mgas + Mstar
    Mbar_f= lambda rr: Mgas*0 + np.interp(rr, R_KPC, Mbar) if np.ndim(rr) else \
            float(np.interp(rr, R_KPC, Mbar))
    # use direct array (radii match), avoid interpolation noise:
    Mbar_func = lambda rr: Mbar  # rr == R_KPC by construction
    M_mond = M_mond_of_r(lambda rr: Mbar, R_KPC)
    M_res  = M_lens - M_mond
    out = dict(name=name, R=R_KPC, M_lens=M_lens, Mgas=Mgas, Mstar=Mstar,
               Mbar=Mbar, M_mond=M_mond, M_res=M_res, relaxed=relaxed,
               include_icl=include_icl, Re=Re_bcg, Mbcg=Mbcg)
    return out

def shape_diagnostics(out):
    R, M_res, Mgas, Mstar = out['R'], out['M_res'], out['Mgas'], out['Mstar']
    # ratios (guard against negative residual)
    res_gas  = M_res / Mgas
    res_star = M_res / Mstar
    # inner log-slope of M_res(r): d ln M_res / d ln r between 100 and 300 kpc
    # (use positive-residual core window; 100-300 is the FPS/Bullet discriminant band)
    def logslope(r1, r2):
        i1 = np.argmin(np.abs(R-r1)); i2 = np.argmin(np.abs(R-r2))
        if M_res[i1] <= 0 or M_res[i2] <= 0:
            return np.nan
        return np.log(M_res[i2]/M_res[i1]) / np.log(R[i2]/R[i1])
    slope_30_100  = logslope(30,100)
    slope_100_300 = logslope(100,300)
    slope_100_420 = logslope(100,420)
    # GAS-tracking test: is res_gas flat across 100-420? (slope of res_gas ~ 0)
    def ratio_slope(ratio, r1, r2):
        i1 = np.argmin(np.abs(R-r1)); i2 = np.argmin(np.abs(R-r2))
        if ratio[i1] <= 0 or ratio[i2] <= 0:
            return np.nan
        return np.log(ratio[i2]/ratio[i1]) / np.log(R[i2]/R[i1])
    resgas_slope_100_420  = ratio_slope(res_gas, 100, 420)
    resstar_slope_100_420 = ratio_slope(res_star, 100, 420)
    return dict(res_gas=res_gas, res_star=res_star,
                slope_30_100=slope_30_100, slope_100_300=slope_100_300,
                slope_100_420=slope_100_420,
                resgas_slope_100_420=resgas_slope_100_420,
                resstar_slope_100_420=resstar_slope_100_420)

def fmt(a):
    return "  ".join(f"{x:9.3e}" for x in a)

print("="*94)
print("FRAMEWORK FOOTING:  a0 = 9.36e-11 m/s^2 (dS-Unruh),  g_obs = sqrt(g_bar^2 + g_bar*a0)")
print("Radii (kpc):", "  ".join(f"{r:7.0f}" for r in R_KPC))
print("="*94)

runs = {}
configs = [
    # name, M_lens, Mgas, Mbcg, Re, include_icl, relaxed
    ("RXJ1347 (merger, BCG-only)",          M_lens_RXJ , Mgas_RXJ , Mstar_BCG_RXJ , 30., False, False),
    ("RXJ1347 (merger, BCG+ICL favorable)", M_lens_RXJ , Mgas_RXJ , Mstar_BCG_RXJ , 30., True , False),
    ("A383 (relaxed, BCG-only)",            M_lens_A383, Mgas_A383, Mstar_BCG_A383, 30., False, True ),
    ("A383 (relaxed, BCG+ICL favorable)",   M_lens_A383, Mgas_A383, Mstar_BCG_A383, 30., True , True ),
]

for cfg in configs:
    out = run_cluster(*cfg)
    diag= shape_diagnostics(out)
    runs[cfg[0]] = (out, diag)
    print("\n" + "-"*94)
    print(f"### {out['name']}    [Re_BCG={out['Re']:.0f} kpc, M_BCG={out['Mbcg']:.2e}, "
          f"{'+ICL' if out['include_icl'] else 'BCG-only'}, relaxed={out['relaxed']}]")
    print(f"{'r(kpc)':>8} {'M_lens':>11} {'M_gas':>11} {'M_star':>11} {'M_bar':>11} "
          f"{'M_MOND':>11} {'M_res':>11} {'res/gas':>9} {'res/star':>9}")
    for i,r in enumerate(R_KPC):
        print(f"{r:8.0f} {out['M_lens'][i]:11.3e} {out['Mgas'][i]:11.3e} "
              f"{out['Mstar'][i]:11.3e} {out['Mbar'][i]:11.3e} {out['M_mond'][i]:11.3e} "
              f"{out['M_res'][i]:11.3e} {diag['res_gas'][i]:9.2f} {diag['res_star'][i]:9.2f}")
    print(f"  inner log-slope d lnM_res/d lnr :  [30->100]={diag['slope_30_100']:+.2f}  "
          f"[100->300]={diag['slope_100_300']:+.2f}  [100->420]={diag['slope_100_420']:+.2f}")
    print(f"  slope of (M_res/M_gas)  [100->420] = {diag['resgas_slope_100_420']:+.2f}   "
          f"(~0 => GAS-tracking/flat; <0 => res falls slower than gas... see read)")
    print(f"  slope of (M_res/M_star) [100->420] = {diag['resstar_slope_100_420']:+.2f}   "
          f"(~0 => GALAXY-tracking)")

# ----------------------------------------------------------------------------- R_e sensitivity
print("\n" + "="*94)
print("R_e SENSITIVITY (A383 relaxed, BCG-only): does the read flip with BCG concentration?")
print("="*94)
for Re in [20., 30., 40.]:
    out = run_cluster("A383 Re-scan", M_lens_A383, Mgas_A383, Mstar_BCG_A383, Re, False, True)
    diag= shape_diagnostics(out)
    print(f"  Re={Re:4.0f} kpc:  res/star @100kpc={diag['res_star'][2]:7.1f}  @420kpc={diag['res_star'][5]:7.1f}  "
          f"| res/gas @100={diag['res_gas'][2]:6.1f} @420={diag['res_gas'][5]:6.1f}  "
          f"| slope(res/gas)={diag['resgas_slope_100_420']:+.2f}")

# ----------------------------------------------------------------------------- core-coverage implication
print("\n" + "="*94)
print("NO-PARTICLE CORE COVERAGE IMPLICATION (<420 kpc)")
print("="*94)
for key in ["A383 (relaxed, BCG-only)", "RXJ1347 (merger, BCG-only)"]:
    out, diag = runs[key]
    i420 = -1
    Mlens420 = out['M_lens'][i420]
    Mmond420 = out['M_mond'][i420]
    Mres420  = out['M_res'][i420]
    # framework MI phantom coverage = (M_mond - M_bar) is the phantom; coverage of the
    # LENS-required total by MOND alone:
    cover_mond = Mmond420 / Mlens420
    print(f"  {key}: M_lens(<420)={Mlens420:.3e}  M_MOND(<420)={Mmond420:.3e}  "
          f"M_res(<420)={Mres420:.3e}  -> MOND covers {cover_mond*100:.0f}% of lensing total")

# ----------------------------------------------------------------------------- DENSITY-SLOPE read (the discriminant)
print("\n" + "="*94)
print("LOCAL DENSITY-SLOPE READ (the gas-vs-galaxy discriminant) -- A383 relaxed, BCG-only")
print("="*94)
out, diag = runs["A383 (relaxed, BCG-only)"]
def shell_density(M):
    dM = np.gradient(M, R_KPC)
    return dM/(4*np.pi*R_KPC**2)          # arb units
rho_res  = shell_density(out['M_res'])
rho_gas  = shell_density(out['Mgas'])
rho_star = shell_density(out['Mstar'])
def dlnrho(y,i1,i2): return np.log(y[i2]/y[i1])/np.log(R_KPC[i2]/R_KPC[i1])
print(f"  d ln rho_res /d ln r [50->300] = {dlnrho(rho_res ,1,4):+.2f}   (residual)")
print(f"  d ln rho_gas /d ln r [50->300] = {dlnrho(rho_gas ,1,4):+.2f}   (hot gas)")
print(f"  d ln rho_star/d ln r [50->300] = {dlnrho(rho_star,1,4):+.2f}   (BCG stars -- de Vauc/Hernquist)")
print("  -> residual slope ~ -1.8 sits BETWEEN gas (-1.3) and stars (-3.6), MUCH closer to gas.")
print("  -> BCG stellar mass is ~74% enclosed by 100 kpc, ~93% by 420 kpc (Hernquist SATURATES);")
print("     the residual keeps CLIMBING to 420 kpc -> stars cannot track it -> NOT galaxy-tracking.")
print("  READ: gas-tracking / shared-MOND-gap family (a broad ~isothermal cored component, more")
print("        centrally concentrated than the gas but FAR more extended than the stellar light).")
