"""CFG234 common: repo locator, loaders (CRISTAL, NOEMA3D, vector), kernels, bootstrap, classifier, tee.
Referee re-derivation of CFG213 from CFG234_FROZEN_CRITERIA.md (sha256 97600594...). Repo is read-only.
CFG213 scripts/outputs are NOT read by any CFG234 script."""
import os, sys, math, json
import numpy as np
import pandas as pd
from scipy import optimize

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
        if os.path.isfile(os.path.join(c, "data_assembly", "arxiv_tables", "cristal2025_dynamics.csv")):
            return c
    raise SystemExit("repo not found; set ZF_REPO")


REPO = find_repo()
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
VEC = os.path.join(AT, "cristal_vector")
NOEMA = os.path.join(REPO, "data_assembly", "noema3d", "noema3d_per_galaxy.csv")

G = 6.6743e-11
KPC = 3.0856775814913673e19
MSUN = 1.98847e30
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}
OM = 0.315
K0 = 3.36


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
    t = Tee(os.path.join(HERE, name + ".out"))
    sys.stdout = t
    print("<repo> =", "<repo>", "| <scratch> =", "<scratch>")
    return t


def savejson(name, obj):
    def conv(o):
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, np.bool_): return bool(o)
        raise TypeError(type(o))
    with open(os.path.join(HERE, name + "_results.json"), "w") as f:
        json.dump(obj, f, indent=1, default=conv)


# ---------------------------------------------------------------- kernels (re-implemented from the CFG5 docstring)
def E_of_z(z):
    z = np.asarray(z, float)
    return np.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def _h_rar(y):
    y = np.asarray(y, float)
    return y / np.expm1(np.sqrt(y))


def _dh(t):
    s = math.sqrt(t); e = math.expm1(s)
    return (2 * e - s * (1 + e)) / (2 * e ** 2)


_YP = optimize.brentq(_dh, 1.0, 5.0, xtol=1e-15, rtol=1e-15, maxiter=500)
_HP = float(_h_rar(_YP))
_DELTA = 0.05
_YS = optimize.brentq(lambda t: _dh(t) - _DELTA * _HP / (t + _YP), 1.0, _YP, xtol=1e-15, rtol=1e-15, maxiter=500)


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    yr = np.minimum(y, _YS)
    h = np.where(y <= _YS, _h_rar(yr), float(_h_rar(_YS)) + _DELTA * _HP * np.log((y + _YP) / (_YS + _YP)))
    return 1.0 + h / y


def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


KERN = {"mono": nu_mono, "p2": nu_p2}


def invert_nu(D, kern):
    """solve nu(y) = D for y (vectorised bisection in log10 y; nu decreasing)."""
    D = np.atleast_1d(np.asarray(D, float))
    lo = np.full(D.shape, -12.0); hi = np.full(D.shape, 12.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        v = kern(10 ** mid)
        up = v > D  # nu too big -> y too small -> raise lo
        lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
    return 10 ** (0.5 * (lo + hi))


def c4_crosscheck():
    """C4: my nu_mono / P2 against the imported objects. CFG5_common.nu_mono is the record's standing kernel (its docstring is what I re-derived);
    CFG4_common.nu_mono is an older copy; both are compared and both differences printed."""
    out = dict(ok=True, y_star=_YS, y_peak=_YP)
    y = np.logspace(-6, 4, 2001)
    sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
    try:
        import CFG5_common as C5  # noqa
        out["max_rel_diff_nu_mono_vs_CFG5"] = float(np.max(np.abs(C5.nu_mono(y) / nu_mono(y) - 1)))
        out["max_rel_diff_p2_vs_CFG5"] = float(np.max(np.abs(C5.nu_p2(y) / nu_p2(y) - 1)))
    except Exception as e:
        out["ok"] = False; out["error_CFG5"] = repr(e)[:200]
    try:
        import CFG4_common as C4  # noqa
        r = np.abs(C4.nu_mono(y) / nu_mono(y) - 1)
        out["max_rel_diff_nu_mono_vs_CFG4"] = float(np.max(r))
        out["max_rel_diff_nu_mono_vs_CFG4_y_ge_1e-2"] = float(np.max(r[y >= 1e-2]))
        out["max_rel_diff_p2_vs_CFG4"] = float(np.max(np.abs(C4.nu_p2(y) / nu_p2(y) - 1)))
        a0 = (float(C4.A0["canonical"]), float(C4.A0["alt"]))
        out["a0_CFG4"] = a0
        out["a0_match"] = bool(abs(a0[0] - A0["canonical"]) < 1e-15 and abs(a0[1] - A0["alt"]) < 1e-15)
    except Exception as e:
        out["error_CFG4"] = repr(e)[:200]
    return out


# ---------------------------------------------------------------- statistics
def boot_ci(x, seed=234, B=10000):
    x = np.asarray(x, float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    m = np.median(x[idx], axis=1)
    lo, hi = np.percentile(m, [2.5, 97.5])
    return float(np.median(x)), float(lo), float(hi)


def classify(lo, hi):
    if lo > 0: return "over"
    if hi < 0: return "under"
    return "CONS"


def stat(x, seed=234, B=10000):
    m, lo, hi = boot_ci(x, seed, B)
    return dict(med=m, lo=lo, hi=hi, cls=classify(lo, hi), n=len(x))


def fmt(s):
    lab = {"over": "DISFAVOURED-over", "under": "DISFAVOURED-under", "CONS": "CONSISTENT"}[s["cls"]]
    return f"{s['med']:+.3f} [{s['lo']:+.3f}, {s['hi']:+.3f}] {lab} (n={s['n']})"


# ---------------------------------------------------------------- CRISTAL loaders
ID12 = ["02", "03", "06b", "07a", "08", "10a-E", "11", "12", "19", "20", "23b", "23c"]
EXCL = ["09", "15"]
ID14 = ["02", "03", "06b", "07a", "08", "09", "10a-E", "11", "12", "15", "19", "20", "23b", "23c"]
SAMPLE_ALIAS = {"09": "09a"}
KIN_ALIAS = {"09": "09a"}
VEC_ALIAS = {"10a-E": "10a"}   # the vector figure calls the dynamics table's 10a-E disc '10a' (validation.csv R_e and sigma_0 match 10a-E)


def load_cristal():
    dyn = pd.read_csv(os.path.join(AT, "cristal2025_dynamics.csv")).set_index("id")
    smp = pd.read_csv(os.path.join(AT, "cristal2025_sample.csv")).set_index("id")
    kin = pd.read_csv(os.path.join(AT, "cristal2025_kinematics.csv")).set_index("id")
    rows = []
    for i in ID14:
        d = dyn.loc[i]; s = smp.loc[SAMPLE_ALIAS.get(i, i)]; k = kin.loc[KIN_ALIAS.get(i, i)]
        rows.append(dict(id=i, z=float(s.z_cii), logMstar=float(s.logMstar), f_molgas=float(k.f_molgas),
                         cls=str(k.classification),
                         logMtot=float(d.logMtot), Re=float(d.Re_disk_kpc), Vrot=float(d.Vrot_Re_kms),
                         sig=float(d.sigma0_kms), fDM=float(d.fDM_Re),
                         e=dict(logMtot=(float(d.logMtot_errhi), float(d.logMtot_errlo)),
                                Re=(float(d.Re_disk_kpc_errhi), float(d.Re_disk_kpc_errlo)),
                                Vrot=(float(d.Vrot_Re_kms_errhi), float(d.Vrot_Re_kms_errlo)),
                                sig=(float(d.sigma0_kms_errhi), float(d.sigma0_kms_errlo)),
                                fDM=(float(d.fDM_Re_errhi), float(d.fDM_Re_errlo)))))
    df = pd.DataFrame(rows).set_index("id", drop=False)
    return df


def gacc(V_kms, R_kpc):
    return (np.asarray(V_kms, float) * 1e3) ** 2 / (np.asarray(R_kpc, float) * KPC)


def base_quantities(df, k=K0):
    """per-galaxy D_obs, V_circ, g_obs, g_bar at the k=3.36 baseline."""
    f = df.fDM.values
    D0 = 1.0 / (1.0 - f)
    Vc2 = df.Vrot.values ** 2 + K0 * df.sig.values ** 2
    gobs0 = gacc(np.sqrt(Vc2), df.Re.values)
    gbar = gobs0 / D0
    return dict(D0=D0, Vc0=np.sqrt(Vc2), gobs0=gobs0, gbar=gbar)


def cell(df, k=K0, mode="Hg", kernel="mono", foot="canonical", rival=False, Dmul=1.0, Zlaw=None, gbar_mul=None, route=None):
    """delta for every galaxy in df. mode: Hg (g_bar held at k=3.36 value) | Hf (D held). Zlaw: array of z used for E(z).
    gbar_mul: per-galaxy multiplier of g_bar (route). route: None|'hold'|'recompute' (only with gbar_mul)."""
    q = base_quantities(df)
    Vck2 = df.Vrot.values ** 2 + k * df.sig.values ** 2
    gobsk = gacc(np.sqrt(Vck2), df.Re.values)
    if mode == "Hg":
        gbar = q["gbar"].copy(); D = gobsk / gbar
    else:
        D = q["D0"].copy(); gbar = gobsk / D
    if gbar_mul is not None:
        gbar_ind = gbar * gbar_mul
        if route == "recompute":
            D = gobsk / gbar_ind
        gbar = gbar_ind
    D = D * Dmul
    z = df.z.values if Zlaw is None else Zlaw
    a0 = A0[foot] * (E_of_z(z) if rival else 1.0)
    y = gbar / a0
    dl = np.log10(D) - np.log10(KERN[kernel](y))
    return dl, D, y


def route_factor(df):
    Mind = 10 ** df.logMstar.values / (1.0 - df.f_molgas.values)
    return Mind / 10 ** df.logMtot.values


ROUTE9 = [i for i in ID12 if i not in ("06b", "10a-E", "23c")]
BEST6 = ["03", "08", "11", "19", "20", "23c"]
DETECTED6 = ["02", "03", "07a", "11", "19", "20"]   # dust-detected gas (data chat list, commit 2ad335eea; post-freeze item)


# ---------------------------------------------------------------- vector
def load_vector():
    cur = pd.read_csv(os.path.join(VEC, "cristal_curves.csv"))
    pts = pd.read_csv(os.path.join(VEC, "cristal_points.csv"))
    val = pd.read_csv(os.path.join(VEC, "cristal_validation.csv"))
    out = pd.read_csv(os.path.join(VEC, "cristal_outer_summary.csv"))
    return cur, pts, val, out


def vec_curve(cur, vid, curve):
    s = cur[(cur.id == vid) & (cur.curve == curve)].sort_values("R_kpc")
    R = s.R_kpc.values; V = s.value.values
    # collapse duplicate R
    Ru, ix = np.unique(R, return_index=True)
    return Ru, V[ix]


def vec_at(cur, vid, curve, R, log=False):
    Rc, V = vec_curve(cur, vid, curve)
    if log:
        m = Rc > 0
        return float(np.interp(np.log(R), np.log(Rc[m]), V[m]))
    return float(np.interp(R, Rc, V))


# ---------------------------------------------------------------- NOEMA3D
def load_noema():
    d = pd.read_csv(NOEMA)
    return d


def noema_frame(d):
    """return a frame with the CRISTAL column names so cell() can be reused: Vrot := sqrt(Vc^2 - 3.36 sig^2) so k=3.36 gives V_c."""
    Vc = d.Vc_at_Re_disk_kms.values.astype(float)
    sig = d.sigma0_kms.values.astype(float)
    Vrot2 = Vc ** 2 - K0 * sig ** 2
    df = pd.DataFrame(dict(id=d.id.values, z=d.z.values, Re=d.Re_disk_fixed_kpc.values, Vrot=np.sqrt(np.abs(Vrot2)) * np.sign(Vrot2),
                           sig=sig, fDM=d.fDM_Re_disk.values, logMstar=d.logMstar_SED.values,
                           logMgas=d.logMgas_CO_P1.values, logMbary=d.logMbary_dyn.values))
    return df.set_index("id", drop=False), Vrot2


def cell_noema(df, Vrot2, k=K0, mode="Hg", kernel="mono", foot="canonical", rival=False, gbar_mul=None, route=None):
    D0 = 1.0 / (1.0 - df.fDM.values)
    Vc2_0 = Vrot2 + K0 * df.sig.values ** 2   # = Vc^2
    gobs0 = gacc(np.sqrt(Vc2_0), df.Re.values)
    gbar0 = gobs0 / D0
    Vck2 = Vc2_0 - (K0 - k) * df.sig.values ** 2
    gobsk = gacc(np.sqrt(np.maximum(Vck2, 1e-9)), df.Re.values)
    if mode == "Hg":
        gbar = gbar0.copy(); D = gobsk / gbar
    else:
        D = D0.copy(); gbar = gobsk / D
    if gbar_mul is not None:
        gi = gbar * gbar_mul
        if route == "recompute": D = gobsk / gi
        gbar = gi
    a0 = A0[foot] * (E_of_z(df.z.values) if rival else 1.0)
    y = gbar / a0
    return np.log10(D) - np.log10(KERN[kernel](y)), D, y


def noema_route_factor(df):
    Mind = 10 ** df.logMstar.values + 10 ** df.logMgas.values
    return Mind / 10 ** df.logMbary.values


# ---------------------------------------------------------------- mocks (attack e, control M7)
def mad_sigma(x):
    x = np.asarray(x, float)
    return float(1.4826 * np.median(np.abs(x - np.median(x))))


def boot_med_batch(dl, B, rng):
    """dl: (N, n). returns (median, sd of B bootstrap medians, lo, hi) per mock."""
    N, n = dl.shape
    med = np.median(dl, axis=1)
    lo = np.empty(N); hi = np.empty(N); sd = np.empty(N)
    ch = max(1, int(4e6 // (B * n)))
    for a in range(0, N, ch):
        b = min(N, a + ch)
        idx = rng.integers(0, n, size=(b - a, B, n))
        m = np.median(np.take_along_axis(dl[a:b, None, :].repeat(B, 1), idx, axis=2), axis=2)
        sd[a:b] = m.std(axis=1, ddof=0)
        lo[a:b] = np.percentile(m, 2.5, axis=1); hi[a:b] = np.percentile(m, 97.5, axis=1)
    return med, sd, lo, hi


def mock_deltas(rng, y_flat_obs, y_riv_obs, truth, n, N, s, b=0.0):
    """resample n galaxies with replacement from the sample's observed (y_flat, y_rival); D from the truth law at y_obs*10^-b, times 10^eps."""
    m = len(y_flat_obs)
    idx = rng.integers(0, m, size=(N, n))
    yf = y_flat_obs[idx]; yr = y_riv_obs[idx]
    eps = rng.normal(0.0, s, size=(N, n))
    yt = (yf if truth == "flat" else yr) * 10 ** (-b)
    D = nu_mono(yt) * 10 ** eps
    dlf = np.log10(D) - np.log10(nu_mono(yf))
    dlr = np.log10(D) - np.log10(nu_mono(yr))
    return dlf, dlr


def recovery_control(y_flat_obs, y_riv_obs, s, seed=234, N=2000, B=300, n=12):
    rng = np.random.default_rng(seed)
    res = {}
    for truth in ("flat", "rival"):
        dlf, dlr = mock_deltas(rng, y_flat_obs, y_riv_obs, truth, n, N, s)
        out = {}
        for nm, dl in (("flat_law", dlf), ("rival_law", dlr)):
            med, sd, lo, hi = boot_med_batch(dl, B, rng)
            out[nm] = dict(over=float(np.mean(lo > 0)), under=float(np.mean(hi < 0)), cons=float(np.mean((lo <= 0) & (hi >= 0))))
        res[truth] = out
    ok = (res["flat"]["rival_law"]["under"] >= 0.90 and res["flat"]["flat_law"]["over"] <= 0.10 and
          res["rival"]["flat_law"]["over"] >= 0.90 and res["rival"]["rival_law"]["under"] <= 0.10)
    return res, bool(ok)
