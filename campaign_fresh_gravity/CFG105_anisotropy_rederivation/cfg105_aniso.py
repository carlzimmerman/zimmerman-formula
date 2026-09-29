#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG105 independent re-derivation of CFG113's headline (GC orbital anisotropy vs the law's SLUGGS deficit).
Spec: CFG105_SPEC_FROZEN.txt (frozen before any run; its sha256 is printed).  Env: ZF_REPO (repo root; else searched upward from the
script and the cwd), MUTATE=0|1|2, STAGE=controls|all.
REUSED from CFG76 (cfg76_sluggs_jam.py), copied with the absolute path replaced: data loading, GC clipping/binning, kernels, Hernquist
stars, JAM calibration, NFW/collapse-debris rule machinery.  WRITTEN NEW here: the anisotropic Jeans solver (on-demand Gauss-Legendre,
general tracer / general beta(r)), all controls, the attack rows.  CFG76's own sigma_r2/sigma_los are copied ONLY as the C1 comparison.
No CFG113 file is read or imported by this script."""
import os, sys, math, json, hashlib, time
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.special import gammaln

HERE = os.path.dirname(os.path.abspath(__file__))
def find_repo():
    cands = []
    if os.environ.get("ZF_REPO"): cands.append(os.environ["ZF_REPO"])
    for start in (HERE, os.getcwd()):
        p = start
        for _ in range(12):
            cands.append(p); p = os.path.dirname(p)
    for c in cands:
        if os.path.isdir(os.path.join(c, "real_research", "data")): return c
    raise SystemExit("repo root not found: set ZF_REPO")
REPO = find_repo()
DATA = os.path.join(REPO, "real_research", "data")
MUTATE = int(os.environ.get("MUTATE", "0"))
STAGE = os.environ.get("STAGE", "all")
PROJ = 0.0 if MUTATE == 2 else 1.0        # MUTATE=2: drop the anisotropy projection factor (1 - beta R^2/r^2)
spec = open(os.path.join(HERE, "CFG105_SPEC_FROZEN.txt"), "rb").read()
out_lines = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); out_lines.append(s)
P("CFG105  MUTATE=%d STAGE=%s  spec sha256 %s  repo=%s" % (MUTATE, STAGE, hashlib.sha256(spec).hexdigest()[:16], os.path.basename(REPO)))
FAILS = []
def check(name, ok, detail=""):
    P(("  [PASS] " if ok else "  [FAIL] ") + name + ("   (" + detail + ")" if detail else ""))
    if not ok: FAILS.append(name)

# ------------------------------------------------------------------ constants (CFG76 / hunt_lib values)
G = 6.674e-11; kpc = 3.0857e19; Mpc = 3.0857e22; Msun = 1.989e30
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
FB = 0.02237 / (0.02237 + 0.1200)
ARCSEC = 206264.806
FOOTS = ("canonical", "alt")

# ------------------------------------------------------------------ kernel (plain RAR; floor 1e-40 instead of CFG76's 1e-12: only matters beyond 1e7 kpc)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-40)
    return 1.0 / (-np.expm1(-np.sqrt(y)))
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
KERN = nu_rar

# ------------------------------------------------------------------ data (CFG76, copied)
def read_viz(fname):
    lines = [l.rstrip("\n") for l in open(os.path.join(DATA, fname), encoding="latin-1") if l.strip() and not l.startswith("#")]
    i = next(k for k, l in enumerate(lines) if set(l.replace("\t", "").strip()) <= set("- "))
    hdr = [h.strip() for h in lines[i - 2].split("\t")]
    return hdr, [l.split("\t") for l in lines[i + 1:]]
def col(hdr, rec, name, cast=float, default=np.nan):
    try:
        v = rec[hdr.index(name)].strip()
        return cast(v) if v else default
    except Exception:
        return default
hg, rg_ = read_viz("sluggs_forbes2017_galaxies.tsv")
GAL = {}
for r in rg_:
    n = col(hg, r, "NGC", int, None)
    if n is None: continue
    GAL[n] = dict(ngc=n, D=col(hg, r, "Dist"), lMs=col(hg, r, "logM*"), Re_as=col(hg, r, "Reff"), vsys=col(hg, r, "Vsys"),
                  ra=col(hg, r, "RAJ2000"), de=col(hg, r, "DEJ2000"))
hv, rv_ = read_viz("sluggs_forbes2017_gcvel.tsv")
def load_gcs():
    keys = {f"NGC{n:04d}": n for n in GAL}      # h50's key (silently drops 3-digit NGCs), as CFG55/76/113 baseline
    GC = {n: [] for n in GAL}; nall = 0
    for r in rv_:
        nm = col(hv, r, "Star", str, ""); pre = nm.split("_")[0]
        n = keys.get(pre, None)
        if n is None: continue
        v = col(hv, r, "HRV"); ev = col(hv, r, "e_HRV"); rg = col(hv, r, "Rgal")
        ra = col(hv, r, "RAJ2000"); de = col(hv, r, "DEJ2000")
        if not (np.isfinite(v) and np.isfinite(rg) and np.isfinite(ra) and np.isfinite(de)): continue
        nall += 1; g = GAL[n]
        dra = (ra - g["ra"]) * math.cos(math.radians(de)); dde = de - g["de"]
        GC[n].append((rg, v, ev if np.isfinite(ev) else 15.0, math.degrees(math.atan2(dde, dra))))
    return GC, nall
def mle_sigma(v, e):
    v = np.asarray(v, float); e = np.asarray(e, float)
    s2 = max(v.var() - (e ** 2).mean(), 1.0)
    for _ in range(200):
        w = 1.0 / (s2 + e ** 2); mu = (w * v).sum() / w.sum()
        s2n = max((w ** 2 * ((v - mu) ** 2 - e ** 2)).sum() / (w ** 2).sum(), 1.0)
        if abs(s2n - s2) < 1e-6 * s2: s2 = s2n; break
        s2 = s2n
    return mu, math.sqrt(s2)
def clip(rec, vsys, nsig=3.0):
    if len(rec) < 8: return np.zeros((0, 4))
    a = np.array(rec, float); a = a[np.abs(a[:, 1] - vsys) < 1200.0]
    for _ in range(12):
        if len(a) < 8: break
        mu, s = mle_sigma(a[:, 1], a[:, 2])
        keep = np.abs(a[:, 1] - mu) < nsig * math.hypot(s, a[:, 2].mean())
        if keep.all(): break
        a = a[keep]
    return a
ARCMIN = math.pi / 180 / 60
def make_bins(GC):
    B = {}
    for n, g in GAL.items():
        if not (np.isfinite(g["D"]) and np.isfinite(g["lMs"])): continue
        a = clip(GC[n], g["vsys"])
        if len(a) < 30: continue
        D = g["D"]; Rk = a[:, 0] * ARCMIN * D * 1e3; Re = g["Re_as"] / ARCSEC * D * 1e3
        o = np.argsort(Rk); a = a[o]; Rk = Rk[o]
        nb = max(2, min(6, len(a) // 25))
        edges = np.interp(np.linspace(0, len(a), nb + 1), np.arange(len(a) + 1), np.concatenate([Rk, [Rk[-1] * 1.001]]))
        bins = []
        for i in range(nb):
            m = (Rk >= edges[i]) & (Rk < edges[i + 1]) if i < nb - 1 else (Rk >= edges[i])
            if m.sum() < 12: continue
            mu, s = mle_sigma(a[m, 1], a[m, 2]); bins.append((float(np.median(Rk[m])), s, Rk[m].copy()))
        if len(bins) < 2: continue
        Rb = np.array([b[0] for b in bins]); Sb = np.array([b[1] for b in bins])
        out = Rb > max(1.0 * Re, 2.0)
        if out.sum() == 0: out = np.ones(len(Rb), bool)
        B[n] = dict(n=n, N=len(a), Re=Re, Rb=Rb, Sb=Sb, out=out, D=D, lMs=g["lMs"], Rmem=[b[2] for b in bins])
    return B

# ------------------------------------------------------------------ halo / rule machinery (CFG76, copied)
H48 = 67.4
RHO_C = 3 * (H48 * 1e3 / Mpc) ** 2 / (8 * math.pi * G) / Msun * Mpc ** 3
OM48 = 0.315
def cdm(M200c): return 10 ** (0.905 - 0.101 * (math.log10(M200c * 0.674) - 12.0))
def mfun(t): return math.log1p(t) - t / (1 + t)
def nfw_enclosed(Mh, r_kpc):
    c = cdm(Mh); R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
    x = np.clip(np.asarray(r_kpc, float) / R200, 1e-4, 5.0)
    return Mh * (np.log1p(c * x) - c * x / (1 + c * x)) / mfun(c)
def m200m_of_c(M200c):
    c = cdm(M200c); R200 = (3 * M200c / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.)
    f = lambda R: M200c * mfun(c * R / R200) / mfun(c) / (4 * math.pi / 3 * R ** 3) - 200 * OM48 * RHO_C
    R = brentq(f, R200, 20 * R200, xtol=1e-14, rtol=1e-14)
    return M200c * mfun(c * R / R200) / mfun(c), R, R200, c
LMC = np.linspace(8.0, 16.0, 1601); LMM = np.array([math.log10(m200m_of_c(10 ** x)[0]) for x in LMC])
def m200c_from_m200m(M200m): return 10 ** np.interp(math.log10(M200m), LMM, LMC)
T = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "mandelbaum2016_lbg_halo_mass.tsv")) if l.strip() and not l.startswith("#")]
RED = np.array([[float(r[1]), float(r[3])] for r in T[1:] if r[0] == "red"])
def collapse_Mh(Ms):
    lx = np.interp(math.log10(Ms), RED[:, 0], RED[:, 1])
    return float(m200c_from_m200m(10 ** lx / 0.673))
def one_plus_delta_ta(Om):
    OL = 1 - Om
    if OL > 0: t_age = 2.0 / (3 * math.sqrt(OL)) * math.asinh(math.sqrt(OL / Om))
    else: t_age = 2.0 / 3.0
    def tta(k):
        def f(th):
            u = math.sin(th) ** 2
            if u <= 0: return 0.0
            arg = k * Om * (1 / u - 1) + OL * (u * u - 1)
            return 2 * math.sin(th) * math.cos(th) / math.sqrt(max(arg, 1e-300))
        return quad(f, 0, math.pi / 2, limit=200)[0]
    k_lo = max(2 * OL / Om * 1.0000001, 1.0001)
    return brentq(lambda k: tta(k) - t_age, k_lo, 1e4, xtol=1e-12)
GMPC = 4.30091727e-9
H0P, OMP = 67.36, 0.3153
K_TA = one_plus_delta_ta(OMP)
RHOM0 = OMP * 3 * H0P ** 2 / (8 * math.pi * GMPC)
A0_MPC = {f: A0[f] / (1e6 / 3.0856775814913673e22) for f in FOOTS}
def edge_phantom(Mb, foot, kern, xe=0.40):
    a0 = A0_MPC[foot]
    Mlaw = lambda r: Mb * float(kern(np.array([GMPC * Mb / r ** 2 / a0]))[0])
    fn = lambda lr: math.log(Mlaw(math.exp(lr)) / (4 * math.pi / 3 * math.exp(3 * lr) * RHOM0)) - math.log(K_TA)
    rta = math.exp(brentq(fn, math.log(1e-5), math.log(1e3), xtol=1e-13))
    return Mlaw(xe * rta) - Mb
def rule_parts(Ms, foot, kern):
    Mh = collapse_Mh(Ms); Mc = (1 - FB) * Mh
    fex = max(0.0, 1.0 - edge_phantom(Ms, foot, kern) / Mc)
    return fex, Mh

lines = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "atlas3d_fj_table.tsv")) if l.strip() and not l.startswith("#")]
AH = lines[0]; AT = {}
for r in lines[1:]:
    d = dict(zip(AH, r))
    def _fl(v):
        try: return float(v)
        except Exception: return float("nan")
    AT[d["name"]] = {k: (_fl(v) if k != "name" else v) for k, v in d.items()}
def jam_inputs(n, D_S):
    """'dyn' distance mode (M_JAM ~ D), which is what reproduces CFG55 exactly (CFG76)."""
    a = AT[f"NGC{n:04d}"]
    ml = 10 ** a["logML_JAM"]
    MJ = ml * 10 ** a["logL"] * (D_S / a["Dist_Mpc"])
    r12 = 10 ** a["logr12"] / ARCSEC * D_S * 1e3
    return MJ, r12, a["qual"]
def calibrate(MJ, r12, Re, foot, kern, rule):
    a0 = A0[foot]; f = 0.5
    def F(lM):
        M = 10 ** lM; gN = G * f * M * Msun / (r12 * kpc) ** 2
        tot = f * M * float(kern(np.array([gN / a0]))[0])
        if rule:
            fex, Mh = rule_parts(M, foot, kern)
            tot += fex * (1 - FB) * float(nfw_enclosed(Mh, r12))
        return tot - MJ / 2.0
    grid = np.linspace(6.5, 13.8, 220) if rule else np.linspace(1.0, 13.8, 130)
    vals = np.array([F(x) for x in grid])
    roots = [brentq(F, grid[i], grid[i + 1], xtol=1e-12) for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
    if not roots: return None
    return 10 ** max(roots)
def gfun_maker(Ms, a_h, a0, fex=0.0, Mh=None, kern=None):
    kern = kern or KERN
    def g(r):
        r = np.asarray(r, float)
        Mb = Ms * Msun * r ** 2 / (r + a_h) ** 2; gN = G * Mb / (r * kpc) ** 2
        gg = gN * kern(gN / a0)
        if fex > 0: gg = gg + G * fex * (1 - FB) * nfw_enclosed(Mh, r) * Msun / (r * kpc) ** 2
        return gg
    return g

# ================================================================== THE NEW ANISOTROPIC JEANS SOLVER (written for CFG105)
# Jeans:  d(nu s_r^2)/dr + 2 beta(r) nu s_r^2 / r = -nu g,   g = +GM(<r)/r^2 (inward acceleration magnitude).
# With F(r) = exp(2 int beta dln r):  d(F nu s_r^2)/dr = -F nu g  =>  s_r^2(r) = (1/(F nu)(r)) int_r^inf F nu g ds        [nu s_r^2 -> 0 at inf]
# Substituting s = r e^x:  s_r^2(r) = int_0^inf exp[(lnF+ln nu)(r e^x) - (lnF+ln nu)(r)] g(r e^x) r e^x dx.       (units: kpc*m/s^2 -> x kpc)
# Line of sight (beta(r) = 1 - s_t^2/s_r^2, Binney & Mamon 1982): Sigma(R) s_los^2(R) = 2 int_R^inf (1 - beta R^2/r^2) nu s_r^2 r dr / sqrt(r^2-R^2);
# with z = sqrt(r^2-R^2) (r dr / sqrt(r^2-R^2) = dz) and z = R sinh u, r = R cosh u (dz = R cosh u du):
#   s_los^2(R) = int_0^inf (1 - beta(r) R^2/r^2) nu(r) s_r^2(r) cosh u du / int_0^inf nu(r) cosh u du.
def gl_panels(a, b, npan, order):
    x, w = np.polynomial.legendre.leggauss(order); edges = np.linspace(a, b, npan + 1)
    nodes = np.concatenate([0.5 * (hi - lo) * x + 0.5 * (hi + lo) for lo, hi in zip(edges[:-1], edges[1:])])
    wts = np.concatenate([0.5 * (hi - lo) * w for lo, hi in zip(edges[:-1], edges[1:])])
    return nodes, wts
QUAD = dict(xmax=40.0, xpan=16, umax=25.0, upan=10, order=24)
def set_quad(scale=1):
    global XN, XW, UN, UW
    XN, XW = gl_panels(0.0, QUAD["xmax"], QUAD["xpan"] * scale, QUAD["order"])
    UN, UW = gl_panels(0.0, QUAD["umax"], QUAD["upan"] * scale, QUAD["order"])
set_quad(1)

class Aniso:
    """anisotropy profile: beta(r) and ln F(r) = 2 int beta dln r (up to a constant)."""
    def __init__(self, kind, par):
        self.kind, self.par = kind, par
    def beta(self, r):
        if self.kind == "const": return self.par + 0.0 * r
        return r ** 2 / (r ** 2 + self.par ** 2)            # Osipkov-Merritt
    def lnF(self, r):
        if self.kind == "const": return 2 * self.par * np.log(r)
        return np.log(r ** 2 + self.par ** 2)               # F = r^2 + r_a^2
def const_beta(b): return Aniso("const", b)
def om_beta(ra): return Aniso("om", ra)
def ln_nu_power(gamma): return lambda r: -gamma * np.log(r)

def sigma_r2(r, g, lnnu, an):
    """radial dispersion^2 (m/s)^2 at radii r (kpc, any shape) by on-demand Gauss-Legendre in x = ln(s/r)."""
    r = np.asarray(r, float); s = r[..., None] * np.exp(XN)
    ex = an.lnF(s) + lnnu(s) - (an.lnF(r) + lnnu(r))[..., None]
    integ = np.exp(ex) * g(s) * s
    return kpc * (integ * XW).sum(-1)
def sigma_los2(R, g, lnnu, an):
    """line-of-sight dispersion^2 (m/s)^2 at projected radii R (kpc, 1-D)."""
    R = np.atleast_1d(np.asarray(R, float)); ch = np.cosh(UN)
    r = R[:, None] * ch[None, :]
    s2 = sigma_r2(r, g, lnnu, an)
    w = np.exp(lnnu(r) - lnnu(R)[:, None]) * ch[None, :] * UW[None, :]
    proj = 1.0 - PROJ * an.beta(r) * (R[:, None] / r) ** 2
    return (proj * w * s2).sum(1) / w.sum(1)
def sigma_los_kms(R, g, lnnu, an): return np.sqrt(sigma_los2(R, g, lnnu, an)) / 1e3

# ---- CFG76's own solver, copied unmodified (used only in C1)
RG76 = np.geomspace(0.02, 3e4, 1200); LRG76 = np.log(RG76)
def sigma_r2_76(gfun, gamma, beta=0.0):
    g = gfun(RG76); w = RG76 ** (2 * beta - gamma)
    integ = w * g * (RG76 * kpc)
    tail = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(LRG76))[::-1])[::-1], [0.0]])
    return tail / RG76 ** (2 * beta - gamma)
def sigma_los_76(R, s2, gamma, beta=0.0, umax=6.0):
    u = np.linspace(0.0, umax, 500); ch = np.cosh(u)
    r = np.outer(np.atleast_1d(R), ch)
    s = np.exp(np.interp(np.log(r), LRG76, np.log(np.maximum(s2, 1e-6))))
    rho = r ** (-gamma)
    num = np.trapz((1 - beta / ch ** 2) * rho * s * r, u, axis=1)
    den = np.trapz(rho * r, u, axis=1)
    return np.sqrt(num / den) / 1e3

# ================================================================== controls that need no galaxy
P("\n== C2 isothermal sphere, constant beta: closed forms ==")
# s_r^2: integrand exp[(2 beta - gamma) x] (v^2/s) s dx -> v^2/(gamma - 2 beta).  Projection: int_R^inf r^{-a} r dr/sqrt(r^2-R^2) = R^{1-a} B(1/2,(a-1)/2)/2,
# so int (1 - beta R^2/r^2) r^{-gamma} .. / int r^{-gamma} .. = 1 - beta B(1/2,(gamma+1)/2)/B(1/2,(gamma-1)/2) = 1 - beta (gamma-1)/gamma.
VC = 200e3
g_iso = lambda r: VC ** 2 / (np.asarray(r, float) * kpc)
worst_r = worst_l = 0.0
for gam in (2.5, 3.0, 3.43):
    for bt in (-0.5, 0.0, 0.5, 0.9):
        an = const_beta(bt); ln = ln_nu_power(gam)
        exp_r = VC ** 2 / (gam - 2 * bt)
        e_r = float(np.max(np.abs(sigma_r2(np.array([0.5, 5.0, 300.0]), g_iso, ln, an) / exp_r - 1)))
        exp_l = VC ** 2 * (1 - bt * (gam - 1) / gam) / (gam - 2 * bt)
        e_l = float(np.max(np.abs(sigma_los2(np.array([1.0, 5.0, 50.0]), g_iso, ln, an) / exp_l - 1)))
        # cross-check with the CFG113-frozen closed form written as (gamma - beta(gamma-1))/(gamma(gamma-2beta))
        alt = VC ** 2 * (gam - bt * (gam - 1)) / (gam * (gam - 2 * bt)); assert abs(alt / exp_l - 1) < 1e-13
        worst_r = max(worst_r, e_r); worst_l = max(worst_l, e_l)
check("C2 isothermal: s_r^2 = v_c^2/(gamma-2beta) and s_los^2/v_c^2 = (gamma-beta(gamma-1))/(gamma(gamma-2beta)), 12 (gamma,beta) x 3 radii",
      worst_r < 1e-4 and worst_l < 1e-4, f"max rel err s_r^2 {worst_r:.1e}, s_los^2 {worst_l:.1e}")

P("\n== C3 power-law halo g = A r^-p (r in kpc) ==")
def los_closed(R, C, q, gam, bt):
    lg = lambda a: gammaln((a - 1) / 2) - gammaln(a / 2)           # ln[Gamma((a-1)/2)/Gamma(a/2)]  (I(a) R^(a-1) = (sqrt(pi)/2) exp(lg(a)))
    return C * R ** (-q) * (np.exp(lg(gam + q)) - bt * np.exp(lg(gam + q + 2))) / np.exp(lg(gam))
A_ = 1e-10; worst_r = worst_l = 0.0
for p in (0.0, 1.0, 2.0):
    for gam, bt in ((3.0, 0.0), (2.5, 0.5), (3.43, -0.5), (2.7, 0.3)):
        g_pl = lambda r, p=p: A_ * np.asarray(r, float) ** (-p)
        C = A_ * kpc / (gam - 2 * bt + p - 1); q = p - 1
        rr = np.array([0.7, 4.0, 40.0]); an = const_beta(bt); ln = ln_nu_power(gam)
        e_r = float(np.max(np.abs(sigma_r2(rr, g_pl, ln, an) / (C * rr ** (-q)) - 1)))
        e_l = float(np.max(np.abs(sigma_los2(rr, g_pl, ln, an) / los_closed(rr, C, q, gam, bt) - 1)))
        worst_r = max(worst_r, e_r); worst_l = max(worst_l, e_l)
check("C3 power-law halo p=0,1,2, 4 (gamma,beta): s_r^2 and Gamma-function s_los^2 closed forms", worst_r < 1e-4 and worst_l < 1e-4,
      f"max rel err s_r^2 {worst_r:.1e}, s_los^2 {worst_l:.1e}")
M0 = 1e11; g_kep = lambda r: G * M0 * Msun / (np.asarray(r, float) * kpc) ** 2
rr = np.array([1.0, 3.0, 10.0, 30.0, 100.0])
e_k = float(np.max(np.abs(sigma_r2(rr, g_kep, ln_nu_power(3.0), const_beta(0.0)) / (G * M0 * Msun / (4 * rr * kpc)) - 1)))
check("C3b Kepler point mass, gamma=3, beta=0: s_r^2 = GM/(4r)", e_k < 1e-4, f"{e_k:.1e}")

# ================================================================== sample, calibration, gamma_i
GCf, nall_f = load_gcs()
BINS = make_bins(GCf)
SEL = sorted(n for n in BINS if f"NGC{n:04d}" in AT and AT[f"NGC{n:04d}"]["qual"] >= 1)
NOAT = sorted(n for n in BINS if f"NGC{n:04d}" not in AT)
P("\n== sample ==")
P(f"  galaxies {len(GAL)}, GC RVs {nall_f}, dispersion sample {len(BINS)}, JAM sample {len(SEL)}: " + ", ".join(f"NGC{n}" for n in SEL))
check("C6 sample = 16, the rest exactly NGC 1400/1407/3115 outside ATLAS3D (and 27/3440/19 catalogue counts)",
      len(SEL) == 16 and NOAT == [1400, 1407, 3115] and len(GAL) == 27 and nall_f == 3440 and len(BINS) == 19, f"{len(SEL)}, {NOAT}, {len(GAL)}/{nall_f}/{len(BINS)}")
def alabi(lMs): return float(np.clip(-0.63 * lMs + 9.81, 2.0, 4.0))
ALABI_T1 = {720: 2.71, 821: 2.88, 1023: 2.89, 2768: 2.75, 3377: 3.20, 3607: 2.63, 4278: 2.91, 4365: 2.56, 4374: 2.56,
            4459: 2.89, 4473: 2.91, 4486: 2.49, 4494: 2.87, 4526: 2.72, 4649: 2.50, 4697: 2.79, 5846: 2.59, 7457: 3.43}
dmax = max(abs(alabi(GAL[n]["lMs"]) - v) for n, v in ALABI_T1.items())
check("C5 Alabi+2017 relation reproduces the 18 Table-1 gammas quoted in CFG111's frozen file to 0.01", dmax <= 0.0100001, f"max |diff| {dmax:.4f}")
GAM = {n: alabi(BINS[n]["lMs"]) for n in SEL}
P("  gamma_i: " + ", ".join(f"{n}:{GAM[n]:.2f}" for n in SEL))

PREP = {}
t0 = time.time()
for f in FOOTS:
    PREP[f] = {}
    for n in SEL:
        b = BINS[n]; a_h = b["Re"] / 1.8153
        MJ, r12, q = jam_inputs(n, b["D"])
        Ml = calibrate(MJ, r12, b["Re"], f, KERN, False); Mr = calibrate(MJ, r12, b["Re"], f, KERN, True)
        d = dict(Ml=Ml, Mr=Mr, a_h=a_h, Re=b["Re"])
        d["g_law"] = gfun_maker(Ml, a_h, A0[f])
        if Mr is not None:
            fex, Mh = rule_parts(Mr, f, KERN); d["fex"], d["Mh"] = fex, Mh
            d["g_rule"] = gfun_maker(Mr, a_h, A0[f], fex, Mh)
        Ms = 10 ** b["lMs"]; fs, Mhs = rule_parts(Ms, f, KERN)           # SLUGGS population masses (for row A7)
        d["g_law_S"] = gfun_maker(Ms, a_h, A0[f]); d["g_rule_S"] = gfun_maker(Ms, a_h, A0[f], fs, Mhs)
        PREP[f][n] = d
P(f"  calibrations done in {time.time()-t0:.1f}s")

# ------------------------------------------------------------------ offsets
def sig_pred(b, g, lnnu, an, aperture=False):
    """predicted s_los at the bin radii: point evaluation at the bin's median projected radius, or (aperture) the member-averaged s_los^2."""
    if not aperture: return sigma_los_kms(b["Rb"], g, lnnu, an)
    out = np.zeros(len(b["Rb"]))
    for i, Rm in enumerate(b["Rmem"]):
        lo, hi = Rm.min(), Rm.max()
        gr = np.geomspace(lo, hi, 9)
        s2 = sigma_los2(gr, g, lnnu, an)
        out[i] = math.sqrt(float(np.mean(np.interp(np.log(Rm), np.log(gr), s2)))) / 1e3
    return out
def gal_offset(n, foot, model, lnnu, an, aperture=False, Sb=None, pop=False):
    b = BINS[n]; d = PREP[foot][n]
    g = d.get(("g_law" if model == "law" else "g_rule") + ("_S" if pop else ""))
    if g is None: return None
    pred = sig_pred(b, g, lnnu, an, aperture)
    S = b["Sb"] if Sb is None else Sb[n]
    return float(np.mean(np.log10(S[b["out"]] / pred[b["out"]])))
def stats(v):
    v = np.array(v); m = v.mean(); e = v.std(ddof=1) / math.sqrt(len(v)); return m, e, len(v)
def run(foot, gam=None, an=None, mk_an=None, delta=0.0, tr_shift=0.0, aperture=False, Sb=None, pop=False, rows=None, dbreak=None):
    """per-galaxy offsets {model: {n: off}}.  gam: dict n->3D slope (default GAM); an: Aniso, or mk_an(n) -> Aniso per galaxy."""
    gam = gam or GAM; rows = rows or SEL; res = {"law": {}, "rule": {}}
    for n in rows:
        gg = gam[n] + tr_shift
        if dbreak is None: lnnu = ln_nu_power(gg)
        else:
            rb = 5.0 * BINS[n]["Re"]; lnnu = (lambda r, gg=gg, rb=rb: -gg * np.log(r) - 0.5 * dbreak * np.log1p((r / rb) ** 2))
        a_ = mk_an(n) if mk_an else an
        for m in ("law", "rule"):
            o = gal_offset(n, foot, m, lnnu, a_, aperture, Sb, pop)
            if o is not None: res[m][n] = o
    return res
def summ(res, sub=None):
    o = {}
    for k in ("law", "rule"):
        d = [v for n, v in res[k].items() if sub is None or n in sub]; o[k] = stats(d)
    return o
def sg(s): return s[0] / s[1]
def fmt(s): return " | ".join(f"{k} {v[0]:+.4f} +- {v[1]:.4f} ({v[0]/v[1]:+.2f}s)" for k, v in s.items())

# ------------------------------------------------------------------ C4 Jeans residual (real potentials)
P("\n== C4 Jeans-equation residual in the real potentials ==")
def jeans_resid(g, lnnu, an, r0):
    h = 1e-3
    def nus2(lr):
        r = np.exp(lr); return float(np.exp(lnnu(np.array([r])))[0] * sigma_r2(np.array([r]), g, lnnu, an)[0])
    lr0 = math.log(r0); r = np.array([r0])
    d = (nus2(lr0 + h) - nus2(lr0 - h)) / (2 * h)
    nu_r = float(np.exp(lnnu(r))[0]); s2 = float(sigma_r2(r, g, lnnu, an)[0])
    return abs(d + 2 * float(an.beta(r)[0]) * nu_r * s2 + nu_r * float(g(r)[0]) * r0 * kpc) / abs(nu_r * float(g(r)[0]) * r0 * kpc)
worst = 0.0; worst_lbl = ""
for n in (SEL[0], SEL[-1]):
    for mdl in ("law", "rule"):
        g = PREP["canonical"][n]["g_law" if mdl == "law" else "g_rule"]
        for an, lbl in ([(const_beta(b), f"beta={b:+.2f}") for b in (-0.5, 0.0, 0.5, 0.9)] + [(om_beta(3 * BINS[n]["Re"]), "OM 3Re")]):
            for r0 in (1.0, 5.0, 30.0):
                e = jeans_resid(g, ln_nu_power(GAM[n]), an, r0)
                if e > worst: worst, worst_lbl = e, f"NGC{n} {mdl} {lbl} r={r0}"
check("C4 Jeans residual |d(nu s_r^2)/dln r + 2 beta nu s_r^2 + nu g r|/|nu g r| < 1e-4 (2 galaxies x law/rule x 5 profiles x 3 radii)", worst < 1e-4, f"max {worst:.1e} at {worst_lbl}")

# ------------------------------------------------------------------ C0 baseline at gamma=3, beta=0 vs CFG76's published headline
P("\n== C0 own baseline (own solver) at gamma = 3, beta = 0 vs CFG76's headline ==")
G3 = {n: 3.0 for n in SEL}
s0 = {f: summ(run(f, gam=G3, an=const_beta(0.0))) for f in FOOTS}
for f in FOOTS: P(f"  {f:9s}: {fmt(s0[f])}")
c0_ok = (abs(s0["canonical"]["law"][0] - 0.096984) < 3e-4 and abs(s0["canonical"]["rule"][0] - 0.045640) < 3e-4
         and abs(s0["canonical"]["law"][1] - 0.02431) < 3e-4 and abs(s0["canonical"]["rule"][1] - 0.01771) < 3e-4
         and abs(s0["alt"]["law"][0] - 0.088) < 1.5e-3 and abs(s0["alt"]["rule"][0] - 0.047) < 1.5e-3)
check("C0 baseline reproduces CFG76 (law +0.09698+-0.02431, rule +0.04564+-0.01771 canonical; alt ~+0.088/+0.047)", c0_ok,
      f"canonical law {s0['canonical']['law'][0]:+.5f}+-{s0['canonical']['law'][1]:.5f}, rule {s0['canonical']['rule'][0]:+.5f}+-{s0['canonical']['rule'][1]:.5f}")

# ------------------------------------------------------------------ C1 isotropic limit vs copied CFG76 solver at published gamma_i
P("\n== C1 own solver vs CFG76's solver (copied) at the published gamma_i ==")
def off76(n, foot, model, gam, beta):
    b = BINS[n]; g = PREP[foot][n]["g_law" if model == "law" else "g_rule"]
    pred = sigma_los_76(b["Rb"], sigma_r2_76(g, gam, beta), gam, beta)
    return float(np.mean(np.log10(b["Sb"][b["out"]] / pred[b["out"]])))
c1 = {}
for bt in (0.0, -0.5, 0.5):
    md = 0.0; mm = 0.0
    for f in FOOTS:
        for m in ("law", "rule"):
            mine = run(f, an=const_beta(bt))[m]
            d = [abs(mine[n] - off76(n, f, m, GAM[n], bt)) for n in SEL if n in mine]
            md = max(md, max(d));
    c1[bt] = md; P(f"  beta {bt:+.1f}: max per-galaxy |own - CFG76 solver| over both footings, law and rule = {md:.2e} dex")
check("C1 isotropic limit: own solver == CFG76 estimator at the published slopes (max per-galaxy diff < 1e-3 dex)", c1[0.0] < 1e-3, f"{c1[0.0]:.1e}")
check("C1b same at beta = +-0.5 (< 2e-3 dex; numerics only, same projection kernel)", max(c1[-0.5], c1[0.5]) < 2e-3, f"{max(c1[-0.5], c1[0.5]):.1e}")

# ------------------------------------------------------------------ C7 convergence
BET = (-0.5, -0.25, 0.0, 0.25, 0.5)
ref = summ(run("canonical", an=const_beta(0.5)))["law"]
set_quad(2); ref2 = summ(run("canonical", an=const_beta(0.5)))["law"]; set_quad(1)
check("C7 headline (law, beta=+0.5, canonical) unchanged to 1e-5 dex when the quadrature order/panels are doubled", abs(ref[0] - ref2[0]) < 1e-5, f"{ref[0]:+.7f} vs {ref2[0]:+.7f}")

if STAGE == "controls":
    P("\nSTAGE=controls: stopping before the main table.")
    P(f"FAILED CHECKS ({len(FAILS)}): " + "; ".join(FAILS)); sys.exit(1 if FAILS else 0)

# ================================================================== MUTATE=1: remove the deficit, keep the scatter
SB_MUT = {f: None for f in FOOTS}
if MUTATE == 1:
    for f in FOOTS:
        D = summ(run(f, an=const_beta(0.5)))["law"][0]
        SB_MUT[f] = {n: BINS[n]["Sb"] * 10 ** (-D) for n in SEL}
        P(f"  MUTATE=1 {f}: D = law mean offset at (gamma_i, beta=+0.5) = {D:+.5f} dex removed from every observed dispersion")

# ================================================================== MAIN
P("\n== MAIN: constant beta at the published gamma_i (JAM-calibrated masses, N=16) ==" + ("  [MUTATE=%d]" % MUTATE if MUTATE else ""))
BETAS = (-0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 0.9)
MAIN = {f: {} for f in FOOTS}
for f in FOOTS:
    for bt in BETAS:
        r = run(f, an=const_beta(bt), Sb=SB_MUT[f]); MAIN[f][bt] = (r, summ(r))
P("  beta    | law canonical             | law alt        | rule canonical            | rule alt")
for bt in BETAS:
    c, a = MAIN["canonical"][bt][1], MAIN["alt"][bt][1]
    P(f"  {bt:+.2f}   | {c['law'][0]:+.4f} +- {c['law'][1]:.4f} ({sg(c['law']):.2f}s) | {sg(a['law']):.2f}s | {c['rule'][0]:+.4f} +- {c['rule'][1]:.4f} ({sg(c['rule']):+.2f}s) | {sg(a['rule']):+.2f}s"
      + ("   [beyond the bracket]" if bt > 0.5 else ""))
CF113 = {"law": {"canonical": {-0.5: 3.66, -0.25: 3.64, 0.0: 3.60, 0.25: 3.53, 0.5: 3.38, 0.75: 2.99, 0.9: 2.46},
                 "alt": {-0.5: 3.31, -0.25: 3.28, 0.0: 3.22, 0.25: 3.12, 0.5: 2.93, 0.75: 2.48, 0.9: 1.91}},
         "rule": {"canonical": {-0.5: 2.06, -0.25: 1.84, 0.0: 1.55, 0.25: 1.13, 0.5: 0.56, 0.75: -0.21, 0.9: -0.75},
                  "alt": {-0.5: 2.10, -0.25: 1.91, 0.0: 1.64, 0.25: 1.26, 0.5: 0.69, 0.75: -0.10, 0.9: -0.68}}}
P("  sigma differences (own - CFG113 README table), law / rule, canonical then alt:")
for m in ("law", "rule"):
    for f in FOOTS:
        P(f"    {m:4s} {f:9s}: " + "  ".join(f"{bt:+.2f}:{sg(MAIN[f][bt][1][m]) - CF113[m][f][bt]:+.3f}" for bt in BETAS))
lawmin = {f: min(sg(MAIN[f][bt][1]["law"]) for bt in BET) for f in FOOTS}
P(f"  law minimum over the bracket: canonical {lawmin['canonical']:.3f}s at beta=+0.5, alt {lawmin['alt']:.3f}s")
def near(x, y, tol=0.01): return abs(x - y) <= tol
check("R1 law minimum over the bracket = 3.38 s (canonical) and 2.93 s (alt)", near(lawmin["canonical"], 3.38) and near(lawmin["alt"], 2.93),
      f"{lawmin['canonical']:.3f}, {lawmin['alt']:.3f}")
r_p, r_m = sg(MAIN["canonical"][0.5][1]["rule"]), sg(MAIN["canonical"][-0.5][1]["rule"])
ra_p, ra_m = sg(MAIN["alt"][0.5][1]["rule"]), sg(MAIN["alt"][-0.5][1]["rule"])
check("R2 rule at beta=+0.5 / -0.5 = 0.56 / 2.06 s canonical (alt 0.69 / 2.10)", near(r_p, 0.56) and near(r_m, 2.06) and near(ra_p, 0.69) and near(ra_m, 2.10),
      f"{r_p:.3f} / {r_m:.3f}; alt {ra_p:.3f} / {ra_m:.3f}")
check("H1 law's offset exceeds 2 sigma at every beta in the bracket on both footings", all(sg(MAIN[f][bt][1]["law"]) > 2 for f in FOOTS for bt in BET),
      f"min canonical {lawmin['canonical']:.2f}, alt {lawmin['alt']:.2f}")
if MUTATE == 1:
    for f in FOOTS:
        m0 = MAIN[f][0.5][1]["law"][0]
        check(f"MUTATE=1 sanity: law mean at beta=+0.5 is 0 on {f}", abs(m0) < 1e-9, f"{m0:+.2e}")
json.dump({f: {str(bt): {k: list(v) for k, v in MAIN[f][bt][1].items()} for bt in BETAS} for f in FOOTS},
          open(os.path.join(HERE, "cfg105_main%s_results.json" % ("_MUTATE%d" % MUTATE if MUTATE else "")), "w"), indent=1)
if MUTATE:
    P("\n(MUTATE run: attack rows skipped.)")
    open(os.path.join(HERE, "cfg105_MUTATE%d.out" % MUTATE), "w").write("\n".join(out_lines) + "\n")
    P(f"\nFAILED CHECKS ({len(FAILS)}): " + "; ".join(FAILS)); sys.exit(1 if FAILS else 0)

# ================================================================== ATTACK / REPORTED ROWS (main run only)
P("\n== A1/R3: the single constant beta nulling the law's mean ==")
def mean_at(f, bt, model="law"):
    return summ(run(f, an=const_beta(bt)))[model][0]
for f in FOOTS:
    for m in ("law", "rule"):
        lo, hi = mean_at(f, -1.0, m), mean_at(f, 0.99, m)
        if lo * hi < 0:
            bz = brentq(lambda b: mean_at(f, b, m), -1.0, 0.99, xtol=1e-4); P(f"  {f:9s} {m:4s}: mean nulled at beta = {bz:+.3f}")
        else:
            P(f"  {f:9s} {m:4s}: no sign change on [-1, 0.99]: mean {lo:+.4f} (beta=-1) ... {hi:+.4f} (beta=0.99)")

P("\n== A2: Osipkov-Merritt beta(r) = r^2/(r^2+ra^2), ra = k * R_e ==")
for k in (1, 2, 3, 5, 10):
    row = []
    for f in FOOTS:
        s = summ(run(f, mk_an=lambda n, k=k: om_beta(k * BINS[n]["Re"])))
        row.append(f"{f[:3]}: law {s['law'][0]:+.4f} ({sg(s['law']):.2f}s) rule {s['rule'][0]:+.4f} ({sg(s['rule']):+.2f}s)")
    P(f"  ra = {k:2d} Re : " + " | ".join(row))
P("  (a mixture: OM ra=3Re with beta=const 0.5 for comparison is in the main table at beta=+0.5)")

P("\n== A3: slope-radius dependence  nu = r^-gamma_i [1+(r/5Re)^2]^(-Delta/2) ==")
for dl in (-0.5, 0.5, 1.0):
    for bt in (0.0, 0.5):
        row = []
        for f in FOOTS:
            s = summ(run(f, an=const_beta(bt), dbreak=dl))
            row.append(f"{f[:3]}: law {s['law'][0]:+.4f} ({sg(s['law']):.2f}s) rule {s['rule'][0]:+.4f} ({sg(s['rule']):+.2f}s)")
        P(f"  Delta {dl:+.1f} beta {bt:+.1f}: " + " | ".join(row))

P("\n== A4: tracer slope reading  gamma_3D = gamma_i + 1 (if the published slope were the projected one), and gamma_i -1 ==")
for sh in (+1.0, -1.0):
    for bt in (-0.5, 0.0, 0.5):
        row = []
        for f in FOOTS:
            s = summ(run(f, an=const_beta(bt), tr_shift=sh))
            row.append(f"{f[:3]}: law {s['law'][0]:+.4f} ({sg(s['law']):.2f}s) rule {s['rule'][0]:+.4f} ({sg(s['rule']):+.2f}s)")
        P(f"  shift {sh:+.0f} beta {bt:+.1f}: " + " | ".join(row))

P("\n== A5: aperture convention: bin-median point evaluation vs member-averaged s_los^2 ==")
for bt in (-0.5, 0.0, 0.5):
    row = []
    for f in FOOTS:
        s = summ(run(f, an=const_beta(bt), aperture=True)); pt = MAIN[f][bt][1]
        row.append(f"{f[:3]}: law {s['law'][0]:+.4f} ({sg(s['law']):.2f}s; point {sg(pt['law']):.2f}s) rule {s['rule'][0]:+.4f} ({sg(s['rule']):+.2f}s; point {sg(pt['rule']):+.2f}s)")
    P(f"  beta {bt:+.1f}: " + " | ".join(row))

P("\n== A6: per galaxy (canonical): gamma_i, logM*, Re, offsets at beta = -0.5, 0, +0.5 and the change -0.5 -> +0.5 ==")
rn, r0, rp = MAIN["canonical"][-0.5][0], MAIN["canonical"][0.0][0], MAIN["canonical"][0.5][0]
P("  NGC   gamma  logM*   Re_kpc |  law(-.5) law(0) law(+.5) d_law | rule(-.5) rule(0) rule(+.5) d_rule")
for n in sorted(SEL, key=lambda n: rp["rule"][n] - rn["rule"][n]):
    P(f"  {n:<5d} {GAM[n]:.2f}  {BINS[n]['lMs']:.2f}  {BINS[n]['Re']:6.2f} | {rn['law'][n]:+.3f} {r0['law'][n]:+.3f} {rp['law'][n]:+.3f} {rp['law'][n]-rn['law'][n]:+.4f} | "
      f"{rn['rule'][n]:+.3f} {r0['rule'][n]:+.3f} {rp['rule'][n]:+.3f} {rp['rule'][n]-rn['rule'][n]:+.4f}")
dr = np.array([rp["rule"][n] - rn["rule"][n] for n in SEL]); dl_ = np.array([rp["law"][n] - rn["law"][n] for n in SEL])
gm = np.array([GAM[n] for n in SEL])
P(f"  mean d_rule {dr.mean():+.4f}, mean d_law {dl_.mean():+.4f}; corr(d, gamma): rule {np.corrcoef(dr, gm)[0,1]:+.2f}, law {np.corrcoef(dl_, gm)[0,1]:+.2f}")
P(f"  galaxies with gamma_i > 3 (beta-sensitivity of opposite sign): {[n for n in SEL if GAM[n] > 3]}")
P("  leave-one-out on the rule's sigma at beta = -0.5 / +0.5 (canonical):")
for n in SEL:
    sub = [m for m in SEL if m != n]
    P(f"    without NGC{n:<5d}: {sg(summ(rn, sub)['rule']):+.2f} / {sg(summ(rp, sub)['rule']):+.2f}   (law {sg(summ(rn, sub)['law']):.2f} / {sg(summ(rp, sub)['law']):.2f})")
top = [n for n in SEL if BINS[n]["lMs"] > 11.3]
P(f"  the four group/cluster centrals removed (M87, 4365, 4374, 5846), beta +0.5 canonical N=12: " +
  fmt(summ(rp, [n for n in SEL if n not in (4486, 4365, 4374, 5846)])))

P("\n== A7: gamma = 3 for every galaxy (CFG55 baseline); SLUGGS population masses; four centrals removed ==")
for bt in (-0.5, 0.5):
    row = []
    for f in FOOTS:
        s = summ(run(f, gam=G3, an=const_beta(bt))); sp = summ(run(f, an=const_beta(bt), pop=True))
        row.append(f"{f[:3]}: gamma=3 law {sg(s['law']):.2f}s rule {sg(s['rule']):+.2f}s | pop.masses law {sg(sp['law']):.2f}s rule {sg(sp['rule']):+.2f}s")
    P(f"  beta {bt:+.1f}: " + " | ".join(row))

open(os.path.join(HERE, "cfg105_main.out"), "w").write("\n".join(out_lines) + "\n")
P(f"\nFAILED CHECKS ({len(FAILS)}): " + "; ".join(FAILS))
sys.exit(1 if FAILS else 0)
