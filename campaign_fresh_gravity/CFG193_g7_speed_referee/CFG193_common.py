#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG193_common -- shared machinery of the CFG193 referee re-derivation of CFG186 (SPARC a0 vs speed through the CMB frame).
Own code: loader, catalogue matching, velocity chain, baryon model, batch Levenberg-Marquardt profiler, 2D curves, weighting,
fitter.  Shared (declared in CFG193_FROZEN_CRITERIA.md): the data files, the NED cz column of sparc_cosmicweb_match.csv, and
nu_mono (imported read-only from CFG4_common; my own P2 / exponential-RAR kernels are the independent cross-checks).
Nothing here is a result.  No absolute home path is printed anywhere: the repo root is shown as <repo>.
"""
import os
import sys
import re
import io
import csv
import json
import math
import time
import builtins
import hashlib

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
C_KMS = 299792.458
KPC_M = 3.0856775814913673e19
CONV = 1e6 / KPC_M                      # (km/s)^2/kpc -> m/s^2
LN10 = math.log(10.0)
VARIANT = os.environ.get("CFG193_VARIANT", "")      # "" = main; "U2" = the reported alternative point mask (baryonic V^2 > 0 at fiducial Upsilon, unsigned V_disk^2, V_bul^2)
W_REF = 600.0
V_SUN, SUN_L, SUN_B = 369.8, 264.0, 48.3           # frozen (rounded) values
V_SUN_ALT = (369.82, 264.021, 48.253)              # Planck, sensitivity
V_LG, LG_L, LG_B = 627.0, 276.0, 30.0              # from memory in the frozen text (S5)
OM, H0_PRIMARY, H0_ALT = 0.311, 67.66, 73.0
UPS_D0, UPS_B0, UPS_SIG = 0.5, 0.7, 0.1
XG = np.round(np.arange(-11.30, -9.00 + 1e-9, 0.02), 6)      # 116 points
TG = np.round(np.arange(-4.0, 4.0 + 1e-9, 0.25), 6)          # 33 points
TF = np.round(np.arange(-4.0, 4.0 + 1e-9, 0.05), 6)          # 161 points


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "campaign_fresh_gravity")):
        return os.path.abspath(r)
    for start in (HERE, os.getcwd()):
        d = start
        for _ in range(12):
            if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")) and os.path.isdir(os.path.join(d, "real_research")):
                return d
            d = os.path.dirname(d)
    raise SystemExit("repo root not found: set ZF_REPO")


REPO = find_repo()
DATA = os.path.join(REPO, "real_research", "data")


def scrub(s):
    """no absolute home path in any output"""
    s = str(s)
    s = s.replace(REPO, "<repo>").replace(HERE, "<here>")
    s = re.sub(r"/Users/[^\s'\"]+", "<path>", s)
    s = re.sub(r"/private/tmp/[^\s'\"]+", "<path>", s)
    return s


class Tee:
    """writes the script's own .out (name given by mode) and echoes to stdout, scrubbed"""

    def __init__(self, path):
        self.f = builtins.open(path, "w")
        self.checks = []

    def p(self, *a):
        s = scrub(" ".join(str(x) for x in a))
        print(s)
        self.f.write(s + "\n")
        self.f.flush()

    def check(self, name, ok, detail="", load=True):
        self.checks.append((name, bool(ok), load))
        self.p("  [%s] %s%s  %s" % ("PASS" if ok else "FAIL", name, " (load-bearing)" if load else " (reported)", detail))
        return bool(ok)

    def failed_load(self):
        return [n for n, ok, ld in self.checks if ld and not ok]


def jdump(obj, path):
    def conv(o):
        if isinstance(o, (np.floating,)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return [conv(x) for x in o.tolist()]
        if isinstance(o, float):
            return None if not math.isfinite(o) else o
        if isinstance(o, dict):
            return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(x) for x in o]
        return o
    with builtins.open(path, "w") as f:
        json.dump(conv(obj), f, indent=1, sort_keys=True)


# ------------------------------------------------------------------------------------------------ kernels
def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))


def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


_NU_MONO = None


def get_kernel(name):
    global _NU_MONO
    if name == "P2":
        return nu_p2
    if name == "RAR":
        return nu_rar
    if _NU_MONO is None:                                       # S3: shared, read-only
        sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
        import CFG4_common as c4
        _NU_MONO = c4.nu_mono
    return _NU_MONO


# ------------------------------------------------------------------------------------------------ SPARC (own loader)
def load_sparc():
    d_ = os.path.join(DATA, "sparc_data")
    tab = {}
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat",
            "eVflat", "Q")
    for line in builtins.open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19:
            continue
        try:
            vals = [float(t) for t in tok[1:18]]
        except ValueError:
            continue
        row = dict(zip(keys, vals))
        for k in ("T", "fD", "Q"):
            row[k] = int(row[k])
        tab[tok[0]] = row
    gal = []
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        nm = f.replace("_rotmod.dat", "")
        try:
            a = np.genfromtxt(os.path.join(d_, f), comments="#")
        except Exception:
            continue
        if a.ndim != 2 or a.shape[1] < 6 or nm not in tab:
            continue
        g = dict(name=nm, R=a[:, 0], V=a[:, 1], eV=a[:, 2], Vg=a[:, 3], Vd=a[:, 4], Vb=a[:, 5], meta=tab[nm])
        gal.append(g)
    return gal


def usable_mask(g, rule="U1"):
    m = np.isfinite(g["R"]) & np.isfinite(g["V"]) & np.isfinite(g["eV"]) & (g["R"] > 0) & (g["V"] > 0) & (g["eV"] > 0)
    if rule == "U2":
        v2 = g["Vg"] * np.abs(g["Vg"]) + UPS_D0 * g["Vd"] * np.abs(g["Vd"]) + UPS_B0 * g["Vb"] * np.abs(g["Vb"])
        m &= np.isfinite(v2) & (v2 > 0)
    return m


def clean_sample(gal, rule="U1"):
    out = []
    for g in gal:
        m = g["meta"]
        if m["Q"] <= 2 and m["Inc"] >= 30.0 and usable_mask(g, rule).sum() >= 5:
            out.append(g)
    return out


def raw_count(gal):
    """Q<=2 and Inc>=30, no point cut"""
    return [g for g in gal if g["meta"]["Q"] <= 2 and g["meta"]["Inc"] >= 30.0]


# ------------------------------------------------------------------------------------------------ positions, velocities
def read_tsv_vizier(path):
    rows, hdr = [], None
    with builtins.open(path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            t = line.rstrip("\n").split("\t")
            if hdr is None:
                hdr = [x.strip() for x in t]
                continue
            if set(t[0].strip()) <= set("- ") and len(t[0].strip()) > 2 or (len(t) > 1 and t[0].strip() == "" and t[1].strip() in ("deg", "")):
                continue
            if t[0].strip() and set(t[0].strip()) <= set("-"):
                continue
            rows.append({h: (t[i].strip() if i < len(t) else "") for i, h in enumerate(hdr)})
    return hdr, rows


def to_gal(ra, dec):
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    c = SkyCoord(ra=np.asarray(ra) * u.deg, dec=np.asarray(dec) * u.deg, frame="fk5").galactic
    return c.l.deg, c.b.deg


def unit(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    return np.array([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)])


def ang_sep_arcmin(ra1, dec1, ra2, dec2):
    r1, d1, r2, d2 = map(np.radians, (ra1, dec1, ra2, dec2))
    s = np.sin(d1) * np.sin(d2) + np.cos(d1) * np.cos(d2) * np.cos(r1 - r2)
    return np.degrees(np.arccos(np.clip(s, -1, 1))) * 60.0


def load_positions():
    hdr, rows = read_tsv_vizier(os.path.join(DATA, "sparc_lelli2016_table1_pos.tsv"))
    pos = {}
    for r in rows:
        try:
            pos[r["Name"]] = (float(r["_RAJ2000"]), float(r["_DEJ2000"]))
        except (ValueError, KeyError):
            continue
    return pos


def load_ned():
    d = {}
    with builtins.open(os.path.join(DATA, "sparc_cosmicweb_match.csv")) as f:
        for r in csv.DictReader(f):
            if r["cz_kms"].strip():
                d[r["name"]] = float(r["cz_kms"])
    return d


def _nearest(ra, dec, cat_ra, cat_dec):
    sep = ang_sep_arcmin(ra, dec, cat_ra, cat_dec)
    j = int(np.argmin(sep))
    return j, float(sep[j])


def load_catalogues():
    """UNGC (HRV), KT2017 (HRV, with group flag), 2MRS (cz): arrays for nearest-neighbour matching"""
    cats = {}
    hdr, rows = read_tsv_vizier(os.path.join(DATA, "ungc_karachentsev2013.tsv"))
    ra, dec, v, nm = [], [], [], []
    for r in rows:
        try:
            a_, b_, c_ = float(r["_RAJ2000"]), float(r["_DEJ2000"]), float(r["HRV"])
        except (ValueError, KeyError):
            continue
        ra.append(a_); dec.append(b_); v.append(c_); nm.append(r["Name"])
    cats["UNGC"] = (np.array(ra), np.array(dec), np.array(v), nm)
    hdr, rows = read_tsv_vizier(os.path.join(DATA, "kt2017_galaxies.tsv"))
    ra, dec, v, grp = [], [], [], []
    for r in rows:
        try:
            a_, b_, c_ = float(r["RAJ2000"]), float(r["DEJ2000"]), float(r["HRV"])
        except (ValueError, KeyError):
            continue
        ra.append(a_); dec.append(b_); v.append(c_); grp.append(r["PGC1"])
    ra, dec, v = np.array(ra), np.array(dec), np.array(v)
    grp = np.array(grp)
    varies = {}
    for gname in set(grp.tolist()):
        vv = v[grp == gname]
        varies[gname] = bool(len(vv) > 1 and np.ptp(vv) > 0.5)
    cats["KT2017"] = (ra, dec, v, list(grp), varies)
    hdr, rows = read_tsv_vizier(os.path.join(DATA, "2mrs_huchra2012.tsv"))
    ra, dec, v = [], [], []
    for r in rows:
        try:
            a_, b_, c_ = float(r["RAJ2000"]), float(r["DEJ2000"]), float(r["cz"])
        except (ValueError, KeyError):
            continue
        ra.append(a_); dec.append(b_); v.append(c_)
    cats["2MRS"] = (np.array(ra), np.array(dec), np.array(v), None)
    return cats


def heliocentric_velocity(name, ra, dec, ned, cats, radius=1.5):
    """first available source: NED, UNGC, KT2017 (only if its group's members carry different values), 2MRS.
    returns (cz_hel, source, alt) with alt = list of (source, cz, sep) from other sources (overlap check)"""
    cand = []
    if name in ned:
        cand.append(("NED", ned[name], 0.0))
    ra_, de_, v_, nm_ = cats["UNGC"]
    j, s = _nearest(ra, dec, ra_, de_)
    if s <= radius:
        cand.append(("UNGC", float(v_[j]), s))
    ra_, de_, v_, grp, varies = cats["KT2017"]
    j, s = _nearest(ra, dec, ra_, de_)
    if s <= radius and varies.get(grp[j], False):
        cand.append(("KT2017", float(v_[j]), s))
    ra_, de_, v_, _ = cats["2MRS"]
    j, s = _nearest(ra, dec, ra_, de_)
    if s <= radius:
        cand.append(("2MRS", float(v_[j]), s))
    if not cand:
        return None, None, []
    return cand[0][1], cand[0][0], cand


# ------------------------------------------------------------------------------------------------ cosmology
_ZTAB = None


def _comoving_table(h0, om):
    z = np.linspace(0.0, 0.2, 40001)
    E = np.sqrt(om * (1 + z) ** 3 + (1 - om))
    dc = np.concatenate([[0.0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(z))]) * C_KMS / h0   # Mpc
    return z, dc


_CACHE = {}


def z_cos(D_mpc, h0=H0_PRIMARY, om=OM, dist="comoving", linear=False):
    """cosmological redshift for a distance D (Mpc): comoving (primary), luminosity (variant), or linear cz = H0 D"""
    D = np.asarray(D_mpc, float)
    if linear:
        return h0 * D / C_KMS
    key = (h0, om)
    if key not in _CACHE:
        _CACHE[key] = _comoving_table(h0, om)
    z, dc = _CACHE[key]
    if dist == "luminosity":
        return np.interp(D, dc * (1 + z), z)
    return np.interp(D, dc, z)


def cmb_convert(cz_hel, l, b, vsun=V_SUN, lsun=SUN_L, bsun=SUN_B):
    n = unit(l, b)
    vec = vsun * unit(lsun, bsun)
    vn = float(np.sum(n * vec)) if n.ndim == 1 else np.sum(n * vec[:, None], axis=0)
    zh = cz_hel / C_KMS
    zc = (1 + zh) / (1 - vn / C_KMS) - 1.0
    return zc


def u_los(zcmb, D_mpc, h0=H0_PRIMARY, **kw):
    zc = z_cos(D_mpc, h0, **kw)
    return C_KMS * (zcmb - zc) / (1 + zc)


def build_table(gal_all, ned, pos, cats, vsun=(V_SUN, SUN_L, SUN_B)):
    """for every galaxy in gal_all: position, l, b, heliocentric velocity + source, zcmb"""
    out = {}
    for g in gal_all:
        nm = g["name"]
        if nm not in pos:
            continue
        ra, dec = pos[nm]
        l, b = to_gal([ra], [dec])
        l, b = float(l[0]), float(b[0])
        cz, src, cand = heliocentric_velocity(nm, ra, dec, ned, cats)
        if cz is None:
            out[nm] = dict(ra=ra, dec=dec, l=l, b=b, cz_hel=None, src=None, cand=[])
            continue
        zc = cmb_convert(cz, l, b, *vsun)
        out[nm] = dict(ra=ra, dec=dec, l=l, b=b, cz_hel=cz, src=src, cand=cand, zcmb=float(zc))
    return out


# ------------------------------------------------------------------------------------------------ profile: batch LM
class Gal:
    """arrays for the profile of one galaxy"""

    def __init__(self, g):
        m = usable_mask(g, "U2" if VARIANT == "U2" else "U1")
        self.name = g["name"]
        self.R = g["R"][m]; self.V = g["V"][m]; self.eV = g["eV"][m]
        self.Sg = g["Vg"][m] * np.abs(g["Vg"][m])
        if VARIANT == "U2":
            self.Sd = g["Vd"][m] ** 2; self.Sb = g["Vb"][m] ** 2
        else:
            self.Sd = g["Vd"][m] * np.abs(g["Vd"][m]); self.Sb = g["Vb"][m] * np.abs(g["Vb"][m])
        self.hasb = bool(np.any(g["Vb"][m] != 0))
        me = g["meta"]
        self.D, self.eD, self.inc = me["D"], me["eD"], me["Inc"]
        self.einc = me["eInc"] if me["eInc"] > 0 else 1.0
        self.fD = me["fD"]
        self.N = int(m.sum())


def model_v(G, lyd, lyb, inc, a0, scl, nu):
    """(K,) params -> (K,N) predicted velocities.  scl = sqrt(D'/D) (K,).  g_bar invariant to D."""
    yd = (10.0 ** lyd)[:, None]; yb = (10.0 ** lyb)[:, None]
    gb = (G.Sg[None, :] + yd * G.Sd[None, :] + yb * G.Sb[None, :]) / G.R[None, :] * CONV
    gb = np.maximum(gb, 1e-16)
    go = nu(gb / a0[:, None]) * gb
    vp = np.sqrt(go * (G.R * KPC_M)[None, :]) / 1e3
    vp = vp * (np.sin(np.radians(inc)) / math.sin(math.radians(G.inc)))[:, None] * scl[:, None]
    return vp


def resid(G, th, a0, scl, nu, prior=True, Vobs=None):
    V = G.V if Vobs is None else Vobs
    vp = model_v(G, th[:, 0], th[:, 1], th[:, 2], a0, scl, nu)
    r = (V[None, :] - vp) / G.eV[None, :]
    if prior:
        p1 = (th[:, 0] - math.log10(UPS_D0)) / UPS_SIG
        p2 = (th[:, 1] - math.log10(UPS_B0)) / UPS_SIG
        p3 = (th[:, 2] - G.inc) / G.einc
        r = np.concatenate([r, p1[:, None], p2[:, None], p3[:, None]], axis=1)
    return r


LO = np.array([-1.6, -1.6, 5.0])
HI = np.array([0.8, 0.8, 89.0])
HSTEP = np.array([1e-4, 1e-4, 1e-3])


def lm_profile(G, a0, scl, nu, th0, iters=100, Vobs=None, free=(True, True, True), prior=True):
    """batch Levenberg-Marquardt over K cells (a0, scl (K,)); returns chi2 (K,), theta (K,3)"""
    K = a0.shape[0]
    th = np.array(th0, float).copy()
    lam = np.full(K, 1e-2)
    r = resid(G, th, a0, scl, nu, prior, Vobs)
    chi = np.sum(r * r, axis=1)
    fmask = np.array(free, float)
    for _ in range(iters):
        J = np.empty(r.shape + (3,))
        for k in range(3):
            if not free[k]:
                J[:, :, k] = 0.0
                continue
            t2 = th.copy(); t2[:, k] += HSTEP[k]
            J[:, :, k] = (resid(G, t2, a0, scl, nu, prior, Vobs) - r) / HSTEP[k]
        A = np.einsum("kni,knj->kij", J, J)
        g = np.einsum("kni,kn->ki", J, r)
        dA = np.einsum("kii->ki", A).copy()
        dA = np.maximum(dA, 1e-9)
        for k in range(3):
            if not free[k]:
                dA[:, k] = 1.0
        Ad = A.copy()
        for k in range(3):
            Ad[:, k, k] += lam * dA[:, k] + (0.0 if free[k] else 1.0)
        try:
            dl = np.linalg.solve(Ad, -g[:, :, None])[:, :, 0]
        except np.linalg.LinAlgError:
            dl = -g / dA
        dl *= fmask[None, :]
        tn = np.minimum(np.maximum(th + dl, LO), HI)
        rn = resid(G, tn, a0, scl, nu, prior, Vobs)
        cn = np.sum(rn * rn, axis=1)
        ok = np.isfinite(cn) & (cn < chi)
        th = np.where(ok[:, None], tn, th)
        r = np.where(ok[:, None], rn, r)
        chi = np.where(ok, cn, chi)
        lam = np.where(ok, np.maximum(lam / 3.0, 1e-7), np.minimum(lam * 5.0, 1e7))
    return chi, th


def starts(G, K):
    """three starts: prior centre, a perturbed low-M/L one, a perturbed high-M/L one"""
    base = np.array([math.log10(UPS_D0), math.log10(UPS_B0), G.inc])
    S = []
    for dy, di in ((0.0, 0.0), (-0.15, -1.0), (0.15, 1.0)):
        th = np.tile(base, (K, 1)); th[:, 0] += dy; th[:, 1] += dy; th[:, 2] = np.clip(th[:, 2] + di * G.einc, 6, 88)
        S.append(th)
    return S


def profile_grid(G, nu, xg=XG, tg=TG, Vobs=None, nstart=2, free=(True, True, True), prior=True, return_all=False, iters=100):
    """chi2(x,t) with the nuisances profiled (min over nstart starts); the distance prior t^2 is NOT added here.
    Returns C (nt, nx) with NaN for infeasible cells (D' < 0.3 D)."""
    nt, nx = len(tg), len(xg)
    Dp = G.D + G.eD * tg
    feas = Dp >= 0.3 * G.D
    T, X = np.meshgrid(tg, xg, indexing="ij")
    a0 = (10.0 ** X).ravel() if False else (10.0 ** X.ravel())
    scl = np.sqrt(np.maximum(G.D + G.eD * T.ravel(), 1e-9) / G.D)
    K = a0.shape[0]
    res = []
    for th0 in starts(G, K)[:nstart]:
        chi, th = lm_profile(G, a0, scl, nu, th0, iters=iters, Vobs=Vobs, free=free, prior=prior)
        res.append(chi)
    res = np.array(res)
    C = res.min(axis=0).reshape(nt, nx)
    C[~feas, :] = np.nan
    if return_all:
        return C, res.reshape(len(res), nt, nx)
    return C


# ------------------------------------------------------------------------------------------------ 2D curves -> C_eff
def spline_t(C, tg=TG, tf=TF):
    """cubic spline along t of a (nt,nx) curve onto the fine grid; infeasible t rows -> 1e6"""
    from scipy.interpolate import CubicSpline
    ok = np.all(np.isfinite(C), axis=1)
    out = np.full((len(tf), C.shape[1]), 1e6)
    if ok.sum() < 4:
        return out
    cs = CubicSpline(tg[ok], C[ok], axis=0)
    inr = (tf >= tg[ok].min() - 1e-9) & (tf <= tg[ok].max() + 1e-9)
    out[inr] = cs(tf[inr])
    return out


def halfwidth(xg, f):
    """Delta = 1 half-width of a curve f(x) (min subtracted) around its minimum; one-sided crossings mirrored; edge -> other side"""
    j = int(np.argmin(f))
    fm = f[j]
    def cross(rng):
        prev = j
        for k in rng:
            if f[k] - fm >= 1.0:
                a = (1.0 - (f[prev] - fm)) / max(f[k] - f[prev], 1e-12)
                return abs(xg[prev] + a * (xg[k] - xg[prev]) - xg[j])
            prev = k
        return None
    r = cross(range(j + 1, len(xg)))
    l = cross(range(j - 1, -1, -1))
    if r is None and l is None:
        return 1.2
    if r is None:
        return l
    if l is None:
        return r
    return 0.5 * (r + l)


class Curves:
    """per-galaxy 2D curves and everything derived: d0 = C - t^2 (unscaled data part), s (Birge), tau; builds C_eff."""

    def __init__(self, names, C, tg=TG, xg=XG, meta=None):
        self.names = list(names)
        self.C = C                              # (G, nt, nx) coarse t, raw chi2 (no t^2), NaN infeasible
        self.tg, self.xg = tg, xg
        self.G = len(names)
        self.Ct = np.array([spline_t(C[i] + tg[:, None] ** 2, tg) for i in range(self.G)])     # (G, nf, nx) incl t^2
        self.nf = len(TF)
        # global minima and Birge factors
        self.chi2min = np.array([np.nanmin(C[i] + tg[:, None] ** 2) for i in range(self.G)])
        self.N = np.array(meta["N"], float)
        self.s = np.maximum(1.0, self.chi2min / np.maximum(self.N - 1, 1))
        self.meta = meta

    def data_part(self, birge=True):
        """d(x,t) = (C - t^2)/s on the fine grid: (G, nf, nx)"""
        d = self.Ct - (TF ** 2)[None, :, None]
        if birge:
            d = d / self.s[:, None, None]
        d[self.Ct > 5e5] = 1e6
        return d

    def sigma_i(self, birge=True):
        """distance-profiled width: half-width of min_t[t^2 + d] curve"""
        d = self.data_part(birge)
        p = np.min((TF ** 2)[None, :, None] + d, axis=1)          # (G, nx)
        sig = np.array([halfwidth(self.xg, p[i]) for i in range(self.G)])
        xhat = self.xg[np.argmin(p, axis=1)]
        return sig, xhat, p

    def tau_ml(self, sig, xhat, w=None):
        from scipy.optimize import minimize
        w = np.ones(len(xhat)) if w is None else w
        def nll(pr):
            L, lt = pr
            v = sig ** 2 + math.exp(2 * lt)
            return 0.5 * np.sum(w * (np.log(v) + (xhat - L) ** 2 / v))
        best = None
        for lt0 in (-2.0, -1.0, -0.5):
            r = minimize(nll, [np.average(xhat, weights=w), lt0], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-9, maxiter=2000))
            if best is None or r.fun < best.fun:
                best = r
        return float(best.x[0]), float(math.exp(best.x[1]))

    def ceff(self, tau, birge=True, soften=True):
        """C_eff(x,t) = t^2 + m(t) + q(t) [d - m], q = sigma_x(t)^2/(sigma_x(t)^2 + tau^2)  (never scales the prior)"""
        d = self.data_part(birge)
        m = d.min(axis=2)                                           # (G, nf)
        if not soften:
            return (TF ** 2)[None, :, None] + d
        q = np.ones_like(m)
        for i in range(self.G):
            for k in range(0, self.nf):
                if m[i, k] > 5e5:
                    continue
                sx = halfwidth(self.xg, d[i, k])
                q[i, k] = sx * sx / (sx * sx + tau * tau)
        return (TF ** 2)[None, :, None] + m[:, :, None] + q[:, :, None] * (d - m[:, :, None])

    def ceff_fast(self, tau, birge=True):
        """same as ceff but vectorised half-widths (used on every mock)"""
        d = self.data_part(birge)
        m = d.min(axis=2)
        sx = halfwidth_batch(self.xg, d - m[:, :, None])
        q = sx * sx / (sx * sx + tau * tau)
        q[m > 5e5] = 1.0
        return (TF ** 2)[None, :, None] + m[:, :, None] + q[:, :, None] * (d - m[:, :, None])


def halfwidth_batch(xg, f):
    """f: (G, nf, nx) with min 0 on last axis; returns (G, nf) half-widths (one-sided mirrored; none -> 1.2)"""
    G_, nf, nx = f.shape
    j = np.argmin(f, axis=2)                                        # (G, nf)
    idx = np.arange(nx)[None, None, :]
    above = f >= 1.0
    right = above & (idx > j[:, :, None])
    left = above & (idx < j[:, :, None])
    kr = np.where(right.any(axis=2), np.argmax(right, axis=2), -1)
    kl = np.where(left.any(axis=2), nx - 1 - np.argmax(left[:, :, ::-1], axis=2), -1)
    def xcross(k, step):
        kk = np.clip(k, 1 if step < 0 else 0, nx - 1)
        prev = np.clip(kk - step, 0, nx - 1)
        fk = np.take_along_axis(f, kk[:, :, None], 2)[:, :, 0]
        fp = np.take_along_axis(f, prev[:, :, None], 2)[:, :, 0]
        a = (1.0 - fp) / np.maximum(fk - fp, 1e-12)
        return xg[prev] + a * (xg[kk] - xg[prev])
    xj = xg[j]
    r = np.where(kr >= 0, np.abs(xcross(kr, 1) - xj), np.nan)
    l = np.where(kl >= 0, np.abs(xcross(kl, -1) - xj), np.nan)
    hw = np.where(np.isnan(r) & np.isnan(l), 1.2, np.where(np.isnan(r), l, np.where(np.isnan(l), r, 0.5 * (r + l))))
    return hw


# ------------------------------------------------------------------------------------------------ the statistic
class Stat:
    """F(L, beta) = sum_i w_i min_t Ceff_i(L + log10(1 + beta z_i(t)) + extra_i, t)."""

    def __init__(self, ceff, xg=XG):
        self.ce = ceff                      # (G, nf, nx)
        self.xg = xg
        self.dx = xg[1] - xg[0]
        self.G, self.nf, self.nx = ceff.shape
        # outward slopes for the non-decreasing continuation
        self.sl_lo = np.maximum(0.0, (ceff[:, :, 0] - ceff[:, :, 1]) / self.dx)
        self.sl_hi = np.maximum(0.0, (ceff[:, :, -1] - ceff[:, :, -2]) / self.dx)
        self.gi = np.arange(self.G)[:, None]
        self.ti = np.arange(self.nf)[None, :]

    def val(self, xq):
        """xq (G, nf) -> Ceff at xq: cubic Catmull-Rom in x inside the grid (exact for quadratics; the first version of this
        routine was piecewise linear and failed the M0 exactness control, see README); outside the grid the curve continues
        linearly with the outward slope if that slope is increasing and flat otherwise (non-decreasing continuation)"""
        p = (xq - self.xg[0]) / self.dx
        p0 = np.clip(np.floor(np.nan_to_num(p, nan=0.0)).astype(int), 0, self.nx - 2)
        fr = np.clip(p - p0, 0.0, 1.0)
        i0 = np.clip(p0 - 1, 0, self.nx - 1); i1 = p0; i2 = p0 + 1; i3 = np.clip(p0 + 2, 0, self.nx - 1)
        f0 = self.ce[self.gi, self.ti, i0]; f1 = self.ce[self.gi, self.ti, i1]
        f2 = self.ce[self.gi, self.ti, i2]; f3 = self.ce[self.gi, self.ti, i3]
        v = 0.5 * (2.0 * f1 + (-f0 + f2) * fr + (2.0 * f0 - 5.0 * f1 + 4.0 * f2 - f3) * fr ** 2 + (-f0 + 3.0 * f1 - 3.0 * f2 + f3) * fr ** 3)
        lo = p < 0
        hi = p > self.nx - 1
        if lo.any():
            v = np.where(lo, self.ce[:, :, 0] + self.sl_lo * (self.xg[0] - xq), v)
        if hi.any():
            v = np.where(hi, self.ce[:, :, -1] + self.sl_hi * (xq - self.xg[-1]), v)
        return v

    def per_gal(self, L, beta, z, extra=None):
        """min over t for each galaxy; z (G, nf).  returns (G,) and argmin t idx"""
        arg = 1.0 + beta * z
        arg = np.maximum(arg, 0.05)
        xq = L + np.log10(arg)
        if extra is not None:
            xq = xq + extra
        v = self.val(xq)
        j = np.argmin(v, axis=1)
        return v[np.arange(self.G), j], j

    def F(self, L, beta, z, w=None, extra=None):
        f, _ = self.per_gal(L, beta, z, extra)
        return float(np.sum(f if w is None else w * f))


def fit_LB(stat, z, w=None, bmin=None, bmax=20.0, starts_b=(-0.5, 0.0, 0.5, 2.0), L0=None, extra=None, retall=False):
    from scipy.optimize import minimize
    if bmin is None:
        bmin = -0.95 / max(float(np.max(z)), 1e-6)
    if L0 is None:
        L0 = -10.1
    best = None
    for b0 in starts_b:
        b0 = min(max(b0, bmin + 1e-3), bmax - 1e-3)
        def obj(p):
            L, b = p
            if b < bmin or b > bmax:
                return 1e12 + 1e6 * (abs(b - min(max(b, bmin), bmax)))
            return stat.F(L, b, z, w, extra)
        r = minimize(obj, [L0, b0], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-6, maxiter=400, initial_simplex=np.array([[L0, b0], [L0 + 0.05, b0], [L0, b0 + 0.15 + 0.1 * abs(b0)]])))
        if best is None or r.fun < best.fun:
            best = r
    L, b = float(best.x[0]), float(best.x[1])
    if retall:
        return L, b, float(best.fun)
    return L, b


# ------------------------------------------------------------------------------------------------ speed arrays
def z_of_t(u0, dudt_tf, w2=None):
    """z_i(t) = (u_i(t)/600)^2 on the fine t grid.  u0: (G,) at catalogue distance; dudt_tf: (G, nf) u(t) - u(0)"""
    u = u0[:, None] + dudt_tf
    return (u / W_REF) ** 2


def sha256_file(p):
    h = hashlib.sha256()
    with builtins.open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()
