#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cfg182_common -- shared machinery for lane CFG182 (is SPARC's acceleration scale direction-dependent on the sky?).

Nothing here is a result.  It holds:
  * the run harness (tee to this lane's own .out, named checks with a load-bearing flag, results JSON, outputs named by
    mode: MUTATE=1 writes *_MUTATE.*);
  * the SPARC loader (CFG4_common.load_sparc, read-only import) and the kernels (nu_mono and P2 from CFG4_common, which
    exec's FP1's committed nu_mono read-only; the "simple" kernel defined here);
  * sky positions from the VizieR copy of Lelli et al. 2016 table 1 (real_research/data/sparc_lelli2016_table1_pos.tsv),
    converted to Galactic with astropy, cross-checked against real_research/data/sparc_cosmicweb_match.csv;
  * the per-galaxy PROFILE likelihood: at each log10 a0 on a fixed grid the nuisances (Upsilon_disk, Upsilon_bul, distance,
    inclination; Li, McGaugh & Lelli 2018 priors) are minimised, giving chi2_i(log a0);
  * the curve machinery: Catmull-Rom interpolation of the per-galaxy curves, the global fit of a template model
    x_i = L + sum_k beta_k Z_ik + log10(1 + T_i . theta) (the dipole is T_i = n_i), fixed-direction fits, permutations,
    bootstraps, hemisphere scans.

kappa = 1/2 stays FITTED; a0 is fitted in this lane (a0_bar free).  Run nothing from here directly.
"""
import os
import sys
import json
import math
import time
import builtins

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.optimize import least_squares, minimize

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
REPO = os.path.dirname(CFGDIR)
DATA = os.path.join(REPO, "real_research", "data")
MUTATE = os.environ.get("MUTATE", "0") == "1"
sys.path.insert(0, CFGDIR)
import CFG4_common as C4                                     # read-only: loader + kernels (nothing written on import)

KPC_M = 3.0857e19
LN10 = math.log(10.0)
H0_SPARC = 73.0                                              # SPARC's Hubble-flow convention (km/s/Mpc)
A0_REF = 1.2e-10                                             # MUTATE injection reference only (declared)
UPS_D0, UPS_B0, UPS_SIG = 0.5, 0.7, 0.1                      # LML 2018 priors (log-normal, 0.1 dex)
GRID = np.round(np.arange(-11.30, -8.9999, 0.01), 2)         # log10 a0 grid of the profile curves


# ------------------------------------------------------------------------------------------------ harness
class Run:
    def __init__(self, slug):
        self.slug = slug
        self.mutate = MUTATE
        suf = "_MUTATE" if MUTATE else ""
        self.suf = suf
        self.out_path = os.path.join(HERE, f"{slug}{suf}.out")
        self.json_path = os.path.join(HERE, f"{slug}_results{suf}.json")
        self._f = builtins.open(self.out_path, "w", encoding="utf-8")
        self._stdout = sys.stdout
        sys.stdout = self
        self.t0 = time.time()
        self.OUT = {"lane": "CFG182", "script": slug, "mutate": MUTATE, "checks": {}, "numbers": {}}
        self.CH = []

    def write(self, t):
        self._stdout.write(t)
        self._f.write(t)

    def flush(self):
        self._stdout.flush()
        self._f.flush()

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)

    def el(self):
        return f"[{time.time() - self.t0:.0f} s]"

    def check(self, name, measured, ok, load_bearing=True, reading=""):
        ok = bool(ok)
        key = name.split()[0]
        k2, j = key, 1
        while k2 in self.OUT["checks"]:
            j += 1
            k2 = f"{key}#{j}"
        self.CH.append((k2, ok, load_bearing))
        self.OUT["checks"][k2] = {"ok": ok, "load_bearing": load_bearing, "measured": str(measured), "name": name}
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def num(self, key, value):
        self.OUT["numbers"][key] = jclean(value)
        return value

    def finish(self):
        npass = sum(1 for _, ok, _ in self.CH if ok)
        nlb = sum(1 for _, ok, lb in self.CH if (not ok) and lb)
        self.OUT["summary"] = {"n_checks": len(self.CH), "n_pass": npass, "load_bearing_failures": nlb,
                               "failed": [k for k, ok, _ in self.CH if not ok], "seconds": round(time.time() - self.t0, 1)}
        with builtins.open(self.json_path, "w", encoding="utf-8") as fh:
            json.dump(jclean(self.OUT), fh, indent=1)
        self.P(f"\n  {npass}/{len(self.CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(self.json_path)} "
               f"({time.time() - self.t0:.0f} s)")
        rc = 1 if nlb else 0
        self.P(f"rc = {rc}")
        sys.stdout = self._stdout
        self._f.close()
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
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return str(o)
    return o


# ------------------------------------------------------------------------------------------------ kernels
def nu_simple(y):
    """the 'simple' kernel 1/2 + sqrt(1/4 + 1/y) (the door-11 text's 'P2')."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


KERNELS = {"nu_mono": C4.nu_mono, "P2": C4.nu_p2, "simple": nu_simple}


def dlnnu_dlny(nuf, y, h=1e-4):
    return (np.log(nuf(y * math.exp(h))) - np.log(nuf(y * math.exp(-h)))) / (2 * h)


# ------------------------------------------------------------------------------------------------ geometry
def unitvec(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    return np.stack([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)], axis=-1)


def lb_of(v):
    v = np.asarray(v, float)
    v = v / np.linalg.norm(v)
    return float(np.degrees(np.arctan2(v[1], v[0])) % 360.0), float(np.degrees(np.arcsin(np.clip(v[2], -1, 1))))


def angle_deg(u, v):
    u = np.asarray(u, float) / np.linalg.norm(u)
    v = np.asarray(v, float) / np.linalg.norm(v)
    return float(np.degrees(np.arccos(np.clip(u @ v, -1, 1))))


def random_unit(rng, n=None):
    z = rng.uniform(-1, 1, n)
    phi = rng.uniform(0, 2 * np.pi, n)
    s = np.sqrt(1 - z ** 2)
    return np.stack([s * np.cos(phi), s * np.sin(phi), z], axis=-1)


# ------------------------------------------------------------------------------------------------ data
def load_positions():
    """VizieR J/AJ/152/157 table 1 (J2000) -> Galactic (l, b) with astropy; name -> (ra, dec, l, b)."""
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    rows = {}
    for line in builtins.open(os.path.join(DATA, "sparc_lelli2016_table1_pos.tsv")):
        if line.startswith("#"):
            continue
        tok = line.rstrip("\n").split("\t")
        if len(tok) < 5:
            continue
        try:
            ra, de = float(tok[0]), float(tok[1])
        except ValueError:
            continue
        rows[tok[2].strip()] = (ra, de)
    names = list(rows)
    ra = np.array([rows[n][0] for n in names])
    de = np.array([rows[n][1] for n in names])
    g = SkyCoord(ra=ra * u.deg, dec=de * u.deg, frame="fk5", equinox="J2000").galactic
    return {n: (ra[i], de[i], float(g.l.deg[i]), float(g.b.deg[i])) for i, n in enumerate(names)}


def load_cosmicweb():
    import csv
    out = {}
    with builtins.open(os.path.join(DATA, "sparc_cosmicweb_match.csv")) as fh:
        for r in csv.DictReader(fh):
            out[r["name"]] = r
    return out


def load_galaxies():
    """SPARC rotation curves + master table + positions; usable points and per-galaxy flags (no selection applied)."""
    gal = C4.load_sparc()
    pos = load_positions()
    out = []
    for g in gal:
        m = g["meta"]
        if m is None or g["name"] not in pos:
            continue
        R, V, eV, Vg, Vd, Vb = g["R"], g["Vobs"], g["eV"], g["Vgas"], g["Vdisk"], g["Vbul"]
        Vbar2_fid = Vg * np.abs(Vg) + UPS_D0 * Vd ** 2 + UPS_B0 * Vb ** 2
        ok = (V > 0) & (eV > 0) & (R > 0) & (Vbar2_fid > 0) & np.isfinite(V + eV + Vbar2_fid)
        ra, de, l, b = pos[g["name"]]
        out.append(dict(name=g["name"], R=R[ok], V=V[ok], eV=eV[ok], Vg=Vg[ok], Vd=Vd[ok], Vb=Vb[ok], npt=int(ok.sum()),
                        D=m["D"], eD=m["eD"], fD=m["fD"], Inc=m["Inc"], eInc=m["eInc"], Q=m["Q"], ra=ra, dec=de, l=l, b=b,
                        n=unitvec(l, b), clean=bool(m["Q"] <= 2 and m["Inc"] >= 30.0 and ok.sum() >= 5),
                        usable=bool(ok.sum() >= 5), has_bul=bool(np.any(Vb[ok] > 0))))
    return out


# ------------------------------------------------------------------------------------------------ the per-galaxy profile
def _model(p, g, a0, nuf):
    ud, ub, tD, ti = p
    Yd = UPS_D0 * 10 ** (UPS_SIG * ud)
    Yb = UPS_B0 * 10 ** (UPS_SIG * ub)
    S = g["Vg"] * np.abs(g["Vg"]) + Yd * g["Vd"] ** 2 + Yb * g["Vb"] ** 2
    S = np.maximum(S, 1e-6)
    k = 1e6 / (g["R"] * KPC_M)
    y = S * k / a0
    nu = nuf(y)
    F = nu * S
    rD = 1.0 + (g["eD"] / g["D"]) * tD
    inc0 = math.radians(g["Inc"])
    inc1 = math.radians(g["Inc"] + g["eInc"] * ti)
    si = math.sin(inc1) / math.sin(inc0)
    V = np.sqrt(F * rD) * si
    return V, S, y, nu, F, rD, inc1, Yd, Yb


def _resid(p, g, a0, nuf, V_obs):
    V = _model(p, g, a0, nuf)[0]
    return np.concatenate([(V_obs - V) / g["eV"], p])


def _jac(p, g, a0, nuf, V_obs):
    V, S, y, nu, F, rD, inc1, Yd, Yb = _model(p, g, a0, nuf)
    dlog = dlnnu_dlny(nuf, y)
    dFdS = nu * (1.0 + dlog)                                  # d(nu S)/dS = nu + y nu'
    fac = V / (2.0 * F) * dFdS
    J = np.zeros((len(V) + 4, 4))
    J[:len(V), 0] = -fac * g["Vd"] ** 2 * Yd * UPS_SIG * LN10 / g["eV"]
    J[:len(V), 1] = -fac * g["Vb"] ** 2 * Yb * UPS_SIG * LN10 / g["eV"]
    J[:len(V), 2] = -V / (2.0 * rD) * (g["eD"] / g["D"]) / g["eV"]
    J[:len(V), 3] = -V * (math.cos(inc1) / math.sin(inc1)) * math.radians(g["eInc"]) / g["eV"]
    J[len(V):, :] = np.eye(4)
    return J


def _bounds(g):
    tDlo = max(-8.0, -0.7 * g["D"] / g["eD"])
    ilo = max(g["Inc"] - 8 * g["eInc"], 5.0)
    ihi = min(g["Inc"] + 8 * g["eInc"], 90.0)
    tilo = (ilo - g["Inc"]) / g["eInc"] if g["eInc"] > 0 else -1e-9
    tihi = (ihi - g["Inc"]) / g["eInc"] if g["eInc"] > 0 else 1e-9
    return np.array([-10.0, -10.0, tDlo, min(tilo, -1e-9)]), np.array([10.0, 10.0, 8.0, max(tihi, 1e-9)])


def profile_galaxy(args):
    """chi2_i(log a0) on the grid, nuisances profiled with warm starts outward from log a0 = -9.92."""
    g, kname, grid, V_obs = args
    nuf = KERNELS[kname]
    V_obs = g["V"] if V_obs is None else V_obs
    lo, hi = _bounds(g)
    if g["eInc"] <= 0:
        lo[3], hi[3] = -1e-9, 1e-9
    G = len(grid)
    chi = np.full(G, np.nan)
    par = np.full((G, 4), np.nan)
    j0 = int(np.argmin(np.abs(grid - (-9.92))))
    order = [list(range(j0, G)), list(range(j0 - 1, -1, -1))]
    for seq in order:
        p = np.zeros(4)
        if seq and seq[0] != j0 and np.all(np.isfinite(par[j0])):
            p = par[j0].copy()
        for j in seq:
            a0 = 10 ** grid[j]
            p = np.clip(p, lo + 1e-9, hi - 1e-9)
            best = None
            for p_start in ((p,) if j != j0 else (p, np.array([0.0, 0.0, 0.0, 0.0]))):
                r = least_squares(_resid, p_start, jac=_jac, bounds=(lo, hi), args=(g, a0, nuf, V_obs), method="trf",
                                  xtol=1e-10, ftol=1e-10, gtol=1e-10, max_nfev=200)
                if best is None or r.cost < best.cost:
                    best = r
            chi[j] = 2.0 * best.cost
            par[j] = best.x
            p = best.x
    return chi, par


def compute_profiles(gals, kname, grid=GRID, V_override=None, nproc=14):
    """run profile_galaxy over all galaxies in a process pool; returns chi (N, G), par (N, G, 4)."""
    import multiprocessing as mp
    args = [(g, kname, grid, None if V_override is None else V_override[i]) for i, g in enumerate(gals)]
    ctx = mp.get_context("fork")
    with ctx.Pool(nproc) as pool:
        res = pool.map(profile_galaxy, args, chunksize=1)
    return np.array([r[0] for r in res]), np.array([r[1] for r in res])


def model_velocity(g, p, a0, kname):
    return _model(np.asarray(p, float), g, a0, KERNELS[kname])[0]


# ------------------------------------------------------------------------------------------------ curve machinery
class Curves:
    """per-galaxy scaled profile curves c_i(x) on a uniform grid; Catmull-Rom interpolation, linear beyond the edges."""

    def __init__(self, grid, chi, npt=None, birge=True):
        self.x0 = float(grid[0])
        self.h = float(grid[1] - grid[0])
        self.G = len(grid)
        self.grid = np.asarray(grid, float)
        chi = np.asarray(chi, float)
        self.chimin = np.nanmin(chi, axis=1)
        if npt is not None and birge:
            dof = np.maximum(np.asarray(npt) - 1, 1)
            self.s = np.maximum(1.0, self.chimin / dof)
        else:
            self.s = np.ones(len(chi))
        self.C = (chi - self.chimin[:, None]) / self.s[:, None]
        self.N = len(chi)
        self.xhat = self.grid[np.nanargmin(self.C, axis=1)]
        self.sig = self.halfwidths()

    def subset(self, idx):
        c = Curves.__new__(Curves)
        c.__dict__.update(self.__dict__)
        c.C, c.chimin, c.s, c.xhat, c.sig = self.C[idx], self.chimin[idx], self.s[idx], self.xhat[idx], self.sig[idx]
        c.N = len(idx)
        return c

    def halfwidths(self):
        """Delta chi2 = 1 half-width of each (scaled) curve, averaged over the two sides (capped at 1 dex)."""
        out = np.zeros(self.N)
        for i in range(self.N):
            c = self.C[i]
            j = int(np.argmin(c))
            ws = []
            for step in (1, -1):
                k = j
                while 0 <= k + step < self.G and c[k + step] < 1.0:
                    k += step
                if 0 <= k + step < self.G:
                    c1, c2 = c[k], c[k + step]
                    f = (1.0 - c1) / (c2 - c1) if c2 != c1 else 0.0
                    ws.append(abs((k + f * step) - j) * self.h)
            out[i] = min(np.mean(ws), 1.0) if ws else 1.0
        return out

    def ev(self, x, delta=None, idx=None):
        """values and derivatives of c_i(x_i - delta_i); x (N,) or (M, N)."""
        C = self.C if idx is None else self.C[idx]
        x = np.asarray(x, float)
        if delta is not None:
            x = x - delta
        t = (x - self.x0) / self.h
        tlo, thi = 1.0, self.G - 2.0
        tc = np.clip(t, tlo, thi - 1e-9)
        j = np.floor(tc).astype(int)
        f = tc - j
        rows = np.arange(C.shape[0])
        if x.ndim == 2:
            rows = rows[None, :]
        p0, p1, p2, p3 = C[rows, j - 1], C[rows, j], C[rows, j + 1], C[rows, np.minimum(j + 2, self.G - 1)]
        a = 3 * (p1 - p2) + p3 - p0
        bq = 2 * p0 - 5 * p1 + 4 * p2 - p3
        val = p1 + 0.5 * f * (p2 - p0 + f * (bq + f * a))
        der = (0.5 * (p2 - p0) + f * bq + 1.5 * f * f * a) / self.h
        out = t - tc
        val = val + der * out * self.h                        # linear continuation beyond the edges
        return val, der


def _u_safe(u):
    """log10(u) with a linear continuation below u = 0.05 and a quadratic penalty (keeps 1 + D.n > 0)."""
    u0 = 0.05
    ok = u >= u0
    lg = np.where(ok, np.log10(np.maximum(u, u0)), math.log10(u0) + (u - u0) / (u0 * LN10))
    dlg = np.where(ok, 1.0 / (np.maximum(u, u0) * LN10), 1.0 / (u0 * LN10))
    pen = np.where(ok, 0.0, 1e4 * (u0 - u) ** 2)
    dpen = np.where(ok, 0.0, -2e4 * (u0 - u))
    return lg, dlg, pen, dpen


def obj_template(cv, T, Z=None, w=None, delta=None, idx=None):
    """the objective F(q) and its gradient, q = (L, beta, theta)."""
    N = cv.N if idx is None else len(idx)
    m = 0 if Z is None else Z.shape[1]
    w = np.ones(N) if w is None else w

    def fun(q):
        L = q[0]
        beta = q[1:1 + m]
        th = q[1 + m:]
        u = 1.0 + T @ th
        lg, dlg, pen, dpen = _u_safe(u)
        x = L + lg + (Z @ beta if m else 0.0)
        v, d = cv.ev(x, delta, idx)
        F = np.sum(w * (v + pen))
        gL = np.sum(w * d)
        gb = (Z.T @ (w * d)) if m else np.zeros(0)
        gt = T.T @ (w * (d * dlg + dpen))
        return F, np.concatenate([[gL], gb, gt])
    return fun


def hessian(fun, q, h=1e-4):
    """numerical Hessian from the analytic gradient (central differences), symmetrised."""
    k = len(q)
    H = np.zeros((k, k))
    for a in range(k):
        e = np.zeros(k)
        e[a] = h
        H[a] = (fun(q + e)[1] - fun(q - e)[1]) / (2 * h)
    return 0.5 * (H + H.T)


def fit_template(cv, T, Z=None, w=None, delta=None, starts=None, theta_max=0.95, idx=None):
    """minimise F = sum_i w_i c_i(L + Z_i.beta + log10(1 + T_i.theta) - delta_i) over (L, beta, theta).
    T: (N, k) template (dipole: n_i), Z: (N, m) or None.  Returns dict(F, L, beta, theta, q, ok)."""
    N = cv.N if idx is None else len(idx)
    k = T.shape[1]
    m = 0 if Z is None else Z.shape[1]
    w = np.ones(N) if w is None else w

    def fun(q):
        L = q[0]
        beta = q[1:1 + m]
        th = q[1 + m:]
        u = 1.0 + T @ th
        lg, dlg, pen, dpen = _u_safe(u)
        x = L + lg + (Z @ beta if m else 0.0)
        v, d = cv.ev(x, delta, idx)
        F = np.sum(w * (v + pen))
        gL = np.sum(w * d)
        gb = (Z.T @ (w * d)) if m else np.zeros(0)
        gt = T.T @ (w * (d * dlg + dpen))
        return F, np.concatenate([[gL], gb, gt])

    Lg = np.median(cv.xhat if idx is None else cv.xhat[idx])
    if starts is None:
        starts = [np.zeros(k)]
    bnds = [(-12.0, -8.0)] + [(-5.0, 5.0)] * m + [(-theta_max, theta_max)] * k
    best = None
    for s0 in starts:
        q0 = np.concatenate([[Lg], np.zeros(m), s0])
        r = minimize(fun, q0, jac=True, method="L-BFGS-B", bounds=bnds, options=dict(maxiter=500, ftol=1e-12, gtol=1e-8))
        if best is None or r.fun < best.fun:
            best = r
    q = best.x
    return dict(F=float(best.fun), L=float(q[0]), beta=q[1:1 + m].copy(), theta=q[1 + m:].copy(), ok=bool(best.success),
                nit=int(best.nit), q=q.copy())


def fit_const(cv, w=None, delta=None, idx=None, Z=None):
    """theta = 0: the no-dipole fit (L and optional beta)."""
    k = 1
    N = cv.N if idx is None else len(idx)
    r = fit_template(cv, np.zeros((N, k)), Z=Z, w=w, delta=delta, idx=idx)
    return r


def hemisphere_scan(cv, nvec, dirs, min_n=10, idx_perm=None):
    """hemisphere anisotropy H(d) = 2 (a_N - a_S)/(a_N + a_S), a0 fitted in each hemisphere (grid sum + parabola)."""
    C = cv.C if idx_perm is None else cv.C[idx_perm]
    with np.errstate(all="ignore"):                            # numpy 1.26 + macOS Accelerate emits spurious FP warnings in
        M = (dirs @ nvec.T > 0).astype(float)                  # matmul; verified identical to einsum (README, part B note)
        SN = M @ C
    ST = C.sum(axis=0)[None, :]
    SS = ST - SN
    nN = M.sum(axis=1)
    nS = nvec.shape[0] - nN

    def argmin_par(S):
        j = np.clip(np.argmin(S, axis=1), 1, S.shape[1] - 2)
        r = np.arange(S.shape[0])
        y0, y1, y2 = S[r, j - 1], S[r, j], S[r, j + 1]
        den = y0 - 2 * y1 + y2
        off = np.where(den > 0, 0.5 * (y0 - y2) / np.where(den > 0, den, 1), 0.0)
        return cv.x0 + (j + np.clip(off, -1, 1)) * cv.h

    xN, xS = argmin_par(SN), argmin_par(SS)
    aN, aS = 10 ** xN, 10 ** xS
    H = 2 * (aN - aS) / (aN + aS)
    H = np.where((nN >= min_n) & (nS >= min_n), H, np.nan)
    return H, xN, xS


def healpix_dirs(nside):
    import healpy as hp
    v = np.array(hp.pix2vec(nside, np.arange(hp.nside2npix(nside)))).T
    return v
