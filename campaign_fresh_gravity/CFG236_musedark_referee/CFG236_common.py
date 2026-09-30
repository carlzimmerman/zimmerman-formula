"""CFG236 common code (referee re-derivation of CFG198 + CFG199).  Written from CFG236_FROZEN_CRITERIA.md only.
No absolute home path is ever printed: REPO -> <repo>, EXT -> <ext>, scratch -> <scratch>.
Repo is found from ZF_REPO, else by walking up from this file, else ~/new_physics/zimmerman-formula.  Repo is only read.
"""
import os, sys, json, math, csv, hashlib, re
import numpy as np
from scipy import special, stats

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    e = os.environ.get("ZF_REPO")
    if e and os.path.isdir(e):
        return os.path.abspath(e)
    d = HERE
    for _ in range(12):
        if os.path.isdir(os.path.join(d, "data_assembly", "musedark_catalogues")):
            return d
        d = os.path.dirname(d)
    return os.path.expanduser("~/new_physics/zimmerman-formula")


REPO = find_repo()
EXT = os.path.join(os.path.dirname(REPO), "_external_data", "muse_dark", "numeric")
EXT_CAT = os.path.join(os.path.dirname(REPO), "_external_data", "muse_dark")
CAT = os.path.join(REPO, "data_assembly", "musedark_catalogues")
HOME = os.path.expanduser("~")


def san(s):
    s = str(s)
    for a, b in ((EXT, "<ext>"), (EXT_CAT, "<ext>"), (REPO, "<repo>"), (HERE, "<scratch>"), (HOME, "~")):
        s = s.replace(a, b)
    return s


class Out:
    def __init__(self, name):
        suf = os.environ.get("CFG236_SUFFIX", "")
        self.name = f"CFG236_{name}{suf}"
        self.f = open(os.path.join(HERE, self.name + ".out"), "w")
        self.res = {}

    def P(self, *a):
        t = san(" ".join(str(x) for x in a))
        print(t)
        self.f.write(t + "\n")
        self.f.flush()

    def finish(self):
        self.f.close()
        with open(os.path.join(HERE, self.name + "_results.json"), "w") as fh:
            json.dump(jclean(self.res), fh, indent=1)


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    return o


# ---------------------------------------------------------------- constants
G = 4.30091e-6               # kpc (km/s)^2 / Msun
CONV = 1e6 / 3.0856775814913673e19   # (km/s)^2/kpc -> m/s^2
A0_CAN, A0_ALT = 9.3603e-11, 1.1312e-10
LOG_CAN, LOG_ALT = math.log10(A0_CAN), math.log10(A0_ALT)
OM = 0.315


def Ez(z):
    return np.sqrt(OM * (1 + z) ** 3 + 1 - OM)


# ---------------------------------------------------------------- data
def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


NUM_STR = ("adrift", "rotation_curve", "dispersion_profile", "thickness_profile")


def load_numeric():
    rows = list(csv.DictReader(open(os.path.join(CAT, "musedark_numeric.csv"))))
    T = {}
    for k in rows[0]:
        T[k] = np.array([r[k] for r in rows]) if k in NUM_STR else np.array([_f(r[k]) for r in rows])
    return T


def load_joined():
    rows = list(csv.DictReader(open(os.path.join(CAT, "musedark_joined.csv"))))
    return {int(r["muse_id"]): r for r in rows}


def sample(T, verbose=None):
    """the frozen sample chain.  returns (index array, counts dict)."""
    n0 = len(T["z"])
    fin = np.ones(n0, bool)
    for k in ("z", "logMstar_phot", "DC14_logMdisk", "fDM_at_Re", "Re_kpc", "gas_density_Msun_pc2"):
        fin &= np.isfinite(T[k])
    bulge_all = int(np.sum(T["has_bulge"] == 1))
    m1 = fin
    bulge_in = int(np.sum(m1 & (T["has_bulge"] == 1)))
    m2 = m1 & (T["has_bulge"] == 0)
    m3 = m2 & (T["fDM_at_Re"] > 0) & (T["fDM_at_Re"] < 1)
    c = dict(n_rows=n0, n_finite=int(m1.sum()), bulge_all=bulge_all, bulge_in_finite=bulge_in,
             n_disc=int(m2.sum()), n_S=int(m3.sum()))
    return np.where(m3)[0], c


# ---------------------------------------------------------------- physics
def y2_term(y):
    return y * y * (special.i0(y) * special.k0(y) - special.i1(y) * special.k1(y))


def g_disc(M, R, Rd):
    """thin exponential disc, (km/s)^2/kpc at radius R (kpc), M in Msun."""
    y = R / (2.0 * Rd)
    v2 = 2.0 * G * M / Rd * y2_term(y)
    return v2 / R


def g_hi(Sig):
    return math.pi * G * np.asarray(Sig, float) * 1e6


def mu_mol(z, logM, scale=1.0, natlog=False):
    lz = np.log(1 + z) if natlog else np.log10(1 + z)
    return scale * 10 ** (0.06 - 3.3 * (lz - 0.65) ** 2 - 0.41 * (logM - 10.7))


def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


_NU_MONO = None


def nu_mono_import():
    """labelled import row only: CFG4_common's FP1 nu_mono (shared object; independence stops)."""
    global _NU_MONO
    if _NU_MONO is None:
        try:
            sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                import CFG4_common as C
            _NU_MONO = C.nu_mono
        except Exception as e:  # noqa
            _NU_MONO = False
            print("nu_mono import failed:", type(e).__name__)
    return _NU_MONO or None


KERN = {"RAR": nu_rar, "P2": nu_p2}


def get_kernel(name):
    if name == "mono":
        k = nu_mono_import()
        if k is None:
            raise RuntimeError("nu_mono unavailable")
        return k
    return KERN[name]


def invert(D, kern):
    """y* with nu(y*) = D by vectorised bisection in ln y; NaN where D <= 1 (nu > 1 always)."""
    D = np.asarray(D, float)
    out = np.full(D.shape, np.nan)
    ok = np.isfinite(D) & (D > 1.0)
    if not ok.any():
        return out
    d = D[ok]
    lo = np.full(d.shape, -25.0)
    hi = np.full(d.shape, 25.0)
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        v = np.asarray(kern(np.exp(mid)), float)
        big = v > d          # nu too large -> y too small -> move lo up
        lo = np.where(big, mid, lo)
        hi = np.where(big, hi, mid)
    out[ok] = np.exp(0.5 * (lo + hi))
    return out


def a0_from(gbar, D, kern, floor=1.05):
    """a0 = gbar / y*(D); NaN where D <= floor; a0bound = value at D = floor (upper bound for censored rows)."""
    D = np.asarray(D, float)
    Dv = np.where(D > floor, D, np.nan)
    ys = invert(Dv, kern)
    a0 = gbar / ys
    Db = np.full(D.shape, floor)
    bound = gbar / invert(Db, kern)
    return a0, bound


# ---------------------------------------------------------------- routes
def get_cols(T, idx):
    g = lambda k: T[k][idx]
    return dict(z=g("z"), Re=g("Re_kpc"), fDM=g("fDM_at_Re"), logMfit=g("DC14_logMdisk"),
                logMsed=g("logMstar_phot"), Sig=g("gas_density_Msun_pc2"), incl=g("incl_deg"),
                v22=g("v22"), logMdyn=g("logMdyn"), sig_fit=g("sigma_fit_kms"))


def routes(C, cfg=None):
    """cfg keys: mode 'R198'|'R199'; gperp (R199, (km/s)^2/kpc); kernel; Sig (override array or scalar); mu_scale;
    tH (H2 z-tilt, dex/z); tau, off (SED bias); floor; accscale (multiplicative array on all accelerations); natlog; zmed."""
    cfg = cfg or {}
    mode = cfg.get("mode", "R198")
    kern = get_kernel(cfg.get("kernel", "RAR"))
    z, Re, fDM = C["z"], C["Re"], C["fDM"]
    zmed = cfg.get("zmed", np.median(z))
    Rd = Re / 1.678
    Sig0 = C["Sig"]
    Sig = Sig0 if cfg.get("Sig") is None else np.broadcast_to(np.asarray(cfg["Sig"], float), Sig0.shape)
    gcoef = cfg.get("gcoef", 1.0)
    acc = cfg.get("accscale", 1.0)
    logMs = C["logMsed"] - cfg.get("tau", 0.0) * (z - zmed) - cfg.get("off", 0.0)
    mu = mu_mol(z, logMs, cfg.get("mu_scale", 1.0), cfg.get("natlog", False)) * 10 ** (cfg.get("tH", 0.0) * (z - zmed)) * cfg.get("mu_fac", 1.0)
    M = {"i": 10 ** C["logMfit"], "ii": 10 ** logMs * (1 + mu), "iii": 10 ** logMs}
    if cfg.get("swap") and mode == "R198":
        M["i"], M["ii"] = M["ii"], M["i"]
    gd = {r: g_disc(M[r], Re, Rd) * acc for r in M}
    ghi = gcoef * g_hi(Sig) * acc
    out = {"mu": mu, "z": z}
    if mode == "R198":
        gfit0 = g_disc(10 ** C["logMfit"], Re, Rd) + gcoef * g_hi(Sig0)
        gobs = gfit0 / (1 - fDM) * acc          # the model's total, from the fitted mass and fitted Sigma_HI; held fixed
        if cfg.get("gobs_fixed") is not None:
            gobs = np.asarray(cfg["gobs_fixed"], float) * acc
        gb = {r: gd[r] + ghi for r in M}
        Dd = {r: gobs / gb[r] for r in M}
        out["gobs"] = gobs
    else:
        gperp = np.asarray(cfg["gperp"], float) * acc
        gbi = (1 - fDM) * gperp
        gdf = g_disc(10 ** C["logMfit"], Re, Rd) * acc
        rho = {r: (gd[r] + ghi) / (gdf + ghi) for r in ("ii", "iii")}
        if cfg.get("swap"):
            rho = {r: 1.0 / rho[r] for r in rho}
        gb = {"i": gbi, "ii": gbi * rho["ii"], "iii": gbi * rho["iii"]}
        Dd = {"i": np.full(z.shape, 1.0) / (1 - fDM), "ii": gperp / gb["ii"], "iii": gperp / gb["iii"]}
        out["gobs"] = gperp
    floor = cfg.get("floor", 1.05)
    for r in M:
        a0, bd = a0_from(gb[r], Dd[r], kern, floor)
        out["a0_" + r] = a0
        out["bound_" + r] = bd
        out["D_" + r] = Dd[r]
        out["gb_" + r] = gb[r]
    return out


# ---------------------------------------------------------------- slopes
def ts_pairs(z, y):
    dz = z[None, :] - z[:, None]
    dy = y[None, :] - y[:, None]
    with np.errstate(all="ignore"):
        S = np.where(dz != 0, dy / dz, np.nan)
    return S


def theil_sen(z, y):
    m = np.isfinite(y) & np.isfinite(z)
    z, y = z[m], y[m]
    n = len(z)
    if n < 3:
        return float("nan")
    iu = np.triu_indices(n, 1)
    S = ts_pairs(z, y)[iu]
    S = S[np.isfinite(S)]
    return float(np.median(S)) if len(S) else float("nan")


def ols(z, y):
    m = np.isfinite(y) & np.isfinite(z)
    return float(np.polyfit(z[m], y[m], 1)[0])


def boot_slopes(z, cols, B, seed, pairs_of=None):
    """bootstrap over galaxies.  cols: dict name -> y array (NaN = undefined, dropped per quantity).
    pairs_of: dict name -> tuple of col names whose joint validity defines a 'paired' quantity (difference of slopes
    on the intersection): value = slope(a on intersection) - slope(b on intersection) with pairs_of[name]=(a, b)."""
    n = len(z)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(B, n))
    iu0, iu1 = np.triu_indices(n, 1)
    mats = {k: ts_pairs(z, v) for k, v in cols.items()}
    pm = {}
    if pairs_of:
        for name, (a, b) in pairs_of.items():
            both = np.isfinite(cols[a]) & np.isfinite(cols[b])
            ya = np.where(both, cols[a], np.nan)
            yb = np.where(both, cols[b], np.nan)
            pm[name] = (ts_pairs(z, ya), ts_pairs(z, yb))
    res = {k: np.empty(B) for k in list(cols) + list(pairs_of or {})}
    for t in range(B):
        ii = idx[t]
        a, b = ii[iu0], ii[iu1]
        for k, M in mats.items():
            v = M[a, b]
            v = v[np.isfinite(v)]
            res[k][t] = np.median(v) if len(v) else np.nan
        for name, (Ma, Mb) in pm.items():
            va = Ma[a, b]
            va = va[np.isfinite(va)]
            vb = Mb[a, b]
            vb = vb[np.isfinite(vb)]
            res[name][t] = (np.median(vb) - np.median(va)) if len(va) and len(vb) else np.nan
    return res


def ci(x, lo=2.5, hi=97.5):
    x = x[np.isfinite(x)]
    return float(np.percentile(x, lo)), float(np.percentile(x, hi))


def sd(x):
    x = x[np.isfinite(x)]
    return float(np.std(x))


def slope_table(z, cols, B, seed, pairs_of=None):
    """returns dict name -> dict(b, lo, hi, sd, n)"""
    bs = boot_slopes(z, cols, B, seed, pairs_of)
    out = {}
    for k, v in cols.items():
        out[k] = dict(b=theil_sen(z, v), n=int(np.isfinite(v).sum()))
    if pairs_of:
        for name, (a, b) in pairs_of.items():
            both = np.isfinite(cols[a]) & np.isfinite(cols[b])
            ya = np.where(both, cols[a], np.nan)
            yb = np.where(both, cols[b], np.nan)
            out[name] = dict(b=theil_sen(z, yb) - theil_sen(z, ya), n=int(both.sum()))
    for k in out:
        lo, hi = ci(bs[k])
        out[k].update(lo=lo, hi=hi, sd=sd(bs[k]))
    return out, bs


def ref_slopes(z):
    return dict(flat=0.0, Ez=ols(z, np.log10(Ez(z))), III=ols(z, np.log10(1 + 1.59 * z)))


def classify(st, refs):
    """which reference slopes are INSIDE / OUTSIDE the 95% CI; signed distance in bootstrap SD."""
    r = {}
    for k, v in refs.items():
        inside = st["lo"] <= v <= st["hi"]
        r[k] = dict(inside=bool(inside), dist_sd=(st["b"] - v) / st["sd"] if st["sd"] > 0 else float("nan"))
    return r


def outside_set(st, refs):
    return [k for k, v in classify(st, refs).items() if not v["inside"]]


def wilson(k, n, zc=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + zc ** 2 / n
    c = (p + zc ** 2 / (2 * n)) / den
    h = zc * math.sqrt(p * (1 - p) / n + zc ** 2 / (4 * n * n)) / den
    return (c - h, c + h)


# ---------------------------------------------------------------- external data (.dat)
def verify_hashes(out=None):
    """verify the 882 files against the repo's numeric manifest, and the 9 catalogue files against manifest.json."""
    res = dict(n_listed=0, n_ok=0, n_bad=0, n_missing=0, bad=[], cat_ok=0, cat_bad=0, cat_missing=0)
    for line in open(os.path.join(CAT, "numeric_manifest_sha256.txt")):
        p = line.split()
        if len(p) != 2:
            continue
        h, rel = p
        res["n_listed"] += 1
        fp = os.path.join(EXT, rel)
        if not os.path.exists(fp):
            res["n_missing"] += 1
            continue
        hh = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        if hh == h:
            res["n_ok"] += 1
        else:
            res["n_bad"] += 1
            res["bad"].append(rel)
    mj = json.load(open(os.path.join(CAT, "manifest.json")))
    for name, d in mj.items():
        fp = os.path.join(EXT_CAT, name)
        if not os.path.exists(fp):
            res["cat_missing"] += 1
            continue
        if hashlib.sha256(open(fp, "rb").read()).hexdigest() == d["sha256"]:
            res["cat_ok"] += 1
        else:
            res["cat_bad"] += 1
    return res


def read_vrot(n):
    fp = os.path.join(EXT, f"ID{int(n):04d}", f"DC14_{int(n)}_true_Vrot.dat")
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in open(fp) if l.strip()]
    return np.array([[float(c) for c in r] for r in rows[1:]])


def at_radius(A, x, col):
    """mean over the two sides of |A[:,col]| at |rad_Re| = x (linear interpolation per side; one side if only one reaches)."""
    vals = []
    for sgn in (1, -1):
        m = sgn * A[:, 1] > 0
        r = np.abs(A[m, 1])
        if len(r) < 2 or r.max() < x or r.min() > x:
            continue
        o = np.argsort(r)
        vals.append(np.interp(x, r[o], np.abs(A[m, col])[o]))
    return float(np.mean(vals)) if vals else float("nan")


def load_dat(T, idx):
    """for galaxies idx: v_f, sigma_f at 1.0 R_e and at 1.311 R_e (=2.2 R_d); dict of arrays"""
    out = {k: np.empty(len(idx)) for k in ("v1", "s1", "v22r", "s22r")}
    for j, i in enumerate(idx):
        A = read_vrot(int(T["muse_id"][i]))
        out["v1"][j] = at_radius(A, 1.0, 3)
        out["s1"][j] = at_radius(A, 1.0, 4)
        out["v22r"][j] = at_radius(A, 2.2 / 1.678, 3)
        out["s22r"][j] = at_radius(A, 2.2 / 1.678, 4)
    return out


def dat_available():
    return os.path.isdir(EXT)


def gperp_reading(v1, Re, incl, reading="a", sig1=None, drift=None):
    """g_perp (or g_c) in (km/s)^2/kpc.  reading a: v_perp = v_f; b: v_perp = v_f / sin i.
    drift None|'D1'|'D2': v_c^2 = v_perp^2 + v_AD^2 at R_e (D1: 0.92 sigma^2 (R_e/R_d); D2: 0.92 (0.15)^2 (R_e/R_d) v_c^2)."""
    v = v1 / np.sin(np.radians(incl)) if reading == "b" else v1
    v2 = v * v
    if drift == "D1":
        v2 = v2 + 0.92 * 1.678 * sig1 ** 2
    elif drift == "D2":
        v2 = v2 / (1 - 0.92 * 0.15 ** 2 * 1.678)
    return v2 / Re


def level_log(a0_internal):
    return np.log10(a0_internal * CONV)


def thirds(z):
    o = np.argsort(z, kind="stable")
    return np.array_split(o, 3)


def boot_median(x, B, seed):
    x = x[np.isfinite(x)]
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    m = np.median(x[idx], axis=1)
    return ci(m)


def header(o, title):
    o.P(f"# {title}")
    o.P(f"repo=<repo>  ext=<ext>  numpy {np.__version__}  scipy {__import__('scipy').__version__}")
