#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG104 independent re-derivation of CFG112's headline.  The frozen spec is CFG104_SPEC_FROZEN.txt (sha256 printed at run time).
Estimator functions (kernels, Jeans, halo, ATLAS3D, GC dispersions) are REUSED by copy from CFG76's cfg76_sluggs_jam.py; the phi layer,
per-galaxy gamma_i, scans, intersections and attack rows are new.  Data as read-only DATA: real_research/data/* and CFG71's committed results JSON
(the nine other populations and the C1 control target).  Repo root: env ZF_REPO, else searched upward from this file / the cwd.
MUTATE=1: gamma_i = 3 for every galaxy."""
import os, sys, math, json, hashlib, time
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
def find_repo():
    cands = []
    if os.environ.get("ZF_REPO"): cands.append(os.environ["ZF_REPO"])
    for start in (HERE, os.getcwd()):
        p = start
        for _ in range(12):
            cands.append(p); p = os.path.dirname(p)
    for c in cands:
        if os.path.isdir(os.path.join(c, "real_research", "data")) and os.path.isdir(os.path.join(c, "campaign_fresh_gravity")):
            return c
    raise SystemExit("repo root not found: set ZF_REPO")
REPO = find_repo()
DATA = os.path.join(REPO, "real_research", "data")
CFG71_JSON = os.path.join(REPO, "campaign_fresh_gravity", "CFG71_universal_fraction_dynamical_sluggs_results.json")
MUTATE = os.environ.get("MUTATE", "0") == "1"
spec = open(os.path.join(HERE, "CFG104_SPEC_FROZEN.txt"), "rb").read()
out_lines = []
T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); out_lines.append(s)
P("CFG104  MUTATE=%s  spec sha256 %s  repo=%s" % (MUTATE, hashlib.sha256(spec).hexdigest()[:16], "<ZF_REPO>"))
FAILS = []
def check(name, ok, detail=""):
    P(("  [PASS] " if ok else "  [FAIL] ") + name + ("   (" + detail + ")" if detail else ""))
    if not ok: FAILS.append(name)

# ---------------------------------------------------------------- constants (as CFG76 / hunt_lib)
G = 6.674e-11; kpc = 3.0857e19; Mpc = 3.0857e22; Msun = 1.989e30
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
FB = 0.02237 / (0.02237 + 0.1200)
ARCSEC = 206264.806
FOOTS = ("canonical", "alt")
def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))
KERN = nu_rar          # CFG76: the plain RAR kernel reproduces CFG55/CFG71

# ---------------------------------------------------------------- data (CFG76 copy)
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
    keys = {f"NGC{n:04d}": n for n in GAL}      # h50's key ('NGC720' silently dropped), as CFG76's faithful reading
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
            mu, s = mle_sigma(a[m, 1], a[m, 2]); bins.append((float(np.median(Rk[m])), s))
        if len(bins) < 2: continue
        Rb = np.array([b[0] for b in bins]); Sb = np.array([b[1] for b in bins])
        out = Rb > max(1.0 * Re, 2.0)
        if out.sum() == 0: out = np.ones(len(Rb), bool)
        B[n] = dict(n=n, N=len(a), Re=Re, Rb=Rb, Sb=Sb, out=out, D=D, lMs=g["lMs"])
    return B

# ---------------------------------------------------------------- Jeans (CFG76 copy; g given as an array on RG)
RG = np.geomspace(0.02, 3e4, 1200); LRG = np.log(RG)
def sigma_r2_arr(g, gamma, beta=0.0):
    w = RG ** (2 * beta - gamma)
    integ = w * g * (RG * kpc)
    tail = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(LRG))[::-1])[::-1], [0.0]])
    return tail / RG ** (2 * beta - gamma)
def sigma_r2(gfun, gamma, beta=0.0): return sigma_r2_arr(gfun(RG), gamma, beta)
_U = np.linspace(0.0, 6.0, 500); _CH = np.cosh(_U)
def sigma_los(R, s2, gamma, beta=0.0):
    r = np.outer(np.atleast_1d(R), _CH)
    s = np.exp(np.interp(np.log(r), LRG, np.log(np.maximum(s2, 1e-6))))
    rho = r ** (-gamma)
    num = np.trapz((1 - beta / _CH ** 2) * rho * s * r, _U, axis=1)
    den = np.trapz(rho * r, _U, axis=1)
    return np.sqrt(num / den) / 1e3

# ---------------------------------------------------------------- halo machinery (CFG76 copy)
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
T_ = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "mandelbaum2016_lbg_halo_mass.tsv")) if l.strip() and not l.startswith("#")]
RED = np.array([[float(r[1]), float(r[3])] for r in T_[1:] if r[0] == "red"])
def collapse_Mh(Ms):
    lx = np.interp(math.log10(Ms), RED[:, 0], RED[:, 1])
    return float(m200c_from_m200m(10 ** lx / 0.673))
def one_plus_delta_ta(Om):
    OL = 1 - Om
    t_age = 2.0 / (3 * math.sqrt(OL)) * math.asinh(math.sqrt(OL / Om))
    def tta(k):
        def f(th):
            u = math.sin(th) ** 2
            if u <= 0: return 0.0
            arg = k * Om * (1 / u - 1) + OL * (u * u - 1)
            return 2 * math.sin(th) * math.cos(th) / math.sqrt(max(arg, 1e-300))
        return quad(f, 0, math.pi / 2, limit=200)[0]
    k_lo = max(2 * OL / Om * 1.0000001, 1.0001)
    return brentq(lambda k: tta(k) - t_age, k_lo, 1e4, xtol=1e-12)
import warnings; warnings.filterwarnings("ignore")
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

# ---------------------------------------------------------------- ATLAS3D (CFG76 copy, dist_mode 'dyn')
lines = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "atlas3d_fj_table.tsv")) if l.strip() and not l.startswith("#")]
AH = lines[0]; AT = {}
for r in lines[1:]:
    d = dict(zip(AH, r))
    def _fl(v):
        try: return float(v)
        except Exception: return float("nan")
    AT[d["name"]] = {k: (_fl(v) if k != "name" else v) for k, v in d.items()}
def jam_inputs(n, D_S):
    a = AT[f"NGC{n:04d}"]
    ml = 10 ** a["logML_JAM"]
    MJ = ml * 10 ** a["logL"] * (D_S / a["Dist_Mpc"])          # CFG76 dist_mode 'dyn': M_JAM ~ D
    r12 = 10 ** a["logr12"] / ARCSEC * D_S * 1e3
    return MJ, r12, a["qual"]

# ================================================================ NEW: the phi layer
PHI = np.round(np.linspace(0.0, 1.0, 101), 2)
class Gal:
    """one SLUGGS galaxy, one footing: phi-dependent calibration (exact, memoised T) and phi-dependent prediction"""
    def __init__(self, b, foot):
        self.b = b; self.foot = foot; self.n = b["n"]
        self.MJ, self.r12, _ = jam_inputs(self.n, b["D"])
        self.a0 = A0[foot]; self.Re = b["Re"]; self.a_h = self.Re / 1.8153
        self.f = 0.5
        self.Tm = {}
        self.grid_rule = np.linspace(6.5, 13.8, 220); self.grid_law = np.linspace(1.0, 13.8, 130)
        self.base_rule = np.array([self.base(x) for x in self.grid_rule]); self.T_rule = np.array([self.T(x) for x in self.grid_rule])
        self.base_law = np.array([self.base(x) for x in self.grid_law])
        self.cache = {}
    def base(self, lM):
        M = 10 ** lM; gN = G * self.f * M * Msun / (self.r12 * kpc) ** 2
        return self.f * M * float(KERN(np.array([gN / self.a0]))[0]) - self.MJ / 2.0
    def T(self, lM):
        if lM not in self.Tm:
            fex, Mh = rule_parts(10 ** lM, self.foot, KERN)
            self.Tm[lM] = fex * (1 - FB) * float(nfw_enclosed(Mh, self.r12))
        return self.Tm[lM]
    def calibrate(self, phi):
        if phi == 0:
            grid, vals, F = self.grid_law, self.base_law, self.base
        else:
            grid = self.grid_rule; vals = self.base_rule + phi * self.T_rule
            F = lambda x: self.base(x) + phi * self.T(x)
        roots = [brentq(F, grid[i], grid[i + 1], xtol=1e-12) for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
        return (10 ** max(roots)) if roots else None
    def state(self, phi):
        if phi in self.cache: return self.cache[phi]
        Ms = self.calibrate(phi)
        if Ms is None: st = None
        else:
            fex, Mh = rule_parts(Ms, self.foot, KERN) if phi > 0 else (0.0, None)
            Mb = Ms * Msun * RG ** 2 / (RG + self.a_h) ** 2; gN = G * Mb / (RG * kpc) ** 2
            g = gN * KERN(gN / self.a0)
            if phi > 0 and fex > 0: g = g + phi * G * fex * (1 - FB) * nfw_enclosed(Mh, RG) * Msun / (RG * kpc) ** 2
            st = (Ms, g)
        self.cache[phi] = st; return st
    def offset(self, phi, gamma):
        st = self.state(phi)
        if st is None: return np.nan
        b = self.b
        pred = sigma_los(b["Rb"], sigma_r2_arr(st[1], gamma), gamma)
        return float(np.mean(np.log10(b["Sb"][b["out"]] / pred[b["out"]])))

def scan_stats(off):
    """off: (ngal, nphi) with nan for dropped; returns o, e (ddof=1 SEM), n"""
    o = np.full(off.shape[1], np.nan); e = np.full(off.shape[1], np.nan); cnt = np.sum(np.isfinite(off), axis=0)
    for j in range(off.shape[1]):
        v = off[np.isfinite(off[:, j]), j]
        if len(v) >= 2: o[j] = v.mean(); e[j] = v.std(ddof=1) / math.sqrt(len(v))
    return o, e, cnt

# ---------------------------------------------------------------- intersections
def okpts(o, e, k): return np.isfinite(o) & np.isfinite(e) & (np.abs(o) <= k * e)
def segs_of(mask, grid):
    segs = []; i = 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j + 1 < len(mask) and mask[j + 1]: j += 1
            segs.append((float(grid[i]), float(grid[j]))); i = j + 1
        else: i += 1
    return segs
def fmt_segs(s): return "empty" if not s else " U ".join("[%.2f, %.2f]" % x for x in s)
def inter_mask(sets, k):
    m = np.ones(len(PHI), bool)
    for (o, e) in sets: m &= okpts(o, e, k)
    return m

# ================================================================ closed-form controls (reused Jeans)
P("\n== C2 closed-form limits of the reused Jeans functions ==")
rr = np.array([1.0, 3.0, 10.0, 30.0, 100.0]); M0 = 1e11
def g_pt(r): return G * M0 * Msun / (r * kpc) ** 2
errs = []
for gam in (2.0, 2.5, 3.0, 4.0):
    s2i = np.interp(np.log(rr), LRG, sigma_r2(g_pt, gam)); ref = G * M0 * Msun / ((gam + 1) * rr * kpc)
    errs.append(float(np.max(np.abs(s2i / ref - 1))))
check("C2a point mass, isotropic, rho~r^-gamma: sigma_r^2 = GM/((gamma+1) r), gamma in {2,2.5,3,4}", max(errs) < 1e-3, "max rel err " + ", ".join("%.1e" % e for e in errs))
a0c = A0["canonical"]
def g_dm(r): return np.sqrt(G * M0 * Msun * a0c) / (r * kpc)
errs = []
for gam in (2.5, 3.0):
    s2d = np.interp(np.log(rr), LRG, sigma_r2(g_dm, gam)); refd = np.sqrt(G * M0 * Msun * a0c) / gam
    sl = sigma_los(rr, sigma_r2(g_dm, gam), gam)
    errs += [float(np.max(np.abs(s2d / refd - 1))), float(np.max(np.abs(sl * 1e3 / np.sqrt(refd) - 1)))]
check("C2b deep-MOND point mass: sigma_r^2 = sqrt(G M a0)/gamma; LOS of constant sigma_r = sigma_r", max(errs) < 1e-3, "max rel err %.1e" % max(errs))

# ================================================================ sample
P("\n== sample ==")
GC_, nall = load_gcs(); BINS = make_bins(GC_)
SEL = sorted(n for n in BINS if f"NGC{n:04d}" in AT and AT[f"NGC{n:04d}"]["qual"] >= 1)
check("S1 sample: 27 galaxies, 3440 GC RVs, 19 in dispersion sample, 16 with JAM quality >= 1", len(GAL) == 27 and nall == 3440 and len(BINS) == 19 and len(SEL) == 16, f"{len(GAL)}/{nall}/{len(BINS)}/{len(SEL)}")
GAMMA_REL = {n: float(np.clip(-0.63 * BINS[n]["lMs"] + 9.81, 2.0, 4.0)) for n in SEL}
GAM = {n: (3.0 if MUTATE else GAMMA_REL[n]) for n in SEL}
P("  gamma_i (relation -0.63 logM* + 9.81 clipped [2,4]): " + ", ".join("NGC%d %.2f(logM*=%.2f)" % (n, GAMMA_REL[n], BINS[n]["lMs"]) for n in SEL))
P("  used gamma_i: min %.2f max %.2f mean %.2f  %s" % (min(GAM.values()), max(GAM.values()), np.mean(list(GAM.values())), "(MUTATE: all 3)" if MUTATE else ""))

# ================================================================ scans
P("\n== building calibrations and scans (exact) ==")
GALS = {f: {n: Gal(BINS[n], f) for n in SEL} for f in FOOTS}
def sluggs_scan(foot, gam):
    off = np.full((len(SEL), len(PHI)), np.nan)
    for i, n in enumerate(SEL):
        for j, ph in enumerate(PHI): off[i, j] = GALS[foot][n].offset(float(ph), gam[n])
    return off
OFF = {}; OFF3 = {}
for f in FOOTS:
    OFF[f] = sluggs_scan(f, GAM)
    OFF3[f] = OFF[f] if MUTATE else sluggs_scan(f, {n: 3.0 for n in SEL})
    P(f"  {f}: scans done at {time.time()-T0:.0f}s")
SC = {f: scan_stats(OFF[f]) for f in FOOTS}
SC3 = {f: scan_stats(OFF3[f]) for f in FOOTS}

# ---------------------------------------------------------------- the nine other populations (CFG71 JSON = DATA)
J = json.load(open(CFG71_JSON))["numbers"]["scan"]
NAMES = ["U1 MW ultra-faints (KM median)", "U2 MW classical dSphs", "U3 M31 Collins+13", "U4 M31 LVD", "U6 X-ray ellipticals",
         "U7 DT23 four S0/S0a", "U8 UGC 2487", "U9 Bootes I (multi-epoch)", "U10 Tucana II (multi-epoch)"]
NINE = {f: {nm: (np.array(J[f"{nm}|{f}"]["o"]), np.array(J[f"{nm}|{f}"]["e"])) for nm in NAMES} for f in FOOTS}
U5J = {f: (np.array(J[f"U5 SLUGGS (dynamical masses, 16)|{f}"]["o"]), np.array(J[f"U5 SLUGGS (dynamical masses, 16)|{f}"]["e"])) for f in FOOTS}
check("J0 CFG71 JSON scan grid is my 101-point grid", np.allclose(J[f"{NAMES[0]}|canonical"]["phi"], PHI, atol=1e-9))

# ---------------------------------------------------------------- controls C1 / C1b / C3 / C4
P("\n== controls ==")
for f in FOOTS:
    o3, e3, n3 = SC3[f]; oj, ej = U5J[f]
    do = float(np.nanmax(np.abs(o3 - oj))); de = float(np.nanmax(np.abs(e3 - ej)))
    if not MUTATE or True:
        check(f"C1 gamma=3: my SLUGGS scan == CFG71 committed U5 scan, all 101 points ({f}); tol 1e-4", do < 1e-4 and de < 1e-4, f"max|d o| {do:.2e}, max|d e| {de:.2e}, n(phi) {n3.min()}-{n3.max()}")
REF = {"canonical": dict(law=(0.09698, 0.02431), rule=(0.04564, 0.01771)), "alt": dict(law=(0.08800, 0.02414), rule=(0.04665, 0.01792))}
for f in FOOTS:
    o3, e3, n3 = SC3[f]
    ok = all(abs(o3[i] - REF[f][k][0]) < 5e-4 and abs(e3[i] - REF[f][k][1]) < 5e-4 for k, i in (("law", 0), ("rule", 100)))
    check(f"C1b gamma=3 law(phi=0)/rule(phi=1) means and errors ({f}) vs CFG76/CFG71, 5e-4", ok, f"law {o3[0]:+.5f}+-{e3[0]:.5f}, rule {o3[100]:+.5f}+-{e3[100]:.5f}")
def nine_window(f, k, names=NAMES):
    return inter_mask([NINE[f][nm] for nm in names], k)
for f, ref in (("canonical", (0.23, 0.71)), ("alt", (0.21, 0.66))):
    s = segs_of(nine_window(f, 2), PHI)
    check(f"C3/P2 nine-population 2-sigma intersection ({f}) = CFG75's {ref}", len(s) == 1 and abs(s[0][0] - ref[0]) < 1e-9 and abs(s[0][1] - ref[1]) < 1e-9, fmt_segs(s))
for f in FOOTS:
    o, e, n = SC[f]; d = np.diff(o[np.isfinite(o)])
    check(f"C4 SLUGGS offset non-increasing in phi ({f})", bool(np.all(d <= 1e-6)), f"max step {d.max():+.2e}; n(phi) {n.min()}-{n.max()}")

# ---------------------------------------------------------------- main results, R1 / P1-P4
P("\n== MAIN: SLUGGS with gamma_i%s ==" % (" (MUTATE: gamma = 3)" if MUTATE else ""))
RES = {}
for f in FOOTS:
    o, e, n = SC[f]
    P(f"  [{f}] SLUGGS offset(phi) / sigma: " + "; ".join("phi=%.2f %+.4f (%.2fs, n=%d)" % (ph, o[int(round(ph * 100))], o[int(round(ph * 100))] / e[int(round(ph * 100))], n[int(round(ph * 100))]) for ph in (0, 0.25, 0.5, 0.71, 0.75, 1.0)))
    RES[f] = {}
    for k in (1, 2, 3):
        sl = segs_of(okpts(o, e, k), PHI)
        ni = segs_of(nine_window(f, k), PHI)
        te = segs_of(inter_mask([(o, e)] + [NINE[f][nm] for nm in NAMES], k), PHI)
        RES[f][k] = dict(sluggs=sl, nine=ni, ten=te)
        P(f"  [{f}] {k} sigma: SLUGGS {fmt_segs(sl)} | nine {fmt_segs(ni)} | ten {fmt_segs(te)}")
    # individual windows at 2 sigma -> binding populations
    ind = {}
    for nm in NAMES:
        s = segs_of(okpts(*NINE[f][nm], 2), PHI); ind[nm] = s
    lo_pop = max(NAMES, key=lambda nm: ind[nm][0][0] if ind[nm] else 9); hi_pop = min(NAMES, key=lambda nm: ind[nm][-1][1] if ind[nm] else -9)
    RES[f]["lo_pop"] = lo_pop; RES[f]["hi_pop"] = hi_pop
    P(f"  [{f}] individual 2-sigma windows: " + "; ".join(f"{nm.split()[0]} {fmt_segs(ind[nm])}" for nm in NAMES))
    P(f"  [{f}] nine-set lower edge set by {lo_pop}; upper edge set by {hi_pop}")
for f, ref in (("canonical", (0.77, 1.0)), ("alt", (0.77, 1.0))):
    s = RES[f][2]["sluggs"]
    check(f"P1 SLUGGS 2-sigma window with gamma_i = [0.77, 1.00] ({f})", len(s) == 1 and abs(s[0][0] - ref[0]) < 1e-9 and abs(s[0][1] - ref[1]) < 1e-9, fmt_segs(s))
for f in FOOTS:
    check(f"P3 the binding (upper-edge) population of the nine is the M31 LVD ({f})", RES[f]["hi_pop"].startswith("U4"), RES[f]["hi_pop"])
for f in FOOTS:
    check(f"P4 [HEADLINE] ten-population 2-sigma intersection is empty ({f})", RES[f][2]["ten"] == [], fmt_segs(RES[f][2]["ten"]))

# ---------------------------------------------------------------- R2 / R3: fine-grid gap and minimax level
PF = np.linspace(0, 1, 2001)
def interp_pair(o, e): return (np.interp(PF, PHI, o), np.interp(PF, PHI, e))
def fine_window(pairs, k):
    m = np.ones(len(PF), bool)
    for (o, e) in pairs: m &= (np.abs(o) <= k * e)
    return segs_of(m, PF)
def kstar(pairs):
    z = np.max([np.abs(o) / e for (o, e) in pairs], axis=0); i = int(np.argmin(z)); return float(z[i]), float(PF[i])
P("\n== R2/R3: fine-grid (0.0005, linear interpolation of o and e) windows, gap, and minimax level k* ==")
for f in FOOTS:
    sp = interp_pair(*SC[f][:2]); sp3 = interp_pair(*SC3[f][:2]); np_ = [interp_pair(*NINE[f][nm]) for nm in NAMES]
    sw = fine_window([sp], 2); nw = fine_window(np_, 2)
    gap = (sw[0][0] - nw[-1][1]) if sw and nw else float("nan")
    ks, ps = kstar([sp] + np_); ks3, ps3 = kstar([sp3] + np_); kn, pn = kstar(np_)
    lvd = interp_pair(*NINE[f]["U4 M31 LVD"]); kl, pl = kstar([sp, lvd])
    P(f"  [{f}] fine 2-sigma: SLUGGS {fmt_segs(sw)}; nine {fmt_segs(nw)}; gap (SLUGGS low - nine high) = {gap:+.4f}")
    P(f"  [{f}] k* (min over phi of the largest |o/e|): ten {ks:.3f} at phi {ps:.3f} | ten with gamma=3 {ks3:.3f} at {ps3:.3f} | nine {kn:.3f} at {pn:.3f} | SLUGGS+LVD only {kl:.3f} at {pl:.3f}")
    RES[f]["fine"] = dict(sluggs=sw, nine=nw, gap=gap, kstar_ten=ks, phi_kstar=ps, kstar_ten_g3=ks3, kstar_nine=kn, kstar_slug_lvd=kl)

# ---------------------------------------------------------------- gamma-grid table for R4/R5/R6
P("\n== gamma-grid table (1.5-5.0 step 0.1) of per-galaxy offsets for the sensitivity rows ==")
GG = np.round(np.arange(1.5, 5.0001, 0.1), 2)
TAB = {}   # foot -> (ngal, nphi, ngamma)
for f in FOOTS:
    t = np.full((len(SEL), len(PHI), len(GG)), np.nan)
    for i, n in enumerate(SEL):
        for j, ph in enumerate(PHI):
            if GALS[f][n].state(float(ph)) is None: continue
            for k, gm in enumerate(GG): t[i, j, k] = GALS[f][n].offset(float(ph), float(gm))
    TAB[f] = t; P(f"  {f}: table done at {time.time()-T0:.0f}s")
SPL = {f: [[CubicSpline(GG, np.nan_to_num(TAB[f][i, j]), extrapolate=False) if np.isfinite(TAB[f][i, j, 0]) else None for j in range(len(PHI))] for i in range(len(SEL))] for f in FOOTS}
def off_from_table(f, gam_vec):
    o = np.full((len(SEL), len(PHI)), np.nan)
    for i in range(len(SEL)):
        for j in range(len(PHI)):
            if SPL[f][i][j] is not None: o[i, j] = float(SPL[f][i][j](gam_vec[i]))
    return o
# interpolation control
mx = 0.0
for f in FOOTS:
    for i, n in enumerate(SEL[:6]):
        for j in (0, 50, 100):
            for gm in (2.55, 3.33):
                d = abs(float(SPL[f][i][j](gm)) - GALS[f][n].offset(float(PHI[j]), gm)) if SPL[f][i][j] is not None else 0.0
                mx = max(mx, d)
check("R6c gamma-table cubic interpolation vs direct evaluation (36 checks), max |d offset| < 1e-4", mx < 1e-4, f"{mx:.2e}")
GV = np.array([GAM[n] for n in SEL])
for f in FOOTS:
    d = np.nanmax(np.abs(off_from_table(f, GV) - OFF[f]))
    check(f"R6d table reproduces the direct gamma_i scan ({f}), max |d| < 1e-4", d < 1e-4, f"{d:.2e}")

def analysis(f, off):
    o, e, n = scan_stats(off)
    sw = segs_of(okpts(o, e, 2), PHI); nw = segs_of(nine_window(f, 2), PHI); tw = segs_of(inter_mask([(o, e)] + [NINE[f][nm] for nm in NAMES], 2), PHI)
    pairs = [interp_pair(o, e)] + [interp_pair(*NINE[f][nm]) for nm in NAMES]
    ks, ps = kstar(pairs)
    return sw, tw, ks, o, e

P("\n== R4: global shift of every gamma_i by delta ==")
R4 = {}
for f in FOOTS:
    for dl in (-0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 1.0):
        gv = np.clip(GV + dl, GG[0], GG[-1])
        sw, tw, ks, o, e = analysis(f, off_from_table(f, gv))
        R4[(f, dl)] = (sw, tw, ks)
        P(f"  [{f}] delta {dl:+.1f}: SLUGGS 2-sigma {fmt_segs(sw):>14s} | ten {fmt_segs(tw):>14s} | k* {ks:.3f} | SLUGGS phi=1 {o[100]/e[100]:+.2f}s")

P("\n== R5: per-galaxy offsets and leave-one-out of the SLUGGS window ==")
for f in FOOTS:
    P(f"  [{f}] per-galaxy offset at phi=0/1 (gamma_i): " + "; ".join("NGC%d %+.3f/%+.3f" % (n, OFF[f][i, 0], OFF[f][i, 100]) for i, n in enumerate(SEL)))
    lo = []
    for i, n in enumerate(SEL):
        off = np.delete(OFF[f], i, axis=0); o, e, _ = scan_stats(off)
        sw = segs_of(okpts(o, e, 2), PHI); tw = segs_of(inter_mask([(o, e)] + [NINE[f][nm] for nm in NAMES], 2), PHI)
        lo.append((n, sw, tw))
    P(f"  [{f}] leave-one-out SLUGGS 2-sigma windows: " + "; ".join("-NGC%d %s%s" % (n, fmt_segs(sw), "" if not tw else " TEN=" + fmt_segs(tw)) for n, sw, tw in lo))
    RES[f]["loo_open"] = [n for n, sw, tw in lo if tw]

P("\n== R6: Monte Carlo scatter on the per-galaxy slopes (200 draws each, seed 20260929) ==")
rng = np.random.default_rng(20260929)
MC = {}
for sg in (0.2, 0.4):
    for f in FOOTS:
        lows = []; nopen = 0; ks_l = []
        for d in range(200):
            gv = np.clip(GV + rng.normal(0, sg, len(GV)), 1.5, 4.5)
            sw, tw, ks, o, e = analysis(f, off_from_table(f, gv))
            lows.append(sw[0][0] if sw else np.nan); ks_l.append(ks)
            if tw: nopen += 1
        lows = np.array(lows)
        MC[(sg, f)] = dict(open=nopen, lows=lows)
        P(f"  sigma_gamma {sg} [{f}]: ten-set 2-sigma non-empty in {nopen}/200 draws; SLUGGS lower edge quantiles 5/50/95% = {np.nanpercentile(lows,5):.2f}/{np.nanpercentile(lows,50):.2f}/{np.nanpercentile(lows,95):.2f} (SLUGGS window empty in {int(np.isnan(lows).sum())}); k* median {np.median(ks_l):.2f}")

P(f"\nR7 (text): the relation's values {min(GAMMA_REL.values()):.2f}-{max(GAMMA_REL.values()):.2f} are 3-D density slopes only if the source quotes 3-D slopes; if it quotes projected (surface-density) slopes Gamma, gamma_3D = Gamma+1 (R4 delta +1.0 row). "
  "The SLUGGS error e is the sample SEM of the offsets and contains no gamma uncertainty.")
json.dump(dict(mutate=MUTATE, res={f: {str(k): v for k, v in RES[f].items()} for f in FOOTS}, gamma=GAMMA_REL,
               scan={f: {"o": SC[f][0].tolist(), "e": SC[f][1].tolist(), "n": SC[f][2].tolist()} for f in FOOTS},
               R4={f"{k[0]}|{k[1]}": [v[0], v[1], v[2]] for k, v in R4.items()},
               MC={f"{k[0]}|{k[1]}": dict(open=v["open"], lows=[None if not np.isfinite(x) else float(x) for x in v["lows"]]) for k, v in MC.items()}),
          open(os.path.join(HERE, "cfg104_MUTATE_results.json" if MUTATE else "cfg104_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, "cfg104_MUTATE.out" if MUTATE else "cfg104_main.out"), "w").write("\n".join(out_lines) + "\n")
P(f"\nseconds {time.time()-T0:.0f}\nFAILED CHECKS ({len(FAILS)}): " + "; ".join(FAILS))
sys.exit(1 if FAILS else 0)
