#!/usr/bin/env python3
"""
L57 -- THE NONLOCAL FUNCTIONAL: the one successor L56's theorem explicitly does not cover
=========================================================================================

L56 closed the potential-depth trigger and stated the theorem that closes every SINGLE LOCAL trigger in
this theory.  It named exactly one successor its theorem does not cover:

    "A weight built on a NON-LOCAL functional that is not a function of the local field value -- for
     instance one responding to the size of the region over which the field is coherent rather than to
     the field's depth there.  That is a different object; it is not tested here and the theorem does
     not cover it."

WHY THAT IS NOT GRASPING AT STRAWS.  L56's kill is B5 + C3: the covariant carrier of a depth is
X = 1 - Q/Q0, whose zero is the COSMOLOGICAL background, so X is the TOTAL depth, additive over sources,
and "there is no LOCAL field that sees a host and not its substructure".  A functional smoothed on a
length l distinguishes a host from its substructure by SCALE rather than by depth: a galaxy is compact
against l and averages away, a cluster is extended and survives.  That is exactly the distinction L56
proved no local field can make.

THE QUESTION: can a nonlocal functional make the host/substructure distinction, and does the theory have
room for the length it needs?

THE ORDER, fixed in advance so the answer cannot drift.
  PART A  CONTROLS.  The 9 sigma shear-shape failure, L51's 8.8 -> 4.9 ceiling, the measured
          lensing-to-dynamical ratio, and -- the number this lane has to beat -- L56's convention-free
          crux, that matching the slip profile POINTWISE fixes the embedded response at 0.806 / 0.669.
          Plus the smoothing machinery itself, validated three ways.
  PART B  ADMISSIBILITY, SETTLED BEFORE ANY FITTING.  L56 B1 proved a constant deepening of Phi is an
          EXACT ISOMETRY, so no functional of the metric -- local OR NONLOCAL, at any order -- can
          measure a depth.  A nonlocal DEPTH trigger is therefore already dead and is NOT built here.
          Which nonlocal quantities survive?  Each candidate is tested, not assumed.
  PART C  THE MASTER FORMULA AND THE LENGTH.  The whole lane reduces to ONE dimensionless number: the
          suppression S by which a smoothed trigger responds less to a compact source, per unit of that
          source's own acceleration, than it does to the extended cluster.  R_embedded = (M_P/M_fw) x S
          exactly, so L56's kill is the S = 1 corner of this one.  S(l) is then measured on real
          profiles for a family of realisable kernels, and its FLOOR is derived.
  PART D  THE TWO LENGTHS.  Can the trigger's l differ from the kernel's xi, or does the action force
          them equal?  And does the theory have any length near the required one?
  PART E  PRICING THE LENGTH against what already constrains it: wide binaries, the Solar System, disc
          outskirts, X-ray groups, and the external-field effect.
  PART F  THE RUN.  Best achievable shear-shape improvement subject to every gate, as a CURVE.
  PART G  VERDICT.

HONESTY RULES, carried verbatim from L51 and L56 and held to in BOTH directions.
  * A tuned length fitted to five clusters is NOT a mechanism.  If that is what this is, the lane says so.
  * The five-cluster scatter of the required weight is noise-limited (L51 C13b) and is NOT used anywhere,
    in either direction.  Every number here is an AMPLITUDE or a structural identity.
  * Both a0 footings on every dimensional number: 9.3619e-11 / 1.1279e-10 m s^-2.
  * The halo and its NFW profile are LambdaCDM's, imported.  Nothing here says data favour this
    framework over LambdaCDM.
  * Where a choice is generous to the door it is made generously AND SAID, so that a FAIL is robust.

Nothing under closure_2026/ or the lead agent's directories is imported or executed.  The symbolic algebra
is built here in sympy.  The cluster, group and galaxy data are read directly from the on-disk public
archives (X-COP FITS, Herbonnet 2020 Tables 2-3, SPARC rotmod, Lovisari et al. 2015).
"""
import numpy as np, math, json, os, sys, glob, warnings
import sympy as sp
from scipy.integrate import quad, IntegrationWarning
warnings.filterwarnings("ignore", category=IntegrationWarning)

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

def sec(title):
    print("\n" + "=" * 118); print(title); print("=" * 118, flush=True)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; c_light = 2.99792458e8
H0 = 70e3 / Mpc; h70 = 1.0; OmM, OmL = 0.3, 0.7
H0_planck = 67.4e3 / Mpc
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
C2 = c_light ** 2
TOL_THEORY = 1e-4      # the deposited theory's own no-slip result, Phi = Psi to 1e-4 in galaxies (L11)
TOL_DATA = 0.20        # a generous EMPIRICAL galaxy-lensing tolerance on the fractional slip
CASSINI = 2.3e-5
rho_b_cosmic = 0.049 * 3 * H0_planck ** 2 / (8 * math.pi * G)

print("=" * 118)
print("L57 -- the nonlocal functional: the one successor L56's theorem does not cover")
print("=" * 118, flush=True)
print(f"    a0 footings: canonical {A0['canonical']:.4e} m/s^2, alt {A0['alt']:.4e} m/s^2")
print( "    convention: ds^2 = -(1+2 Phi) dt^2 + (1-2 Psi) dx^2;  slip s = Phi - Psi;  lensing potential")
print( "    (Phi+Psi)/2.  A slip is observable only through its GRADIENT: a constant s shifts Phi and Psi")
print( "    by equal and opposite constants and moves neither dynamics nor lensing.  That fact is what")
print( "    makes this lane's crux a gradient ratio and not an overlap.")
print(f"    cosmic mean baryon density (Planck h, Omega_b = 0.049): {rho_b_cosmic:.3e} kg/m^3")


# ==================================================================================================
sec("PART A -- CONTROLS")
# ==================================================================================================

# ---------- the carried kernel ----------
def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s / np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
def g_kernel(g_bar, a0): return g_bar + a0 * Delta(g_bar / a0)
def nu_of(g_bar, a0):                     # the kernel's boost factor  g_fw / g_bar
    g_bar = np.asarray(g_bar, float)
    return g_kernel(g_bar, a0) / np.maximum(g_bar, 1e-300)

# ---------- NFW, analytic ----------
def Ez(z): return math.sqrt(OmM * (1 + z) ** 3 + OmL)
def rho_crit(z): return 3 * (H0 * Ez(z)) ** 2 / (8 * math.pi * G)
def nfw_delta_c(cc): return (200.0 / 3.0) * cc ** 3 / (math.log(1 + cc) - cc / (1 + cc))
def nfw_rho(r, rs, dc, rhoc): return dc * rhoc / ((r / rs) * (1 + r / rs) ** 2)
def nfw_Sigma(R, rs, dc, rhoc):
    x = R / rs; A = 2 * rs * dc * rhoc
    if abs(x - 1) < 1e-8: return A / 3.0
    if x < 1: return A / (x * x - 1) * (1 - 2 / math.sqrt(1 - x * x) * math.atanh(math.sqrt((1 - x) / (1 + x))))
    return A / (x * x - 1) * (1 - 2 / math.sqrt(x * x - 1) * math.atan(math.sqrt((x - 1) / (x + 1))))
def nfw_gfun(x):
    if abs(x - 1) < 1e-8: return math.log(x / 2.0) + 1.0
    if x < 1: return math.log(x / 2.0) + math.acosh(1.0 / x) / math.sqrt(1 - x * x)
    return math.log(x / 2.0) + math.acos(1.0 / x) / math.sqrt(x * x - 1)
def nfw_Sigmabar(R, rs, dc, rhoc): return 4 * rs * dc * rhoc * nfw_gfun(R / rs) / (R / rs) ** 2
def nfw_DS(R, rs, dc, rhoc): return nfw_Sigmabar(R, rs, dc, rhoc) - nfw_Sigma(R, rs, dc, rhoc)
def nfw_M3d(r, rs, dc, rhoc):
    x = r / rs; return 4 * math.pi * dc * rhoc * rs ** 3 * (math.log(1 + x) - x / (1 + x))
def c200_DM14(M200, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M200 * h70 / 1e12))
def nfw_from_M200(M200, z):
    cc = c200_DM14(M200, z)
    r200 = (3 * M200 * MSUN / (4 * math.pi * 200.0 * rho_crit(z))) ** (1.0 / 3.0)
    return r200 / cc, nfw_delta_c(cc), rho_crit(z), cc, r200

# ---------- projection ----------
def Sigma_of_R(rho, R, zmax):
    f = lambda zz: rho(math.sqrt(R * R + zz * zz))
    a = quad(f, 0.0, R, limit=200)[0]
    b = quad(f, R, zmax, limit=400)[0] if zmax > R else 0.0
    return 2.0 * (a + b)
def Sigmabar_of_R(rho, R, zmax, n=40):
    xg, wg = np.polynomial.legendre.leggauss(n)
    Rp = 0.5 * R * (xg + 1.0); wp = 0.5 * R * wg
    return 2.0 * sum(wi * Rpi * Sigma_of_R(rho, Rpi, zmax) for Rpi, wi in zip(Rp, wp)) / (R * R)

print("\n  A1 -- CONTROL: the projection machinery against the analytic NFW convergence and shear.")
zc = 0.08
rs_c, dc_c, rhoc_c, ccc, r200c = nfw_from_M200(1.0e15, zc); zmx = 3000 * rs_c
rho_cb = lambda r: nfw_rho(r, rs_c, dc_c, rhoc_c)
eS, eD = [], []
for R in np.array([0.5, 1.0, 2.0]) * Mpc:
    Sn = Sigma_of_R(rho_cb, R, zmx); Sa = nfw_Sigma(R, rs_c, dc_c, rhoc_c)
    SBn = Sigmabar_of_R(rho_cb, R, zmx); SBa = nfw_Sigmabar(R, rs_c, dc_c, rhoc_c)
    eS.append(abs(Sn / Sa - 1)); eD.append(abs((SBn - Sn) / (SBa - Sa) - 1))
    print(f"      R = {R/Mpc:4.2f} Mpc : Sigma num/ana = {Sn/Sa:.6f}   DeltaSigma num/ana = {(SBn-Sn)/(SBa-Sa):.6f}")
check("A1 [control] the projection machinery reproduces the analytic NFW Sigma and DeltaSigma to 0.5%",
      max(eS) < 5e-3 and max(eD) < 5e-3, f"max |Sigma err| {max(eS):.2e}, max |DeltaSigma err| {max(eD):.2e}")

# ---------- the clusters ----------
from astropy.io import fits
XDIR = os.path.join(REPO, "real_research/data/xcop")
WL_H20 = {   # Herbonnet et al. 2020 MNRAS 497, 4684, Tables 2 and 3 (masses in 1e14 Msun)
 "A85":    dict(z=0.055, M200=8.4,  M500=5.7,  eM500=2.2, Rmax=1.6),
 "A1795":  dict(z=0.062, M200=13.9, M500=9.3,  eM500=2.2, Rmax=1.8),
 "A2029":  dict(z=0.077, M200=18.1, M500=12.1, eM500=2.5, Rmax=2.2),
 "A2142":  dict(z=0.091, M200=14.5, M500=9.7,  eM500=2.3, Rmax=2.5),
 "ZW1215": dict(z=0.075, M200=5.1,  M500=3.5,  eM500=2.2, Rmax=2.1),
}
WLN = list(WL_H20)
def _rkpc(rad, unit, R500):
    u = (unit or "").strip().lower()
    if u in ("r/r500", "r500"): return np.asarray(rad, float) * R500
    if u == "mpc": return np.asarray(rad, float) * 1e3
    return np.asarray(rad, float)
def load_cluster(name):
    p = os.path.join(XDIR, name); c = {"name": name}
    with fits.open(os.path.join(p, name + "_hydro_mass.fits")) as f:
        dd = f[1].data; R5 = float(f[1].header["R500"]); c["R500"] = R5
        c["rh"] = _rkpc(dd["RADIUS"], f[1].columns["RADIUS"].unit, R5)
        c["Mh"] = np.array(dd["M_FORW"], float); c["eMh"] = np.array(dd["EM_FORW"], float)
    with fits.open(os.path.join(p, name + "_fgas_profile.fits")) as f:
        dd = f[1].data
        c["rg"] = _rkpc(dd["RADIUS"], f[1].columns["RADIUS"].unit, c["R500"]); c["Mg"] = np.array(dd["MGAS"], float)
    with fits.open(os.path.join(p, name + "_mstar.fits")) as f:
        dd = f[2].data
        c["rs"] = _rkpc(dd["RADIUS"], f[2].columns["RADIUS"].unit, c["R500"]); c["Ms"] = np.array(dd["MSTAR"], float)
    return c
ETT = json.load(open(os.path.join(XDIR, "xcop_r500_ettori2019.json")))
CLU = {n: load_cluster(n) for n in WLN}
GRID = np.exp(np.linspace(math.log(1.0), math.log(1.0e5), 1200))     # kpc
RGRID_M = GRID * kpc
def loginterp(xq, xp, fp):
    m = np.isfinite(xp) & np.isfinite(fp) & (fp > 0) & (xp > 0)
    return np.exp(np.interp(np.log(xq), np.log(xp[m]), np.log(fp[m]), left=np.nan, right=np.nan))
def build(c):
    def extend(rp, fp, r, steepen):
        f = loginterp(r, rp, fp); lo, hi = rp.min(), rp.max()
        sin_ = (math.log(fp[2]) - math.log(fp[0])) / (math.log(rp[2]) - math.log(rp[0]))
        sout = min(max((math.log(fp[-1]) - math.log(fp[-4])) / (math.log(rp[-1]) - math.log(rp[-4])), 0.0), 1.5)
        f = np.where(r < lo, fp[0] * (r / lo) ** sin_, f)
        if steepen: f = np.where(r > hi, fp[-1] + sout * fp[-1] * (1.0 - (r / hi) ** -1.0), f)
        else:       f = np.where(r > hi, fp[-1] * np.ones_like(r), f)
        return f
    c["Mgas_i"] = extend(c["rg"], c["Mg"], GRID, True)
    c["Mstar_i"] = extend(c["rs"], c["Ms"], GRID, False)
    c["Mbar"] = c["Mgas_i"] + c["Mstar_i"]
    c["Mh_i"] = np.exp(np.interp(np.log(GRID), np.log(c["rh"]), np.log(c["Mh"]),
                                 left=np.nan, right=math.log(c["Mh"][-1])))
    c["eMh_i"] = np.exp(np.interp(np.log(GRID), np.log(c["rh"]), np.log(c["eMh"]),
                                  left=np.nan, right=math.log(c["eMh"][-1])))
    c["R200"] = ETT[c["name"]]["R200"] * 1e3 if c["name"] in ETT else 1.6 * c["R500"]
    # the cluster's own BARYON density profile -- the source every nonlocal trigger below is built from
    c["rho_b"] = np.maximum(np.gradient(c["Mbar"] * MSUN, np.log(GRID)) / (4 * math.pi * RGRID_M ** 3), 1e-45)
    return c
for n in WLN: build(CLU[n])
for n in WLN:
    d = WL_H20[n]; d["rs"], d["dc"], d["rhoc"], d["c200"], d["r200"] = nfw_from_M200(d["M200"] * 1e14, d["z"])
print(f"\n      X-COP profiles read for the five clusters with published weak lensing (measured stellar "
      f"profiles present for all five)")

def rho_from_M(Mgrid, r_trunc_kpc):
    lg = np.log(GRID)
    rr = np.maximum(np.gradient(np.asarray(Mgrid, float), lg) * MSUN / (4 * math.pi * RGRID_M ** 3), 1e-45)
    lr = np.log(rr)
    def f(r_m):
        rk = r_m / kpc
        if rk > r_trunc_kpc: return 0.0
        return math.exp(np.interp(math.log(max(rk, GRID[0])), lg, lr))
    return f
def Mfw_grid(c, a0):
    gb = G * np.asarray(c["Mbar"], float) * MSUN / RGRID_M ** 2
    return g_kernel(gb, a0) * RGRID_M ** 2 / (G * MSUN)
def at(vals, r_kpc): return float(np.exp(np.interp(math.log(r_kpc), np.log(GRID), np.log(np.maximum(vals, 1e-30)))))

print("\n  A2 -- CONTROL: the 9 sigma cluster shear-SHAPE failure (L24 C11 / L51 C2 / L56 A3).")
SHAPE, BASE = {}, {}
for foot, a0 in A0.items():
    rows = []
    for n in WLN:
        c = CLU[n]; d = WL_H20[n]; rt = 2.0 * c["R200"]; zt = rt * kpc
        Mfw = Mfw_grid(c, a0); rho_fw = rho_from_M(Mfw, rt)
        Rf = np.exp(np.linspace(math.log(0.5 * Mpc), math.log(min(2.0, d["Rmax"]) * Mpc), 12))
        DSfw = np.array([Sigmabar_of_R(rho_fw, R, zt) - Sigma_of_R(rho_fw, R, zt) for R in Rf])
        DSwl = np.array([nfw_DS(R, d["rs"], d["dc"], d["rhoc"]) for R in Rf])
        sfw = np.polyfit(np.log(Rf), np.log(DSfw), 1)[0]; swl = np.polyfit(np.log(Rf), np.log(DSwl), 1)[0]
        rows.append(dict(name=n, Rf=Rf, DSfw=DSfw, DSwl=DSwl, sfw=sfw, swl=swl, Mfw=Mfw, rt=rt,
                         R500=c["R500"], Mfw500=at(Mfw, c["R500"]),
                         MWL500=nfw_M3d(c["R500"] * kpc, d["rs"], d["dc"], d["rhoc"]) / MSUN,
                         MHSE500=at(c["Mh_i"], c["R500"]), eMHSE500=at(c["eMh_i"], c["R500"])))
    dsl = np.array([r["sfw"] - r["swl"] for r in rows])
    SHAPE[foot] = (float(dsl.mean()), float(dsl.std(ddof=1) / math.sqrt(len(dsl)))); BASE[foot] = rows
    print(f"      {foot:9s}: framework log-slope {np.mean([r['sfw'] for r in rows]):+.3f}, measured "
          f"{np.mean([r['swl'] for r in rows]):+.3f}, difference {SHAPE[foot][0]:+.3f} +/- {SHAPE[foot][1]:.3f} "
          f"({abs(SHAPE[foot][0])/SHAPE[foot][1]:.1f} sigma)")
zs = {f: abs(SHAPE[f][0]) / SHAPE[f][1] for f in A0}
check("A2 [control] the 9-sigma cluster shear-shape failure is reproduced independently "
      "(L51 C2 / L56 A3: +0.516 +/- 0.058 / +0.521 +/- 0.058)",
      all(abs(SHAPE[f][0] - 0.518) < 0.05 for f in A0) and all(zs[f] > 6 for f in A0),
      ", ".join(f"{f} {SHAPE[f][0]:+.3f} +/- {SHAPE[f][1]:.3f} ({zs[f]:.1f} sigma)" for f in A0))

print("\n  A3 -- CONTROL: the measured cluster lensing-to-dynamical mass ratio.")
ratios, eratios = [], []
for r in BASE["canonical"]:
    d = WL_H20[r["name"]]; Rw = r["MWL500"] / r["MHSE500"]
    eratios.append(Rw * math.hypot(d["eM500"] / d["M500"], r["eMHSE500"] / r["MHSE500"])); ratios.append(Rw)
ratios = np.array(ratios); eratios = np.array(eratios); wgt = 1.0 / eratios ** 2
Rmeas = float(np.sum(wgt * ratios) / np.sum(wgt)); eRmeas = float(1.0 / math.sqrt(np.sum(wgt)))
print(f"      inverse-variance mean over the five clusters: {Rmeas:.3f} +/- {eRmeas:.3f} "
      f"(L51 C5 1.148 +/- 0.146; L24 C5 1.154 +/- 0.147).  The deposited theory predicts 1.000.")
check("A3 [control] the measured cluster lensing/dynamical mass ratio is reproduced",
      abs(Rmeas - 1.15) < 0.08, f"{Rmeas:.3f} +/- {eRmeas:.3f}")

print("\n  A4 -- CONTROL: the required lensing phantom, and L56's CONVENTION-FREE CRUX.")
print("""      Matching the required slip profile POINTWISE gives  W'(X) = 2 g_P/g_fw = 2 M_P(<r)/M_fw(<r),
      and a small object embedded at ambient X then suffers a fractional slip W'(X)/2 = M_P/M_fw exactly.
      This is the number L57 has to beat, and it is reproduced here before anything else is attempted.""")
FIT = {}
for foot, a0 in A0.items():
    out = []
    for r in BASE[foot]:
        c = CLU[r["name"]]; d = WL_H20[r["name"]]; rt = r["rt"]
        MWL = np.array([nfw_M3d(x * kpc, d["rs"], d["dc"], d["rhoc"]) / MSUN for x in GRID])
        msk = GRID <= rt; rr_m = GRID[msk] * kpc
        gfw = G * np.maximum(r["Mfw"][msk], 0) * MSUN / rr_m ** 2
        gwl = G * np.maximum(MWL[msk], 0) * MSUN / rr_m ** 2
        def cum(gg):
            tot = np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(rr_m))])
            return -(tot[-1] - tot)                                  # Phi(r) = - int_r^{rt} g dr'
        Phi_fw = cum(gfw); Pot_P = cum(gwl) - Phi_fw
        i5 = int(np.argmin(np.abs(GRID[msk] - r["R500"])))
        out.append(dict(name=r["name"], fP=float((MWL[np.argmin(np.abs(GRID - r["R500"]))] - r["Mfw500"]) / r["Mfw500"]),
                        slip500=abs(2 * Pot_P[i5]) / C2, frac500=abs(2 * Pot_P[i5]) / max(abs(2 * Phi_fw[i5]), 1e-30),
                        rgrid=GRID[msk], PotP=Pot_P, Phifw=Phi_fw,
                        gP=(gwl - gfw), gfw=gfw, MP=(MWL[msk] - r["Mfw"][msk]), Mfw=r["Mfw"][msk]))
    FIT[foot] = out
    print(f"      {foot:9s}: median M_P(<R500)/M_fw(<R500) = {np.median([o['fP'] for o in out]):.3f}, "
          f"median |slip| at R500 = {np.median([o['slip500'] for o in out]):.3e} "
          f"({np.median([o['frac500'] for o in out]):.2f} x the framework's own lensing potential)")
R_EMB_LOCAL = {f: float(np.median([o["fP"] for o in FIT[f]])) for f in A0}
for foot in A0:
    print(f"      {foot:9s}: per cluster M_P/M_fw -- "
          + ", ".join(f"{o['name']} {o['fP']:.2f}" for o in FIT[foot]))
check("A4 [control] L56's convention-free crux reproduces: the embedded response fixed by pointwise "
      "matching is M_P/M_fw = 0.806 (canonical) / 0.669 (alt)",
      abs(R_EMB_LOCAL["canonical"] - 0.806) < 0.05 and abs(R_EMB_LOCAL["alt"] - 0.669) < 0.05,
      ", ".join(f"{f} {R_EMB_LOCAL[f]:.3f}" for f in A0)
      + f", i.e. {min(R_EMB_LOCAL.values())/TOL_THEORY:.1e} - {max(R_EMB_LOCAL.values())/TOL_THEORY:.1e} x the "
        f"theory's own 1e-4 and {min(R_EMB_LOCAL.values())/TOL_DATA:.2f} - {max(R_EMB_LOCAL.values())/TOL_DATA:.2f} x a 20% bound")

print("\n  A5 -- CONTROL: L51's ceiling -- inside the 3 sigma lensing/dynamics budget, 8.8 -> 4.9 / 9.0 -> 4.7.")
BEST51 = {}
for foot in A0:
    rows = BASE[foot]; fPmed = R_EMB_LOCAL[foot]
    f_cap = min(max(0.0, (Rmeas + 3 * eRmeas - 1.0)) / fPmed, 1.0)
    best = None
    for f in np.linspace(0.0, 1.0, 51):
        dsl = np.array([np.polyfit(np.log(r["Rf"]), np.log((1 - f) * r["DSfw"] + f * r["DSwl"]), 1)[0] - r["swl"]
                        for r in rows])
        m = float(dsl.mean()); e = float(dsl.std(ddof=1) / math.sqrt(len(dsl)))
        if f <= f_cap + 1e-9: best = (f, m, e, abs(m) / max(e, 1e-9))
    f, m, e, zz = best; BEST51[foot] = dict(f=f, m=m, e=e, z=zz, f_cap=f_cap, fPmed=fPmed)
    print(f"      {foot:9s}: 3-sigma ceiling f <= {f_cap:.2f}; residual shape error {m:+.3f} +/- {e:.3f} "
          f"({zz:.1f} sigma, from {zs[foot]:.1f} sigma)")
check("A5 [control] L51's ceiling reproduces: inside the 3-sigma lensing/dynamics budget the freedom "
      "takes the shape residual from 8.8 to 4.9 sigma (canonical) / 9.0 to 4.7 (alt)",
      abs(BEST51["canonical"]["z"] - 4.9) < 0.6 and abs(BEST51["alt"]["z"] - 4.7) < 0.6,
      ", ".join(f"{f} {zs[f]:.1f} -> {BEST51[f]['z']:.1f} sigma at f = {BEST51[f]['f']:.2f}" for f in A0))


# ---------- the smoothing machinery ----------
print("""
  A6/A7 -- THE SMOOTHING MACHINERY.  A nonlocal trigger needs a kernel, and the kernel must be one the
  theory could actually carry.  The realisable family is the ELLIPTIC tower on the preferred slice,
  U = (1 - l^2 D^2)^{-n} rho, whose Green's function is generated here from G_1 = e^{-mr}/(4 pi r) by the
  exact recursion  G_{n+1} = -(1/(2 m n)) dG_n/dm  (from d/d(m^2) of (k^2+m^2)^{-n}), normalised as
  K_n = m^{2n} G_n so that int K_n d^3r = 1.  The GAUSSIAN is carried as well and is labelled for what it
  is: NOT realisable by any finite-order local operator (it is e^{l^2 D^2/2}), and used here only as the
  most generous member of the family.
""")
r_s, m_s = sp.symbols("r m", positive=True)
Gsym = [None, sp.exp(-m_s * r_s) / (4 * sp.pi * r_s)]
for nn in range(1, 7):
    Gsym.append(sp.simplify(-sp.diff(Gsym[nn], m_s) / (2 * m_s * nn)))
KSYM, dKSYM, small_r = {}, {}, {}
for nn in range(1, 7):
    K = sp.simplify(m_s ** (2 * nn) * Gsym[nn]); KSYM[nn] = K
    dK = sp.simplify(sp.diff(K, r_s)); dKSYM[nn] = dK
    norm = sp.simplify(sp.integrate(4 * sp.pi * r_s ** 2 * K, (r_s, 0, sp.oo)))
    if nn == 1:   lead, lab = sp.simplify(sp.limit(dK * r_s ** 2, r_s, 0)), "K_n'(r) ~ %s / r^2"
    elif nn == 2: lead, lab = sp.simplify(sp.limit(dK, r_s, 0)), "K_n'(r) ~ %s  (a nonzero CONSTANT)"
    else:         lead, lab = sp.simplify(sp.limit(dK / r_s, r_s, 0)), "K_n'(r) ~ %s x r"
    small_r[nn] = lead
    print(f"      n = {nn}: K_n = {K}   int K d^3r = {norm}   small-r: " + (lab % sp.nsimplify(lead)))
norms_ok = all(sp.simplify(sp.integrate(4 * sp.pi * r_s ** 2 * KSYM[nn], (r_s, 0, sp.oo)) - 1) == 0
               for nn in range(1, 7))
# the structural fact the whole lane turns on: for n >= 3 the kernel derivative is LINEAR in r at small r,
# exactly as for a Gaussian; for n = 1 it diverges and for n = 2 it is a nonzero constant.
lin_from_3 = all(small_r[nn].is_finite and small_r[nn] != 0 for nn in (3, 4, 5, 6))
n2_const = small_r[2].is_finite and small_r[2] != 0
n1_div = small_r[1] != 0
check("A6 [control] the realisable elliptic kernel tower is generated and normalised exactly, and its "
      "small-source behaviour is fixed: K_n'(r) is linear in r for every n >= 3 (as for a Gaussian), a "
      "nonzero CONSTANT for n = 2, and divergent as 1/r^2 for n = 1",
      norms_ok and lin_from_3 and n2_const and n1_div,
      "int K_n d^3r = 1 for n = 1..6 symbolically; K_n'(r) -> " +
      ", ".join(f"n={nn}: {sp.nsimplify(small_r[nn])} x r" for nn in (3, 4, 5, 6)) +
      " -- so a compact source's contribution to the trigger GRADIENT is suppressed as R for every "
      "realisable kernel of order 3 or more, and the Gaussian buys nothing extra")

def Ifun_gauss(s, l): return (2 * math.pi * l * l) ** -1.5 * l * l * (1 - np.exp(-s * s / (2 * l * l)))
def Kgauss(r, l): return (2 * math.pi * l * l) ** -1.5 * np.exp(-r * r / (2 * l * l))
def dKgauss(r, l): return -(r / (l * l)) * Kgauss(r, l)
_Kl = {nn: sp.lambdify((r_s, m_s), KSYM[nn], "numpy") for nn in range(1, 7)}
_dKl = {nn: sp.lambdify((r_s, m_s), dKSYM[nn], "numpy") for nn in range(1, 7)}
_Il = {}
for nn in range(1, 7):
    _prim = sp.integrate(KSYM[nn] * r_s, r_s)
    _Iexp = sp.expand(sp.simplify(_prim - sp.limit(_prim, r_s, 0)))
    # expand() distributes the exp(-m r), so no exp(+m r) survives and the form is overflow-safe
    assert not _Iexp.has(sp.exp(m_s * r_s)), f"unstable antiderivative at n = {nn}"
    _Il[nn] = sp.lambdify((r_s, m_s), _Iexp, "numpy")
def make_kernel(tag):
    """returns (I(s,l), K(r,l), dK(r,l), rms_radius/l).  I(s) = int_0^s K(t) t dt."""
    if tag == "gauss":
        return Ifun_gauss, Kgauss, dKgauss, math.sqrt(3.0)
    nn = int(tag[1:])
    rms = math.sqrt(float(sp.integrate(4 * sp.pi * r_s ** 4 * KSYM[nn].subs(m_s, 1), (r_s, 0, sp.oo))))
    return (lambda s, l, nn=nn: _Il[nn](np.maximum(s, 1e-12 * l), 1.0 / l),
            lambda r, l, nn=nn: _Kl[nn](np.maximum(r, 1e-12 * l), 1.0 / l),
            lambda r, l, nn=nn: _dKl[nn](np.maximum(r, 1e-12 * l), 1.0 / l), rms)
KERNELS = ["gauss"] + [f"n{nn}" for nn in (1, 2, 3, 4, 5, 6)]
KER = {t: make_kernel(t) for t in KERNELS}
print("      kernel rms radius in units of l: " + ", ".join(f"{t} {KER[t][3]:.2f}" for t in KERNELS))
print("      (every length quoted below is the kernel's rms radius l_rms, so the kernels are compared at")
print("       equal physical smoothing scale and not at equal nominal l)")

def smooth_radial(rq, rprof, rho, Ifun, l):
    """(rho * K)(r) = (2 pi / r) int r' rho(r') [I(r+r') - I(|r-r'|)] dr'  -- exact for spherical rho."""
    rq = np.atleast_1d(np.asarray(rq, float)); out = np.zeros_like(rq)
    for i, r in enumerate(rq):
        out[i] = 2 * math.pi / r * np.trapz(rprof * rho * (Ifun(r + rprof, l) - Ifun(np.abs(r - rprof), l)), rprof)
    return out

RP = np.exp(np.linspace(math.log(1e17), math.log(3e25), 3000))       # profile integration grid, m
lt = 5e21
val_uni, val_pt, val_mass = [], [], []
rho_uni = np.ones_like(RP) * 1e-25
Mpt = 2e41; rball = 1e19
rho_pt = np.where(RP < rball, Mpt / (4.0 / 3.0 * math.pi * rball ** 3), 0.0)
Mpt_eff = 4 * math.pi * np.trapz(RP ** 2 * rho_pt, RP)
for tag in KERNELS:
    If, Kf, dKf, _ = KER[tag]
    v1 = smooth_radial(np.array([1e22]), RP, rho_uni, If, lt)[0] / 1e-25
    rq = np.array([2e21, 6e21]); v2 = smooth_radial(rq, RP, rho_pt, If, lt) / (Mpt_eff * Kf(rq, lt))
    rq3 = np.exp(np.linspace(math.log(1e19), math.log(1e23), 60))
    sm = smooth_radial(rq3, RP, rho_pt, If, lt)
    v3 = 4 * math.pi * np.trapz(rq3 ** 2 * sm, rq3) / Mpt_eff
    val_uni.append(abs(v1 - 1)); val_pt.append(float(np.max(np.abs(v2 - 1)))); val_mass.append(abs(v3 - 1))
    print(f"      {tag:6s}: uniform-density fixed point {v1:.6f}   point mass / M K(r) "
          f"{v2[0]:.5f}, {v2[1]:.5f}   mass conservation {v3:.4f}")
allv = np.array(val_uni + val_pt + val_mass, float)
check("A7 [control] the spherical smoothing machinery is exact: a uniform density is a fixed point of "
      "every kernel, a compact source returns M K(r), and mass is conserved",
      bool(np.all(np.isfinite(allv))) and max(val_uni) < 1e-3 and max(val_pt) < 1e-2 and max(val_mass) < 0.05,
      f"worst uniform error {max(val_uni):.2e}, worst point-source error {max(val_pt):.2e}, worst mass "
      f"error {max(val_mass):.2e}")
print("""      The uniform fixed point is the first structural fact of this lane and it is not a technicality:
      EVERY normalised kernel leaves the cosmological background exactly where it is, so smoothing can
      only move a point TOWARD the background value, never away from it.""")


# ==================================================================================================
sec("PART B -- ADMISSIBILITY: which nonlocal quantities survive, settled before any fitting")
# ==================================================================================================
t_, x_, y_, z_ = sp.symbols("t x y z", real=True)
XV = (t_, x_, y_, z_); ETA = sp.diag(-1, 1, 1, 1)
def d1(f, mm): return sp.diff(f, XV[mm])
def lin_ricci(Hm):
    Gam = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for mm in range(4):
            for nn in range(4):
                Gam[l][mm][nn] = sp.Rational(1, 2) * ETA[l, l] * (d1(Hm[l, nn], mm) + d1(Hm[l, mm], nn) - d1(Hm[mm, nn], l))
    R = sp.zeros(4, 4)
    for mm in range(4):
        for nn in range(4):
            R[mm, nn] = sp.expand(sum(d1(Gam[l][mm][nn], l) - d1(Gam[l][l][mm], nn) for l in range(4)))
    return R

print("""
  B1 -- CONTROL, and the reason a nonlocal DEPTH trigger is NOT built in this lane.  L56 B1 showed that a
  constant deepening of Phi is an EXACT isometry -- a rescaling of t -- not merely a linear-order
  degeneracy.  Reproduced here symbolically.  Its force is exactly that it covers NONLOCAL functionals in
  one line: no functional of the metric and its derivatives, of any order, local or nonlocal, can measure
  a potential depth, because the two metrics are the SAME metric in different coordinates.
""")
cshift = sp.Symbol("c0", positive=True); Phi_s = sp.Function("Phi")(x_, y_, z_); Psi_s = sp.Function("Psi")(x_, y_, z_)
g_orig = -(1 + 2 * Phi_s); g_shift = -((1 + 2 * cshift) * (1 + 2 * Phi_s))
pullback = sp.simplify(g_shift / (1 + 2 * cshift))
b1_isometry = sp.simplify(pullback - g_orig) == 0
print(f"      deepen by a constant, 1 + 2 Phi~ = (1 + 2 c0)(1 + 2 Phi), then set t~ = sqrt(1+2 c0) t :")
print(f"      pulled-back g_00 = {sp.simplify(pullback)}   vs original {sp.simplify(g_orig)}   -> identical")
check("B1 [control] L56's exact-isometry obstruction reproduces: a constant deepening of the potential "
      "is an exact diffeomorphism, so NO functional of the metric -- local or nonlocal, at any order -- "
      "can measure a depth", b1_isometry,
      "verified symbolically; this is why a nonlocal DEPTH trigger is excluded a priori and is not built "
      "in this lane")

print("""
  B2 -- AND THE CLOCK-CARRIED DEPTH DOES NOT ESCAPE BY BEING SMOOTHED EITHER.  L56 B4 found the one
  covariant carrier of a depth, X = 1 - Q/Q0 with Q = n^mu d_mu phi, and L56 B5 killed it because X is
  ADDITIVE over sources: a galaxy inside a cluster carries the cluster's X.  Smoothing is a LINEAR
  operation, so it commutes with superposition exactly.  Tested rather than asserted.
""")
P1, P2 = sp.symbols("Phi1 Phi2", real=True); Wk1, Wk2 = sp.symbols("w1 w2", positive=True)
lin_smooth = sp.simplify((Wk1 * (P1 + P2) + Wk2 * (P1 + P2)) - ((Wk1 + Wk2) * P1 + (Wk1 + Wk2) * P2))
# numerical form: the smoothed depth of a two-component source equals the sum of the smoothed depths
rho_a = np.exp(-((RP - 2e21) / 3e20) ** 2) * 1e-24
rho_b_ = np.exp(-((RP - 8e21) / 5e20) ** 2) * 1e-24
If, Kf, dKf, _ = KER["gauss"]
sm_a = smooth_radial(np.array([5e21]), RP, rho_a, If, lt)[0]
sm_b = smooth_radial(np.array([5e21]), RP, rho_b_, If, lt)[0]
sm_ab = smooth_radial(np.array([5e21]), RP, rho_a + rho_b_, If, lt)[0]
add_err = abs(sm_ab / (sm_a + sm_b) - 1)
print(f"      smoothing a two-component source: <A+B> / (<A> + <B>) - 1 = {add_err:.3e}  -- exactly additive")
check("B2 [test] smoothing the clock-carried DEPTH X = 1 - Q/Q0 escapes L56 B5 -- i.e. a smoothed depth "
      "can be referenced to the host rather than to the total",
      not (lin_smooth == 0 and add_err < 1e-6),
      "NO -- smoothing is a linear operation and commutes with superposition exactly (additivity error "
      f"{add_err:.1e}), so <X_host + X_sub> = <X_host> + <X_sub> and the embedded object still carries the "
      "host's trigger.  A nonlocal DEPTH trigger inherits L56 B5 unchanged and is excluded on TWO "
      "independent grounds (B1 for a metric-built depth, additivity for the clock-carried one).  This "
      "lane does not build one")

print("""
  B3 -- WHICH NONLOCAL QUANTITIES ARE THEN ADMISSIBLE.  The requirement is: (i) a covariant scalar of the
  theory's own fields; (ii) blind to a constant deepening (B1); (iii) not reducible to a depth.  Each
  candidate is tested against Phi -> Phi + c0 and, separately, against a UNIFORM field Phi -> Phi + g.x
  (L31 Step E), because a quantity blind to both is a genuine curvature and a quantity blind only to the
  first is an acceleration -- which the theory already uses in its own kernel argument Y, so it is
  admissible but carries the external-field effect with it.
""")
gvec = sp.symbols("g1 g2 g3", real=True)
lapPhi = sum(sp.diff(Phi_s, v, 2) for v in (x_, y_, z_))
CANDS = [
    ("<Phi>_l          smoothed potential DEPTH", Phi_s, "depth"),
    ("<|grad Phi|>_l   smoothed acceleration", sp.sqrt(sum(sp.diff(Phi_s, v) ** 2 for v in (x_, y_, z_))), "accel"),
    ("<lap Phi>_l      smoothed density / Ricci", lapPhi, "curv"),
    ("<(d_i d_j Phi)^2>_l  smoothed tidal invariant",
     sum(sp.diff(Phi_s, a, b) ** 2 for a in (x_, y_, z_) for b in (x_, y_, z_)), "curv"),
]
adm = {}
for nm, expr, kind in CANDS:
    blind_c = sp.simplify(expr.subs(Phi_s, Phi_s + cshift) - expr) == 0
    ex_u = expr.subs(Phi_s, Phi_s + gvec[0] * x_ + gvec[1] * y_ + gvec[2] * z_)
    blind_u = sp.simplify(sp.expand(ex_u - expr)) == 0
    adm[nm] = (blind_c, blind_u, kind)
    print(f"      {nm:52s}  depth-blind {'YES' if blind_c else 'NO ':3s}   uniform-field-blind "
          f"{'YES' if blind_u else 'NO'}")
ok_b3 = ((not adm[CANDS[0][0]][0]) and adm[CANDS[1][0]][0] and adm[CANDS[2][0]][0] and adm[CANDS[3][0]][0]
         and adm[CANDS[2][0]][1] and adm[CANDS[3][0]][1] and (not adm[CANDS[1][0]][1]))
check("B3 [test] the admissible nonlocal quantities are exactly the smoothed CURVATURES (density and "
      "tidal invariant) and the smoothed ACCELERATION; the smoothed DEPTH is not admissible",
      ok_b3,
      "the smoothed depth fails the constant-shift test and is excluded (B1, B2); the smoothed density "
      "<lap Phi> and the smoothed tidal invariant are blind to BOTH a constant and a uniform field, so "
      "they are genuine curvatures; the smoothed acceleration is depth-blind but not uniform-field-blind, "
      "which is admissible here only because the theory's own kernel argument Y already is not")

print("""
  B4 -- CONTROL, AND A REAL POSITIVE.  A spatial smoothing is not defined without a slicing: 'the ball of
  radius l around this event' is not a covariant notion in a frame-free theory, and a covariantly smeared
  4-volume average with a timelike direction picked out is exactly what a preferred foliation supplies.
  The theory HAS one -- n_mu = -d_mu tau / sqrt(-(d tau)^2), hypersurface-orthogonal by construction.  So
  the nonlocal functional is definable in THIS theory and not in a frame-free one.  Recorded as a
  positive, exactly as L56 recorded B4.
""")
tau_ = sp.Function("tau")(t_, x_, y_, z_); f_ = sp.Function("f")
dtau = sp.Matrix([sp.diff(tau_, v) for v in XV])
dftau = sp.Matrix([sp.diff(f_(tau_), v) for v in XV])
n_of = lambda dv: sp.simplify(dv / sp.sqrt(sum(-ETA[i, i] * dv[i] ** 2 for i in range(4))))
reparam_ok = sp.simplify((n_of(dftau) - n_of(dtau) * sp.sign(sp.Derivative(f_(tau_), tau_))).applyfunc(
    lambda e: sp.simplify(e.subs(sp.Derivative(f_(tau_), tau_), sp.Symbol("fp", positive=True))))) == sp.zeros(4, 1)
check("B4 [control] the theory's clock supplies the slicing a spatial smoothing needs, and it is "
      "reparametrisation-invariant (tau -> f(tau) leaves n_mu unchanged for f' > 0)",
      reparam_ok,
      "n_mu is invariant under tau -> f(tau), so the smoothing hypersurface is a property of the theory "
      "and not of a coordinate choice.  A frame-free theory has no such slicing and therefore cannot "
      "write ANY spatial nonlocal functional -- so this successor exists only because the clock does")

print("""
  B5 -- THE FIRST OBSTRUCTION THE ESCAPE MUST BEAT, AND IT ELIMINATES TWO OF THE THREE SURVIVORS.
  For any spherically symmetric normalised kernel, Newton's theorem says the smoothed source's POTENTIAL
  and ACCELERATION outside radius ~l are EXACTLY those of the unsmoothed source.  So a smoothed potential
  or a smoothed acceleration is not suppressed at all at the radii where a galaxy's lensing and dynamical
  masses are actually compared, unless l exceeds that radius -- whereas the smoothed DENSITY is suppressed
  everywhere by the kernel itself.  Verified numerically on the machinery of A7.
""")
gsm = []
for tag in ("gauss", "n1", "n2", "n4", "n6"):
    If, Kf, dKf, rmsf = KER[tag]
    l_nom = lt / rmsf                                   # so that the rms radius is exactly lt
    rq = np.array([1.0, 2.0, 5.0]) * lt
    rr_int = np.exp(np.linspace(math.log(1e18), math.log(8 * lt), 500))
    sm_prof = smooth_radial(rr_int, RP, rho_pt, If, l_nom)
    Menc = np.array([4 * math.pi * np.trapz((rr_int[rr_int <= rr] ** 2) * sm_prof[rr_int <= rr],
                                            rr_int[rr_int <= rr]) for rr in rq])
    gsm.append(Menc / Mpt_eff)
    print(f"      {tag:6s}: smoothed enclosed mass / true mass at r/l_rms = 1, 2, 5 : "
          + ", ".join(f"{v:.4f}" for v in Menc / Mpt_eff))
gsm_arr = np.array(gsm, float)
assert np.all(np.isfinite(gsm_arr)), "B5 smoothing returned non-finite values"
newton_ok = all(abs(v[-1] - 1) < 0.05 for v in gsm)
check("B5 [test] a smoothed POTENTIAL or ACCELERATION trigger suppresses a compact source at the radii "
      "where galaxy lensing and dynamics are compared",
      not newton_ok,
      "NO -- by Newton's theorem the smoothed source's enclosed mass, and hence its potential and its "
      "acceleration, return to the unsmoothed values within 5% by r = 5 l_rms for every kernel tested.  A "
      "potential- or acceleration-triggered weight is therefore blind to the smoothing outside l and "
      "needs l > the probe radius before it does anything at all.  ONLY the smoothed DENSITY (equivalently "
      "the smoothed Ricci / tidal invariant), which is the kernel itself, is suppressed at every radius.  "
      "That single fact selects the trigger this lane then tests")

print("""
  B6 -- AND THE NONLOCALITY MUST NOT COST A MODE.  Two realisations, and only one is admissible.
""")
om, kk, lsym = sp.symbols("omega k l", positive=True)
cov_den = 1 + lsym ** 2 * (om ** 2 - kk ** 2)          # (1 - l^2 box)  with box = -d_t^2 + D^2
ell_den = 1 + lsym ** 2 * kk ** 2                      # (1 - l^2 D^2), D spatial on the slice
cov_poles = sp.solve(sp.Eq(cov_den, 0), om)
ell_poles = sp.solve(sp.Eq(ell_den.subs(kk, sp.Symbol("kreal", real=True)), 0), om)
print(f"      covariant (1 - l^2 box)^-1 : new poles at omega^2 = {sp.simplify(kk**2 - 1/lsym**2)}  -> a new "
      f"propagating mode (and, being a simple pole of a squared inverse propagator, a ghost)")
print(f"      elliptic  (1 - l^2 D^2)^-1 : denominator 1 + l^2 k^2 > 0 for every real spatial k  -> NO new "
      f"pole, hence no new propagating mode; it is a CONSTRAINT on the slice, like the lapse and shift")
check("B6 [test] the smoothing can be made covariant without adding a propagating mode",
      len(cov_poles) > 0 and len(ell_poles) == 0,
      "YES, but only in one realisation: the ELLIPTIC operator on the clock's own slices adds no pole "
      "and therefore no mode (this is L17's A5 observation and L51 D1's mode budget, reached here "
      "independently), while the covariant (1 - l^2 box)^-1 adds a pole at omega^2 = k^2 - 1/l^2 and is "
      "excluded.  The price is that the smoothing is INSTANTANEOUS in the preferred frame -- a genuine "
      "cost, and the same cost the programme's York/CMC branch was closed on")


# ==================================================================================================
sec("PART C -- THE MASTER FORMULA, AND THE LENGTH THE MECHANISM NEEDS")
# ==================================================================================================
print("""
  C0 -- THE MASTER FORMULA, derived once and used for everything below.

  Let the slip be s = W(U) for ANY trigger U, local or nonlocal.  Two facts fix everything.

  (1) THE CLUSTER FIXES W' POINTWISE.  The shear data require a definite added lensing phantom, hence a
      definite slip PROFILE s_req(r) over 0.5-2 Mpc.  Matching it pointwise,
            W'(U_cl) = (d s_req/dr) / (dU/dr)|_cl.
  (2) A SLIP IS OBSERVABLE ONLY THROUGH ITS GRADIENT.  An object of any mass sitting at ambient U adds
      its own dU_obj(R) to the trigger, so the slip varies across it by W'(U_cl) d(dU_obj)/dR, against
      its own lensing signature 2 g_obj/c^2.  Its fractional lensing-versus-dynamical discrepancy is
            R_emb = W'(U_cl) |d(dU_obj)/dR| c^2 / (2 g_obj).

  Putting them together, with  ratio(X) = |dU/dr| / g  the trigger gradient PER UNIT ACCELERATION,

            R_emb  =  (g_P/g_fw)|_cl  x  [ratio_obj / ratio_cl]  =  (M_P/M_fw) x S,     S = ratio_obj/ratio_cl.

  L56 IS THE S = 1 CORNER.  For the local depth trigger U = Phi/c^2, dU/dr = -g/c^2 for EVERY object, so
  ratio = 1/c^2 identically and S = 1 -- which is exactly why L56's response was object-independent and
  equal to M_P/M_fw with no convention entering.  S is therefore the ONLY thing a nonlocal trigger can
  buy, and this lane measures it.

  NOTE WHAT DROPS OUT.  Because only gradients are observable, there is NO requirement that the trigger
  values of clusters and galaxies fail to overlap.  L51's C9 overlap argument and L56's non-overlap
  bookkeeping are both VACUOUS for a nonlocal trigger.  That is a structural gain and it is recorded as
  one; it does not by itself buy anything, because S is what the gates measure.
""")
# control: the local depth trigger gives ratio == 1/c^2 for every object, on real profiles
dep_ratio = []
for foot, a0 in A0.items():
    for n in WLN:
        c = CLU[n]; gb = G * c["Mbar"] * MSUN / RGRID_M ** 2; gfw = g_kernel(gb, a0)
        Phi = -np.concatenate([[0.0], np.cumsum(0.5 * (gfw[1:] + gfw[:-1]) * np.diff(RGRID_M))])[::-1][::-1]
        Phi = np.concatenate([[0.0], np.cumsum(0.5 * (gfw[1:] + gfw[:-1]) * np.diff(RGRID_M))])
        dPhi = np.gradient(Phi, RGRID_M)
        sel = (GRID > 500) & (GRID < 2000)
        dep_ratio.append(float(np.max(np.abs(dPhi[sel] / gfw[sel] - 1))))
check("C0 [control] the master formula reduces to L56 exactly: for the LOCAL DEPTH trigger the gradient "
      "per unit acceleration is 1 for every object, so S = 1 identically and R_emb = M_P/M_fw",
      max(dep_ratio) < 1e-3,
      f"|dPhi/dr / g - 1| <= {max(dep_ratio):.2e} over 0.5-2 Mpc in all five clusters and both footings "
      f"(the residual is the log-grid finite difference; the identity dU/dr = -g/c^2 is exact by "
      f"construction for a depth trigger); "
      f"L56's 0.806 / 0.669 is therefore the S = 1 value of this lane's formula")

# ---------------- the galaxy population ----------------
UPS_D, UPS_B = 0.5, 0.7
GALS = {}
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    try: dd = np.loadtxt(fn, comments="#")
    except Exception: continue
    if dd.ndim != 2 or dd.shape[1] < 6: continue
    rr = dd[:, 0] * kpc; Vo = dd[:, 1] * 1e3; eV = dd[:, 2] * 1e3
    Vg = dd[:, 3] * 1e3; Vd = dd[:, 4] * 1e3; Vb = dd[:, 5] * 1e3
    Vb2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
    m = (rr > 0) & (Vo > 0) & (Vb2 > 0) & (eV / np.maximum(Vo, 1) < 0.10)
    if m.sum() < 3: continue
    rr, Vo, Vb2 = rr[m], Vo[m], Vb2[m]
    GALS[os.path.basename(fn).replace("_rotmod.dat", "")] = dict(r=rr, M=Vb2 * rr / G, vo=Vo)
MB_GAL = np.array([GALS[g]["M"][-1] for g in GALS])
RB_GAL = np.array([GALS[g]["r"][-1] for g in GALS])
print(f"      SPARC: {len(GALS)} galaxies, baryonic mass {MB_GAL.min()/MSUN:.2e} - {MB_GAL.max()/MSUN:.2e} "
      f"Msun, outermost measured radius {RB_GAL.min()/kpc:.1f} - {RB_GAL.max()/kpc:.1f} kpc")
MG_REF = 1.0e11 * MSUN      # an L* galaxy: the population galaxy-galaxy lensing actually measures
RG_REF = 20.0 * kpc

# ---------------- vectorised smoothing ----------------
def smooth_vec(rq, rprof, rho, Ifun, l):
    rq = np.atleast_1d(np.asarray(rq, float))
    A = Ifun(rq[:, None] + rprof[None, :], l) - Ifun(np.abs(rq[:, None] - rprof[None, :]), l)
    return 2 * math.pi / rq * np.trapz(rprof[None, :] * rho[None, :] * A, rprof, axis=1)

# cluster baryon density on the integration grid (extended, then the cosmic mean outside)
def rho_prof(c):
    lg = np.log(GRID); lr = np.log(np.maximum(c["rho_b"], 1e-45))
    rk = RP / kpc
    out = np.exp(np.interp(np.log(rk), lg, lr, left=lr[0], right=-np.inf))
    r_trunc = 3.0 * c["R200"]
    return np.where(rk > r_trunc, rho_b_cosmic, np.maximum(out, rho_b_cosmic))

print("""
  C1 -- CONTROL: the galaxy side is a FULL convolution, not a point-source approximation, and S does not
  depend on the galaxy's own structure.  A realistic spherical-equivalent baryon profile is used
  (M(r) = M_b [1 - (1 + r/r_d) e^{-r/r_d}], the exponential sphere), and the answer is checked against a
  galaxy twice as large and against one ten times as massive.
""")
def gal_profile(Mb, rd):
    rho = Mb / (8 * math.pi * rd ** 3) * np.exp(-RP / rd)
    return rho * Mb / (4 * math.pi * np.trapz(RP ** 2 * rho, RP))
GAL_RD = 4.0 * kpc
GPROF = gal_profile(MG_REF, GAL_RD)
def ratio_gal_of(tag, l_rms_kpc, Rmax_kpc, prof=None, Mb=MG_REF, nu=1.0, a0=None, npts=26):
    """max over R <= Rmax of |d<rho>_l/dR| / g_gal(R), the trigger gradient per unit of the galaxy's
       own acceleration.  g_gal is the EFE-corrected internal field nu x G M(<R)/R^2."""
    If, Kf, dKf, rmsf = KER[tag]; l_nom = l_rms_kpc * kpc / rmsf
    prof = GPROF if prof is None else prof
    Rq = np.exp(np.linspace(math.log(1.0 * kpc), math.log(Rmax_kpc * kpc), npts))
    sm_hi = smooth_vec(Rq * 1.02, RP, prof, If, l_nom); sm_lo = smooth_vec(Rq * 0.98, RP, prof, If, l_nom)
    grad = np.abs(sm_hi - sm_lo) / (0.04 * Rq)
    Menc = np.array([4 * math.pi * np.trapz(RP[RP <= R] ** 2 * prof[RP <= R], RP[RP <= R]) for R in Rq])
    g_gal = nu * G * np.maximum(Menc, 1e-30) / Rq ** 2
    return float(np.max(grad / g_gal)), Rq, grad / g_gal
r0, _, _ = ratio_gal_of("gauss", 1000.0, 100.0)
r1, _, _ = ratio_gal_of("gauss", 1000.0, 100.0, prof=gal_profile(MG_REF, 2 * GAL_RD))
r2, _, _ = ratio_gal_of("gauss", 1000.0, 100.0, prof=gal_profile(10 * MG_REF, GAL_RD), Mb=10 * MG_REF)
print(f"      reference galaxy (M_b = 1e11 Msun, r_d = 4 kpc):        ratio_gal = {r0:.4e}")
print(f"      the same mass in a disc twice as large (r_d = 8 kpc):   ratio_gal = {r1:.4e}  ({r1/r0:.3f} x)")
print(f"      ten times the mass, same scale radius:                  ratio_gal = {r2:.4e}  ({r2/r0:.3f} x)")
check("C1 [control] S is a property of the two SCALES, not of the galaxy: the trigger gradient per unit "
      "of the object's own acceleration is independent of the object's mass and insensitive to its size",
      abs(r2 / r0 - 1) < 0.02 and abs(r1 / r0 - 1) < 0.10,
      f"mass x10 changes it by {abs(r2/r0-1)*100:.2f}%, size x2 by {abs(r1/r0-1)*100:.1f}% -- the mass "
      f"cancels EXACTLY between the trigger and the acceleration, which is what makes the response "
      f"object-independent in the same way L56's was")

print("""
  C2 -- S(l), MEASURED ON REAL PROFILES.  ratio_cl comes from the smoothed X-COP BARYON density profile
  of each cluster and the framework's own acceleration at 1 Mpc; ratio_gal from a full convolution of the
  reference galaxy, maximised over R <= R_max.  Three choices are made GENEROUSLY to the door and named:
    (a) the embedded galaxy's internal field carries the EXTERNAL-FIELD boost G_eff/G = nu(g_ext/a0)
        (the angle-averaged value), LARGER than the radial dg_fw/dg and therefore making S SMALLER;
    (b) beyond 3 R200 the cluster's surroundings are replaced by the cosmic mean, which UNDERSTATES the
        mass inside a large smoothing ball and therefore understates S at large l;
    (c) R_max, the largest radius at which a galaxy's lensing and dynamical masses are BOTH measured, is
        the parameter the answer turns on, and all three of 30 / 100 / 300 kpc are carried.
""")
LGRID = np.array([30., 100., 300., 600., 1000., 2000., 3000., 6000., 10000., 30000.])   # l_rms, kpc
RMAX_LIST = [30.0, 100.0, 300.0]
RCL_EVAL = 1000.0
TAGS = ["gauss", "n1", "n2", "n3", "n4", "n6"]
CLINFO = {}
for foot, a0 in A0.items():
    gbs = [G * at(CLU[n]["Mbar"], RCL_EVAL) * MSUN / (RCL_EVAL * kpc) ** 2 for n in WLN]
    nue = [float(g_kernel(g, a0) / g) for g in gbs]
    nur = [float((g_kernel(g * 1.01, a0) - g_kernel(g * 0.99, a0)) / (0.02 * g)) for g in gbs]
    CLINFO[foot] = dict(nu_e=float(np.median(nue)), nu_r=float(np.median(nur)),
                        gfw=[float(g_kernel(g, a0)) for g in gbs])
print("      external-field boost at 1 Mpc in the cluster: " +
      ", ".join(f"{f} nu = {CLINFO[f]['nu_e']:.2f} (angle-averaged, USED) / {CLINFO[f]['nu_r']:.2f} (radial)"
                for f in A0))
RATIO_CL, RATIO_GAL = {}, {}
for foot, a0 in A0.items():
    for tag in TAGS:
        If, Kf, dKf, rmsf = KER[tag]
        for lr_ in LGRID:
            l_nom = lr_ * kpc / rmsf; vals = []
            for i, n in enumerate(WLN):
                rho = rho_prof(CLU[n])
                rq = np.array([RCL_EVAL * 0.98, RCL_EVAL * 1.02]) * kpc
                sm = smooth_vec(rq, RP, rho, If, l_nom)
                vals.append(abs((sm[1] - sm[0]) / (rq[1] - rq[0])) / CLINFO[foot]["gfw"][i])
            RATIO_CL[(foot, tag, lr_)] = float(np.median(vals))
for tag in TAGS:
    for lr_ in LGRID:
        for Rmax in RMAX_LIST:
            for foot in A0:
                RATIO_GAL[(foot, tag, lr_, Rmax)] = ratio_gal_of(tag, lr_, Rmax, nu=CLINFO[foot]["nu_e"])[0]
def Sval(foot, tag, lr_, Rmax): return RATIO_GAL[(foot, tag, lr_, Rmax)] / RATIO_CL[(foot, tag, lr_)]
def Remb(foot, tag, lr_, Rmax): return R_EMB_LOCAL[foot] * Sval(foot, tag, lr_, Rmax)
for Rmax in RMAX_LIST:
    print(f"\n      R_emb = (M_P/M_fw) x S, canonical footing, R_max = {Rmax:.0f} kpc "
          f"(the theory's own gate is {TOL_THEORY:.0e}, a generous empirical gate {TOL_DATA:.2f}):")
    print(f"      {'l_rms[kpc]':>11s}" + "".join(f"{t:>12s}" for t in TAGS))
    for lr_ in LGRID:
        print(f"      {lr_:11.0f}" + "".join(f"{Remb('canonical', t, lr_, Rmax):12.3e}" for t in TAGS))
print("\n      (the alt footing differs only through M_P/M_fw = "
      f"{R_EMB_LOCAL['alt']:.3f} vs {R_EMB_LOCAL['canonical']:.3f} and nu; it is carried in every gate below)")

print("""
  C3 -- THE FLOOR, AND WHY IT IS A THEOREM RATHER THAN A NUMBER.  Once l exceeds BOTH scales, the cluster
  and the galaxy are both compact against the kernel and every kernel factor cancels:
        ratio_obj / ratio_cl  ->  [R_p^q / (nu G)] / [M_cl r_cl^q / (G M_fw,cl)]  =  (R_p/r_cl)^q x
                                  M_fw,cl / (nu M_cl),
  where q is fixed by the kernel's behaviour at the origin, K'(r) ~ r^{q-2}.  A6 established that for the
  realisable elliptic tower K'(r) ~ 1/r^2 (n = 1, so q = 0: NO discrimination at all), K'(r) ~ const
  (n = 2, q = 2) and K'(r) ~ r for EVERY n >= 3 (q = 3) -- and the Gaussian, the n -> infinity member, is
  also q = 3.  So the discrimination saturates at the CUBE of the scale ratio and no higher order, and no
  length, buys anything more.
""")
# the dilution factor: at large l the cluster's "compact" mass is everything inside the ball, not M(<r_cl)
DIL = float(np.median([at(CLU[n]["Mbar"], RCL_EVAL) / at(CLU[n]["Mbar"], 3.0 * CLU[n]["R200"]) for n in WLN]))
print(f"      dilution factor M_b(<r_cl) / M_b(<3 R200) = {DIL:.3f}  (the cluster mass a large smoothing "
      f"ball sees, relative to the mass inside the evaluation radius)")
FLOOR = {}
for tag in TAGS:
    q = {"n1": 0, "n2": 2}.get(tag, 3)      # ratio_gal ~ R_p^q from K'(r) ~ r^{q-2}
    for Rmax in RMAX_LIST:
        pred = (Rmax / RCL_EVAL) ** q * DIL
        obs = min(Sval("canonical", tag, lr_, Rmax) for lr_ in LGRID if lr_ >= 3000.)
        FLOOR[(tag, Rmax)] = (q, pred, obs)
print(f"      {'kernel':>8s} {'q':>3s} {'R_max[kpc]':>11s} {'predicted floor':>16s} {'measured floor S':>18s} {'ratio':>8s}")
for tag in TAGS:
    for Rmax in RMAX_LIST:
        q, pred, obs = FLOOR[(tag, Rmax)]
        print(f"      {tag:>8s} {q:3d} {Rmax:11.0f} {pred:16.3e} {obs:18.3e} {obs/pred:8.2f}")
ratios_floor = [FLOOR[(t, Rm)][2] / FLOOR[(t, Rm)][1] for t in TAGS for Rm in RMAX_LIST]
# the sharp, normalisation-free content of the floor law is the EXPONENT: how the floor scales with R_p
print(f"\n      the normalisation-free test -- how the measured floor scales with the probe radius:")
print(f"      {'kernel':>8s} {'q':>3s} {'S(100)/S(30)':>14s} {'(10/3)^q':>10s} {'S(300)/S(100)':>15s} {'3^q':>8s}")
exp_err = []
for tag in TAGS:
    q = FLOOR[(tag, 30.0)][0]
    r1 = FLOOR[(tag, 100.0)][2] / FLOOR[(tag, 30.0)][2]; r2 = FLOOR[(tag, 300.0)][2] / FLOOR[(tag, 100.0)][2]
    exp_err += [abs(r1 / (10 / 3.) ** q - 1), abs(r2 / 3.0 ** q - 1)]
    print(f"      {tag:>8s} {q:3d} {r1:14.2f} {(10/3.)**q:10.2f} {r2:15.2f} {3.0**q:8.2f}")
check("C3 [control] the floor law S_min ~ (R_p/r_cl)^q with q = 0, 2, 3 for n = 1, n = 2 and every "
      "n >= 3 (Gaussian included) reproduces the measured floor's scaling with the probe radius to 5%",
      max(exp_err) < 0.05,
      f"worst exponent error {max(exp_err)*100:.1f}% over six kernels; the ABSOLUTE floor is then "
      f"{min(ratios_floor):.2f} - {max(ratios_floor):.2f} x the crude estimate (R_p/r_cl)^q x "
      f"M_b(<r_cl)/M_b(<3 R200) = {DIL:.2f}, the spread being how much cluster mass a given ball actually "
      f"sees.  Note the direction of the one approximation: this lane replaces the cluster's surroundings "
      f"beyond 3 R200 with the cosmic mean, which UNDERSTATES the mass a large smoothing ball sees and "
      f"therefore UNDERSTATES the floor.  It runs against the door, not for it")

print("""
  C4 -- SO: DOES A SMOOTHED TRIGGER MAKE THE HOST/SUBSTRUCTURE DISTINCTION?  This is the lane's first
  question and the answer is quantitative, not rhetorical.
""")
BEST = {}
for foot in A0:
    for Rmax in RMAX_LIST:
        best = min(((Remb(foot, t, lr_, Rmax), t, lr_) for t in TAGS for lr_ in LGRID))
        BEST[(foot, Rmax)] = best
        print(f"      {foot:9s} R_max = {Rmax:5.0f} kpc: best R_emb = {best[0]:.3e} at kernel {best[1]}, "
              f"l_rms = {best[2]:.0f} kpc   ({R_EMB_LOCAL[foot]/best[0]:.1e} x better than L56's "
              f"{R_EMB_LOCAL[foot]:.3f})")
gain = min(R_EMB_LOCAL[f] / BEST[(f, Rm)][0] for f in A0 for Rm in RMAX_LIST)
gain_max = max(R_EMB_LOCAL[f] / BEST[(f, Rm)][0] for f in A0 for Rm in RMAX_LIST)
check("C4 [test] a nonlocal (smoothed) trigger makes the host/substructure distinction that L56 proved "
      "no local field can make",
      gain > 10.0,
      f"YES -- it buys a factor {gain:.0f} - {gain_max:.0f} on the embedded response, entirely by SCALE: "
      f"the suppression is (R_p/r_cl)^3, the cube of the ratio of the radius at which a galaxy is "
      f"measured to the radius at which the cluster needs the slip.  This is a real positive and it is "
      f"the first thing this lane found")

print("""
  C5 -- BUT DOES IT PASS THE GATES?  The two the corpus carries: the deposited theory's own no-slip
  result Phi = Psi to 1e-4 in galaxies, and a generous EMPIRICAL galaxy-lensing tolerance of 20%.
""")
pass_th = {(f, Rm): BEST[(f, Rm)][0] <= TOL_THEORY for f in A0 for Rm in RMAX_LIST}
pass_da = {(f, Rm): BEST[(f, Rm)][0] <= TOL_DATA for f in A0 for Rm in RMAX_LIST}
for f in A0:
    for Rm in RMAX_LIST:
        b = BEST[(f, Rm)][0]
        print(f"      {f:9s} R_max = {Rm:5.0f} kpc: R_emb = {b:.3e}  ->  theory gate "
              f"{'PASS' if pass_th[(f,Rm)] else 'FAIL'} ({b/TOL_THEORY:.2f} x), empirical gate "
              f"{'PASS' if pass_da[(f,Rm)] else 'FAIL'} ({b/TOL_DATA:.3f} x)")
R100 = max(BEST[(f, 100.0)][0] for f in A0)
check("C5a [test] at the FULL repair amplitude the smoothed trigger preserves the deposited theory's OWN "
      "no-slip result (1e-4) on the galaxies that sit at cluster radii, at the radii where their lensing "
      "and dynamical masses are compared (R_max = 100 kpc; PART F carries the amplitude curve)",
      R100 <= TOL_THEORY,
      f"NO -- best achievable {R100:.2e}, i.e. {R100/TOL_THEORY:.1f} x the bound.  The FLOOR is "
      f"(R_p/r_cl)^3 x M_P/M_fw and no kernel order and no length beats it.  The verdict FLIPS at "
      f"R_max = {RCL_EVAL*(TOL_THEORY/R_EMB_LOCAL['canonical'])**(1/3.):.0f} kpc: inside that radius the "
      f"theory gate is met, outside it is not.  This is a 3-order-of-magnitude improvement on L56's "
      f"{R_EMB_LOCAL['canonical']:.2f} and it still does not reach the theory's own number")
check("C5b [test] the smoothed trigger passes a generous EMPIRICAL galaxy-lensing tolerance of 20% "
      "fractional slip, at every probe radius carried",
      all(pass_da.values()),
      "YES at every R_max from 30 to 300 kpc and on both footings: best " +
      ", ".join(f"{f} R_max={Rm:.0f} {BEST[(f,Rm)][0]:.1e}" for f in A0 for Rm in RMAX_LIST) +
      f".  This is the first mechanism in this programme to clear the embedded-galaxy gate on the "
      f"empirical arm, and the lane records it as such rather than burying it")

print("""
  C6 -- THE LENGTH.  What is the SMALLEST smoothing length that meets each gate?  This is the number the
  rest of the lane has to price.
""")
LNEED = {}
for foot in A0:
    for Rmax in RMAX_LIST:
        for tag in TAGS:
            for gate, tol in (("theory", TOL_THEORY), ("data", TOL_DATA)):
                ok = [lr_ for lr_ in LGRID if Remb(foot, tag, lr_, Rmax) <= tol]
                LNEED[(foot, Rmax, tag, gate)] = min(ok) if ok else None
print(f"      smallest l_rms [kpc] meeting each gate, canonical footing:")
print(f"      {'R_max[kpc]':>11s} {'gate':>8s}" + "".join(f"{t:>10s}" for t in TAGS))
for Rmax in RMAX_LIST:
    for gate in ("theory", "data"):
        print(f"      {Rmax:11.0f} {gate:>8s}" + "".join(
            f"{(str(int(LNEED[('canonical',Rmax,t,gate)])) if LNEED[('canonical',Rmax,t,gate)] else 'none'):>10s}"
            for t in TAGS))
l_data_100 = [LNEED[(f, 100.0, t, "data")] for f in A0 for t in TAGS if LNEED[(f, 100.0, t, "data")]]
L_REQ = min(l_data_100)
print(f"\n      => on the EMPIRICAL arm at R_max = 100 kpc the mechanism needs l_rms >= {L_REQ:.0f} kpc "
      f"(smallest over kernels and footings; {max(l_data_100):.0f} kpc on the worst realisable kernel).")
print(f"      => on the THEORY arm at R_max = 100 kpc no length works at all: the floor is above the gate.")
check("C6 [test] the required smoothing length is smaller than the cluster radii the repair is required "
      "at (0.5-2 Mpc), so the trigger still RESOLVES the region it is repairing",
      L_REQ <= 500.0,
      f"NO -- the smallest length meeting even the generous empirical gate is l_rms = {L_REQ:.0f} kpc, "
      f"which is comparable to or larger than the 0.5-2 Mpc shell where the shear shape must be repaired. "
      f"The smoothing that hides a galaxy is not much smaller than the object it must not hide, and C7 "
      f"prices what that costs in the required weight")

print("""
  C7 -- WHAT THE LENGTH COSTS AT THE CLUSTER.  The trigger must still be MONOTONE across 0.5-2 Mpc (so a
  single-valued W exists), its gradient must have the SIGN the required slip needs (so W is INCREASING in
  density, off in the field and off in the cosmological background), and the logarithmic slope
  p_local = d ln W / d ln U it demands there is a naturalness cost in exactly the sense L56 F2 priced.
""")
PLOC, MONO, SIGN = {}, {}, {}
rr_cl = np.exp(np.linspace(math.log(500.0), math.log(2000.0), 16)) * kpc
for foot, a0 in A0.items():
    for tag in ("gauss", "n4"):
        If, Kf, dKf, rmsf = KER[tag]
        for lr_ in (300., 600., 1000., 2000., 3000.):
            l_nom = lr_ * kpc / rmsf; ps, mo, sg = [], [], []
            for i, n in enumerate(WLN):
                c = CLU[n]; rho = rho_prof(c)
                U = smooth_vec(rr_cl, RP, rho, If, l_nom)
                dU = np.gradient(U, rr_cl)
                o = FIT[foot][i]
                gP = np.exp(np.interp(np.log(rr_cl / kpc), np.log(o["rgrid"]),
                                      np.log(np.maximum(o["gP"], 1e-30))))
                dsdr = -2 * gP / C2                      # ds/dr = -2 g_P/c^2
                Wp = dsdr / dU                            # = dW/dU
                mo.append(bool(np.all(np.diff(U) < 0)))
                sg.append(bool(np.all(Wp > 0)))
                sel = np.isfinite(Wp) & (Wp > 0)
                if sel.sum() > 4:
                    ps.append(np.polyfit(np.log(U[sel]), np.log(Wp[sel]), 1)[0] + 1.0)
            PLOC[(foot, tag, lr_)] = float(np.median(ps)) if ps else float("nan")
            MONO[(foot, tag, lr_)] = all(mo); SIGN[(foot, tag, lr_)] = all(sg)
print(f"      {'kernel':>8s} {'l_rms':>7s} {'foot':>10s} {'U monotone':>12s} {'W increasing':>14s} {'p_local':>9s}")
for tag in ("gauss", "n4"):
    for lr_ in (300., 600., 1000., 2000., 3000.):
        for foot in A0:
            print(f"      {tag:>8s} {lr_:7.0f} {foot:>10s} {str(MONO[(foot,tag,lr_)]):>12s} "
                  f"{str(SIGN[(foot,tag,lr_)]):>14s} {PLOC[(foot,tag,lr_)]:9.2f}")
mono_ok = all(MONO.values()); sign_ok = all(SIGN.values())
check("C7a [control] the smoothed trigger is monotone across 0.5-2 Mpc and the required weight has the "
      "sign a workable mechanism needs -- W INCREASING with the smoothed density, so it is off in the "
      "field and off in the cosmological background (which every normalised kernel leaves untouched, A7)",
      mono_ok and sign_ok,
      "both hold for every kernel, every length and both footings -- so a single-valued increasing W(U) "
      "exists and the cosmological-ordering objection that closed L6's screened force does NOT apply here")
L_NEEDED = {f: LNEED[(f, 100.0, "gauss", "data")] for f in A0}
p_at_need = [PLOC[(f, t, L_NEEDED[f])] for f in A0 for t in ("gauss", "n4")]
print(f"      at the length the empirical gate actually needs (l_rms = "
      + ", ".join(f"{f} {L_NEEDED[f]:.0f} kpc" for f in A0)
      + f"): p_local = {min(p_at_need):.2f} - {max(p_at_need):.2f}")
check("C7b [test] the weight the mechanism needs is as gentle as chameleon/symmetron screening "
      "(logarithmic slope <= 3) at the length the gate it can meet actually requires",
      max(p_at_need) <= 3.0,
      f"YES: p_local = {min(p_at_need):.2f} - {max(p_at_need):.2f} at the required l_rms, against 1-3 for "
      f"chameleon and symmetron -- and this is a genuine positive, because L51 needed 6.5-16.0 and L56 "
      f"needed 5.4-22.4 on the depth trigger.  But the trade is explicit and it is printed above: the "
      f"longer the smoothing, the flatter the trigger across the cluster and the steeper the weight must "
      f"be, reaching p_local = {max(PLOC.values()):.1f} at l_rms = 3 Mpc.  The mechanism buys gentleness "
      f"in the weight by spending length, and PART D and PART E price the length")


# ==================================================================================================
sec("PART D -- THE TWO LENGTHS: can the trigger's l differ from the kernel's xi?")
# ==================================================================================================
print("""
  D1 -- CONTROL: L51's operator structure, rebuilt here, because it is what makes the question sharp.
  Varying an added term with an undetermined weight on the ten components of a general static h_mu_nu:
  the FRAME-FREE curvature scalar sources both the 00 equation and the traceless ij equation (so it
  carries the SLIP), while the u-built R_mn u^m u^n sources only the 00 equation (so it carries the
  LENSING).  The MOND kernel J(Y) and its coherence length xi live in the MOND scalar's own sector and
  feed the 00 equation.  So the weight W and the kernel J are attached to DIFFERENT operators.
""")
hs = sp.symbols("h00 h11 h22 h33 h12 h13 h23", real=True)
w1f = sp.Function("w1")(x_, y_, z_); w2f = sp.Function("w2")(x_, y_, z_)
H = sp.zeros(4, 4)
H00 = sp.Function("h00")(x_, y_, z_); H11 = sp.Function("h11")(x_, y_, z_); H22 = sp.Function("h22")(x_, y_, z_)
H33 = sp.Function("h33")(x_, y_, z_); H12 = sp.Function("h12")(x_, y_, z_)
H[0, 0] = H00; H[1, 1] = H11; H[2, 2] = H22; H[3, 3] = H33; H[1, 2] = H12; H[2, 1] = H12
R1g = lin_ricci(H)
S1g = sp.expand(sum(ETA[a, a] * R1g[a, a] for a in range(4)))       # frame-free
S2g = sp.expand(R1g[0, 0])                                          # u-built
def EL(L, F):
    """Euler-Lagrange derivative of int L w.r.t. the function F (second order suffices here)."""
    e = sp.diff(L, F)
    for v in (x_, y_, z_):
        e -= sp.diff(sp.diff(L, sp.Derivative(F, v)), v)
        e += sp.diff(sp.diff(L, sp.Derivative(F, v, 2)), v, 2)
    for a, b in ((x_, y_), (x_, z_), (y_, z_)):
        e += sp.diff(sp.diff(L, sp.Derivative(F, a, b)), a, b)
    return sp.simplify(sp.expand(e))
L1 = sp.expand(w1f * S1g); L2 = sp.expand(w2f * S2g)
row1 = [EL(L1, H00), EL(L1, H11), EL(L1, H12)]
row2 = [EL(L2, H00), EL(L2, H11), EL(L2, H12)]
print(f"      frame-free  w1 S1 : d/dh00 = {row1[0]},  d/dh11 = {row1[1]},  d/dh12 = {row1[2]}")
print(f"      u-built     w2 S2 : d/dh00 = {row2[0]},  d/dh11 = {row2[1]},  d/dh12 = {row2[2]}")
d1_ok = (row1[2] != 0) and (row2[1] == 0) and (row2[2] == 0) and (row2[0] != 0)
check("D1 [control] L51's operator split reproduces: the frame-free term sources the traceless ij "
      "equation and therefore carries the SLIP; the u-built term sources only the 00 equation and "
      "therefore carries the LENSING", d1_ok,
      "so the slip weight W and the MOND kernel J(Y) multiply different operators; nothing in the "
      "variation ties their coefficients, let alone their lengths")

print("""
  D2 -- DOES THE ACTION FORCE l = xi?  The theory's coherence length sits inside the kernel --
  THE_ACTION 2026-09-05 section 1 and PAPER8 eq. (1) both display J(Y + xi^2 q q grad V grad V), and the
  scripts that solve it put a bare xi^2 grad^4 on the scalar (L47's placement audit).  Either way xi is a
  property of the MOND SCALAR's gradient term.  The nonlocal weight is an elliptic operator acting on the
  SOURCE of the frame-free curvature term.  D1 shows those are different operators.  There is therefore
  no identity forcing l = xi -- which is what the brief asked, and the answer is a positive.  The price is
  named at once: the theory then carries TWO independent lengths in the same sector.
""")
check("D2 [test] the trigger's length is free to differ from the kernel's coherence length xi",
      d1_ok,
      "YES -- they multiply different operators (D1), so the action does not force them equal.  This is "
      "the escape the brief named and it survives.  What it costs is a SECOND independent length in the "
      "same sector, related to the first by nothing")

print("""
  D3 -- AND IF THEY WERE FORCED EQUAL, THE LANE WOULD DIE AT ONCE.  L47's exact result for the fourth-order
  carrier equation is M_ph(<r)/M = r^2/(2 xi^2): inside the healing length the scalar responds to the
  enclosed POTENTIAL, and the MOND phantom is cut off.  Put xi at the length PART C requires and read the
  phantom a galaxy would then have.
""")
Mgal_test = 1.0e11 * MSUN; rgal_test = 20.0 * kpc
print(f"      a 1e11 Msun galaxy at 20 kpc: MOND needs a phantom-to-baryon ratio of order "
      f"{float(nu_of(G*Mgal_test/rgal_test**2, A0['canonical'])) - 1:.2f} (the kernel's own boost)")
mond_kill = []
for xi_kpc in (0.004, 0.585, 600.0, 2000.0):
    ratio = (rgal_test / (xi_kpc * kpc)) ** 2 / 2.0
    mond_kill.append(ratio)
    print(f"      xi = {xi_kpc:9.3f} kpc : M_ph(<20 kpc)/M = r^2/(2 xi^2) = {ratio:.3e}")
need = float(nu_of(G * Mgal_test / rgal_test ** 2, A0["canonical"]) - 1)
check("D3 [test] if the action DID force l = xi, galactic MOND would survive at the length PART C needs",
      mond_kill[2] >= need,
      f"NO -- at xi = 600 kpc the cone law gives a phantom-to-baryon ratio of {mond_kill[2]:.2e} at 20 kpc "
      f"against the {need:.2f} the kernel itself requires, i.e. short by {need/mond_kill[2]:.1e}.  So the "
      f"mechanism EXISTS only because D2 holds; if the two lengths were tied, the lane would be dead by "
      f"four orders of magnitude and no further test would be needed")

print("""
  D4 -- DOES THE THEORY HAVE ROOM FOR THE LENGTH IT NEEDS?  Every length the corpus actually carries,
  against the l_rms >= 0.6-2 Mpc PART C requires.  The coherence length is quoted in BOTH of L47's
  placements and the placement used is named: the primary number is the OUTSIDE-J value, 4.00 pc, because
  that is the one L47 obtains from an exact solve of the action's own scalar equation with a symbolically
  verified Green's function and it is identical on both footings; the inside-J value, 585/642 pc, is an
  asymptotic balance and is carried as the alternative.  Neither is close.
""")
LENGTHS = [
    ("xi, outside-J placement, L47 exact solve (both footings)", 4.00 * 3.0857e16 / kpc),
    ("xi, inside-J placement, L47 asymptotic balance (canonical/alt 585/642 pc)", 585.0 * 3.0857e16 / kpc),
    ("xi, the standing PAPER8 value 0.10 / 0.15 pc", 0.10 * 3.0857e16 / kpc),
    ("c / H0 (the one intrinsic length of the cosmology)", c_light / H0_planck / kpc),
    ("c^2 / a0 (L17's unique filter length, canonical)", C2 / A0["canonical"] / kpc),
    ("sqrt(G M_b(cluster) / a0), the cluster MOND radius -- MASS-DEPENDENT, not a constant",
     math.sqrt(G * 1.3e14 * MSUN / A0["canonical"]) / kpc),
    ("a0 / (G rho_b,cosmic)", A0["canonical"] / (G * rho_b_cosmic) / kpc),
]
print(f"      required l_rms: {L_REQ:.0f} - 2000 kpc\n")
print(f"      {'candidate':>74s} {'length [kpc]':>14s} {'dex from required':>19s}")
dexes = []
for nm, Lk in LENGTHS:
    d = math.log10(Lk / L_REQ); dexes.append((abs(d), nm, Lk, d))
    print(f"      {nm:>74s} {Lk:14.4e} {d:+19.2f}")
best_dex = min(d[0] for d in dexes if "MASS-DEPENDENT" not in d[1])
best_nm = [d[1] for d in dexes if d[0] == best_dex][0]
check("D4 [test] a length the theory already carries, or a principled combination of its own constants, "
      "supplies the required smoothing scale to within 0.5 dex",
      best_dex < 0.5,
      f"NO -- the closest fixed candidate is '{best_nm}' at {best_dex:.2f} dex.  The theory's own "
      f"coherence length is {L_REQ*kpc/(4.00*3.0857e16):.1e} x too small in the outside-J placement and "
      f"{L_REQ*kpc/(585.0*3.0857e16):.0f} x too small in the inside-J one; c/H0 and c^2/a0 are 3-4 dex "
      f"too LARGE.  The one candidate of roughly the right size, the cluster MOND radius sqrt(G M/a0), is "
      f"MASS-DEPENDENT and therefore not a kernel length at all -- it is L17's objection, that no single "
      f"operator length serves a range of masses.  The length is set by the cluster data and by nothing "
      f"else")


# ==================================================================================================
sec("PART E -- PRICING THE LENGTH against what already constrains it")
# ==================================================================================================
print("""
  ONE HONESTY NOTE BEFORE ANY NUMBER.  The cluster data fix W'(U) only over the cluster's own range of U.
  Below that range W is a FREE function -- it has to fall to zero somewhere, but how is not measured.  So
  every number in this part is quoted at the REFERENCE value W'(U_cl), and each scales linearly with
  W'(U_sys)/W'(U_cl), which is unknown and is NOT assumed to be <= 1.  (At the lengths the gates require
  the measured p_local is near 1, so W' is roughly flat there; but that is an observation about the
  cluster range, not a bound below it.)  Where the margin is many orders of magnitude -- the Solar System
  and the wide binaries -- no continuation of W could bridge it and the conclusion is robust.  Where the
  margin is a factor of a few -- the groups -- it is NOT robust and the lane says so instead of scoring it.
""")
TAG_E, LE = "n4", 1000.0                       # a realisable kernel and a length that meets the empirical gate
print(f"      working point: kernel {TAG_E} (a realisable elliptic operator of order 4), l_rms = {LE:.0f} kpc")

def ratio_point(tag, l_rms_kpc, R_m, nu=1.0):
    """trigger gradient per unit acceleration for a COMPACT source probed at radius R (mass cancels)"""
    If, Kf, dKf, rmsf = KER[tag]; l_nom = l_rms_kpc * kpc / rmsf
    return abs(float(dKf(R_m, l_nom))) * R_m ** 2 / (nu * G)

print("\n  E1 -- CASSINI AND THE WIDE BINARIES.  L56's window was EMPTY because Cassini capped the amplitude")
print("       from BELOW: a weaker cluster slip needed a shallower weight and a shallow weight is nearly")
print("       scale-free.  Here the suppression is a SCALE effect and needs no steepness at all, so that")
print("       cap does not exist.  Checked, not asserted.")
E1 = {}
for foot in A0:
    for nm, R_m in (("Cassini, Saturn's orbit (9.58 AU)", 9.58 * 1.496e11),
                    ("a wide binary at 10 kAU", 1.0e4 * 1.496e11),
                    ("a globular cluster at 10 pc", 10 * 3.0857e16),
                    ("the Milky Way's OWN slip at 8.2 kpc", 8.2 * kpc)):
        rr = ratio_point(TAG_E, LE, R_m, nu=CLINFO[foot]["nu_e"])
        E1[(foot, nm)] = R_EMB_LOCAL[foot] * rr / RATIO_CL[(foot, TAG_E, LE)]
        if foot == "canonical":
            print(f"      {nm:36s}: R = {E1[(foot, nm)]:.3e}   ({E1[(foot,nm)]/CASSINI:.1e} x Cassini)")
cass = max(E1[(f, "Cassini, Saturn's orbit (9.58 AU)")] for f in A0)
wb = max(E1[(f, "a wide binary at 10 kAU")] for f in A0)
check("E1 [test] the mechanism passes CASSINI and the wide-binary regime",
      cass <= CASSINI and wb <= CASSINI,
      f"YES by {CASSINI/cass:.1e} at Cassini and {CASSINI/wb:.1e} at 10 kAU, on both footings, with NO "
      f"steepness assumed anywhere -- the suppression is (R_p/r_cl)^3 and a Solar-System probe radius is "
      f"{9.58*1.496e11/(RCL_EVAL*kpc):.1e} of a cluster radius.  L56 E3's pincer, in which Cassini capped "
      f"the amplitude from below, is LIFTED.  This is the second real positive of the lane")

print("\n  E2 -- DISC OUTSKIRTS AND ISOLATED FIELD GALAXIES, on the real SPARC profiles.")
SPARC_R = []
for gname in GALS:
    gd = GALS[gname]; Mb = float(gd["M"][-1]); rlast = float(gd["r"][-1])
    rd = max(rlast / 4.0, 0.3 * kpc)                       # a STATED model: exponential sphere, r_d = R_last/4
    prof = gal_profile(Mb, rd)
    rgv, _, _ = ratio_gal_of(TAG_E, LE, min(300.0, 3 * rlast / kpc), prof=prof,
                             nu=CLINFO["canonical"]["nu_e"], npts=12)
    SPARC_R.append(R_EMB_LOCAL["canonical"] * rgv / RATIO_CL[("canonical", TAG_E, LE)])
SPARC_R = np.array(SPARC_R)
print(f"      {len(SPARC_R)} SPARC galaxies, each given its OWN measured baryonic mass and its own size "
      f"(r_d = R_last/4),\n      probed out to 3 R_last (capped at 300 kpc):")
print(f"      reference response R = {SPARC_R.min():.3e} - {SPARC_R.max():.3e} (median {np.median(SPARC_R):.3e})")
n_pass_da = int((SPARC_R <= TOL_DATA).sum())
check("E2 [test] disc outskirts and isolated field galaxies keep the deposited theory's no-slip result "
      "at the working point (kernel n4, l_rms = 1 Mpc)",
      SPARC_R.max() <= TOL_THEORY,
      f"the reference response reaches {SPARC_R.max():.2e}, i.e. {SPARC_R.max()/TOL_THEORY:.0f} x the "
      f"theory's own 1e-4 and {SPARC_R.max()/TOL_DATA:.2f} x the 20% empirical bound, while the median "
      f"galaxy sits at {np.median(SPARC_R):.1e} and {n_pass_da}/{len(SPARC_R)} clear the 20% bound.  The "
      f"largest values belong to the physically largest discs, probed to 300 kpc, exactly as the "
      f"(R_p/r_cl)^3 law says they must: at THIS working point (l_rms = 1 Mpc) the empirical gate holds "
      f"out to about 150 kpc and not to 300 kpc, and reaching 300 kpc needs l_rms >= 2 Mpc (C6).  The "
      f"theory-arm FAIL is the same one C5a records and is not independent of it")
print("\n  E3 -- X-RAY GROUPS, which is where the mechanism makes its sharpest prediction.")
GRP = []
with open(os.path.join(REPO, "real_research/data/lovisari2015_groups.tsv")) as fh:
    hdr = None
    for line in fh:
        if line.startswith("#") or not line.strip(): continue
        parts = line.rstrip("\n").split("\t")
        if hdr is None: hdr = parts; continue
        d = dict(zip(hdr, parts))
        try:
            R500 = float(d["R500_kpc"]); Mg = float(d["Mgas500_1e12"]) * 1e12
        except Exception: continue
        GRP.append(dict(name=d["name"], R500=R500, Mb=Mg * 1.30 * MSUN))
print(f"      {len(GRP)} X-ray groups (Lovisari, Reiprich & Schellenberger 2015 Tables 1-2), each modelled")
print(f"      as an isothermal sphere rho ~ r^-2 truncated at 2 R500 and normalised to M_gas500 x 1.30 --")
print(f"      a STATED model, and the one that maximises the group's own trigger gradient")
GRPR = []
If4, Kf4, dKf4, rms4 = KER[TAG_E]; l4 = LE * kpc / rms4
for g in GRP:
    rt = 2 * g["R500"] * kpc
    prof = np.where(RP <= rt, g["Mb"] / (4 * math.pi * rt * np.maximum(RP, 1e18) ** 2), 0.0)
    Rq = np.array([0.98, 1.02]) * g["R500"] * kpc
    sm = smooth_vec(Rq, RP, prof, If4, l4)
    grad = abs((sm[1] - sm[0]) / (Rq[1] - Rq[0]))
    gb = G * g["Mb"] * 0.5 / (g["R500"] * kpc) ** 2
    gfw = float(g_kernel(gb, A0["canonical"]))
    GRPR.append(R_EMB_LOCAL["canonical"] * (grad / gfw) / RATIO_CL[("canonical", TAG_E, LE)])
GRPR = np.array(GRPR)
print(f"      bounded group response R = {GRPR.min():.3e} - {GRPR.max():.3e} (median {np.median(GRPR):.3e})")
check("E3 [test] X-ray groups keep the deposited theory's no-slip result at the working point",
      GRPR.max() <= TOL_THEORY,
      f"NO -- the bound reaches {GRPR.max():.2e}, {GRPR.max()/TOL_THEORY:.0e} x the theory's own 1e-4 and "
      f"{GRPR.max()/TOL_DATA:.2f} x the 20% empirical bound (median {np.median(GRPR)/TOL_DATA:.2f} x).  "
      f"Groups are EXTENDED against the smoothing, so the mechanism does not hide them -- that is not a "
      f"bug, it is the mechanism working as designed, and it is the sharpest thing it predicts: a "
      f"lensing-versus-hydrostatic discrepancy in GROUPS of order {100*np.median(GRPR):.0f}%.  Whether "
      f"that is excluded is NOT decided here: this repository's own group-scale estimator disagreement "
      f"(KT2017 vs g06, +0.42 dex on 19 shared hosts) is larger than the effect, so the channel is "
      f"estimator-limited and the lane refuses to score it in either direction")

print("\n  E4 -- THE EXTERNAL FIELD.  A nonlocal trigger IS an external-field effect on the slip: a galaxy's")
print("       weight is set by everything within l_rms of it.  That is a prediction, and it is testable.")
UGAL, UCL = {}, {}
for foot in A0:
    If, Kf, dKf, rmsf = KER[TAG_E]; l_nom = LE * kpc / rmsf
    UCL[foot] = float(np.median([smooth_vec(np.array([RCL_EVAL * kpc]), RP, rho_prof(CLU[n]), If, l_nom)[0]
                                 for n in WLN]))
    UGAL[foot] = float(smooth_vec(np.array([10.0 * kpc]), RP, GPROF, If, l_nom)[0]) + rho_b_cosmic
print(f"      smoothed trigger at l_rms = {LE:.0f} kpc:  cluster at 1 Mpc {UCL['canonical']:.3e} kg/m^3;  "
      f"an isolated 1e11 Msun galaxy {UGAL['canonical']:.3e};  cosmic mean {rho_b_cosmic:.3e}")
sep = UCL["canonical"] / UGAL["canonical"]
print(f"      separation cluster : field galaxy = {sep:.1f} x, and the field galaxy sits "
      f"{UGAL['canonical']/rho_b_cosmic:.2f} x the cosmic mean")
R_work = max(Remb(f, TAG_E, LE, 100.0) for f in A0)
print(f"      => the weight at a field galaxy is smaller than at a cluster by {sep:.0f}^p_local ~ "
      f"{sep**PLOC[('canonical', 'n4', LE)]:.0f} x, so the predicted galaxy-galaxy-lensing slip is "
      f"strongly environment-dependent: at the working point, {100*R_work:.2f}% for a galaxy at cluster\n"
      f"         radii ({100*max(BEST[(f,100.0)][0] for f in A0):.3f}% at the floor) against essentially "
      f"zero in the field.")
check("E4 [test] the environmental dependence the mechanism predicts is already excluded by measurement",
      False,
      "NOT DECIDED, and this is the honest state of it.  The mechanism predicts a lensing-versus-dynamical "
      f"discrepancy of {100*max(BEST[(f,100.0)][0] for f in A0):.3f}% - {100*R_work:.1f}% for galaxies "
      f"sitting at cluster radii and essentially none in the field.  "
      f"Galaxy-galaxy lensing of cluster members is not measured anywhere near 0.1%, so the prediction is "
      f"neither confirmed nor refuted.  It is, however, the measurement that would decide this door, and "
      f"it is named here as such")

print("\n  E5 -- THE COSMOLOGICAL BACKGROUND.  A normalised kernel leaves a homogeneous universe exactly")
print("       where it is (A7), so the background trigger is the cosmic mean and W there is off.  But a")
print("       linear perturbation of wavelength LONGER than l_rms is not smoothed at all, so it is not")
print("       suppressed.  Bounded here with the cluster's own W'.")
lam = 10.0 * Mpc; delta = 1.0
gN_pert = (4 * math.pi / 3) * G * rho_b_cosmic * delta * (lam / 2)
gfw_pert = float(g_kernel(gN_pert, A0["canonical"]))
ratio_pert = (rho_b_cosmic * delta / (lam / 2)) / gfw_pert
R_pert = R_EMB_LOCAL["canonical"] * ratio_pert / RATIO_CL[("canonical", TAG_E, LE)]
print(f"      a delta = 1 perturbation on 10 Mpc: g_fw = {gfw_pert:.2e} m/s^2, bounded slip response "
      f"R = {R_pert:.3e}")
check("E5 [test] the REFERENCE cosmological slip on 10 Mpc scales is under 1%",
      R_pert < 0.01,
      f"bounded at {R_pert:.2e}, i.e. a gravitational slip of order {100*R_pert:.1f}% on 10 Mpc scales.  "
      f"The bound uses the CLUSTER's W' and is therefore a large over-estimate -- the true value depends "
      f"on W below the cluster range, which is unconstrained -- so this is reported as an open channel "
      f"with a named calculation (a Limber cosmic-shear forecast with the pinned W), NOT as a kill and "
      f"NOT as a pass")


# ==================================================================================================
sec("PART F -- THE RUN: the best achievable shear-shape improvement, as a curve")
# ==================================================================================================
print("""
  Four constraints act on the amplitude f of the added lensing phantom.  Unlike L56, only ONE of them is
  a real cap here:
    (1) the lensing-to-dynamics ratio (measured 1.148 +/- 0.146 against the theory's 1.000) caps f ABOVE;
    (2) the embedded-galaxy consistency R_emb = f x (M_P/M_fw) x S caps f ABOVE;
    (3) CASSINI -- which emptied L56's window by capping f from BELOW -- does not cap f at all (E1),
        because the suppression is geometric and needs no steep weight;
    (4) the isolated-galaxy gate is implied by (2) and does not bind separately.
""")
WORK = [("floor (gauss, l_rms = 30 Mpc -- NOT realisable, shown as the ceiling of the mechanism)",
         "gauss", 30000.0),
        ("realisable working point (n4, l_rms = 2 Mpc)", "n4", 2000.0),
        ("realisable working point (n4, l_rms = 1 Mpc)", "n4", 1000.0)]
CURVE, CEIL = {}, {}
for foot in A0:
    rows = BASE[foot]; tab = []
    for f in np.concatenate([np.geomspace(1e-6, 0.09, 30), np.linspace(0.1, 1.0, 46)]):
        dsl = np.array([np.polyfit(np.log(r["Rf"]), np.log((1 - f) * r["DSfw"] + f * r["DSwl"]), 1)[0] - r["swl"]
                        for r in rows])
        m = float(dsl.mean()); e = float(dsl.std(ddof=1) / math.sqrt(len(dsl)))
        row = dict(f=f, z_shape=abs(m) / max(e, 1e-9), z_ld=abs((1.0 + f * R_EMB_LOCAL[foot]) - Rmeas) / eRmeas)
        for lab, tag, lr_ in WORK:
            for Rmax in RMAX_LIST:
                row[(tag, lr_, Rmax)] = f * Remb(foot, tag, lr_, Rmax)
        tab.append(row)
    CURVE[foot] = tab
print(f"      the curve, canonical footing.  R_emb columns are at R_max = 100 kpc.")
print(f"      {'f':>9s} {'shape sig':>10s} {'lens/dyn sig':>13s} {'R_emb floor':>13s} {'R_emb n4 2Mpc':>15s} "
      f"{'R_emb n4 1Mpc':>15s}")
for row in CURVE["canonical"][::8] + [CURVE["canonical"][-1]]:
    print(f"      {row['f']:9.2e} {row['z_shape']:10.2f} {row['z_ld']:13.2f} "
          f"{row[('gauss', 30000.0, 100.0)]:13.3e} {row[('n4', 2000.0, 100.0)]:15.3e} "
          f"{row[('n4', 1000.0, 100.0)]:15.3e}")
def ceiling(tab, cond):
    ok = [r for r in tab if r["z_ld"] < 3.0 and cond(r)]
    return (max(ok, key=lambda r: r["f"]), len(ok)) if ok else (tab[0], 0)
print(f"\n      {'constraint set':>62s} {'canonical':>26s} {'alt':>26s}")
CEILROWS = []
for lab, tag, lr_ in WORK:
    for Rmax in RMAX_LIST:
        for gate, tol in (("theory 1e-4", TOL_THEORY), ("empirical 20%", TOL_DATA)):
            out = {}
            for foot in A0:
                r, nok = ceiling(CURVE[foot], lambda rr: rr[(tag, lr_, Rmax)] <= tol)
                out[foot] = (r, nok)
            CEILROWS.append((lab, tag, lr_, Rmax, gate, out))
for lab, tag, lr_, Rmax, gate, out in CEILROWS:
    if Rmax != 100.0: continue
    txt = []
    for foot in A0:
        r, nok = out[foot]
        txt.append("EMPTY -> %.1f sigma" % zs[foot] if nok == 0 else
                   "f <= %.2f -> %.1f sigma" % (r["f"], r["z_shape"]))
    print(f"      {(tag + ' l=' + str(int(lr_)) + ' kpc, ' + gate):>62s} {txt[0]:>26s} {txt[1]:>26s}")
r_gates_only = {f: ceiling(CURVE[f], lambda rr: True) for f in A0}
print(f"\n      gates 1+2 only (L51's own question, reproduced): "
      + ", ".join(f"{f} f <= {r_gates_only[f][0]['f']:.2f} -> {r_gates_only[f][0]['z_shape']:.1f} sigma"
                  for f in A0))
check("F1 [control] gate 1 alone reproduces L51's answer, 8.8 -> 4.9 / 9.0 -> 4.7 sigma",
      abs(r_gates_only["canonical"][0]["z_shape"] - 4.9) < 0.4 and
      abs(r_gates_only["alt"][0]["z_shape"] - 4.7) < 0.4,
      ", ".join(f"{f} -> {r_gates_only[f][0]['z_shape']:.1f} sigma" for f in A0))
best_emp = {}
for foot in A0:
    r, nok = ceiling(CURVE[foot], lambda rr: rr[("n4", 2000.0, 100.0)] <= TOL_DATA)
    best_emp[foot] = (r["z_shape"] if nok else zs[foot], r["f"] if nok else 0.0, nok)
best_th = {}
for foot in A0:
    cands = []
    for lab, tag, lr_ in WORK:
        r, nok = ceiling(CURVE[foot], lambda rr: rr[(tag, lr_, 100.0)] <= TOL_THEORY)
        if nok: cands.append(r["z_shape"])
    best_th[foot] = (min(cands) if cands else zs[foot], bool(cands))
check("F2 [test] subject to ALL the gates, the mechanism removes the cluster shear-shape failure "
      "(residual under 3 sigma)",
      all(best_emp[f][0] < 3.0 for f in A0),
      "NO, and the reason is NOT the new mechanism.  On the EMPIRICAL arm the FULL L51 ceiling is "
      "available -- " + ", ".join(f"{f} {zs[f]:.1f} -> {best_emp[f][0]:.1f} sigma at f <= {best_emp[f][1]:.2f}"
                                  for f in A0) +
      " -- because the embedded-galaxy gate no longer binds and Cassini never did.  But the "
      "lensing-versus-dynamics budget alone still caps the phantom, so the shape failure is HALVED and "
      "not cured; that ceiling is L51's and this mechanism does not move it.  On the theory's own 1e-4 arm "
      "the amplitude is capped instead by the embedded galaxies: the best is " +
      ", ".join(f"{f} {zs[f]:.1f} -> {best_th[f][0]:.1f} sigma" for f in A0) +
      ", and that only at the Gaussian floor with l_rms = 30 Mpc, which is not realisable by a "
      "finite-order operator and is larger than the objects it is meant to select.  At the realisable "
      "working points the theory arm allows f <= 0.03 (l_rms = 2 Mpc, 8.8 -> 8.4 sigma) and nothing at "
      "l_rms = 1 Mpc")

print("""
  F3 -- THE PRICE, counted the way L56 counted it.
""")
print(f"      what is added: (i) a free function W of a NEW variable, the smoothed baryon density;")
print(f"                     (ii) a smoothing LENGTH l_rms, required >= {L_REQ:.0f} kpc, supplied by nothing "
      f"in the theory (D4, closest fixed candidate {best_dex:.1f} dex away);")
print(f"                     (iii) the ORDER n of the elliptic operator, which must be >= 3 for the "
      f"(R_p/r_cl)^3 suppression\n                           (A6) -- n = 1 buys nothing at all and n = 2 "
      f"only the square;")
print(f"                     (iv) the nonlocality is INSTANTANEOUS on the clock's slices (B6).")
print(f"      what it is fitted to: {len(WLN)} cluster shear log-slopes and one lensing-to-dynamics ratio.")
check("F3 [test] the addition is cheap -- one new coupling constant or fewer",
      False,
      f"a new free function of a new variable, plus a length that nothing in the theory supplies, plus an "
      f"integer operator order, fitted to {len(WLN)} cluster shear log-slopes.  A smoothing length fitted "
      f"to five clusters is not a mechanism, and this lane says so: the length is chosen to make the "
      f"embedded-galaxy gate pass, it is 5 orders from the theory's own coherence length, and nothing "
      f"else in the corpus predicts it")


# ==================================================================================================
sec("PART G -- VERDICT")
# ==================================================================================================
usable = (max(BEST[(f, 100.0)][0] for f in A0) <= TOL_THEORY and best_dex < 0.5 and
          all(best_emp[f][0] < 3.0 for f in A0))
check("G1 [VERDICT] the nonlocal functional is a USABLE handle on the cluster shear shape",
      usable,
      "PARTLY, and the three parts have to be kept apart.  (1) IT WORKS AS A MECHANISM: a smoothed "
      "trigger does make the host/substructure distinction L56 proved no local field can make, by a "
      f"factor {gain:.0f} - {gain_max:.0f}, and it clears the embedded-galaxy gate on the EMPIRICAL arm at "
      f"every probe radius, with Cassini and the wide binaries safe by 15-25 orders and the required "
      f"weight GENTLER (p ~ 0.6-1.3) than chameleon screening.  L56's pincer is broken.  (2) IT DOES NOT "
      f"REACH THE THEORY'S OWN NUMBER: the floor is (R_p/r_cl)^3 x M_P/M_fw and at R_max = 100 kpc that is "
      f"{max(BEST[(f,100.0)][0] for f in A0):.1e}, i.e. {max(BEST[(f,100.0)][0] for f in A0)/TOL_THEORY:.1f} x "
      f"the deposited theory's own Phi = Psi to 1e-4, on both footings and for every kernel and length.  "
      f"(3) THE LENGTH IS FITTED, NOT PREDICTED: l_rms >= {L_REQ:.0f} kpc against the theory's own xi = "
      f"4.00 pc, {L_REQ*kpc/(4.00*3.0857e16):.0e} x larger, with the closest principled candidate "
      f"{best_dex:.1f} dex away.  And even at its ceiling the mechanism HALVES the failure -- "
      + ", ".join(f"{f} {zs[f]:.1f} -> {best_emp[f][0]:.1f} sigma" for f in A0) +
      " -- because the lensing-versus-dynamics budget, not the new mechanism, is what caps the phantom")

print("""
  G2 -- WHAT THIS DOES AND DOES NOT DO TO L56's THEOREM.

  L56's theorem is UNTOUCHED and it does NOT become unconditional.  It closes every SINGLE LOCAL trigger,
  and it named this successor precisely.  The successor survives its own first two obstructions --

    * the exactness obstruction (B1): a nonlocal DEPTH trigger is dead, on two independent grounds, and
      was not built here.  What survives is the smoothed CURVATURE family -- the smoothed baryon density
      and the smoothed tidal invariant -- which are blind to both a constant deepening and a uniform
      field.  A smoothed acceleration or potential survives the first test and fails a second one: by
      Newton's theorem the smoothing is EXACTLY invisible to them outside l (B5).
    * the additivity obstruction (B2, = L56 B5): smoothing is linear, so it cannot make a depth
      non-additive.  But it does NOT have to: what an object suffers is set by GRADIENTS, and a compact
      source's contribution to a smoothed gradient is suppressed by the cube of its size.

  SO THE STANDING RECORD SHOULD SAY: the cluster weak-lensing shape has exactly ONE named live mechanism
  in this action -- a slip weighted by the baryon density smoothed on a length of order 1-2 Mpc -- and it
  is live only in the sense that nothing measured excludes it.  It is not a prediction: its length is
  fitted, its order is fitted, its weight is a free function, and it repairs half of the 9 sigma rather
  than the whole of it.  A tuned length fitted to five clusters is not a mechanism, and this one is a
  tuned length fitted to five clusters.

  WHAT WOULD DECIDE IT, in order of decisiveness.
    1. THE LENSING-VERSUS-DYNAMICAL MASS OF GALAXIES INSIDE CLUSTERS, to 0.1%.  The mechanism predicts a
       fractional slip of 0.02% - 2% there and essentially zero for the same galaxies in the field.  That
       environmental contrast is the mechanism's signature and nothing else in this programme predicts it.
    2. GROUP lensing versus hydrostatic masses, to better than 20%.  Groups are EXTENDED against the
       smoothing, so the mechanism does not hide them: it predicts a group-scale lensing-versus-dynamics
       discrepancy of order 20-45%.  This repository's own group estimators disagree by more than that
       (+0.42 dex on 19 shared hosts), so the channel is estimator-limited today.
    3. A COSMIC-SHEAR forecast with the pinned weight.  A perturbation longer than l is not smoothed, so
       the slip is not suppressed there; the reference estimate is a few tenths of a percent on 10 Mpc,
       but it depends on how W is continued below the cluster range, which is a free function.

  WHAT THIS LANE DELIBERATELY DID NOT DO.
    * The five-cluster scatter of the required weight is NOT used anywhere, in either direction (L51 C13b:
      noise-limited, fractional error 1.41).  Every number above is an amplitude or a scaling law.
    * The length was NOT fitted to the shear data and then quoted as a success.  It was DERIVED from the
      gate it has to pass and then priced against everything else, and the price is recorded as a cost.
    * Two approximations run AGAINST the door and are named: the cluster's surroundings beyond 3 R200 are
      replaced by the cosmic mean (understating the floor), and the embedded galaxy's acceleration uses
      the angle-averaged external-field boost rather than the smaller radial one (understating S).
    * Three findings run FOR the door and are recorded as such: the host/substructure distinction is real
      (C4), Cassini's from-below cap is lifted (E1), and the required weight is gentler than chameleon
      screening (C7b).
    * No statement anywhere that data favour this framework over LambdaCDM.  The halo, its NFW profile and
      its concentration relation are LambdaCDM's, imported.
""")

sec("SUMMARY")
print(f"    FAILS: {len(FAILS)}")
for f in FAILS: print(f"      - {f}")
print(f"\n    a0 footings carried on every dimensional number: {A0['canonical']:.4e} / {A0['alt']:.4e} m s^-2")
print( "    deliverables: L57_nonlocal_functional.py, L57_nonlocal_functional.out, L57_NONLOCAL_FUNCTIONAL.md")
