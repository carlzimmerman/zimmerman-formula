#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG106 independent re-derivation of CFG114's headline (SLUGGS deficit in the gamma-shift x beta box).
Spec: CFG106_SPEC_FROZEN.txt (frozen before the first run; its sha256 is printed).  That file IS the frozen docstring: question, model, box, sigma statistic,
pass lines G0-G6, controls C1-C6, MUTATE, reported rows R1-R8.
Reuses (disclosed) the CFG76 pipeline (data, GC bins, JAM calibration, rule debris); the Jeans solver below is NEW code.
Does not read/exec/import any CFG114/CFG112/CFG113 script or output.
Repo root: env ZF_REPO, else walk up from this file / cwd until real_research/data is found.  MUTATE=1: bin dispersions x 10^(-D) at the weakest cell."""
import os, sys, math, json, hashlib, time
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.special import gamma as GAMMA

HERE = os.path.dirname(os.path.abspath(__file__))
def find_repo():
    if os.environ.get("ZF_REPO"): return os.environ["ZF_REPO"]
    for start in (HERE, os.getcwd()):
        d = start
        while True:
            if os.path.isdir(os.path.join(d, "real_research", "data")): return d
            nd = os.path.dirname(d)
            if nd == d: break
            d = nd
    raise SystemExit("set ZF_REPO to the repository root")
REPO = find_repo(); DATA = os.path.join(REPO, "real_research", "data")
MUTATE = os.environ.get("MUTATE", "0") == "1"
T0 = time.time()
spec = open(os.path.join(HERE, "CFG106_SPEC_FROZEN.txt"), "rb").read()
out_lines = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); out_lines.append(s)
P("CFG106  MUTATE=%s  spec sha256 %s" % (MUTATE, hashlib.sha256(spec).hexdigest()[:16]))
FAILS = []
def check(name, ok, detail=""):
    P(("  [PASS] " if ok else "  [FAIL] ") + name + ("   (" + detail + ")" if detail else ""))
    if not ok: FAILS.append(name)

# ------------------------------------------------------------------ constants (CFG76 values)
G = 6.674e-11; kpc = 3.0857e19; Mpc = 3.0857e22; Msun = 1.989e30
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
FB = 0.02237 / (0.02237 + 0.1200)
ARCSEC = 206264.806
FOOTS = ("canonical", "alt")
def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))
kern = nu_rar

# ------------------------------------------------------------------ data + GC bins (CFG76 pipeline, reused)
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
    keys = {f"NGC{n:04d}": n for n in GAL}      # h50-faithful key (drops 3-digit NGCs)
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
def clip3(rec, vsys, nsig=3.0):
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
        a = clip3(GC[n], g["vsys"])
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

# ------------------------------------------------------------------ halo/rule machinery (CFG76 as documented in CFG35/36; reused)
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
    t_age = 2.0 / (3 * math.sqrt(OL)) * math.asinh(math.sqrt(OL / Om)) if OL > 0 else 2.0 / 3.0
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
def edge_phantom(Mb, foot, xe=0.40):
    a0 = A0_MPC[foot]
    Mlaw = lambda r: Mb * float(kern(np.array([GMPC * Mb / r ** 2 / a0]))[0])
    fn = lambda lr: math.log(Mlaw(math.exp(lr)) / (4 * math.pi / 3 * math.exp(3 * lr) * RHOM0)) - math.log(K_TA)
    rta = math.exp(brentq(fn, math.log(1e-5), math.log(1e3), xtol=1e-13))
    return Mlaw(xe * rta) - Mb
def rule_parts(Ms, foot):
    Mh = collapse_Mh(Ms); Mc = (1 - FB) * Mh
    return max(0.0, 1.0 - edge_phantom(Ms, foot) / Mc), Mh

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
    MJ = 10 ** a["logML_JAM"] * 10 ** a["logL"] * (D_S / a["Dist_Mpc"])          # dist_mode 'dyn': M_JAM ~ D  (CFG76's exact reproduction of CFG55)
    r12 = 10 ** a["logr12"] / ARCSEC * D_S * 1e3
    return MJ, r12, a["qual"]
def Menc_frac(r12, Re, mode):
    if mode == "half": return 0.5
    a_h = Re / 1.8153; return (r12 / (r12 + a_h)) ** 2
def calibrate(MJ, r12, Re, foot, rule, fmode="half"):
    a0 = A0[foot]; f = Menc_frac(r12, Re, fmode)
    def F(lM):
        M = 10 ** lM; gN = G * f * M * Msun / (r12 * kpc) ** 2
        tot = f * M * float(kern(np.array([gN / a0]))[0])
        if rule:
            fex, Mh = rule_parts(M, foot)
            tot += fex * (1 - FB) * float(nfw_enclosed(Mh, r12))
        return tot - MJ / 2.0
    grid = np.linspace(6.5, 13.8, 220) if rule else np.linspace(1.0, 13.8, 130)
    vals = np.array([F(x) for x in grid])
    roots = [brentq(F, grid[i], grid[i + 1], xtol=1e-12) for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
    if not roots: return None
    return 10 ** max(roots)
def gfun_maker(Ms, a_h, a0, fex=0.0, Mh=None):
    def g(r):
        Mb = Ms * Msun * r ** 2 / (r + a_h) ** 2; gN = G * Mb / (r * kpc) ** 2
        gg = gN * kern(gN / a0)
        if fex > 0: gg = gg + G * fex * (1 - FB) * nfw_enclosed(Mh, r) * Msun / (r * kpc) ** 2
        return gg
    return g

# ================================================================== NEW: the Jeans / anisotropy solver
class Jeans:
    """Spherical Jeans, tracer nu = r^-gamma, constant beta.  Grid values g(r) [m/s^2] on self.r [kpc]."""
    def __init__(self, npts=4000, rmin=0.03, rmax=1e5, nodes=24, segs=((0, 1), (1, 3), (3, 8), (8, 22))):
        self.lr = np.linspace(math.log(rmin), math.log(rmax), npts); self.r = np.exp(self.lr); self.dl = self.lr[1] - self.lr[0]
        x, w = np.polynomial.legendre.leggauss(nodes)
        us, ws = [], []
        for a, b in segs:
            us.append(0.5 * (b - a) * x + 0.5 * (b + a)); ws.append(0.5 * (b - a) * w)
        self.u = np.concatenate(us); self.w = np.concatenate(ws); self.ch = np.cosh(self.u)
    def sr2(self, g, gamma, beta):
        """s_r^2(r) = r^(gamma-2b) INT_r^inf r'^(2b-gamma) g dr'  [(m/s)^2]; analytic tail beyond the grid (g -> C/r)."""
        p = 2.0 * beta - gamma
        integ = self.r ** p * g * (self.r * kpc)                   # d ln r measure
        seg = 0.5 * (integ[1:] + integ[:-1]) * self.dl
        tail = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
        C = g[-1] * self.r[-1] * kpc                                # C = g r (m^2/s^2) at the edge
        # INT_edge^inf r'^p g dr' with g = C/(r' kpc), dr' in metres = kpc*dr'(kpc): = C INT r'^(p-1) dr' = C r_edge^p/(gamma-2b)
        tail_edge = C * self.r[-1] ** p / (gamma - 2.0 * beta)
        return (tail + tail_edge) / self.r ** p
    def slos(self, R, s2, gamma, beta):
        """s_los(R) [km/s] at projected radii R [kpc], constant beta, r = R cosh u."""
        R = np.atleast_1d(np.asarray(R, float))
        lr = np.log(R)[:, None] + np.log(self.ch)[None, :]
        s = np.interp(lr, self.lr, s2)                              # clamps to the edge values (the exact asymptote at large r)
        wt = self.w[None, :] * self.ch[None, :] ** (1.0 - gamma)    # r^(1-gamma) du / R^(1-gamma)
        num = (wt * (1.0 - beta / self.ch[None, :] ** 2) * s).sum(axis=1)
        den = wt.sum(axis=1)
        return np.sqrt(num / den) / 1e3
    def den_closed(self, R, gamma):
        return (math.sqrt(math.pi) / 2 * GAMMA((gamma - 1) / 2) / GAMMA(gamma / 2)) * np.ones_like(np.atleast_1d(R))
J = Jeans(); J2 = Jeans(npts=8000, nodes=48)

# ================================================================== controls C1-C4 (closed forms)
P("\n== C1-C4 closed-form checks of the Jeans/anisotropy solver ==")
PAIRS = [(2.5, -0.5), (3.0, 0.0), (2.09, 0.5), (3.83, 0.25)]
Mpm = 1e11 * Msun; vflat = 2.0e5
Rt = np.array([1.0, 3.0, 10.0, 30.0, 100.0]); rin = np.geomspace(0.5, 1000.0, 40)
e1 = e2a = e2b = e3 = e4 = 0.0
for gm, bt in PAIRS:
    g_pt = G * Mpm / (J.r * kpc) ** 2
    s2 = J.sr2(g_pt, gm, bt); ref = G * Mpm / ((gm + 1 - 2 * bt) * rin * kpc)
    e1 = max(e1, float(np.max(np.abs(np.interp(np.log(rin), J.lr, s2) / ref - 1))))
    g_fl = vflat ** 2 / (J.r * kpc)
    s2f = J.sr2(g_fl, gm, bt)
    e2a = max(e2a, float(np.max(np.abs(np.interp(np.log(rin), J.lr, s2f) / (vflat ** 2 / (gm - 2 * bt)) - 1))))
    sl = J.slos(Rt, s2f, gm, bt) * 1e3
    cf = vflat * math.sqrt((gm - bt * (gm - 1)) / (gm * (gm - 2 * bt)))
    e2b = max(e2b, float(np.max(np.abs(sl / cf - 1))))
    # C3: point-mass LOS closed form
    Jf = lambda s, R: R ** (-s) * math.sqrt(math.pi) / 2 * GAMMA(s / 2) / GAMMA((s + 1) / 2)
    Kp = G * Mpm / ((gm + 1 - 2 * bt) * kpc)                          # s_r^2 = Kp / r[kpc]
    cf3 = np.array([math.sqrt(Kp * (Jf(gm, R) - bt * R ** 2 * Jf(gm + 2, R)) / Jf(gm - 1, R)) for R in Rt])
    e3 = max(e3, float(np.max(np.abs(J.slos(Rt, J.sr2(g_pt, gm, bt), gm, bt) * 1e3 / cf3 - 1))))
    # C4: constant s_r, beta = 0 ; denominator closed form
    if bt == 0.0:
        e4 = max(e4, float(np.max(np.abs(J.slos(Rt, np.full_like(J.r, 1e10), gm, 0.0) * 1e3 / 1e5 - 1))))
    dn = (J.w[None, :] * J.ch[None, :] ** (1.0 - gm)).sum(axis=1)
    e4 = max(e4, float(np.max(np.abs(dn / J.den_closed(Rt, gm) - 1))))
check("C1 point mass: s_r^2 = GM/((gamma+1-2beta) r) at 4 (gamma,beta)", e1 < 1e-4, f"max rel err {e1:.1e}")
check("C2 flat curve: s_r^2 = v^2/(gamma-2beta), s_los^2 = v^2 (gamma-beta(gamma-1))/(gamma(gamma-2beta))", e2a < 1e-4 and e2b < 1e-4, f"{e2a:.1e}, {e2b:.1e}")
check("C3 point-mass s_los(R) from Gamma-function closed form", e3 < 1e-4, f"max rel err {e3:.1e}")
check("C4 beta=0 constant s_r => s_los = s_r; projection denominator = Gamma closed form", e4 < 1e-6, f"max rel err {e4:.1e}")

# ================================================================== sample
P("\n== sample ==")
GCf, nall = load_gcs(); BINS = make_bins(GCf)
SEL = sorted(n for n in BINS if f"NGC{n:04d}" in AT and AT[f"NGC{n:04d}"]["qual"] >= 1)
P(f"  GC RVs parsed (h50 key) {nall}; galaxies in dispersion sample {len(BINS)}; JAM sample {len(SEL)}: " + ", ".join(f"NGC{n}" for n in SEL))
check("S1 sample = 27 galaxies / 3440 GC RVs / 19 dispersion galaxies / 16 with JAM", len(GAL) == 27 and nall == 3440 and len(BINS) == 19 and len(SEL) == 16)
CENTRALS = {4486, 4365, 4374, 5846}
GAM0 = {n: float(np.clip(-0.63 * BINS[n]["lMs"] + 9.81, 2.0, 4.0)) for n in BINS}
P("  published gamma_i: " + ", ".join(f"{n}:{GAM0[n]:.2f}" for n in SEL) + f"  | range {min(GAM0[n] for n in SEL):.2f}-{max(GAM0[n] for n in SEL):.2f}, mean {np.mean([GAM0[n] for n in SEL]):.3f}")

# ================================================================== masses -> g arrays
def build_sets(fmode="half", Jn=J):
    S = {}
    for foot in FOOTS:
        law, rule = {}, {}
        for n in SEL:
            b = BINS[n]; a_h = b["Re"] / 1.8153
            MJ, r12, q = jam_inputs(n, b["D"])
            Ml = calibrate(MJ, r12, b["Re"], foot, False, fmode)
            Mr = calibrate(MJ, r12, b["Re"], foot, True, fmode)
            law[n] = gfun_maker(Ml, a_h, A0[foot])(Jn.r)
            if Mr is not None:
                fex, Mh = rule_parts(Mr, foot); rule[n] = gfun_maker(Mr, a_h, A0[foot], fex, Mh)(Jn.r)
        S[foot] = (law, rule)
    return S
def build_sluggs(Jn=J):
    S = {}
    for foot in FOOTS:
        law, rule = {}, {}
        for n in SEL:
            b = BINS[n]; a_h = b["Re"] / 1.8153; Ms = 10 ** b["lMs"]
            law[n] = gfun_maker(Ms, a_h, A0[foot])(Jn.r)
            fex, Mh = rule_parts(Ms, foot); rule[n] = gfun_maker(Ms, a_h, A0[foot], fex, Mh)(Jn.r)
        S[foot] = (law, rule)
    return S
P("\n== calibrating masses (JAM, Hernquist-fraction variant, SLUGGS masses) ==")
SET_JAM = build_sets("half"); SET_HERN = build_sets("hern"); SET_SL = build_sluggs()
P(f"  rule roots present: canonical {len(SET_JAM['canonical'][1])}/16, alt {len(SET_JAM['alt'][1])}/16  ({time.time()-T0:.0f}s)")
SCALE = {f: 1.0 for f in FOOTS}                                  # MUTATE: 10^(-D)

def offset_gal(n, g, foot, gamma, beta, Jn=J):
    b = BINS[n]
    pred = Jn.slos(b["Rb"], Jn.sr2(g, gamma, beta), gamma, beta)
    o = np.log10(b["Sb"] * SCALE[foot] / pred)[b["out"]]
    return float(np.mean(o))
def cell(sset, foot, rule, dl, be, gam=None, Jn=J, rows=None):
    g_all = sset[foot][1 if rule else 0]
    res = {}
    for n in (rows if rows is not None else SEL):
        if n not in g_all: continue
        gm = (GAM0[n] + dl) if gam is None else gam
        res[n] = offset_gal(n, g_all[n], foot, gm, be, Jn)
    return res
def stat(res, drop=(), ddof=1):
    v = np.array([o for n, o in res.items() if n not in drop]); N = len(v)
    m = float(v.mean()); e = float(v.std(ddof=ddof) / math.sqrt(N))
    return m, e, m / e, N, float(np.sqrt(np.mean(v ** 2)))
DELTAS = [-0.4, -0.2, 0.0, 0.2, 0.4]; BETAS = [-0.5, -0.25, 0.0, 0.25, 0.5]
def box(sset, foot, rule, Jn=J, **kw):
    B = {}
    for dl in DELTAS:
        for be in BETAS:
            B[(dl, be)] = stat(cell(sset, foot, rule, dl, be, Jn=Jn), **kw)
    return B
def fmt_box(B, what="z"):
    idx = {"m": 0, "e": 1, "z": 2}[what]
    s = "  delta\\beta " + "".join(f"{b:>8.2f}" for b in BETAS) + "\n"
    for dl in DELTAS:
        s += f"  {dl:+.1f}      " + "".join(f"{B[(dl,b)][idx]:>8.3f}" for b in BETAS) + "\n"
    return s

# ---- MUTATE: D from the unmodified data
if MUTATE:
    for foot in FOOTS:
        Bm = box(SET_JAM, foot, False)
        kmin = min(Bm, key=lambda k: Bm[k][2]); D = Bm[kmin][0]
        SCALE[foot] = 10 ** (-D)
        P(f"  MUTATE {foot}: weakest law cell (delta,beta)={kmin}, z={Bm[kmin][2]:.3f}, D={D:+.5f} dex removed (bins x {SCALE[foot]:.5f})")

# ================================================================== main box
P("\n== MAIN: the 5 x 5 box (JAM-calibrated masses, N=16) ==" + ("  [MUTATE]" if MUTATE else ""))
BOX = {}
for foot in FOOTS:
    for rule in (False, True):
        BOX[(foot, rule)] = box(SET_JAM, foot, rule)
for foot in FOOTS:
    for rule in (False, True):
        nm = ("rule" if rule else "law")
        P(f"\n {nm} z, {foot}:\n" + fmt_box(BOX[(foot, rule)], "z") + f" {nm} mean offset (dex), {foot}:\n" + fmt_box(BOX[(foot, rule)], "m"))
        P(f" {nm} err (dex), {foot}:\n" + fmt_box(BOX[(foot, rule)], "e"))
def n_above(B): return sum(1 for k in B if B[k][2] > 2.0)
def n_fit(B): return sum(1 for k in B if abs(B[k][2]) < 2.0)
cnt = {}
for foot in FOOTS:
    cnt[foot] = (n_above(BOX[(foot, False)]), n_fit(BOX[(foot, True)]))
    lz = BOX[(foot, False)]; kmin = min(lz, key=lambda k: lz[k][2])
    P(f"  R3-count {foot}: law z>2 in {cnt[foot][0]}/25 cells; rule |z|<2 in {cnt[foot][1]}/25; law smallest at (delta,beta)={kmin}: {lz[kmin][0]:+.4f} +- {lz[kmin][1]:.4f} dex, z={lz[kmin][2]:.3f}")
    P(f"     law cells below 2 sigma: " + ", ".join(f"({k[0]:+.1f},{k[1]:+.2f}):{lz[k][2]:.2f}" for k in lz if lz[k][2] <= 2.0))
    rz = BOX[(foot, True)]
    P(f"     rule cells |z|>=2: " + ", ".join(f"({k[0]:+.1f},{k[1]:+.2f}):{rz[k][2]:+.2f}" for k in rz if abs(rz[k][2]) >= 2.0))
h1 = all(BOX[(f, False)][k][2] > 2 for f in FOOTS for k in BOX[(f, False)])
P(f"  H1_CFG114 (law > 2 sigma in EVERY cell, both footings): {'TRUE' if h1 else 'FALSE'} (reported only)")

# ================================================================== gates
P("\n== gates ==")
def close(a, b, tol): return abs(a - b) <= tol
# G0 baseline gamma=3, beta=0
G0 = {}
for foot in FOOTS:
    for rule in (False, True):
        G0[(foot, rule)] = stat(cell(SET_JAM, foot, rule, 0.0, 0.0, gam=3.0))
P("  G0 values: " + "; ".join(f"{f[:3]} {'rule' if r else 'law'} {v[0]:+.5f} +- {v[1]:.5f} z={v[2]:.3f} N={v[3]}" for (f, r), v in G0.items()))
ok0 = (close(G0[("canonical", False)][0], 0.0970, 0.0015) and close(G0[("canonical", False)][2], 3.99, 0.05) and
       close(G0[("canonical", True)][0], 0.0456, 0.0015) and close(G0[("canonical", True)][2], 2.58, 0.05) and
       close(G0[("alt", False)][0], 0.088, 0.0015) and close(G0[("alt", False)][2], 3.65, 0.1) and
       close(G0[("alt", True)][0], 0.047, 0.0015) and close(G0[("alt", True)][2], 2.6, 0.1))
check("G0 baseline gamma=3, beta=0 reproduces CFG55/CFG76 (law +0.0970 3.99s, rule +0.0456 2.58s; alt 3.65/2.6)", ok0)
Lc, Rc, La, Ra = BOX[("canonical", False)], BOX[("canonical", True)], BOX[("alt", False)], BOX[("alt", True)]
ok1 = (close(Lc[(0.0, 0.0)][0], 0.082, 0.0015) and close(Lc[(0.0, 0.0)][2], 3.60, 0.02) and close(La[(0.0, 0.0)][2], 3.22, 0.02) and
       close(Rc[(0.0, 0.0)][0], 0.028, 0.0015) and close(Rc[(0.0, 0.0)][2], 1.55, 0.02) and close(Ra[(0.0, 0.0)][2], 1.64, 0.02))
check("G1 published gamma_i, beta=0 (CFG111 cell): law +0.082 z 3.60/3.22, rule +0.028 z 1.55/1.64", ok1,
      f"law {Lc[(0.0,0.0)][0]:+.4f} z {Lc[(0.0,0.0)][2]:.3f}/{La[(0.0,0.0)][2]:.3f}; rule {Rc[(0.0,0.0)][0]:+.4f} z {Rc[(0.0,0.0)][2]:.3f}/{Ra[(0.0,0.0)][2]:.3f}")
T2 = {"Lc": [3.66, 3.64, 3.60, 3.53, 3.38], "La": [3.31, 3.28, 3.22, 3.12, 2.93], "Rc": [2.06, 1.84, 1.55, 1.13, 0.56], "Ra": [2.10, 1.91, 1.64, 1.26, 0.69]}
BX = {"Lc": Lc, "La": La, "Rc": Rc, "Ra": Ra}
d2 = max(abs(BX[k][(0.0, b)][2] - T2[k][i]) for k in T2 for i, b in enumerate(BETAS))
m2 = max(abs(Lc[(0.0, b)][0] - v) for b, v in zip(BETAS, [0.086, 0.084, 0.082, 0.079, 0.074]))
check("G2 beta row at published slopes (CFG113): law/rule z, both footings, and law means", d2 <= 0.02 and m2 <= 0.0015, f"max |dz| {d2:.3f}, max |d mean| {m2:.4f}")
c_lc, c_la, c_rc, c_ra = cnt["canonical"][0], cnt["alt"][0], cnt["canonical"][1], cnt["alt"][1]
check("G3 [HEADLINE] law z>2 in 23/25 canonical and 21/25 alt; rule |z|<2 in 13/25 on each footing", (c_lc, c_la, c_rc, c_ra) == (23, 21, 13, 13), f"got {c_lc}, {c_la}, {c_rc}, {c_ra}")
cc = (-0.4, 0.5)
ok4 = (close(Lc[cc][0], 0.013, 0.0015) and close(Lc[cc][1], 0.022, 0.0015) and close(Lc[cc][2], 0.59, 0.02) and close(La[cc][2], 0.08, 0.03) and close(Rc[cc][2], -2.59, 0.03))
check("G4 corner (delta -0.4, beta +0.5): law +0.013 +- 0.022 z 0.59 (alt 0.08); rule z -2.59", ok4,
      f"law {Lc[cc][0]:+.4f} +- {Lc[cc][1]:.4f} z {Lc[cc][2]:.3f}; alt z {La[cc][2]:.3f}; rule z {Rc[cc][2]:+.3f}")
T5 = {-0.4: [2.95, 2.68, 2.28, 1.66, 0.59], -0.2: [3.31, 3.17, 2.97, 2.65, 2.09], 0.0: [3.66, 3.64, 3.60, 3.53, 3.38], 0.2: [4.00, 4.09, 4.19, 4.33, 4.51], 0.4: [4.34, 4.52, 4.74, 5.06, 5.51]}
d5 = max(abs(Lc[(dl, b)][2] - T5[dl][i]) for dl in DELTAS for i, b in enumerate(BETAS))
altbelow = {k: La[k][2] for k in La if La[k][2] <= 2.0}
exp_alt = {(-0.4, 0.0): 1.86, (-0.4, 0.25): 1.20, (-0.4, 0.5): 0.08, (-0.2, 0.5): 1.61}
ok5b = set(altbelow) == set(exp_alt) and all(abs(altbelow[k] - exp_alt[k]) <= 0.03 for k in exp_alt) if set(altbelow) == set(exp_alt) else False
check("G5 canonical law z table (25 cells, +-0.02) and the four alt cells below 2 sigma", d5 <= 0.02 and ok5b, f"max |dz| canonical {d5:.3f}; alt below-2 cells {sorted(altbelow.items())}")
exp_fail = {(dl, b) for dl in (0.2, 0.4) for b in BETAS} | {(0.0, -0.5), (-0.4, 0.5)}
got_fail = {f: {k for k in BX["R" + f[0]] if abs(BX["R" + f[0]][k][2]) >= 2.0} for f in ("c", "a")}
check("G6 rule |z|>=2 exactly in the 10 steep-slope cells, (0,-0.5) and the corner, both footings", got_fail["c"] == exp_fail and got_fail["a"] == exp_fail,
      f"canonical extra {sorted(got_fail['c']-exp_fail)} missing {sorted(exp_fail-got_fail['c'])}; alt extra {sorted(got_fail['a']-exp_fail)} missing {sorted(exp_fail-got_fail['a'])}")
# C5 resolution
P("  building resolution-doubled masses (C5) ...")
SET_JAM2 = {}
for foot in FOOTS:
    law, rule = {}, {}
    for n in SEL:
        b = BINS[n]; a_h = b["Re"] / 1.8153; MJ, r12, q = jam_inputs(n, b["D"])
        Ml = calibrate(MJ, r12, b["Re"], foot, False); Mr = calibrate(MJ, r12, b["Re"], foot, True)
        law[n] = gfun_maker(Ml, a_h, A0[foot])(J2.r)
        if Mr is not None:
            fex, Mh = rule_parts(Mr, foot); rule[n] = gfun_maker(Mr, a_h, A0[foot], fex, Mh)(J2.r)
    SET_JAM2[foot] = (law, rule)
dmax = 0.0
for foot in FOOTS:
    for rule in (False, True):
        B2 = box(SET_JAM2, foot, rule, Jn=J2)
        dmax = max(dmax, max(abs(B2[k][0] - BOX[(foot, rule)][k][0]) for k in B2))
check("C5 doubling the radial grid (8000) and GL nodes (48) moves every box mean by < 1e-5 dex", dmax < 1e-5, f"max {dmax:.1e}")
check("C6 (0,0) cell equals G1's numbers and the beta row at published slopes is monotone", ok1 and all(BX['Lc'][(0.0, BETAS[i])][2] > BX['Lc'][(0.0, BETAS[i+1])][2] for i in range(4)))

# ================================================================== reported rows (skipped in MUTATE except R1/R2)
def report_variants():
    P("\n== R2 corner variants ==")
    for foot in FOOTS:
        # SLUGGS population masses
        Bs_l = box(SET_SL, foot, False); Bs_r = box(SET_SL, foot, True)
        Bh_l = box(SET_HERN, foot, False); Bh_r = box(SET_HERN, foot, True)
        cn = {n for n in SEL if n in CENTRALS}
        rows12 = [n for n in SEL if n not in CENTRALS]
        nc_l = stat(cell(SET_JAM, foot, False, -0.4, 0.5, rows=rows12)); nc_r = stat(cell(SET_JAM, foot, True, -0.4, 0.5, rows=rows12))
        d0 = stat(cell(SET_JAM, foot, False, -0.4, 0.5), ddof=0)
        P(f"  {foot}: corner law, JAM masses z={BOX[(foot,False)][cc][2]:+.2f}; SLUGGS pop masses law z={Bs_l[cc][2]:+.2f} rule z={Bs_r[cc][2]:+.2f} (CFG114 README: -0.24 canonical law); "
          f"no centrals (N={nc_l[3]}) law z={nc_l[2]:+.2f} rule z={nc_r[2]:+.2f} (README -0.58); ddof=0 law z={d0[2]:+.2f}; Hernquist-fraction calibration law z={Bh_l[cc][2]:+.2f} rule z={Bh_r[cc][2]:+.2f}")
        P(f"     cells law z>2: SLUGGS masses {n_above(Bs_l)}/25, Hernquist-fraction {n_above(Bh_l)}/25 ; rule |z|<2: SLUGGS masses {n_fit(Bs_r)}/25, Hernquist {n_fit(Bh_r)}/25 ; published-cell law z: SLUGGS masses {Bs_l[(0.0,0.0)][2]:.2f}, Hernquist {Bh_l[(0.0,0.0)][2]:.2f}")
    return

def bisect(f, lo, hi, it=40):
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0: return None
    for _ in range(it):
        mid = 0.5 * (lo + hi); fm = f(mid)
        if fm * flo > 0: lo, flo = mid, fm
        else: hi = mid
    return 0.5 * (lo + hi)
def report_nulling():
    P("\n== R3 nulling loci beyond the box (law and rule, JAM masses) ==")
    gmin = min(GAM0[n] for n in SEL)
    for foot in FOOTS:
        for rule in (False, True):
            nm = "rule" if rule else "law"
            rows = SEL if not rule else [n for n in SEL if n in SET_JAM[foot][1]]
            mean = lambda dl, be: float(np.mean(list(cell(SET_JAM, foot, rule, dl, be, rows=rows).values())))
            s = f"  {foot} {nm}: delta* nulling the mean at beta = "
            parts = []
            for be in BETAS:
                lo = max(-1.5, 2 * be + 0.08 - gmin)
                d = bisect(lambda x: mean(x, be), lo, 1.5)
                parts.append(f"{be:+.2f}: " + (f"{d:+.3f}" if d is not None else "none in range"))
            P(s + "; ".join(parts))
            parts = []
            for dl in DELTAS:
                b = bisect(lambda x: mean(dl, x), -0.9, 0.995)
                parts.append(f"{dl:+.1f}: " + (f"{b:+.3f}" if b is not None else ">0.995 or <-0.9 (none)"))
            P(f"  {foot} {nm}: beta* nulling the mean at delta = " + "; ".join(parts))

def sigma_gamma(lM, rho, sa=0.17, sb=1.94): return math.sqrt(sb ** 2 + lM ** 2 * sa ** 2 + 2 * lM * rho * sa * sb)
def report_relation():
    P("\n== R4 the slope relation's uncertainty (a,b) = (-0.63+-0.17, 9.81+-1.94) ==")
    lMs = np.array([BINS[n]["lMs"] for n in SEL]); mbar = float(lMs.mean())
    for rho in (0.0, -0.9, -0.99):
        sg = [sigma_gamma(x, rho) for x in lMs]
        P(f"  rho={rho:+.2f}: 1-sigma of gamma at the 16 masses: {min(sg):.2f}-{max(sg):.2f}; coherent (mean-slope) 1-sigma = sigma_gamma(mean lM={mbar:.2f}) = {sigma_gamma(mbar, rho):.3f}; box half-width 0.4 = {0.4/sigma_gamma(mbar, rho):.1f} sigma")
    rng = np.random.default_rng(106); NDR = 1000
    for rho in (0.0, -0.9, -0.99):
        cov = [[0.17 ** 2, rho * 0.17 * 1.94], [rho * 0.17 * 1.94, 1.94 ** 2]]
        draws = rng.multivariate_normal([-0.63, 9.81], cov, NDR)
        for foot in FOOTS:
            zs = {0.0: [], 0.5: []}; mm = []
            for a_, b_ in draws:
                gam = {n: float(np.clip(a_ * BINS[n]["lMs"] + b_, 2.0, 4.0)) for n in SEL}
                for be in (0.0, 0.5):
                    res = {n: offset_gal(n, SET_JAM[foot][0][n], foot, gam[n], be) for n in SEL}
                    zs[be].append(stat(res)[2])
                mm.append(np.mean([gam[n] - GAM0[n] for n in SEL]))
            for be in (0.0, 0.5):
                z = np.array(zs[be])
                P(f"  rho={rho:+.2f} {foot} beta={be:+.1f}: law z median {np.median(z):.2f} [16-84%: {np.percentile(z,16):.2f}, {np.percentile(z,84):.2f}]; fraction of {NDR} (a,b) draws with z<2: {np.mean(z<2):.3f}; mean-slope shift rms {np.std(mm):.3f}")

def report_incoherent():
    P("\n== R5 independent per-galaxy shifts and betas (law, JAM masses; 500 draws) ==")
    rng = np.random.default_rng(1060); ND = 500
    settings = [("delta_i~N(0,0.2), beta_i~U(-.5,.5)", lambda: rng.normal(0, 0.2, 16), lambda: rng.uniform(-0.5, 0.5, 16)),
                ("delta_i~N(0,0.4), beta_i~U(-.5,.5)", lambda: rng.normal(0, 0.4, 16), lambda: rng.uniform(-0.5, 0.5, 16)),
                ("delta_i~U(-.4,.4), beta_i~U(-.5,.5)", lambda: rng.uniform(-0.4, 0.4, 16), lambda: rng.uniform(-0.5, 0.5, 16)),
                ("delta_i~N(0,0.4), beta_i=+0.5", lambda: rng.normal(0, 0.4, 16), lambda: np.full(16, 0.5)),
                ("delta_i~N(-0.4,0.2), beta_i=+0.5 (a biased draw around the corner)", lambda: rng.normal(-0.4, 0.2, 16), lambda: np.full(16, 0.5))]
    for foot in FOOTS:
        for name, fd, fb in settings:
            zs = []
            for _ in range(ND):
                dd, bb = fd(), fb()
                res = {n: offset_gal(n, SET_JAM[foot][0][n], foot, float(np.clip(GAM0[n] + dd[i], 2.05, 4.0)), float(bb[i])) for i, n in enumerate(SEL)}
                zs.append(stat(res)[2])
            z = np.array(zs)
            P(f"  {foot:9s} {name:66s}: law z median {np.median(z):.2f} [5-95%: {np.percentile(z,5):.2f}, {np.percentile(z,95):.2f}]; fraction with z<2: {np.mean(z<2):.3f}")

def report_galaxies():
    P("\n== R6 per-galaxy (law, JAM masses) ==")
    for foot in FOOTS:
        cells = {"published": (0.0, 0.0), "corner(-0.4,+0.5)": (-0.4, 0.5), "(-0.4,-0.5)": (-0.4, -0.5), "(+0.4,+0.5)": (0.4, 0.5), "(+0.4,-0.5)": (0.4, -0.5)}
        for nm, (dl, be) in cells.items():
            res = cell(SET_JAM, foot, False, dl, be); v = np.array(list(res.values()))
            P(f"  {foot:9s} {nm:18s}: N(o>+0.05)={int((v>0.05).sum())}  N(|o|<=0.05)={int((np.abs(v)<=0.05).sum())}  N(o<-0.05)={int((v<-0.05).sum())}  mean {v.mean():+.3f}  rms about zero {np.sqrt(np.mean(v**2)):.3f}  sd {v.std(ddof=1):.3f}")
        cube = {n: {k: 0.0 for k in [(d, b) for d in DELTAS for b in BETAS]} for n in SEL}
        for dl in DELTAS:
            for be in BETAS:
                res = cell(SET_JAM, foot, False, dl, be)
                for n in SEL: cube[n][(dl, be)] = res[n]
        mins = {n: min(cube[n].values()) for n in SEL}
        P(f"  {foot}: galaxies whose minimum offset over the box is <= 0 (can be nulled in the box): {sum(1 for n in SEL if mins[n] <= 0)}/16; not nullable: " +
          ", ".join(f"NGC{n}({mins[n]:+.3f})" for n in SEL if mins[n] > 0))
        for be in (0.0, 0.5):
            nul = [n for n in SEL if min(cube[n][(d, be)] for d in DELTAS) <= 0]
            P(f"     at beta={be:+.1f} the shift range [-0.4,+0.4] nulls {len(nul)}/16 galaxies")
        P(f"     per-galaxy offset at the corner (-0.4,+0.5): " + ", ".join(f"{n}:{cube[n][(-0.4,0.5)]:+.3f}" for n in SEL))
        P(f"     per-galaxy offset at published (0,0):          " + ", ".join(f"{n}:{cube[n][(0.0,0.0)]:+.3f}" for n in SEL))
        # galaxies whose own null needs a slope below the published range or beta beyond the box
        need = []
        for n in SEL:
            f_ = lambda d: offset_gal(n, SET_JAM[foot][0][n], foot, GAM0[n] + d, 0.5)
            lo = max(-1.5, 2 * 0.5 + 0.08 - GAM0[n]); d0 = bisect(f_, lo, 1.5)
            need.append((n, d0))
        P(f"     delta_i needed to null galaxy i alone at beta=+0.5: " + ", ".join(f"{n}:" + (f"{d:+.2f}" if d is not None else "none") for n, d in need) + f"  -> within [-0.4,0.4]: {sum(1 for n,d in need if d is not None and -0.4<=d<=0.4)}/16")
        need0 = []
        for n in SEL:
            f_ = lambda d: offset_gal(n, SET_JAM[foot][0][n], foot, GAM0[n] + d, 0.0)
            lo = max(-1.5, 0.08 - GAM0[n]); need0.append((n, bisect(f_, lo, 1.5)))
        P(f"     delta_i needed to null galaxy i alone at beta=0: " + ", ".join(f"{n}:" + (f"{d:+.2f}" if d is not None else "none") for n, d in need0) + f"  -> within [-0.4,0.4]: {sum(1 for n,d in need0 if d is not None and -0.4<=d<=0.4)}/16")

def report_params():
    P("\n== R7 parameter counting ==")
    nb = sum(int(BINS[n]["out"].sum()) for n in SEL)
    P(f"  data: 16 galaxy offsets ({nb} outer bins); free shifts tuned in the box: 2 (delta,beta), both coherent; the law itself has no free parameter beyond fixed a0; the box has 25 cells, 2 of which (canonical) are < 2 sigma")
    for foot in FOOTS:
        L = BOX[(foot, False)]; kmin = min(L, key=lambda k: L[k][2])
        P(f"  {foot}: best law cell {kmin} z={L[kmin][2]:.2f}; published-cell z^2={L[(0.0,0.0)][2]**2:.1f}, best-cell z^2={L[kmin][2]**2:.2f}, improvement {L[(0.0,0.0)][2]**2-L[kmin][2]**2:.1f} for 2 tuned parameters at the box boundary (a corner: {kmin[0] in (-0.4,0.4) and kmin[1] in (-0.5,0.5)})")
        R = BOX[(foot, True)]
        P(f"     rule at that cell z={R[kmin][2]:+.2f}; rule best-fit z^2 cell {min(R, key=lambda k: abs(R[k][2]))} z={R[min(R, key=lambda k: abs(R[k][2]))][2]:+.2f}")
        inside = [k for k in L if abs(L[k][2]) < 2.0]
        P(f"     cells where the LAW fits: {inside}; cells where BOTH law and rule fit at 2 sigma: {[k for k in inside if abs(R[k][2]) < 2.0]}")

# ---- R8 solver cross-check against the CFG76 copy (verbatim, used only here)
RG76 = np.geomspace(0.02, 3e4, 1200); LRG76 = np.log(RG76)
def cfg76_sigma_r2(gfun, gamma, beta=0.0):
    g = gfun(RG76); w = RG76 ** (2 * beta - gamma)
    integ = w * g * (RG76 * kpc)
    tail = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(LRG76))[::-1])[::-1], [0.0]])
    return tail / RG76 ** (2 * beta - gamma)
def cfg76_sigma_los(R, s2, gamma, beta=0.0, umax=6.0):
    u = np.linspace(0.0, umax, 500); ch = np.cosh(u)
    r = np.outer(np.atleast_1d(R), ch)
    s = np.exp(np.interp(np.log(r), LRG76, np.log(np.maximum(s2, 1e-6))))
    rho = r ** (-gamma)
    num = np.trapz((1 - beta / ch ** 2) * rho * s * r, u, axis=1)
    den = np.trapz(rho * r, u, axis=1)
    return np.sqrt(num / den) / 1e3
def report_cross():
    P("\n== R8 cross-check of my solver against a verbatim copy of CFG76's (canonical, JAM law masses) ==")
    foot = "canonical"
    for nm, (dl, be) in {"published (0,0)": (0.0, 0.0), "corner (-0.4,+0.5)": (-0.4, 0.5), "(-0.4,-0.5)": (-0.4, -0.5)}.items():
        mx = 0.0
        for n in SEL:
            b = BINS[n]; a_h = b["Re"] / 1.8153; MJ, r12, q = jam_inputs(n, b["D"])
            Ml = calibrate(MJ, r12, b["Re"], foot, False); gf = gfun_maker(Ml, a_h, A0[foot])
            gm = GAM0[n] + dl
            mine = J.slos(b["Rb"], J.sr2(gf(J.r), gm, be), gm, be)
            old = cfg76_sigma_los(b["Rb"], cfg76_sigma_r2(gf, gm, be), gm, be)
            mx = max(mx, float(np.max(np.abs(mine / old - 1))))
        P(f"  {nm}: max |mine/CFG76-solver - 1| over all bins of 16 galaxies = {mx:.2e}")

if not MUTATE:
    report_variants(); report_nulling(); report_relation(); report_incoherent(); report_galaxies(); report_params(); report_cross()
else:
    report_variants()
    P("  (MUTATE: R3-R8 skipped)")
    P('  MUTATE failing checks: ' + '; '.join(f for f in FAILS if f[:2] in ('G3','G4','G5')))

json.dump({"mutate": MUTATE, "box": {f"{f}|{'rule' if r else 'law'}": {f"{k[0]:+.2f},{k[1]:+.2f}": list(v) for k, v in B.items()} for (f, r), B in BOX.items()},
           "counts": {f: {"law_gt2": cnt[f][0], "rule_fit": cnt[f][1]} for f in FOOTS}},
          open(os.path.join(HERE, "cfg106_MUTATE_results.json" if MUTATE else "cfg106_results.json"), "w"), indent=1)
P(f"\nelapsed {time.time()-T0:.0f}s")
P(f"FAILED CHECKS ({len(FAILS)}): " + "; ".join(FAILS))
open(os.path.join(HERE, "cfg106_MUTATE.out" if MUTATE else "cfg106_main.out"), "w").write("\n".join(out_lines) + "\n")
sys.exit(1 if FAILS else 0)
