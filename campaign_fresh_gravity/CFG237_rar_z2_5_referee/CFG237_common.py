"""CFG237 common: repo locator, tee, constants, cosmology, kernels (shared lineage with CFG233/234/236), laws, Freeman disc,
loaders (Amvrosiadis, ALPAKA, CRISTAL, RC100), bootstrap. Referee re-derivation of CFG227 from CFG237_FROZEN_CRITERIA.md (sha256 6ad68510...).
Repo is read-only. No CFG227 file is read by any CFG237 script except CFG237_compare.py (post-run)."""
import os, sys, math, json, re
import numpy as np
import pandas as pd
from scipy import special, optimize, integrate

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = os.environ.get("MUTATE", "").strip()          # '' | '1'..'8'
SUF = ("_M" + MODE) if MODE else ""


def find_repo():
    cands = []
    if os.environ.get("ZF_REPO"):
        cands.append(os.environ["ZF_REPO"])
    for start in (HERE, os.getcwd()):
        p = start
        for _ in range(12):
            cands.append(p); p = os.path.dirname(p)
    cands.append(os.path.expanduser("~/new_physics/zimmerman-formula"))
    for c in cands:
        if os.path.isfile(os.path.join(c, "data_assembly", "arxiv_tables", "amvrosiadis_bestfit.csv")):
            return c
    raise SystemExit("repo not found; set ZF_REPO")


REPO = find_repo()
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
VEC = os.path.join(AT, "cristal_vector")
DA = os.path.join(REPO, "data_assembly")

G = 6.6743e-11
KPC = 3.0856775814913673e19
MSUN = 1.98847e30
C_KMS = 299792.458
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}
OM = 0.315
H0 = 67.4
K0 = 3.36
RD_FAC = 1.67835          # R_e = 1.67835 R_d for an exponential disc
SEED, SEED2, SEED3 = 237, 238, 239


class Tee:
    def __init__(self, path):
        self.f = open(path, "w"); self.so = sys.__stdout__
        self.subs = [(REPO, "<repo>"), (HERE, "<scratch>"), (os.path.expanduser("~"), "~")]

    def _clean(self, s):
        for a, b in self.subs:
            s = s.replace(a, b)
        return s

    def write(self, s):
        s = self._clean(s); self.f.write(s); self.so.write(s)

    def flush(self):
        self.f.flush(); self.so.flush()


def start(name):
    t = Tee(os.path.join(HERE, name + SUF + ".out"))
    sys.stdout = t
    print("<repo> = <repo> | <scratch> = <scratch> | MUTATE =", MODE or "none")
    return t


def savejson(name, obj):
    def conv(o):
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, np.bool_): return bool(o)
        return str(o)
    with open(os.path.join(HERE, name + SUF + "_results.json"), "w") as f:
        json.dump(obj, f, indent=1, default=conv)


class Checks:
    """pass lines recorded; mutate runs exit 1 when a designated line fails."""
    def __init__(self):
        self.rows = []

    def add(self, name, ok, detail="", expected_fail=False):
        self.rows.append((name, bool(ok), detail, expected_fail))
        tag = "PASS  " if ok else ("FAIL* " if expected_fail else "FAIL  ")
        print(tag + name + ((" :: " + detail) if detail else ""))

    def n_fail(self, prefix=None):
        return sum(1 for r in self.rows if not r[1] and not r[3] and (prefix is None or r[0].startswith(prefix)))


# ------------------------------------------------------------------ cosmology, kernels, laws
def E_of_z(z):
    z = np.asarray(z, float)
    return np.sqrt(OM * (1 + z) ** 3 + 1 - OM)


_zg = np.linspace(0, 8, 8001)
_chi = integrate.cumulative_trapezoid(1.0 / E_of_z(_zg), _zg, initial=0.0) * C_KMS / H0    # comoving distance, Mpc


def kpc_per_arcsec(z):
    Dc = np.interp(z, _zg, _chi)
    return Dc / (1 + np.asarray(z, float)) * 1e3 * math.pi / (180 * 3600)


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


def _dm14_c(z):
    z = np.asarray(z, float)
    a = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * z ** 1.21)
    return 10 ** a            # M = 1e12 h^-1 Msun so the mass term vanishes


def _cf(c):
    return c ** 2 / (np.log1p(c) - c / (1 + c))


def F_proxy(z):
    z = np.asarray(z, float)
    El = np.sqrt(0.3027 * (1 + z) ** 3 + 0.6973)
    return El ** (4.0 / 3.0) * _cf(_dm14_c(z)) / _cf(_dm14_c(0.0))


def F_mdec(z, w0=-0.838, wa=-0.62):
    z = np.asarray(z, float)
    return (1 + z) ** (1.5 * (1 + w0 + wa)) * np.exp(-1.5 * wa * z / (1 + z))


LAWS = {"FLAT": lambda z: np.ones_like(np.asarray(z, float)), "PROXY": F_proxy, "Hz": E_of_z, "MDEC": F_mdec}
LAWNAMES = ["FLAT", "PROXY", "Hz", "MDEC"]


def delta(gobs, gbar, z, law="FLAT", foot="canonical", kern="mono", D=None):
    """delta = log10[g_obs / (g_bar nu(g_bar/(a0 F)))]; if D given it replaces g_obs/g_bar."""
    gobs = np.asarray(gobs, float); gbar = np.asarray(gbar, float)
    a0 = A0[foot] * LAWS[law](z)
    Dobs = gobs / gbar if D is None else np.asarray(D, float)
    return np.log10(Dobs) - np.log10(KERN[kern](gbar / a0))


# ------------------------------------------------------------------ Freeman disc
def disc_v2(r_kpc, M_msun, Rd_kpc):
    """Freeman exponential thin disc, in-plane: V^2 = (2GM/Rd) y^2 [I0K0 - I1K1], y = r/(2 Rd); returns m^2/s^2."""
    r = np.asarray(r_kpc, float); Rd = np.asarray(Rd_kpc, float)
    y = r / (2 * Rd)
    f = y ** 2 * (special.i0(y) * special.k0(y) - special.i1(y) * special.k1(y))
    return 2 * G * np.asarray(M_msun, float) * MSUN / (Rd * KPC) * f


def disc_g(r_kpc, M_msun, Rd_kpc):
    return disc_v2(r_kpc, M_msun, Rd_kpc) / (np.asarray(r_kpc, float) * KPC)


def gacc(V_kms, R_kpc):
    return (np.asarray(V_kms, float) * 1e3) ** 2 / (np.asarray(R_kpc, float) * KPC)


# ------------------------------------------------------------------ statistics
def boot(x, seed=SEED, B=10000):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    m = np.median(x[idx], axis=1)
    lo, hi = np.percentile(m, [2.5, 97.5])
    return dict(med=float(np.median(x)), lo=float(lo), hi=float(hi), n=int(len(x)))


def fs(s):
    return f"{s['med']:+.3f} [{s['lo']:+.3f}, {s['hi']:+.3f}] n={s['n']}"


def edge_adjacent(x, e1, e2):
    """DISCRETENESS helper: both edges are order statistics of the n values and adjacent?"""
    x = np.sort(np.asarray(x, float))
    i1 = int(np.argmin(np.abs(x - e1))); i2 = int(np.argmin(np.abs(x - e2)))
    return abs(i1 - i2) <= 1 and abs(x[i1] - e1) < 0.006 + 1e-9 and abs(x[i2] - e2) < 0.006 + 1e-9


# ------------------------------------------------------------------ loaders
def load_s1(zmin=2.0, zmax=5.0):
    b = pd.read_csv(os.path.join(AT, "amvrosiadis_bestfit.csv"), dtype={"alessid": str})
    p = pd.read_csv(os.path.join(AT, "amvrosiadis_parent.csv"), dtype={"alessid": str})
    d = b.merge(p, on="alessid")
    d = d[(d.z >= zmin) & (d.z <= zmax)].reset_index(drop=True)
    d["kpas"] = kpc_per_arcsec(d.z.values)
    d["re_kpc"] = d.re_arcsec * d.kpas
    d["V"] = d.vcirc_2re_kms
    d["V_err"] = 0.5 * (d.vcirc_2re_kms_errhi + d.vcirc_2re_kms_errlo)
    d["slog_gobs"] = 2 * 0.4343 * d.V_err / d.V
    d["Mstar"] = 10 ** d.logMstar
    d["Mgas"] = 10 ** d.logMgas_msun
    d["footnote_other_paper"] = d.alessid.isin(["049.1", "075.1", "122.1"])
    return d


S1_IDS = ["007.1", "022.1", "041.1", "049.1", "065.1", "066.1", "071.1", "075.1", "122.1"]


def s1_points(d, alpha=0.92, bM=0.0, di=0.0, s=1.0, mstar_mult=1, k=0.0, tau=0.0, bias_gas=0.0, bias_star=0.0, gobs_mul=1.0, hold_V=True):
    """S1 baryon and velocity model. alpha: alpha_CO (gas x alpha/0.92); bM: M* zero point (dex); di: inclination shift (deg);
    s: R_e scale (both components and evaluation radius; V held); mstar_mult: R_e,* = mstar_mult x R_e; k: V_c^2 = V^2 + k sigma^2;
    tau: gas shift (dex) on top; bias_gas/bias_star: extra dex (mutations)."""
    re = d.re_kpc.values * s
    r = 2 * re
    inc = d.inc_deg.values
    if di != 0.0:
        inew = np.clip(inc + di, 15.0, np.maximum(85.0, inc))
        Vf = np.sin(np.radians(inc)) / np.sin(np.radians(inew))
    else:
        Vf = np.ones(len(d))
    V2 = (d.V.values * Vf) ** 2 + k * d.sigma_kms.values ** 2
    gobs = V2 * 1e6 / (r * KPC) * gobs_mul
    Mst = d.Mstar.values * 10 ** (bM + bias_star)
    Mg = d.Mgas.values * (alpha / 0.92) * 10 ** (tau + bias_gas)
    g_st = disc_g(r, Mst, re * mstar_mult / RD_FAC)
    g_gas = disc_g(r, Mg, re / RD_FAC)
    gbar = g_st + g_gas
    return dict(gobs=gobs, gbar=gbar, g_st=g_st, g_gas=g_gas, r=r, z=d.z.values, D=gobs / gbar, Mst=Mst, Mg=Mg, re=re)


# ---- ALPAKA
ALPAKA_IDS = [13, 15, 18, 19, 20, 22, 23, 24, 25, 28]


def load_alpaka():
    o = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv"))
    pr = pd.read_csv(os.path.join(AT, "alpaka1_properties.csv"))
    kin = pd.read_csv(os.path.join(AT, "alpaka1_kinematics.csv"))
    smp = pd.read_csv(os.path.join(AT, "alpaka1_sample.csv"))
    pr = pr.iloc[:, :15]
    d = o.merge(pr[["id", "mstar_1e10msun", "e_mstar"]], on="id", how="left")
    kk = kin[["id", "vext_kms", "vext_errhi", "vext_errlo", "sigma_ext_kms"]].iloc[:, :5]
    d = d.merge(kk, on="id", how="left").merge(smp[["id", "name", "ra_deg", "dec_deg"]], on="id", how="left")
    return d[d.id.isin(ALPAKA_IDS)].reset_index(drop=True)


def alpaka_points(d, alpha_p=0.0, rext_over_re=1.2):
    """stars-only exponential disc at R_ext; R_e = dashed line if drawn else R_ext/1.2. g_bar is a LOWER limit."""
    R = d.R_ext_kpc.values
    Re = np.where(np.isfinite(d.Re_kpc_dashed_line.values), d.Re_kpc_dashed_line.values, R / rext_over_re)
    M = d.mstar_1e10msun.values * 1e10
    V2 = d.Vext_kms_table.values ** 2 + alpha_p * np.nan_to_num(d.sigma_ext_kms.values) ** 2
    gobs = V2 * 1e6 / (R * KPC)
    gbar = np.where(np.isfinite(M), disc_g(R, np.where(np.isfinite(M), M, 1.0), Re / RD_FAC), np.nan)
    return dict(gobs=gobs, gbar=gbar, z=d.z.values, R=R, Re=Re, ids=d.id.values)


# ---- CRISTAL (R_e fit/independent rows; R_out from the vector summary)
ID14 = ["02", "03", "06b", "07a", "08", "09", "10a-E", "11", "12", "15", "19", "20", "23b", "23c"]
ID12 = ["02", "03", "06b", "07a", "08", "10a-E", "11", "12", "19", "20", "23b", "23c"]
DETECTED6 = ["02", "03", "07a", "11", "19", "20"]
SAMPLE_ALIAS = {"09": "09a"}


def load_cristal():
    dyn = pd.read_csv(os.path.join(AT, "cristal2025_dynamics.csv")).set_index("id")
    smp = pd.read_csv(os.path.join(AT, "cristal2025_sample.csv")).set_index("id")
    kin = pd.read_csv(os.path.join(AT, "cristal2025_kinematics.csv")).set_index("id")
    rows = []
    for i in ID14:
        dd = dyn.loc[i]; ss = smp.loc[SAMPLE_ALIAS.get(i, i)]; kk = kin.loc[SAMPLE_ALIAS.get(i, i)]
        rows.append(dict(id=i, z=float(ss.z_cii), logMstar=float(ss.logMstar), f_molgas=float(kk.f_molgas),
                         logMtot=float(dd.logMtot), Re=float(dd.Re_disk_kpc), Vrot=float(dd.Vrot_Re_kms),
                         sig=float(dd.sigma0_kms), fDM=float(dd.fDM_Re)))
    return pd.DataFrame(rows).set_index("id", drop=False)


def cristal_Re_rows(df, tau=0.0, k=K0):
    """R_e rows: g_obs = V_circ^2/R_e; D_obs = 1/(1-fDM); g_bar,fit = g_obs/D_obs; independent route g_bar,ind = rho g_bar,fit with
    rho = M_ind/M_fit, M_ind = M* + M_gas 10^tau, M_gas = M* f/(1-f) (tau=0 -> M*/(1-f)); D_ind = g_obs/g_bar,ind."""
    Vc2 = df.Vrot.values ** 2 + k * df.sig.values ** 2
    gobs = gacc(np.sqrt(Vc2), df.Re.values)
    D0 = 1.0 / (1.0 - df.fDM.values)
    gfit = gobs / D0
    Mst = 10 ** df.logMstar.values
    Mg = Mst * df.f_molgas.values / (1 - df.f_molgas.values)
    Mind = Mst + Mg * 10 ** tau
    rho = Mind / 10 ** df.logMtot.values
    gind = gfit * rho
    return dict(gobs=gobs, gfit=gfit, gind=gind, Dfit=D0, Dind=gobs / gind, rho=rho, z=df.z.values, ids=df.id.values)


def load_vec_outer():
    return pd.read_csv(os.path.join(VEC, "cristal_outer_summary.csv"), dtype={"id": str})


def cristal_Rout_rows(df, vec, radius="table_Rout", tau=0.0):
    sub = vec[vec.radius_definition == radius].set_index("id")
    ids = [i for i in df.id if i in sub.index]
    R = np.array([sub.loc[i, "R_kpc"] for i in ids]); Vb = np.array([sub.loc[i, "Vbary_kms"] for i in ids]); Vt = np.array([sub.loc[i, "Vtot_kms"] for i in ids])
    gobs = gacc(Vt, R); gfit = gacc(Vb, R)
    d = df.loc[ids]
    Mst = 10 ** d.logMstar.values
    Mg = Mst * d.f_molgas.values / (1 - d.f_molgas.values)
    rho = (Mst + Mg * 10 ** tau) / 10 ** d.logMtot.values
    gind = gfit * rho
    return dict(gobs=gobs, gfit=gfit, gind=gind, Dfit=gobs / gfit, Dind=gobs / gind, rho=rho, z=d.z.values, ids=np.array(ids), R=R)


# ---- RC100
def load_rc100(which="corrected"):
    if which == "corrected":
        p = os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")
    else:
        p = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv")
    return pd.read_csv(p)


def rc100_rows(d, zmin=2.0):
    d = d[d.z >= zmin]
    gobs = gacc(d.Vc_Re_kms.values, d.Re_kpc.values)
    gbar = (1 - d.fDM_within_Re.values) * gobs
    return dict(gobs=gobs, gbar=gbar, z=d.z.values, ids=d.idx.values)
