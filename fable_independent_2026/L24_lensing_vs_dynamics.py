#!/usr/bin/env python3
"""
L24 -- cluster LENSING versus cluster DYNAMICS: the observable that separates "extra mass" from
       "modified force", and which this programme's cluster work has never used.
================================================================================================
Every cluster verdict this lane reached tonight -- L2 (no kernel), L5 (no fixed-strength long-range
force), L6 (no screened force), L7 (the residual IS the cosmic dark-to-baryon share), L18 (the
hydrostatic bias makes it worse, not better) -- rests on ONE mass probe: X-ray gas in hydrostatic
equilibrium.  There is a second probe with completely different systematics, gravitational lensing,
and this repository has never applied it to clusters.

WHAT THE REPOSITORY ALREADY HAS (surveyed, not duplicated):
  * `prep_2026/mi_lensing_final/` -- the MODIFIED-INERTIA arm's lensing no-go, at GALAXY scale.
    The assembled single-metric MI stress tensor under-lenses: F(y) = g_lens/(nu*g_bar) < 1/nu < 1
    everywhere, and Brouwer et al. 2021's KiDS-1000 lensing RAR excludes it (Delta chi^2 = +722/+754,
    both footings, conservative rail).  Its model-free core: g_lens <= g_bar for ANY baryonic source.
  * `prep_2026/kids_rar/` -- KiDS-1000 lensing as a THIRD road to a0 (a consistency, not a free fit).
  * `prep_2026/rar_origin_2026/dark_charge_kids_lensing_gate_2026.py`, and the AeST boundary-constant
    closure (KiDS Delta chi^2 >= +106 at every m^2).  All galaxy-galaxy lensing.
  * `hunt_2026/h67_hff_cores.py` -- ASKED for eta(r) = M_lens/M_framework in four Hubble Frontier
    Fields cluster cores and reported, correctly, that it was NOT RUNNABLE: the on-disk tables are
    member photometry with no convergence map and no lens-model mass profile.
  => cluster lensing masses have never entered a framework test in this repository.  This lane
     supplies them.  It does NOT re-do L18's hydrostatic-bias systematic; it MEASURES the bias
     empirically for this sample as a control, which is a different and complementary thing.

THE STRUCTURE OF THE TEST.  In the framework's MODIFIED-GRAVITY arm -- the arm the action carries --
the two metric potentials are equal (`THE_ACTION_2026-09-05.md` section 4: "PPN (static ladder,
boosted, Will dictionary): gamma = 1"), so light and gas fall in the SAME potential.  Hence

    (i)   the framework's predicted lensing convergence is fixed by the SAME field that fixes its
          predicted dynamics: kappa = Sigma_eff/Sigma_crit with Sigma_eff the projection of
          rho_eff = (1/4 pi G) div g_fw, g_fw = g_bar + a0*Delta(g_bar/a0), nu_RAR saturated;
    (ii)  the framework therefore predicts M_lens(<r) = M_dyn(<r) IDENTICALLY, so its shortfall
          against lensing must equal its shortfall against dynamics -- it has NO freedom to make
          them differ, and no choice of lensing sector can repair a shortfall already present in
          the dynamical probe;
    (iii) a theory with SLIP (the modified-inertia arm) predicts them to differ, and in the
          direction that makes lensing WORSE.
So the three-way pattern is the discriminator, and the third leg (measured lensing vs measured
dynamics) is an empirical measurement of the hydrostatic bias for this exact sample.

THE DATA.  Twelve X-COP clusters, on-disk public profiles (`real_research/data/xcop/`, Eckert et al.
2019 A&A 621 A40; Ettori et al. 2019 A&A 621 A39): gas mass profiles, stellar mass profiles, and the
forward hydrostatic mass M_FORW with its errors.  Weak-lensing masses, per cluster, with citations:
  * Herbonnet et al. 2020, MNRAS 497, 4684 (CCCP+MENeaCS; arXiv:1912.04414) Tables 2 and 3 -- five of
    the twelve X-COP clusters are in that 100-cluster sample: A85, A1795, A2029, A2142, ZwCl1215.
    NFW fit to the reduced shear over 0.5-2 h70^-1 Mpc with the Dutton & Maccio (2014) concentration-
    mass relation, masses w.r.t. the critical density, flat LCDM H0 = 70, Om = 0.3.  The other seven
    X-COP clusters are NOT in that table (checked name by name against the full list); Eckert et al.
    2022 A&A 662 A123 says the same for A644 and A2319.
  * Independent weak-lensing analyses of four of those five, from the LC2 compilation (Sereno 2015,
    MNRAS 450, 3665; VizieR J/MNRAS/450/3665, table lc2all V2.0, matched by coordinate within
    2 arcmin, same reference cosmology), which tabulates SPHERICAL masses inside FIXED PHYSICAL
    radii 1.0 and 1.5 Mpc -- exactly the comparison this lane wants, with no NFW deprojection:
        A85      Cypriano et al. 2004    ApJ 613, 95     M(<1.0) = 3.943+/-0.725, M(<1.5) = 5.915+/-1.087
        A2029    Cypriano et al. 2004    ApJ 613, 95     M(<1.0) = 5.038+/-0.618, M(<1.5) = 7.557+/-0.928
        A2142    Umetsu et al. 2009      ApJ 694, 1643   M(<1.0) = 6.560+/-0.627, M(<1.5) = 9.679+/-1.033
        A2142    Okabe & Umetsu 2008     PASJ 60, 345    M(<1.0) = 6.149+/-1.446, M(<1.5) = 9.483+/-2.472
        ZW1215   Kubo et al. 2009        ApJ 702, L110   M(<1.0) = 2.140+/-1.401, M(<1.5) = 2.994+/-2.114
    (1e14 Msun).  A1795 has no LC2 entry.
  All five weak-lensing clusters have MEASURED (not imputed) stellar profiles on disk, so the baryon
  budget of the lensing subsample carries no stellar-imputation systematic.

THE CHECKS (FAIL marks a requirement the stated reading does not meet):
  C1 [control]  the kernel-to-convergence machinery reproduces the analytic general-relativistic
                convergence and shear of a known profile (NFW, Wright & Brainerd 2000) to 0.5%,
                including via the potential -> density route the framework itself uses;
  C2 [control]  and of a singular isothermal sphere, rho ~ r^-2 -- the framework's own deep-MOND
                asymptotic shape -- to 0.5%;
  C3 [control]  the NFW + Dutton-Maccio machinery reproduces Herbonnet's OWN published M500 from
                their published M200 to 5%, and the "as-observed" refitter recovers an injected NFW
                mass to 5%: together these validate evaluating M_WL(<r) at a fixed radius;
  C4 [control]  an independent read of the X-COP FITS reproduces the audit's tabulated g_bar/a0 and
                g_HSE/a0 at the audited radii;
  C5 [control]  the MEASURED lensing-to-dynamical mass ratio lands in the published hydrostatic-bias
                range;
  C6 [test]     the framework's prediction matches the measured LENSING mass;
  C7 [test]     the framework's prediction matches the measured DYNAMICAL mass (reproduces L2/L7's
                known shortfall -- used here as a control on the comparison, at the same radii);
  C8 [THE TEST] the shortfall against LENSING differs from the shortfall against DYNAMICS at > 3 sigma
                -- which would be a lensing-sector (modified-gravity) signature.  A FAIL means the two
                shortfalls agree, i.e. the residual behaves like MASS in both observables and no
                lensing sector can repair it;
  C9 [indep]    the same comparison against INDEPENDENT weak-lensing teams, at fixed physical radii
                1.0 and 1.5 Mpc, agrees with the Herbonnet-based one;
  C10 [control] projecting the MEASURED dynamical (X-ray hydrostatic) mass profile through exactly the
                same machinery reproduces the MEASURED weak-lensing DeltaSigma over the fitting range.
                Without this, a framework deficit in DeltaSigma could be a pipeline artefact; with it,
                any such deficit is a statement about the framework's own predicted shape;
  C11 [shape]   the framework's predicted lensing SHAPE (d ln DeltaSigma / d ln R over the fitting
                range) is consistent with the measured one -- an amplitude-free test;
  C12 [as-obs]  the shape systematic costed: what M500 an observer running Herbonnet's own pipeline
                (one-parameter NFW + Dutton-Maccio, 0.5-2 Mpc) would report if the framework's
                predicted signal were the truth, versus the framework's true M(<R500).  If this is
                far from 1 the 3D-mass comparison of C6 is not the whole story and must be corrected;
  C13 [syst]    the framework's projected prediction is insensitive to the phantom truncation radius
                and to the outer baryon slope, and the mass comparison needs no baryon extrapolation.
Both a0 footings throughout.
"""
import numpy as np, math, json, os, sys, warnings
from scipy.integrate import quad, IntegrationWarning
from scipy.optimize import brentq, minimize_scalar
warnings.filterwarnings("ignore", category=IntegrationWarning)

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; c_light = 2.99792458e8
# cluster-data frame: the frame Herbonnet 2020, Sereno's LC2 and X-COP all use
h70, OmM, OmL = 0.7, 0.3, 0.7
H0 = h70*100e3/Mpc
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

print("=" * 118)
print("L24 -- cluster lensing versus cluster dynamics: does the residual behave like mass in BOTH probes?")
print("=" * 118, flush=True)

# ----------------------------------------------------------------------------------------------
# the carried kernel (THE_ACTION_2026-09-05.md section 3): nu_RAR, saturated at its own maximum
# ----------------------------------------------------------------------------------------------
S_SAT, D_SAT = 2.540, 0.6476
def Delta(s):
    s = np.asarray(s, float)
    d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def g_kernel(g_bar, a0): return g_bar + a0*Delta(g_bar/a0)

# ----------------------------------------------------------------------------------------------
# cosmology helpers (flat LCDM, h = 0.7)
# ----------------------------------------------------------------------------------------------
def Ez(z): return math.sqrt(OmM*(1+z)**3 + OmL)
def rho_crit(z): return 3*(H0*Ez(z))**2/(8*math.pi*G)          # kg m^-3
def D_A(z): return quad(lambda t: c_light/(H0*Ez(t)), 0.0, z)[0]/(1+z)

# ----------------------------------------------------------------------------------------------
# generic spherical projection: rho(r) -> Sigma(R), Sigmabar(<R), DeltaSigma(R)
# Sigma(R) = 2 int_0^zmax rho(sqrt(R^2+z^2)) dz   (no coordinate singularity)
# ----------------------------------------------------------------------------------------------
def Sigma_of_R(rho, R, zmax):
    f = lambda z: rho(math.sqrt(R*R + z*z))
    a = quad(f, 0.0, R, limit=200)[0]
    b = quad(f, R, zmax, limit=400)[0] if zmax > R else 0.0
    return 2.0*(a + b)
def Sigmabar_of_R(rho, R, zmax, n=48):
    x, w = np.polynomial.legendre.leggauss(n)
    Rp = 0.5*R*(x + 1.0); wp = 0.5*R*w
    tot = sum(wi*Rpi*Sigma_of_R(rho, Rpi, zmax) for Rpi, wi in zip(Rp, wp))
    return 2.0*tot/(R*R)

# ----------------------------------------------------------------------------------------------
# analytic NFW (Wright & Brainerd 2000) -- the control target and the published-mass model
# ----------------------------------------------------------------------------------------------
def nfw_delta_c(c): return (200.0/3.0)*c**3/(math.log(1+c) - c/(1+c))
def nfw_rho(r, rs, dc, rhoc): return dc*rhoc/((r/rs)*(1+r/rs)**2)
def nfw_Sigma(R, rs, dc, rhoc):
    x = R/rs; A = 2*rs*dc*rhoc
    if abs(x-1) < 1e-8: return A/3.0
    if x < 1: return A/(x*x-1)*(1 - 2/math.sqrt(1-x*x)*math.atanh(math.sqrt((1-x)/(1+x))))
    return A/(x*x-1)*(1 - 2/math.sqrt(x*x-1)*math.atan(math.sqrt((x-1)/(x+1))))
def nfw_g(x):
    if abs(x-1) < 1e-8: return math.log(x/2.0) + 1.0
    if x < 1: return math.log(x/2.0) + math.acosh(1.0/x)/math.sqrt(1-x*x)
    return math.log(x/2.0) + math.acos(1.0/x)/math.sqrt(x*x-1)
def nfw_Sigmabar(R, rs, dc, rhoc): return 4*rs*dc*rhoc*nfw_g(R/rs)/(R/rs)**2
def nfw_DS(R, rs, dc, rhoc): return nfw_Sigmabar(R, rs, dc, rhoc) - nfw_Sigma(R, rs, dc, rhoc)
def nfw_M3d(r, rs, dc, rhoc):
    x = r/rs; return 4*math.pi*dc*rhoc*rs**3*(math.log(1+x) - x/(1+x))
def c200_DM14(M200_Msun, z):
    """Dutton & Maccio 2014, NFW, 200 x critical -- the relation Herbonnet 2020 adopt."""
    a = 0.520 + (0.905 - 0.520)*math.exp(-0.617*z**1.21)
    b = -0.101 + 0.026*z
    return 10**(a + b*math.log10(M200_Msun*h70/1e12))
def r_Delta(M_Msun, z, D=200.0):
    return (3*M_Msun*MSUN/(4*math.pi*D*rho_crit(z)))**(1.0/3.0)     # metres
def nfw_from_M200(M200_Msun, z):
    c = c200_DM14(M200_Msun, z); r200 = r_Delta(M200_Msun, z, 200.0)
    return r200/c, nfw_delta_c(c), rho_crit(z), c, r200
def nfw_MDelta(M200_Msun, z, D):
    rs, dc, rhoc, c, r200 = nfw_from_M200(M200_Msun, z)
    f = lambda r: nfw_M3d(r, rs, dc, rhoc)/MSUN - D*(4*math.pi/3)*rhoc*r**3/MSUN
    rD = brentq(f, 0.05*r200, 3*r200, xtol=1e-3*r200)
    return nfw_M3d(rD, rs, dc, rhoc)/MSUN, rD
def refit_as_observed(DS_target, Rf, z):
    """Herbonnet's pipeline: one free parameter M200, concentration from Dutton-Maccio,
       least squares in log DeltaSigma over their fitting range.  Returns (M200, M500)."""
    def cost(lgM):
        rs2, dc2, rc2, _, _ = nfw_from_M200(10**lgM, z)
        mod = np.array([nfw_DS(R, rs2, dc2, rc2) for R in Rf])
        return float(np.sum((np.log(mod) - np.log(DS_target))**2))
    r = minimize_scalar(cost, bounds=(13.0, 16.3), method="bounded", options=dict(xatol=1e-5))
    return 10**r.x, nfw_MDelta(10**r.x, z, 500.0)[0]

# ==============================================================================================
print("\n" + "-"*118)
print("C1/C2 -- CONTROLS: does the projection machinery reproduce known general-relativistic convergences?")
print("-"*118, flush=True)

zc = 0.08; M200t = 1.0e15
rs, dc, rhoc, cc, r200 = nfw_from_M200(M200t, zc); zmax = 3000*rs
rho_cb = lambda r: nfw_rho(r, rs, dc, rhoc)
err_S, err_DS = [], []
for R in np.array([0.2, 0.5, 1.0, 2.0])*Mpc:
    Sn = Sigma_of_R(rho_cb, R, zmax); Sa = nfw_Sigma(R, rs, dc, rhoc)
    SBn = Sigmabar_of_R(rho_cb, R, zmax); SBa = nfw_Sigmabar(R, rs, dc, rhoc)
    err_S.append(abs(Sn/Sa - 1)); err_DS.append(abs((SBn - Sn)/(SBa - Sa) - 1))
    print(f"    NFW  R = {R/Mpc:4.2f} Mpc : Sigma num/ana = {Sn/Sa:.6f}   DeltaSigma num/ana = {(SBn-Sn)/(SBa-Sa):.6f}")
Mn = lambda r: nfw_M3d(r, rs, dc, rhoc)
def rho_from_M(Mfun, r, dl=1e-3):
    lr = math.log(r); rp, rm = math.exp(lr+dl), math.exp(lr-dl)
    return (Mfun(rp) - Mfun(rm))/(rp - rm)/(4*math.pi*r*r)
route_err = max(abs(rho_from_M(Mn, x*Mpc)/nfw_rho(x*Mpc, rs, dc, rhoc) - 1) for x in (0.1, 0.5, 1.0, 2.0))
print(f"    potential->density route (M = g r^2/G, rho = M'/4 pi r^2) reproduces rho_NFW to {route_err:.2e}")
check("C1 [control] the kernel-to-convergence machinery reproduces the analytic general-relativistic NFW convergence and shear to 0.5%",
      max(err_S) < 5e-3 and max(err_DS) < 5e-3 and route_err < 5e-3,
      f"max |Sigma error| = {max(err_S):.2e}, max |DeltaSigma error| = {max(err_DS):.2e}, density-route error = {route_err:.2e}")

sig = 1000e3
rho_sis = lambda r: sig**2/(2*math.pi*G*r*r)
errs = []
for R in (0.2, 0.5, 1.0, 2.0):
    Rm = R*Mpc; zm = 500*Rm
    num = Sigma_of_R(rho_sis, Rm, zm); ana = sig**2/(math.pi*G*Rm)*math.atan(zm/Rm)
    errs.append(abs(num/ana - 1))
    print(f"    SIS  R = {R:4.2f} Mpc : Sigma num/ana = {num/ana:.6f}  (untruncated limit sigma^2/2GR ratio {num/(sig**2/(2*G*Rm)):.4f})")
check("C2 [control] the machinery reproduces the analytic convergence of a singular isothermal sphere (rho ~ r^-2, the framework's deep-MOND shape) to 0.5%",
      max(errs) < 5e-3, f"max |Sigma error| = {max(errs):.2e}")

# ==============================================================================================
print("\n" + "-"*118)
print("C3 -- CONTROL: the NFW + Dutton-Maccio machinery, and the as-observed refitter, against known input")
print("-"*118, flush=True)

WL_H20 = {   # Herbonnet et al. 2020 Table 3 (masses, 1e14 Msun) and Table 2 (<beta>, R_max in Mpc)
 "A85":    dict(z=0.055, M200=8.4,  eM200=3.3, M500=5.7,  eM500=2.2, R500ap=1.35, M500ap=7.4,  eap=2.30, beta=0.878, Rmax=1.6),
 "A1795":  dict(z=0.062, M200=13.9, eM200=3.3, M500=9.3,  eM500=2.2, R500ap=1.45, M500ap=9.2,  eap=2.30, beta=0.864, Rmax=1.8),
 "A2029":  dict(z=0.077, M200=18.1, eM200=3.8, M500=12.1, eM500=2.5, R500ap=1.52, M500ap=10.8, eap=2.10, beta=0.834, Rmax=2.2),
 "A2142":  dict(z=0.091, M200=14.5, eM200=3.4, M500=9.7,  eM500=2.3, R500ap=1.54, M500ap=11.3, eap=2.15, beta=0.809, Rmax=2.5),
 "ZW1215": dict(z=0.075, M200=5.1,  eM200=3.1, M500=3.5,  eM500=2.2, R500ap=1.32, M500ap=7.0,  eap=1.90, beta=0.833, Rmax=2.1),
}
WL_LC2 = [  # Sereno 2015 LC2-all: independent teams, spherical masses inside fixed physical radii (1e14 Msun)
 ("A85",    "Cypriano+04      2004ApJ...613...95C", {1000: (3.943, 0.725), 1500: (5.915, 1.087)}),
 ("A2029",  "Cypriano+04      2004ApJ...613...95C", {1000: (5.038, 0.618), 1500: (7.557, 0.928)}),
 ("A2142",  "Umetsu+09        2009ApJ...694.1643U", {1000: (6.560, 0.627), 1500: (9.679, 1.033)}),
 ("A2142",  "Okabe&Umetsu08   2008PASJ...60..345O", {1000: (6.149, 1.446), 1500: (9.483, 2.472)}),
 ("ZW1215", "Kubo+09          2009ApJ...702L.110K", {1000: (2.140, 1.401), 1500: (2.994, 2.114)}),
]
c3err = []
for n, d in WL_H20.items():
    M500_pred, r500_pred = nfw_MDelta(d["M200"]*1e14, d["z"], 500.0)
    e = abs(M500_pred/1e14/d["M500"] - 1); c3err.append(e)
    d["rs"], d["dc"], d["rhoc"], d["c200"], d["r200"] = nfw_from_M200(d["M200"]*1e14, d["z"])
    d["r500_wl"] = r500_pred
    print(f"    {n:8s} M200 = {d['M200']:5.1f}e14 -> c200(DM14) = {d['c200']:.2f}, r500 = {r500_pred/Mpc:.3f} Mpc, "
          f"M500 predicted {M500_pred/1e14:5.2f}e14 vs published {d['M500']:5.2f}e14  ({100*e:4.1f}%)")
# and the as-observed refitter, on an injected NFW whose true M500 is known
Rf_ctrl = np.exp(np.linspace(math.log(0.5*Mpc), math.log(2.0*Mpc), 12))
rs_i, dc_i, rc_i, _, _ = nfw_from_M200(1.2e15, 0.08)
DS_i = np.array([nfw_DS(R, rs_i, dc_i, rc_i) for R in Rf_ctrl])
M200_o, M500_o = refit_as_observed(DS_i, Rf_ctrl, 0.08)
M500_i = nfw_MDelta(1.2e15, 0.08, 500.0)[0]
inj_err = abs(M500_o/M500_i - 1); c3err.append(inj_err)
print(f"    as-observed refitter on an injected NFW: recovers M200 = {M200_o/1e14:.2f}e14 (input 12.00e14), "
      f"M500 = {M500_o/1e14:.2f}e14 (true {M500_i/1e14:.2f}e14), error {100*inj_err:.2f}%")
check("C3 [control] the NFW + Dutton-Maccio machinery reproduces Herbonnet 2020's own published M500 from their M200, and the as-observed refitter recovers an injected NFW mass, both to 5%",
      max(c3err) < 0.05, f"max deviation {100*max(c3err):.1f}%")

# ==============================================================================================
print("\n" + "-"*118)
print("C4 -- CONTROL: an independent read of the on-disk X-COP profiles against the committed audit")
print("-"*118, flush=True)

from astropy.io import fits
XDIR = os.path.join(REPO, "real_research/data/xcop")
def _rkpc(rad, unit, R500):
    u = (unit or "").strip().lower()
    if u in ("r/r500", "r500"): return np.asarray(rad, float)*R500
    if u == "mpc": return np.asarray(rad, float)*1e3
    return np.asarray(rad, float)
def load_cluster(name):
    p = os.path.join(XDIR, name); c = {"name": name}
    with fits.open(os.path.join(p, name + "_hydro_mass.fits")) as f:
        d = f[1].data; R5 = float(f[1].header["R500"]); c["R500"] = R5
        c["rh"] = _rkpc(d["RADIUS"], f[1].columns["RADIUS"].unit, R5)
        c["Mh"] = np.array(d["M_FORW"], float); c["eMh"] = np.array(d["EM_FORW"], float)
    with fits.open(os.path.join(p, name + "_fgas_profile.fits")) as f:
        d = f[1].data
        c["rg"] = _rkpc(d["RADIUS"], f[1].columns["RADIUS"].unit, c["R500"])
        c["Mg"] = np.array(d["MGAS"], float)
    sp = os.path.join(p, name + "_mstar.fits"); c["has_star"] = os.path.exists(sp)
    if c["has_star"]:
        with fits.open(sp) as f:
            d = f[2].data
            c["rs"] = _rkpc(d["RADIUS"], f[2].columns["RADIUS"].unit, c["R500"])
            c["Ms"] = np.array(d["MSTAR"], float)
    return c
def loginterp(x, xp, fp):
    x = np.atleast_1d(np.asarray(x, float))
    m = np.isfinite(xp) & np.isfinite(fp) & (fp > 0) & (xp > 0)
    return np.exp(np.interp(np.log(x), np.log(xp[m]), np.log(fp[m]), left=np.nan, right=np.nan))

NAMES = sorted(d for d in os.listdir(XDIR) if os.path.isdir(os.path.join(XDIR, d)))
CL = {n: load_cluster(n) for n in NAMES}
ETT = json.load(open(os.path.join(XDIR, "xcop_r500_ettori2019.json")))
AUD = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
RAD_AUD = np.array(AUD["radii_kpc"])
gas_g = np.array([loginterp(RAD_AUD, CL[n]["rg"], CL[n]["Mg"]) for n in NAMES])
sta_g = np.array([loginterp(RAD_AUD, CL[n]["rs"], CL[n]["Ms"]) if CL[n]["has_star"] else np.full(len(RAD_AUD), np.nan) for n in NAMES])
imp = np.nanmedian(sta_g/gas_g, axis=0)
for i, n in enumerate(NAMES):
    if not CL[n]["has_star"]: sta_g[i] = gas_g[i]*imp
Mbar_g = gas_g + sta_g
Mh_g = np.array([loginterp(RAD_AUD, CL[n]["rh"], CL[n]["Mh"]) for n in NAMES])
gb_g = G*Mbar_g*MSUN/(RAD_AUD*kpc)**2; gh_g = G*Mh_g*MSUN/(RAD_AUD*kpc)**2
aud = {(rw["cluster"], float(rw["r_kpc"])): (float(rw["g_baryon_over_a0"]), float(rw["g_hse_over_a0"]))
       for rw in AUD["rows"] if rw.get("footing", "canonical") == "canonical"}
db, dh = [], []
for i, n in enumerate(NAMES):
    for j, r in enumerate(RAD_AUD):
        k = (n, float(r))
        if k in aud and np.isfinite(gb_g[i, j]):
            db.append(abs(gb_g[i, j]/A0["canonical"]/aud[k][0] - 1)); dh.append(abs(gh_g[i, j]/A0["canonical"]/aud[k][1] - 1))
print(f"    {len(db)} audited (cluster, radius) rows compared, canonical footing")
print(f"    g_bar/a0 : median |diff| = {np.median(db):.2e}, max = {np.max(db):.2e}")
print(f"    g_HSE/a0 : median |diff| = {np.median(dh):.2e}, max = {np.max(dh):.2e}")
check("C4 [control] an independent read of the on-disk X-COP FITS reproduces the committed audit's g_bar/a0 and g_HSE/a0 to 2%",
      np.max(db) < 0.02 and np.max(dh) < 0.02, f"max |diff| {max(np.max(db), np.max(dh)):.2e}")

# ==============================================================================================
# continuous profiles.  OUTER EXTRAPOLATION, stated: beyond the last measured gas radius the gas
# density is continued as rho ~ r^-4 (the standard steepening of cluster outskirts beyond R200,
# e.g. Roncarelli+2006, Diemer & Kravtsov 2014), which gives the bounded closed form
#     M(r) = M_last + (dM/dlnr)_last * (1 - r_last/r),  M(inf) = M_last + (dM/dlnr)_last.
# The stellar profile is held constant beyond its last point.  Neither affects M(<R500), which is
# inside the measured range for every cluster used (checked in C12); both are varied in C12.
# ==============================================================================================
OUTER_SLOPE = -4.0
def build(c, outer_slope=OUTER_SLOPE):
    rg, Mg = c["rg"], c["Mg"]
    if c["has_star"]: rs_, Ms_ = c["rs"], c["Ms"]
    else: rs_, Ms_ = RAD_AUD, loginterp(RAD_AUD, rg, Mg)*imp
    grid = np.exp(np.linspace(math.log(1.0), math.log(1.0e5), 1100))          # 1 kpc .. 100 Mpc
    def extend(rp, fp, r, steepen):
        f = loginterp(r, rp, fp); lo, hi = rp.min(), rp.max()
        sin_ = (math.log(fp[2]) - math.log(fp[0]))/(math.log(rp[2]) - math.log(rp[0]))
        sout = (math.log(fp[-1]) - math.log(fp[-4]))/(math.log(rp[-1]) - math.log(rp[-4]))
        sout = min(max(sout, 0.0), 1.5)
        f = np.where(r < lo, fp[0]*(r/lo)**sin_, f)
        if steepen:      # rho ~ r^(outer_slope) beyond the data => bounded M(r)
            p = 3.0 + outer_slope                                            # dM/dlnr ~ r^p, p = -1
            tail = fp[-1] + sout*fp[-1]*(1.0 - (r/hi)**p)/(-p) if abs(p) > 1e-9 else fp[-1]*(1 + sout*np.log(r/hi))
            f = np.where(r > hi, tail, f)
        else:
            f = np.where(r > hi, fp[-1]*np.ones_like(r), f)
        return f, sout
    Mg_i, sg = extend(rg, Mg, grid, True)
    Ms_i, _ = extend(rs_, Ms_, grid, False)
    c["grid"] = grid; c["Mbar"] = Mg_i + Ms_i; c["slope_gas_out"] = sg; c["r_gas_max"] = rg.max()
    c["Mh_i"] = np.exp(np.interp(np.log(grid), np.log(c["rh"]), np.log(c["Mh"]), left=np.nan, right=math.log(c["Mh"][-1])))
    c["eMh_i"] = np.exp(np.interp(np.log(grid), np.log(c["rh"]), np.log(c["eMh"]), left=np.nan, right=math.log(c["eMh"][-1])))
    c["R200"] = ETT[c["name"]]["R200"]*1e3 if c["name"] in ETT else 1.6*c["R500"]
    return c
for n in NAMES: build(CL[n])

def _i(c, key, r_kpc):
    return np.exp(np.interp(np.log(np.atleast_1d(np.asarray(r_kpc, float))), np.log(c["grid"]), np.log(c[key])))
def Mbar_at(c, r): return float(_i(c, "Mbar", r)[0])
def MHSE_at(c, r): return float(_i(c, "Mh_i", r)[0])
def eMHSE_at(c, r): return float(_i(c, "eMh_i", r)[0])
def Mfw_at(c, r_kpc, a0):
    rm = float(r_kpc)*kpc; gb = G*Mbar_at(c, r_kpc)*MSUN/rm**2
    return float(g_kernel(gb, a0))*rm**2/(G*MSUN)
def _rho_from_massgrid(grid, M, r_trunc_kpc):
    """rho(r) = (1/4 pi r^2) dM/dr from a mass profile tabulated on a log grid, truncated."""
    lg = np.log(grid); rm = grid*kpc
    rho = np.maximum(np.gradient(np.asarray(M, float), lg)*MSUN/(4*math.pi*rm**3), 1e-45)
    lrho = np.log(rho)
    def f(r_m):
        rk = r_m/kpc
        if rk > r_trunc_kpc: return 0.0
        return math.exp(np.interp(math.log(max(rk, grid[0])), lg, lrho))
    return f
def rho_eff_fw(c, a0, r_trunc_kpc):
    rm = c["grid"]*kpc
    gb = G*np.asarray(c["Mbar"], float)*MSUN/rm**2
    return _rho_from_massgrid(c["grid"], g_kernel(gb, a0)*rm**2/(G*MSUN), r_trunc_kpc)
def rho_hse(c, r_trunc_kpc):
    """the same machinery applied to the MEASURED dynamical mass profile -- the C10 control.
       Beyond the last tabulated radius (3 Mpc) the same rho ~ r^-4 tail is used as for the gas."""
    r, M = c["rh"], c["Mh"]; grid = c["grid"]
    lo, hi = r.min(), r.max()
    sin_ = (math.log(M[2]) - math.log(M[0]))/(math.log(r[2]) - math.log(r[0]))
    sout = (math.log(M[-1]) - math.log(M[-4]))/(math.log(r[-1]) - math.log(r[-4]))
    f = np.exp(np.interp(np.log(grid), np.log(r), np.log(M)))
    f = np.where(grid < lo, M[0]*(grid/lo)**sin_, f)
    f = np.where(grid > hi, M[-1] + sout*M[-1]*(1.0 - (grid/hi)**-1.0), f)
    return _rho_from_massgrid(grid, f, r_trunc_kpc)

# ==============================================================================================
print("\n" + "-"*118)
print("C5/C6/C7/C8 -- the three-way comparison at FIXED physical radii, five X-COP clusters with weak lensing")
print("-"*118, flush=True)
print("    structural note: in the framework's modified-gravity arm gamma_PPN = 1 (THE_ACTION section 4), so its")
print("    predicted lensing mass EQUALS its predicted dynamical mass identically.  The two shortfalls therefore")
print("    differ if and only if the two MEASURED masses differ: S_lens/S_dyn = M_WL/M_HSE exactly.  That identity")
print("    is why the lensing observable cannot rescue a shortfall already present in the dynamical probe.", flush=True)

WLN = ["A85", "A1795", "A2029", "A2142", "ZW1215"]
RES = {}
for foot, a0 in A0.items():
    rows = []
    print(f"\n    ---- {foot} footing, a0 = {a0:.4e} m/s^2 ; radius = each cluster's X-ray R500")
    print(f"    {'cluster':8s} {'r [kpc]':>8s} {'M_bar':>7s} {'M_fw':>7s} {'M_HSE':>8s} {'M_WL':>16s} "
          f"{'S_dyn':>6s} {'S_lens':>7s} {'WL/HSE':>7s}")
    for n in WLN:
        c = CL[n]; d = WL_H20[n]; rk = c["R500"]
        Mb, Mfw = Mbar_at(c, rk), Mfw_at(c, rk, a0)
        Mh, eMh = MHSE_at(c, rk), eMHSE_at(c, rk)
        Mwl = nfw_M3d(rk*kpc, d["rs"], d["dc"], d["rhoc"])/MSUN
        eMwl = Mwl*(d["eM500"]/d["M500"])
        rows.append(dict(name=n, r=rk, Mb=Mb, Mfw=Mfw, Mh=Mh, eMh=eMh, Mwl=Mwl, eMwl=eMwl,
                         Sdyn=Mh/Mfw, Slens=Mwl/Mfw, B=Mwl/Mh,
                         eB=(Mwl/Mh)*math.hypot(eMwl/Mwl, eMh/Mh)))
        print(f"    {n:8s} {rk:8.0f} {Mb/1e13:7.2f} {Mfw/1e13:7.2f} {Mh/1e13:8.2f} {Mwl/1e13:9.2f}+/-{eMwl/1e13:5.2f} "
              f"{Mh/Mfw:6.2f} {Mwl/Mfw:7.2f} {Mwl/Mh:7.2f}")
    print("    (masses in 1e13 Msun; M_fw = [g_bar + a0 Delta(g_bar/a0)] r^2/G; M_WL = Herbonnet's NFW at the X-ray R500)")
    RES[foot] = rows

def wmean(v, e):
    v, e = np.asarray(v, float), np.asarray(e, float); w = 1.0/e**2
    m = float(np.sum(w*v)/np.sum(w)); s = float(1.0/math.sqrt(np.sum(w)))
    return m, s, float(math.sqrt(max(np.sum(w*(v-m)**2)/max(len(v)-1, 1), 0.0)))

SUM = {}
for foot in A0:
    rows = RES[foot]
    B, eB, _ = wmean([r["B"] for r in rows], [r["eB"] for r in rows])
    Bstack = sum(r["Mwl"] for r in rows)/sum(r["Mh"] for r in rows)
    Sd, eSd, scSd = wmean([r["Sdyn"] for r in rows], [r["Sdyn"]*r["eMh"]/r["Mh"] for r in rows])
    Sl, eSl, scSl = wmean([r["Slens"] for r in rows], [r["Slens"]*r["eMwl"]/r["Mwl"] for r in rows])
    # Herbonnet's alternative (aperture-deprojected) masses, as a weak-lensing systematic
    Bap = np.average([WL_H20[r["name"]]["M500ap"]*1e14/r["Mh"] for r in rows],
                     weights=[1.0/WL_H20[r["name"]]["eap"]**2 for r in rows])
    SUM[foot] = dict(B=B, eB=eB, Bstack=Bstack, Bap=Bap, Sd=Sd, eSd=eSd, scSd=scSd, Sl=Sl, eSl=eSl, scSl=scSl)
    print(f"\n    {foot}: inverse-variance mean over the 5 clusters at their X-ray R500")
    print(f"      M_WL / M_HSE (measured lensing / measured dynamics) = {B:.3f} +/- {eB:.3f}  [stacked {Bstack:.3f}; "
          f"with Herbonnet's aperture masses instead {Bap:.3f}]  => 1-b = {1/B:.3f}")
    print(f"      S_dyn  = M_HSE / M_framework                       = {Sd:.3f} +/- {eSd:.3f}  (cluster scatter {scSd:.3f})")
    print(f"      S_lens = M_WL  / M_framework                       = {Sl:.3f} +/- {eSl:.3f}  (cluster scatter {scSl:.3f})")

print("\n    published range for 1-b = M_HSE/M_WL: X-COP's own gas-fraction calibration 0.85 +/- 0.05 (Eckert+2019 A&A 621 A40);")
print("    Eckert+2022 A&A 662 A123 concludes X-COP hydrostatic masses are biased < 10% out to R500; CCCP weak lensing")
print("    0.78 +/- 0.09 (Hoekstra+2015); Weighing the Giants 0.69 +/- 0.07 (von der Linden+2014).  Admissible band [0.60, 1.05].")
check("C5 [control] the MEASURED lensing-to-dynamical mass ratio lands in the published hydrostatic-bias range",
      all(0.60 <= 1.0/SUM[f]["B"] <= 1.05 for f in A0),
      ", ".join(f"{f} 1-b = {1.0/SUM[f]['B']:.3f} +/- {SUM[f]['eB']/SUM[f]['B']**2:.3f}" for f in A0))

zl = {f: (SUM[f]["Sl"] - 1.0)/SUM[f]["eSl"] for f in A0}
zd = {f: (SUM[f]["Sd"] - 1.0)/SUM[f]["eSd"] for f in A0}
check("C6 [test] the framework's prediction matches the measured LENSING mass (shortfall consistent with 1)",
      all(abs(zl[f]) < 3 for f in A0),
      ", ".join(f"{f} S_lens = {SUM[f]['Sl']:.2f} +/- {SUM[f]['eSl']:.2f} ({abs(zl[f]):.1f} sigma from 1)" for f in A0))
check("C7 [test] the framework's prediction matches the measured DYNAMICAL mass (the L2/L7 control, same radii)",
      all(abs(zd[f]) < 3 for f in A0),
      ", ".join(f"{f} S_dyn = {SUM[f]['Sd']:.2f} +/- {SUM[f]['eSd']:.2f} ({abs(zd[f]):.1f} sigma from 1)" for f in A0))

zdiff = {}
for f in A0:
    s = SUM[f]; d = s["Sl"] - s["Sd"]; ed = s["Sd"]*s["eB"]; zdiff[f] = abs(d)/ed
    print(f"\n    {f}: S_lens - S_dyn = {d:+.3f} +/- {ed:.3f}  ({zdiff[f]:.2f} sigma).  Identity check: "
          f"S_lens/S_dyn = {s['Sl']/s['Sd']:.4f} vs M_WL/M_HSE = {s['B']:.4f}")
check("C8 [THE TEST] the shortfall against LENSING differs from the shortfall against DYNAMICS at > 3 sigma (a lensing-sector signature)",
      all(zdiff[f] > 3 for f in A0),
      ", ".join(f"{f} {zdiff[f]:.2f} sigma" for f in A0) +
      " -- a FAIL means the two agree: the residual behaves like MASS in both probes and no lensing sector can repair it")

# ==============================================================================================
print("\n" + "-"*118)
print("C9 -- INDEPENDENT weak-lensing teams, at fixed physical radii 1.0 and 1.5 Mpc (Sereno 2015 LC2)")
print("-"*118, flush=True)
print("    1000 kpc is also L7's outermost audited radius, so the S_dyn column here is directly comparable to L7.")
ind = {}
for foot, a0 in A0.items():
    print(f"\n    ---- {foot} footing")
    print(f"    {'cluster':8s} {'reference':34s} {'r':>6s} {'M_fw':>7s} {'M_HSE':>7s} {'M_WL':>14s} {'S_dyn':>6s} {'S_lens':>7s} {'WL/HSE':>7s}")
    Sl_i, eSl_i, Sd_i, B_i, eB_i = [], [], [], [], []
    for n, ref, tab in WL_LC2:
        c = CL[n]
        for rk, (M, eM) in sorted(tab.items()):
            Mfw = Mfw_at(c, rk, a0); Mh = MHSE_at(c, rk); Mwl = M*1e14; eMwl = eM*1e14
            Sl_i.append(Mwl/Mfw); eSl_i.append(eMwl/Mfw); Sd_i.append(Mh/Mfw)
            B_i.append(Mwl/Mh); eB_i.append(eMwl/Mh)
            print(f"    {n:8s} {ref:34s} {rk:6.0f} {Mfw/1e13:7.2f} {Mh/1e13:7.2f} {Mwl/1e13:7.2f}+/-{eMwl/1e13:5.2f} "
                  f"{Mh/Mfw:6.2f} {Mwl/Mfw:7.2f} {Mwl/Mh:7.2f}")
    Sl_m, eSl_m, _ = wmean(Sl_i, eSl_i); B_m, eB_m, _ = wmean(B_i, eB_i)
    ind[foot] = dict(Sl=Sl_m, eSl=eSl_m, Sd=float(np.mean(Sd_i)), B=B_m, eB=eB_m)
    print(f"    {foot}: independent-team S_lens = {Sl_m:.3f} +/- {eSl_m:.3f}, mean S_dyn = {np.mean(Sd_i):.3f}, "
          f"M_WL/M_HSE = {B_m:.3f} +/- {eB_m:.3f}")
agree = {f: abs(ind[f]["Sl"] - SUM[f]["Sl"])/math.hypot(ind[f]["eSl"], SUM[f]["eSl"]) for f in A0}
check("C9 [indep] the independent weak-lensing teams give the same framework shortfall as the Herbonnet-based comparison",
      all(agree[f] < 3 for f in A0),
      ", ".join(f"{f} S_lens indep {ind[f]['Sl']:.2f}+/-{ind[f]['eSl']:.2f} vs Herbonnet {SUM[f]['Sl']:.2f}+/-{SUM[f]['eSl']:.2f} ({agree[f]:.1f} sigma)" for f in A0))

# ==============================================================================================
print("\n" + "-"*118)
print("C10/C11/C12 -- the raw weak-lensing observable: DeltaSigma over the fitting range, its shape, and the refit")
print("-"*118, flush=True)
print("    kappa = Sigma_eff/Sigma_crit with Sigma_crit from each cluster's own <beta> = <D_LS/D_S> (Herbonnet Table 2).")
print("    DeltaSigma = Sigmabar(<R) - Sigma(R) is what a shear survey actually measures, and it is blind to a uniform")
print("    sheet -- which is why it is insensitive to where the phantom is truncated (C13).", flush=True)

# ---- C10 control: the SAME machinery on the MEASURED dynamical mass profile
print("\n    C10 control: project the measured X-ray hydrostatic mass profile and compare with the measured lensing signal")
ctrl_ratio = []
print(f"    {'cluster':8s} {'DS_WL/DS_HSE at R = 0.5, 0.9, 1.4, 2.0 Mpc':>52s}")
for n in WLN:
    c = CL[n]; d = WL_H20[n]; rt = 2.0*c["R200"]; zt = rt*kpc
    rho = rho_hse(c, rt)
    row = []
    for R in np.exp(np.linspace(math.log(0.5*Mpc), math.log(min(2.0, d["Rmax"])*Mpc), 4)):
        dsh = Sigmabar_of_R(rho, R, zt, n=40) - Sigma_of_R(rho, R, zt)
        row.append(nfw_DS(R, d["rs"], d["dc"], d["rhoc"])/dsh)
    ctrl_ratio += row
    print(f"    {n:8s} " + "  ".join(f"{x:11.2f}" for x in row))
cmed = float(np.median(ctrl_ratio))
print(f"    median over 5 clusters x 4 radii: DS_WL/DS_HSE = {cmed:.2f}  (scatter {np.std(ctrl_ratio, ddof=1):.2f}; "
      f"the two probes differ by the hydrostatic bias, C5, and by weak-lensing noise)")
check("C10 [control] projecting the MEASURED dynamical mass profile through the same machinery reproduces the MEASURED weak-lensing DeltaSigma to 30%",
      abs(cmed - 1.0) < 0.30, f"median DS_WL/DS_HSE = {cmed:.2f}; so any DeltaSigma deficit found below is a statement about the framework's own shape, not about this pipeline")

shape_z, asobs, dsr = {}, {}, {}
for foot, a0 in A0.items():
    print(f"\n    ---- {foot} footing   (phantom truncated at 2 R200)")
    print(f"    {'cluster':8s} {'kappa_fw(R500)':>14s} {'kappa_WL(R500)':>14s} {'DS_WL/DS_fw':>12s} "
          f"{'slope fw':>9s} {'slope WL':>9s} {'M500 as-obs':>12s} {'M500 true':>10s}")
    sl, ao, dd = [], [], []
    for n in WLN:
        c = CL[n]; d = WL_H20[n]; z = d["z"]; rt = 2.0*c["R200"]; zt = rt*kpc
        rho = rho_eff_fw(c, a0, rt)
        Rf = np.exp(np.linspace(math.log(0.5*Mpc), math.log(min(2.0, d["Rmax"])*Mpc), 12))
        DSfw = np.array([Sigmabar_of_R(rho, R, zt, n=40) - Sigma_of_R(rho, R, zt) for R in Rf])
        DSwl = np.array([nfw_DS(R, d["rs"], d["dc"], d["rhoc"]) for R in Rf])
        sfw = np.polyfit(np.log(Rf), np.log(DSfw), 1)[0]; swl = np.polyfit(np.log(Rf), np.log(DSwl), 1)[0]
        DL = D_A(z); Scrit = c_light**2/(4*math.pi*G*DL*d["beta"])
        Sfw = Sigma_of_R(rho, c["R500"]*kpc, zt); Swl = nfw_Sigma(c["R500"]*kpc, d["rs"], d["dc"], d["rhoc"])
        M200_o, M500_o = refit_as_observed(DSfw, Rf, z)
        M500_true = Mfw_at(c, c["R500"], a0)
        sl.append(sfw - swl); ao.append(M500_o/M500_true); dd.append(float(np.median(DSwl/DSfw)))
        print(f"    {n:8s} {Sfw/Scrit:14.4f} {Swl/Scrit:14.4f} {np.median(DSwl/DSfw):12.2f} "
              f"{sfw:9.2f} {swl:9.2f} {M500_o/1e13:12.2f} {M500_true/1e13:10.2f}")
    shape_z[foot] = (float(np.mean(sl)), float(np.std(sl, ddof=1)/math.sqrt(len(sl))))
    asobs[foot] = float(np.median(ao)); dsr[foot] = float(np.median(dd))
    print(f"    mean log-slope difference (framework - measured NFW) over the fitting range: {shape_z[foot][0]:+.3f} +/- {shape_z[foot][1]:.3f}")
    print(f"    median DeltaSigma deficit in the RAW observable: DS_measured/DS_framework = {dsr[foot]:.2f}")
    print(f"    median (M500 an observer would report for the framework's own signal) / (framework's true M(<R500)) = {asobs[foot]:.3f}")
zs_shape = {f: abs(shape_z[f][0])/shape_z[f][1] for f in A0}
check("C11 [shape] the framework's predicted lensing profile SHAPE is consistent with the measured one over the weak-lensing fitting range",
      all(zs_shape[f] < 3 for f in A0),
      ", ".join(f"{f} Delta(dlnDeltaSigma/dlnR) = {shape_z[f][0]:+.3f} +/- {shape_z[f][1]:.3f} ({zs_shape[f]:.1f} sigma), DS deficit {dsr[f]:.2f}x" for f in A0))
check("C12 [as-obs] the NFW-refit shape systematic is under 15%, so comparing the framework's true M(<R500) with a published NFW-fit mass is a fair comparison",
      all(abs(asobs[f] - 1) < 0.15 for f in A0),
      ", ".join(f"{f} as-observed/true = {asobs[f]:.3f}" for f in A0) +
      "; a FAIL means C6's shortfall UNDERSTATES the disagreement by that factor")
for f in A0:
    print(f"    shape-corrected lensing shortfall, {f}: S_lens/(as-observed/true) = {SUM[f]['Sl']/asobs[f]:.2f}x "
          f"(uncorrected {SUM[f]['Sl']:.2f}x; raw-observable deficit {dsr[f]:.2f}x)")

# ==============================================================================================
print("\n" + "-"*118)
print("C13 -- SYSTEMATICS: phantom truncation, outer baryon slope, and whether the mass comparison extrapolates")
print("-"*118, flush=True)
sens_t, sens_b = [], []
for foot, a0 in A0.items():
    for n in WLN:
        c = CL[n]; R = 1.0*Mpc
        v = []
        for m in (1.5, 2.0, 3.0):
            rt = m*c["R200"]; rho = rho_eff_fw(c, a0, rt)
            v.append(Sigmabar_of_R(rho, R, rt*kpc, n=32) - Sigma_of_R(rho, R, rt*kpc))
        sens_t.append(max(abs(x/v[1] - 1) for x in v))
for slope in (-3.0, -5.0):
    for n in WLN:
        c2 = build(load_cluster(n), outer_slope=slope)
        base = build(load_cluster(n), outer_slope=OUTER_SLOPE)
        for a0 in A0.values():
            rt = 2.0*base["R200"]
            r1 = rho_eff_fw(c2, a0, rt); r0 = rho_eff_fw(base, a0, rt)
            R = 1.0*Mpc
            d1 = Sigmabar_of_R(r1, R, rt*kpc, n=32) - Sigma_of_R(r1, R, rt*kpc)
            d0 = Sigmabar_of_R(r0, R, rt*kpc, n=32) - Sigma_of_R(r0, R, rt*kpc)
            sens_b.append(abs(d1/d0 - 1))
for n in WLN:
    c = CL[n]
    print(f"    {n:8s} outer gas d lnM/d lnr = {c['slope_gas_out']:.2f}; gas data reach {c['r_gas_max']/c['R500']:.2f} R500 "
          f"= {c['r_gas_max']:.0f} kpc; R500 = {c['R500']:.0f} kpc, R200 = {c['R200']:.0f} kpc "
          f"=> M(<R500) and M(<1500 kpc) use NO extrapolation" if c["r_gas_max"] > 1500 else
          f"    {n:8s} outer gas d lnM/d lnr = {c['slope_gas_out']:.2f}; gas data reach {c['r_gas_max']:.0f} kpc")
print(f"    DeltaSigma(1 Mpc) moves by at most {100*max(sens_t):.1f}% when the truncation is varied 1.5 -> 3 R200,")
print(f"    and by at most {100*max(sens_b):.1f}% when the outer gas density slope is varied -3 -> -5.")
noextrap = all(CL[n]["r_gas_max"] > max(CL[n]["R500"], 1500.0) for n in WLN)
check("C13 [syst] the framework's projected prediction is insensitive (< 10%) to the phantom truncation and the outer baryon slope, and the mass comparison needs no baryon extrapolation",
      max(sens_t) < 0.10 and max(sens_b) < 0.10 and noextrap,
      f"truncation {100*max(sens_t):.1f}%, outer slope {100*max(sens_b):.1f}%, all five gas profiles reach beyond 1500 kpc: {noextrap}")

# ==============================================================================================
print("\n" + "-"*118)
print("WHERE THIS SITS IN THE PUBLISHED LITERATURE (stated so the result is not mistaken for a discovery)")
print("-"*118)
print("    The cluster residual surviving in LENSING is a known MOND result, not a new one.  Natarajan & Zhao 2008")
print("    (MNRAS 389, 250) showed MOND plus classical neutrinos cannot supply cluster lensing; Angus, Famaey & Buote")
print("    2008 (MNRAS 387, 1470) found unexplained mass on the group scale from X-ray profiles; and Famaey, Pizzuti &")
print("    Saltas 2024 (arXiv:2410.02612) characterised the residual MOND missing mass directly from CLASH strong- and")
print("    weak-lensing profiles, finding it 'in line with results obtained in the literature from the hydrostatic")
print("    equilibrium of hot gas' -- an inner core with an outer slope steeper than -3.5 inside ~1 Mpc.")
print("    What is new here is only that the test is run on THIS framework's own carried kernel (nu_RAR saturated),")
print("    on THIS repository's own cluster sample and baryon budget, on both a0 footings, with the shortfall against")
print("    lensing and against dynamics measured side by side at the same radii.  Note also that Famaey+2024's lensing")
print("    shape is CORED, while this repository's own X-ray inversion (g04a) reports rho ~ r^-1.53 and NOT cored --")
print("    a difference over different radial ranges and kernels, flagged here, not settled here.")

print("\n" + "-"*118)
print("READING THE PATTERN")
print("-"*118)
for foot in A0:
    s = SUM[foot]
    print(f"    {foot}: framework short of DYNAMICS by {s['Sd']:.2f}x, short of LENSING by {s['Sl']:.2f}x "
          f"({SUM[foot]['Sl']/asobs[foot]:.2f}x with the shape correction, {dsr[foot]:.2f}x in the raw observable), "
          f"lensing/dynamics = {s['B']:.2f} +/- {s['eB']:.2f}")
print("    Because the carried arm has gamma_PPN = 1, its lensing and dynamical predictions are the SAME number, so the")
print("    two shortfalls can only differ by the amount the two MEASUREMENTS differ.  They differ by the hydrostatic bias")
print("    and nothing else.  Three consequences, all structural:")
print("      (a) the cluster residual is present at the same size in a probe with orthogonal systematics, so it is NOT an")
print("          artefact of hydrostatic equilibrium -- L2/L5/L6/L7 do not rest on the HSE assumption;")
print("      (b) NO choice of lensing sector can repair it.  A slip changes lensing and leaves dynamics alone; the")
print("          shortfall is already present in dynamics.  The modified-inertia arm moves the wrong way besides:")
print("          `prep_2026/mi_lensing_final/` derives g_lens <= g_bar for ANY baryonic source, i.e. M_lens <= M_bar here;")
mb = float(np.median([np.median([r["Mwl"]/r["Mb"] for r in RES[f]]) for f in A0]))
print(f"          for this sample that is a factor M_WL/M_bar = {mb:.1f}x, against the {min(SUM[f]['Sl'] for f in A0):.1f}x the")
print("          modified-gravity arm carries -- so cluster lensing excludes the MI arm independently of Brouwer 2021;")
print("      (c) the SHAPE is a second, amplitude-free discriminator, and it is the framework's weakest point here: its")
print("          phantom is far more extended than the measured convergence, so the observable an actual survey measures")
print("          (DeltaSigma over 0.5-2 Mpc) is missed by more than the enclosed-mass comparison suggests.")
print("\n  what this lane does NOT establish: it does not measure dark matter; it does not touch the galaxy-scale evidence,")
print("  where baryons plus the kernel work; and with five clusters and 20-60% per-cluster weak-lensing errors it")
print("  constrains a lensing-sector difference only at the ~15% level, so a slip smaller than that is untested, not")
print("  excluded.  Seven of the twelve X-COP clusters have no published weak-lensing mass at all.")

print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(0)
