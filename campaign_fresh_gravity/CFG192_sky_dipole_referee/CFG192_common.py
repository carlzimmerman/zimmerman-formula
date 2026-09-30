#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG192_common -- shared machinery of the CFG192 referee lane (independent re-derivation of CFG182's SPARC a0 sky-dipole test).
Repo-import-free: the repo enters ONLY as data files (ZF_REPO, or found by walking up from this file / the cwd).
Nothing is printed on import.  Frozen criteria: CFG192_FROZEN_CRITERIA.md.
"""
import os
import sys
import math
import json
import time
import builtins
import multiprocessing as mp

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import least_squares, minimize, brentq
from scipy.interpolate import CubicSpline
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
KPC = 3.0856775814913673e19
LN10 = math.log(10.0)
NPROC = int(os.environ.get("CFG192_NPROC", "12"))


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.exists(os.path.join(r, "real_research", "data", "SPARC_Lelli2016c.mrt")):
        return os.path.abspath(r)
    for start in (HERE, os.getcwd()):
        d = os.path.abspath(start)
        for _ in range(12):
            if os.path.exists(os.path.join(d, "real_research", "data", "SPARC_Lelli2016c.mrt")):
                return d
            d = os.path.dirname(d)
    raise RuntimeError("repo not found: set ZF_REPO")


REPO = find_repo()
DATA = os.path.join(REPO, "real_research", "data")


def scrub(s):
    """no absolute path in any output"""
    return str(s).replace(REPO, "<repo>").replace(HERE, "<cfg192>").replace(os.path.expanduser("~"), "~")


# ---------------------------------------------------------------------------------------------- run harness
class Run:
    def __init__(self, slug, suffix=""):
        self.slug = slug
        self.out_path = os.path.join(HERE, f"{slug}{suffix}.out")
        self.json_path = os.path.join(HERE, f"{slug}{suffix}.json")
        self._f = builtins.open(self.out_path, "w", encoding="utf-8")
        self._so = sys.stdout
        sys.stdout = self
        self.t0 = time.time()
        self.R = {"script": slug, "numbers": {}, "checks": {}}
        self.CH = []

    def write(self, t):
        self._so.write(t)
        self._f.write(scrub(t))

    def flush(self):
        self._so.flush()
        self._f.flush()

    def P(self, *a):
        print(*a, flush=True)

    def T(self, msg):  # timing goes to stderr only (outputs must be byte-identical on re-run)
        sys.stderr.write(f"[{time.time() - self.t0:.0f} s] {msg}\n")
        sys.stderr.flush()

    def banner(self, t):
        self.P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)

    def num(self, k, v):
        self.R["numbers"][k] = jclean(v)
        return v

    def check(self, name, measured, ok, load_bearing=True):
        ok = bool(ok)
        self.CH.append((name, ok, load_bearing))
        self.R["checks"][name] = {"ok": ok, "load_bearing": load_bearing, "measured": str(measured)}
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}  |  {measured}")
        return ok

    def finish(self, rc=0, extra=""):
        nlb = sum(1 for _, ok, lb in self.CH if (not ok) and lb)
        self.R["load_bearing_failures"] = nlb
        with builtins.open(self.json_path, "w", encoding="utf-8") as fh:
            json.dump(jclean(self.R), fh, indent=1)
        self.P(f"\n  {sum(1 for _, ok, _ in self.CH if ok)}/{len(self.CH)} checks pass; load-bearing failures {nlb}; {extra}")
        self.P(f"rc = {rc}")
        sys.stdout = self._so
        self._f.close()
        sys.stderr.write(f"[{time.time() - self.t0:.0f} s] done\n")
        return rc


def jclean(o):
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else str(k)): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, np.floating):
        o = float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float):
        if math.isnan(o) or math.isinf(o):
            return str(o)
    return o


# ---------------------------------------------------------------------------------------------- coordinates
_AG = np.array([[-0.0548755604162154, -0.8734370902348850, -0.4838350155487132],
                [+0.4941094278755837, -0.4448296299600112, +0.7469822444972189],
                [-0.8676661490190047, -0.1980763734312015, +0.4559837761750669]])


def radec_to_gal(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    v = np.array([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)])
    g = _AG @ v
    return math.degrees(math.atan2(g[1], g[0])) % 360.0, math.degrees(math.asin(np.clip(g[2], -1, 1)))


def lb_to_vec(l, b):
    l, b = np.radians(l), np.radians(b)
    return np.array([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)])


def vec_to_lb(v):
    v = np.asarray(v, float)
    v = v / np.linalg.norm(v)
    return math.degrees(math.atan2(v[1], v[0])) % 360.0, math.degrees(math.asin(np.clip(v[2], -1, 1)))


def ang(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return math.degrees(math.acos(np.clip(np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b), -1, 1)))


def axis_ang(a, b):
    t = ang(a, b)
    return min(t, 180.0 - t)


def rand_dirs(rng, n):
    v = rng.normal(size=(n, 3))
    return v / np.linalg.norm(v, axis=1, keepdims=True)


DIRS = {"CMB": lb_to_vec(264.0, 48.3), "bulk": lb_to_vec(304.0, 6.0), "Chang": lb_to_vec(171.30, -15.41),
        "Zhou": lb_to_vec(175.5, -6.5), "Virgo": lb_to_vec(283.8, 74.5)}


# ---------------------------------------------------------------------------------------------- kernel (own implementation)
def _h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore", invalid="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def _dh_rar(y, e=1e-6):
    return (_h_rar(y * (1 + e)) - _h_rar(y * (1 - e))) / (2 * y * e)


_Y_P = brentq(lambda y: float(_dh_rar(y)), 1.0, 5.0)
_H_P = float(_h_rar(_Y_P))
_LYG = np.linspace(-14, 14, 280001)
_YG = 10 ** _LYG
_DH = np.maximum(_dh_rar(_YG), 0.05 * _H_P / (_YG + _Y_P))
_HM = float(_h_rar(_YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (_DH[1:] + _DH[:-1]) * np.diff(_YG))])


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 + np.interp(np.log10(y), _LYG, _HM) / y


def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def nu_simple(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_newton(y):
    return np.ones_like(np.asarray(y, float))


KERNELS = {"mono": nu_mono, "p2": nu_p2, "simple": nu_simple, "newton": nu_newton}


# ---------------------------------------------------------------------------------------------- data
def load_all(verbose=False):
    """all 175 galaxies with rotmod, master-table meta and (l, b) from the VizieR position table. Own parsers."""
    d_ = os.path.join(DATA, "sparc_data")
    gal = {}
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        d = np.loadtxt(os.path.join(d_, f), comments="#", ndmin=2)
        gal[f[:-11]] = dict(name=f[:-11], R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4], Vbul=d[:, 5])
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L", "eL", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    with open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")) as fh:
        for line in fh:
            tok = line.split()
            if len(tok) != 19:
                continue
            try:
                vals = [float(t) for t in tok[1:18]]
            except ValueError:
                continue
            if tok[0] in gal:
                m = dict(zip(keys, vals))
                for k in ("T", "fD", "Q"):
                    m[k] = int(m[k])
                gal[tok[0]]["meta"] = m
    pos = {}
    with open(os.path.join(DATA, "sparc_lelli2016_table1_pos.tsv")) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            t = line.rstrip("\n").split("\t")
            if len(t) < 3:
                continue
            try:
                ra, dec = float(t[0]), float(t[1])
            except ValueError:
                continue
            pos[t[2].strip()] = (ra, dec)
    for nm, g in gal.items():
        if nm in pos:
            g["lb"] = radec_to_gal(*pos[nm])
            g["n"] = lb_to_vec(*g["lb"])
    return [gal[k] for k in sorted(gal)]


def select_points(g):
    Vb2 = g["Vgas"] * np.abs(g["Vgas"]) + 0.5 * g["Vdisk"] * np.abs(g["Vdisk"]) + 0.7 * g["Vbul"] * np.abs(g["Vbul"])
    return (g["Vobs"] > 0) & (g["eV"] > 0) & (Vb2 > 0)


def prep(g):
    m = select_points(g)
    p = dict(name=g["name"], R=g["R"][m], Vobs=g["Vobs"][m].copy(), eV=g["eV"][m],
             Vg2=(g["Vgas"] * np.abs(g["Vgas"]))[m], Vd2=(g["Vdisk"] * np.abs(g["Vdisk"]))[m],
             Vb2=(g["Vbul"] * np.abs(g["Vbul"]))[m], has_bul=bool(np.max(np.abs(g["Vbul"][m])) > 0),
             N=int(m.sum()), n=g.get("n"), lb=g.get("lb"))
    p.update({k: g["meta"][k] for k in ("D", "eD", "fD", "Inc", "eInc", "Q")})
    return p


def gfid(p, a0=1.0):
    """fiducial g_bar (SI), Upsilon_d = 0.5, Upsilon_b = 0.7"""
    return (p["Vg2"] + 0.5 * p["Vd2"] + 0.7 * p["Vb2"]) * 1e6 / (p["R"] * KPC)


def inject_point(p, Dinj, a0ref=1.13e-10, nu=nu_mono, form="mult"):
    """point-level injection: V_obs -> V_obs sqrt(nu(y')/nu(y)), a0' = a0ref (1 + D.n)  (or a0ref 10^(D.n))."""
    q = dict(p)
    n = p["n"]
    fac = (1.0 + float(np.dot(Dinj, n))) if form == "mult" else 10 ** float(np.dot(Dinj, n))
    y = gfid(p) / a0ref
    q["Vobs"] = p["Vobs"] * np.sqrt(nu(y / fac) / nu(y))
    return q


# ---------------------------------------------------------------------------------------------- profile engine
def make_cfg(step=0.01, nu="mono", prof=("Yd", "Yb", "D", "i"), sY=0.1, mD=1.0, mI=1.0, evsin=False, lo=-11.3, hi=-9.0):
    return dict(step=step, nu=nu, prof=tuple(prof), sY=sY, mD=mD, mI=mI, evsin=evsin, lo=lo, hi=hi)


def grid_of(cfg):
    n = int(round((cfg["hi"] - cfg["lo"]) / cfg["step"])) + 1
    return cfg["lo"] + cfg["step"] * np.arange(n)


def _model_V(p, th, la, nuf, act):
    """th = dict of nuisances; returns predicted velocity"""
    Vb2 = p["Vg2"] + 10 ** th["lYd"] * p["Vd2"] + 10 ** th["lYb"] * p["Vb2"]
    a0 = 10 ** la
    floor = 1e-14 * a0 * p["R"] * KPC / 1e6
    Vb2c = np.maximum(Vb2, floor)
    y = Vb2c * 1e6 / (p["R"] * KPC) / a0
    Vp2 = nuf(y) * Vb2c
    sd = math.sin(math.radians(th["ip"])) / math.sin(math.radians(p["Inc"]))
    return np.sqrt(Vp2) * math.sqrt(th["Dp"] / p["D"]) * sd


def _gal_profile(args):
    p, cfg = args
    grid = grid_of(cfg)
    nuf = KERNELS[cfg["nu"]]
    prof = cfg["prof"]
    th0 = dict(lYd=math.log10(0.5), lYb=math.log10(0.7), Dp=p["D"], ip=p["Inc"])
    act = []
    if "Yd" in prof:
        act.append("lYd")
    if "Yb" in prof and p["has_bul"]:
        act.append("lYb")
    if "D" in prof:
        act.append("Dp")
    if "i" in prof:
        act.append("ip")
    sig = dict(lYd=cfg["sY"], lYb=cfg["sY"], Dp=max(p["eD"] * cfg["mD"], 1e-6), ip=max(p["eInc"] * cfg["mI"], 1e-6))
    lb = dict(lYd=math.log10(0.05), lYb=math.log10(0.05), Dp=0.2 * p["D"], ip=5.0)
    ub = dict(lYd=math.log10(3.0), lYb=math.log10(3.0), Dp=3.0 * p["D"], ip=90.0)
    cen = dict(lYd=math.log10(0.5), lYb=math.log10(0.7), Dp=p["D"], ip=p["Inc"])
    ng = len(grid)
    chi_tot = np.empty(ng)
    chi_vel = np.empty(ng)
    thetas = np.empty((ng, 4))
    evs = p["eV"]

    def resid(x, la):
        th = dict(th0)
        for k, v in zip(act, x):
            th[k] = v
        Vp = _model_V(p, th, la, nuf, act)
        e = evs
        if cfg["evsin"]:
            e = evs * math.sin(math.radians(p["Inc"])) / math.sin(math.radians(th["ip"]))
        r = (p["Vobs"] - Vp) / e
        pri = [(th[k] - cen[k]) / sig[k] for k in act]
        return np.concatenate([r, pri]), th

    def fullres(x, la):
        return resid(x, la)[0]

    prev = None
    for k in range(ng):
        la = grid[k]
        if not act:
            r, th = resid(np.array([]), la)
            best = float(np.sum(r ** 2))
            bx = np.array([])
        else:
            x0s = [np.array([th0[a] for a in act])]
            if prev is not None:
                x0s.append(prev)
            best, bx = np.inf, None
            for x0 in x0s:
                try:
                    sol = least_squares(fullres, x0, args=(la,), bounds=([lb[a] for a in act], [ub[a] for a in act]),
                                        x_scale=np.array([sig[a] for a in act]), method="trf", xtol=1e-10, ftol=1e-10, gtol=1e-10)
                    c = 2 * sol.cost
                    if c < best:
                        best, bx = c, sol.x
                except Exception:
                    pass
            prev = bx
        r, th = resid(bx if act else np.array([]), la)
        nv = len(p["Vobs"])
        chi_tot[k] = best
        chi_vel[k] = float(np.sum(r[:nv] ** 2))
        thetas[k] = [th["lYd"], th["lYb"], th["Dp"], th["ip"]]
    return chi_tot, chi_vel, thetas


def _gal_profile_star(a):
    return _gal_profile(a)


def build_profiles(P, cfg, label=""):
    """P: list of prepped galaxies. Returns dict of arrays (Ngal x Ngrid)."""
    grid = grid_of(cfg)
    args = [(p, cfg) for p in P]
    if NPROC > 1:
        ctx = mp.get_context("fork")
        with ctx.Pool(NPROC) as pool:
            res = pool.map(_gal_profile_star, args, chunksize=2)
    else:
        res = [_gal_profile(a) for a in args]
    return dict(grid=grid, chi=np.array([r[0] for r in res]), chiv=np.array([r[1] for r in res]),
                theta=np.array([r[2] for r in res]), N=np.array([p["N"] for p in P]))


def birge(chi, N, mode="primary", chiv=None, cap=None):
    """scale factors s_i = max(1, chi2min/(N-1)) ; mode: primary (total incl. priors), vel (velocity part at argmin), dofN, none"""
    if mode == "none":
        return np.ones(len(N))
    k = np.argmin(chi, axis=1)
    cmin = chi[np.arange(len(N)), k]
    if mode == "vel":
        cmin = chiv[np.arange(len(N)), k]
    dof = N - 1 if mode != "dofN" else N
    s = np.maximum(1.0, cmin / dof)
    if cap is not None:
        s = np.minimum(s, cap)
    return s


def curve_halfwidth(grid, C):
    """half-width of the Delta chi2 = 1 interval of each row of C (linear crossing; grid edge if none)."""
    out = np.empty(len(C))
    best = np.empty(len(C))
    for i, c in enumerate(C):
        k = int(np.argmin(c))
        m = c[k]
        best[i] = grid[k]
        # parabolic refine of the minimum
        if 0 < k < len(c) - 1:
            a, b, d = c[k - 1], c[k], c[k + 1]
            den = a - 2 * b + d
            if den > 0:
                best[i] = grid[k] + 0.5 * (a - d) / den * (grid[1] - grid[0])
        thr = m + 1.0
        r = k
        while r < len(c) - 1 and c[r] < thr:
            r += 1
        if c[r] >= thr and r > k:
            xr = grid[r - 1] + (thr - c[r - 1]) / (c[r] - c[r - 1]) * (grid[r] - grid[r - 1])
        else:
            xr = grid[r]
        l = k
        while l > 0 and c[l] < thr:
            l -= 1
        if c[l] >= thr and l < k:
            xl = grid[l] + (thr - c[l]) / (c[l + 1] - c[l]) * (grid[l + 1] - grid[l])
        else:
            xl = grid[l]
        out[i] = 0.5 * (xr - xl)
    return out, best


# ---------------------------------------------------------------------------------------------- dipole fit on curves
class Curves:
    """per-galaxy chi2_i(x) as piecewise cubics on a uniform grid; vectorised evaluation with value and slope; linear
    extrapolation of the edge slope outside the grid."""

    def __init__(self, grid, C=None, coefs=None):
        self.g0 = float(grid[0])
        self.h = float(grid[1] - grid[0])
        self.n = len(grid)
        self.grid = np.asarray(grid)
        if coefs is None:
            cs = CubicSpline(grid, C, axis=1)
            c = cs.c  # (4, n-1, Ngal)
            self.c = [np.ascontiguousarray(c[k].T) for k in range(4)]
        else:
            self.c = coefs
        self.N = self.c[0].shape[0]
        self.nseg = self.n - 1
        self.idx = np.arange(self.N)
        self._edges()

    def _edges(self):
        self.fL = self.c[3][:, 0]
        self.sL = self.c[2][:, 0]
        a, b, c, d = (self.c[k][:, -1] for k in range(4))
        hh = self.h
        self.fR = ((a * hh + b) * hh + c) * hh + d
        self.sR = (3 * a * hh + 2 * b) * hh + c

    @staticmethod
    def quad(grid, m, sig):
        """exact piecewise coefficients of f_i(x) = (x - m_i)^2 / sig_i^2"""
        g = np.asarray(grid)[:-1][None, :]
        m = np.asarray(m)[:, None]
        w = 1.0 / np.asarray(sig)[:, None] ** 2
        zero = np.zeros((len(m), len(g[0])))
        return Curves(grid, coefs=[zero, np.broadcast_to(w, zero.shape).copy(), 2 * (g - m) * w, (g - m) ** 2 * w])

    def sub(self, ix):
        c = Curves.__new__(Curves)
        c.g0, c.h, c.n, c.grid, c.nseg = self.g0, self.h, self.n, self.grid, self.nseg
        c.c = [a[ix] for a in self.c]
        c.N = len(ix)
        c.idx = np.arange(c.N)
        c._edges()
        return c

    def ev(self, x):
        gN = self.g0 + self.h * self.nseg
        xc = np.clip(x, self.g0, gN)
        j = np.minimum(((xc - self.g0) / self.h).astype(np.int64), self.nseg - 1)
        t = xc - (self.g0 + j * self.h)
        a, b, c, d = (self.c[k][self.idx, j] for k in range(4))
        f = ((a * t + b) * t + c) * t + d
        fp = (3 * a * t + 2 * b) * t + c
        lo = x < self.g0
        hi = x > gN
        if lo.any():
            f = np.where(lo, self.fL + self.sL * (x - self.g0), f)
            fp = np.where(lo, self.sL, fp)
        if hi.any():
            f = np.where(hi, self.fR + self.sR * (x - gN), f)
            fp = np.where(hi, self.sR, fp)
        return f, fp

    def clamped(self, x):
        return int(np.sum((x < self.g0) | (x > self.g0 + self.h * self.nseg)))


DMAX = 0.95


def _xdip(la, D, n, form):
    if form == "mult":
        return la + np.log10(np.maximum(1.0 + n @ D, 1e-3))
    return la + n @ D


def _obj_raw(q, cv, n, form, shift):
    """q = (la, D1, D2, D3): F and gradient wrt q"""
    la, D = q[0], q[1:]
    x = _xdip(la, D, n, form)
    if shift is not None:
        x = x - shift
    f, fp = cv.ev(x)
    if form == "mult":
        dxdD = n / (np.maximum(1.0 + n @ D, 1e-3) * LN10)[:, None]
    else:
        dxdD = n
    g = np.concatenate([[fp.sum()], (fp[:, None] * dxdD).sum(0)])
    return float(f.sum()), g


def _u2D(u):
    return DMAX * u / math.sqrt(1.0 + float(u @ u))


def _obj_u(p, cv, n, form, shift):
    la, u = p[0], p[1:]
    r2 = float(u @ u)
    s = math.sqrt(1.0 + r2)
    D = DMAX * u / s
    F, g = _obj_raw(np.concatenate([[la], D]), cv, n, form, shift)
    J = DMAX * (np.eye(3) / s - np.outer(u, u) / s ** 3)
    return F, np.concatenate([[g[0]], J.T @ g[1:]])


_STARTS = [np.zeros(3)] + [0.3 * np.array(v) for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]


def _la_start(cv, shift=None):
    # best common la at D = 0 by a coarse scan on the grid
    xs = cv.grid
    tot = np.array([cv.ev(np.full(cv.N, x) - (0 if shift is None else shift))[0].sum() for x in xs[::5]])
    return float(xs[::5][int(np.argmin(tot))])


def fit_dipole(cv, n, starts=1, form="mult", shift=None, extra_start=None, la0=None):
    """free-direction dipole fit. Returns dict(la, D, A, F, l, b)."""
    if la0 is None:
        la0 = _la_start(cv, shift)
    best = None
    sts = [np.concatenate([[la0], s]) for s in _STARTS[:starts]]
    if extra_start is not None:
        sts.append(extra_start)
    for p0 in sts:
        r = minimize(_obj_u, p0, args=(cv, n, form, shift), jac=True, method="L-BFGS-B",
                     options=dict(maxiter=300, ftol=1e-15, gtol=1e-10, maxcor=20))
        if best is None or r.fun < best.fun:
            best = r
    D = _u2D(best.x[1:])
    A = float(np.linalg.norm(D))
    out = dict(la=float(best.x[0]), D=D, A=A, F=float(best.fun), u=best.x.copy())
    return out


def F0_fit(cv, shift=None):
    """A = 0 fit (la only)"""
    r = minimize(lambda t: tuple(_f0(t, cv, shift)), [_la_start(cv, shift)], jac=True, method="L-BFGS-B",
                 options=dict(ftol=1e-15, gtol=1e-10))
    return float(r.fun), float(r.x[0])


def _f0(t, cv, shift):
    x = np.full(cv.N, t[0])
    if shift is not None:
        x = x - shift
    f, fp = cv.ev(x)
    return float(f.sum()), np.array([fp.sum()])


def fit_fixed(cv, n, d, form="mult", shift=None, la0=None):
    """fixed-direction amplitude fit: D = s d ; returns dict(la, s, F)"""
    d = np.asarray(d, float) / np.linalg.norm(d)
    if la0 is None:
        la0 = _la_start(cv, shift)

    def obj(p):
        F, g = _obj_raw(np.concatenate([[p[0]], p[1] * d]), cv, n, form, shift)
        return F, np.array([g[0], g[1:] @ d])
    r = minimize(obj, [la0, 0.0], jac=True, method="L-BFGS-B", bounds=[(-13, -7), (-DMAX, DMAX)],
                 options=dict(ftol=1e-15, gtol=1e-10))
    return dict(la=float(r.x[0]), s=float(r.x[1]), F=float(r.fun))


def hessian_raw(cv, n, la, D, form="mult", e=1e-5):
    """Hessian of F wrt (la, D) by central differences of the analytic gradient."""
    q0 = np.concatenate([[la], D])
    H = np.zeros((4, 4))
    for k in range(4):
        qp, qm = q0.copy(), q0.copy()
        qp[k] += e
        qm[k] -= e
        H[:, k] = (_obj_raw(qp, cv, n, form, None)[1] - _obj_raw(qm, cv, n, form, None)[1]) / (2 * e)
    return 0.5 * (H + H.T)


def fisher_cov(cv, n, fit, form="mult"):
    H = hessian_raw(cv, n, fit["la"], fit["D"], form)
    C = 2.0 * np.linalg.inv(H)
    return C  # (la, D) covariance in chi2 units (Delta chi2 = 1 <-> 1 sigma)


# ---------------------------------------------------------------------------------------------- statistics helpers
def cone(dirs, best, q):
    """angle containing fraction q of the directions about `best`"""
    a = np.degrees(np.arccos(np.clip(np.einsum('ij,j->i', dirs, best / np.linalg.norm(best)), -1, 1)))
    return float(np.quantile(a, q))


def pval(null, obs):
    null = np.asarray(null)
    return (1.0 + np.sum(null >= obs)) / (1.0 + len(null))


def spawn(seed, name_index, n):
    return np.random.SeedSequence([seed, name_index]).spawn(n)


def pmap(fn, arglist):
    """ordered parallel map (fork); deterministic given the args"""
    if NPROC <= 1:
        return [fn(a) for a in arglist]
    ctx = mp.get_context("fork")
    with ctx.Pool(NPROC) as pool:
        return pool.map(fn, arglist, chunksize=1)


# ---------------------------------------------------------------------------------------------- permutations
def unit_positions(n_all, uma_mask):
    """block scheme: units = each non-UMa galaxy + one UMa block carrying the mean UMa position"""
    single = np.where(~uma_mask)[0]
    upos = [n_all[i] for i in single]
    if uma_mask.any():
        m = n_all[uma_mask].mean(0)
        upos.append(m / np.linalg.norm(m))
    return single, np.array(upos)


def perm_positions(rng, n_all, uma_mask, scheme):
    N = len(n_all)
    if scheme == "simple" or not uma_mask.any():
        return n_all[rng.permutation(N)]
    single, upos = unit_positions(n_all, uma_mask)
    pi = rng.permutation(len(upos))
    out = np.empty_like(n_all)
    out[single] = upos[pi[:len(single)]]
    out[uma_mask] = upos[pi[len(single)]]
    return out


# ---------------------------------------------------------------------------------------------- hemisphere scan
def fib_sphere(n):
    i = np.arange(n) + 0.5
    z = 1 - 2 * i / n
    r = np.sqrt(1 - z * z)
    ph = math.pi * (1 + 5 ** 0.5) * i
    return np.stack([r * np.cos(ph), r * np.sin(ph), z], 1)


AXES = fib_sphere(3072)


def _min_refine(S, grid):
    """min over grid (last axis) with parabolic refinement -> location"""
    k = np.argmin(S, axis=-1)
    kk = np.clip(k, 1, S.shape[-1] - 2)
    r = np.arange(S.shape[0])
    a, b, d = S[r, kk - 1], S[r, kk], S[r, kk + 1]
    den = a - 2 * b + d
    off = np.where(den > 0, 0.5 * (a - d) / np.where(den > 0, den, 1), 0.0)
    off = np.clip(off, -1, 1)
    h = grid[1] - grid[0]
    return grid[kk] + off * h, k


def hemi_H(C, grid, n, axes=AXES, minn=10):
    """hemisphere anisotropy H = 2 (aN - aS)/(aN + aS) for each axis; NaN where < minn galaxies in a hemisphere.
    In the parent process the einsum path is used (Accelerate matmul in the parent followed by fork() deadlocks the children)."""
    if mp.current_process().name == "MainProcess":
        return hemi_H_einsum(C, grid, n, axes, minn)
    with np.errstate(all="ignore"):
        M = (n @ axes.T > 0).T.astype(float)  # (axes, gal)
        cnt = M.sum(1)
        SN = M @ C
    SS = C.sum(0)[None, :] - SN
    xN, _ = _min_refine(SN, grid)
    xS, _ = _min_refine(SS, grid)
    aN, aS = 10 ** xN, 10 ** xS
    H = 2 * (aN - aS) / (aN + aS)
    ok = (cnt >= minn) & (len(n) - cnt >= minn)
    return np.where(ok, H, np.nan)


def hemi_H_einsum(C, grid, n, axes=AXES, minn=10):
    """same as hemi_H with einsum (no BLAS) -- cross-check of the Accelerate matmul"""
    M = (np.einsum("gk,ak->ag", n, axes) > 0).astype(float)
    cnt = M.sum(1)
    SN = np.einsum("ag,gk->ak", M, C)
    SS = C.sum(0)[None, :] - SN
    xN, _ = _min_refine(SN, grid)
    xS, _ = _min_refine(SS, grid)
    aN, aS = 10 ** xN, 10 ** xS
    H = 2 * (aN - aS) / (aN + aS)
    ok = (cnt >= minn) & (len(n) - cnt >= minn)
    return np.where(ok, H, np.nan)


def hemi_H_axis(C, grid, n, axis):
    M = (n @ axis > 0).astype(float)
    if M.sum() < 1 or (1 - M).sum() < 1:
        return np.nan
    SN = (M[:, None] * C).sum(0)
    SS = C.sum(0) - SN
    xN, _ = _min_refine(SN[None, :], grid)
    xS, _ = _min_refine(SS[None, :], grid)
    aN, aS = 10 ** xN[0], 10 ** xS[0]
    return float(2 * (aN - aS) / (aN + aS))


# ---------------------------------------------------------------------------------------------- parallel workers (fork; globals in _W)
_W = {}


def setW(**kw):
    _W.clear()
    _W.update(kw)


def _rng_of(ss):
    return np.random.default_rng(ss)


def _w_perm(a):
    ss, nper, scheme, form, starts, hemi = a
    rng = _rng_of(ss)
    cv, n, uma, la0 = _W["cv"], _W["n"], _W["uma"], _W["la0"]
    A = np.empty(nper)
    F = np.empty(nper)
    D = np.empty((nper, 3))
    H = np.full((nper, 2), np.nan)
    for k in range(nper):
        npos = perm_positions(rng, n, uma, scheme)
        r = fit_dipole(cv, npos, starts=starts, form=form, la0=la0)
        A[k], F[k], D[k] = r["A"], r["F"], r["D"]
        if hemi:
            Hs = hemi_H(_W["C"], _W["grid"], npos)
            H[k, 0] = np.nanmax(Hs)
            H[k, 1] = hemi_H_axis(_W["C"], _W["grid"], npos, DIRS["Zhou"])
    return A, F, D, H


def run_perms(cv, n, uma, C, grid, la0, scheme, seed, idx, N, chunk=100, form="mult", starts=1, hemi=False):
    setW(cv=cv, n=n, uma=uma, la0=la0, C=C, grid=grid)
    nch = N // chunk
    ss = np.random.SeedSequence([seed, idx]).spawn(nch)
    res = pmap(_w_perm, [(ss[c], chunk, scheme, form, starts, hemi) for c in range(nch)])
    return (np.concatenate([r[0] for r in res]), np.concatenate([r[1] for r in res]),
            np.concatenate([r[2] for r in res]), np.concatenate([r[3] for r in res]))


def _w_boot(a):
    ss, nb, ix, fixdir, extra, form = a
    rng = _rng_of(ss)
    cv, n, la0 = _W["cv"], _W["n"], _W["la0"]
    out = np.empty((nb, 3))
    amp = np.empty(nb)
    for k in range(nb):
        ib = rng.choice(ix, size=len(ix), replace=True)
        cb, nbb = cv.sub(ib), n[ib]
        if fixdir is None:
            r = fit_dipole(cb, nbb, starts=1, form=form, extra_start=extra, la0=la0)
            out[k], amp[k] = r["D"], r["A"]
        else:
            r = fit_fixed(cb, nbb, fixdir, form=form, la0=la0)
            amp[k] = r["s"]
            out[k] = r["s"] * fixdir
    return out, amp


def run_boot(cv, n, la0, ix, seed, idx, N, chunk=50, fixdir=None, extra=None, form="mult"):
    setW(cv=cv, n=n, la0=la0)
    nch = max(1, N // chunk)
    ss = np.random.SeedSequence([seed, idx]).spawn(nch)
    res = pmap(_w_boot, [(ss[c], N // nch, ix, fixdir, extra, form) for c in range(nch)])
    return np.concatenate([r[0] for r in res]), np.concatenate([r[1] for r in res])


def _w_inj(a):
    """injection trials. scheme None: real positions; else position-permuted. dirs: (ntr,3) array of injection directions."""
    ss, dirs, Ainj, scheme, form_inj, form_fit, starts = a
    rng = _rng_of(ss)
    cv, n, uma, la0 = _W["cv"], _W["n"], _W["uma"], _W["la0"]
    nt = len(dirs)
    Dh = np.empty((nt, 3))
    Ah = np.empty(nt)
    for k in range(nt):
        npos = n if scheme is None else perm_positions(rng, n, uma, scheme)
        Dinj = Ainj * dirs[k]
        sh = np.log10(1.0 + npos @ Dinj) if form_inj == "mult" else npos @ Dinj
        r = fit_dipole(cv, npos, starts=starts, form=form_fit, shift=sh, la0=la0 + float(sh.mean()))
        Dh[k], Ah[k] = r["D"], r["A"]
    return Dh, Ah


def run_inj(cv, n, uma, la0, scheme, seed, idx, dirs, Ainj, chunk=125, form_inj="mult", form_fit="mult", starts=1):
    setW(cv=cv, n=n, uma=uma, la0=la0)
    nt = len(dirs)
    nch = max(1, int(math.ceil(nt / chunk)))
    ss = np.random.SeedSequence([seed, idx]).spawn(nch)
    parts = [(ss[c], dirs[c * chunk:(c + 1) * chunk], Ainj, scheme, form_inj, form_fit, starts) for c in range(nch)]
    res = pmap(_w_inj, parts)
    return np.concatenate([r[0] for r in res]), np.concatenate([r[1] for r in res])


def _w_neyman(a):
    ss, Ainj, ntr, scheme, form = a
    rng = _rng_of(ss)
    cv, n, uma, la0 = _W["cv"], _W["n"], _W["uma"], _W["la0"]
    out = np.empty(ntr)
    for k in range(ntr):
        d = rand_dirs(rng, 1)[0]
        npos = perm_positions(rng, n, uma, scheme)
        sh = np.log10(1.0 + npos @ (Ainj * d))
        r = fit_dipole(cv, npos, starts=1, form=form, shift=sh, la0=la0 + float(sh.mean()))
        out[k] = r["A"]
    return out


def neyman_table(cv, n, uma, la0, scheme, seed, agrid, ntr=1000, chunk=250, form="mult"):
    setW(cv=cv, n=n, uma=uma, la0=la0)
    tasks = []
    for ia, A in enumerate(agrid):
        ss = np.random.SeedSequence([seed, ia]).spawn(ntr // chunk)
        tasks += [(ss[c], float(A), chunk, scheme, form) for c in range(ntr // chunk)]
    res = pmap(_w_neyman, tasks)
    per = ntr // chunk
    return np.array([np.concatenate(res[i * per:(i + 1) * per]) for i in range(len(agrid))])  # (nA, ntr)


def a95_from_table(T, agrid, obs):
    P = (T >= obs).mean(1)
    ok = np.where(P >= 0.95)[0]
    return (float(agrid[ok[0]]) if len(ok) else float("nan")), P


# ---------------------------------------------------------------------------------------------- data bundle from a profile npz
def load_bundle(path, birge_mode="primary", sel="primary", cap=None):
    z = np.load(path, allow_pickle=False)
    d = {k: z[k] for k in z.files}
    m = np.ones(len(d["N"]), bool)
    if sel == "primary":
        m = (d["Q"] <= 2) & (d["Inc"] >= 30)
    d["mask"] = m
    d["s"] = birge(d["chi"], d["N"], birge_mode, d["chiv"], cap)
    return d


def sub_bundle(d, m):
    """restrict to galaxies m (bool over all usable): returns Curves (Birge-scaled), positions, meta arrays, C (scaled) """
    ix = np.where(m)[0]
    C = d["chi"][ix] / d["s"][ix][:, None]
    cv = Curves(d["grid"], C)
    return dict(cv=cv, n=d["n"][ix], C=C, grid=d["grid"], fD=d["fD"][ix], Inc=d["Inc"][ix], D=d["D"][ix], eD=d["eD"][ix], N=d["N"][ix],
                names=d["names"][ix], ix=ix, s=d["s"][ix], uma=(d["fD"][ix] == 4))


# ---------------------------------------------------------------------------------------------- one-call variant statistics
def dip_stats(cv, n, uma, C, grid, idx, nperm=1000, nboot=500, seed_p=19201, seed_b=19203, hemi=False, form="mult", fisher=True):
    """A, direction, Fisher, bootstrap sigma, permutation p (simple) for one curve set."""
    F0, la0 = F0_fit(cv)
    fit = fit_dipole(cv, n, starts=5, form=form)
    out = dict(N=cv.N, la0=la0, A=fit["A"], D=fit["D"], lb=vec_to_lb(fit["D"]), dchi=F0 - fit["F"], la=fit["la"])
    if fisher:
        try:
            Cf = fisher_cov(cv, n, fit, form)
            out["fisher_rms"] = float(math.sqrt(np.trace(Cf[1:, 1:]) / 3))
            out["Cf"] = Cf
        except np.linalg.LinAlgError:
            out["fisher_rms"] = float("nan")
    if nperm:
        A, F, D, H = run_perms(cv, n, uma, C, grid, la0, "simple", seed_p, idx, nperm, chunk=max(1, nperm // 20 if nperm >= 200 else nperm), form=form, hemi=hemi)
        out["p"] = pval(A, fit["A"])
        out["null_med"] = float(np.median(A))
        out["null_A"] = A
        out["null_D"] = D
        out["null_H"] = H
    if nboot:
        Db, Ab = run_boot(cv, n, la0, np.arange(cv.N), seed_b, idx, nboot, chunk=max(1, nboot // 10), extra=fit["u"], form=form)
        out["sig_std"] = float(np.std(Ab, ddof=1))
        out["sig_comp"] = float(math.sqrt(np.trace(np.cov(Db.T)) / 3))
        dirs = Db / np.linalg.norm(Db, axis=1, keepdims=True)
        out["cone68"], out["cone95"] = cone(dirs, fit["D"], .68), cone(dirs, fit["D"], .95)
    return out


def fmt_stats(o, name=""):
    s = f"{name:34s} N={o['N']:3d} A={o['A']:.3f} ({o['lb'][0]:.0f},{o['lb'][1]:+.0f}) dchi2={o['dchi']:5.1f}"
    if "fisher_rms" in o:
        s += f" Fis={o['fisher_rms']:.3f}"
    if "sig_comp" in o:
        s += f" sig(std/comp)={o['sig_std']:.3f}/{o['sig_comp']:.3f}"
    if "p" in o:
        s += f" p={o['p']:.3f} nullmed={o['null_med']:.3f}"
    return s


def _call_fn(a):
    return _W["_fn"](a)


def pmap_local(fn, arglist):
    """parallel map of a local (closure) function via fork; results in argument order"""
    _W["_fn"] = fn
    if NPROC <= 1:
        return [fn(a) for a in arglist]
    ctx = mp.get_context("fork")
    with ctx.Pool(NPROC) as pool:
        return pool.map(_call_fn, arglist, chunksize=1)
