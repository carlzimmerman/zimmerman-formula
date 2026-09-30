"""CFG235_common.py -- shared machinery for the CFG235 break search (criteria frozen in CFG235_FROZEN_CRITERIA.md).
No output of its own.  Repo root: env ZF_REPO, else walk up from __file__ looking for data_assembly/.  Nothing is written
into the repo (bytecode writing is disabled before any repo import).  kappa = 1/2 is FITTED; nothing here says the data
favour any theory."""
import os, sys, math, csv, hashlib, json, warnings
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import i0, i1, k0, k1
from scipy.stats import norm
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.interpolate import interp1d

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    e = os.environ.get("ZF_REPO")
    if e and os.path.isdir(os.path.join(e, "data_assembly")):
        return os.path.abspath(e)
    p = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(p, "data_assembly")) and os.path.isdir(os.path.join(p, "campaign_fresh_gravity")):
            return p
        p = os.path.dirname(p)
    raise SystemExit("repo root not found: set ZF_REPO")


REPO = find_repo()
TAB = os.path.join(REPO, "data_assembly", "arxiv_tables")
MUT = int(os.environ.get("MUTATE", "0") or 0)


def clean(s):
    return str(s).replace(REPO, "<repo>").replace(HERE, "<scratch>")


# ------------------------------------------------------------------------------------------------ constants
G_KPC = 4.30091e-6                     # kpc (km/s)^2 / Msun
KPC_M = 3.0856775814913673e19
A0_FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0K = {k: v * KPC_M / 1e6 for k, v in A0_FOOT.items()}          # (km/s)^2 / kpc
K_PRESS = 3.36
KTOT_D = 1.8
LN10 = math.log(10.0)
Z_THRESH = 3.0
M_TRIALS = 62 if MUT != 8 else 31
ALPHA_FW = 0.05
Z_B = float(norm.isf(ALPHA_FW / M_TRIALS))
N_MC = int(os.environ.get("CFG235_NMC", "200000"))
SEED = 235
SIGSET = {"narrow": (0.20, 0.10), "primary": (0.25, 0.15), "wide": (0.30, 0.25)}     # (M*/baryon sys, dyn sys) dex
if MUT == 2:
    SIGSET = {k: (0.0, 0.0) for k in SIGSET}
GEOMS = ["GS", "GD", "GC"]
KERN = ["P2", "mono"]
FOOT = ["canonical", "alt"]


# ------------------------------------------------------------------------------------------------ kernels
def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def _h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        s = np.sqrt(np.minimum(y, 1e4))
        return np.where(y < 1e4, y / np.expm1(s), 0.0)


def _dh(t):
    s = math.sqrt(t)
    e = math.expm1(s)
    return (2 * e - s * (1 + e)) / (2 * e * e)


_YP = brentq(_dh, 1.0, 5.0)
_HP = float(_h_rar(_YP))
_DELTA = 0.05
_YS = brentq(lambda t: _dh(t) - _DELTA * _HP / (t + _YP), 1.0, _YP)


def nu_mono(y):
    """nu_RAR up to y* then the monotone log splice (delta = 0.05); re-implemented from the CFG5_common docstring."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    h = np.where(y <= _YS, _h_rar(y), _h_rar(_YS) + _DELTA * _HP * np.log((y + _YP) / (_YS + _YP)))
    return 1.0 + h / y


NU = {"P2": nu_p2, "mono": nu_mono}


# ------------------------------------------------------------------------------------------------ geometry
def f_enc(s):
    return 1.0 - (1.0 + s) * np.exp(-s)


def c_geo(geom, rr, tier="S"):
    """c = V_bar^2 r / (G M_bar): rr = r / r_e."""
    if tier == "G":
        return 1.0
    if geom == "GS":
        return float(f_enc(1.678 * rr))
    if geom == "GC":
        return float(f_enc(1.678 * rr / 0.6))
    if geom == "GD":
        rd = 1.0 / 1.678                      # r_d in units of r_e
        r = rr
        y = r / (2 * rd)
        return float(2 * (r / rd) * y * y * (i0(y) * k0(y) - i1(y) * k1(y)))
    raise ValueError(geom)


# ------------------------------------------------------------------------------------------------ cosmology (Planck 2018 values as hunt_lib)
h = 0.674
OM_B = 0.02237 / h ** 2
OM_M = (0.02237 + 0.1200) / h ** 2
OM_L = 1 - OM_M
NS, S8, DELTA_C = 0.965, 0.811, 1.686
C_KMS = 299792.458
H0 = 100.0 * h
RHO_CRIT0 = 2.77536627e11 * h ** 2          # Msun / Mpc^3
RHO_M_COM = 2.775e11 * OM_M                 # Msun/h per (Mpc/h)^3


def E(z):
    return np.sqrt(OM_M * (1 + np.asarray(z, float)) ** 3 + OM_L)


def Dc(z):
    return C_KMS / H0 * quad(lambda t: 1.0 / E(t), 0, z)[0]      # Mpc


def kpc_per_arcsec(z):
    return Dc(z) / (1 + z) * 1e3 * math.pi / 648000.0


def vol_survey(z, area_deg2=2.0, dz=1.0):
    om = area_deg2 * (math.pi / 180.0) ** 2
    return om / 3.0 * (Dc(z + dz / 2) ** 3 - Dc(max(z - dz / 2, 0.0)) ** 3)       # Mpc^3 comoving


# Eisenstein & Hu 1998 no-wiggle transfer function
_theta, _om, _ob = 2.7255 / 2.7, OM_M * h * h, OM_B * h * h
_fb = _ob / _om
_s_eh = 44.5 * math.log(9.83 / _om) / math.sqrt(1 + 10 * _ob ** 0.75)
_alpha_g = 1 - 0.328 * math.log(431 * _om) * _fb + 0.38 * math.log(22.3 * _om) * _fb ** 2


def T_eh(k):
    kmpc = np.asarray(k, float) * h
    gam = OM_M * h * (_alpha_g + (1 - _alpha_g) / (1 + (0.43 * kmpc * _s_eh) ** 4))
    q = np.asarray(k, float) * _theta ** 2 / gam
    L = np.log(2 * math.e + 1.8 * q)
    Cc = 14.2 + 731.0 / (1 + 62.5 * q)
    return L / (L + Cc * q * q)


_KG = np.logspace(-4, 3.0, 4000)
_PG = _KG ** NS * T_eh(_KG) ** 2


def _sigma2(R):
    x = _KG * R
    W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return np.trapz(_KG ** 2 * _PG * W ** 2, _KG) / (2 * math.pi ** 2)


_AMP = S8 ** 2 / _sigma2(8.0)
_LM = np.linspace(1.0, 16.5, 500)
_LS = np.array([0.5 * math.log(_AMP * _sigma2((3 * 10 ** lm / (4 * math.pi * RHO_M_COM)) ** (1 / 3.))) for lm in _LM])
_dlnsig = np.gradient(_LS, _LM * LN10)

_zg = np.concatenate([np.linspace(0, 5, 60), np.linspace(5.1, 60, 150)])


def _growth_raw(z):
    a = 1.0 / (1 + z)
    f = lambda x: 1.0 / (x * math.sqrt(OM_M / x ** 3 + OM_L)) ** 3
    return float(E(z)) * quad(f, 1e-9, a, limit=200)[0]


_D0 = _growth_raw(0.0)
_Dg = interp1d(_zg, np.array([_growth_raw(z) / _D0 for z in _zg]), kind="cubic")


def growth(z):
    return float(_Dg(z))


def dndlnM_h(lm, z):
    """Sheth-Tormen dn/dlnM in (h/Mpc)^3; lm = log10 of M in Msun/h."""
    sig = np.exp(np.interp(lm, _LM, _LS)) * growth(z)
    nup = math.sqrt(0.707) * DELTA_C / sig
    nufnu = 0.3222 * math.sqrt(2 / math.pi) * nup * (1 + nup ** (-0.6)) * np.exp(-nup ** 2 / 2)
    return (RHO_M_COM / 10 ** lm) * nufnu * np.abs(np.interp(lm, _LM, _dlnsig))


def n_above_h(Mh, z, lmax=16.2):
    lm0 = math.log10(Mh)
    if lm0 >= lmax:
        return 0.0
    xs = np.linspace(lm0, lmax, 400)
    return float(np.trapz(dndlnM_h(xs, z) * LN10, xs))


_LGRID = np.linspace(8.0, 16.4, 841)           # log10 M200 (Msun)


def logN_table(z, vol_mpc3):
    """log10 N_exp(> M200) on _LGRID for survey volume (Mpc^3 comoving); M200 in Msun (converted to Msun/h)."""
    lm = _LGRID + math.log10(h)
    dn = dndlnM_h(np.linspace(lm[0], 16.5, 1500), z) * LN10          # per dlog10M
    xs = np.linspace(lm[0], 16.5, 1500)
    cum = np.concatenate([[0], np.cumsum(0.5 * (dn[1:] + dn[:-1]) * np.diff(xs))])
    tot = cum[-1]
    nab = np.maximum(tot - np.interp(lm, xs, cum), 1e-320)           # (h/Mpc)^3
    return np.log10(nab * h ** 3 * vol_mpc3)


def rho_crit_z(z):
    return RHO_CRIT0 * float(E(z)) ** 2 / 1e9                        # Msun / kpc^3


def r200_kpc(M200, z):
    return (3 * M200 / (4 * math.pi * 200 * rho_crit_z(z))) ** (1 / 3.)


def logc_dm14(lM200, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21)
    b = -0.101 + 0.026 * z
    return a + b * (lM200 - 12.0 + math.log10(h))


def logc_d08(lM200, z):
    return math.log10(5.71) - 0.084 * (lM200 - math.log10(2e12) + math.log10(h)) - 0.47 * math.log10(1 + z)


CM = {"DM14": logc_dm14, "D08": logc_d08}
SIG_LOGC = 0.11


def nfw_dm_enc(lM200, r_kpc, z, cm, dlogc=0.0):
    M200 = 10 ** np.asarray(lM200, float)
    c = 10 ** (np.array([CM[cm](l, z) for l in np.atleast_1d(lM200)]) + dlogc)
    R200 = (3 * M200 / (4 * math.pi * 200 * rho_crit_z(z))) ** (1 / 3.)
    x = r_kpc / R200
    m = lambda u: np.log(1 + u) - u / (1 + u)
    return M200 * m(c * x) / m(c)


# ------------------------------------------------------------------------------------------------ loaders
def rd(f):
    return list(csv.DictReader(open(os.path.join(TAB, f))))


def fnum(s, default=float("nan")):
    try:
        v = float(s)
        return v
    except Exception:
        return default


def fin(s):
    return math.isfinite(fnum(s))


KNOWN = {"D_1082948", "D_1009935", "D_1015956", "D_1085659", "C_02", "C_03", "C_23b"}
KNOWN_SEEN = {"R_BRI1335-0417", "C_09", "C_15"}            # section 10: also known before freezing
CRISTAL_FIELD_GOODSS = {"08": "ECDFS", "12": "GOODS-S"}
DUST_DET = {"02", "03", "07a", "11", "19", "20"}
RO_RINGS = {"BRI1335-0417": (5, 0.15), "J081740": (4, 0.13), "SGP38326-1": (5, 0.13), "SGP38326-2": (3, 0.12)}


def load_sample():
    rows = []
    # D -- Danhaive gold
    for r in rd("danhaive2025_gold.csv"):
        rows.append(dict(id="D_" + r["jades_id"], src="D", kind="D", tier="S", z=fnum(r["z"]), field="GOODS",
                         lMstar=fnum(r["logMstar"]), e_Mstar_lo=fnum(r["logMstar_errlo"], 0.0),
                         lMdyn=fnum(r["logMdyn"]), e_Mdyn_hi=fnum(r["logMdyn_errhi"], 0.0),
                         r_kpc=fnum(r["re_kpc"]), e_r_hi=fnum(r["re_kpc_errhi"], 0.0), e_r_lo=fnum(r["re_kpc_errlo"], 0.0),
                         rr=1.0, sigma0=fnum(r["sigma0_kms"]), sigma_lim=r["sigma0_kms_lim"],
                         vsig=fnum(r["v_over_sigma0"]), Mstar_lim=r["logMstar_lim"], Mdyn_lim=r["logMdyn_lim"],
                         gas=None))
    # C -- CRISTAL
    samp = {r["id"]: r for r in rd("cristal2025_sample.csv")}
    kin = {r["id"]: r for r in rd("cristal2025_kinematics.csv")}
    names = {i: samp[i]["name"] for i in samp}

    def find(tab, i):
        return tab.get(i) if i in tab else tab.get(i + "a")

    def field_of(i):
        base = "".join(ch for ch in i if ch.isdigit())[:2]
        nm = None
        for k2, v2 in names.items():
            if "".join(ch for ch in k2 if ch.isdigit())[:2] == base and v2 != "\\ldots":
                nm = v2
                break
        nm = nm or ""
        if "efdcs" in nm:
            return "ECDFS"
        if "GOODSS" in nm:
            return "GOODS-S"
        return "COSMOS"

    for r in rd("cristal2025_dynamics.csv"):
        i = r["id"]
        s = find(samp, i)
        k = find(kin, i)
        mstar = fnum(s["logMstar"]) if s else float("nan")
        fm = fnum(k["f_molgas"]) if k else float("nan")
        gas = None
        if i in DUST_DET and math.isfinite(mstar) and math.isfinite(fm):
            gas = float(mstar + math.log10(fm / (1 - fm)))
        rows.append(dict(id="C_" + i, src="C", kind="C", tier="S", z=fnum(s["z_cii"]), field=field_of(i),
                         lMstar=mstar, e_Mstar_lo=0.0,
                         vrot=fnum(r["Vrot_Re_kms"]), e_vrot_hi=fnum(r["Vrot_Re_kms_errhi"], 0.0),
                         sigma0=fnum(r["sigma0_kms"]), e_sig_hi=fnum(r["sigma0_kms_errhi"], 0.0),
                         r_kpc=fnum(r["Re_disk_kpc"]), e_r_hi=fnum(r["Re_disk_kpc_errhi"], 0.0), e_r_lo=fnum(r["Re_disk_kpc_errlo"], 0.0),
                         rr=1.0, vsig=fnum(r["Vrot_Re_kms"]) / fnum(r["sigma0_kms"]), lgas=gas,
                         fdm=fnum(r["fDM_Re"]), Mstar_lim="", Mdyn_lim="", sigma_lim="",
                         mapped=(i not in samp)))
    # R -- Roman-Oliveira (tier G)
    ro = {r["id"]: r for r in rd("romanoliveira2023_kinematics.csv")}
    rs = {r["id"]: r for r in rd("romanoliveira2023_sample.csv")}
    rg = {r["id"]: r for r in rd("romanoliveira2023_gasmasses.csv")}
    for i, r in ro.items():
        z = fnum(rs[i]["z"])
        n, sep = RO_RINGS[i]
        rk = (n - 1) * sep * fnum(rs[i]["kpc_per_arcsec"])
        mh = fnum(rg[i]["mh2_msun"])
        e = fnum(rg[i]["e_mh2"])
        sdg = (e / mh / LN10) if math.isfinite(e) else 0.30          # phase-2 reading: missing error -> 0.3 dex (as CFG197)
        rows.append(dict(id="R_" + i, src="R", kind="R", tier="G", z=z, field="none", lMstar=float("nan"), e_Mstar_lo=0.0,
                         vext=fnum(r["vrot_ext_kms"]), e_v_hi=fnum(r["vrot_ext_kms_errhi"], 0.0),
                         sigma0=fnum(r["sigma_ext_kms"]), e_sig_hi=fnum(r["sigma_ext_kms_errhi"], 0.0),
                         r_kpc=rk, e_r_hi=0.0, e_r_lo=0.0, rr=1.0, vsig=fnum(r["vext_over_sigma_ext"]),
                         lgas_floor=math.log10(mh / 3.0), sd_gas=sdg, gas_err_missing=not math.isfinite(e),
                         Mstar_lim="", Mdyn_lim="", sigma_lim=""))
    # A -- Amvrosiadis (z >= 3.5 fitted)
    par = {r["alessid"]: r for r in rd("amvrosiadis_parent.csv")}
    for r in rd("amvrosiadis_bestfit.csv"):
        a = r["alessid"]
        z = fnum(par[a]["z"])
        if z <= 3.5:
            continue
        kpa = kpc_per_arcsec(z)
        rows.append(dict(id="A_" + a, src="A", kind="A", tier="S", z=z, field="ECDFS", lMstar=fnum(par[a]["logMstar"]),
                         e_Mstar_lo=fnum(par[a]["logMstar_errlo"], 0.0),
                         vc=fnum(r["vcirc_2re_kms"]), e_v_hi=fnum(r["vcirc_2re_kms_errhi"], 0.0),
                         sigma0=fnum(r["sigma_kms"]), r_kpc=2 * fnum(r["re_arcsec"]) * kpa,
                         e_r_hi=2 * fnum(r["re_arcsec_errhi"], 0.0) * kpa, e_r_lo=2 * fnum(r["re_arcsec_errlo"], 0.0) * kpa,
                         rr=2.0, vsig=fnum(r["vmax_kms"]) / fnum(r["sigma_kms"]), Mstar_lim="", Mdyn_lim="", sigma_lim="",
                         flag_agn=(a == "071.1")))
    # P -- ALPAKA ID 28
    pr = {r["id"]: r for r in rd("alpaka1_properties.csv")}["28"]
    pk = {r["id"]: r for r in rd("alpaka1_kinematics.csv")}["28"]
    ps = {r["id"]: r for r in rd("alpaka1_sample.csv")}["28"]
    with open(os.path.join(TAB, "alpaka1_digitised", "alpaka1_outer_summary.csv")) as f:
        od = {r["id"]: r for r in csv.DictReader(f)}["28"]
    ms = fnum(pr["mstar_1e10msun"]) * 1e10
    es = fnum(pr["e_mstar"]) * 1e10
    rows.append(dict(id="P_28", src="P", kind="P", tier="S", z=fnum(ps["z"]), field="none", lMstar=math.log10(ms),
                     e_Mstar_lo=math.log10(ms) - math.log10(ms - es),
                     vext=fnum(pk["vext_kms"]), e_v_hi=fnum(pk["vext_errhi"], 0.0), sigma0=fnum(pk["sigma_ext_kms"]),
                     r_kpc=fnum(od["R_ext_kpc"]), e_r_hi=0.0, e_r_lo=0.0, rr=1.0,
                     vsig=fnum(pk["vext_kms"]) / fnum(pk["sigma_ext_kms"]), Mstar_lim="", Mdyn_lim="",
                     sigma_lim=pk["sigma_ext_lim"], re_digitised_kpc=fnum(od["Re_kpc_dashed_line"])))
    for r in rows:
        r["known"] = "known-before-freezing" if r["id"] in KNOWN else ("known-seen-in-READMEs" if r["id"] in KNOWN_SEEN else "")
    return rows


# ------------------------------------------------------------------------------------------------ draws
def _ln(v, err):
    return err / (v * LN10) if (v > 0 and math.isfinite(err)) else 0.0


def base_draws(row, n, rng):
    """standard normals shared by every cell (common random numbers)."""
    return {k: rng.standard_normal(n) for k in ("V", "s", "r", "d", "b", "ds", "bs")}


def gen(row, nd, n=None):
    """log10 of M_dyn,enc, baryon floor M_b and r (kpc) for each draw (statistical errors only)."""
    k = row["kind"]
    if k == "D":
        lMd = row["lMdyn"] - math.log10(KTOT_D) + row["e_Mdyn_hi"] * nd["d"]
        rsd = 0.5 * (row["e_r_hi"] + row["e_r_lo"])
        lr = math.log10(row["r_kpc"]) + _ln(row["r_kpc"], rsd) * nd["r"]
        vc2 = None
    elif k in ("C", "R", "P", "A"):
        V = row.get("vrot", row.get("vext", row.get("vc")))
        eV = row.get("e_vrot_hi", row.get("e_v_hi", 0.0))
        lV = math.log10(V) + _ln(V, eV) * nd["V"]
        V2 = 10 ** (2 * lV)
        if k == "A":
            vc2 = V2
        else:
            sg = row["sigma0"]
            esg = row.get("e_sig_hi", 0.0)
            lsg = math.log10(sg) + _ln(sg, esg) * nd["s"]
            vc2 = V2 + K_PRESS * 10 ** (2 * lsg)
        if k in ("C", "A"):
            lr = math.log10(row["r_kpc"]) + _ln(row["r_kpc"], row["e_r_hi"]) * nd["r"]
        else:
            lr = np.full_like(nd["r"], math.log10(row["r_kpc"]))
        lMd = np.log10(vc2) + lr - math.log10(G_KPC)
    else:
        raise ValueError(k)
    if row["tier"] == "G":
        lMb = row["lgas_floor"] + row["sd_gas"] * nd["b"]
    else:
        lMb = row["lMstar"] + row["e_Mstar_lo"] * nd["b"]
    return lMd, lMb, lr


def gas_ext(row, nd):
    """S+G cell: measured gas at x1/3 (only the six CRISTAL dust detections)."""
    g = row.get("lgas")
    return None if g is None else g - math.log10(3.0)


def logmb(row, lMb, nd, sb, gas_mult=None):
    """baryon floor (log) for one cell: stars (or gas for tier G); MUTATE 4 adds gas x3."""
    lm = lMb + sb * nd["bs"]
    if MUT == 4 and row.get("lgas") is not None:
        lm = np.log10(10 ** lm + 3.0 * 10 ** row["lgas"])
    return lm


def limit_untestable(row):
    """section 3.5: M* upper limit -> no lower bound on the floor; M_dyn lower limit -> no break possible."""
    if row["tier"] == "S" and (not math.isfinite(row["lMstar"]) or str(row.get("Mstar_lim", "")).strip() in ("<", "upper")):
        return True
    if str(row.get("Mdyn_lim", "")).strip() in (">",):
        return True
    return False


def cell_stats(row, nd, dr, geom, sset, kern=None, foot=None, extra_gas=False, nop=False):
    """returns (mean, sd) of Delta = log floor - log R_obs  for L1 (kern None) or F1."""
    lMd, lMb, lr = dr
    sb, sd_ = SIGSET[sset]
    lMd_c = lMd + sd_ * nd["ds"]
    if nop and row["kind"] in ("D", "C"):
        pass
    lmb = logmb(row, lMb, nd, sb)
    if extra_gas and row.get("lgas") is not None:
        lmb = np.log10(10 ** lmb + 10 ** (row["lgas"] - math.log10(3.0)))
    cg = c_geo(geom, row["rr"], row["tier"])
    if MUT == 5 and row.get("fdm") is not None:
        lMd_c = lmb + math.log10(cg) + math.log10(1.0 / max(1.0 - row["fdm"], 1e-9))
    dL1 = lmb + math.log10(cg) - lMd_c                    # -log10 R_obs
    if kern is None:
        d = dL1
    else:
        gstar = cg * G_KPC * 10 ** lmb / 10 ** (2 * lr)
        x = gstar / A0K[foot]
        d = dL1 + np.log10(NU[kern](x))
    return float(np.mean(d)), float(np.std(d))


def rng_for(row_id, seed=SEED):
    hh = int(hashlib.sha256(row_id.encode()).hexdigest()[:8], 16)
    return np.random.default_rng([seed, hh])


def score_row_LF(row, n=N_MC, nop=False):
    """L1 and F1 over every frozen cell.  Returns dict; z = mean/sd; nan if undefined / not testable."""
    out = dict(id=row["id"])
    if limit_untestable(row):
        out.update(L1=dict(defined=False, reason="no finite/valid stellar floor (M* missing or upper limit)"),
                   F1=dict(defined=False, reason="same"))
        return out
    rng = rng_for(row["id"])
    nd = base_draws(row, n, rng)
    dr = gen(row, nd)
    if nop and row["kind"] in ("D", "C"):
        pass
    res = {}
    for crit in ("L1", "F1"):
        cells = {}
        if MUT == 1:
            swap = "F1" if crit == "L1" else "L1"
        else:
            swap = crit
        for geom in GEOMS:
            for sset in SIGSET:
                if swap == "L1":
                    m, s = cell_stats(row, nd, dr, geom, sset)
                    cells[(geom, sset, "-", "-")] = (m, s)
                else:
                    for kern in KERN:
                        for foot in FOOT:
                            cells[(geom, sset, kern, foot)] = cell_stats(row, nd, dr, geom, sset, kern, foot)
        if MUT == 1 and crit == "L1":
            # L1 now reads the framework floor: replicate over kernel/footing cells
            pass
        zs = {c: (m / s if s > 0 else (math.inf if m > 0 else -math.inf)) for c, (m, s) in cells.items()}
        prim_key = next(k for k in zs if k[0] == "GS" and k[1] == "primary" and (k[2] in ("-", "P2")) and (k[3] in ("-", "canonical")))
        zmin_key = min(zs, key=lambda k: zs[k])
        zrob = zs[zmin_key] if MUT != 6 else zs[prim_key]
        ckey = zmin_key if MUT != 6 else prim_key
        res[crit] = dict(defined=True, z_primary=zs[prim_key], z_rob=zrob, cell_min="/".join(ckey),
                         delta_min=cells[ckey][0], sd_min=cells[ckey][1], n_cells=len(cells))
    out.update(res)
    # analytic L1 check (primary cell)
    lMd, lMb, lr = dr
    sb, sd_ = SIGSET["primary"]
    cg = c_geo("GS", row["rr"], row["tier"])
    mean_an = (np.mean(lMb) + math.log10(cg)) - np.mean(lMd)
    sd_an = math.sqrt(np.var(lMb) + np.var(lMd) + sb ** 2 + sd_ ** 2)
    out["L1_z_analytic_primary"] = float(mean_an / sd_an)
    # reported-only variants (primary cell): S+G, no-pressure
    rep = {}
    if row.get("lgas") is not None:
        m, s = cell_stats(row, nd, dr, "GS", "primary", extra_gas=True)
        rep["SG_L1_z"] = m / s
        m, s = cell_stats(row, nd, dr, "GS", "primary", "P2", "canonical", extra_gas=True)
        rep["SG_F1_z"] = m / s
    out["reported"] = rep
    return out


# ------------------------------------------------------------------------------------------------ L2
L2_VOLS = [1.0, 10.0]
AREA_ACTUAL = 0.049
L2_SHIFT = [0.0, -0.3]
L2_SCAT = [0.0, SIG_LOGC]
L2_CM = ["DM14", "D08"]
_Nt_cache = {}


def Ntab(z, area):
    key = (round(z, 4), round(area, 5))
    if key not in _Nt_cache:
        _Nt_cache[key] = logN_table(z, vol_survey(z, area))
    return _Nt_cache[key]


def score_row_L2(row, n=N_MC, clamp=False):
    z = row["z"]
    out = dict(id=row["id"], z=z)
    if limit_untestable(row):
        out.update(defined=False, reason="no stellar/baryon floor")
        return out
    if z > 5.0 and not clamp:
        out.update(defined=False, reason="z > 5: outside the c-M calibration (UNDEFINED, frozen rule)")
        return out
    zc = min(z, 5.0)
    rng = rng_for(row["id"])
    nd = base_draws(row, n, rng)
    lMd, lMb, lr = gen(row, nd)
    r_kpc = row["r_kpc"]
    cg = c_geo("GS", row["rr"], row["tier"])
    # central values (primary sigma, no noise)
    need0 = 10 ** np.mean(lMd) - cg * 10 ** np.mean(lMb)
    area0 = 2.0 if MUT != 7 else AREA_ACTUAL
    out["need_central_Msun"] = float(need0)
    if need0 <= 0:
        out.update(defined=True, not_needed=True, z_rob=0.0, z_primary=0.0, n_exp_central=None, literal_break=False)
        return out
    lg = _LGRID

    def inv(need_arr, cm, dlogc):
        tab = np.log10(np.maximum(nfw_dm_enc(lg, r_kpc, zc, cm, dlogc), 1e-30))
        lnd = np.log10(np.maximum(need_arr, 1e-30))
        return np.interp(lnd, tab, lg)             # log10 M200 (clamped at grid ends)

    lM200_c = float(inv(np.array([need0]), "DM14", 0.0)[0])
    out["M200_central_log"] = lM200_c
    if not (10.0 <= lM200_c <= 15.0):
        out.update(defined=False, reason="solved M200 outside 1e10-1e15 (UNDEFINED, frozen rule)", M200_central_log=lM200_c)
        return out
    Nt0 = Ntab(z, area0)
    out["n_exp_central"] = float(10 ** np.interp(lM200_c, lg, Nt0))
    out["literal_break"] = bool(out["n_exp_central"] < 1.0)
    # 1-halo mass at V_ref
    out["M1_log"] = float(np.interp(0.0, Nt0[::-1], lg[::-1]))
    cells = {}
    for sset, (sb, sdy) in SIGSET.items():
        lMd_c = lMd + sdy * nd["ds"]
        lmb = lMb + sb * nd["bs"]
        need = 10 ** lMd_c - cg * 10 ** lmb
        pos = need > 0
        for cm in L2_CM:
            for sc in L2_SCAT:
                lM = inv(np.where(pos, need, 1e-30), cm, sc)
                for sh in L2_SHIFT:
                    for vm in L2_VOLS:
                        Nt = Ntab(z, area0 * vm)
                        N = 10 ** np.interp(lM + sh, lg, Nt)
                        N = np.where(pos, N, 1e30)
                        p2 = float(np.mean(-np.expm1(-np.minimum(N, 700.0))))
                        zz = float(norm.isf(max(p2, 1e-300))) if p2 < 1 else -8.0
                        cells[(sset, cm, sc, sh, vm)] = (zz, p2, float(np.mean(lM[pos] + sh)) if pos.any() else float("nan"),
                                                         float(np.std(lM[pos])) if pos.any() else float("nan"))
    zs = {c: v[0] for c, v in cells.items()}
    prim = ("primary", "DM14", 0.0, 0.0, 1.0)
    kmin = min(zs, key=lambda k: zs[k])
    zrob = zs[kmin] if MUT != 6 else zs[prim]
    km = kmin if MUT != 6 else prim
    m1 = float(np.interp(0.0, logN_table(z, vol_survey(z, area0 * km[4]))[::-1], lg[::-1]))
    out.update(defined=True, not_needed=False, z_primary=zs[prim], p2_primary=cells[prim][1], z_rob=zrob, cell_min="/".join(str(v) for v in km),
               p2_min=cells[km][1], delta_min=cells[km][2] - m1, sd_min=max(cells[km][3], 1e-3), n_cells=len(cells))
    return out


# ------------------------------------------------------------------------------------------------ look-elsewhere tiers
def wy_stepdown(delta, sigma, n_perm=100000, seed=SEED):
    """Westfall-Young step-down max-T over permutations of the residual vector with sigma held."""
    rng = np.random.default_rng(seed)
    delta = np.asarray(delta, float)
    sigma = np.asarray(sigma, float)
    n = len(delta)
    z = delta / sigma
    order = np.argsort(-z)
    cnt = np.zeros(n)
    done = 0
    chunk = 5000
    while done < n_perm:
        m = min(chunk, n_perm - done)
        perm = np.argsort(rng.random((m, n)), axis=1)
        Zs = delta[perm] / sigma[None, :]
        Zo = Zs[:, order]
        sufmax = np.maximum.accumulate(Zo[:, ::-1], axis=1)[:, ::-1]
        cnt += (sufmax >= z[order][None, :] - 1e-12).sum(axis=0)
        done += m
    p_sorted = cnt / n_perm
    p_sorted = np.maximum.accumulate(p_sorted)
    p = np.empty(n)
    p[order] = p_sorted
    return p


def parametric_null(delta, sigma, s_int=0.27, n_sim=100000, seed=SEED):
    """reported-only: truth exactly on the floor, noise sqrt(sigma^2 + s_int^2); step-down adjusted p for each galaxy."""
    rng = np.random.default_rng(seed + 1)
    delta = np.asarray(delta, float)
    sigma = np.asarray(sigma, float)
    n = len(delta)
    z = delta / sigma
    order = np.argsort(-z)
    cnt = np.zeros(n)
    done = 0
    while done < n_sim:
        m = min(5000, n_sim - done)
        Zs = rng.standard_normal((m, n)) * np.sqrt(sigma ** 2 + s_int ** 2)[None, :] / sigma[None, :]
        Zo = Zs[:, order]
        sufmax = np.maximum.accumulate(Zo[:, ::-1], axis=1)[:, ::-1]
        cnt += (sufmax >= z[order][None, :]).sum(axis=0)
        done += m
    p_sorted = np.maximum.accumulate(cnt / n_sim)
    p = np.empty(n)
    p[order] = p_sorted
    return p


def score_sample(rows, n=N_MC, n_perm=100000, n_sim=100000, m_trials=None):
    """full pipeline: L1, L2, F1 per row, three tiers, labels.  m_trials: Bonferroni family size."""
    global Z_B
    m_trials = m_trials or M_TRIALS
    zB = float(norm.isf(ALPHA_FW / m_trials))
    res = []
    for r in rows:
        lf = score_row_LF(r, n=n)
        l2 = score_row_L2(r, n=n)
        res.append(dict(id=r["id"], src=r["src"], z=r["z"], L1=lf["L1"], F1=lf["F1"], L2=l2, rep=lf.get("reported", {}),
                        l1_an=lf.get("L1_z_analytic_primary")))
    tiers = {}
    for crit in ("L1", "F1", "L2"):
        idx = [i for i, q in enumerate(res) if q[crit].get("defined") and not q[crit].get("not_needed", False)
               and q[crit].get("sd_min", 0) > 0]
        if crit == "L2":
            idx = [i for i in idx if math.isfinite(res[i][crit].get("delta_min", float("nan")))]
        d = np.array([res[i][crit]["delta_min"] for i in idx])
        s = np.array([res[i][crit]["sd_min"] for i in idx])
        if len(idx) >= 2:
            pw = wy_stepdown(d, s, n_perm=n_perm)
            pp = parametric_null(d, s, n_sim=n_sim)
        else:
            pw = np.ones(len(idx))
            pp = np.ones(len(idx))
        for j, i in enumerate(idx):
            res[i][crit]["p_wy"] = float(pw[j])
            res[i][crit]["p_param"] = float(pp[j])
        tiers[crit] = dict(n_defined=len(idx))
    for q in res:
        for crit in ("L1", "F1", "L2"):
            c = q[crit]
            z = c.get("z_rob") if c.get("defined") else None
            if z is None:
                c.update(T0=False, T1=False, T2=False, T2param=False)
                continue
            t0 = z > Z_THRESH
            t1 = z >= zB
            t2 = t1 and c.get("p_wy", 1.0) < 0.05
            if MUT == 3:
                t2 = t0
            c.update(T0=bool(t0), T1=bool(t1), T2=bool(t2), T2param=bool(t1 and c.get("p_param", 1.0) < 0.05))
    for q in res:
        for tier in ("T0", "T1", "T2"):
            lam = q["L1"][tier] or q["L2"][tier]
            fw = q["F1"][tier]
            q["label_" + tier] = ("both" if (lam and fw) else "LCDM-only" if lam else "framework-only" if fw else "neither")
    return res, dict(zB=zB, m=m_trials, tiers=tiers)


def sha256_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


FROZEN_SHA = "d70dad70f0964a645ae5963bb55db762a607ace212a4a404dac31b261137d9ba"


def frozen_path():
    for p in (os.path.join(REPO, "campaign_fresh_gravity", "CFG235_FROZEN_CRITERIA.md"), os.path.join(HERE, "CFG235_FROZEN_CRITERIA.md")):
        if os.path.exists(p):
            return p
    return None


SGRP = ("GOODS-S", "ECDFS", "GOODS")          # 'GOODS' (Danhaive: GOODS-S or GOODS-N) may overlap GOODS-S/ECDFS


def dup_pairs(rws):
    """frozen 2.4: same field AND |dz| <= 0.02, different sources => POSSIBLE duplicate."""
    pairs = []
    for a in rws:
        for b in rws:
            if a["id"] >= b["id"] or a["src"] == b["src"]:
                continue
            if a["field"] in SGRP and b["field"] in SGRP and abs(a["z"] - b["z"]) <= 0.02 + 1e-9:
                pairs.append((a["id"], b["id"], round(abs(a["z"] - b["z"]), 4), a["field"] + "/" + b["field"]))
    return pairs
