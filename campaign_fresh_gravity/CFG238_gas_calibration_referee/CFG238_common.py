#!/usr/bin/env python3
"""CFG238 common module (referee of CFG224 / CFG224b). Own code; imports nothing from any CFG224 file.
Repo locator: ZF_REPO env or walk up from __file__ or cwd; outputs print <repo>, <scratch>, <ext>, <home> only."""
import os, sys, re, csv, json, math, hashlib, itertools
import numpy as np
import warnings
# macOS Accelerate BLAS raises spurious floating-point-flag RuntimeWarnings on matmul (results verified equal to lstsq to 1e-15); silenced.
warnings.filterwarnings('ignore', category=RuntimeWarning)

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    e = os.environ.get("ZF_REPO")
    if e and os.path.isdir(e):
        return os.path.abspath(e)
    for start in (HERE, os.getcwd()):
        p = start
        for _ in range(12):
            if os.path.isdir(os.path.join(p, "data_assembly", "multitracer_gas")):
                return p
            p = os.path.dirname(p)
    raise SystemExit("ZF_REPO not found")


REPO = find_repo()
SCR = HERE
EXT = os.environ.get("ZF_EXT") or os.path.join(os.path.dirname(REPO), "_external_data", "cds_tables")
HOME = os.path.expanduser("~")
MT = os.path.join(REPO, "data_assembly", "multitracer_gas")
DU = os.path.join(MT, "dunne2022")
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
NO = os.path.join(REPO, "data_assembly", "noema3d")
RAW = os.path.join(MT, "raw_small")


def clean(s):
    for a, b in ((SCR, "<scratch>"), (REPO, "<repo>"), (EXT, "<ext>"), (HOME, "<home>")):
        s = s.replace(a, b)
    return s


class Tee:
    def __init__(self, path):
        self.f = open(path, "w")
        self.lines = []

    def __call__(self, *a):
        s = clean(" ".join(str(x) for x in a))
        print(s)
        self.f.write(s + "\n")
        self.f.flush()

    def close(self):
        self.f.close()


def out_paths(name):
    mode = os.environ.get("MUTATE")
    suf = f"_M{mode}" if mode else ""
    return os.path.join(SCR, f"{name}{suf}.out"), os.path.join(SCR, f"{name}{suf}_results.json")


def dump(path, obj):
    def conv(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (set, tuple)):
            return list(o)
        return str(o)
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=1, default=conv)


def fl(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except Exception:
        return None


def readcsv(path):
    return list(csv.DictReader(open(path, encoding="utf8", errors="ignore")))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- statistics
def msd(d):
    d = np.asarray(d, float)
    n = len(d)
    mu = d.mean()
    s = d.std(ddof=1) if n > 1 else float("nan")
    return dict(N=n, mean=mu, sd=s, se=s / math.sqrt(n) if n > 1 else float("nan"),
                median=float(np.median(d)), mad=float(1.4826 * np.median(np.abs(d - np.median(d)))))


def Kfun(mu, se):
    return math.sqrt(se ** 2 + (abs(mu) / 2) ** 2)


def Kclass(K):
    return ("below the CFG223 range" if K < 0.05 else "inside the CFG223 range" if K < 0.10
            else "between CFG223 and CFG221" if K < 0.15 else "at or above the CFG221 requirement")


def boot_mean_ci(d, B=10000, seed=238):
    rng = np.random.default_rng(seed)
    d = np.asarray(d, float)
    m = d[rng.integers(0, len(d), (B, len(d)))].mean(1)
    return float(np.percentile(m, 16)), float(np.percentile(m, 84))


def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    n, p = X.shape
    s2 = res @ res / (n - p)
    cov = s2 * np.linalg.inv(X.T @ X)
    return beta, np.sqrt(np.diag(cov)), float(np.sqrt(s2))


def ols_boot(X, y, B=10000, seed=238):
    rng = np.random.default_rng(seed)
    n, p = X.shape
    out = np.empty((B, p))
    chunk = 2000
    i = 0
    while i < B:
        m = min(chunk, B - i)
        idx = rng.integers(0, n, (m, n))
        Xb = X[idx]
        yb = y[idx]
        A = np.einsum("bni,bnj->bij", Xb, Xb)
        r = np.einsum("bni,bn->bi", Xb, yb)
        out[i:i + m] = np.linalg.solve(A, r[..., None])[..., 0]
        i += m
    return out


def design(x, L=None, extra=None):
    cols = [np.ones_like(x), x]
    if L is not None:
        cols.append(L - 11.7)
    if extra is not None:
        cols += list(extra)
    return np.column_stack(cols)


# ---------------------------------------------------------------- Dunne+22
def norm_name(s):
    return re.sub(r"[\s*]", "", s.lower())


FLAGS = ["SMG", "MS", "SLUGs", "B19", "VALES", "S16local", "S16SMG", "V20"]


def load_master():
    M = readcsv(os.path.join(DU, "dunne2022_master.csv"))
    keys = {}
    for i, r in enumerate(M):
        for k in ("Name", "OName", "SimbadName"):
            keys.setdefault(norm_name(r[k]), set()).add(i)
    return M, keys


TABLES = ("ad", "dax", "xa", "xd")


def load_opt(t):
    return readcsv(os.path.join(DU, f"dunne2022_opt_{t}.csv"))


FACTORS = {  # (table, column, label)
    ("ad", "aCO"): "alpha_CO", ("dax", "aCO"): "alpha_CO", ("xa", "aCO"): "alpha_CO",
    ("dax", "XCI"): "X_CI", ("xa", "XCI"): "X_CI", ("xd", "XCI"): "X_CI",
    ("ad", "kappaH"): "kappa_H", ("dax", "GDR"): "GDR", ("xd", "GDR"): "GDR",
}
COMBOS = list(FACTORS.keys())
ERRCOL = {"aCO": "e_aCO", "XCI": "e_XCI", "kappaH": "e_kappaH", "GDR": "e_GDR"}

_cache = {}


def joined(t):
    """Rows of opt table t joined to the master by D1. Returns (rows, info); each row is the opt dict plus z, LIRm, flags, master index."""
    if t in _cache:
        return _cache[t]
    M, keys = load_master()
    R = load_opt(t)
    rows = []
    unmatched = []
    amb = []
    for r in R:
        s = keys.get(norm_name(r["Name"]), set())
        if not s:
            unmatched.append(r["Name"])
            continue
        zs = {M[i]["z"] for i in s}
        if len(zs) > 1:
            amb.append(r["Name"])
            continue
        i = sorted(s)[0]
        m = M[i]
        z = fl(m["z"])
        if z is None:
            continue
        d = dict(r)
        d["_z"] = z
        d["_LIRm"] = fl(m["logLIR"])
        d["_LIRo"] = fl(r.get("logLIR"))
        d["_flags"] = {k: int(m[k] == "1") for k in FLAGS}
        d["_mi"] = i
        rows.append(d)
    info = dict(n_table=len(R), n_join=len(rows), unmatched=unmatched, ambiguous=amb)
    _cache[t] = (rows, info)
    return _cache[t]


def factor_arrays(t, col, use_opt_L=False):
    """z, x=log10(1+z), L, y=log10(factor), sigma_dex, flags matrix, names for the joined, finite, positive rows."""
    rows, _ = joined(t)
    z, L, y, sg, fm, nm = [], [], [], [], [], []
    for r in rows:
        v = fl(r[col])
        if use_opt_L == 'fb':
            Lv = r["_LIRm"] if r["_LIRm"] is not None else r["_LIRo"]
        else:
            Lv = r["_LIRo"] if use_opt_L else r["_LIRm"]
        if v is None or v <= 0:
            continue
        if Lv is None:
            Lv = float('nan')
        e = fl(r.get(ERRCOL[col], ""))
        z.append(r["_z"]); L.append(Lv); y.append(math.log10(v))
        sg.append(e / (v * math.log(10)) if e is not None else float("nan"))
        fm.append([r["_flags"][k] for k in FLAGS]); nm.append(r["Name"])
    return dict(z=np.array(z), x=np.log10(1 + np.array(z)), L=np.array(L), y=np.array(y), sg=np.array(sg),
                F=np.array(fm, float), names=nm)


BINS = [("B1", -1, 0.6), ("B2", 0.6, 1.6), ("B3", 1.6, 3.0), ("B4", 3.0, 99)]


def bin_of(z):
    for b, lo, hi in BINS:
        if lo <= z < hi:
            return b


def bin_stats(A):
    out = {}
    for b, lo, hi in BINS:
        m = (A["z"] >= lo) & (A["z"] < hi)
        if m.sum() >= 1:
            s = msd(A["y"][m]) if m.sum() > 1 else dict(N=1, mean=float(A["y"][m][0]), sd=float("nan"), se=float("nan"))
            s["sig_mean"] = float(np.nanmean(A["sg"][m])) if np.isfinite(A["sg"][m]).any() else float("nan")
            out[b] = s
    return out


def drifts(bs):
    res = {}
    if "B1" not in bs:
        return res
    for b in ("B2", "B3", "B4"):
        if b in bs and bs[b]["N"] >= 3:
            dl = bs[b]["mean"] - bs["B1"]["mean"]
            sed = math.sqrt(bs[b]["se"] ** 2 + bs["B1"]["se"] ** 2)
            res[b] = dict(drift=dl, se_drift=sed, K_direct=bs[b]["se"], K_local=math.sqrt(dl ** 2 + sed ** 2))
    return res


def slope_fit(A, withL=True, B=10000, seed=238, extra=None, mask=None):
    m = np.ones(len(A["y"]), bool) if mask is None else mask.copy()
    if withL:
        m &= np.isfinite(A["L"])
    x, y, L = A["x"][m], A["y"][m], A["L"][m]
    ex = None if extra is None else [e[m] for e in extra]
    X = design(x, L if withL else None, ex)
    beta, se, s = ols(X, y)
    bo = ols_boot(X, y, B, seed)
    return dict(N=int(m.sum()), b=float(beta[1]), b_se_ols=float(se[1]), b_boot_sd=float(bo[:, 1].std(ddof=1)),
                b_lo=float(np.percentile(bo[:, 1], 2.5)), b_hi=float(np.percentile(bo[:, 1], 97.5)),
                c=float(beta[2]) if withL else None, c_boot_sd=float(bo[:, 2].std(ddof=1)) if withL else None,
                res_sd=s, beta=beta.tolist())


# ---------------------------------------------------------------- Stripe82, Bourne, NOEMA3D, singles
def load_s82():
    R = readcsv(os.path.join(MT, "stripe82_z_lt0.3_CO_dust.csv"))
    out = []
    for r in R:
        d = {k: fl(r[k]) for k in ("z", "logMstar", "Z_12logOH", "logMdust", "logMgas_dust", "logMgas_CO", "logMdyn", "logMHI",
                                   "logMgas_CO_errlo", "logMgas_dust_errlo", "logMdyn_errlo")}
        d["id"] = r["id"]
        out.append(d)
    return out


def s82_d(mut=None):
    S = load_s82()
    d = np.array([r["logMgas_CO"] - r["logMgas_dust"] for r in S if r["logMgas_CO"] is not None and r["logMgas_dust"] is not None])
    return d, S


def load_bourne():
    R = readcsv(os.path.join(MT, "bourne2019_z1_CI_CO_dust.csv"))
    out = []
    for r in R:
        a, b = fl(r["Mmol_CI_1e9"]), fl(r["Mmol_cont_1e9"])
        if a and b:
            out.append(dict(id=r["id"], z=fl(r["z"]), logCI=math.log10(a * 1e9), logDust=math.log10(b * 1e9)))
    return out


def load_noema():
    R = readcsv(os.path.join(MT, "noema3d_three_tracer_reconstruction.csv"))
    out = []
    for r in R:
        out.append(dict(id=r["id"], z=fl(r["z"]), group=r["group"], ok=int(r["CO_control_pass"]),
                        CO_t1=fl(r["logMmol_CO_table1"]), CO_rec=fl(r["logMmol_CO_reconstructed"]),
                        CI=fl(r["logMmol_CI_reconstructed"]), dust=fl(r["logMmol_dust_reconstructed"])))
    return out


def noema_pairs(rows, co="CO_t1"):
    P = []
    for r in rows:
        P.append(dict(id=r["id"], CO_dust=r[co] - r["dust"], CO_CI=(r[co] - r["CI"]) if r["CI"] is not None else None,
                      CI_dust=(r["CI"] - r["dust"]) if r["CI"] is not None else None))
    return P


def hat(dAB, dAC, dBC):
    """three-cornered hat from pair differences d_AB=A-B, d_AC=A-C, d_BC=B-C; returns variances of A, B, C."""
    vAB, vAC, vBC = (np.var(np.asarray(v), ddof=1) for v in (dAB, dAC, dBC))
    return (vAB + vAC - vBC) / 2, (vAB + vBC - vAC) / 2, (vAC + vBC - vAB) / 2


def sgn_sqrt(v):
    return math.copysign(math.sqrt(abs(v)), v)


# ---------------------------------------------------------------- ACE
def load_ace():
    R = readcsv(os.path.join(MT, "ace_merged_per_galaxy.csv"))
    out = []
    for r in R:
        co_ok = fl(r["Mmol_CO_1e10"]) is not None and r["Mmol_CO_flag"].strip() != "<"
        du_ok = fl(r["logMdust_2609_20926"]) is not None and r["logMdust_flag"].strip() != "<"
        out.append(dict(id=r["id"], z=fl(r["z"]), OH=fl(r["OH"]), Mstar=fl(r["Mstar_1e10"]), Mmol=fl(r["Mmol_CO_1e10"]),
                        Mmol_flag=r["Mmol_CO_flag"], logMmol_b=fl(r["logMmol_2609_20926"]), logMdust=fl(r["logMdust_2609_20926"]),
                        dust_flag=r["logMdust_flag"], Mdust21040=fl(r["Mdust_1e7_2609_21040"]), d21040_flag=r["Mdust_flag_2609_21040"],
                        logLpCO32=fl(r["logLpCO32"]), logLnu873=fl(r["logLnu873"]), both=co_ok and du_ok))
    return out


# ---------------------------------------------------------------- toy optimiser (D12)
def toy_optimise(logLa, logLb, log_pa, log_pb, w):
    """Two tracers with prior-mean conversions: mass_a = logLa + log_pa, mass_b = logLb + log_pb.
    r = mass_a - mass_b at prior means. Posterior shifts: factor a -= (1-w) r? Convention: w = share taken by tracer a.
    a-factor shift = -w r ; b-factor shift = +(1-w) r  => masses agree exactly."""
    ma = logLa + log_pa
    mb = logLb + log_pb
    r = ma - mb
    da = -w * r
    db = (1 - w) * r
    return ma + da, mb + db, da, db, r


def banner(T, name):
    T(f"# {name}")
    T(f"repo=<repo> scratch=<scratch> ext=<ext> mutate={os.environ.get('MUTATE', '0')}")
