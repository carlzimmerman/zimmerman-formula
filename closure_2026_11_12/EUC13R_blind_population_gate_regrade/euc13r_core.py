"""EUC13R core machinery, written for the blind re-grade from the frozen criteria text only.

Units: kpc, Msun, km/s; accelerations in (km/s)^2/kpc. Nothing here is imported from any other lane.
"""
import csv
import glob
import math
import os
import re

import numpy as np
from scipy.special import gammainc, gammaincinv

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXT = os.path.join(REPO, "_external_data")

G = 4.300917270e-6            # kpc (km/s)^2 / Msun
C_KMS = 299792.458
ACC_SI = 1.0e6 / 3.0856775814913673e19   # 1 (km/s)^2/kpc in m/s^2
A0_SI = {"canonical": 9.3603e-11, "alt": 1.132e-10}
A0 = {k: v / ACC_SI for k, v in A0_SI.items()}
SIGCR_PREF = C_KMS ** 2 / (4.0 * math.pi * G)   # Msun/kpc times 1/kpc -> Msun/kpc^2 when divided by kpc
RMAX = 1.0e6                  # kpc
ARCSEC = math.pi / (180.0 * 3600.0)


# ---------------------------------------------------------------- cosmology
class Cosmo:
    def __init__(self, H0=67.74, Om=0.3089, zmax=1200.0, npts=200001):
        self.H0, self.Om = H0, Om
        s = np.linspace(0.0, math.log1p(zmax), npts)          # s = ln(1+z)
        z = np.expm1(s)
        E = np.sqrt(Om * (1 + z) ** 3 + (1 - Om))
        f = (1 + z) / E                                        # dz/E = (1+z) ds / E
        dc = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(s))])
        self.s, self.dc = s, dc * (C_KMS / H0) * 1.0e3        # kpc

    def DC(self, z):
        return np.interp(np.log1p(np.asarray(z, float)), self.s, self.dc)

    def DA(self, z):
        z = np.asarray(z, float)
        return self.DC(z) / (1 + z)

    def DA12(self, z1, z2):
        z2 = np.asarray(z2, float)
        return (self.DC(z2) - self.DC(z1)) / (1 + z2)

    def sigcr(self, zl, zs):
        """Critical density, Msun/kpc^2. zs <= zl gives inf."""
        zl = np.asarray(zl, float)
        zs = np.asarray(zs, float)
        dl, ds, dls = self.DA(zl), self.DA(zs), self.DA12(zl, zs)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = SIGCR_PREF * ds / (dl * dls)
        return np.where(dls > 0, out, np.inf)

    def dls_ds(self, zl, zs):
        zs = np.asarray(zs, float)
        return np.clip(self.DA12(zl, zs) / self.DA(zs), 0.0, None)


EUCLID = Cosmo(67.74, 0.3089)
AUGER = Cosmo(70.0, 0.3)


# ---------------------------------------------------------------- Sersic / Prugniel-Simien
def b_n(n):
    return gammaincinv(2.0 * np.asarray(n, float), 0.5)


def ps_p(n):
    n = np.asarray(n, float)
    return 1.0 - 0.6097 / n + 0.05463 / n ** 2


def ps_frac3d(y, n):
    """Enclosed 3D mass fraction of a Prugniel-Simien body at r = y R_e."""
    n = np.asarray(n, float)
    a = n * (3.0 - ps_p(n))
    return gammainc(a, b_n(n) * np.power(y, 1.0 / n))


def ps_rho_shape(y, n):
    """Unnormalised 3D density of the PS body, total mass normalisation done by the caller."""
    p = ps_p(n)
    return np.power(y, -p) * np.exp(-b_n(n) * np.power(y, 1.0 / n))


def sersic_lfrac2d(x, n):
    n = np.asarray(n, float)
    return gammainc(2.0 * n, b_n(n) * np.power(x, 1.0 / n))


# ---------------------------------------------------------------- projected law-S mass
K_NODES = 240
_GL = {}


def gl(k):
    if k not in _GL:
        _GL[k] = np.polynomial.legendre.leggauss(k)
    return _GL[k]


def h_nodes(R, Re, n, M, k=K_NODES):
    """Return (wu, h): quadrature weights in u (scaled to [0,U]) and h = G M f(r)/r^2 at r = R cosh u, unit B.
    Shapes (N, k)."""
    R = np.atleast_1d(np.asarray(R, float))
    Re = np.broadcast_to(np.asarray(Re, float), R.shape)
    n = np.broadcast_to(np.asarray(n, float), R.shape)
    M = np.broadcast_to(np.asarray(M, float), R.shape)
    x, w = gl(k)
    U = np.arccosh(np.maximum(RMAX / R, 1.0 + 1e-12))
    u = 0.5 * U[:, None] * (x[None, :] + 1.0)
    wu = 0.5 * U[:, None] * w[None, :]
    r = R[:, None] * np.cosh(u)
    f = ps_frac3d(r / Re[:, None], n[:, None])
    h = G * M[:, None] * f / r ** 2
    return wu, h


def g_law(gN, a0):
    if a0 <= 0:
        return gN
    return 0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / gN))


def m2d_from_nodes(R, wu, h, B, a0):
    """M_2D(<R) for mass multipliers B. B shape (N,) or (N, nb). Returns same shape as B."""
    R = np.atleast_1d(R)
    B = np.asarray(B, float)
    if B.ndim == 1:
        g = g_law(B[:, None] * h, a0)
        return R ** 2 / G * np.sum(wu * g, axis=1)
    out = np.empty(B.shape)
    for j in range(B.shape[1]):
        g = g_law(B[:, j:j + 1] * h, a0)
        out[:, j] = R ** 2 / G * np.sum(wu * g, axis=1)
    return out


BGRID = np.round(np.arange(-1.5, 2.5 + 1e-9, 0.05), 10)


def build_table(R, Re, n, M, a0, chunk=400):
    """log10 M_2D(<R) on BGRID for each lens. (N, nb)."""
    N = len(R)
    out = np.empty((N, len(BGRID)))
    Bs = 10.0 ** BGRID
    for s in range(0, N, chunk):
        sl = slice(s, min(N, s + chunk))
        wu, h = h_nodes(R[sl], Re[sl], n[sl], M[sl])
        for j, B in enumerate(Bs):
            g = g_law(B * h, a0)
            out[sl, j] = np.log10(R[sl] ** 2 / G * np.sum(wu * g, axis=1))
    return out


def solve_b_direct(R, Re, n, M, target, a0, lo=-4.0, hi=7.0, iters=60, chunk=2000):
    """Bisection for b: M_2D(<R; 10^b M) = target. Vectorised."""
    R = np.atleast_1d(np.asarray(R, float))
    target = np.broadcast_to(np.asarray(target, float), R.shape)
    out = np.empty(len(R))
    for s in range(0, len(R), chunk):
        sl = slice(s, min(len(R), s + chunk))
        wu, h = h_nodes(R[sl], np.broadcast_to(Re, R.shape)[sl], np.broadcast_to(n, R.shape)[sl],
                        np.broadcast_to(M, R.shape)[sl])
        a = np.full(R[sl].shape, lo)
        b = np.full(R[sl].shape, hi)
        T = target[sl]
        for _ in range(iters):
            mid = 0.5 * (a + b)
            m = m2d_from_nodes(R[sl], wu, h, 10.0 ** mid, a0)
            up = m < T
            a = np.where(up, mid, a)
            b = np.where(up, b, mid)
        out[sl] = 0.5 * (a + b)
    return out


def interp_rows(table, logT):
    """Invert monotone rows: b such that table[i](b) = logT[i] (logT shape (N,) or (N, k)).
    Returns b and a mask of out-of-grid entries (b set to nan there)."""
    logT = np.asarray(logT, float)
    one = logT.ndim == 1
    if one:
        logT = logT[:, None]
    N, k = logT.shape
    nb = table.shape[1]
    idx = np.sum(table[:, None, :] < logT[:, :, None], axis=2)      # (N, k): number of grid values below
    oob = (idx == 0) | (idx == nb)
    i0 = np.clip(idx - 1, 0, nb - 2)
    rows = np.arange(N)[:, None]
    t0 = table[rows, i0]
    t1 = table[rows, i0 + 1]
    frac = (logT - t0) / (t1 - t0)
    b = BGRID[i0] + frac * (BGRID[1] - BGRID[0])
    b = np.where(oob, np.nan, b)
    if one:
        return b[:, 0], oob[:, 0]
    return b, oob


# ---------------------------------------------------------------- catalogue: sample P
KEY = os.path.join(EXT, "euclid_dr1_eclipse", "eclipse_dr1_catalogue_key_v20261103.csv")
OBJ = os.path.join(EXT, "euclid_dr1_eclipse", "ECLIPSE_object_catalogue.csv")


def _tf(s):
    return str(s).strip().lower() in ("true", "1", "t", "yes")


def _fl(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


def load_eclipse():
    obj = {}
    with open(OBJ, newline="") as fh:
        for row in csv.DictReader(fh):
            obj[row["Unique_Identifier"]] = row
    key = []
    with open(KEY, newline="") as fh:
        for row in csv.DictReader(fh):
            key.append(row)
    return key, obj


def select_P(key, obj):
    rows, removed = [], {"theta_E<=0": 0, "theta_e<=0": 0, "n_range": 0, "phz<=0": 0, "mass<=0": 0}
    for r in key:
        o = obj.get(r["unique_identifier"])
        if o is None:
            continue
        if not (r["lens_grade"] == "A" and _tf(r["lens_model_success"]) and _tf(r["final_sample"])
                and not _tf(o["large_system_warning"])):
            continue
        tE, te, n = _fl(r["eclipse_effective_einstein_radius"]), _fl(r["eclipse_effective_radius"]), _fl(r["eclipse_sersic_index"])
        z, m = _fl(r["eclipse_median_phz"]), _fl(r["eclipse_log_survived_mass_med"])
        if not tE > 0:
            removed["theta_E<=0"] += 1; continue
        if not te > 0:
            removed["theta_e<=0"] += 1; continue
        if not (0.6 <= n <= 10):
            removed["n_range"] += 1; continue
        if not z > 0:
            removed["phz<=0"] += 1; continue
        if not m > 0:
            removed["mass<=0"] += 1; continue
        rows.append((r, o))
    return rows, removed


def lens_arrays(rows):
    k = lambda c: np.array([_fl(r[c]) for r, o in rows])
    d = dict(
        uid=np.array([r["unique_identifier"] for r, o in rows]),
        zl=k("eclipse_median_phz"), zlo=k("eclipse_min70_phz"), zhi=k("eclipse_max70_phz"),
        logm=k("eclipse_log_survived_mass_med"), logm_lo=k("eclipse_log_survived_mass_low"),
        logm_hi=k("eclipse_log_survived_mass_upp"),
        tE=k("eclipse_effective_einstein_radius"), tE_lo=k("eclipse_effective_einstein_radius_lower_1_sigma"),
        tE_hi=k("eclipse_effective_einstein_radius_upper_1_sigma"),
        te=k("eclipse_effective_radius"), te_lo=k("eclipse_effective_radius_lower_1_sigma"),
        te_hi=k("eclipse_effective_radius_upper_1_sigma"),
        n=k("eclipse_sersic_index"), ratio=k("eclipse_vis_ratio_ls_l"),
        ra=k("ra"), dec=k("dec"),
        mer=np.array([o["MER_object_id"].strip() for r, o in rows]),
        specz=np.array([_fl(o["desi_deflector_specz"]) for r, o in rows]),
    )
    return d


def load_mer_flux():
    flux = {}
    for f in sorted(glob.glob(os.path.join(EXT, "euclid_dr1_eclipse", "nisp_tables", "mer_*.csv"))):
        with open(f, newline="") as fh:
            for row in csv.DictReader(fh):
                oid = row["object_id"].strip()
                v = _fl(row["flux_detection_total"])
                if oid and np.isfinite(v) and oid not in flux:
                    flux[oid] = v
    return flux


def mer_key(s):
    s = str(s).strip()
    if not s:
        return ""
    try:
        return str(int(float(s))) if "e" in s.lower() or "." in s else str(int(s))
    except ValueError:
        return s


# ---------------------------------------------------------------- COSMOS2020 counts
ZEDGES = np.round(np.arange(0.0, 6.0 + 1e-9, 0.05), 10)
ZC = 0.5 * (ZEDGES[1:] + ZEDGES[:-1])
MEDGES = np.round(np.arange(16.0, 28.0 + 1e-9, 0.1), 10)


def load_cosmos_rows():
    d = os.path.join(EXT, "euc13_population_gate")
    files = sorted(glob.glob(os.path.join(d, "cosmos2020_classic_i*.tsv")))
    pat = re.compile(r"_i([0-9.]+)_([0-9.]+)\.tsv$")
    sl = []
    for f in files:
        m = pat.search(f)
        sl.append((float(m.group(1)), float(m.group(2)), f))
    sl.sort()
    mags, zs, info = [], [], []
    for k, (lo, hi, f) in enumerate(sl):
        last = k == len(sl) - 1
        nraw = nkeep = 0
        header_seen = False
        with open(f) as fh:
            for line in fh:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.rstrip("\n").split("\t")
                if not header_seen:
                    if parts[0].strip() == "HSCimagAuto":
                        header_seen = True
                        cols = [p.strip() for p in parts]
                    continue
                if parts[0].startswith("-") or parts[0].strip() == "mag":
                    continue
                if len(parts) < 3:
                    continue
                rec = dict(zip(cols, [p.strip() for p in parts]))
                try:
                    m_ = float(rec["HSCimagAuto"]); z_ = float(rec["lpzBEST"]); fl = int(rec["FlagCOMBINED"])
                except ValueError:
                    continue
                nraw += 1
                if fl != 0:
                    continue
                if not (lo <= m_ < hi or (last and m_ == hi)):
                    continue
                nkeep += 1
                mags.append(m_); zs.append(z_)
        info.append((os.path.basename(f), lo, hi, nraw, nkeep))
    return np.array(mags), np.array(zs), info


def cosmos_counts(mags, zs):
    ok = np.isfinite(zs) & (zs >= 0) & (zs < 6.0) & (mags >= 16.0) & (mags < 28.0)
    H, _, _ = np.histogram2d(mags[ok], zs[ok], bins=[MEDGES, ZEDGES])
    return H, int(ok.sum())


class Window:
    """Counts in a magnitude window [m-0.25, m+0.25] by exact overlap with the 0.1-mag bins."""

    def __init__(self, H):
        self.cum = np.vstack([np.zeros(H.shape[1]), np.cumsum(H, axis=0)])   # at MEDGES

    def cumulative(self, m):
        m = np.clip(np.asarray(m, float), MEDGES[0], MEDGES[-1])
        pos = (m - MEDGES[0]) / 0.1
        i = np.clip(np.floor(pos).astype(int), 0, len(MEDGES) - 2)
        fr = pos - i
        return self.cum[i] * (1 - fr)[..., None] + self.cum[i + 1] * fr[..., None]

    def counts(self, m):
        return self.cumulative(np.asarray(m) + 0.25) - self.cumulative(np.asarray(m) - 0.25)


MU_GRID = np.exp(np.linspace(math.log(2.0), math.log(30.0), 401))
MU_MID = np.sqrt(MU_GRID[1:] * MU_GRID[:-1])
MU_W = MU_MID ** -3 * np.diff(MU_GRID)
MU_W = MU_W / MU_W.sum()


def n_of_z(win, m_arc, setting):
    """n(z | arc) on ZC for an array of arc magnitudes. Returns (N, 120) and the clamped weight fraction (N,)."""
    m_arc = np.atleast_1d(np.asarray(m_arc, float))
    if setting in ("mu3", "mu10"):
        mu = 3.0 if setting == "mu3" else 10.0
        mi = m_arc + 2.5 * math.log10(mu)
        cl = (mi > 27.5).astype(float)
        c = win.counts(np.minimum(mi, 27.5))
        s = c.sum(axis=1, keepdims=True)
        return c / np.where(s > 0, s, 1.0), cl
    out = np.zeros((len(m_arc), len(ZC)))
    cl = np.zeros(len(m_arc))
    for mu, w in zip(MU_MID, MU_W):
        mi = m_arc + 2.5 * math.log10(mu)
        cl += w * (mi > 27.5)
        out += w * win.counts(np.minimum(mi, 27.5))
    return out, cl


# ---------------------------------------------------------------- published tables
LIT = os.path.join(EXT, "euc10_published_source_z", "lit", "x")


def _num(s):
    s = s.replace("\\^", "").replace("$", "").strip()
    m = re.match(r"^-?[0-9.]+", s)
    return float(m.group(0)) if m else float("nan")


def parse_agel():
    rows = []
    for part in ("redshifts_part1.tex", "redshifts_part2.tex"):
        with open(os.path.join(LIT, "2503.08041", "tables", part)) as fh:
            for line in fh:
                if not line.startswith("AGEL"):
                    continue
                c = [x.strip() for x in line.split("\\\\")[0].split("&")]
                name = c[0]
                rows.append(dict(name=name, sys=name[:-1], arc=name[-1], zs=_num(c[1]), zs_flag=_num(c[2]),
                                 zl=_num(c[4]), zl_lit="\\^" in c[4], ra=_num(c[9]), dec=_num(c[10])))
    return rows


def agel_sample(rule):
    rows = parse_agel()
    systems = {}
    for r in rows:
        systems.setdefault(r["sys"], []).append(r)
    out = []
    for s, arcs in systems.items():
        if rule in ("A1", "A3"):
            a = [x for x in arcs if x["arc"] == "A"]
            if not a:
                continue
            a = a[0]
            fmin = 2 if rule == "A1" else 1
            if np.isfinite(a["zs"]) and a["zs_flag"] >= fmin and np.isfinite(a["zl"]):
                out.append((a["zl"], a["zs"], s, a["ra"], a["dec"]))
        elif rule == "A2":
            good = [x for x in arcs if np.isfinite(x["zs"]) and x["zs_flag"] >= 2 and np.isfinite(x["zl"])]
            if not good:
                continue
            good.sort(key=lambda x: (-x["zs_flag"], x["arc"]))
            a = good[0]
            out.append((a["zl"], a["zs"], s, a["ra"], a["dec"]))
    return out


def parse_slf4():
    path = os.path.join(LIT, "2509.18078", "main.tex")
    with open(path) as fh:
        txt = fh.read()
    start = txt.index("\\label{tab:sourcespositions}")
    start = txt.index("\\endlastfoot", start)
    end = txt.index("\\end{longtable}", start)
    systems = []
    cur = None
    for raw in txt[start:end].split("\n"):
        line = raw.strip()
        if not line or line.startswith("%") or line.startswith("\\hline"):
            continue
        line = line.split("%")[0]
        if "&" not in line:
            continue
        c = [x.strip() for x in line.split("\\\\")[0].split("&")]
        if c[0].startswith("DESI"):
            cur = dict(name=c[0].replace("~", " "), rows=[])
            systems.append(cur)
        obj = c[1]
        zq = _num(c[5]) if len(c) > 5 else float("nan")

        def mag(i):
            if len(c) <= i:
                return float("nan")
            v = c[i].replace(",", "").strip()
            try:
                return float(v)
            except ValueError:
                return float("nan")
        cur["rows"].append(dict(obj=obj, ra=_num(c[2]), dec=_num(c[3]), z=_num(c[4]), q=zq,
                                g=mag(6), r=mag(7), i=mag(8), zmag=mag(9)))
    return systems


def _is_source(obj):
    return obj.startswith("Source")


def _is_lens(obj):
    return obj.startswith("Lens")


def slf4_sample(rule):
    out = []
    for s in parse_slf4():
        lens = [r for r in s["rows"] if _is_lens(r["obj"])]
        src = [r for r in s["rows"] if _is_source(r["obj"])]
        if not lens or not src:
            continue
        L = lens[0]
        if rule in ("S1", "S3"):
            P = src[0]
            if not P["q"] <= 2:
                continue
            if rule == "S3" and not L["q"] <= 2:
                continue
        else:
            good = [r for r in src if r["q"] <= 2]
            if not good:
                continue
            P = good[0]
        out.append((L["z"], P["z"], s["name"], L["ra"], L["dec"], P))
    return out


def vis_proxy(P):
    if np.isfinite(P["i"]):
        return P["i"]
    if np.isfinite(P["r"]) and np.isfinite(P["zmag"]):
        return -2.5 * math.log10(0.5 * (10 ** (-0.4 * P["r"]) + 10 ** (-0.4 * P["zmag"])))
    return float("nan")


def load_slacs():
    path = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
    rows = []
    header = None
    with open(path) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if header is None:
                header = [p.strip() for p in parts]
                continue
            if parts[0].strip() in ("", "-" * 8) or parts[0].startswith("-"):
                continue
            rec = dict(zip(header, [p.strip() for p in parts]))
            if not rec.get("recno", "").isdigit():
                continue
            rows.append(rec)
    return rows


def sexa_to_deg(ra, dec):
    h, m, s = [float(x) for x in ra.split()]
    sign = -1 if dec.strip().startswith("-") else 1
    d, dm, ds = [abs(float(x)) for x in dec.split()]
    return 15 * (h + m / 60 + s / 3600), sign * (d + dm / 60 + ds / 3600)
