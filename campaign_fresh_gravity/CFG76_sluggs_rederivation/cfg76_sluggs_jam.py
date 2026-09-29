#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG76 independent re-derivation of CFG55's SLUGGS/JAM headline.  Spec: CFG76_SPEC_FROZEN.txt (frozen before the first run; sha256 printed).
Own implementation; reads only real_research/data/*.  No CFG38/CFG55/CFG71 code read/executed.  MUTATE=1 halves every JAM mass."""
import os, sys, math, json, hashlib
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data"
MUTATE = os.environ.get("MUTATE", "0") == "1"
JAMF = 0.5 if MUTATE else 1.0
spec = open(os.path.join(HERE, "CFG76_SPEC_FROZEN.txt"), "rb").read()
out_lines = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); out_lines.append(s)
P("CFG76  MUTATE=%s  spec sha256 %s" % (MUTATE, hashlib.sha256(spec).hexdigest()[:16]))
FAILS = []
def check(name, ok, detail=""):
    P(("  [PASS] " if ok else "  [FAIL] ") + name + ("   (" + detail + ")" if detail else ""))
    if not ok: FAILS.append(name)

# ---------------------------------------------------------------- constants (hunt_lib values, re-typed)
G = 6.674e-11; kpc = 3.0857e19; Mpc = 3.0857e22; Msun = 1.989e30
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
FB = 0.02237 / (0.02237 + 0.1200)
ARCSEC = 206264.806
FOOTS = ("canonical", "alt")

# ---------------------------------------------------------------- kernels
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0)
H_P = float(h_rar(Y_P))
LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG
DH = np.maximum(dh_rar(YG), 0.05 * H_P / (YG + Y_P))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 + np.interp(np.log10(y), LYG, HM) / y
KERNELS = {"nu_mono": nu_mono, "nu_rar": nu_rar}

# ---------------------------------------------------------------- data
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
def load_gcs(faithful_key):
    """faithful_key=True: the GC name prefix ('NGC720') is looked up among keys 'NGC%04d' (h50's key, silently dropping 3-digit NGCs)."""
    keys = {f"NGC{n:04d}": n for n in GAL} if faithful_key else {}
    GC = {n: [] for n in GAL}; nall = 0; unmatched = {}
    for r in rv_:
        nm = col(hv, r, "Star", str, "")
        pre = nm.split("_")[0]
        if faithful_key:
            n = keys.get(pre, None)
        else:
            try: n = int(pre.replace("NGC", "")) if pre.startswith("NGC") else None
            except Exception: n = None
            if n not in GAL: n = None
        if n is None:
            unmatched[pre] = unmatched.get(pre, 0) + 1; continue
        v = col(hv, r, "HRV"); ev = col(hv, r, "e_HRV"); rg = col(hv, r, "Rgal")
        ra = col(hv, r, "RAJ2000"); de = col(hv, r, "DEJ2000")
        if not (np.isfinite(v) and np.isfinite(rg) and np.isfinite(ra) and np.isfinite(de)): continue
        nall += 1; g = GAL[n]
        dra = (ra - g["ra"]) * math.cos(math.radians(de)); dde = de - g["de"]
        GC[n].append((rg, v, ev if np.isfinite(ev) else 15.0, math.degrees(math.atan2(dde, dra))))
    return GC, nall, unmatched

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
            mu, s = mle_sigma(a[m, 1], a[m, 2]); bins.append((float(np.median(Rk[m])), s))
        if len(bins) < 2: continue
        Rb = np.array([b[0] for b in bins]); Sb = np.array([b[1] for b in bins])
        out = Rb > max(1.0 * Re, 2.0)
        if out.sum() == 0: out = np.ones(len(Rb), bool)
        B[n] = dict(n=n, N=len(a), Re=Re, Rb=Rb, Sb=Sb, out=out, D=D, lMs=g["lMs"])
    return B

# ---------------------------------------------------------------- Jeans
RG = np.geomspace(0.02, 3e4, 1200); LRG = np.log(RG)
def sigma_r2(gfun, gamma, beta=0.0):
    g = gfun(RG); w = RG ** (2 * beta - gamma)
    integ = w * g * (RG * kpc)
    tail = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(LRG))[::-1])[::-1], [0.0]])
    return tail / RG ** (2 * beta - gamma)
def sigma_los(R, s2, gamma, beta=0.0, umax=6.0):
    u = np.linspace(0.0, umax, 500); ch = np.cosh(u)
    r = np.outer(np.atleast_1d(R), ch)
    s = np.exp(np.interp(np.log(r), LRG, np.log(np.maximum(s2, 1e-6))))
    rho = r ** (-gamma)
    num = np.trapz((1 - beta / ch ** 2) * rho * s * r, u, axis=1)
    den = np.trapz(rho * r, u, axis=1)
    return np.sqrt(num / den) / 1e3

# ---------------------------------------------------------------- halo machinery (CFG35/36 as documented)
H48 = 67.4
RHO_C = 3 * (H48 * 1e3 / Mpc) ** 2 / (8 * math.pi * G) / Msun * Mpc ** 3      # Msun/Mpc^3
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

# ---- LCDM turnaround at a=1 (own solution of the Lambda shell energy equation)
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
A0_MPC = {f: A0[f] / (1e6 / 3.0856775814913673e22) for f in FOOTS}      # (km/s)^2/Mpc; hunt_lib a0 values
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

# ---------------------------------------------------------------- ATLAS3D
lines = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "atlas3d_fj_table.tsv")) if l.strip() and not l.startswith("#")]
AH = lines[0]; AT = {}
for r in lines[1:]:
    d = dict(zip(AH, r))
    def _fl(v):
        try: return float(v)
        except Exception: return float("nan")
    AT[d["name"]] = {k: (_fl(v) if k != "name" else v) for k, v in d.items()}

def jam_inputs(n, D_S, dist_mode="literal", salp=False):
    a = AT[f"NGC{n:04d}"]
    L = 10 ** a["logL"] * (D_S / a["Dist_Mpc"]) ** 2
    ml = 10 ** (a["logML_Salp"] if salp else a["logML_JAM"])
    MJ = ml * L
    if dist_mode == "dyn" and not salp: MJ = ml * 10 ** a["logL"] * (D_S / a["Dist_Mpc"])
    r12 = 10 ** a["logr12"] / ARCSEC * D_S * 1e3
    return MJ * JAMF, r12, a["qual"]

# ---------------------------------------------------------------- calibration + prediction
def Menc_frac(r12, Re, mode):
    if mode == "half": return 0.5
    a_h = Re / 1.8153; return (r12 / (r12 + a_h)) ** 2
def calibrate(MJ, r12, Re, foot, kern, rule, fmode="half"):
    a0 = A0[foot]; f = Menc_frac(r12, Re, fmode)
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
    if not roots: return None, 0
    return 10 ** max(roots), len(roots)
def gfun_maker(Ms, a_h, a0, kern, fex=0.0, Mh=None):
    def g(r):
        Mb = Ms * Msun * r ** 2 / (r + a_h) ** 2; gN = G * Mb / (r * kpc) ** 2
        gg = gN * kern(gN / a0)
        if fex > 0: gg = gg + G * fex * (1 - FB) * nfw_enclosed(Mh, r) * Msun / (r * kpc) ** 2
        return gg
    return g
def offset(b, Ms, foot, kern, rule, gamma=3.0, beta=0.0):
    a_h = b["Re"] / 1.8153
    fex, Mh = rule_parts(Ms, foot, kern) if rule else (0.0, None)
    pred = sigma_los(b["Rb"], sigma_r2(gfun_maker(Ms, a_h, A0[foot], kern, fex, Mh), gamma, beta), gamma, beta)
    return float(np.mean(np.log10(b["Sb"][b["out"]] / pred[b["out"]])))

def stats(v):
    v = np.array(v); n = len(v)
    m = v.mean(); e1 = v.std(ddof=1) / math.sqrt(n); e0 = v.std(ddof=0) / math.sqrt(n)
    return m, e1, e0

# ================================================================ C1 closed-form controls
P("\n== C1 closed-form limits ==")
rr = np.array([1.0, 3.0, 10.0, 30.0, 100.0]); M0 = 1e11
def g_pt(r): return G * M0 * Msun / (r * kpc) ** 2
s2n = sigma_r2(g_pt, 3.0); s2i = np.interp(np.log(rr), LRG, s2n); ref = G * M0 * Msun / (4 * rr * kpc)
e_a = float(np.max(np.abs(s2i / ref - 1)))
check("C1a point-mass Newton gamma=3: sigma_r^2 = GM/(4r)", e_a < 1e-3, f"max rel err {e_a:.1e}")
a0c = A0["canonical"]
def g_dm(r): return np.sqrt(G * M0 * Msun * a0c) / (r * kpc)
s2d = np.interp(np.log(rr), LRG, sigma_r2(g_dm, 3.0)); refd = np.sqrt(G * M0 * Msun * a0c) / 3.0
e_b = float(np.max(np.abs(s2d / refd - 1)))
sl = sigma_los(rr, sigma_r2(g_dm, 3.0), 3.0); e_b2 = float(np.max(np.abs(sl * 1e3 / np.sqrt(refd) - 1)))
check("C1b deep-MOND point mass: sigma_r^2 = sqrt(G M a0)/3, and sigma_los = sigma_r for constant sigma_r (beta=0)", e_b < 1e-3 and e_b2 < 1e-3, f"{e_b:.1e}, {e_b2:.1e}")
Mj = 3e11; r12t = 6.0
Mnew, _ = calibrate(Mj, r12t, 5.0, "canonical", nu_mono, False)
Mnew_newt = calibrate_res = None
def calib_a0(a0f):
    saveA = dict(A0);
    for f in FOOTS: A0[f] = saveA[f] * a0f
    try: return calibrate(Mj, r12t, 5.0, "canonical", nu_mono, False)[0]
    finally: A0.update(saveA)
M_newt = calib_a0(1e-6)
M_deep = calib_a0(1e6)
e_c1 = abs(M_newt / Mj - 1)
M_expect = Mj ** 2 * G / (2 * (r12t * kpc) ** 2 * (A0["canonical"] * 1e6)) / Msun * Msun   # M* in kg-free Msun: see below
# deep MOND: M*_kg = MJ_kg^2 G/(2 r^2 a0); with M in Msun: M* = MJ^2 * Msun * G/(2 r^2 a0)
M_expect = Mj ** 2 * Msun * G / (2 * (r12t * kpc) ** 2 * A0["canonical"] * 1e6)
e_c2 = abs(M_deep / M_expect - 1)
check("C1c Newtonian limit of the calibration (a0 x1e-6): M* = M_JAM; deep limit (a0 x1e6): M* = MJ^2 G/(2 r^2 a0)", e_c1 < 1e-4 and e_c2 < 1e-3, f"{e_c1:.1e}, {e_c2:.1e} (deep-limit tolerance 1e-3: nu_mono -> y^-1/2 only up to 1/y)")
k_eds = one_plus_delta_ta(1.0)
check("C1d EdS turnaround (3pi/4)^2", abs(k_eds - (3 * math.pi / 4) ** 2) < 1e-6, f"{k_eds:.8f} vs {(3*math.pi/4)**2:.8f}; LCDM(0.3153) 1+delta_ta(a=1) = {K_TA:.4f}")
errs = [abs(m200m_of_c(M)[0] / (200 * OM48 * RHO_C * 4 * math.pi / 3 * m200m_of_c(M)[1] ** 3) - 1) for M in (1e12, 1e13, 1e14)]
rt = [abs(m200c_from_m200m(m200m_of_c(M)[0]) / M - 1) for M in (1e12, 1e13, 1e14)]
check("C1e M200m->M200c: the NFW mass in R200m equals 200 rho_m V; the inverse table round-trips", max(errs) < 1e-6 and max(rt) < 1e-4, f"{max(errs):.1e}, round trip {max(rt):.1e}")
yy = np.logspace(-6, math.log10(2.0), 400)
e_f = float(np.max(np.abs(nu_mono(yy) / nu_rar(yy) - 1)))
check("C1f nu_mono == nu_RAR for y < 2 and h_mono monotone", e_f < 1e-6 and bool(np.all(np.diff(HM) >= 0)), f"max rel diff {e_f:.1e}; Y_P {Y_P:.4f}")

# ================================================================ sample
P("\n== sample ==")
GCf, nall_f, unm_f = load_gcs(True)
P(f"  galaxies in catalogue {len(GAL)}; GC RVs parsed with h50's key: {nall_f}; dropped prefixes (top): " + ", ".join(f"{k}:{v}" for k, v in sorted(unm_f.items(), key=lambda t: -t[1])[:8]))
BINS = make_bins(GCf)
P(f"  h50-faithful sample: {len(BINS)} galaxies: " + ", ".join(f"NGC{n}" for n in sorted(BINS)))
check("C2 h50's committed sample: 27 galaxies, 3440 GC RVs, 19 in the dispersion sample", len(GAL) == 27 and nall_f == 3440 and len(BINS) == 19, f"{len(GAL)} / {nall_f} / {len(BINS)}")
SEL = sorted(n for n in BINS if f"NGC{n:04d}" in AT and AT[f"NGC{n:04d}"]["qual"] >= 1)
NOAT = sorted(n for n in BINS if f"NGC{n:04d}" not in AT)
P(f"  with ATLAS3D JAM quality >= 1: {len(SEL)}; not in ATLAS3D: {NOAT}; in ATLAS3D but qual<1: {[n for n in BINS if f'NGC{n:04d}' in AT and AT[f'NGC{n:04d}']['qual']<1]}")
check("G2 sample = 16, the rest exactly NGC 1400/1407/3115", len(SEL) == 16 and NOAT == [1400, 1407, 3115], f"{len(SEL)}; outside ATLAS3D {NOAT}")
GCc, nall_c, unm_c = load_gcs(False)
BINS_c = make_bins(GCc)
extra = sorted(set(BINS_c) - set(BINS))
P(f"  corrected key: GC RVs {nall_c}; extra galaxies entering: {['NGC%d' % n for n in extra]}")

# ================================================================ main computation
def run(rows, kernname, foot, dist_mode="literal", fmode="half", salp=False, gamma=3.0, beta=0.0, sluggs_mass=False, note=False, bins=BINS):
    kern = KERNELS[kernname]; res = {"law": {}, "rule": {}}; excl = []; nroot = {}
    for n in rows:
        b = bins[n]
        if not sluggs_mass: MJ, r12, q = jam_inputs(n, b["D"], dist_mode, salp)
        if sluggs_mass:
            Ms_l = Ms_r = 10 ** b["lMs"]
        else:
            Ms_l, _ = calibrate(MJ, r12, b["Re"], foot, kern, False, fmode)
            Ms_r, nr = calibrate(MJ, r12, b["Re"], foot, kern, True, fmode)
            nroot[n] = nr
        res["law"][n] = offset(b, Ms_l, foot, kern, False, gamma, beta)
        if Ms_r is None: excl.append(n)
        else: res["rule"][n] = offset(b, Ms_r, foot, kern, True, gamma, beta)
        res.setdefault("Ms", {})[n] = (Ms_l, Ms_r)
    res["excl"] = excl; res["nroot"] = nroot
    return res
def summ(res, sub=None):
    o = {}
    for k in ("law", "rule"):
        d = {n: v for n, v in res[k].items() if sub is None or n in sub}
        m, e1, e0 = stats(list(d.values())); o[k] = (m, e1, e0, len(d))
    return o
def fmt(o):
    return " | ".join(f"{k} {v[0]:+.3f} +- {v[1]:.3f} ({v[0]/v[1]:+.2f}s; ddof0 {v[2]:.3f}, {v[0]/v[2]:+.2f}s) N={v[3]}" for k, v in o.items())

ALL = {}
P("\n== MAIN: JAM-calibrated masses, N=16 ==" + ("  [MUTATE: JAM x0.5]" if MUTATE else ""))
for kn in KERNELS:
    for f in FOOTS:
        r = run(SEL, kn, f); ALL[(kn, f)] = r
        P(f"  {kn:8s} {f:9s}: {fmt(summ(r))}; rule-excluded {r['excl']}; multi-root galaxies {[n for n,c in r['nroot'].items() if c>1]}")

P("\n== SLUGGS masses, same 16 (and 19 for the law) ==")
SL = {}
for kn in KERNELS:
    for f in FOOTS:
        r16 = run(SEL, kn, f, sluggs_mass=True); r19 = run(sorted(BINS), kn, f, sluggs_mass=True)
        SL[(kn, f)] = (summ(r16), summ(r19))
        P(f"  {kn:8s} {f:9s}: 16: {fmt(summ(r16))}\n{'':22s}19: {fmt(summ(r19))}")

# ---------------------------------------------------------------- gates
REF = {"canonical": dict(law=(0.097, 0.024), rule=(0.046, 0.018)), "alt": dict(law=(0.088, 0.024), rule=(0.047, 0.018))}
REFS = {"canonical": dict(law=0.077, rule=0.007), "alt": dict(law=0.063, rule=0.002)}
def g1(kn, conv="e1"):
    ok = True; det = []
    for f in FOOTS:
        s = summ(ALL[(kn, f)])
        for k in ("law", "rule"):
            m, e1, e0, n = s[k]; e = e1 if conv == "e1" else e0
            rm, re_ = REF[f][k]
            d_m, d_e = m - rm, e - re_
            ok &= abs(d_m) < 0.0015 and abs(d_e) < 0.0015 and abs(m / e - rm / re_) < 0.1 + 0.05
            det.append(f"{f[:3]} {k}: {m:+.3f}({d_m:+.3f}) err {e:.3f}({d_e:+.3f}) {m/e:.2f}s")
    return ok, "; ".join(det)
P("\n== gates ==")
for kn in KERNELS:
    for conv in ("e1", "e0"):
        ok, det = g1(kn, conv)
        check(f"G1 reproduction of CFG55 headline, kernel {kn}, error ddof={'1' if conv=='e1' else '0'}", ok, det)
def g3(kn):
    ok = True; det = []
    for f in FOOTS:
        s16, s19 = SL[(kn, f)]
        ok &= abs(s16["law"][0] - REFS[f]["law"]) < 0.0015 and abs(s16["rule"][0] - REFS[f]["rule"]) < 0.0015
        det.append(f"{f[:3]} 16: law {s16['law'][0]:+.3f} rule {s16['rule'][0]:+.3f}; 19: law {s19['law'][0]:+.3f} +-{s19['law'][1]:.3f} rule {s19['rule'][0]:+.3f} +-{s19['rule'][1]:.3f}")
    ok &= abs(SL[(kn, "canonical")][1]["law"][0] - 0.080) < 0.0015 and abs(SL[(kn, "alt")][1]["law"][0] - 0.065) < 0.0015
    return ok, "; ".join(det)
for kn in KERNELS:
    ok, det = g3(kn); check(f"G3 SLUGGS-mass rows (CFG55 16-galaxy law/rule; CFG38 19-galaxy law +0.080/+0.065), kernel {kn}", ok, det)

# ---------------------------------------------------------------- C3 / sensitivities computed at MAIN only
if not MUTATE:
    P("\n== C3: JAM x 1/2 (own implementation) ==")
    JAMF_SAVE = JAMF; globals()["JAMF"] = 0.5
    half = {}
    for kn in KERNELS:
        r = run(SEL, kn, "canonical"); half[kn] = summ(r)
        P(f"  {kn}: {fmt(half[kn])}; excluded {r['excl']}")
    globals()["JAMF"] = JAMF_SAVE
    for kn in KERNELS:
        m, e1, e0, n = half[kn]["law"]
        check(f"C3 JAM x1/2 law offset -> +0.216 (9.1 sigma), kernel {kn}", abs(m - 0.216) < 0.0015, f"{m:+.3f} +- {e1:.3f} = {m/e1:.1f}s (ddof0 {m/e0:.1f}s)")
    json.dump({kn: {k: list(v) for k, v in half[kn].items()} for kn in half}, open(os.path.join(HERE, "cfg76_half_jam.json"), "w"))

    P("\n== reported sensitivities (canonical, primary kernel nu_mono unless stated; N=16) ==")
    def rep(label, **kw):
        r = run(kw.pop("rows", SEL), kw.pop("kn", "nu_mono"), "canonical", **kw)
        P(f"  {label:58s}: {fmt(summ(r))}" + (f"; rule-excluded {r['excl']}" if r['excl'] else "")); return r
    rep("primary")
    rep("distance mode dyn (M_JAM ~ D)", dist_mode="dyn")
    rep("Hernquist enclosed fraction at r_1/2", fmode="hern")
    r0 = ALL[("nu_mono", "canonical")]
    sub = [n for n in SEL if n != 7457]
    P(f"  {'without NGC 7457':58s}: {fmt(summ(r0, sub))}")
    rep("Salpeter population masses (ATLAS3D logML_Salp x L)", salp=True)
    for gam in (2.4, 2.7, 3.3, 3.6):
        rep(f"gamma = {gam}", gamma=gam)
    for bt in (-0.3, 0.3):
        rep(f"beta = {bt:+.1f}", beta=bt)
    # corrected-key sample with JAM (only galaxies in ATLAS3D qual>=1)
    SELc = sorted(n for n in BINS_c if f"NGC{n:04d}" in AT and AT[f"NGC{n:04d}"]["qual"] >= 1)
    rep(f"corrected-key sample, N={len(SELc)}", rows=SELc, bins=BINS_c)
    if extra:
        rep(f"corrected-key extras only {['NGC%d'%n for n in extra]}", rows=[n for n in extra if n in SELc], bins=BINS_c)
    # r_1/2 vs Re
    ratio = [10 ** AT[f"NGC{n:04d}"]["logr12"] / ARCSEC * BINS[n]["D"] * 1e3 / BINS[n]["Re"] for n in SEL]
    P(f"  r_1/2(ATLAS3D at SLUGGS D) / R_e(SLUGGS): median {np.median(ratio):.2f}, range {min(ratio):.2f}-{max(ratio):.2f}")
    dr = [BINS[n]["D"] / AT[f"NGC{n:04d}"]["Dist_Mpc"] for n in SEL]
    P(f"  D_SLUGGS/D_ATLAS3D: median {np.median(dr):.3f}, range {min(dr):.3f}-{max(dr):.3f}")
    lm = [math.log10(ALL[('nu_mono','canonical')]['Ms'][n][0]) - BINS[n]['lMs'] for n in SEL]
    P(f"  log10(M*_JAM-calibrated law / SLUGGS M*): median {np.median(lm):+.3f} (CFG55: -0.10)")
    P("\n== per-galaxy (canonical, nu_mono): NGC, D, logM*_SLUGGS, logM*_law, logM*_rule, off_law, off_rule, off_law(SLUGGS M*) ==")
    rs = SL[("nu_mono", "canonical")]
    rsl = run(SEL, "nu_mono", "canonical", sluggs_mass=True)
    for n in SEL:
        Ml, Mr = r0["Ms"][n]
        P(f"  NGC{n:<5d} D={BINS[n]['D']:5.1f} {BINS[n]['lMs']:.2f} {math.log10(Ml):.2f} " + (f"{math.log10(Mr):.2f}" if Mr else " n/a ") +
          f"  {r0['law'][n]:+.3f} " + (f"{r0['rule'][n]:+.3f}" if n in r0['rule'] else " n/a  ") + f"  {rsl['law'][n]:+.3f}")
    json.dump({"main": {f"{k[0]}|{k[1]}": {kk: list(vv) for kk, vv in summ(v).items()} for k, v in ALL.items()},
               "sluggs_mass": {f"{k[0]}|{k[1]}": {"16": {kk: list(vv) for kk, vv in v[0].items()}, "19": {kk: list(vv) for kk, vv in v[1].items()}} for k, v in SL.items()},
               "per_galaxy_law": {str(n): r0["law"][n] for n in SEL}, "per_galaxy_rule": {str(n): v for n, v in r0["rule"].items()},
               "per_galaxy_all": {f"{k[0]}|{k[1]}": {"law": {str(n): v for n, v in r_["law"].items()}, "rule": {str(n): v for n, v in r_["rule"].items()},
                                                    "Ms": {str(n): list(v) for n, v in r_["Ms"].items()}} for k, r_ in ALL.items()},
               "sluggs_per_galaxy": {f"{k[0]}|{k[1]}": {str(n): v for n, v in run(SEL, k[0], k[1], sluggs_mass=True)["law"].items()} for k in ALL}},
              open(os.path.join(HERE, "cfg76_results.json"), "w"), indent=1)

# ---------------------------------------------------------------- MUTATE gates
if MUTATE:
    ref = json.load(open(os.path.join(HERE, "cfg76_results.json")))["main"]
    P("\n== MUTATE checks against the stored main run ==")
    for kn in KERNELS:
        for f in FOOTS:
            s = summ(ALL[(kn, f)]); mm = ref[f"{kn}|{f}"]
            dl = s["law"][0] - mm["law"][0]; dr_ = s["rule"][0] - mm["rule"][0]
            P(f"  {kn} {f}: law {mm['law'][0]:+.3f} -> {s['law'][0]:+.3f} ({dl:+.3f}); rule {mm['rule'][0]:+.3f} -> {s['rule'][0]:+.3f} ({dr_:+.3f})")
            check(f"M1 both offsets rise by > 0.05 dex when JAM masses are halved ({kn}, {f})", dl > 0.05 and dr_ > 0.05)
    P("  (the G1/G3 checks above are the headline gate: they must FAIL in this mode)")

open(os.path.join(HERE, "cfg76_MUTATE.out" if MUTATE else "cfg76_main.out"), "w").write("\n".join(out_lines) + "\n")
P(f"\nFAILED CHECKS ({len(FAILS)}): " + "; ".join(FAILS))
sys.exit(1 if FAILS else 0)
