#!/usr/bin/env python3
"""CFG949 (criteria FROZEN_CRITERIA.md, 7330f9e99): clusters as UNTETHERED cold energy (H-UT).

Each eRASS1 cluster's whole cosmic-ratio cold supply (5.364 x catchment baryons) is ordinary self-gravitating cold matter in native
collapse-debris NFW (no law boost on it), scored with CFG687/CFG922's machinery: A_MID, A_OUTER and the T2 outer mass-scaling slope.

Stages (one at a time; OMP_NUM_THREADS=1 nice -n 10; run from this directory):
  CFG949_MODE=K       python3 cfg949.py   -> cfg949_K.out, cfg949_results_K.json            (K0-K5)
  CFG949_MODE=MUTATE  python3 cfg949.py   -> cfg949_MUTATE.out, cfg949_results_MUTATE.json  (MT, M0, MI, MS)
                      python3 cfg949.py   -> cfg949.out, cfg949_results.json                (main, B0/B1/B2, both footings)
Read-only inputs: CFG686 (exec'd slices of its script; no KiDS shear columns), CFG687 (law() slice, per-cluster npz, results), CFG922
(engine and Stack slices, K json, results), CFG932 (exec'd slice of its script, results), CFG930 (results), CFG654 native tables.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad, cumulative_trapezoid

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MODE = os.environ.get("CFG949_MODE", "MAIN").upper()
assert MODE in ("K", "MUTATE", "MAIN")
TAG = {"K": "_K", "MUTATE": "_MUTATE", "MAIN": ""}[MODE]
OUTF = open(os.path.join(HERE, "cfg949" + TAG + ".out"), "w")
T0 = time.time()
RSS_LIMIT_GB = 0.95


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()


def rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r * 1024 / 1e9


def guard(label):
    g = rss_gb()
    if g > RSS_LIMIT_GB:
        P(f"RSS GUARD: {g:.3f} GB > {RSS_LIMIT_GB} GB at '{label}' -> abort"); OUTF.close(); sys.exit(3)
    return g


CHECKS = []


def check(name, ok, detail):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail)); P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


# ============================================================================ CFG686 / CFG687 / CFG922 machinery (exec, read-only)
sys.path.insert(0, LANES)
os.environ.pop("MUTATE", None)
import CFG4_common as C4                                                     # noqa: E402  committed nu_mono + both footings
A0 = {"canonical": float(C4.A0["canonical"]), "alt": float(C4.A0["alt"])}
FEET = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15


def nu_s(y):                                                                 # g_N = g^2/(g + a0)  (CFG695/726/922)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


KERN = {"s": nu_s, "mono": C4.nu_mono}
TRAPZ = np.trapz

SRC686 = os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py"); TXT686 = open(SRC686).read()
NS = {"__file__": SRC686, "__name__": "cfg686"}
_argv = sys.argv; sys.argv = [SRC686, "UNUSED"]
with contextlib.redirect_stdout(io.StringIO()) as _buf:                      # CFG922's exec recipe, verbatim (no KiDS sources)
    exec(TXT686.split("# ---- sources ----")[0], NS)
    NS["EDGES"] = np.logspace(np.log10(0.15), np.log10(3.0), 9); NS["RC"] = np.sqrt(NS["EDGES"][1:] * NS["EDGES"][:-1]); NS["M_BIAS"] = -0.01
    exec(TXT686.split("# ---- the law's prediction from ACCEPT gas ----")[1].split("# ---- measure ----")[0], NS)
sys.argv = _argv
SELFTEST = _buf.getvalue().strip().splitlines()
G, MSUN, MPC, KG, DM, RC, RGRID = NS["G"], NS["MSUN"], NS["MPC"], NS["KG_PER_MSUN_PC2"], NS["DM"], NS["RC"], NS["RGRID"]
CLIGHT = NS["c"]

SRC687 = os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_stack.py"); TXT687 = open(SRC687).read()
NS7 = dict(RGRID=RGRID, MPC=MPC, MSUN=MSUN, G=G, nu_mono=C4.nu_mono, sigma_proj=NS["sigma_proj"], RC=RC, KG=KG, np=np)
exec("def law(" + TXT687.split("def law(")[1].split("BR = [")[0], NS7)
law687 = NS7["law"]

SRC922 = os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922.py"); TXT922 = open(SRC922).read()
E9 = dict(np=np, math=math, G=G, MSUN=MSUN, MPC=MPC, KG=KG, DM=DM, RC=RC, RGRID=RGRID, CLIGHT=CLIGHT, NS=NS, TRAPZ=TRAPZ)
exec("R = RGRID; RM = R * MPC" + TXT922.split("R = RGRID; RM = R * MPC")[1].split("A_BCG = 0.015")[0], E9)   # engine, gas_beta, gas_accept
exec(TXT922.split("# ---- band amplitudes ----")[1].split("# ---- inputs ----")[0], E9)                      # Stack, zsc
dsig_law, gas_beta, gas_accept, proj_cyl, Stack, PRE = E9["dsig"], E9["gas_beta"], E9["gas_accept"], E9["proj_cyl"], E9["Stack"], E9["PRE"]
R = RGRID; RM = R * MPC; NR = len(R); RKPC = R * 1e3
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}


def dsig_newton(M3, chunk=40):
    """truncation-aware Newtonian DeltaSigma (Msun/pc^2) of a 3D cumulative mass (N x NR, kg): CFG922's vectorised algebra with
    log rho floored at 1e-300 in EVERY row (no clamped fallback), so a truncated density projects as zero beyond its edge."""
    M3 = np.atleast_2d(M3)
    if M3.shape[0] > chunk:
        return np.vstack([dsig_newton(M3[i:i + chunk], chunk) for i in range(0, M3.shape[0], chunk)])
    rho = np.gradient(M3, RM, axis=1) / (4 * np.pi * RM ** 2)
    lrho = np.log(np.where(rho > 0, rho, 1e-300)); out = np.empty((M3.shape[0], len(RC)))
    for j, (u, rr, i0, f, sel, fac) in enumerate(PRE):
        Sig = 2 * TRAPZ(np.exp((1 - f) * lrho[:, i0] + f * lrho[:, i0 + 1]) * rr * MPC, u, axis=1)
        M2 = np.array([np.interp(RC[j], R, m) for m in M3]) + TRAPZ(rho[:, sel] * fac, R[sel] * MPC, axis=1)
        out[:, j] = (M2 / (np.pi * (RC[j] * MPC) ** 2) - Sig) / KG
    return out


def law_split(Mb, a0, nu):
    """law lensing mass ML and phantom (kg) on RGRID for baryons Mb (N x NR), CFG687 law() algebra."""
    gb = G * Mb / RM ** 2; gL = gb * nu(gb / a0); ML = gL * RM ** 2 / G
    return ML, ML - Mb


# ---- inputs ----
PC7 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
R7 = json.load(open(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_results.json")))
R6 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))
K922 = json.load(open(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_K.json")))["K"]
RES922 = json.load(open(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_results.json")))["results"]
R932 = json.load(open(os.path.join(LANES, "CFG932_settling_energy_bookkeeping", "cfg932_results.json")))
R930 = json.load(open(os.path.join(LANES, "CFG930_energy_limited_settling", "cfg930_results.json")))
MG, R500, ZC, RA, DEC = (np.asarray(PC7[k], float) for k in ("mg", "R500", "z", "ra", "dec"))
D7 = np.nan_to_num(np.asarray(PC7["D"], float)); E7 = np.asarray(PC7["E"], float); NE = len(MG)
STE = Stack(D7, E7, RA, "jk")
W7 = np.where(E7 > 0, 1 / E7 ** 2, 0)                                       # CFG687's T2 weights, verbatim
_order = np.argsort(RA); PATCH = np.empty(NE, int); PATCH[_order] = np.arange(NE) * 30 // NE
_q = np.quantile(MG, [0, 1 / 3, 2 / 3, 1]); TID = np.clip(np.digitize(MG, _q[1:-1]), 0, 2)


def outer_stack(sel, arr):
    j = BANDS["OUTER"]; return (W7[sel][:, j] * arr[sel][:, j]).sum() / W7[sel][:, j].sum()


def slope(sel, arr):                                                         # CFG687 T2, verbatim
    xs, ys = [], []
    for t in range(3):
        s = sel & (TID == t); v = outer_stack(s, arr)
        if v <= 0: return np.nan
        xs.append(np.log10(np.median(MG[s]))); ys.append(np.log10(v))
    return np.polyfit(xs, ys, 1)[0]


def slope_obs():
    full = slope(np.ones(NE, bool), D7); reps = np.array([slope(PATCH != p, D7) for p in range(30)])
    return float(full), float(np.sqrt(29 / 30 * np.sum((reps - reps.mean()) ** 2)))


S_OBS, S_ERR = slope_obs()


def s_model(Pm): return float(slope(np.ones(NE, bool), Pm))


def band_sel(Pm, sel):
    """A per band on a subset, with the 30-patch jackknife restricted to that subset."""
    def A(s): return {b: float((W7[s][:, j] * D7[s][:, j]).sum() / (W7[s][:, j] * Pm[s][:, j]).sum()) for b, j in BANDS.items()}
    full = A(sel); reps = [A(sel & (PATCH != p)) for p in range(30)]
    return {k: (full[k], float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}


def lam_band(Pb, Pc, band):
    """multiplier on the cold component that makes A_band = 1 (closed form; A is linear in the model)."""
    j = BANDS[band]; W = STE.W
    return float(((W[:, j] * STE.D[:, j]).sum() - (W[:, j] * Pb[:, j]).sum()) / (W[:, j] * Pc[:, j]).sum())


# ============================================================================ native cosmology: R930 family (CFG930 code, copied)
GMPC = 4.30091727e-9                                                         # CFG7_common G [Mpc (km/s)^2 / Msun]
SUP = 5.364; FBN = 1.0 / (1.0 + SUP)
DELTA_C, FPROG, MED_HN = 1.686, 0.01, 0.6744897501960817
TS = np.load(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_scorer_tables_cmb.npz"))
TI = np.load(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_ics_tables_cmb.npz"))
DTA = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta_cmb.json")))
h_, Om, Or, OL, NSI = float(TS["h"]), float(TS["Om"]), float(TS["Or"]), float(TS["OL"]), float(TI["ns"])
KH, PK = np.asarray(TS["kh"], float), np.asarray(TS["Plin_z0"], float)
LNA_T, LND_T = np.asarray(TS["lna"], float), np.asarray(TS["lnD"], float)
ZTA, DTAV = np.array(DTA["z"], float), np.array(DTA["D"], float); DTA0 = float(DTAV[0])
RHOC_H = 3 * 100.0 ** 2 / (8 * math.pi * GMPC); RHOM0_H = Om * RHOC_H; RHOM0_KPC = Om * RHOC_H * h_ ** 2 / 1e9
GAM = Om * h_
KK = np.logspace(-4, 5, 9001); LKK = np.log(KK); KMAX = float(KH[-1])
PT = np.exp(np.interp(LKK, np.log(KH), np.log(PK)))
_ext = KK > KMAX
PT[_ext] = PK[-1] * (KK[_ext] / KMAX) ** (NSI - 4.0) * (np.log1p(2.34 * KK[_ext] / GAM) / math.log1p(2.34 * KMAX / GAM)) ** 2


def W_th(x):
    x = np.asarray(x, float); out = np.empty_like(x); s = x < 1e-3
    out[s] = 1.0 - x[s] ** 2 / 10.0; xx = x[~s]; out[~s] = 3.0 * (np.sin(xx) - xx * np.cos(xx)) / xx ** 3
    return out


def sig2_R(R_):
    return float(np.trapz(KK ** 3 * PT * W_th(KK * R_) ** 2, LKK) / (2 * math.pi ** 2))


LMG = np.arange(0.0, 17.0001, 0.01)
SIG2G = np.array([sig2_R((3 * 10 ** lm * h_ / (4 * math.pi * RHOM0_H)) ** (1.0 / 3.0)) for lm in LMG])


def sig2M(M): return float(np.exp(np.interp(math.log10(M), LMG, np.log(SIG2G))))


LND0 = float(np.interp(0.0, LNA_T, LND_T)); LNDN = LND_T - LND0


def D_of_z(z): return float(math.exp(np.interp(-math.log1p(z), LNA_T, LNDN)))


def z_of_D(D): return float(math.exp(-np.interp(math.log(D), LNDN, LNA_T)) - 1.0)


def m_(x):
    x = np.asarray(x, float)
    return np.where(x < 1e-3, x * x / 2 - 2 * x ** 3 / 3 + 3 * x ** 4 / 4, np.log1p(x) - x / (1 + x))


def conc_from(rhs):
    return math.exp(brentq(lambda lc: math.log(float(m_(math.exp(lc)))) - 3 * lc - math.log(rhs), math.log(1e-4), math.log(1e8), xtol=1e-13))


_lna = np.linspace(-20.0, 0.0, 20001); _a = np.exp(_lna)
_H = 100 * h_ * np.sqrt(Om / _a ** 3 + Or / _a ** 4 + OL)
_t = cumulative_trapezoid(1.0 / _H, _lna, initial=0.0) + 0.5 / (100 * h_ * math.sqrt(Or)) * _a[0] ** 2


def dta_of(z):                                                               # Delta_ta(z): linear in ln(1+z) between the N0 nodes
    return float(np.interp(math.log1p(z), np.log1p(ZTA), DTAV))


def dvir_of(z):                                                              # 8 Delta_ta(z_ta) [(1+z_ta)/(1+z)]^3, t(z_ta) = t(z)/2
    tz = float(np.interp(-math.log1p(z), _lna, _t)); a_ta = float(np.exp(np.interp(0.5 * tz, _t, _lna))); zt = 1.0 / a_ta - 1.0
    return 8.0 * dta_of(zt) * ((1.0 + zt) / (1.0 + z)) ** 3


def fret_of(lM):                                                             # CFG416 / CFG556 / CFG804 census, verbatim (CFG930)
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def mta_fixed(Mb):                                                           # CFG930 mta_fixed, verbatim
    f = 0.10; lMb = math.log10(Mb)
    for _ in range(200):
        lMta = lMb - math.log10(f * FBN); fn = fret_of(lMta)
        if abs(fn - f) < 1e-12: break
        f = 0.5 * (f + fn)
    return f, 10 ** lMta


def zcoll930(M, zi):
    ds2 = sig2M(FPROG * M) - sig2M(M)
    if ds2 <= 0: return zi
    Dc = 1.0 / (1.0 / D_of_z(zi) + MED_HN * math.sqrt(ds2) / DELTA_C)
    return max(z_of_D(Dc), zi)


def prof930(Mta, zi, C, bnd):
    """R930 native NFW: (c, r_s kpc, r_b kpc, z_c)."""
    zc = zcoll930(Mta, zi); Db = dta_of(zi) if bnd == "rta" else dvir_of(zi)
    rb = (3 * Mta / (4 * math.pi * Db * RHOM0_KPC * (1 + zi) ** 3)) ** (1.0 / 3.0)
    c = conc_from(Db * (1 + zi) ** 3 / (3 * C * (1 + zc) ** 3))
    return c, rb / c, rb, zc


# ============================================================================ R932 family (CFG932 functions exec'd read-only)
SRC932 = os.path.join(LANES, "CFG932_settling_energy_bookkeeping", "cfg932.py"); TXT932 = open(SRC932).read()
N9 = {"__file__": SRC932, "__name__": "cfg932"}
_m932 = os.environ.pop("CFG932_MUTATE", None)
exec(TXT932.split("def W_self(")[0], N9)                                     # constants, native tables, sigM, Dz, conc, systems, supply, phantom
from scipy.special import erfcinv                                            # noqa: E402


def conc932(Mta, rule, F, zi):
    """CFG932 conc() generalised to observation at z_i (z_i = 0 is CFG932's rule exactly); returns (c, flag)."""
    m1 = float(N9["mfun"](1.0)); Dti = N9["Dz"](zi); dta = dta_of(zi) * (1 + zi) ** 3
    def z_dens(c): return (dta * c ** 3 * m1 / float(N9["mfun"](c)) / N9["DVIR"]) ** (1 / 3) - 1
    def z_coll(c):
        Ms = Mta * m1 / float(N9["mfun"](c))
        if rule == "PS1":
            Dn = N9["DC"] / N9["sigM"](Ms)
        else:
            s2 = N9["sigM"](F * Mta) ** 2 - N9["sigM"](Mta) ** 2
            x = float(erfcinv(Ms / Mta)); Dn = N9["DC"] / (N9["DC"] / Dti + x * math.sqrt(2 * s2))
        return max(N9["z_of_D"](Dn), zi)
    f = lambda lc: z_dens(math.exp(lc)) - z_coll(math.exp(lc))
    if f(0.0) > 0: return 1.0, True
    return math.exp(brentq(f, 0.0, math.log(1e4), xtol=1e-12)), False


def prof932(Mta, zi, rule, F):
    c, flag = conc932(Mta, rule, F, zi)
    rb = (3 * Mta / (4 * math.pi * dta_of(zi) * N9["RHOM"] * (1 + zi) ** 3)) ** (1 / 3)
    return c, rb / c, rb, flag


PROFILES = [("C3000|rta", "930", 3000.0, "rta"), ("C1500|rta", "930", 1500.0, "rta"), ("C6000|rta", "930", 6000.0, "rta"),
            ("C3000|rvir", "930", 3000.0, "rvir"), ("C1500|rvir", "930", 1500.0, "rvir"), ("C6000|rvir", "930", 6000.0, "rvir"),
            ("PS1", "932", "PS1", None), ("EPS0.2", "932", "EPS", 0.2), ("EPS0.05", "932", "EPS", 0.05), ("EPS0.01", "932", "EPS", 0.01)]
SUPPLIES = ("S-cen", "S-floor", "S-closed", "S-R500")
PRIMARY = ("C3000|rta", "S-cen")


def supply(rule, Mgas3, Mgas500, fstar):
    """returns (M_ta, f_ret) in Msun for one cluster."""
    Mret = (1 + fstar) * Mgas3
    if rule == "S-cen":
        f, Mta = mta_fixed(Mret); return Mta, f
    if rule == "S-floor":
        bc = max(fstar * Mgas3 / 0.10, Mret / 0.90); return bc / FBN, Mret / bc
    if rule == "S-closed":
        return Mret / FBN, 1.0
    if rule == "S-R500":
        f, Mta = mta_fixed(1.2 * Mgas500); return Mta, f
    raise ValueError(rule)


def cold_profile(Mta, c, rs, rb):
    """(1 - f_b) M_ta NFW truncated at r_b, on RGRID, kg."""
    return (1 - FBN) * Mta * m_(np.minimum(RKPC, rb) / rs) / float(m_(c)) * MSUN


def build_cold(prof, sup, gas_kg, fstar, zrule="own"):
    """per-cluster cold arrays (kg) and meta for one profile x supply corner."""
    name, fam, a, b = [p for p in PROFILES if p[0] == prof][0]
    Mg3 = gas_kg[:, -1] / MSUN; out = np.empty((NE, NR)); meta = dict(Mta=[], fret=[], c=[], rs=[], rb=[], zc=[], flag=0)
    for i in range(NE):
        zi = float(ZC[i]) if zrule == "own" else 0.0
        Mta, f = supply(sup, float(Mg3[i]), float(MG[i]), fstar)
        if fam == "930":
            c, rs, rb, zc = prof930(Mta, zi, a, b)
        else:
            c, rs, rb, fl = prof932(Mta, zi, a, b); zc = np.nan; meta["flag"] += int(fl)
        out[i] = cold_profile(Mta, c, rs, rb)
        for k, v in (("Mta", Mta), ("fret", f), ("c", c), ("rs", rs), ("rb", rb), ("zc", zc)): meta[k].append(v)
    meta = {k: (np.asarray(v, float) if isinstance(v, list) else v) for k, v in meta.items()}
    return out, meta


def classify(bd, s_mod):
    tm = abs(bd["MID"][0] - 1) < 2 * bd["MID"][1]; to = abs(bd["OUTER"][0] - 1) < 2 * bd["OUTER"][1]
    ts = abs(S_OBS - s_mod) < 2 * S_ERR
    if tm and to and ts: lab = "EXPLAINS"
    elif tm or to: lab = "PARTIAL"
    else: lab = "FAILS"
    return dict(label=lab, T_MID=bool(tm), T_OUT=bool(to), T_S=bool(ts),
                Z_MID=(bd["MID"][0] - 1) / bd["MID"][1], Z_OUT=(bd["OUTER"][0] - 1) / bd["OUTER"][1], dS_over_err=(s_mod - S_OBS) / S_ERR)


def fmt(bd): return "  ".join(f"{b} {bd[b][0]:.3f}±{bd[b][1]:.3f}" for b in ("INNER", "MID", "OUTER"))


RES = {"lane": "CFG949", "criteria": "7330f9e99", "mode": MODE, "selftest_686": SELFTEST,
       "s_obs": [S_OBS, S_ERR], "settings": dict(kappa=0.5, footings=A0, f_b=FBN, cold_per_b=SUP, rss_limit_gb=RSS_LIMIT_GB)}
P(f"CFG949 [{MODE}]  criteria 7330f9e99  n_eRASS1 {NE}  s_obs {S_OBS:.4f} ± {S_ERR:.4f}  native h {h_:.4f} Om {Om:.4f} Delta_ta(0) {DTA0:.4f}")
guard("setup")

# baseline baryons (CFG687 primary), shared by every stage
GAS = gas_beta(MG, R500)                                                     # kg, N x NR
MB = GAS * 1.20


# ============================================================================ K stage
def run_K():
    K = {}
    # K0 units / tables
    mmed = float(np.median(MG)); r5 = float(np.median(R500))
    nodes = max(abs(dta_of(z) - d) for z, d in zip(ZTA, DTAV))
    ok0 = 5e12 < mmed < 5e13 and 0.3 < r5 < 2.0 and nodes < 1e-12 and abs(D_of_z(0.0) - 1) < 1e-12 and abs(N9["Dz"](0.0) - 1) < 1e-9
    K["K0"] = dict(median_Mgas500=mmed, median_R500=r5, dta_node_maxdiff=nodes, D0=D_of_z(0.0), D0_932=N9["Dz"](0.0), pass_=ok0)
    check("K0 units/tables", ok0, f"median Mgas500 {mmed:.3e} Msun, R500 {r5:.3f} Mpc, Delta_ta nodes {nodes:.1e}, D(0) {D_of_z(0.0):.6f}/{N9['Dz'](0.0):.6f}")
    # K1 CFG687 (nu_mono law, primary cell)
    PL = np.asarray(PC7["PL"], float); PN = np.asarray(PC7["PN"], float)
    rows = []
    for i in range(0, NE, 53):
        cl = dict(Mgas500=MG[i], R500=R500[i]); rows.append(np.max(np.abs(law687(cl, A0["canonical"]) / PL[i] - 1)))
    Lc = dsig_law(MB, A0["canonical"], C4.nu_mono); La = dsig_law(MB, A0["alt"], C4.nu_mono)
    relPL = float(np.max(np.abs(Lc / PL - 1)))
    bc, ba, bn = STE.band(Lc), STE.band(La), STE.band(PN)
    st = R7["A"]; dA = 0.0
    for key, bd in (("canonical|b0.67|rc0.15|f0.20", bc), ("alt|b0.67|rc0.15|f0.20", ba), ("newton", bn)):
        for b in ("MID", "OUTER"): dA = max(dA, abs(bd[b][0] - st[key][b][0]), abs(bd[b][1] - st[key][b][1]))
    s_law = s_model(Lc); s_N = s_model(PN); T2 = R7["T2"]
    dS = max(abs(S_OBS - T2["s_obs"]), abs(S_ERR - T2["s_err"]), abs(s_law - T2["s_law"]), abs(s_N - T2["s_newton"]))
    ok1 = relPL < 1e-9 and dA < 1e-6 and dS < 1e-6 and max(rows) < 1e-9
    K["K1"] = dict(maxrel_PL_engine=relPL, maxrel_law687_sample=float(max(rows)), A_can=bc, A_alt=ba, A_newton_stored_PN=bn, maxdiff_A=dA,
                   s=dict(obs=[S_OBS, S_ERR], law=s_law, newton=s_N), maxdiff_s=dS, pass_=ok1)
    check("K1 CFG687 law/A/T2", ok1, f"PL rel {relPL:.1e}; A can {fmt(bc)}; alt {fmt(ba)}; Newton(stored PN) {fmt(bn)}; maxdiff A {dA:.1e}; "
          f"s obs {S_OBS:.4f}±{S_ERR:.4f} law {s_law:.4f} N {s_N:.4f} (diff {dS:.1e})")
    # K2 CFG916/922 nu_s; K2b CFG686 ACCEPT (nu_mono) bootstrap replay
    d2 = 0.0; k2 = {}
    for foot in FEET:
        bd = STE.band(dsig_law(MB, A0[foot], nu_s)); ref = K922["K3"][foot]["eRASS1_MID"]
        d2 = max(d2, abs(bd["MID"][0] - ref[0]), abs(bd["MID"][1] - ref[1])); k2[foot] = bd
    ok2 = d2 < 1e-4
    K["K2"] = dict(eRASS1_nu_s=k2, maxdiff=d2, pass_=ok2)
    check("K2 CFG916/922 nu_s (frozen)", ok2, f"nu_s MID can {k2['canonical']['MID'][0]:.4f}±{k2['canonical']['MID'][1]:.4f} alt "
          f"{k2['alt']['MID'][0]:.4f}±{k2['alt']['MID'][1]:.4f} (diff {d2:.1e})")
    # K2b (extra, not frozen; split out after RUN1, see README): CFG686 ACCEPT law A_MID with CFG686's per-key bootstrap replay (CFG922 K2 recipe)
    AC = R6["clusters"]; ACD = np.nan_to_num(np.array([c["dsig"] for c in AC])); ACE = np.array([c["err"] for c in AC], float)
    STA = Stack(ACD, ACE, np.array([c["ra"] for c in AC]), "boot"); NA = len(AC)
    GA = np.array([gas_accept(c["key"], c["z"])[0] for c in AC])
    keys = list(AC[0]["pred"].keys()) + ["newton"]; rb_ = np.random.default_rng(1); draws = {k: [rb_.integers(0, NA, NA) for _ in range(1000)] for k in keys}
    d2b = 0.0; k2b = {}
    for foot in FEET:
        kk = f"{foot}|b+0.0|f0.20"; Pe = dsig_law(GA * 1.2, A0[foot], C4.nu_mono)
        Am = STA.A(Pe)["MID"]; sg = float(np.nanstd([STA.A(Pe, s)["MID"] for s in draws[kk]])); st6 = R6["A"][kk]["MID"]
        d2b = max(d2b, abs(Am - st6[0]), abs(sg - st6[1])); k2b[foot] = (Am, sg)
    ok2b = d2b < 1e-6
    K["K2b"] = dict(ACCEPT_mono=k2b, maxdiff=d2b, pass_=ok2b)
    check("K2b CFG686 ACCEPT law (extra)", ok2b, f"MID can {k2b['canonical'][0]:.4f}±{k2b['canonical'][1]:.4f} alt {k2b['alt'][0]:.4f}±{k2b['alt'][1]:.4f} (diff {d2b:.1e})")
    guard("K2")
    # K3 CFG932 cluster-core: this lane's R932 profile code at z = 0, CFG932's own supply and f_b
    S = N9["systems"](); cl = [s for s in S if s["name"] == "cluster-core"][0]
    Mta, fr = N9["supply"](cl["Mb_tot"], 1); FB9 = N9["FB"]; d3 = 0.0; x3 = {}
    for foot, fk in (("canonical", "can"), ("alt", "alt")):
        a0k = N9["a0k"](N9["FOOT"][fk]); Mph, dMph = N9["phantom"](cl, a0k)
        for cn, rule, F in (("PS1", "PS1", None), ("EPS0.2", "EPS", 0.2), ("EPS0.05", "EPS", 0.05), ("EPS0.01", "EPS", 0.01)):
            st_ = R932["grid"][f"{fk}|{cn}|L1"]["cluster-core"]
            c, rs, rb, fl = prof932(Mta, 0.0, rule, F)
            mc = float(N9["mfun"](c)); ro = cl["r_obs"]
            Mp = lambda r, c=c, rs=rs, rb=rb, mc=mc: (1 - FB9) * Mta * N9["mfun"](np.minimum(r, rb) / rs) / mc
            dMp = lambda r, c=c, rs=rs, rb=rb, mc=mc: np.where(r < rb, (1 - FB9) * Mta * (r / rs) / (1 + r / rs) ** 2 / (rs * mc), 0.0)
            Mmax = N9["simpson_ln"](lambda r: np.maximum(dMph(r), dMp(r)), ro * 1e-10, ro)
            Mbro = float(cl["Mb"](np.array(ro))); Mphro = float(Mph(np.array(ro))); Mpro = float(Mp(np.array(ro)))
            X = math.log10((Mbro + Mmax) / (Mbro + Mphro)); XB0 = math.log10((Mbro + Mpro) / (Mbro + Mphro))
            rel = max(abs(Mta / st_["M_ta"] - 1), abs(c / st_["c_ta"] - 1), abs(rb / st_["r_ta_kpc"] - 1), abs(rs / st_["r_s_kpc"] - 1),
                      abs(Mpro / st_["Mp_robs"] - 1)); dx = abs(X - st_["X_ret_dex"])
            d3 = max(d3, rel, dx); x3[f"{foot}|{cn}"] = dict(c=c, rb_kpc=rb, rs_kpc=rs, Mp_robs=Mpro, X_ret=X, X_ret_stored=st_["X_ret_dex"],
                                                             B0_core_excess_dex=XB0, rel=rel, dX=dx)
    ok3 = d3 < 1e-6
    K["K3"] = dict(M_ta=Mta, f_ret=fr, rows=x3, maxdiff=d3, pass_=ok3)
    check("K3 CFG932 cluster-core (R932 code, z=0)", ok3, "; ".join(f"{k} c {v['c']:.3f} X {v['X_ret']:+.3f} (B0 {v['B0_core_excess_dex']:+.3f})" for k, v in x3.items())
          + f"; maxdiff {d3:.1e}")
    # K4 CFG930 median cluster: this lane's R930 code at z = 0
    MGM = float(np.median(MG)); k4 = {}; d4 = 0.0
    for key, C, bnd in (("NB|C3000|rta|x1", 3000.0, "rta"), ("NB|C6000|rvir|x1", 6000.0, "rvir")):
        pt = R930["corners"][key]["canonical"]["cluster"]["corners"]["1.2|noAGN|med"]
        f, Mta4 = mta_fixed(1.2 * MGM); c, rs, rb, zc = prof930(Mta4, 0.0, C, bnd)
        Mc = cold_profile(Mta4, c, rs, rb)[None, :]
        m2 = float(proj_cyl(Mc, 0.5)[0]) / MSUN; ref = pt["M2D"] / (1 - pt["fs"])
        rel = max(abs(Mta4 / pt["Mta"] - 1), abs(m2 / ref - 1)); d4 = max(d4, rel)
        k4[key] = dict(Mta=Mta4, Mta_stored=pt["Mta"], c=c, rs_kpc=rs, rb_kpc=rb, zc=zc, m2_cyl05=m2, m2_stored=ref, rel=rel)
    # K4b: CFG687 Newton column, record projection vs truncation-aware projection
    PNr = dsig_law(MB, 0.0, C4.nu_mono)                                      # a0 = 0 -> CFG922 exact (record) fallback
    relPN = float(np.max(np.abs(PNr / np.asarray(PC7["PN"], float) - 1)))
    PNt = dsig_newton(MB); bnt = STE.band(PNt); bnr = STE.band(PNr)
    flag = {b: abs(bnt[b][0] / bnr[b][0] - 1) for b in ("MID", "OUTER")}
    ok4 = d4 < 1e-3 and relPN < 1e-9
    K["K4"] = dict(rows=k4, maxrel=d4, K4b=dict(maxrel_PN_record=relPN, A_newton_record=bnr, A_newton_truncation_aware=bnt,
                                                  frac_diff=flag, flagged=bool(max(flag.values()) > 0.05)), pass_=ok4)
    check("K4 CFG930 median cluster (R930 code, z=0) + K4b record PN", ok4,
          "; ".join(f"{k}: Mta {v['Mta']:.4e} (st {v['Mta_stored']:.4e}) c {v['c']:.2f} m2 {v['m2_cyl05']:.4e} (st {v['m2_stored']:.4e}) rel {v['rel']:.1e}" for k, v in k4.items())
          + f"; PN record rel {relPN:.1e}")
    P(f"   K4b Newton baryons-only: record projection {fmt(bnr)} | truncation-aware {fmt(bnt)} | frac diff MID {flag['MID']:.3f} OUTER {flag['OUTER']:.3f}"
      + ("  ** FLAGGED (>5%) **" if max(flag.values()) > 0.05 else ""))
    # K5 projection vs analytic NFW (Wright & Brainerd 2000) and vs scipy quad for a truncated NFW
    rs5, c5, M5 = 0.4, 5.0, 1e15
    rhos = M5 / (4 * math.pi * rs5 ** 3 * float(m_(c5)))                     # Msun/Mpc^3
    Mun = 4 * math.pi * rhos * rs5 ** 3 * m_(R / rs5) * MSUN
    def wb(Rr):
        x = Rr / rs5
        if x < 1:
            a = math.atanh(math.sqrt((1 - x) / (1 + x))); f = (1 - 2 / math.sqrt(1 - x * x) * a) / (x * x - 1); h = 2 / math.sqrt(1 - x * x) * a + math.log(x / 2)
        else:
            a = math.atan(math.sqrt((x - 1) / (x + 1))); f = (1 - 2 / math.sqrt(x * x - 1) * a) / (x * x - 1); h = 2 / math.sqrt(x * x - 1) * a + math.log(x / 2)
        return (4 * rhos * rs5 * h / (x * x) - 2 * rhos * rs5 * f) / 1e12     # Msun/pc^2
    got = dsig_newton(Mun[None, :])[0]; exp_ = np.array([wb(Rr) for Rr in RC]); e5a = float(np.max(np.abs(got / exp_ - 1)))
    rb5 = 5.0; Mtr = 4 * math.pi * rhos * rs5 ** 3 * m_(np.minimum(R, rb5) / rs5) * MSUN
    rho5 = lambda r: rhos / ((r / rs5) * (1 + r / rs5) ** 2)
    def q_ds(Rr):
        um = math.acosh(rb5 / Rr)
        Sig = 2 * quad(lambda u: rho5(Rr * math.cosh(u)) * Rr * math.cosh(u), 0, um, limit=400, epsabs=0, epsrel=1e-10)[0]
        shell = quad(lambda u: 4 * math.pi * (Rr * math.cosh(u)) ** 2 * rho5(Rr * math.cosh(u)) * (1 - math.tanh(u)) * Rr * math.sinh(u), 0, um, limit=400, epsabs=0, epsrel=1e-10)[0]
        Mcyl = 4 * math.pi * rhos * rs5 ** 3 * float(m_(Rr / rs5)) + shell
        return (Mcyl / (math.pi * Rr ** 2) - Sig) / 1e12
    got_t = dsig_newton(Mtr[None, :])[0]; exp_t = np.array([q_ds(Rr) for Rr in RC]); e5b = float(np.max(np.abs(got_t / exp_t - 1)))
    rec_t = dsig_law(Mtr[None, :], 0.0, C4.nu_mono)[0]; e5c = float(np.max(np.abs(rec_t / exp_t - 1)))
    ok5 = e5a < 0.01 and e5b < 0.005
    K["K5"] = dict(untruncated_vs_WB=dict(got=got.tolist(), exact=exp_.tolist(), maxrel=e5a),
                   truncated_vs_quad=dict(got=got_t.tolist(), exact=exp_t.tolist(), maxrel=e5b),
                   record_projection_truncated_vs_quad=dict(got=rec_t.tolist(), maxrel=e5c), pass_=ok5)
    check("K5 projection vs analytic/quad NFW", ok5, f"untruncated vs WB00 max rel {e5a:.2e}; truncated (5 Mpc) vs quad {e5b:.2e}; "
          f"[record clamped projection on the truncated NFW: {e5c:.2e}]")
    return K


# ============================================================================ MUTATE stage
def b0_primary(gas=GAS, fstar=0.20, prof=PRIMARY[0], sup=PRIMARY[1], zrule="own"):
    Mb = gas * (1 + fstar); Mc, meta = build_cold(prof, sup, gas, fstar, zrule)
    return dsig_newton(Mb), dsig_newton(Mc), Mc, meta


def run_MUTATE():
    M = {}
    Pb, Pc, Mc, meta = b0_primary(); Pb0 = Pb + Pc; bd0 = STE.band(Pb0); s0 = s_model(Pb0)
    P(f"B0 primary (reference for the arms): {fmt(bd0)}; s {s0:.3f}")
    # MT tethered limit
    Lc = dsig_law(MB, A0["canonical"], C4.nu_mono); La = dsig_law(MB, A0["alt"], C4.nu_mono)
    bc, ba = STE.band(Lc), STE.band(La); st = R7["A"]
    d = max(abs(bc[b][0] - st["canonical|b0.67|rc0.15|f0.20"][b][0]) for b in ("MID", "OUTER"))
    d = max(d, max(abs(ba[b][0] - st["alt|b0.67|rc0.15|f0.20"][b][0]) for b in ("MID", "OUTER")))
    one = STE.band(Lc, D=Lc); d1 = max(abs(one[b][0] - 1) for b in ("MID", "OUTER"))
    moved = abs(bc["MID"][0] - bd0["MID"][0]) > 0.05 or abs(bc["OUTER"][0] - bd0["OUTER"][0]) > 0.05
    okT = d < 1e-6 and d1 < 1e-12 and moved
    M["MT"] = dict(A_can=bc, A_alt=ba, maxdiff_vs_stored=d, A_mock_law=one, maxdev_one=d1, moved_from_B0=moved, pass_=okT)
    check("MT tethered limit = the law", okT, f"can {fmt(bc)} | alt {fmt(ba)} | stored diff {d:.1e} | mock-law A-1 {d1:.1e} | moved from B0 {moved}")
    # M0 cold x 0
    PNr = dsig_law(MB, 0.0, C4.nu_mono); bnr = STE.band(PNr); bnt = STE.band(Pb)
    dn = abs(bnr["OUTER"][0] - st["newton"]["OUTER"][0])
    ok0 = dn < 1e-6 and bnt["OUTER"][0] > 3
    M["M0"] = dict(A_record=bnr, A_truncation_aware=bnt, diff_stored=dn, pass_=ok0)
    check("M0 cold x 0 (baryons-only Newton)", ok0, f"record {fmt(bnr)} (stored OUTER {st['newton']['OUTER'][0]:.3f}) | truncation-aware {fmt(bnt)}")
    # MI injection
    Dm = Pb + 1.5 * Pc
    def lam_mock(Dd):
        j = BANDS["OUTER"]; W = STE.W
        return float(((W[:, j] * Dd[:, j]).sum() - (W[:, j] * Pb[:, j]).sum()) / (W[:, j] * Pc[:, j]).sum())
    l0 = lam_mock(Dm); rng = np.random.default_rng(949); En = np.where(np.isfinite(E7) & (E7 < 1e8), E7, 0.0)
    l1 = lam_mock(Dm + rng.normal(0, 1, Dm.shape) * En)
    bdm = STE.band(Pb0, D=Dm)
    okI = abs(l0 / 1.5 - 1) < 0.01 and abs(l1 / 1.5 - 1) < 0.25
    M["MI"] = dict(lam_noiseless=l0, lam_noisy=l1, A_of_mock_vs_unscaled_model=bdm, pass_=okI)
    check("MI injection x1.5", okI, f"lambda_OUT noiseless {l0:.5f}, noisy {l1:.3f}; mock A vs unscaled model {fmt(bdm)}")
    # MS shuffle
    perm = np.random.default_rng(949).permutation(NE); s_sh = s_model(Pb + Pc[perm])
    okS = abs(s_sh - s0) > 0.1
    M["MS"] = dict(s_B0=s0, s_shuffled=s_sh, pass_=okS)
    check("MS shuffle of cold masses moves s", okS, f"s B0 {s0:.3f} -> shuffled {s_sh:.3f}")
    return M


# ============================================================================ MAIN stage
def run_MAIN():
    out = {}
    # ---- B0 primary
    Pb, Pc, Mc, meta = b0_primary(); P0 = Pb + Pc
    bd = STE.band(P0); s0 = s_model(P0); cls = classify(bd, s0)
    lm, lo = lam_band(Pb, Pc, "MID"), lam_band(Pb, Pc, "OUTER")
    terc = {}
    for t in range(3):
        sel = TID == t; terc[t] = dict(Mgas_med=float(np.median(MG[sel])), B0=band_sel(P0, sel))
    med = {k: float(np.nanmedian(v)) for k, v in meta.items() if isinstance(v, np.ndarray)}
    med["Mta_over_Mret"] = float(np.median(meta["Mta"] / (1.2 * GAS[:, -1] / MSUN)))
    out["B0_primary"] = dict(A=bd, s=s0, cls=cls, lam_MID=lm, lam_OUT=lo, shape_ratio=bd["MID"][0] / bd["OUTER"][0],
                             terciles=terc, medians=med, flags932=meta["flag"])
    P("\n=== B0 (H-UT as posed: no law boost, footing-independent), primary corner S-cen x R930 C3000 r_ta, z_i ===")
    P(f"A: {fmt(bd)} | MID/OUTER {bd['MID'][0] / bd['OUTER'][0]:.3f} (law 1.888/1.893) | s_HUT {s0:.3f} vs s_obs {S_OBS:.3f}±{S_ERR:.3f} (law 0.466, Newton 0.836)")
    P(f"class: {cls['label']}  (T-MID {cls['T_MID']} Z {cls['Z_MID']:+.2f}; T-OUT {cls['T_OUT']} Z {cls['Z_OUT']:+.2f}; T-S {cls['T_S']} {cls['dS_over_err']:+.2f} s_err)")
    P(f"lambda (cold multiplier for A = 1): MID {lm:.3f}, OUTER {lo:.3f}")
    P("medians: " + ", ".join(f"{k} {v:.4g}" for k, v in med.items()))
    for t, v in terc.items():
        P(f"  tercile {t} (Mgas500 med {v['Mgas_med']:.3e}): {fmt(v['B0'])}")
    guard("B0 primary")
    # ---- robustness: 40 B0 corners (z_i), cold arrays cached per corner for B1/B2
    corners = {}; labels = []
    PL = {(k, f): dsig_law(MB, A0[f], KERN[k]) for k in KERN for f in FEET}
    PHrb = {}
    Mstar = GAS * 0.20; PG = dsig_newton(GAS); PSL = {(k, f): dsig_law(Mstar, A0[f], KERN[k]) for k in KERN for f in FEET}
    LAWB = {(k, f): law_split(MB, A0[f], KERN[k])[1] for k in KERN for f in FEET}
    LAWS = {(k, f): law_split(Mstar, A0[f], KERN[k])[1] for k in KERN for f in FEET}
    for prof in [p[0] for p in PROFILES]:
        for sup in SUPPLIES:
            if (prof, sup) == PRIMARY:
                Pc_, meta_ = Pc, meta
            else:
                Mc_, meta_ = build_cold(prof, sup, GAS, 0.20); Pc_ = dsig_newton(Mc_)
            Pm = Pb + Pc_; b = STE.band(Pm); s = s_model(Pm); c = classify(b, s); labels.append(c["label"])
            row = dict(A=b, s=s, cls=c, lam_MID=lam_band(Pb, Pc_, "MID"), lam_OUT=lam_band(Pb, Pc_, "OUTER"),
                       med_c=float(np.median(meta_["c"])), med_rs_kpc=float(np.median(meta_["rs"])), med_rb_kpc=float(np.median(meta_["rb"])),
                       med_Mta=float(np.median(meta_["Mta"])), med_fret=float(np.median(meta_["fret"])), flags932=int(meta_["flag"]))
            # B1 / B2 readings at this corner (remainder fraction scales the same NFW shape)
            Mcold = (1 - FBN) * meta_["Mta"]; rb_m = meta_["rb"] / 1e3
            for k in KERN:
                for f in FEET:
                    if k == "mono" and (prof, sup) != PRIMARY: continue
                    ph_b = np.array([np.interp(rb_m[i], R, LAWB[(k, f)][i]) for i in range(NE)]) / MSUN
                    ph_s = np.array([np.interp(rb_m[i], R, LAWS[(k, f)][i]) for i in range(NE)]) / MSUN
                    fr1 = np.clip((Mcold - ph_b) / Mcold, 0, None); fr2 = np.clip((Mcold - ph_s) / Mcold, 0, None)
                    P1 = PL[(k, f)] + fr1[:, None] * Pc_; P2 = PG + PSL[(k, f)] + fr2[:, None] * Pc_
                    b1, b2 = STE.band(P1), STE.band(P2); s1, s2 = s_model(P1), s_model(P2)
                    row[f"B1|{k}|{f}"] = dict(A=b1, s=s1, cls=classify(b1, s1), med_free_frac=float(np.median(fr1)))
                    row[f"B2|{k}|{f}"] = dict(A=b2, s=s2, cls=classify(b2, s2), med_free_frac=float(np.median(fr2)))
            corners[f"{prof}|{sup}"] = row
            P(f"  B0 {prof:11s} {sup:8s}: {fmt(b)} s {s:.3f} -> {c['label']:8s} | lam MID {row['lam_MID']:.2f} OUT {row['lam_OUT']:.2f} | "
              f"c {row['med_c']:.1f} r_s {row['med_rs_kpc']:.0f} kpc | B1(s,can) {row['B1|s|canonical']['cls']['label']} "
              f"MID {row['B1|s|canonical']['A']['MID'][0]:.2f} OUT {row['B1|s|canonical']['A']['OUTER'][0]:.2f} free {row['B1|s|canonical']['med_free_frac']:.2f} | "
              f"B2(s,can) {row['B2|s|canonical']['cls']['label']} MID {row['B2|s|canonical']['A']['MID'][0]:.2f} OUT {row['B2|s|canonical']['A']['OUTER'][0]:.2f}")
            guard(f"corner {prof} {sup}")
    counts = {l: labels.count(l) for l in set(labels)}
    rob = "ROBUST" if counts.get(cls["label"], 0) == len(labels) else "FRAGILE"
    out["corners"] = corners; out["B0_counts"] = counts; out["robustness"] = rob
    P(f"\nB0 40-corner counts: {counts} -> {rob} (primary class {cls['label']})")
    # B1/B2 classes at the primary corner, per footing and kernel
    pr = corners[f"{PRIMARY[0]}|{PRIMARY[1]}"]; rb12 = {}
    for rd in ("B1", "B2"):
        for k in KERN:
            for f in FEET:
                x = pr[f"{rd}|{k}|{f}"]; rb12[f"{rd}|{k}|{f}"] = x["cls"]["label"]
                P(f"  {rd} [{k}, {f}] primary corner: {fmt(x['A'])} s {x['s']:.3f} free frac {x['med_free_frac']:.3f} -> {x['cls']['label']}")
        for f in FEET:
            labs = [corners[c][f"{rd}|s|{f}"]["cls"]["label"] for c in corners]
            rb12[f"{rd}|s|{f}|40corners"] = {l: labs.count(l) for l in set(labs)}
            P(f"  {rd} [s, {f}] 40-corner counts: {rb12[f'{rd}|s|{f}|40corners']}")
    out["B1_B2_primary_and_counts"] = rb12
    # ---- one-at-a-time variants (B0, primary corner)
    var = {}
    for vn, kw in (("z_i->0 (CFG930 rule verbatim)", dict(zrule="zero")), ("beta 0.6", dict(beta=0.6)), ("beta 0.8", dict(beta=0.8)),
                   ("r_c 0.10 R500", dict(rcf=0.10)), ("r_c 0.20 R500", dict(rcf=0.20)), ("f* 0.10", dict(fstar=0.10)), ("f* 0.30", dict(fstar=0.30))):
        gas = gas_beta(MG, R500, beta=kw.get("beta", 2 / 3), rcf=kw.get("rcf", 0.15)) if ("beta" in kw or "rcf" in kw) else GAS
        Pb_, Pc_, _, _ = b0_primary(gas=gas, fstar=kw.get("fstar", 0.20), zrule=kw.get("zrule", "own"))
        Pm = Pb_ + Pc_; b = STE.band(Pm); s = s_model(Pm); c = classify(b, s)
        var[vn] = dict(A=b, s=s, cls=c, lam_MID=lam_band(Pb_, Pc_, "MID"), lam_OUT=lam_band(Pb_, Pc_, "OUTER"))
        P(f"  variant {vn:30s}: {fmt(b)} s {s:.3f} -> {c['label']} | lam MID {var[vn]['lam_MID']:.2f} OUT {var[vn]['lam_OUT']:.2f}")
        guard(f"variant {vn}")
    vl = [v["cls"]["label"] for v in var.values()]; out["variants"] = var; out["variant_counts"] = {l: vl.count(l) for l in set(vl)}
    # ---- diagnostics: projected excess inside 0.5 Mpc vs CFG922's needed extra; ACCEPT 8; galaxy side
    MLc = law_split(MB, A0["canonical"], nu_s)[0]; MLa = law_split(MB, A0["alt"], nu_s)[0]
    cyl_b0 = (proj_cyl(MB, 0.5) + proj_cyl(Mc, 0.5)) / MSUN
    ex = {f: float(np.median(cyl_b0 - proj_cyl(ML_, 0.5) / MSUN)) for f, ML_ in (("canonical", MLc), ("alt", MLa))}
    need = {f: RES922[f"eRASS1|s|{f}"]["needed_masses"]["U"]["needed"] for f in FEET}
    out["core_cyl05"] = dict(B0_minus_law_median=ex, CFG922_needed=need, B0_cold_cyl_median=float(np.median(proj_cyl(Mc, 0.5) / MSUN)))
    P(f"\ncore (R < 0.5 Mpc cylinder): B0 - law (nu_s) median {ex['canonical']:.3e} / {ex['alt']:.3e} Msun vs CFG922 needed extra "
      f"{need['canonical']:.3e} / {need['alt']:.3e}")
    AC = R6["clusters"]; ACD = np.nan_to_num(np.array([c["dsig"] for c in AC])); ACE = np.array([c["err"] for c in AC], float)
    STA = Stack(ACD, ACE, np.array([c["ra"] for c in AC]), "boot")
    GA = np.array([gas_accept(c["key"], c["z"])[0] for c in AC]); MBA = GA * 1.2
    McA = np.empty_like(MBA); mA = []
    for i, c in enumerate(AC):
        Mta, f = supply("S-cen", GA[i, -1] / MSUN, np.nan, 0.20); cc, rs, rb, zc = prof930(Mta, float(c["z"]), 3000.0, "rta")
        McA[i] = cold_profile(Mta, cc, rs, rb); mA.append(dict(name=c["name"], z=c["z"], Mta=Mta, c=cc, rs_kpc=rs))
    bA = STA.band(dsig_newton(MBA) + dsig_newton(McA)); bAL = {f: STA.band(dsig_law(MBA, A0[f], nu_s)) for f in FEET}
    out["ACCEPT8"] = dict(B0=bA, law_nu_s=bAL, halos=mA)
    P(f"ACCEPT 8 (no class weight): B0 {fmt(bA)} | law nu_s can {fmt(bAL['canonical'])}")
    i0 = int(np.argsort(MG)[NE // 2]); rs, rb, cc = meta["rs"][i0], meta["rb"][i0], meta["c"][i0]
    Mta0 = meta["Mta"][i0]; rhos = (1 - FBN) * Mta0 / (4 * math.pi * rs ** 3 * float(m_(cc)))   # Msun/kpc^3
    gal = {}
    for Rk in (250.0, 500.0, 1000.0):
        rho = rhos / ((Rk / rs) * (1 + Rk / rs) ** 2)
        gal[f"{Rk:.0f}kpc"] = dict(rho_Msun_kpc3=rho, **{f"Mu_over_Mb_r{rr:.0f}": (4 * math.pi / 3 * rho * rr ** 3) / (5e10 * rr ** 2 / (rr + 3.0) ** 2)
                                                         for rr in (10.0, 30.0, 100.0)})
    out["galaxy_side"] = dict(cluster_index=i0, Mgas500=float(MG[i0]), z=float(ZC[i0]), c=cc, rs_kpc=rs, rb_kpc=rb, Mta=Mta0, rows=gal)
    P(f"galaxy side (median cluster, Mgas500 {MG[i0]:.2e}, c {cc:.1f}, r_s {rs:.0f} kpc): " + "; ".join(
        f"R {k}: rho {v['rho_Msun_kpc3']:.2e} Msun/kpc^3, Mu/Mb(<10,30,100 kpc) {v['Mu_over_Mb_r10']:.3f}/{v['Mu_over_Mb_r30']:.3f}/{v['Mu_over_Mb_r100']:.3f}" for k, v in gal.items()))
    # ---- CFG932's cluster: B0 analogue of X_ret (from the K stage numbers, recomputed here for the record)
    S = N9["systems"](); cl = [s for s in S if s["name"] == "cluster-core"][0]; Mta9, _ = N9["supply"](cl["Mb_tot"], 1); x9 = {}
    for fk in ("can", "alt"):
        Mph, _ = N9["phantom"](cl, N9["a0k"](N9["FOOT"][fk])); ro = cl["r_obs"]
        for cn, rule, F in (("PS1", "PS1", None), ("EPS0.2", "EPS", 0.2), ("EPS0.05", "EPS", 0.05), ("EPS0.01", "EPS", 0.01)):
            c9, rs9, rb9, _ = prof932(Mta9, 0.0, rule, F); Mp = (1 - N9["FB"]) * Mta9 * float(N9["mfun"](min(ro, rb9) / rs9)) / float(N9["mfun"](c9))
            Mb9 = float(cl["Mb"](np.array(ro))); x9[f"{fk}|{cn}"] = math.log10((Mb9 + Mp) / (Mb9 + float(Mph(np.array(ro)))))
    out["CFG932_cluster_B0_excess_dex"] = x9
    P("CFG932 cluster-core, B0 3D excess over the law at 500 kpc: " + ", ".join(f"{k} {v:+.3f}" for k, v in x9.items()))
    # ---- class per footing (B0 has no a0: same number on both)
    out["class"] = {f: dict(B0=cls["label"], robustness=rob, B1_nu_s=rb12[f"B1|s|{f}"], B2_nu_s=rb12[f"B2|s|{f}"]) for f in FEET}
    P(f"\nCLASS (H-UT = B0, footing-independent): {cls['label']} on both footings, {rob} ({counts}); "
      f"B1 nu_s {rb12['B1|s|canonical']} / {rb12['B1|s|alt']}; B2 nu_s {rb12['B2|s|canonical']} / {rb12['B2|s|alt']}")
    return out


def jsonable(x):
    if isinstance(x, dict): return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [jsonable(v) for v in x]
    if isinstance(x, np.ndarray): return jsonable(x.tolist())
    if isinstance(x, (np.floating,)): return float(x)
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.bool_,)): return bool(x)
    return x


if MODE == "K":
    RES["K"] = run_K()
elif MODE == "MUTATE":
    RES["MUTATE"] = run_MUTATE()
else:
    RES["main"] = run_MAIN()
RES["checks"] = CHECKS; RES["all_checks_pass"] = all(c["ok"] for c in CHECKS)
RES["peak_rss_gb"] = rss_gb(); RES["runtime_s"] = time.time() - T0
P(f"\nchecks: {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} pass; peak RSS {RES['peak_rss_gb']:.3f} GB; runtime {RES['runtime_s']:.0f} s")
P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.")
json.dump(jsonable(RES), open(os.path.join(HERE, "cfg949_results" + TAG + ".json"), "w"), indent=1)
OUTF.close()
if _m932 is not None:
    os.environ["CFG932_MUTATE"] = _m932
sys.exit(0 if RES["all_checks_pass"] else 1)
