#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG261 -- the ABSOLUTE implied-a0 level of the KiDS-1000 lensing RAR in lens-redshift thirds (z ~ 0.2 and 0.4), M* calibration named as the dominant systematic.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG261_kids_absolute_a0_zthirds/FROZEN_CRITERIA.md (ec413346f).
  data     cfg110_perlens.npz (WG, WW, NN per lens and g_bar bin), lr_lenses.npz, the 50 June patches; K1 = bins 8-14.
  rows     CFG255's per-class thirds (T-*), a mass-matched window 10.3 <= log M* < 10.9 (MM-*), two joint one-s rows (J-*).
  model    CFG61/CFG255's L law stack with EVERY profile rebuilt at a0 * s (turnaround radius and truncation included); s-grid log10 s = -1..+1.25 (spline);
           "true baryon mass" shifts (bands, scenarios) multiply M_gal in the profile and the point term only; the g_bar binning keeps the nominal M_gal.
  fit      inverse-variance least squares in s on K1 (jackknife variances), patch bootstrap B = 10,000, jackknife SD beside it.
  STAGE=A  the blind pre-flight: controls, levers, mocks, precision, calibration dominance, decisions; no row's level, amplitude or difference is printed.
  STAGE=B  the measurement (run once, after stage A and this script are committed); STAGE=B MUTATE=1 plants s = 2 (reactivity); STAGE=B SELFTEST=1 fabricates data.
Run: STAGE=A python3 .../cfg261_kids_abs.py ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, io, json, math, time, zlib, csv, hashlib, contextlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.stats import chi2 as CHI2

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
STAGE = os.environ.get("STAGE", "").strip().upper()
MUTATE = os.environ.get("MUTATE", "0") == "1"
SELFTEST = os.environ.get("SELFTEST", "0") == "1"
assert STAGE in ("A", "B"), "set STAGE=A or STAGE=B"
assert not ((MUTATE or SELFTEST) and STAGE == "A") and not (MUTATE and SELFTEST), "MUTATE / SELFTEST apply to stage B, one at a time"
SFX = f"_stage{STAGE}" + ("_MUTATE1" if MUTATE else "") + ("_SELFTEST" if SELFTEST else "") + ("_noiseless" if (SELFTEST and os.environ.get("SELFTEST_NOISE", "1") == "0") else "")
S_TRUE_SELF = float(os.environ.get("SELFTEST_S", "1.7"))
SELF_NOISE = float(os.environ.get("SELFTEST_NOISE", "1"))            # SELFTEST only: 0 = noiseless fabricated data (a weighting-bias check)
CACHE = os.environ.get("CFG261_CACHE", os.path.join(HERE, "_cache"))
os.makedirs(CACHE, exist_ok=True)
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: a planted s = 2 (every lens's WG times its own cell's m_k(2)/m_k(1)) ***" if MUTATE else "")
  + (f"  *** SELFTEST: FABRICATED data at s_true = {S_TRUE_SELF}; no real ESD is used; debugging only ***" if SELFTEST else ""))

# ------------------------------------------------------------------ data
LR = os.path.join(REPO, "real_research", "data", "lensing_rar")
PL = np.load(os.path.join(LR, "cfg110_perlens.npz"))
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
JK = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
KG = 1.989e30 / (3.0857e16) ** 2
WG0, WW, NNL = PL["WG"].astype(float), PL["WW"].astype(float), PL["NN"].astype(float)
typ, Mgal, zlen, lM = LN["typ"], LN["Mgal"], LN["z"], LN["logM"]
patch = JK["patch"]
NPAT, K1 = 50, [8, 9, 10, 11, 12, 13, 14]
NLENS = len(typ)
H12 = lambda p: (NPAT - p - 2) / (NPAT - 1)          # Hartlap factor for a p-bin covariance from 50 patches


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 22), b""): h.update(ch)
    return h.hexdigest()[:16]


P("data sha256 prefixes: " + ", ".join(f"{n} {sha(os.path.join(LR, n))}" for n in ("cfg110_perlens.npz", "lr_lenses.npz", "lr_esd_jackknife.npz")))

# ------------------------------------------------------------------ rows
Q1 = {c: float(np.quantile(zlen[typ == c], 1 / 3)) for c in (0, 1)}
Q2 = {c: float(np.quantile(zlen[typ == c], 2 / 3)) for c in (0, 1)}
WIN = (lM >= 10.3) & (lM < 10.9)
QW1 = {c: float(np.quantile(zlen[(typ == c) & WIN], 1 / 3)) for c in (0, 1)}
QW2 = {c: float(np.quantile(zlen[(typ == c) & WIN], 2 / 3)) for c in (0, 1)}
CN = {0: "late", 1: "early"}
ROWS = {}
for c in (0, 1):
    ROWS[f"T-{CN[c]}-LO"] = (typ == c) & (zlen < Q1[c])
    ROWS[f"T-{CN[c]}-HI"] = (typ == c) & (zlen >= Q2[c])
for c in (0, 1):
    ROWS[f"MM-{CN[c]}-LO"] = (typ == c) & WIN & (zlen < QW1[c])
    ROWS[f"MM-{CN[c]}-HI"] = (typ == c) & WIN & (zlen >= QW2[c])
JOINT = {"J-LO": ("T-late-LO", "T-early-LO"), "J-HI": ("T-late-HI", "T-early-HI")}
SINGLE = list(ROWS)
ALLROWS = SINGLE + list(JOINT)
CLASS_OF = {r: (0 if "late" in r else 1) for r in SINGLE}

# ------------------------------------------------------------------ the committed machinery, read-only (CFG61 prefix, as CFG255)


def lane_prefix(fname, marker):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(CFG, fname)).read()
    g = {"__file__": os.path.join(CFG, fname), "__name__": "lane_" + fname}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:src.index(marker)], fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


g61 = lane_prefix("CFG61_kids_colour_split.py", "\nRES = {}\n")
C = g61["C"]
fcold, project, trapz = g61["fcold"], g61["project"], g61["trapz"]
LMG, ZG, RG, rgrid, EDGES, SUB = g61["LMG"], g61["ZG"], g61["RG"], g61["rgrid"], g61["EDGES"], g61["SUB"]
G_SI, MSUN, MPC = g61["G_SI"], g61["MSUN"], g61["MPC"]
im, iz, Mg61 = g61["im"], g61["iz"], g61["Mg"]
assert np.array_equal(Mg61, Mgal) and np.array_equal(g61["typ"], typ) and np.array_equal(g61["zl"], zlen)
A0C, A0A = C.A0["canonical"], C.A0["alt"]
nA, nB, nR = len(LMG), len(ZG), len(RG)
LRG = np.log(RG)
MTAB = 10 ** LMG * (1 + fcold(LMG))
LGE = [np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), SUB + 1) for k in range(15)]
GS = np.array([np.exp(0.5 * (l[1:] + l[:-1])) for l in LGE])                       # (15, SUB)
RJ = np.sqrt(G_SI * MTAB[None, None, :] * MSUN / GS[:, :, None]) / MPC              # (15, SUB, nA) pair radii [Mpc] from the NOMINAL masses
LRJ = np.log(RJ)
IDX = np.clip(np.searchsorted(LRG, LRJ, side="right") - 1, 0, nR - 2)
FRAC = (np.clip(LRJ, LRG[0], LRG[-1]) - LRG[IDX]) / (LRG[IDX + 1] - LRG[IDX])
WJ = 1.0 / GS
AR, BR = np.arange(nA)[:, None], np.arange(nB)[None, :]


def project_vec(r, Md, Rs):
    """CFG61's projector, vectorised over the projected radii (same x-grid, same trapezoid)."""
    dMdr = np.gradient(Md, r); lr = np.log(r)
    X = np.sqrt(np.maximum(r[-1] ** 2 - Rs ** 2, 0.0))
    a = 1e-5 * Rs
    t = np.linspace(0.0, 1.0, 1200)
    x = np.concatenate([np.zeros((len(Rs), 1)), a[:, None] * (X / a)[:, None] ** t[None, :]], axis=1)
    rr = np.sqrt(x * x + Rs[:, None] ** 2)
    dm = np.interp(np.log(rr).ravel(), lr, dMdr, right=0.0).reshape(rr.shape)
    Sig = trapz(dm / rr ** 2, x, axis=1) / (2 * math.pi)
    Mcyl = np.interp(np.log(Rs), lr, Md) + trapz(dm * (1 - x / rr) * (x / rr), x, axis=1)
    return Mcyl / (math.pi * Rs ** 2) - Sig


def cell_values(DS, MB):
    """bin-averaged model ESD [Msun/pc^2] of every (mass node, z node) cell in all 15 g_bar bins."""
    out = np.zeros((nA, nB, 15))
    for k in range(15):
        num = 0.0; den = 0.0
        for j in range(SUB):
            i0 = IDX[k, j][:, None]; f = FRAC[k, j][:, None]
            ds = DS[AR, BR, i0] * (1 - f) + DS[AR, BR, i0 + 1] * f + MB / (math.pi * RJ[k, j][:, None] ** 2)
            num = num + WJ[k, j] * ds; den = den + WJ[k, j]
        out[:, :, k] = num / den / 1e12
    return out


def build_cells(ls, shift=0.0, kern="mono", tfac=0.40, gasf=1.0, eps=0.0, a0=A0C):
    """cell tables of the L law with every profile at a0 * 10**ls; the TRUE baryon mass of a lens is M*(1 + gasf f_cold) 10**(shift + eps (lm - 10.5))."""
    kf = C.nu_mono if kern == "mono" else C.nu_p2
    s = 10.0 ** ls
    DS = np.zeros((nA, nB, nR)); MB = np.zeros((nA, nB))
    for a, lm in enumerate(LMG):
        Mb = 10 ** lm * (1 + gasf * fcold(lm)) * 10 ** (shift + eps * (lm - 10.5))
        for b, z in enumerate(ZG):
            a0s = a0 * s
            rta = float(C.r_ta_law(Mb, a0s, kf, 1.0 / (1.0 + z)))
            rc = np.minimum(rgrid, tfac * rta)
            ML = np.asarray(C.M_law(Mb, rc, a0s, kf), float)
            DS[a, b] = project_vec(rgrid, ML - Mb, RG)
            MB[a, b] = Mb
    return cell_values(DS, MB)


def cells(ls, **kw):
    key = "_".join([f"ls{ls:+.4f}"] + [f"{k}{v:+.5f}" if isinstance(v, float) else f"{k}{v}" for k, v in sorted(kw.items())]) + ".npy"
    p = os.path.join(CACHE, key)
    if os.path.exists(p):
        return np.load(p)
    out = build_cells(ls, **kw)
    np.save(p, out)
    return out


LSN = np.arange(-1.0, 1.25 + 1e-9, 0.25)                      # the s-grid nodes (log10 s)
LSF = np.linspace(-1.0, 1.25, 2251)                           # the solver grid
BASE = dict(shift=0.0, kern="mono", tfac=0.40, gasf=1.0, eps=0.0)
SETS = {"base": BASE,
        "b-30": dict(BASE, shift=-0.30), "b-15": dict(BASE, shift=-0.15), "b+15": dict(BASE, shift=+0.15), "b+30": dict(BASE, shift=+0.30),
        "hot0.5": dict(BASE, shift=math.log10(1.5)), "hot1.0": dict(BASE, shift=math.log10(2.0)),
        "dz0.02": dict(BASE, shift=0.02), "dz0.05": dict(BASE, shift=0.05),
        "kernP2": dict(BASE, kern="p2"), "tf0.20": dict(BASE, tfac=0.20), "tf0.80": dict(BASE, tfac=0.80),
        "gf0.50": dict(BASE, gasf=0.5), "gf1.50": dict(BASE, gasf=1.5), "epP": dict(BASE, eps=+0.10), "epM": dict(BASE, eps=-0.10)}
_TCACHE = {}


def tables(name):
    if name not in _TCACHE:
        _TCACHE[name] = np.array([cells(float(l), **SETS[name]) for l in LSN])        # (10, nA, nB, 15)
    return _TCACHE[name]


def cellw(mask, mode="Mg"):
    if mode == "Mg":
        w = np.zeros((nA, nB)); np.add.at(w, (im[mask], iz[mask]), Mgal[mask]); return w
    w = np.zeros((nA, nB, 15))
    for k in range(15): np.add.at(w[:, :, k], (im[mask], iz[mask]), WW[mask][:, k])
    return w


def nodes_for(T, w):
    if w.ndim == 2:
        return np.einsum("sabk,ab->sk", T, w) / w.sum()
    return np.einsum("sabk,abk->sk", T, w) / w.sum(axis=(0, 1))


class Model:
    """a row's K1 model on the s-nodes: cubic spline in (log s, log m_k)."""

    def __init__(self, Mnodes, ksel=None):
        cols = K1 if ksel is None else ksel
        self.spl = CubicSpline(LSN, np.log10(Mnodes[:, cols]), axis=0)
        self.fine = 10 ** self.spl(LSF)

    def at(self, ls):
        return 10 ** self.spl(ls)

    def dlog(self, ls, h=1e-4):
        return (np.log10(self.at(ls + h)) - np.log10(self.at(ls - h))) / (2 * h)


def solve_many(d, Wm, mf, chunk=500):
    """argmin over the fine grid of (d - m)' Wm (d - m) with parabolic refinement; returns log10 s and the unbounded flag."""
    WM = mf @ Wm
    A = np.einsum("gp,gp->g", WM, mf)
    G = len(LSF); step = LSF[1] - LSF[0]
    out = np.empty(len(d)); unb = np.zeros(len(d), bool)
    for i0 in range(0, len(d), chunk):
        dd = d[i0:i0 + chunk]
        chi = A[None, :] - 2.0 * (dd @ WM.T)
        g = chi.argmin(1)
        r = np.arange(len(dd))
        gm, gp = np.clip(g - 1, 0, G - 1), np.clip(g + 1, 0, G - 1)
        y0, y1, y2 = chi[r, gm], chi[r, g], chi[r, gp]
        den = y0 - 2 * y1 + y2
        off = np.where((den > 0) & (g > 0) & (g < G - 1), 0.5 * (y0 - y2) / np.where(den > 0, den, 1.0), 0.0)
        out[i0:i0 + len(dd)] = LSF[g] + off * step
        unb[i0:i0 + len(dd)] = (g == 0) | (g == G - 1)
    return out, unb


def solve1(d, Wm, mf):
    o, u = solve_many(np.asarray(d, float)[None, :], Wm, mf)
    return float(o[0]), bool(u[0])


# ------------------------------------------------------------------ the data side
def esd_sums(mask, wg, cols=K1):
    pa = patch[mask]
    Sg = np.stack([np.bincount(pa, weights=wg[mask][:, k], minlength=NPAT) for k in cols], 1)
    Sw = np.stack([np.bincount(pa, weights=WW[mask][:, k], minlength=NPAT) for k in cols], 1)
    Sn = np.stack([np.bincount(pa, weights=NNL[mask][:, k], minlength=NPAT) for k in cols], 1)
    return Sg, Sw, Sn


class RowData:
    def __init__(self, mask, wg):
        self.mask = mask
        self.Sg, self.Sw, self.Sn = esd_sums(mask, wg)
        tg, tw = self.Sg.sum(0), self.Sw.sum(0)
        self.d = tg / tw / KG
        self.loo = (tg[None] - self.Sg) / (tw[None] - self.Sw) / KG
        Rr = self.loo - self.loo.mean(0)
        self.cov = (NPAT - 1) / NPAT * (Rr.T @ Rr)
        self.sig = np.sqrt(np.diag(self.cov))
        self.n = int(mask.sum()); self.zmed = float(np.median(zlen[mask]))
        self.nn = self.Sn.sum(0)
        self.cw = cellw(mask)

    def model(self, setname="base", weights="Mg", ksel=None):
        T = tables(setname)
        w = self.cw if weights == "Mg" else cellw(self.mask, "WW")
        return Model(nodes_for(T, w), ksel)


def diagW(sig): return np.diag(1.0 / sig ** 2)


def boot_idx(label, B):
    rng = np.random.default_rng(zlib.crc32(label.encode()) % 100000)
    return rng.multinomial(NPAT, np.full(NPAT, 1.0 / NPAT), size=B).astype(float)


def interval(ls_b, unb_b):
    lo68, hi68 = np.percentile(ls_b, [16, 84]); lo95, hi95 = np.percentile(ls_b, [2.5, 97.5])
    return dict(lo68=float(lo68), hi68=float(hi68), lo95=float(lo95), hi95=float(hi95), sd=float(ls_b.std()), unb_frac=float(unb_b.mean()))


def jack_sd(vals):
    v = np.asarray(vals); return float(np.sqrt((NPAT - 1) / NPAT * np.sum((v - v.mean()) ** 2)))


# ------------------------------------------------------------------ the data actually used (real / MUTATE / SELFTEST)
def cell_per_lens(Mnodes_tables, ls):
    spl = CubicSpline(LSN, np.log10(Mnodes_tables), axis=0)          # (nA,nB,15) at ls
    return 10 ** spl(ls)


WGd = WG0
if MUTATE:
    T0b = tables("base")
    m1, m2 = cell_per_lens(T0b, 0.0), cell_per_lens(T0b, math.log10(2.0))
    fac = (m2 / m1)[im, iz, :]                                       # (NLENS, 15): each lens's own cell
    WGd = WG0 * fac
    P(f"MUTATE: WG times the planted factor m_k(2)/m_k(1) per lens cell (K1 median factor {np.median(fac[:, K1]):.3f})")
if SELFTEST:
    T0b = tables("base")
    mt = cell_per_lens(T0b, math.log10(S_TRUE_SELF))[im, iz, :]
    rng = np.random.default_rng(2610)
    WGd = WW * KG * mt
    for c in (0, 1):
        mk = typ == c
        RRc = RowData(mk, WG0)                    # only its jackknife sigma and weight sums are used (nothing of the real signal is printed or kept)
        tau = RRc.sig / (np.sqrt((RRc.Sw ** 2).sum(0)) / RRc.Sw.sum(0))         # per-bin tau so that Var(d) = sigma^2 at the class level
        xi = SELF_NOISE * rng.standard_normal((NPAT, len(K1)))
        for ki, k in enumerate(K1):
            WGd[mk, k] = WGd[mk, k] + KG * tau[ki] * WW[mk, k] * xi[patch[mk], ki]
    P(f"SELFTEST: fabricated WG = WW x KG x m_cell(s_true = {S_TRUE_SELF}) plus per-(patch, bin) noise at the class jackknife variance (the real jackknife variances are used; no real ESD is)")

# the row data objects (class-level sigmas for the fabricated noise were computed from the REAL sums above only in SELFTEST)
RD = {r: RowData(ROWS[r], WGd) for r in SINGLE}
JD = {}
for jn, (ra, rb) in JOINT.items():
    class JRow: pass
    j = JRow()
    j.Sg = np.hstack([RD[ra].Sg, RD[rb].Sg]); j.Sw = np.hstack([RD[ra].Sw, RD[rb].Sw]); j.Sn = np.hstack([RD[ra].Sn, RD[rb].Sn])
    tg, tw = j.Sg.sum(0), j.Sw.sum(0)
    j.d = tg / tw / KG; j.loo = (tg[None] - j.Sg) / (tw[None] - j.Sw) / KG
    Rr = j.loo - j.loo.mean(0); j.cov = (NPAT - 1) / NPAT * (Rr.T @ Rr); j.sig = np.sqrt(np.diag(j.cov))
    j.n = RD[ra].n + RD[rb].n; j.zmed = float(np.median(zlen[ROWS[ra] | ROWS[rb]])); j.nn = j.Sn.sum(0); j.parts = (ra, rb)
    JD[jn] = j


def jmodel(j, setname="base", weights="Mg", ksel=None):
    ma = RD[j.parts[0]].model(setname, weights, ksel); mb = RD[j.parts[1]].model(setname, weights, ksel)
    class JM: pass
    jm = JM(); jm.fine = np.hstack([ma.fine, mb.fine])
    jm.at = lambda ls: np.concatenate([ma.at(ls), mb.at(ls)])
    jm.dlog = lambda ls, h=1e-4: np.concatenate([ma.dlog(ls, h), mb.dlog(ls, h)])
    return jm


def get(r):
    return JD[r] if r in JD else RD[r]


def model_of(r, *a, **k):
    return jmodel(JD[r], *a, **k) if r in JD else RD[r].model(*a, **k)


P(f"\nrows: " + "; ".join(f"{r} N={get(r).n} z_med={get(r).zmed:.3f}" for r in ALLROWS))
P(f"  thirds z-quantiles (class late/early): Q1 {Q1[0]:.3f}/{Q1[1]:.3f}, Q2 {Q2[0]:.3f}/{Q2[1]:.3f}; window thirds Q1 {QW1[0]:.3f}/{QW1[1]:.3f}, Q2 {QW2[0]:.3f}/{QW2[1]:.3f}")

# ------------------------------------------------------------------ expected laws (CFG223 curves at the row's median z)
J223 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))["curves"]
LAWS = {"FLAT": lambda z: 1.0, "H(z)": lambda z: float(np.interp(z, J223["z"], J223["H(z)"])), "PROXY": lambda z: float(np.interp(z, J223["z"], J223["PROXY"]))}
LAWNAMES = list(LAWS)

TIME_TABLES = time.time()
# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (controls, model levers, mocks and precision; no row's level, amplitude or difference is printed)")
    # ---------------------------------------------------------------- C1, C2 (data plumbing)
    dev = 0.0
    for A_, Jk in ((WG0, "wgE"), (WW, "W"), (NNL, "NN")):
        S = np.zeros((NPAT, 2, 15)); np.add.at(S, (patch, typ), A_)
        dev = max(dev, float(np.max(np.abs(S - JK[Jk]) / np.maximum(np.abs(JK[Jk]), 1e-300))))
    check("C1 CONTROL: per-lens sums reproduce the June per-patch sums to 1e-9 relative", f"max relative deviation {dev:.1e}", dev < 1e-9)
    fr = {c: (ROWS[f"T-{CN[c]}-HI"].sum() / (typ == c).sum(), ROWS[f"T-{CN[c]}-LO"].sum() / (typ == c).sum()) for c in (0, 1)}
    disj = all(not np.any(ROWS[f"T-{CN[c]}-HI"] & ROWS[f"T-{CN[c]}-LO"]) and not np.any(ROWS[f"MM-{CN[c]}-HI"] & ROWS[f"MM-{CN[c]}-LO"]) for c in (0, 1))
    cnt = {r: int(ROWS[r].sum()) for r in SINGLE}
    c2 = disj and all(abs(f - 1 / 3) < 0.01 for c in (0, 1) for f in fr[c]) \
        and abs(cnt["MM-late-LO"] - 14736) <= 1 and abs(cnt["MM-late-HI"] - 14736) <= 1 and abs(cnt["MM-early-LO"] - 21675) <= 1 and abs(cnt["MM-early-HI"] - 21675) <= 1
    check("C2 CONTROL: the thirds are disjoint and hold 1/3 of their class to 1 %; the MM counts equal the frozen table (14,736 / 21,675 per third)",
          "; ".join(f"{r} {cnt[r]}" for r in SINGLE) + f"; z cuts class late {Q1[0]:.3f}/{Q2[0]:.3f}, early {Q1[1]:.3f}/{Q2[1]:.3f}", c2)

    # ---------------------------------------------------------------- the tables (the long part)
    P(f"\nbuilding the model tables (16 sets x 10 s-nodes; cached in {CACHE})")
    for nm in SETS:
        t = time.time(); tables(nm); P(f"  set {nm:7s} ready  ({time.time() - t:.0f} s)")
    TAB = tables("base")

    # ---------------------------------------------------------------- C3: the generalised stack against the committed machinery
    PROF, EDG = g61["PROF"], g61["EDGES"]
    LRGc = np.log(RG)

    def law_stack_ref(mask, foot, prof):                           # CFG255's law_stack, verbatim logic
        w = np.zeros((nA, nB)); np.add.at(w, (im[mask], iz[mask]), Mg61[mask])
        out = np.zeros(15)
        for k in range(15):
            lg = np.linspace(math.log(EDG[k]), math.log(EDG[k + 1]), SUB + 1)
            gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
            num = den = 0.0
            for a in range(nA):
                for b in range(nB):
                    if w[a, b] <= 0: continue
                    Mtab = 10 ** LMG[a] * (1 + fcold(LMG[a]))
                    pr = prof[(foot, "red", LMG[a], ZG[b])]
                    Rj = np.sqrt(G_SI * Mtab * MSUN / gs) / MPC
                    ds = np.interp(np.log(Rj), LRGc, pr["dsL"]) + pr["Mb"] / (math.pi * Rj ** 2)
                    wj = w[a, b] / gs
                    num += float(np.sum(wj * ds)); den += float(np.sum(wj))
            out[k] = num / den / 1e12
        return out

    nodeS1 = int(np.argmin(abs(LSN - 0.0)))
    d3 = 0.0
    c61 = json.load(open(os.path.join(CFG, "CFG61_kids_colour_split_results.json")))["numbers"]["RES"]["canonical"]
    for lab, mask in (("full late", typ == 0), ("full early", typ == 1)):
        mine = np.einsum("abk,ab->k", TAB[nodeS1], cellw(mask)) / cellw(mask).sum()
        ref = law_stack_ref(mask, "canonical", PROF)
        com = np.array(c61["ml"] if lab == "full late" else c61["me"])
        d3 = max(d3, float(np.max(np.abs(mine / ref - 1))), float(np.max(np.abs(mine / com - 1))))
    for r in SINGLE:
        mine = np.einsum("abk,ab->k", TAB[nodeS1], cellw(ROWS[r])) / cellw(ROWS[r]).sum()
        d3 = max(d3, float(np.max(np.abs(mine / law_stack_ref(ROWS[r], "canonical", PROF) - 1))))
    check("C3 CONTROL: the generalised stack at (s = 1, no shift, nu_mono, truncation 0.40, nominal gas, M_gal weights) reproduces CFG61's committed law stacks (full classes) and CFG255's law_stack (all 8 sets), all 15 bins, to 1e-9",
          f"max relative deviation {d3:.1e}", d3 < 1e-9)

    # ---------------------------------------------------------------- C4: spline against direct rebuild; C5: alt footing
    d4 = 0.0
    for lsx in (-0.625, 0.125, 0.875):
        direct = build_cells(lsx)
        for r in SINGLE:
            w = cellw(ROWS[r]); a_ = np.einsum("abk,ab->k", direct, w) / w.sum()
            spl = CubicSpline(LSN, np.log10(nodes_for(TAB, w)[:, :]), axis=0)(lsx)
            d4 = max(d4, float(np.max(np.abs(10 ** spl[K1] / a_[K1] - 1))))
    check("C4 CONTROL: the s-spline reproduces a direct rebuild at off-grid log10 s = -0.625, +0.125, +0.875 to 1e-3 relative in every K1 bin of every row", f"max relative deviation {d4:.1e}", d4 < 1e-3)
    d5 = 0.0
    for lsx in (-0.25, 0.0, 0.5):
        lsA = lsx + math.log10(A0C / A0A)
        d5 = max(d5, float(np.max(np.abs(build_cells(lsA, a0=A0A) / build_cells(lsx, a0=A0C) - 1))))
    check("C5 CONTROL: the alt footing at s' = s x (9.3603e-11 / 1.1312e-10) gives the canonical tables (the model depends on a0 only through a0 x s), 15 bins, all cells", f"max relative deviation {d5:.1e}", d5 < 1e-9)

    # ---------------------------------------------------------------- C6: noiseless identity
    d6 = 0.0
    for r in ALLROWS:
        m = model_of(r); Wm = diagW(get(r).sig)
        for st in (0.5, 1.0, 2.5):
            ls_, _ = solve1(m.at(math.log10(st)), Wm, m.fine)
            d6 = max(d6, abs(ls_ - math.log10(st)))
    check("C6 CONTROL: noiseless data = model(s_true) returns s_true to 1e-4 dex in every row (and both joint rows) for s_true = 0.5, 1, 2.5", f"max |d log10 s| {d6:.1e}", d6 < 1e-4)

    # ---------------------------------------------------------------- C8: mocks; A2 precision
    P("\nC8 / A2  MOCKS (noise N(0, C_row), C_row = the row's jackknife covariance; 2,000 mocks per row and truth)")
    MOCK = {}
    for r in ALLROWS:
        row = get(r); m = model_of(r); Wm = diagW(row.sig)
        rng = np.random.default_rng(zlib.crc32(("C8|" + r).encode()) % 100000)
        noise = rng.multivariate_normal(np.zeros(len(row.sig)), row.cov, size=2000)
        res = {}
        for st in (1.0, 2.5):
            ls_, unb = solve_many(m.at(math.log10(st))[None, :] + noise, Wm, m.fine)
            dd = ls_ - math.log10(st)
            mp = m.at(math.log10(st)) * math.log(10) * m.dlog(math.log10(st))
            w = mp / row.sig ** 2
            lin = float(math.sqrt(w @ row.cov @ w) / abs(w @ mp))
            res[st] = dict(bias=float(dd.mean()), sd=float(dd.std()), lin=lin, unb=float(unb.mean()))
        MOCK[r] = res
    c8 = all(abs(v[st]["bias"]) <= 0.2 * v[st]["sd"] and abs(v[st]["lin"] / v[st]["sd"] - 1) <= 0.15 for v in MOCK.values() for st in (1.0, 2.5))
    check("C8 CONTROL: mocks recover the planted level without bias (|mean| <= 0.2 SD) and the analytic linearised sigma is within 15 % of the mock SD, all rows, s_true = 1 and 2.5",
          "; ".join(f"{r}: bias {MOCK[r][1.0]['bias']:+.3f}/{MOCK[r][2.5]['bias']:+.3f}, SD {MOCK[r][1.0]['sd']:.3f}/{MOCK[r][2.5]['sd']:.3f}, lin {MOCK[r][1.0]['lin']:.3f}/{MOCK[r][2.5]['lin']:.3f}" for r in ALLROWS), c8)

    # ---------------------------------------------------------------- C7: error calibration on random class thirds (only aggregated differences printed)
    rngC7 = np.random.default_rng(261)
    zs = []
    for c in (0, 1):
        idx = np.where(typ == c)[0]
        for t in range(100):
            u = rngC7.random(len(idx)); mA = np.zeros(NLENS, bool); mB = np.zeros(NLENS, bool)
            mA[idx[u < 1 / 3]] = True; mB[idx[u > 2 / 3]] = True
            ra, rb = RowData(mA, WGd), RowData(mB, WGd)
            ma, mb_ = ra.model(), rb.model()
            la, _ = solve1(ra.d, diagW(ra.sig), ma.fine); lb, _ = solve1(rb.d, diagW(rb.sig), mb_.fine)
            LA, _ = solve_many(ra.loo, diagW(ra.sig), ma.fine); LB, _ = solve_many(rb.loo, diagW(rb.sig), mb_.fine)
            sdd = jack_sd(LA - LB)
            zs.append((la - lb) / sdd)
    zs = np.array(zs)
    check("C7 CONTROL (blind error calibration): for 200 random pairs of disjoint class thirds, mean(Delta / sigma_Delta) in [-0.25, 0.25] and SD in [0.8, 1.25] (only these aggregates are printed; the jackknife sigma of the difference of the two thirds' log s*)",
          f"mean {zs.mean():+.3f}, SD {zs.std():.3f}, N {len(zs)}", abs(zs.mean()) <= 0.25 and 0.8 <= zs.std() <= 1.25)

    # ---------------------------------------------------------------- A1 levers (noiseless model against model)
    P("\nA1  LEVERS (noiseless: data = the base model at s = 1; each variant solves against it)")
    LEV = {}
    for r in ALLROWS:
        row = get(r); m0 = model_of(r); d0 = m0.at(0.0); Wm = diagW(row.sig)
        o = {}
        for nm in ("b-30", "b-15", "b+15", "b+30", "hot0.5", "hot1.0", "epP", "epM"):
            o[nm] = solve1(d0, Wm, model_of(r, nm).fine)[0]
        for nm in ("kernP2", "tf0.20", "tf0.80", "gf0.50", "gf1.50"):
            o[nm] = solve1(d0, Wm, model_of(r, nm).fine)[0]
        o["WW"] = solve1(d0, Wm, model_of(r, "base", "WW").fine)[0]
        o["Lb"] = (o["b+15"] - o["b-15"]) / 0.30
        LEV[r] = o
    P("  baryon lever L_b = d log10 s*/d(baryon dex) and the band edges in log10 s* (shift -0.30 / -0.15 / +0.15 / +0.30):")
    for r in ALLROWS:
        o = LEV[r]; P(f"    {r:11s} L_b {o['Lb']:+.3f}   bands {o['b-30']:+.3f} {o['b-15']:+.3f} {o['b+15']:+.3f} {o['b+30']:+.3f}   half-widths inner {0.5 * (o['b-15'] - o['b+15']):.3f} outer {0.5 * (o['b-30'] - o['b+30']):.3f} dex")
    P("  recipe knobs (model against model; Delta log10 s*):")
    for r in ALLROWS:
        o = LEV[r]; P(f"    {r:11s} kernel P2 {o['kernP2']:+.3f}  trunc 0.20/0.80 {o['tf0.20']:+.3f}/{o['tf0.80']:+.3f}  weights WW {o['WW']:+.3f}  cold gas x0.5/x1.5 {o['gf0.50']:+.3f}/{o['gf1.50']:+.3f}")
    P("  hot-gas scenarios on the early rows (Delta log10 s*; f_hot = 0.5 / 1.0): " + "; ".join(f"{r} {LEV[r]['hot0.5']:+.3f}/{LEV[r]['hot1.0']:+.3f}" for r in ("T-early-LO", "T-early-HI", "MM-early-LO", "MM-early-HI")))
    P("  mass-dependent drift eps = +0.10 (level shift of each row, then the shift of d = log s*(HI) - log s*(LO) per class):")
    DD = {}
    for cn in ("late", "early"):
        for pre in ("T", "MM"):
            lo, hi = f"{pre}-{cn}-LO", f"{pre}-{cn}-HI"
            DD[f"{pre}-{cn}"] = dict(epP=(LEV[hi]["epP"] - LEV[lo]["epP"]), epM=(LEV[hi]["epM"] - LEV[lo]["epM"]))
            # redshift drift on the HI third only
            r_ = []
            for nm in ("dz0.02", "dz0.05"):
                r_.append(solve1(model_of(hi).at(0.0), diagW(get(hi).sig), model_of(hi, nm).fine)[0])
            DD[f"{pre}-{cn}"]["dz"] = r_
            P(f"    {pre}-{cn}: levels LO {LEV[lo]['epP']:+.3f} HI {LEV[hi]['epP']:+.3f}; d shift eps=+0.10 {DD[f'{pre}-{cn}']['epP']:+.3f}, eps=-0.10 {DD[f'{pre}-{cn}']['epM']:+.3f}; HI-only drift +0.02 / +0.05: {r_[0]:+.3f} / {r_[1]:+.3f}")

    # ---------------------------------------------------------------- A2 precision, A3 R_cal, A4 sigma_diff
    P("\nA2 / A3  PRECISION AND CALIBRATION DOMINANCE (mock SD of log10 s* at s_true = 1 = the 68 % half-width; R_cal = 0.15 |L_b| / SD)")
    RCAL = {}
    for r in ALLROWS:
        RCAL[r] = 0.15 * abs(LEV[r]["Lb"]) / MOCK[r][1.0]["sd"]
        P(f"    {r:11s} SD {MOCK[r][1.0]['sd']:.3f} dex (analytic {MOCK[r][1.0]['lin']:.3f})   R_cal {RCAL[r]:.2f}   {'CALIBRATION-LIMITED' if RCAL[r] >= 1 else 'statistics-limited'}")
    P("\nA4  THE THIRDS' DIFFERENCE (jackknife sigma of d = log s*(HI) - log s*(LO); no value of d is printed)")
    SDIFF = {}
    for pre in ("T", "MM"):
        for cn in ("late", "early"):
            lo, hi = f"{pre}-{cn}-LO", f"{pre}-{cn}-HI"
            mlo, mhi = model_of(lo), model_of(hi)
            LL, _ = solve_many(RD[lo].loo, diagW(RD[lo].sig), mlo.fine); LH, _ = solve_many(RD[hi].loo, diagW(RD[hi].sig), mhi.fine)
            sdd = jack_sd(LH - LL)
            zl_, zh_ = RD[lo].zmed, RD[hi].zmed
            rv = math.log10(LAWS["H(z)"](zh_) / LAWS["H(z)"](zl_)); px = math.log10(LAWS["PROXY"](zh_) / LAWS["PROXY"](zl_))
            Lb = 0.5 * (abs(LEV[lo]["Lb"]) + abs(LEV[hi]["Lb"]))
            ps = abs(rv) >= 2 * sdd
            psys = {dl: abs(rv) >= 2 * math.sqrt(sdd ** 2 + (Lb * dl) ** 2) for dl in (0.02, 0.05)}
            SDIFF[f"{pre}-{cn}"] = dict(sd=sdd, rival=rv, proxy=px, possible_stat=bool(ps), possible_sys={str(k): bool(v) for k, v in psys.items()})
            P(f"    {pre}-{cn}: sigma_diff {sdd:.3f} dex; H(z) expects d = {rv:+.3f} (PROXY {px:+.3f}) at z {zl_:.3f} -> {zh_:.3f}; POSSIBLE_STAT {ps}; POSSIBLE_SYS at delta 0.02 / 0.05: {psys[0.02]} / {psys[0.05]}")
    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P("\nDECISIONS (the frozen map)")
    P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C8; failed ones listed in the check lines above)")
    P("  PF-D2 CALIBRATION-LIMITED rows: " + ", ".join(f"{r} ({RCAL[r]:.2f})" for r in ALLROWS if RCAL[r] >= 1) + "; statistics-limited: " + ", ".join(f"{r} ({RCAL[r]:.2f})" for r in ALLROWS if RCAL[r] < 1))
    P(f"  PF-D3 FLAT versus H(z) from the thirds' levels (T rows): POSSIBLE_STAT {all(SDIFF[f'T-{c}']['possible_stat'] for c in ('late', 'early'))}; POSSIBLE_SYS at delta 0.02 {all(SDIFF[f'T-{c}']['possible_sys']['0.02'] for c in ('late', 'early'))} / 0.05 {all(SDIFF[f'T-{c}']['possible_sys']['0.05'] for c in ('late', 'early'))}  (NOT POSSIBLE if any False)")
    P(f"  PF-D4 DRAWABLE as a calibration-limited level (needs PF-D1): {pfd1}")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9) scored:")
    he = {}
    prim = ["T-late-LO", "T-late-HI", "T-early-LO", "T-early-HI"]
    he["HE1"] = all(-1.50 <= LEV[r]["Lb"] <= -1.12 for r in prim)
    he["HE2"] = all(0.17 <= 0.5 * (LEV[r]["b-15"] - LEV[r]["b+15"]) <= 0.23 and 0.34 <= 0.5 * (LEV[r]["b-30"] - LEV[r]["b+30"]) <= 0.45 for r in prim)
    rng3 = {"T-late-LO": (0.12, 0.30), "T-late-HI": (0.07, 0.20), "T-early-LO": (0.04, 0.12), "T-early-HI": (0.04, 0.12)}
    he["HE3"] = all(rng3[r][0] <= MOCK[r][1.0]["sd"] <= rng3[r][1] for r in prim)
    he["HE4"] = RCAL["T-early-LO"] >= 1.5 and RCAL["T-early-HI"] >= 1.5 and RCAL["T-late-HI"] >= 1.0 and 0.6 <= RCAL["T-late-LO"] <= 1.6
    he["HE5"] = all(0.03 <= LEV[r]["kernP2"] <= 0.08 for r in prim)
    he["HE6"] = all(abs(LEV[r][k]) <= 0.01 for r in prim for k in ("tf0.20", "tf0.80"))
    he["HE7"] = all(abs(LEV[r]["WW"]) <= 0.03 for r in prim)
    he8 = {"T-late-LO": (0.10, 0.20), "T-late-HI": (0.03, 0.07), "T-early-LO": (0.04, 0.08), "T-early-HI": (0.02, 0.06)}
    he["HE8"] = all(he8[r][0] <= LEV[r]["gf0.50"] <= he8[r][1] for r in prim)
    he["HE9"] = (0.09 <= -DD["T-late"]["epP"] <= 0.14) and (0.03 <= -DD["T-early"]["epP"] <= 0.055) and all(0.01 <= -DD[f"MM-{c}"]["epP"] <= 0.04 for c in ("late", "early")) \
        and all(0.055 <= -DD[f"T-{c}"]["dz"][1] <= 0.075 for c in ("late", "early"))
    he["HE10"] = all(-0.26 <= LEV[r]["hot0.5"] <= -0.20 and -0.44 <= LEV[r]["hot1.0"] <= -0.35 for r in ("T-early-LO", "T-early-HI"))
    he["HE11"] = abs(zs.mean()) <= 0.25 and 0.8 <= zs.std() <= 1.25
    he["HE12"] = c8
    he["HE13"] = not any(SDIFF[f"T-{c}"]["possible_stat"] for c in ("late", "early")) and 0.12 <= SDIFF["T-late"]["sd"] <= 0.35 and 0.05 <= SDIFF["T-early"]["sd"] <= 0.13
    for k, v in he.items():
        P(f"    {k}: {'hit' if v else 'MISS (kept as it falls)'}")
    NUM.update(levers=LEV, mocks={r: {str(k): v for k, v in MOCK[r].items()} for r in MOCK}, rcal=RCAL, sdiff=SDIFF, drift=DD, c7=dict(mean=float(zs.mean()), sd=float(zs.std()), n=len(zs)),
               hand_estimates=he, pf=dict(PF_D1=bool(pfd1)), n={r: get(r).n for r in ALLROWS}, zmed={r: get(r).zmed for r in ALLROWS})

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST: fabricated data)" if SELFTEST else "") + (" (MUTATE: planted s = 2)" if MUTATE else ""))
    BOOT = 10000
    RES = {}
    TAB = tables("base")
    for nm in SETS:
        tables(nm)
    P(f"  tables ready ({time.time() - T0:.0f} s)")

    def central(r, setname="base", weights="Mg", ksel=None, est="diag"):
        row = get(r)
        m = model_of(r, setname, weights, ksel)
        if ksel is not None:
            kk = [K1.index(k) for k in ksel] if r not in JD else None
        d, sig, cov = row.d, row.sig, row.cov
        if ksel is not None:
            if r in JD:
                kk = [K1.index(k) for k in ksel] + [len(K1) + K1.index(k) for k in ksel]
            d, sig, cov = d[kk], sig[kk], cov[np.ix_(kk, kk)]
        if est == "diag": Wm = np.diag(1 / sig ** 2)
        elif est == "gls": Wm = np.linalg.inv(cov)
        else:
            nn = row.nn if ksel is None else row.nn[kk]; Wm = np.outer(nn, nn)
        return solve1(d, Wm, m.fine)

    for r in ALLROWS:
        row = get(r); m = model_of(r); p = len(row.sig)
        seed_lab = r
        Bidx = boot_idx(seed_lab, BOOT)
        tg = Bidx @ row.Sg; tw = Bidx @ row.Sw
        dB = tg / tw / KG
        lsb, ub = solve_many(dB, diagW(row.sig), m.fine)
        ls0, u0 = solve1(row.d, diagW(row.sig), m.fine)
        itv = interval(lsb, ub)
        jl, _ = solve_many(row.loo, diagW(row.sig), m.fine)
        jsd = jack_sd(jl)
        # chi2 with the full covariance (Hartlap) at s* and at s = 1
        Cinv = np.linalg.inv(row.cov) * H12(p)
        mm = m.at(ls0); m1 = m.at(0.0)
        chi_s = float((row.d - mm) @ Cinv @ (row.d - mm)); chi_1 = float((row.d - m1) @ Cinv @ (row.d - m1))
        # bands
        band = {}
        for lab, nm in (("-0.30", "b-30"), ("-0.15", "b-15"), ("+0.15", "b+15"), ("+0.30", "b+30")):
            band[lab] = solve1(row.d, diagW(row.sig), model_of(r, nm).fine)
        lev = (band["+0.15"][0] - band["-0.15"][0]) / 0.30
        # needed baryon shift for s* = 1: linear fit of log s* against the shift through the five points
        xs = np.array([-0.30, -0.15, 0.0, 0.15, 0.30]); ys = np.array([band["-0.30"][0], band["-0.15"][0], ls0, band["+0.15"][0], band["+0.30"][0]])
        slope, icpt = np.polyfit(xs, ys, 1)
        need = float(-icpt / slope) if abs(slope) > 1e-6 else float("nan")
        # recipe knobs
        knob = {}
        knob["kernel P2"] = [central(r, "kernP2")[0] - ls0]
        knob["truncation"] = [central(r, "tf0.20")[0] - ls0, central(r, "tf0.80")[0] - ls0]
        knob["weights WW"] = [central(r, "base", "WW")[0] - ls0]
        knob["cold gas"] = [central(r, "gf0.50")[0] - ls0, central(r, "gf1.50")[0] - ls0]
        knob["K1"] = [central(r, "base", "Mg", [9, 10, 11, 12, 13, 14])[0] - ls0, central(r, "base", "Mg", [8, 9, 10, 11, 12])[0] - ls0]
        knob["estimator"] = [central(r, est="gls")[0] - ls0, central(r, est="amp")[0] - ls0]
        recipe_half = math.sqrt(sum(max(abs(x) for x in v) ** 2 for v in knob.values()))
        hot = {nm: solve1(row.d, diagW(row.sig), model_of(r, nm).fine)[0] for nm in ("hot0.5", "hot1.0")}
        drift = {nm: solve1(row.d, diagW(row.sig), model_of(r, nm).fine)[0] for nm in ("epP", "epM", "dz0.02", "dz0.05")}
        RES[r] = dict(n=row.n, z=row.zmed, ls=ls0, s=10 ** ls0, unb=u0, itv=itv, jsd=jsd, chi_s=chi_s, chi_1=chi_1, p=p, p_s=float(CHI2.sf(chi_s, p - 1)), p_1=float(CHI2.sf(chi_1, p)),
                      band={k: dict(ls=v[0], s=10 ** v[0], unb=v[1]) for k, v in band.items()}, lever=lev, need=need, knob=knob, recipe_half=recipe_half, hot=hot, drift=drift)
        a0 = 10 ** ls0 * 9.3603e-11 * 1e10
        P(f"  {r:11s} N {row.n:6d} z {row.zmed:.3f}:  s* = {10 ** ls0:.3f} (a0 = {a0:.3f}e-10){' [UNBOUNDED]' if u0 else ''}  68% [{10 ** itv['lo68']:.3f}, {10 ** itv['hi68']:.3f}]  95% [{10 ** itv['lo95']:.3f}, {10 ** itv['hi95']:.3f}]  (SD {itv['sd']:.3f}, jackknife {jsd:.3f} dex; unbounded {itv['unb_frac']:.3f})")
        b15 = (10 ** min(band['-0.15'][0], band['+0.15'][0]), 10 ** max(band['-0.15'][0], band['+0.15'][0])); b30 = (10 ** min(band['-0.30'][0], band['+0.30'][0]), 10 ** max(band['-0.30'][0], band['+0.30'][0]))
        P(f"      baryon +-0.15 [{b15[0]:.3f}, {b15[1]:.3f}]  +-0.30 [{b30[0]:.3f}, {b30[1]:.3f}] (lever {lev:+.3f}; baryon shift that gives s* = 1: {need:+.3f} dex);  recipe half-width {recipe_half:.3f} dex;  chi2(s*) {chi_s:.1f}/{p - 1} (p {RES[r]['p_s']:.3g}), chi2(s=1) {chi_1:.1f}/{p} (p {RES[r]['p_1']:.3g})")
        P("      knobs (Delta log10 s*): " + "; ".join(f"{k} " + "/".join(f"{x:+.3f}" for x in v) for k, v in knob.items()))
        P(f"      hot gas f_hot 0.5 / 1.0: {hot['hot0.5'] - ls0:+.3f} / {hot['hot1.0'] - ls0:+.3f};  drift eps +0.10 / -0.10: {drift['epP'] - ls0:+.3f} / {drift['epM'] - ls0:+.3f};  HI-style z drift +0.02 / +0.05: {drift['dz0.02'] - ls0:+.3f} / {drift['dz0.05'] - ls0:+.3f}")

    # ---------------------------------------------------------------- per-class differences, flags, agreement
    P("\nTHE THIRDS' DIFFERENCE d = log10 s*(HI) - log10 s*(LO) per class (jackknife sigma; the drift scenarios on d)")
    DIFF = {}
    c255 = json.load(open(os.path.join(CFG, "CFG255_lensing_rar_zsplit", "cfg255_stageB_results.json")))["numbers"]
    for pre in ("T", "MM"):
        for c, cn in ((0, "late"), (1, "early")):
            lo, hi = f"{pre}-{cn}-LO", f"{pre}-{cn}-HI"
            d_ = RES[hi]["ls"] - RES[lo]["ls"]
            LL, _ = solve_many(RD[lo].loo, diagW(RD[lo].sig), model_of(lo).fine); LH, _ = solve_many(RD[hi].loo, diagW(RD[hi].sig), model_of(hi).fine)
            sd_ = jack_sd(LH - LL)
            sc = {k: (RES[hi]["drift"][k] if k in ("epP", "epM") else None) for k in ("epP", "epM")}
            dsc = {"eps +0.10": RES[hi]["drift"]["epP"] - RES[lo]["drift"]["epP"] - d_, "eps -0.10": RES[hi]["drift"]["epM"] - RES[lo]["drift"]["epM"] - d_,
                   "HI drift +0.02": RES[hi]["drift"]["dz0.02"] - RES[hi]["ls"], "HI drift +0.05": RES[hi]["drift"]["dz0.05"] - RES[hi]["ls"]}
            rv = math.log10(LAWS["H(z)"](RES[hi]["z"]) / LAWS["H(z)"](RES[lo]["z"]))
            DIFF[f"{pre}-{cn}"] = dict(d=d_, sd=sd_, scen=dsc, rival=rv)
            P(f"  {pre}-{cn:5s}: d = {d_:+.3f} +- {sd_:.3f} dex (H(z) expects {rv:+.3f}; FLAT 0)   drift scenarios on d: " + "; ".join(f"{k} {v:+.3f}" for k, v in dsc.items()))
    amp0 = 0.0009
    M3 = {}
    for c, cn in ((0, "late"), (1, "early")):
        a_data = c255["A_class"][str(c)][0]
        M3[cn] = dict(d=DIFF[f"T-{cn}"]["d"], from255=2 * (a_data - amp0), sd=DIFF[f"T-{cn}"]["sd"])
    P("\nFLAGS PER LAW (in the statistical 95 % interval / in its hull with the inner baryon band / with the outer band) and agreements")
    FLAGS = {}
    for r in ALLROWS:
        R_ = RES[r]; f = {}
        b15v = (R_["band"]["-0.15"]["s"], R_["band"]["+0.15"]["s"]); b30v = (R_["band"]["-0.30"]["s"], R_["band"]["+0.30"]["s"])
        lo95, hi95 = 10 ** R_["itv"]["lo95"], 10 ** R_["itv"]["hi95"]
        for L in LAWNAMES:
            sL = LAWS[L](R_["z"])
            f[L] = dict(s=sL, in95=bool(lo95 <= sL <= hi95), in15=bool(min(lo95, *b15v) <= sL <= max(hi95, *b15v)), in30=bool(min(lo95, *b30v) <= sL <= max(hi95, *b30v)))
        FLAGS[r] = f
        P(f"  {r:11s} " + "  ".join(f"{L}: s_L {f[L]['s']:.3f} {''.join('Y' if f[L][k] else 'n' for k in ('in95', 'in15', 'in30'))}" for L in LAWNAMES))
    AGREE = {}
    for pre in ("T", "MM"):
        for th in ("LO", "HI"):
            a, b = RES[f"{pre}-late-{th}"], RES[f"{pre}-early-{th}"]
            wa = (min(a["band"]["-0.30"]["s"], a["band"]["+0.30"]["s"], 10 ** a["itv"]["lo95"]), max(a["band"]["-0.30"]["s"], a["band"]["+0.30"]["s"], 10 ** a["itv"]["hi95"]))
            wb = (min(b["band"]["-0.30"]["s"], b["band"]["+0.30"]["s"], 10 ** b["itv"]["lo95"]), max(b["band"]["-0.30"]["s"], b["band"]["+0.30"]["s"], 10 ** b["itv"]["hi95"]))
            ov = bool(max(wa[0], wb[0]) <= min(wa[1], wb[1]))
            AGREE[f"{pre}-{th}"] = dict(overlap=ov, late=wa, early=wb)
            P(f"  class agreement {pre}-{th}: late [{wa[0]:.3f}, {wa[1]:.3f}] vs early [{wb[0]:.3f}, {wb[1]:.3f}] (95 % widened by the outer band): " + ("consistent within the outer band" if ov else "classes DISAGREE: one a0 does not describe both"))
    P("\nCONTROLS (stage B)")
    NUM.update(rows=RES, diff=DIFF, flags=FLAGS, agree=AGREE, m3=M3)
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg261_stageB_results.json")))["numbers"]["rows"]
        sh = {r: RES[r]["ls"] - main[r]["ls"] for r in ALLROWS}
        check("M2 MUTATE=1 (reactivity): the planted factor 2 moves every row's log10 s* by +0.301 +- 0.02 against the main run (joint rows included)", "; ".join(f"{r} {v:+.3f}" for r, v in sh.items()),
              all(abs(v - 0.30103) <= 0.02 for v in sh.values()))
        NUM["mutate_shift"] = sh
    else:
        if not SELFTEST:
            check("M3 (reported) the thirds' difference d per class agrees with 2 x (A_data - A_FLAT) of CFG255's committed stage B within 1 sigma_diff (different estimators)",
              "; ".join(f"{cn}: d {M3[cn]['d']:+.3f} vs 2(A - A_FLAT) {M3[cn]['from255']:+.3f}, sigma_diff {M3[cn]['sd']:.3f}" for cn in M3), all(abs(M3[cn]["d"] - M3[cn]["from255"]) <= M3[cn]["sd"] for cn in M3), load_bearing=False)
        hull = all(min(RES[a]["ls"], RES[b]["ls"]) - 2 * max(RES[a]["itv"]["sd"], RES[b]["itv"]["sd"]) <= RES[j]["ls"] <= max(RES[a]["ls"], RES[b]["ls"]) + 2 * max(RES[a]["itv"]["sd"], RES[b]["itv"]["sd"])
                   for j, (a, b) in JOINT.items())
        check("M5 each joint row's log10 s* lies in the hull of its two class rows (within 2 bootstrap SD)", "; ".join(f"{j}: {RES[j]['ls']:+.3f} in [{min(RES[a]['ls'], RES[b]['ls']):+.3f}, {max(RES[a]['ls'], RES[b]['ls']):+.3f}]" for j, (a, b) in JOINT.items()), hull)
    if SELFTEST:
        ok = all(RES[r]["itv"]["lo95"] - 0.05 <= math.log10(S_TRUE_SELF) <= RES[r]["itv"]["hi95"] + 0.05 for r in SINGLE)
        check("SELFTEST: every single row returns the fabricated truth inside its 95 % interval (+-0.05 dex allowance for the weighting difference)", "; ".join(f"{r} {RES[r]['s']:.3f}" for r in SINGLE) + f" (truth {S_TRUE_SELF})", ok)

    # ---------------------------------------------------------------- the points file
    cols = ["lane", "object", "gas_class", "z", "z_shown", "no_root", "s_star", "a0_1e-10_m_s2", "stat68_lo", "stat68_hi", "stat95_lo", "stat95_hi", "inner_lo", "inner_hi", "inner_noroot_corner", "outer_lo", "outer_hi", "outer_noroot_corner",
            "recipe_half_dex", "recipe_lo", "recipe_hi", "n", "class", "third", "set", "R_cal", "chi2_s", "p_shape", "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    ref = os.path.join(CFG, "CHART_a0z_combined_2026-09-30", "chart_a0z_points.csv")
    ref_cols = open(ref).readline().strip().split(",")
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{ref_cols == cols[:18]}", ref_cols == cols[:18])
    allsd = {r: RES[r]["itv"]["sd"] for r in ALLROWS}
    with open(os.path.join(HERE, f"cfg261_points{SFX}.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for r in ALLROWS:
            R_ = RES[r]
            b15v = sorted([R_["band"]["-0.15"]["s"], R_["band"]["+0.15"]["s"]]); b30v = sorted([R_["band"]["-0.30"]["s"], R_["band"]["+0.30"]["s"]])
            nr15 = int(R_["band"]["-0.15"]["unb"] or R_["band"]["+0.15"]["unb"]); nr30 = int(R_["band"]["-0.30"]["unb"] or R_["band"]["+0.30"]["unb"])
            hs = 0.5 * abs(R_["band"]["-0.15"]["ls"] - R_["band"]["+0.15"]["ls"])
            rc = hs / max(0.5 * (R_["itv"]["hi68"] - R_["itv"]["lo68"]), 1e-9)
            cl = "joint" if r in JD else CN[CLASS_OF[r]]; th = r.split("-")[-1]; st = "joint" if r in JD else r.split("-")[0]
            thr = "J" if r in JD else ("T" if r.startswith("T") else "MM")
            agree = AGREE.get(f"{thr}-{th}", {}).get("overlap") if r not in JD else None
            q = ("calibration-limited (M* zero point dominates)" if rc >= 1 else "statistics-limited") + ("; shape fails (amplitude-matched only)" if R_["p_s"] < 0.01 else "; shape adequate") \
                + ("" if agree is None else ("; classes consistent within the outer band" if agree else "; classes disagree"))
            if r in JD: q += "; joint one-s fit, not a headline"
            if r.startswith("MM"): q += "; mass-matched window (secondary)"
            fl = FLAGS[r]
            w.writerow(["CFG261", f"KiDS-1000 lensing {r}", "LENS (scaling-relation cold gas)", f"{R_['z']:.4f}", f"{R_['z']:.4f}", int(R_["unb"]), f"{R_['s']:.6f}", f"{R_['s'] * 0.93603:.6f}",
                        f"{10 ** R_['itv']['lo68']:.6f}", f"{10 ** R_['itv']['hi68']:.6f}", f"{10 ** R_['itv']['lo95']:.6f}", f"{10 ** R_['itv']['hi95']:.6f}",
                        f"{b15v[0]:.6f}", f"{b15v[1]:.6f}", nr15, f"{b30v[0]:.6f}", f"{b30v[1]:.6f}", nr30,
                        f"{R_['recipe_half']:.4f}", f"{R_['s'] * 10 ** (-R_['recipe_half']):.6f}", f"{R_['s'] * 10 ** R_['recipe_half']:.6f}", R_["n"], cl, th, st, f"{rc:.3f}", f"{R_['chi_s']:.2f}", f"{R_['p_s']:.4g}",
                        "".join("Y" if fl["FLAT"][k] else "n" for k in ("in95", "in15", "in30")), "".join("Y" if fl["H(z)"][k] else "n" for k in ("in95", "in15", "in30")),
                        "".join("Y" if fl["PROXY"][k] else "n" for k in ("in95", "in15", "in30")), q])
    P(f"\n  points written: cfg261_points{SFX}.csv ({len(ALLROWS)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")


def jc(o):
    if isinstance(o, dict): return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jc(v) for v in o]
    if isinstance(o, np.ndarray): return jc(o.tolist())
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    return o


open(os.path.join(HERE, f"cfg261{SFX}.out"), "w").write("\n".join(LOG) + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=jc(NUM)), open(os.path.join(HERE, f"cfg261{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
