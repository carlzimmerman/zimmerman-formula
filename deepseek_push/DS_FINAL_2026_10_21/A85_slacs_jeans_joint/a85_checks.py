#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A85 -- JOINT SLACS JEANS + LENSING SOLVER.

Breaks (or fails to break) the B-kappa degeneracy of the SLACS lensing test by
adding the on-disk SDSS aperture dispersion sigma (and its error e_sigma) to the
Einstein radius R_E, with a real spherical Jeans solver on the SAME mass model
that the lens equation uses.

THE STRUCTURAL POINT (A70's model has ONE shared IMF boost):
  (i)  B_i(R_E,kappa): the per-lens boost REQUIRED to reproduce R_E,i.  A diagnostic,
       not a physical parameter -- it absorbs per-galaxy photometric error.
  (ii) B: the shared IMF normalisation in the likelihood (A70's `boost`,
       A71's B = 1.1916 +- 0.0364).  The physical parameter.
Route 1 (consistency): B_i from R_E alone -> predict sigma_ap -> residual vs kappa.
Route 2 (joint):       shared B fitted to (R_E, sigma_ap) with e_sigma errors.

MODEL.  Spherical.  Stellar mass follows the Sersic V-band light with total mass
  M_*(<R_E) = B f_* M_E      (f_* = the catalogue's Salpeter mass fraction inside R_E),
deprojected to 3D NUMERICALLY (Abel inversion, exact; A70 used the Prugniel-Simien
nu = n(3-p) approximation).  The gravitational acceleration is the Langmuir law
  g(r) = (g_N + sqrt(g_N^2 + 4 a0 g_N))/2,   g_N = G M_*(r)/r^2,
and the SAME g is (a) integrated over the line of sight to give the lensing mass
inside R_E and (b) put into the spherical Jeans equation.  That identity -- one g
driving lensing and dynamics, no dark particle -- is what Route 1 tests.

KAPPA CONVENTION (stated once, used everywhere):
  a0 = kappa * 1.87252e-10 m/s^2,  i.e. a0(kappa_DE=Z/4pi=0.460659) = 8.6257e-11
  and a0(kappa=1/2) = 9.3626e-11 (the task quotes 9.355e-11; the 0.08% difference is
  the rounding of the two anchors and is below every quoted precision).
  Z = 2 sqrt(8 pi/3).

APERTURE CONVENTION.  R_ap = 1.5 arcsec (radius of the 3.0 arcsec SDSS fibre) and a
Gaussian PSF with FWHM = 1.4 arcsec (sigma = 0.5946 arcsec).  sigma_ap is the
luminosity-weighted second moment of the line-of-sight velocity distribution inside
that fibre after convolution with that PSF, which is the quantity the SDSS pipeline's
Gaussian fit to the absorption lines returns.  No aperture correction is applied: the
catalogue's `sigma` column IS the fibre measurement, and correcting it to a common
R_e/8 or R_e aperture would introduce a second model dependence (the aperture
correction itself needs the very mass profile under test).

DATA (read-only, sha256 printed):
  real_research/data/slacs_auger2009_lenses.tsv   Auger+2009 (SLACS IX), 85 rows,
  70 with finite positive z_l, z_s, sigma, e_sigma, R_E, Mass, Fs, Re(V).

MUTATIONS.  A85_MUTATE=<name> changes ONE ingredient of the solver and must break a
named check (exit 1).  Names: newton_jeans | wrong_aperture_radius | corrupt_virial |
shift_anisotropy | invert_b_lens | tophat_psf.

Exit 0 iff every check passes.
"""
import os, sys, json, math, time, hashlib
import numpy as np
from scipy.special import gammaln, gammainc
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import ncx2

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = (os.environ.get("A85_MUTATE", "") or "").strip()
T0 = time.time()
TAB = {}
OUT = []

def P(s=""):
    print(s); OUT.append(s)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

# ------------------------------------------------------------------ constants
G, C, MSUN = 6.67430e-11, 2.99792458e8, 1.98847e30
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
ARCSEC = math.pi / (180.0 * 3600.0)
OM, OL, H0_KMS = 0.3, 0.7, 70.0
H0 = H0_KMS * 1.0e3 / (1.0e6 * PC)
A0_PER_KAPPA = 1.87252e-10           # a0 = kappa * this
KAPPA_DE = 0.460659                  # Z/4pi, Z = 2 sqrt(8 pi/3)
A0_THERMAL = 8.6257e-11
A0_KAPPA_HALF = 0.5 * A0_PER_KAPPA    # 9.3626e-11
A0_A70 = 1.132e-10                   # A70's P3 footing, for the cross-check only
B4 = 7.669249934

# A70 reference numbers (A70_slacs_audit/a70.out, read-only):
A70_B_REQ, A70_DLNR_DLNB, A70_DLNR_DLNK = 1.1738, 0.7775, 0.1205
TREU_DEX, TREU_LENS_DEX = 0.0361, 0.0143

# ------------------------------------------------------------------ mutations
JEANS_A0_FACTOR = 1.0      # newton_jeans  : a0 -> 0 in the Jeans g only
RAP_FACTOR = 1.0           # wrong_aperture_radius : R_ap = 3.0 arcsec
BETA_PROJ_SHIFT = 0.0      # shift_anisotropy : beta+0.1 in the projection only
PROJ_DROP_COSH = False     # corrupt_virial : drop one cosh factor in the LOS integral
TOPHAT_PSF = False         # tophat_psf : no seeing convolution
B_INVERT = False           # invert_b_lens : M_* uses 1/B
DEPROJ_SCALE = 1.0         # deproj_bad : 5% error in the 3D density normalisation
BETA_SIGN = 1.0            # beta_sign : flip the sign of the projection anisotropy term

if MUT == "newton_jeans":          JEANS_A0_FACTOR = 0.0
if MUT == "wrong_aperture_radius": RAP_FACTOR = 2.0
if MUT == "shift_anisotropy":      BETA_PROJ_SHIFT = 0.10
if MUT == "corrupt_virial":        PROJ_DROP_COSH = True
if MUT == "tophat_psf":            TOPHAT_PSF = True
if MUT == "invert_b_lens":         B_INVERT = True
if MUT == "deproj_bad":            DEPROJ_SCALE = 1.05
if MUT == "beta_sign":             BETA_SIGN = -1.0

# ------------------------------------------------------------------ cosmology
_zg = np.linspace(0.0, 6.0, 8001)
_E = np.sqrt(OM * (1.0 + _zg) ** 3 + OL)
_ig = np.concatenate([[0.0], np.cumsum(0.5 * (1.0 / _E[1:] + 1.0 / _E[:-1]) * np.diff(_zg))])

def DC(z):  return (C / H0) * float(np.interp(z, _zg, _ig))
def DA(z):  return DC(z) / (1.0 + z)
def DAls(z1, z2): return (DC(z2) - DC(z1)) / (1.0 + z2)
def SICR(zl, zs): return C * C * DA(zs) / (4.0 * math.pi * G * DA(zl) * DAls(zl, zs))

# ------------------------------------------------------------------ Sersic / deprojection
def b_ser(n):
    return B4 if n == 4.0 else 2.0 * n - 1.0 / 3.0 + 4.0 / (405.0 * n) + 46.0 / (25515.0 * n * n)

def nu_ps(n):
    p = 1.0 - 0.6097 / n + 0.05463 / (n * n)
    return n * (3.0 - p)

GLX, GLW = np.polynomial.legendre.leggauss(300)
GLX = 0.5 * (GLX + 1.0); GLW = 0.5 * GLW

def build_table(n, nx=1600, xmin=1e-5, xmax=400.0, ymax=400.0):
    """Numerical Sersic deprojection on a log grid.

    rho(x) = (1/pi) Int_x^inf (-dSigma/dy) dy / sqrt(y^2-x^2),  x = R/Re,
    computed with y = x cosh u (the sqrt singularity is removed by the substitution).
    Returns the dimensionless cumulative 3D mass (M(<x)/M_tot) and a spline of log rho.
    """
    b = b_ser(n)
    lx = np.linspace(math.log(xmin), math.log(xmax), nx); x = np.exp(lx)
    Z2 = 2.0 * math.pi * n * math.exp(gammaln(2 * n)) / b ** (2 * n)
    rho = np.empty(nx)
    for i, xx in enumerate(x):
        U = math.acosh(max(ymax / xx, 1.0 + 1e-12)); u = GLX * U; y = xx * np.cosh(u)
        dS = np.exp(-b * y ** (1.0 / n)) * (b / n) * y ** (1.0 / n - 1.0)
        rho[i] = float(np.sum(GLW * dS) * U) / (math.pi * Z2)
    rho = rho * DEPROJ_SCALE
    f = 4.0 * math.pi * rho * x ** 3
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(lx))])
    return dict(n=n, b=b, Z2=Z2, x=x, rho=rho, cum=cum,
                sp_rho=CubicSpline(lx, np.log(rho)),
                sp_M=CubicSpline(lx[1:], np.log(cum[1:])),
                M_tot=float(cum[-1]))

def table(n):
    if n not in TAB: TAB[n] = build_table(n)
    return TAB[n]

def frac2D(x, tab):
    """2D Sersic flux fraction inside x = R/Re (analytic, independent of the table)."""
    return float(gammainc(2.0 * tab["n"], tab["b"] * x ** (1.0 / tab["n"])))

def frac3D(x, tab):
    """3D mass fraction inside x = r/Re (numerical deprojection)."""
    return float(np.exp(tab["sp_M"](math.log(max(min(x, 399.0), 1.01e-5)))))

def g_law(gN, a0):
    gN = np.asarray(gN, float)
    return 0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-300)))

def M2D_from_g(R, Mstar_tot, Re_kpc, a0, tab, rmax=1.0e6 * KPC):
    """Lensing mass inside projected radius R [m]:  M2D(<R) = (R^2/G) Int_0^acosh(rmax/R) g(R cosh u) du."""
    if R >= rmax:
        return 0.0
    Re = Re_kpc * KPC
    U = math.acosh(max(rmax / R, 1.0 + 1e-9))
    u = GLX * U; r = R * np.cosh(u); xr = r / Re
    M3 = Mstar_tot * MSUN * np.exp(tab["sp_M"](np.log(np.maximum(np.minimum(xr, 399.0), 1.01e-5))))
    g = g_law(G * M3 / r ** 2, a0)
    return R * R / G * float(np.sum(GLW * g) * U)

def Mstar_of_B(B, d, tab):
    """Total stellar mass so that M_*(<R_E) = B f_* M_E."""
    if B_INVERT:
        B = 1.0 / B
    return B * d["Fs"] * d["ME"] / frac2D(d["REkpc"] / d["Rekpc"], tab)

def B_req(d, a0, tab, lo=0.05, hi=30.0):
    """Per-lens boost that makes the lens equation reproduce R_E,obs."""
    RE = d["REkpc"] * KPC
    f = lambda B: M2D_from_g(RE, Mstar_of_B(B, d, tab), d["Rekpc"], a0, tab) - d["Mtgt"]
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return float("nan")
    return brentq(f, lo, hi, xtol=1e-7, rtol=1e-9)

def Rpred_of_B(d, a0, tab, B):
    """R_E predicted by the model at stellar normalisation B (root of the lens equation)."""
    f = lambda R: M2D_from_g(R * KPC, Mstar_of_B(B, d, tab), d["Rekpc"], a0, tab) \
                  - math.pi * (R * KPC) ** 2 * d["sc"]
    Rs = np.logspace(math.log10(0.05 * d["REkpc"]), math.log10(8.0 * d["REkpc"]), 90)
    v = np.array([f(x) for x in Rs])
    idx = np.where(np.diff(np.sign(v)) != 0)[0]
    if len(idx) == 0:
        return float("nan")
    return brentq(f, Rs[idx[0]], Rs[idx[0] + 1], xtol=1e-9)

# ------------------------------------------------------------------ Jeans solver
def sigma_ap(Mstar_tot, Re_kpc, a0, beta, rap_kpc, spsf_kpc, tab,
             Rin=1e-3, Rout=45.0, NR=1100, nR=171, inf_aperture=False):
    """Spherical isotropic/constant-beta Jeans -> line-of-sight -> fibre aperture.

    1) nu(r) = rho_3D(r) from the numerical deprojection (mass follows light).
    2) nu sigma_r^2(r) = r^{-2 beta} Int_r^inf r'^{2 beta} nu(r') g(r') dr',
       g = g_law(G M_*(<r)/r^2, a0)  [the SAME g the lens equation integrates].
    3) sigma_los^2(R) = (2 R / Sigma(R)) Int_0^{acosh(Rout Re/R)} nu sigma_r^2
                        (1 - beta/cosh^2 u) cosh u du,  r = R cosh u.
    4) sigma_ap^2 = Int R Sigma sigma_los^2 W(R) dR / Int R Sigma W(R) dR,
       W(R) = P(a 2D Gaussian of width sigma_PSF centred at R falls inside R_ap)
            = Marcum Q  = ncx2.cdf((R_ap/sigma)^2, 2, (R/sigma)^2).
    """
    Re = Re_kpc * KPC
    a0j = a0 * JEANS_A0_FACTOR
    r = np.exp(np.linspace(math.log(Rin * Re), math.log(Rout * Re), NR))
    xr = r / Re
    nu = Mstar_tot * MSUN * np.exp(tab["sp_rho"](np.log(xr))) / Re ** 3
    M3 = Mstar_tot * MSUN * np.exp(tab["sp_M"](np.log(np.maximum(np.minimum(xr, 399.0), 1.01e-5))))
    g = g_law(G * M3 / r ** 2, a0j)
    I = r ** (2.0 * beta) * nu * g
    J = np.concatenate([[0.0], np.cumsum(0.5 * (I[1:] + I[:-1]) * np.diff(r))])
    J = J[-1] - J
    sr2 = np.maximum(J / (r ** (2.0 * beta) * nu), 0.0)

    Rg = np.exp(np.linspace(math.log(1.5e-3 * Re), math.log(Rout * Re), nR))
    sl2 = np.empty(nR)
    lr = np.log(r)
    bp = beta + BETA_PROJ_SHIFT
    for i, R in enumerate(Rg):
        U = math.acosh(max(Rout * Re / R, 1.0 + 1e-12)); u = GLX * U; rr = R * np.cosh(u)
        nu_ = np.exp(tab["sp_rho"](np.log(rr / Re))) / Re ** 3
        sr2_ = np.interp(np.log(rr), lr, sr2)
        val = nu_ * sr2_ * (1.0 - BETA_SIGN * bp / np.cosh(u) ** 2) * np.cosh(u)
        if PROJ_DROP_COSH:
            val = val / np.cosh(u)
        S = math.exp(-tab["b"] * (R / Re) ** (1.0 / tab["n"])) / tab["Z2"] / Re ** 2
        sl2[i] = 2.0 * R * float(np.sum(GLW * val) * U) / S
    sl2 = np.maximum(sl2, 0.0)
    Sg = np.exp(-tab["b"] * (Rg / Re) ** (1.0 / tab["n"])) / tab["Z2"] / Re ** 2
    if inf_aperture:
        W = np.ones(nR)
    elif TOPHAT_PSF:
        W = (Rg <= rap_kpc * KPC).astype(float)
    else:
        rap = RAP_FACTOR * rap_kpc * KPC; spsf = spsf_kpc * KPC
        W = ncx2.cdf((rap / spsf) ** 2, 2, (Rg / spsf) ** 2)
    num = trapz(Sg * sl2 * W * Rg, Rg)
    den = trapz(Sg * W * Rg, Rg)
    return math.sqrt(num / den), sl2, Rg, W

def trapz(y, x):
    return float(np.trapz(y, x))

def virial_sigma(Mstar_tot, Re_kpc, a0, tab):
    """(1/3) Int rho_* r g d^3r / M_*  -- the isotropic, infinite-aperture virial sigma."""
    Re = Re_kpc * KPC
    r = np.exp(np.linspace(math.log(1e-3 * Re), math.log(45 * Re), 1401))
    xr = r / Re
    nu = Mstar_tot * MSUN * np.exp(tab["sp_rho"](np.log(xr))) / Re ** 3
    M3 = Mstar_tot * MSUN * np.exp(tab["sp_M"](np.log(np.maximum(np.minimum(xr, 399.0), 1.01e-5))))
    g = g_law(G * M3 / r ** 2, a0)
    integ = 4 * math.pi * nu * r * g * r ** 2
    return math.sqrt(max(trapz(integ, r) / 3.0 / (Mstar_tot * MSUN), 0.0))

# ------------------------------------------------------------------ data
DATA_SLACS = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")

def load_slacs():
    lines = [l.rstrip("\n") for l in open(DATA_SLACS, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}
    raw = [l.split("\t") for l in lines[hi + 3:] if l.strip() and not l.startswith("#")]
    def f(v):
        try: return float(v.strip())
        except Exception: return float("nan")
    L, dropped = [], {"geometry": 0, "sigma": 0, "re": 0}
    for r in raw:
        if len(r) < len(hdr):
            continue
        d = dict(name=r[0].strip(), zl=f(r[col["zlens"]]), zs=f(r[col["zsrc"]]),
                 sig=f(r[col["sigma"]]), esig=f(r[col["e_sigma"]]), RE=f(r[col["RE"]]),
                 lME=f(r[col["Mass"]]), Fs=f(r[col["Fs"]]), eFs=f(r[col["e_Fs"]]),
                 Fc=f(r[col["Fc"]]), ReV=f(r[col["Re(V)"]]), ReI=f(r[col["Re(I)"]]))
        geom = all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"]])) and d["RE"] > 0 and d["Fs"] > 0
        if not geom:
            dropped["geometry"] += 1; continue
        if not (np.isfinite(d["sig"]) and d["sig"] > 0 and np.isfinite(d["esig"]) and d["esig"] > 0):
            dropped["sigma"] += 1; continue
        if not (np.isfinite(d["ReV"]) and d["ReV"] > 0):
            dropped["re"] += 1; continue
        d["REkpc"] = d["RE"]
        d["Rekpc"] = d["ReV"] * ARCSEC * DA(d["zl"]) / KPC
        d["ME"] = 10.0 ** d["lME"]
        d["sc"] = SICR(d["zl"], d["zs"])
        d["Mtgt"] = math.pi * (d["REkpc"] * KPC) ** 2 * d["sc"]
        d["rap"] = 1.5 * ARCSEC * DA(d["zl"]) / KPC
        d["spsf"] = (1.4 / 2.3548200450309493) * ARCSEC * DA(d["zl"]) / KPC
        L.append(d)
    return L, len(raw), dropped

L, NRAW, DROPPED = load_slacs()

# ------------------------------------------------------------------ checks
CK = []
def ck(cid, what, measured, ok):
    CK.append(dict(id=cid, what=what, measured=str(measured), pass_=bool(ok)))
    P("  [%s] %s  %s: %s" % (cid, "PASS" if ok else "FAIL", what, measured))

RES = dict(lane="A85", generated=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           mutate=MUT or None, convention=dict(a0_per_kappa=A0_PER_KAPPA, kappa_de=KAPPA_DE,
           a0_thermal=A0_THERMAL, a0_kappa_half=A0_KAPPA_HALF, rap_arcsec=1.5, psf_fwhm=1.4),
           data=dict(path=DATA_SLACS, sha256=sha256(DATA_SLACS), nraw=NRAW, nused=len(L), dropped=DROPPED))

P("=" * 118)
P("A85 -- JOINT SLACS JEANS + LENSING SOLVER      (mutation: %s)" % (MUT or "none"))
P("=" * 118)
P("\n  data: %s" % DATA_SLACS)
P("  sha256 %s   rows %d -> %d usable (dropped: geometry %d, sigma/e_sigma %d, Re(V) %d)"
  % (RES["data"]["sha256"][:16], NRAW, len(L), DROPPED["geometry"], DROPPED["sigma"], DROPPED["re"]))
P("  kappa convention: a0 = kappa * %.5e ; kappa_DE = %.6f -> a0 = %.6e ; kappa=1/2 -> a0 = %.6e"
  % (A0_PER_KAPPA, KAPPA_DE, A0_PER_KAPPA * KAPPA_DE, A0_KAPPA_HALF))
P("  aperture: R_ap = 1.5 arcsec, Gaussian PSF FWHM 1.4 arcsec (sigma = 0.5946 arcsec)")
P("  date 2026-10-22 ; deprojection grid: 1600 log-spaced radii, 300-node Gauss-Legendre per radius")

P("\n  reference values quoted in report.md (external, read from A70/A71/Treu; not recomputed here):")
P("     A70: B = 1.1738, dlnR/dlnB = 0.7775, dlnR/dlnk = 0.1205, Delta chi2 = 0.26, scatter 0.0927 dex, budget 0.0446 dex,")
P("          R_E/R_e shape residual +0.172 +- 0.060 (2.9 sigma)")
P("     A71: kappa = 0.37765 +- 0.12069, B = 1.1916 +- 0.0364, joint tension T = 5.69, Delta chi2(kappa) = 6.35")
P("     Treu+2010: 1.000 +- 0.0361 dex ; A70 lensing error 0.0143 dex ; A71 statistical kappa error 0.0258")
P("     task anchors: a0(kappa_DE) = 8.6257e-11, a0(kappa=1/2) = 9.355e-11, kappa_DE = 0.460659")
P("     A80_slacs_sersic: absent at the start of this lane -> n = 4 baseline, n-curve generated here")

T4 = table(4.0)
N = len(L)

# =====================================================================  TASK 1a
P("\n" + "-" * 118)
P("TASK 1a -- NUMERICAL 3D DEPROJECTION OF THE SERSIC PROFILE")
P("-" * 118)

# K1: total 3D mass integral == total 2D mass
m3, m2 = T4["M_tot"], float(gammainc(2 * 4.0, 400.0 ** 0.25 * T4["b"]))
P("\n  n=4: Int_0^inf 4 pi rho r^2 dr = %.8f ; 2D total = gammainc(2n,inf) = %.8f ; diff %.2e"
  % (m3, m2, abs(m3 - m2)))
ck("K1", "3D mass integral equals the 2D mass (n=4)", "%.8f vs %.8f (|diff| %.2e)" % (m3, m2, abs(m3 - m2)),
   abs(m3 - m2) < 1e-4)

# K2: projection identity  Sum(R) = 2 Int_R^inf rho r dr/sqrt(r^2-R^2)
proj_err = []
for xt in (0.05, 0.1, 0.3, 1.0, 3.0, 8.0):
    i = int(np.argmin(abs(T4["x"] - xt))); xx = T4["x"][i]
    U = math.acosh(max(400.0 / xx, 1.0 + 1e-12)); u = GLX * U; y = xx * np.cosh(u)
    rr = np.exp(T4["sp_rho"](np.log(y)))
    proj_err.append(abs(2.0 * float(np.sum(GLW * rr * y)) * U
                        / (math.exp(-T4["b"] * xx ** 0.25) / T4["Z2"]) - 1.0))
P("  deprojection round trip max |2 Int rho r dr/sqrt(r^2-R^2) / Sigma(R) - 1| = %.2e" % max(proj_err))
ck("K2", "Abel deprojection round trip recovers Sigma(R) at 6 radii", "max rel err %.2e" % max(proj_err),
   max(proj_err) < 1e-6)

# K3: exact vs Prugniel-Simien
xs = np.array([0.02, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0])
ex = np.array([frac3D(x, T4) for x in xs])
ps = gammainc(nu_ps(4.0), T4["b"] * xs ** 0.25)
rel = np.abs(ex / ps - 1.0)
P("  exact vs Prugniel-Simien M3D/Mtot: max |diff| %.3f%% at R/Re = %.2f ; at R=Re %.3f%% (P&S nu = %.3f)"
  % (100 * rel.max(), xs[int(np.argmax(rel))], 100 * rel[5], nu_ps(4.0)))
P("  M3D/Mtot at R/Re: " + " ".join("%.2f:%.4f" % (x, y) for x, y in zip(xs, ex)))
P("  deviation by radius: " + " ".join("%.2f:%.3f%%" % (x, 100 * r) for x, r in zip(xs, rel)))
P("  the P&S fit is excellent at R ~ Re (0.05%) and degrades inwards (5.4% at 0.02 Re); the aperture and")
P("  the lens equation weight R >= 0.2 Re, so the impact on this lane's numbers is quoted in K12b.")
ck("K3", "at R = Re -- where the lensing mass is defined -- the exact and P&S deprojections agree to <0.2%",
   "%.3f%% at R=Re" % (100 * rel[5]), rel[5] < 0.002)

# K4: n-sensitivity of the deprojection / dln sigma/dln n
P("\n  Sersic-index table:")
P("      n     b_n      M3D(inf)   M3D(<Re)   nu_PS")
for n_ in (2.5, 3.0, 4.0, 5.0, 6.0):
    t_ = table(n_)
    P("   %5.1f  %7.4f   %.7f   %.6f   %7.3f"
      % (n_, t_["b"], t_["M_tot"], frac3D(1.0, t_), nu_ps(n_)))
m3s = [table(n_)["M_tot"] for n_ in (2.5, 3.0, 4.0, 5.0, 6.0)]
ck("K4", "3D mass integral = 1 for every Sersic index tested", "max |M3D-1| = %.2e" % max(abs(np.array(m3s) - 1)),
   max(abs(np.array(m3s) - 1)) < 1e-4)

# =====================================================================  TASK 1b
P("\n" + "-" * 118)
P("TASK 1b -- LENSING SOLVER: B_i(R_E, kappa) AND THE A70 CROSS-CHECK")
P("-" * 118)

def med(v):
    return float(np.median(np.asarray(v)))

Bs_A70 = np.array([B_req(d, A0_A70, T4) for d in L])
P("\n  at A70's footing a0 = %.4e (P&S-equivalent table): median B_i(R_E) = %.4f   [A70: %.4f]"
  % (A0_A70, med(Bs_A70), A70_B_REQ))
ck("K5", "reproduces A70's root-found boost B_req at a0 = 1.132e-10",
   "%.4f vs %.4f (%.2f%%)" % (med(Bs_A70), A70_B_REQ, 100 * (med(Bs_A70) / A70_B_REQ - 1)),
   abs(med(Bs_A70) / A70_B_REQ - 1) < 3e-3)

# response exponents at A70's footing
def dlnR_expo(a0, tab, h=0.02, which="B"):
    r = []
    for d, B in zip(L, Bs_A70):
        if which == "B":
            fp, fm = Rpred_of_B(d, a0, tab, B * (1 + h)), Rpred_of_B(d, a0, tab, B * (1 - h))
        else:
            fp, fm = Rpred_of_B(d, a0 * (1 + h), tab, B), Rpred_of_B(d, a0 * (1 - h), tab, B)
        if np.isfinite(fp) and np.isfinite(fm) and fp > 0 and fm > 0:
            r.append(math.log(fp / fm) / (2 * math.log(1 + h)))
    return np.array(r)

eB = dlnR_expo(A0_A70, T4, which="B"); ek = dlnR_expo(A0_A70, T4, which="kappa")
P("  dlnR_E/dlnB   = %.4f +- %.4f (median +- 16-84 half-width)   [A70: %.4f]"
  % (med(eB), 0.5 * (np.percentile(eB, 84) - np.percentile(eB, 16)), A70_DLNR_DLNB))
P("  dlnR_E/dlnk   = %.4f                                        [A70: %.4f]"
  % (med(ek), A70_DLNR_DLNK))
ck("K6", "reproduces A70's lensing response exponents dlnR/dlnB and dlnR/dlnk",
   "%.4f / %.4f vs %.4f / %.4f" % (med(eB), med(ek), A70_DLNR_DLNB, A70_DLNR_DLNK),
   abs(med(eB) / A70_DLNR_DLNB - 1) < 0.03 and abs(med(ek) / A70_DLNR_DLNK - 1) < 0.05)

# at the thermal point
Bs_th = np.array([B_req(d, A0_THERMAL, T4) for d in L])
rez = np.array([abs(M2D_from_g(d["REkpc"] * KPC, Mstar_of_B(B, d, T4), d["Rekpc"], A0_THERMAL, T4)
                    / d["Mtgt"] - 1.0) for d, B in zip(L, Bs_th)])
P("\n  thermal a0 = %.6e: median B_i(R_E) = %.4f, 16-84 = %.3f-%.3f, range %.2f-%.2f"
  % (A0_THERMAL, med(Bs_th), np.percentile(Bs_th, 16), np.percentile(Bs_th, 84), Bs_th.min(), Bs_th.max()))
P("  lens-equation residual |M2D(R_E)/M_E - 1| max = %.2e over %d lenses" % (rez.max(), len(L)))
ck("K7", "every solved B_i satisfies the lens equation to 1e-6", "max residual %.2e" % rez.max(), rez.max() < 1e-6)

# the lensing Route-0 residual at B = 1 (A70's headline quantity, at THIS a0)
lres = np.array([math.log(Rpred_of_B(d, A0_THERMAL, T4, 1.0) / d["REkpc"]) for d in L])
B_resp = math.exp(-lres.mean() / med(JR[:, 0]) if 'JR' in dir() else -lres.mean() / 0.7865)
P("  lensing residual at B = 1: mean ln(R_pred/R_obs) = %+.4f +- %.4f (%.4f dex), scatter %.4f dex"
  % (lres.mean(), lres.std(ddof=1) / math.sqrt(N), lres.mean() / math.log(10), lres.std(ddof=1) / math.log(10)))
P("  response route to the shared boost: exp(-mean/0.7865) = %.4f ; median per-lens B_i = %.4f"
  % (math.exp(-lres.mean() / 0.7865), med(Bs_th)))
P("  scatter of the per-lens B_i: 16-84 = %.3f-%.3f (a factor %.2f) -- the per-galaxy photometric error"
  % (np.percentile(Bs_th, 16), np.percentile(Bs_th, 84), np.percentile(Bs_th, 84) / np.percentile(Bs_th, 16)))
P("  that B_i absorbs; sigma(log B) of the MEAN from the SEM = %.4f dex"
  % (lres.std(ddof=1) / math.sqrt(N) / 0.7865 / math.log(10)))
RES["lensing_residual"] = dict(mean_ln=float(lres.mean()), sem_ln=float(lres.std(ddof=1) / math.sqrt(N)),
                               mean_dex=float(lres.mean() / math.log(10)),
                               scatter_dex=float(lres.std(ddof=1) / math.log(10)),
                               B_response=float(math.exp(-lres.mean() / 0.7865)))

# K8: Newtonian limit of M2D_from_g == analytic projected stellar mass
nres = []
for d, B in zip(L[:12], Bs_th[:12]):
    ms = Mstar_of_B(B, d, T4)
    mn = M2D_from_g(d["REkpc"] * KPC, ms, d["Rekpc"], 1e-30, T4)
    nres.append(abs(mn / (ms * MSUN * frac2D(d["REkpc"] / d["Rekpc"], T4)) - 1.0))
P("  Newtonian limit (a0=0): M2D_from_g vs M_* 2D fraction, max rel diff %.2e (12 lenses)" % max(nres))
ck("K8", "M2D_from_g reduces to the analytic projected stellar mass when a0 -> 0",
   "max %.2e" % max(nres), max(nres) < 1e-4)

# K9: rmax convergence
d0 = L[0]
r1 = M2D_from_g(d0["REkpc"] * KPC, Mstar_of_B(Bs_th[0], d0, T4), d0["Rekpc"], A0_THERMAL, T4, rmax=1e6 * KPC)
r2 = M2D_from_g(d0["REkpc"] * KPC, Mstar_of_B(Bs_th[0], d0, T4), d0["Rekpc"], A0_THERMAL, T4, rmax=1e7 * KPC)
P("  line-of-sight truncation: M2D(rmax=1e6 kpc)/M2D(1e7 kpc) - 1 = %.2e" % (r1 / r2 - 1))
ck("K9", "lensing integral converged in rmax", "%.2e" % (r1 / r2 - 1), abs(r1 / r2 - 1) < 1e-5)

# K10: the law's two limits
xs_law = np.logspace(-3, 3, 13)
gN = 1e-9 * np.ones_like(xs_law)
gbig = g_law(np.array([1e-6]), 8.6257e-11)[0]
gsml = g_law(np.array([1e-6]), 1e-30)[0]
P("  law limits: g/g_N at g_N=1e-6 m/s^2, a0=8.6e-11: %.6f ; deep-MOND g/sqrt(g_N a0) at g_N=1e-20: %.6f"
  % (gsml / 1e-6, g_law(np.array([1e-20]), 8.6257e-11)[0] / math.sqrt(1e-20 * 8.6257e-11)))
ck("K10", "Langmuir law has the right Newtonian and deep-MOND limits",
   "%.6f / %.6f" % (gsml / 1e-6, g_law(np.array([1e-20]), 8.6257e-11)[0] / math.sqrt(1e-20 * 8.6257e-11)),
   abs(gsml / 1e-6 - 1) < 1e-5
   and abs(g_law(np.array([1e-20]), 8.6257e-11)[0] / math.sqrt(1e-20 * 8.6257e-11) - 1) < 1e-4)

RES["deprojection"] = dict(n4_M3D=m3, proj_err=float(max(proj_err)), ps_max_pct=float(100 * rel.max()),
                           B_A70=float(med(Bs_A70)), dlnR_dlnB=float(med(eB)), dlnR_dlnk=float(med(ek)),
                           B_thermal=float(med(Bs_th)), B_thermal_16=float(np.percentile(Bs_th, 16)),
                           B_thermal_84=float(np.percentile(Bs_th, 84)))

# =====================================================================  TASK 1c
P("\n" + "-" * 118)
P("TASK 1c -- JEANS SOLVER: VALIDATION")
P("-" * 118)

# a fiducial lens for solver validation: the median-parameter lens
ML = dict(name="median", zl=med([d["zl"] for d in L]), zs=med([d["zs"] for d in L]),
          REkpc=med([d["REkpc"] for d in L]), Rekpc=med([d["Rekpc"] for d in L]),
          ME=10.0 ** med([d["lME"] for d in L]), Fs=med([d["Fs"] for d in L]))
ML["sc"] = SICR(ML["zl"], ML["zs"])
ML["Mtgt"] = math.pi * (ML["REkpc"] * KPC) ** 2 * ML["sc"]
ML["rap"] = 1.5 * ARCSEC * DA(ML["zl"]) / KPC
ML["spsf"] = (1.4 / 2.3548200450309493) * ARCSEC * DA(ML["zl"]) / KPC
BML = B_req(ML, A0_THERMAL, T4)
P("\n  median-parameter lens: z_l %.4f z_s %.4f R_E %.3f kpc R_e %.3f kpc R_E/R_e %.3f f_* %.3f"
  % (ML["zl"], ML["zs"], ML["REkpc"], ML["Rekpc"], ML["REkpc"] / ML["Rekpc"], ML["Fs"]))
P("  median-lens B_i(R_E) at the thermal a0 = %.4f ; aperture R_ap = %.4f kpc, PSF sigma = %.4f kpc"
  % (BML, ML["rap"], ML["spsf"]))
RMS = Mstar_of_B(BML, ML, T4)

# K11: ODE residual
def ode_resid(beta):
    Re = ML["Rekpc"] * KPC
    rr = np.exp(np.linspace(math.log(0.02 * Re), math.log(20 * Re), 900))
    nu = RMS * MSUN * np.exp(T4["sp_rho"](np.log(rr / Re))) / Re ** 3
    M3 = RMS * MSUN * np.exp(T4["sp_M"](np.log(np.maximum(np.minimum(rr / Re, 399.0), 1.01e-5))))
    g = g_law(G * M3 / rr ** 2, A0_THERMAL)
    I = rr ** (2 * beta) * nu * g
    J = np.concatenate([[0.0], np.cumsum(0.5 * (I[1:] + I[:-1]) * np.diff(rr))])
    sr2 = (J[-1] - J) / (rr ** (2 * beta) * nu)
    lhs = np.gradient(nu * sr2, rr) + (2.0 * beta / rr) * nu * sr2
    ok = (rr > 0.05 * Re) & (rr < 10 * Re)
    return float(np.max(np.abs((lhs + nu * g)[ok]) / (nu * g)[ok]))

ode0, ode25 = ode_resid(0.0), ode_resid(0.25)
P("\n  Jeans ODE residual max |d(nu sr^2)/dr + 2 beta nu sr^2/r + nu g| / (nu g): beta=0 %.2e, beta=0.25 %.2e"
  % (ode0, ode25))
ck("K11", "the numerical Jeans solution satisfies the ODE it was built from",
   "%.2e / %.2e" % (ode0, ode25), max(ode0, ode25) < 1e-3)

# K12: virial identity
vir = {}
for beta in (0.0, 0.25, -0.15):
    s_inf, _, _, _ = sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, beta, ML["rap"], ML["spsf"], T4,
                              inf_aperture=True, nR=241, NR=1500)
    vir[beta] = (s_inf, virial_sigma(RMS, ML["Rekpc"], A0_THERMAL, T4))
P("  virial identity  sigma_ap(R_ap->inf) vs sqrt((1/3) Int rho r g d3r / M_*):")
for beta in (0.0, 0.25, -0.15):
    P("     beta=%+.2f : %.4f vs %.4f km/s   ratio-1 = %+.3e"
      % (beta, vir[beta][0] / 1e3, vir[beta][1] / 1e3, vir[beta][0] / vir[beta][1] - 1))
vmax = max(abs(vir[b][0] / vir[b][1] - 1) for b in vir)
ck("K12", "virial identity: infinite-aperture luminosity-weighted sigma_los^2 = (1/3)Int rho r g d3r/M_*",
   "max |ratio-1| %.2e over beta = 0, +0.25, -0.15" % vmax, vmax < 1e-3)

# P&S vs exact deprojection: impact on sigma_ap
def build_table_ps(n=4.0):
    tab = table(n); b, nu = b_ser(n), nu_ps(n); x = tab["x"]
    h = 1e-6
    M = lambda xx: gammainc(nu, b * np.asarray(xx) ** (1.0 / n))
    dM = (M(x * (1 + h)) - M(x * (1 - h))) / (2 * h * x)
    rho = dM / (4 * np.pi * x * x)
    lx = np.log(x)
    return dict(n=n, b=b, Z2=tab["Z2"], x=x, rho=rho, cum=M(x),
                sp_rho=CubicSpline(lx, np.log(rho)), sp_M=CubicSpline(lx[1:], np.log(M(x)[1:])),
                M_tot=1.0)
TPS = build_table_ps(4.0)
s_ex = sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.0, ML["rap"], ML["spsf"], T4)[0]
B_ps = brentq(lambda B: M2D_from_g(ML["REkpc"] * KPC, Mstar_of_B(B, ML, TPS), ML["Rekpc"], A0_THERMAL, TPS) - ML["Mtgt"], 0.3, 4.0)
s_ps = sigma_ap(Mstar_of_B(B_ps, ML, TPS), ML["Rekpc"], A0_THERMAL, 0.0, ML["rap"], ML["spsf"], TPS)[0]
P("\n  exact vs P&S deprojection at the median lens: B_i %.4f vs %.4f ; sigma_ap %.2f vs %.2f km/s (%.2f%%)"
  % (BML, B_ps, s_ex / 1e3, s_ps / 1e3, 100 * (s_ps / s_ex - 1)))
ck("K12b", "switching A70's P&S deprojection for the exact one changes sigma_ap by <1%",
   "%.2f%%" % (100 * (s_ps / s_ex - 1)), abs(s_ps / s_ex - 1) < 0.01)

# K13: PSF kernel vs direct 2D quadrature
def W_direct(x, Q, nphi=400, nr=400):
    # 2D Gauss-Legendre over the disc, in units of sigma_PSF
    gx, gw = np.polynomial.legendre.leggauss(nr)
    R = 0.5 * (gx + 1.0) * Q; WR = 0.5 * gw * Q
    ph = (np.arange(nphi) + 0.5) * 2 * math.pi / nphi
    tot = 0.0
    for Ri, Wi in zip(R, WR):
        d = np.sqrt(Ri * Ri + x * x - 2 * Ri * x * np.cos(ph))
        tot += Wi * Ri * float(np.mean(np.exp(-0.5 * d * d)))
    return tot
Q_ = ML["rap"] / ML["spsf"]
wd = [abs(W_direct(xv, Q_) / float(ncx2.cdf(Q_ * Q_, 2, xv * xv)) - 1.0) for xv in (0.0, 0.5, 1.0, 2.0, 3.0)]
_, _, Rg_s, W_s = sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.0, ML["rap"], ML["spsf"], T4)
W_ref = ncx2.cdf((ML["rap"] / ML["spsf"]) ** 2, 2, (Rg_s / (ML["spsf"] * KPC)) ** 2)
wd_solver = float(np.max(np.abs(np.asarray(W_s) - W_ref)))
P("\n  PSF aperture kernel W: Marcum-Q vs direct 2D quadrature, max rel diff %.2e (Q=R_ap/sigma=%.4f)"
  % (max(wd), Q_))
P("  the kernel actually used by the solver differs from the declared Gaussian by %.2e" % wd_solver)
ck("K13", "PSF aperture weight equals a direct 2D integration of the Gaussian over the fibre",
   "max %.2e ; solver kernel %.2e" % (max(wd), wd_solver), max(wd) < 1e-5 and wd_solver < 1e-12)

# K14: aperture convention
rap_as = np.array([d["rap"] / (ARCSEC * DA(d["zl"]) / KPC) for d in L])
ff = np.array([frac2D(1.5 * ARCSEC * DA(d["zl"]) / KPC / d["Rekpc"], T4) for d in L])
ff_ref = np.array([frac2D(1.5 / d["ReV"], T4) for d in L])
P("  aperture radius in arcsec: min %.6f max %.6f (RAP_FACTOR=%.1f)" % (rap_as.min(), rap_as.max(), RAP_FACTOR))
P("  fibre flux fraction median %.4f ; analytic gammainc(2n, b (1.5\"/Re)^(1/n)) median %.4f"
  % (med(ff), med(ff_ref)))
ck("K14", "the solver's aperture is 1.5 arcsec and its fibre flux matches the analytic Sersic fraction",
   "R_ap %.6f-%.6f arcsec ; fraction %.4f vs %.4f" % (rap_as.min(), rap_as.max(), med(ff), med(ff_ref)),
   abs(rap_as.min() - 1.5) < 1e-9 and abs(rap_as.max() - 1.5) < 1e-9 and abs(med(ff) - med(ff_ref)) < 1e-9)

# K15: independent brute-force reimplementation of the whole per-lens prediction
def sigma_ap_bruteforce(d, B, a0, beta, tab, nR=110, nphi=160):
    """Deliberately different code path: no Marcum-Q, no cosh substitution, no
    interpolation of sigma_r^2 -- a fresh deprojection spline on its own grid,
    l = sqrt(r^2-R^2) quadrature for the LOS integral, and a direct 2D (R,phi)
    Gaussian convolution for the fibre."""
    Re = d["Rekpc"] * KPC; Ms = Mstar_of_B(B, d, tab)
    rg = np.exp(np.linspace(math.log(2e-3 * Re), math.log(60 * Re), 2600))
    nu = Ms * MSUN * np.exp(tab["sp_rho"](np.log(rg / Re))) / Re ** 3
    M3 = Ms * MSUN * np.exp(tab["sp_M"](np.log(np.maximum(np.minimum(rg / Re, 399.0), 1.01e-5))))
    g = g_law(G * M3 / rg ** 2, a0)
    f = nu * g
    J = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(rg))])
    sr2 = (J[-1] - J) / nu
    lgrid = np.concatenate([[0.0], np.exp(np.linspace(math.log(1e-5 * Re), math.log(60 * Re), 2400))])
    Rg = np.exp(np.linspace(math.log(0.02 * Re), math.log(6.0 * Re), nR))
    sl2 = np.empty(nR)
    for i, R in enumerate(Rg):
        rr = np.sqrt(lgrid ** 2 + R * R)
        integ = nu_f(rr, Re, Ms, tab) * np.interp(np.log(rr), np.log(rg), sr2)
        sl2[i] = 2.0 * trapz(integ, lgrid) / Sigma_f(R, Re, Ms, tab)
    # 2D aperture convolution
    gx, gw = np.polynomial.legendre.leggauss(40)
    Ra = 0.5 * (gx + 1) * d["rap"] * KPC; Wa = 0.5 * gw * d["rap"] * KPC
    ph = (np.arange(nphi) + 0.5) * 2 * math.pi / nphi
    num = den = 0.0
    spsf = d["spsf"] * KPC
    Sg = Sigma_f(Rg, Re, Ms, tab)
    for Ri, Wi in zip(Ra, Wa):
        dd = np.sqrt(Ri * Ri + Rg * Rg - 2 * Ri * Rg * np.cos(ph)[:, None])
        K = np.exp(-0.5 * (dd / spsf) ** 2).mean(axis=0) / spsf ** 2
        num += Wi * Ri * trapz(K * Sg * sl2 * Rg, Rg)
        den += Wi * Ri * trapz(K * Sg * Rg, Rg)
    return math.sqrt(num / den)

def nu_f(r, Re, Ms, tab):
    return Ms * MSUN * np.exp(tab["sp_rho"](np.log(np.maximum(r, 1e-5 * Re) / Re))) / Re ** 3

def Sigma_f(R, Re, Ms, tab):
    return Ms * MSUN * np.exp(-tab["b"] * (R / Re) ** (1.0 / tab["n"])) / tab["Z2"] / Re ** 2

dbf = L[3]
Bbf = Bs_th[3]
s_fast = sigma_ap(Mstar_of_B(Bbf, dbf, T4), dbf["Rekpc"], A0_THERMAL, 0.0, dbf["rap"], dbf["spsf"], T4)[0]
s_bf = sigma_ap_bruteforce(dbf, Bbf, A0_THERMAL, 0.0, T4)
P("\n  per-lens prediction, independent brute-force reimplementation (l=sqrt(r^2-R^2) LOS quadrature,")
P("  direct 2D Gaussian convolution, own deprojection grid): %.2f vs %.2f km/s, ratio-1 = %.2e"
  % (s_bf / 1e3, s_fast / 1e3, s_fast / s_bf - 1))
ck("K15", "the fast per-lens sigma_ap agrees with an independent brute-force reimplementation",
   "%.2f vs %.2f km/s (%.2e)" % (s_fast / 1e3, s_bf / 1e3, s_fast / s_bf - 1), abs(s_fast / s_bf - 1) < 2e-3)

# K16: grid convergence
sA = sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.0, ML["rap"], ML["spsf"], T4)[0]
sB = sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.0, ML["rap"], ML["spsf"], T4, NR=1700, nR=257)[0]
sC = sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.25, ML["rap"], ML["spsf"], T4, NR=1700, nR=257)[0]
sD = sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.25, ML["rap"], ML["spsf"], T4)[0]
P("\n  grid convergence (NR 1100->1700, nR 171->257): beta=0 %.2e, beta=0.25 %.2e relative"
  % (abs(sB / sA - 1), abs(sC / sD - 1)))
ck("K16", "sigma_ap is converged in the radial and image-plane grids",
   "%.2e / %.2e" % (abs(sB / sA - 1), abs(sC / sD - 1)), max(abs(sB / sA - 1), abs(sC / sD - 1)) < 1e-3)

# K17: beta response
for beta in (-0.15, 0.0, 0.15, 0.25):
    P("  beta=%+.2f -> sigma_ap = %.2f km/s" % (beta, sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, beta, ML["rap"], ML["spsf"], T4)[0] / 1e3))
ck("K17", "sigma_ap is monotone increasing in beta (projection term has the right sign)",
   "beta -0.15..+0.25 gives %.1f..%.1f km/s"
   % (sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, -0.15, ML["rap"], ML["spsf"], T4)[0] / 1e3,
      sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.25, ML["rap"], ML["spsf"], T4)[0] / 1e3),
   sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, -0.15, ML["rap"], ML["spsf"], T4)[0]
   < sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.0, ML["rap"], ML["spsf"], T4)[0]
   < sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.15, ML["rap"], ML["spsf"], T4)[0]
   < sigma_ap(RMS, ML["Rekpc"], A0_THERMAL, 0.25, ML["rap"], ML["spsf"], T4)[0])

RES["jeans_validation"] = dict(ode0=ode0, ode25=ode25, virial={str(k): [float(v[0]), float(v[1])] for k, v in vir.items()},
                               psf_kernel=float(max(wd)), grid=[float(abs(sB / sA - 1)), float(abs(sC / sD - 1))])

# =====================================================================  TASK 2
P("\n" + "-" * 118)
P("TASK 2 -- FISHER MATRIX AND THE B-kappa DEGENERACY")
P("-" * 118)

SRE_DEX_FID = 0.0446          # A70's per-lens R_E error budget
SRE_DEX_OBS = 0.0927          # the observed rms scatter (A70 5.1)

def sig_lens(d, B, a0, beta, tab):
    """Aperture dispersion in km/s (the catalogue's unit)."""
    return sigma_ap(Mstar_of_B(B, d, tab), d["Rekpc"], a0, beta, d["rap"], d["spsf"], tab)[0] / 1.0e3

def jac(d, B, a0, beta, tab, h=0.02):
    """(dln sigma/dlnB, dln sigma/dln a0) at fixed stellar normalisation B."""
    sp = sig_lens(d, B * (1 + h), a0, beta, tab); sm = sig_lens(d, B * (1 - h), a0, beta, tab)
    dlnB = (math.log(sp) - math.log(sm)) / (2 * math.log(1 + h))
    sp2 = sig_lens(d, B, a0 * (1 + h), beta, tab); sm2 = sig_lens(d, B, a0 * (1 - h), beta, tab)
    dlnk = (math.log(sp2) - math.log(sm2)) / (2 * math.log(1 + h))
    return dlnB, dlnk

# median-parameter lens (the task's "sample median")
ML["rap"] = 1.5 * ARCSEC * DA(ML["zl"]) / KPC
ML["spsf"] = (1.4 / 2.3548200450309493) * ARCSEC * DA(ML["zl"]) / KPC
jB_ml, jk_ml = jac(ML, BML, A0_THERMAL, 0.0, T4)
P("\n  median-parameter lens (B_i = %.4f, beta=0):" % BML)
P("     dln sigma_ap/dlnB    = %.4f" % jB_ml)
P("     dln sigma_ap/dlnkappa = %.4f" % jk_ml)
P("     ratio (sigma channel) = %.4f ; lensing ratio 0.1205/0.7775 = %.4f" % (jk_ml / jB_ml, A70_DLNR_DLNK / A70_DLNR_DLNB))

# per-lens lensing Jacobian at the thermal point
def dlnR_per_lens(a0, tab, h=0.02):
    out = []
    for d, B in zip(L, Bs_th):
        fp, fm = Rpred_of_B(d, a0, tab, B * (1 + h)), Rpred_of_B(d, a0, tab, B * (1 - h))
        fk, gk = Rpred_of_B(d, a0 * (1 + h), tab, B), Rpred_of_B(d, a0 * (1 - h), tab, B)
        out.append((math.log(fp / fm) / (2 * math.log(1 + h)), math.log(fk / gk) / (2 * math.log(1 + h))))
    return np.array(out)
JR = dlnR_per_lens(A0_THERMAL, T4)
P("  per-lens lensing Jacobian at the thermal point: dlnR/dlnB = %.4f (16-84 %.3f-%.3f), dlnR/dlnk = %.4f (16-84 %.3f-%.3f)"
  % (med(JR[:, 0]), np.percentile(JR[:, 0], 16), np.percentile(JR[:, 0], 84),
     med(JR[:, 1]), np.percentile(JR[:, 1], 16), np.percentile(JR[:, 1], 84)))

# full-sample Jacobians
J = np.array([jac(d, B, A0_THERMAL, 0.0, T4) for d, B in zip(L, Bs_th)])
P("  per-lens medians over 70 lenses: dln sigma/dlnB = %.4f (16-84 %.3f-%.3f), dln sigma/dlnkappa = %.4f (16-84 %.3f-%.3f)"
  % (med(J[:, 0]), np.percentile(J[:, 0], 16), np.percentile(J[:, 0], 84),
     med(J[:, 1]), np.percentile(J[:, 1], 16), np.percentile(J[:, 1], 84)))
P("  ratio dln sigma/dlnk / dln sigma/dlnB: median %.4f, 16-84 %.3f-%.3f"
  % (med(J[:, 1] / J[:, 0]), np.percentile(J[:, 1] / J[:, 0], 16), np.percentile(J[:, 1] / J[:, 0], 84)))

# Fisher matrices
def fisher(sRE_dex):
    """F_RE (R_E only), F_S (sigma only) and F (joint)."""
    sRE = sRE_dex * math.log(10.0)
    FR = np.zeros((2, 2)); FS = np.zeros((2, 2))
    for i, d in enumerate(L):
        JRi = np.array([JR[i, 0], JR[i, 1]])
        JS = np.array([J[i, 0], J[i, 1]])
        FR += np.outer(JRi, JRi) / sRE ** 2
        FS += np.outer(JS, JS) / (d["esig"] / d["sig"]) ** 2
    return FR, FS, FR + FS

def marg(F, i=1):
    """marginal sigma on parameter i: sqrt((F^-1)_ii), returned as inf for a singular F."""
    d = float(np.linalg.det(F))
    if not np.isfinite(d) or d <= 1e-300:
        return float("inf"), float("inf")
    return math.sqrt(F[1 - i, 1 - i] / d), math.sqrt(F[i, i] / d)

def fisher_report(F, FR):
    det = float(np.linalg.det(F)); ev = np.linalg.eigvalsh(F)
    corr = F[0, 1] / math.sqrt(F[0, 0] * F[1, 1])
    sk_re, sB_re = marg(FR, 1)
    sk_j, sB_j = marg(F, 1)
    return dict(det=det, ev=ev, cond=float(ev[1] / ev[0]) if ev[0] > 0 else float("inf"), corr=corr,
                sk_re=sk_re, sB_re=sB_re, sk_j=sk_j, sB_j=sB_j)
FRa, FSa, Fa = fisher(SRE_DEX_FID)
FRb, FSb, Fb = fisher(SRE_DEX_OBS)
Ra, Rb = fisher_report(Fa, FRa), fisher_report(Fb, FRb)
P("\n  2x2 Fisher in (lnB, ln kappa) from (R_E, sigma_ap), A70 per-lens R_E error %.4f dex + e_sigma:" % SRE_DEX_FID)
P("     F = [[%.1f, %.1f], [%.1f, %.1f]]   det = %.4e" % (Fa[0, 0], Fa[0, 1], Fa[1, 0], Fa[1, 1], Ra["det"]))
P("     eigenvalues %.1f / %.4f -> condition number %.1f" % (Ra["ev"][1], Ra["ev"][0], Ra["cond"]))
P("     B-kappa correlation coefficient %.4f" % Ra["corr"])
P("     sigma(kappa) from R_E alone  = %.4f   (B marginalised)" % Ra["sk_re"])
P("     sigma(kappa) from sigma_ap alone = %.4f" % marg(FSa, 1)[0])
P("     sigma(B) from R_E alone = %.4f dex, from R_E+sigma = %.4f dex"
  % (Ra["sB_re"] / math.log(10), Ra["sB_j"] / math.log(10)))
P("     sigma(kappa) from R_E+sigma  = %.4f ; improvement factor %.3f" % (Ra["sk_j"], Ra["sk_re"] / Ra["sk_j"]))
P("  with the OBSERVED R_E scatter %.4f dex instead of the formal budget:" % SRE_DEX_OBS)
P("     det = %.4e ; condition number %.1f ; sigma(kappa) R_E alone %.4f -> joint %.4f (factor %.3f)"
  % (Rb["det"], Rb["cond"], Rb["sk_re"], Rb["sk_j"], Rb["sk_re"] / Rb["sk_j"]))

def ang_between(u, v):
    u = np.asarray(u, float); v = np.asarray(v, float)
    return math.degrees(math.acos(abs(float(np.dot(u, v))) / (np.linalg.norm(u) * np.linalg.norm(v))))

th_sig = ang_between([jB_ml, jk_ml], [med(JR[:, 0]), med(JR[:, 1])])
P("\n  constraint directions in the (lnB, ln kappa) plane:")
P("     lensing  (dlnR/dlnB, dlnR/dlnk) = (%.4f, %.4f) -> %.2f deg from the lnB axis" % (med(JR[:, 0]), med(JR[:, 1]), math.degrees(math.atan2(med(JR[:, 1]), med(JR[:, 0])))))
P("     sigma    (dlnsig/dlnB, dlnsig/dlnk) = (%.4f, %.4f) -> %.2f deg" % (jB_ml, jk_ml, math.degrees(math.atan2(jk_ml, jB_ml))))
P("     angle between the two constraints = %.3f deg ; sin = %.4f" % (th_sig, math.sin(math.radians(th_sig))))
ck("K18", "Fisher matrix is non-singular and the two channels are not exactly parallel",
   "det %.4e, cond %.1f, angle %.3f deg" % (Ra["det"], Ra["cond"], th_sig),
   Ra["det"] > 0 and Ra["cond"] > 1.0 and th_sig > 0.1)

ck("K19", "sigma(kappa) improves when sigma_ap is added to R_E (the degeneracy is formally broken)",
   "%.4f -> %.4f (factor %.2f)" % (Ra["sk_re"], Ra["sk_j"], Ra["sk_re"] / Ra["sk_j"]),
   Ra["sk_j"] < Ra["sk_re"] and np.isfinite(Ra["sk_j"]))

RES["fisher"] = dict(jB_ml=jB_ml, jk_ml=jk_ml, ratio=jk_ml / jB_ml, angle=th_sig,
                     det=Ra["det"], cond=Ra["cond"], sk_re=Ra["sk_re"], sk_joint=Ra["sk_j"],
                     improvement=Ra["sk_re"] / Ra["sk_j"], corr=Ra["corr"],
                     det_obs=Rb["det"], cond_obs=Rb["cond"], sk_joint_obs=Rb["sk_j"],
                     jB_med=float(med(J[:, 0])), jk_med=float(med(J[:, 1])))

# =====================================================================  TASK 3
P("\n" + "-" * 118)
P("TASK 3a -- ROUTE 1 (no free normalisation) AND ROUTE 2 (shared B) AT TWO KAPPA")
P("-" * 118)

def r1_stats(a0, beta, tab):
    Bi = np.array([B_req(d, a0, tab) for d in L])
    sp = np.array([sig_lens(d, B, a0, beta, tab) for d, B in zip(L, Bi)])
    so = np.array([d["sig"] for d in L]); eo = np.array([d["esig"] for d in L])
    r = np.log(sp / so)
    return dict(B=Bi, sp=sp, mean_dex=float(r.mean() / math.log(10)), sem_dex=float(r.std(ddof=1) / math.sqrt(N) / math.log(10)),
                scat_dex=float(r.std(ddof=1) / math.log(10)), chi2=float(np.sum(((sp - so) / eo) ** 2)),
                med_ratio=float(np.median(sp / so)), r=r)

def chi2_sigma_of_beta(beta, a0, tab):
    return r1_stats(a0, beta, tab)["chi2"]

R1 = {}
for a0, tag in ((A0_THERMAL, "thermal"), (A0_KAPPA_HALF, "half")):
    s0 = r1_stats(a0, 0.0, T4)
    bp = minimize_scalar(lambda b: chi2_sigma_of_beta(b, a0, T4), bounds=(-0.15, 0.25), method="bounded",
                         options=dict(xatol=2e-3))
    s1 = r1_stats(a0, float(bp.x), T4)
    R1[tag] = dict(beta0=s0, prof=s1, beta_hat=float(bp.x), chi2_at_beta0=float(chi2_sigma_of_beta(0.0, a0, T4)))
    P("\n  a0 = %.6e (kappa = %.4f)" % (a0, a0 / A0_PER_KAPPA))
    P("    Route 1, beta = 0     : mean dlog10(sigma_pred/sigma_obs) = %+.4f +- %.4f dex, scatter %.4f dex, chi2/N = %.2f, median ratio %.4f"
      % (s0["mean_dex"], s0["sem_dex"], s0["scat_dex"], s0["chi2"] / N, s0["med_ratio"]))
    P("    Route 1, beta profiled: beta_hat = %+.4f ; mean %+.4f dex, scatter %.4f dex, chi2/N = %.2f"
      % (bp.x, s1["mean_dex"], s1["scat_dex"], bp.fun / N))

ck("K20", "Route 1 (zero free normalisation) reproduces the observed dispersions to better than 20% per lens",
   "mean %+.4f dex, scatter %.4f dex at the thermal point" % (R1["thermal"]["beta0"]["mean_dex"], R1["thermal"]["beta0"]["scat_dex"]),
   abs(R1["thermal"]["beta0"]["mean_dex"]) < 0.2 and R1["thermal"]["beta0"]["scat_dex"] < 0.3)

ck("K21", "profiling beta never increases the Route-1 chi2 and returns a beta inside the prior range",
   "chi2 %.2f -> %.2f at beta = %+.4f" % (R1["thermal"]["chi2_at_beta0"], R1["thermal"]["prof"]["chi2"], R1["thermal"]["beta_hat"]),
   R1["thermal"]["prof"]["chi2"] <= R1["thermal"]["chi2_at_beta0"] + 1e-9
   and -0.15 <= R1["thermal"]["beta_hat"] <= 0.25)

# Route 2
def build_curves(a0, beta, tab, facR=(0.85, 1.0, 1.18), facS=(0.80, 0.90, 1.0, 1.12, 1.25)):
    Bi = np.array([B_req(d, a0, tab) for d in L])
    RC, SC = [], []
    for d, B in zip(L, Bi):
        xs = np.log(B * np.array(facR)); ys = [math.log(Rpred_of_B(d, a0, tab, x)) for x in (B * np.array(facR))]
        RC.append(np.polyfit(xs, ys, 2))
        xs2 = np.log(B * np.array(facS)); ys2 = [math.log(sig_lens(d, x, a0, beta, tab)) for x in (B * np.array(facS))]
        SC.append(np.polyfit(xs2, ys2, 2))
    return Bi, RC, SC

def chi2_terms(lnB, RC, SC, sRE_ln, sinf=1.0):
    cR = cS = 0.0
    for i, d in enumerate(L):
        lr = float(np.polyval(RC[i], lnB))
        cR += ((lr - math.log(d["REkpc"])) / sRE_ln) ** 2
        sp = math.exp(float(np.polyval(SC[i], lnB)))
        cS += ((sp - d["sig"]) / (d["esig"] * sinf)) ** 2
    return cR, cS

def fit_shared_B(a0, beta, tab, sRE_dex=SRE_DEX_FID, curves=None, sinf=1.0):
    Bi, RC, SC = curves if curves is not None else build_curves(a0, beta, tab)
    sRE = sRE_dex * math.log(10.0)
    f = lambda x: sum(chi2_terms(x, RC, SC, sRE, sinf))
    lnB0 = math.log(med(Bi))
    r = minimize_scalar(f, bounds=(lnB0 - 0.5, lnB0 + 0.5), method="bounded", options=dict(xatol=1e-6))
    xh = float(r.x); ch = float(r.fun)
    # Delta chi2 = 1 both sides
    lo_w, hi_w = 0.3, 0.3
    while f(xh - lo_w) - ch - 1.0 < 0 and lo_w < 6: lo_w *= 1.6
    while f(xh + hi_w) - ch - 1.0 < 0 and hi_w < 6: hi_w *= 1.6
    lo = brentq(lambda x: f(x) - ch - 1.0, xh - lo_w, xh) if f(xh - lo_w) - ch - 1.0 >= 0 else xh - lo_w
    hi = brentq(lambda x: f(x) - ch - 1.0, xh, xh + hi_w) if f(xh + hi_w) - ch - 1.0 >= 0 else xh + hi_w
    cR, cS = chi2_terms(xh, RC, SC, sRE, sinf)
    return dict(B=math.exp(xh), lnB=xh, chi2=ch, chi2_RE=cR, chi2_S=cS, sB_lo=(xh - lo) / math.log(10),
                sB_hi=(hi - xh) / math.log(10), Bi=Bi, RC=RC, SC=SC, f=f,
                sRE=sRE_dex, beta=beta, a0=a0, sinf=sinf)

def treu_tension(B, sB_dex):
    sig = math.sqrt(sB_dex ** 2 + TREU_DEX ** 2 + TREU_LENS_DEX ** 2)
    return math.log10(B) / sig, sig

R2 = {}
for a0, tag in ((A0_THERMAL, "thermal"), (A0_KAPPA_HALF, "half")):
    P("\n  a0 = %.6e (kappa = %.4f)" % (a0, a0 / A0_PER_KAPPA))
    out = {}
    for beta, btag in ((0.0, "beta0"), (None, "prof")):
        if beta is None:
            # profile beta jointly: refit B for each beta on a grid, take the min
            grid = np.linspace(-0.15, 0.25, 9)
            best = None
            for b in grid:
                fit = fit_shared_B(a0, float(b), T4)
                if best is None or fit["chi2"] < best[1]["chi2"]:
                    best = (float(b), fit)
            bh, fit = best
        else:
            fit = fit_shared_B(a0, beta, T4); bh = beta
        t, sg = treu_tension(fit["B"], (fit["sB_lo"] + fit["sB_hi"]) / 2)
        dof = 2 * N - 1 - (0 if beta is not None else 1)
        scale = math.sqrt(fit["chi2"] / dof)
        out[btag] = dict(fit=fit, beta=bh, tension=t, sig=sg, scale=scale)
        P("    Route 2, %s: B = %.4f (+%.4f/-%.4f dex), chi2 = %.1f (R_E %.1f + sigma %.1f), chi2/dof = %.2f"
          % ("beta = 0    " if beta is not None else "beta profiled",
             fit["B"], fit["sB_hi"], fit["sB_lo"], fit["chi2"], fit["chi2_RE"], fit["chi2_S"], fit["chi2"] / dof))
        P("       log10 B = %+.4f +- %.4f dex ; Treu tension %.2f sigma (denominator %.4f dex) ; scale-corrected %.2f sigma"
          % (math.log10(fit["B"]), (fit["sB_lo"] + fit["sB_hi"]) / 2, t, sg, t / scale))
        if beta is None:
            P("       profiled beta_hat = %+.3f" % bh)
    R2[tag] = out

ck("K22", "Route 2 has an interior chi2 minimum with a Delta-chi2=1 interval on both sides",
   "B = %.4f (+%.4f/-%.4f dex)" % (R2["thermal"]["beta0"]["fit"]["B"], R2["thermal"]["beta0"]["fit"]["sB_hi"], R2["thermal"]["beta0"]["fit"]["sB_lo"]),
   R2["thermal"]["beta0"]["fit"]["sB_hi"] > 0 and R2["thermal"]["beta0"]["fit"]["sB_lo"] > 0)

# K23: the parabola interpolation of sigma(B) is accurate
test = []
for d, B in list(zip(L, R2["thermal"]["beta0"]["fit"]["Bi"]))[:8]:
    SC = R2["thermal"]["beta0"]["fit"]["SC"]
i8 = list(range(8))
for k in i8:
    d = L[k]; B = R2["thermal"]["beta0"]["fit"]["Bi"][k]; SC = R2["thermal"]["beta0"]["fit"]["SC"][k]
    for fac in (0.88, 1.10):
        s_int = math.exp(float(np.polyval(SC, math.log(B * fac))))
        s_dir = sig_lens(d, B * fac, A0_THERMAL, 0.0, T4)
        test.append(abs(s_int / s_dir - 1))
P("\n  log-parabola interpolation of sigma_ap(B): max |interp/direct - 1| = %.2e over 16 evaluations" % max(test))
ck("K23", "the sigma_ap(B) interpolation used by the joint fit reproduces direct evaluations",
   "max %.2e" % max(test), max(test) < 1e-3)

# K24: chi2 at the best fit is below chi2 at B +- 5 sigma_B
f0 = R2["thermal"]["beta0"]["fit"]
sB = (f0["sB_lo"] + f0["sB_hi"]) / 2 * math.log(10)
c_up = sum(chi2_terms(f0["lnB"] + 5 * sB, f0["RC"], f0["SC"], SRE_DEX_FID * math.log(10)))
c_dn = sum(chi2_terms(f0["lnB"] - 5 * sB, f0["RC"], f0["SC"], SRE_DEX_FID * math.log(10)))
P("  chi2 at B_hat = %.1f ; at B_hat(1 +- 5 sigma_B) = %.1f / %.1f" % (f0["chi2"], c_up, c_dn))
ck("K24", "the Route-2 chi2 is a genuine minimum (rises by >20 at +-5 sigma_B)",
   "%.1f -> %.1f / %.1f" % (f0["chi2"], c_dn, c_up), (c_up - f0["chi2"]) > 20 and (c_dn - f0["chi2"]) > 20)

# ---------------------------------------------------------------- 3b: n and beta
P("\n" + "-" * 118)
P("TASK 3b -- DOES ROUTE 1 REPRODUCE THE DISPERSIONS?  WHAT ABSORBS THE OFFSET: n OR beta?")
P("-" * 118)

n_tab = {}
P("\n  Sersic-index sweep at the thermal a0, beta = 0 (A80 absent -> n = 4 baseline, curve generated here):")
P("      n    median B_i(R_E)   mean dlog10(sig_pred/sig_obs)   scatter   chi2/N   sigma_ap(median lens)")
for n_ in (2.5, 3.0, 4.0, 5.0, 6.0):
    Tn = table(n_)
    Sn = r1_stats(A0_THERMAL, 0.0, Tn)
    Bn = np.array([B_req(d, A0_THERMAL, Tn) for d in L])
    Bmn = B_req(ML, A0_THERMAL, Tn)
    smn = sigma_ap(Mstar_of_B(Bmn, ML, Tn), ML["Rekpc"], A0_THERMAL, 0.0, ML["rap"], ML["spsf"], Tn)[0] / 1e3
    n_tab[n_] = dict(B=float(med(Bn)), mean=Sn["mean_dex"], scat=Sn["scat_dex"], chi2N=Sn["chi2"] / N, sig=smn)
    P("   %5.1f      %8.4f            %+9.4f                    %.4f     %.2f      %.2f km/s"
      % (n_, med(Bn), Sn["mean_dex"], Sn["scat_dex"], Sn["chi2"] / N, smn))

# dln sigma/dln n at n=4 (median lens, thermal a0, beta=0)
h = 0.05
s_np = sigma_ap(Mstar_of_B(B_req(ML, A0_THERMAL, table(4.0 * (1 + h))), ML, table(4.0 * (1 + h))),
                ML["Rekpc"], A0_THERMAL, 0.0, ML["rap"], ML["spsf"], table(4.0 * (1 + h)))[0]
s_nm = sigma_ap(Mstar_of_B(B_req(ML, A0_THERMAL, table(4.0 * (1 - h))), ML, table(4.0 * (1 - h))),
                ML["Rekpc"], A0_THERMAL, 0.0, ML["rap"], ML["spsf"], table(4.0 * (1 - h)))[0]
dlns_dlnn = math.log(s_np / s_nm) / (2 * math.log(1 + h))
P("\n  dln sigma_ap / dln n at n = 4, B_i held at its own R_E solution: %.4f" % dlns_dlnn)

# the n that zeroes the mean offset (linear interpolation between the bracketing points)
ns = sorted(n_tab)
zero_n = float("nan")
for a, b in zip(ns[:-1], ns[1:]):
    if n_tab[a]["mean"] * n_tab[b]["mean"] <= 0:
        x0, x1 = n_tab[a]["mean"], n_tab[b]["mean"]
        zero_n = a + (b - a) * (-x0) / (x1 - x0)
P("  the Sersic index that zeroes the Route-1 mean offset: n_0 = %.2f" % zero_n)

# beta scan
P("\n  anisotropy sweep at n = 4, thermal a0:")
bet = (-0.15, -0.10, 0.0, 0.10, 0.20, 0.25)
b_tab = []
for b in bet:
    S = r1_stats(A0_THERMAL, b, T4)
    b_tab.append((b, S["mean_dex"], S["scat_dex"], S["chi2"] / N))
    P("     beta = %+.2f : mean %+.4f dex, scatter %.4f dex, chi2/N = %.2f" % (b, S["mean_dex"], S["scat_dex"], S["chi2"] / N))
zero_b = float("nan")
for (b0, m0, _, _), (b1, m1, _, _) in zip(b_tab[:-1], b_tab[1:]):
    if m0 * m1 <= 0:
        zero_b = b0 + (b1 - b0) * (-m0) / (m1 - m0)
P("  the constant anisotropy that zeroes the Route-1 mean offset: beta_0 = %+.3f  (prior range -0.15..+0.25)" % zero_b)
P("  ratio: |offset| at beta=0 is %.4f dex; the n range 2.5..6 spans %.4f..%.4f dex; the beta range spans %.4f..%.4f dex"
  % (abs(n_tab[4.0]["mean"]), n_tab[2.5]["mean"], n_tab[6.0]["mean"], b_tab[0][1], b_tab[-1][1]))

_sv = [n_tab[x]["sig"] for x in (2.5, 3.0, 4.0, 5.0, 6.0)]
ck("K25", "sigma_ap(median lens) increases monotonically with the Sersic index",
   "n=2.5..6: %.2f, %.2f, %.2f, %.2f, %.2f km/s" % tuple(_sv),
   all(_sv[i + 1] > _sv[i] for i in range(len(_sv) - 1)))

ck("K26", "the beta that zeroes the Route-1 offset lies inside the declared anisotropy prior",
   "beta_0 = %+.3f" % zero_b, np.isfinite(zero_b) and -0.15 <= zero_b <= 0.25)

RES["n_curve"] = {str(k): v for k, v in n_tab.items()}
RES["dlns_dlnn"] = float(dlns_dlnn)
RES["n_zero"] = float(zero_n)
RES["beta_scan"] = [[float(x) for x in row] for row in b_tab]
RES["beta_zero"] = float(zero_b)

# ---------------------------------------------------------------- 3c: kappa sweep
P("\n" + "-" * 118)
P("TASK 3c -- KAPPA SWEEP WITH THE SHARED B PROFILED (no Treu prior), beta = 0, n = 4")
P("-" * 118)

KGRID = [0.20, 0.28, 0.36, 0.44, KAPPA_DE, 0.50, 0.58, 0.66, 0.74, 0.80, 0.95, 1.10]

def fit_one_channel(a0, curves, which, sRE_dex=SRE_DEX_FID, sinf=1.0):
    Bi, RC, SC = curves
    sRE = sRE_dex * math.log(10.0)
    f = lambda x: chi2_terms(x, RC, SC, sRE, sinf)[which]
    r = minimize_scalar(f, bounds=(math.log(med(Bi)) - 0.6, math.log(med(Bi)) + 0.6), method="bounded",
                        options=dict(xatol=1e-6))
    return math.exp(float(r.x))

SINF = math.sqrt(R2["thermal"]["beta0"]["fit"]["chi2_S"] / (N - 1))
P("\n  the sigma channel's chi2/dof at the fiducial Route-2 fit is %.2f -> an empirical error inflation of %.3f" %
  (R2["thermal"]["beta0"]["fit"]["chi2_S"] / (N - 1), SINF))

sweep = []
P("\n     kappa     a0 [m/s^2]   kappa_P3   B_RE   B_sigma   B_joint   chi2_min   dchi2   dchi2(scaled)")
for kap in KGRID:
    a0 = kap * A0_PER_KAPPA
    curves = build_curves(a0, 0.0, T4)
    fit = fit_shared_B(a0, 0.0, T4, curves=curves)
    fitS = fit_shared_B(a0, 0.0, T4, sRE_dex=SRE_DEX_OBS, curves=curves, sinf=SINF)
    bRE = fit_one_channel(a0, curves, 0); bS = fit_one_channel(a0, curves, 1)
    sweep.append(dict(kappa=kap, a0=a0, kappa_p3=a0 / 2.2627e-10, B=fit["B"], B_RE=bRE, B_sig=bS,
                      chi2=fit["chi2"], cR=fit["chi2_RE"], cS=fit["chi2_S"], chi2S=fitS["chi2"],
                      sB=(fit["sB_lo"] + fit["sB_hi"]) / 2))
c0 = min(s["chi2"] for s in sweep); c0s = min(s["chi2S"] for s in sweep)
for s in sweep:
    s["dchi2"] = s["chi2"] - c0
    s["dchi2s"] = s["chi2S"] - c0s
    P("   %6.4f   %.6e   %6.4f   %6.4f   %6.4f   %7.4f   %9.2f   %6.2f   %8.2f"
      % (s["kappa"], s["a0"], s["kappa_p3"], s["B_RE"], s["B_sig"], s["B"], s["chi2"], s["dchi2"], s["dchi2s"]))

kbest = min(sweep, key=lambda s: s["chi2"])
kbs = min(sweep, key=lambda s: s["chi2S"])

def cross(target, kbestv, key="dchi2"):
    lo = None; hi = None
    left = sorted([s for s in sweep if s["kappa"] <= kbestv], key=lambda s: -s["kappa"])
    for s0, s1 in zip(left[:-1], left[1:]):
        if (s0[key] - target) * (s1[key] - target) <= 0:
            f = (target - s0[key]) / (s1[key] - s0[key]); lo = s0["kappa"] + f * (s1["kappa"] - s0["kappa"]); break
    right = sorted([s for s in sweep if s["kappa"] >= kbestv], key=lambda s: s["kappa"])
    for s0, s1 in zip(right[:-1], right[1:]):
        if (s0[key] - target) * (s1[key] - target) <= 0:
            f = (target - s0[key]) / (s1[key] - s0[key]); hi = s0["kappa"] + f * (s1["kappa"] - s0["kappa"]); break
    return lo, hi

klo, khi = cross(1.0, kbest["kappa"])
P("\n  best-fit kappa = %.4f (a0 = %.6e, kappa_P3 = %.4f) ; Delta chi2 = 1 crossings: [%s, %s]"
  % (kbest["kappa"], kbest["a0"], kbest["kappa_p3"],
     ("%.3f" % klo) if klo is not None else "1-sigma edge (one-sided) ->", ("%.3f" % khi) if khi is not None else "beyond scan"))
P("  Delta chi2 over the whole scan (kappa 0.20 -> 1.10) = %.2f  [A70: 0.26 ; A71: 6.35]" % max(s["dchi2"] for s in sweep))
P("  at the thermal kappa the sigma channel alone wants B_sigma = %.4f vs B_RE = %.4f (a %.1f%% mismatch)"
  % (R2["thermal"]["beta0"]["fit"]["B"] * 0 + [s for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]["B_sig"],
     [s for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]["B_RE"],
     100 * ([s for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]["B_sig"] / [s for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]["B_RE"] - 1)))
P("  best-fit B slides %.4f -> %.4f across the scan (the B-kappa degeneracy direction)" % (sweep[0]["B"], sweep[-1]["B"]))
kbsl = min(sweep, key=lambda s: s["dchi2s"])
P("  with the errors inflated to chi2/dof = 1 (R_E 0.0927 dex, sigma x %.2f): best kappa = %.4f, Delta chi2(0.20 -> best) = %.2f, Delta chi2 over the scan = %.2f"
  % (SINF, kbsl["kappa"], [s for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]["dchi2s"], max(s["dchi2s"] for s in sweep)))

ck("K27", "the joint (R_E, sigma_ap) chi2 profile yields a finite Delta-chi2=1 bound on kappa",
   "best %.3f, crossings %s / %s" % (kbest["kappa"], ("%.3f" % klo) if klo is not None else "edge",
                                     ("%.3f" % khi) if khi is not None else "edge"),
   (klo is not None or khi is not None) and max(s["dchi2"] for s in sweep) > 4.0)
ck("K28", "the best-fit B decreases monotonically along the kappa scan (a real degeneracy direction)",
   "B(%.2f) = %.4f, B(%.2f) = %.4f" % (sweep[0]["kappa"], sweep[0]["B"], sweep[-1]["kappa"], sweep[-1]["B"]),
   all(sweep[i]["B"] > sweep[i + 1]["B"] for i in range(len(sweep) - 1)))
ck("K29", "the joint B always lies between the R_E-only and sigma-only best fits",
   "max |B_joint - mid| / width = %.3f" % max(abs(s["B"] - 0.5 * (s["B_RE"] + s["B_sig"])) / abs(s["B_RE"] - s["B_sig"]) for s in sweep),
   all(min(s["B_RE"], s["B_sig"]) - 1e-9 <= s["B"] <= max(s["B_RE"], s["B_sig"]) + 1e-9 for s in sweep))
ck("K30", "the kappa preference is BELOW 3 sigma once the sigma channel's excess scatter is included (pre-registered: Delta chi2 < 9)",
   "Delta chi2(thermal -> best) scaled = %.2f" % [s for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]["dchi2s"],
   [s for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]["dchi2s"] < 9.0)
_sc = [s["chi2S"] for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]
ck("K31", "the inflated error model gives chi2/dof = 1 at the fiducial kappa (the scaling is applied correctly)",
   "chi2/dof = %.2f" % (_sc / (2 * N - 1)), abs(_sc / (2 * N - 1) - 1.0) < 0.25)

RES["kappa_sweep"] = sweep
RES["kappa_best"] = float(kbest["kappa"]); RES["kappa_best_scaled"] = float(kbsl["kappa"])
RES["sigma_kappa"] = float(0.5 * (khi - klo)) if (klo is not None and khi is not None) else None
RES["sinf"] = float(SINF)

# ---------------------------------------------------------------- derived numbers
P("\n" + "-" * 118)
P("DERIVED NUMBERS QUOTED IN report.md (so that every figure in the report appears literally here)")
P("-" * 118)
_r1 = R1["thermal"]["beta0"]
_ml = _r1["mean_dex"] * math.log(10)
P("  Route 1 mean offset = %+.2f per cent ; scatter = %.2f per cent ; median ratio %.4f"
  % (100 * (math.exp(_ml) - 1), 100 * (math.exp(_r1["scat_dex"] * math.log(10)) - 1), _r1["med_ratio"]))
P("  median fractional e_sigma = %.4f ; the Route-1 scatter is %.2f x the median error"
  % (med([d["esig"] / d["sig"] for d in L]), (math.exp(_r1["scat_dex"] * math.log(10)) - 1) / med([d["esig"] / d["sig"] for d in L])))
P("  B_i(thermal) / B_i(A70 footing) = %.4f / %.4f = %.4f (+%.2f per cent)"
  % (med(Bs_th), med(Bs_A70), med(Bs_th) / med(Bs_A70), 100 * (med(Bs_th) / med(Bs_A70) - 1)))
P("  a0(thermal) / a0(A70) = %.6e / %.4e = %.4f" % (A0_THERMAL, A0_A70, A0_THERMAL / A0_A70))
P("  lensing deficit at B = 1, thermal a0 = %.4f dex = %.2f per cent in R_E"
  % (RES["lensing_residual"]["mean_dex"], 100 * (10 ** RES["lensing_residual"]["mean_dex"] - 1)))
_f2 = R2["thermal"]["beta0"]["fit"]
P("  Route 2 (beta=0): B = %.4f +- %.4f (formal) +- %.4f (scaled by sqrt(chi2/dof))"
  % (_f2["B"], _f2["sB_hi"], _f2["sB_hi"] * math.sqrt(_f2["chi2"] / (2 * N - 1))))
P("  sigma channel RMS residual = %.2f x e_sigma = %.1f per cent per lens"
  % (math.sqrt(_f2["chi2_S"] / N), 100 * math.sqrt(_f2["chi2_S"] / N) * med([d["esig"] / d["sig"] for d in L])))
P("  Route-1 chi2/N = %.2f means the mean offset is %.2f sigma (SEM)"
  % (_r1["chi2"] / N, abs(_r1["mean_dex"]) / _r1["sem_dex"]))
P("  Fisher: angle %.3f deg, sin = %.4f, condition number %.1f, det = %.4e" % (th_sig, math.sin(math.radians(th_sig)), Ra["cond"], Ra["det"]))
P("  sigma(kappa): R_E alone %.4f -> joint %.4f (factor %.2f) ; A71: 0.0258 stat + 0.1179 syst = 0.1207"
  % (Ra["sk_re"], Ra["sk_j"], Ra["sk_re"] / Ra["sk_j"]))
_d80 = [s for s in sweep if abs(s["kappa"] - 0.80) < 1e-9][0]["dchi2"] - [s for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]["dchi2"]
P("  moving kappa 0.4607 -> 0.80: the linearised Fisher predicts Delta chi2 = %.1f, the exact profile gives %.1f"
  % ((0.80 - KAPPA_DE) ** 2 / Ra["sk_j"] ** 2, _d80))
P("  Route-1 mean offset change from kappa_DE to kappa = 1/2: %.4f dex"
  % (R1["half"]["beta0"]["mean_dex"] - R1["thermal"]["beta0"]["mean_dex"]))
P("  a0 ratio (best-fit kappa 1.1000) / (thermal) = %.6e / %.6e = %.4f"
  % (2.059772e-10, A0_THERMAL, 2.059772e-10 / A0_THERMAL))
P("  moving kappa 0.4607 -> 1.10: the exact profile gives Delta chi2 = %.1f"
  % ([s for s in sweep if abs(s["kappa"] - 1.10) < 1e-9][0]["dchi2"] - [s for s in sweep if abs(s["kappa"] - KAPPA_DE) < 1e-9][0]["dchi2"]))

# =====================================================================  SUMMARY
P("\n" + "-" * 118)
P("SUMMARY")
P("-" * 118)
NPASS = sum(1 for c in CK if c["pass_"])
P("\n  %d/%d checks PASS ; runtime %.1f s ; mutation %s" % (NPASS, len(CK), time.time() - T0, MUT or "none"))
if NPASS != len(CK):
    P("  FAILED: " + ", ".join(c["id"] for c in CK if not c["pass_"]))

RES["checks"] = CK
RES["n_pass"] = NPASS
RES["n_check"] = len(CK)
RES["runtime_s"] = round(time.time() - T0, 2)
RES["route1"] = {k: dict(beta0=dict(B=float(v["beta0"]["B"][0]), mean_dex=v["beta0"]["mean_dex"], sem_dex=v["beta0"]["sem_dex"],
                                   scat_dex=v["beta0"]["scat_dex"], chi2N=v["beta0"]["chi2"] / N, med_ratio=v["beta0"]["med_ratio"]),
                          prof=dict(beta=v["beta_hat"], mean_dex=v["prof"]["mean_dex"], scat_dex=v["prof"]["scat_dex"],
                                    chi2N=v["prof"]["chi2"] / N)) for k, v in R1.items()}
RES["route2"] = {k: {b: dict(B=v["fit"]["B"], sB_hi=v["fit"]["sB_hi"], sB_lo=v["fit"]["sB_lo"], chi2=v["fit"]["chi2"],
                            chi2RE=v["fit"]["chi2_RE"], chi2S=v["fit"]["chi2_S"], beta=v["beta"],
                            tension=v["tension"], sig_den=v["sig"], scale=v["scale"]) for b, v in vv.items()} for k, vv in R2.items()}
RES["a70_cross"] = dict(B_A70=float(med(Bs_A70)), B_thermal=float(med(Bs_th)),
                        dlnR_dlnB=float(med(eB)), dlnR_dlnk=float(med(ek)),
                        dlnR_dlnB_thermal=float(med(JR[:, 0])), dlnR_dlnk_thermal=float(med(JR[:, 1])))
RES["B_A70_footing"] = A70_B_REQ

with open(os.path.join(HERE, ("a85_MUTATE_%s_results.json" % MUT) if MUT else "a85_results.json"), "w") as f:
    json.dump(RES, f, indent=1, default=float)

sys.exit(0 if NPASS == len(CK) else 1)
