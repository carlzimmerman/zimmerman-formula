"""CFG233 common: repo locator, data loaders, re-implemented kernels, Theil-Sen, bootstrap, classifier, tee.
Referee re-derivation of CFG216 from CFG233_FROZEN_CRITERIA.md (sha256 00fdd777...). Repo is read-only."""
import os, sys, math, json, csv, io
import numpy as np
from scipy import special, optimize

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    cands = []
    if os.environ.get("ZF_REPO"):
        cands.append(os.environ["ZF_REPO"])
    for start in (HERE, os.getcwd()):
        p = start
        for _ in range(12):
            cands.append(p)
            p = os.path.dirname(p)
    cands.append(os.path.expanduser("~/new_physics/zimmerman-formula"))
    for c in cands:
        if os.path.isfile(os.path.join(c, "real_research", "data", "rc100_nestorshachar2023_table3.csv")):
            return c
    raise SystemExit("repo not found; set ZF_REPO")


REPO = find_repo()
DATA = os.environ.get("DATA", "committed").strip().lower()     # committed (the CSV CFG216 used) | corrected (six fields, paper values; data_assembly/rc100_provenance)
assert DATA in ("committed", "corrected")
TABLES = {"committed": os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"),
          "corrected": os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")}
TABLE = TABLES[DATA]
SUF = "__" + DATA.upper()
RC41CSV = os.path.join(REPO, "data_assembly", "price2021_rc41", "price2021_rc41.csv")
PHIBSS = os.path.join(REPO, "data_assembly", "kmos3d_phibss", "phibss13_joined.csv")

G = 6.6743e-11
KPC = 3.0856775814913673e19
MSUN = 1.98847e30
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}  # shared constants: values printed by C4 from CFG4_common (criteria quoted 9.3603e-11 / 1.1312e-10)
OM = 0.315
SEED_MAIN, SEED_ALT = 233, 234


class Tee:
    def __init__(self, path):
        self.f = open(path, "w")
        self.so = sys.__stdout__
        self.subs = [(REPO, "<repo>"), (HERE, "<scratch>"), (os.path.expanduser("~"), "~")]

    def _clean(self, s):
        for a, b in self.subs:
            s = s.replace(a, b)
        return s

    def write(self, s):
        s = self._clean(s)
        self.f.write(s)
        self.so.write(s)

    def flush(self):
        self.f.flush(); self.so.flush()


def start(name):
    t = Tee(os.path.join(HERE, name + SUF + ".out"))
    sys.stdout = t
    print("<repo> =", "<repo>", "| <scratch> =", "<scratch>", "| DATA =", DATA.upper(), "(", os.path.relpath(TABLE, REPO), ")")
    return t


def savejson(name, obj):
    def conv(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        raise TypeError(type(o))
    with open(os.path.join(HERE, name + SUF + "_results.json"), "w") as f:
        json.dump(obj, f, indent=1, default=conv)


# ------------------------------------------------------------------ cosmology and kernels (re-implemented)
def E_of_z(z):
    z = np.asarray(z, float)
    return np.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def _h_rar(y):
    y = np.asarray(y, float)
    return y / np.expm1(np.sqrt(y))


def _dh(t):
    s = math.sqrt(t)
    e = math.expm1(s)
    return (2 * e - s * (1 + e)) / (2 * e ** 2)


_YP = optimize.brentq(_dh, 1.0, 5.0)
_HP = float(_h_rar(_YP))
_DELTA = 0.05
_YS = optimize.brentq(lambda t: _dh(t) - _DELTA * _HP / (t + _YP), 1.0, _YP)


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    yr = np.minimum(y, _YS)
    h = np.where(y <= _YS, _h_rar(yr), float(_h_rar(_YS)) + _DELTA * _HP * np.log((y + _YP) / (_YS + _YP)))
    return 1.0 + h / y


def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def nu_simple(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


KERNELS = {"nu_mono": nu_mono, "P2": nu_p2, "simple": nu_simple}


def c4_crosscheck():
    """C4: compare the re-implemented nu_mono to the repo's imported object (read-only import)."""
    try:
        sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
        import CFG4_common as C4  # noqa
        y = np.logspace(-6, 4, 2001)
        dif = float(np.max(np.abs(C4.nu_mono(y) / nu_mono(y) - 1)))
        dif2 = float(np.max(np.abs(C4.nu_p2(y) / nu_p2(y) - 1)))
        a0 = (float(C4.A0["canonical"]), float(C4.A0["alt"]))
        return dict(ok=True, max_rel_diff_nu_mono=dif, max_rel_diff_p2=dif2, a0_canon_alt=a0,
                    a0_match=bool(abs(a0[0] - A0["canonical"]) < 1e-15 and abs(a0[1] - A0["alt"]) < 1e-15),
                    y_star=_YS, y_peak=_YP)
    except Exception as e:  # keep and report
        return dict(ok=False, error=repr(e)[:200], y_star=_YS, y_peak=_YP)


def a0_of(law, z, foot="canonical"):
    z = np.asarray(z, float)
    return A0[foot] * (E_of_z(z) if law == "rival" else np.ones_like(z))


def invert_gbar(gobs, a0, kern):
    """solve g_bar * nu(g_bar/a0) = g_obs for g_bar (vectorised bisection in log10 y)."""
    gobs = np.asarray(gobs, float); a0 = np.broadcast_to(np.asarray(a0, float), gobs.shape)
    x = gobs / a0
    lo = np.full(gobs.shape, -14.0); hi = np.full(gobs.shape, 14.0)
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        y = 10 ** mid
        v = y * kern(y)
        up = v < x
        lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
    return a0 * 10 ** (0.5 * (lo + hi))


def delta_of(D, gbar, z, law, kern="nu_mono", foot="canonical"):
    a0 = a0_of(law, z, foot)
    return np.log10(np.asarray(D, float) / KERNELS[kern](np.asarray(gbar, float) / a0))


# ------------------------------------------------------------------ data
def load_rc100(which=None):
    rows = list(csv.DictReader(open(TABLES[which] if which else TABLE)))
    def fl(k):
        out = []
        for r in rows:
            try:
                out.append(float(r[k]))
            except Exception:
                out.append(float("nan"))
        return np.array(out)
    d = dict(name=[r["name"] for r in rows], z=fl("z"), logM=fl("logMbar_Msun"), Re=fl("Re_kpc"),
             f=fl("fDM_within_Re"), Vc=fl("Vc_Re_kms"), s0=fl("sigma0_kms"))
    ok = np.isfinite(d["z"]) & np.isfinite(d["Re"]) & np.isfinite(d["Vc"]) & np.isfinite(d["f"]) & (d["f"] > 0) & (d["f"] < 1)
    d["idx"] = np.array([int(r["idx"]) for r in rows])[ok]
    d["ok"] = ok
    d["n_all"] = len(rows); d["n_excl"] = int((~ok).sum())
    for k in ("z", "logM", "Re", "f", "Vc", "s0"):
        d[k] = d[k][ok]
    d["name"] = [n for n, o in zip(d["name"], ok) if o]
    d["gobs"] = (d["Vc"] * 1e3) ** 2 / (d["Re"] * KPC)
    d["gbar"] = (1 - d["f"]) * d["gobs"]
    d["D"] = 1.0 / (1 - d["f"])
    return d


def sub(d, m):
    m = np.asarray(m, bool)
    out = {}
    for k, v in d.items():
        if isinstance(v, np.ndarray) and v.shape == m.shape:
            out[k] = v[m]
        elif isinstance(v, list) and len(v) == len(m):
            out[k] = [x for x, o in zip(v, m) if o]
        else:
            out[k] = v
    return out


def load_rc41():
    rows = list(csv.DictReader(open(RC41CSV)))
    return rows


def rc41_match(d):
    """names: RC41 id with '_' -> ' ' exact match to RC100 name. returns mask over d, list matched, unmatched"""
    rc = load_rc41()
    ids = [r["id"].replace("_", " ") for r in rc]
    names = d["name"]
    m = np.array([n in ids for n in names])
    matched = [i for i in ids if i in names]
    unmatched = [r["id"] for r in rc if r["id"].replace("_", " ") not in names]
    return m, matched, unmatched, rc


def load_phibss():
    return list(csv.DictReader(open(PHIBSS)))


# ------------------------------------------------------------------ Theil-Sen and bootstrap
_TRI = {}


def _tri(n):
    if n not in _TRI:
        _TRI[n] = np.triu_indices(n, 1)
    return _TRI[n]


def ts_batch(z_b, d_b, chunk_elems=6_000_000):
    """Theil-Sen slope (median of pairwise slopes over pairs with z_i != z_j), row-wise. z_b,d_b: (B,n)."""
    z_b = np.atleast_2d(z_b); d_b = np.atleast_2d(d_b)
    B, n = z_b.shape
    I, J = _tri(n)
    P = len(I)
    out = np.empty(B)
    step = max(1, chunk_elems // P)
    for a in range(0, B, step):
        zz = z_b[a:a + step]; dd = d_b[a:a + step]
        dz = zz[:, J] - zz[:, I]
        valid = dz != 0
        sl = np.where(valid, (dd[:, J] - dd[:, I]) / np.where(valid, dz, 1.0), np.inf)
        m = valid.sum(1)
        sl.sort(axis=1)
        r = np.arange(len(zz))
        lo = np.clip((m - 1) // 2, 0, P - 1); hi = np.clip(m // 2, 0, P - 1)
        out[a:a + step] = 0.5 * (sl[r, lo] + sl[r, hi])
    return out


def ts(z, d):
    return float(ts_batch(np.asarray(z)[None], np.asarray(d)[None])[0])


def boot_idx(n, B, seed):
    return np.random.default_rng(seed).integers(0, n, (B, n))


def boot_ts(z, dlist, B, seed, chunk=None):
    """bootstrap of galaxies; same resamples for every quantity in dlist. returns (len(dlist), B)."""
    z = np.asarray(z); n = len(z)
    idx = boot_idx(n, B, seed)
    res = np.empty((len(dlist), B))
    step = 400
    for a in range(0, B, step):
        ii = idx[a:a + step]
        zb = z[ii]
        for k, dv in enumerate(dlist):
            res[k, a:a + step] = ts_batch(zb, np.asarray(dv)[ii])
    return res


def ci(x, lo=2.5, hi=97.5):
    return float(np.percentile(x, lo)), float(np.percentile(x, hi))


def classify(fl_ci, rv_ci):
    f_has0 = fl_ci[0] <= 0 <= fl_ci[1]
    r_has0 = rv_ci[0] <= 0 <= rv_ci[1]
    if f_has0 and rv_ci[1] < 0:
        return "W-flat"
    if fl_ci[0] > 0 and r_has0:
        return "W-rival"
    if f_has0 and r_has0:
        return "W-none"
    return "W-mixed"


def label_level(c):
    return "over" if c[0] > 0 else ("under" if c[1] < 0 else "consistent")


def boot_median_ci(x, B, seed):
    x = np.asarray(x); n = len(x)
    idx = boot_idx(n, B, seed)
    m = np.median(x[idx], axis=1)
    return float(np.median(x)), ci(m)


def delta_pair(D, gbar, z, kern="nu_mono", foot="canonical"):
    return delta_of(D, gbar, z, "flat", kern, foot), delta_of(D, gbar, z, "rival", kern, foot)


def expected_slopes(gobs, z, kern="nu_mono", foot="canonical"):
    """slopes of (delta_flat, delta_rival) under flat-true and rival-true (baryons from inversion)."""
    out = {}
    for T in ("flat", "rival"):
        gb = invert_gbar(gobs, a0_of(T, z, foot), KERNELS[kern])
        D = gobs / gb
        out[T] = (ts(z, delta_of(D, gb, z, "flat", kern, foot)), ts(z, delta_of(D, gb, z, "rival", kern, foot)))
    return out  # out[T] = (slope of delta_flat, slope of delta_rival)


def freeman_gbar(logM, Re):
    M = 10 ** np.asarray(logM, float) * MSUN
    Rd = np.asarray(Re, float) / 1.678
    y = 1.678 / 2.0
    fac = y ** 2 * (special.i0(y) * special.k0(y) - special.i1(y) * special.k1(y))
    return 2 * G * M / (Rd * KPC) * fac / (np.asarray(Re, float) * KPC)
