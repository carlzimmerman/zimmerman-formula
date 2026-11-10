#!/usr/bin/env python3
"""RB2 (criteria 3d752864ef): form B on the hosted rows (Coma UDGs, MW and M31 dwarf spheroidals, DF2/DF4).

    python3 rb2.py            -> rb2.json / rb2.out             (known answers KA1-KA6, then the grading)
    python3 rb2.py --mutate   -> rb2_MUTATE.json / rb2_MUTATE.out (M1 external field back on; M2 masses scrambled)

Form B: the isolated a0 law's phantom of each dwarf's own baryons is real mass; no external field; tides cut it at the
Jacobi radius r_J, g_iso(r_J)/r_J = k G M_host(<d)/d^3.  Inside r_J, g_B = nu(g_N/a0) g_N; outside, g_B = g_N + G M_ph(<r_J)/r^2.

Code paths COPIED (not imported) from: X1 (rebuild_2026_10_22/X1_hosted_recount/x1_hosted_recount.py: LVD loader, MC build,
classes, pred_draws), S1 (rebuild_2026_10_22/S1_v3_hosted_small/s1_v3_hosted_small.py: Coma TSV, constants, beta model,
estimator), SE2 (closure_2026_11_06/SE2_step_as_systematics/se2.py: udg_admiss, se_conv, post_udg, summ, seeds),
XF1 (closure_2026_11_08/XF1_moving_host_field/xf1_grade.py: boot_median), U1 (rebuild_2026_10_22/U1_v3_dust_content/
u1_v3_dust_content.py: DF2/DF4 inputs and geometry).  D10's solver is used through a verbatim copy in this folder
(rb2_d10_copy.py).  Committed tables and JSON of those lanes are read as data.
kappa = 1/2 FITTED; not theory closed; footings never pooled; no particle.  Relabels nothing."""
import os, sys, json, math, csv, time, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.dirname(HERE); REPO = os.path.dirname(CL)
sys.path.insert(0, HERE)
import rb2_d10_copy as S   # noqa: E402  (verbatim copy of D10's solver, in this folder)

MUT = "--mutate" in sys.argv
TAG = "rb2_MUTATE" if MUT else "rb2"
T0 = time.time(); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
LN10 = math.log(10.0)
CHK = {}
def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"{name} {'PASS' if ok else 'FAIL'}  {msg}")
def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)

# =============================================================================== X1 (copied verbatim, constants and loaders)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
LFLOOR = {"canonical": 21.68, "alt": 22.85}
NMC, NBOOT = 2000, 4000
DY, DL = 0.6, 0.3
FW_N = 2.0 * (4 / 3) ** 3 / (1 + (4 / 3) ** 2) ** 1.5
R12 = 4.0 / 3.0
UPS_PRIOR = 0.15
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
X1D = os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount")
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None
def load_lvd():
    rows = []
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            s = fl(r.get("vlos_sigma"))
            rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
            ms = fl(r.get("mass_stellar")); mv = fl(r.get("M_V"))
            if not s or s <= 0 or not rh or rh <= 0:
                continue
            if ms is None and mv is not None:
                ms = 0.4 * (4.83 - mv) + 0.301
            if ms is None:
                continue
            rhe = fl(r.get("rhalf_sph_physical_em")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_em"))
            rhp = fl(r.get("rhalf_sph_physical_ep")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_ep"))
            rows.append(dict(name=r["name"], host=host, sigma=s, sem=fl(r.get("vlos_sigma_em")) or 0.1 * s,
                             sep=fl(r.get("vlos_sigma_ep")) or 0.1 * s, ul=bool(r.get("vlos_sigma_ul")),
                             rh=rh, rhem=rhe or 0.1 * rh, rhep=rhp or 0.1 * rh, logms=ms,
                             dmem=fl(r.get("distance_modulus_em")) or 0.1, dmep=fl(r.get("distance_modulus_ep")) or 0.1,
                             dhost=fl(r.get("distance_host")), dist=fl(r.get("distance")),
                             mv=mv, dm31=fl(r.get("distance_m31")),
                             # RB2 additions (not used by X1's build): raw kinematics for the orbit edge
                             _raw=r))
    return rows
ALL = load_lvd()
ARR = list(csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
arr_f07 = {r["lvd_name"]: float(r["sig_f07"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values()))); med_f07 = float(np.median(list(arr_f07.values())))
GEH = {}
for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha_vs_lvd_match.csv"))):
    if r.get("geha_sigma_resolved") == "1" and fl(r.get("geha_sigma")):
        GEH[r["lvd_name"]] = (float(r["geha_sigma"]), fl(r.get("geha_e_sigma_ll")) or 0.1, fl(r.get("geha_e_sigma_ul")) or 0.1)
def split_normal(rng, c, em, ep, n):
    z = rng.standard_normal(n); return c + np.where(z < 0, z * em, z * ep)
def build(rows, a0, rng, ups=2.0, binmode="free", sig_src="lvd", drop_ul=False, mvrule=False):
    keep = [r for r in rows if not (drop_ul and r["ul"])]
    N = len(keep)
    lb = np.empty((N, NMC)); ly = np.empty((N, NMC)); la = np.empty((N, NMC)); Md = np.empty((N, NMC)); Ms_ = np.empty((N, NMC))
    for i, r in enumerate(keep):
        s, sem, sep = r["sigma"], r["sem"], r["sep"]
        if sig_src == "lower" and r["name"] in GEH:
            gs, gl_, gu = GEH[r["name"]]
            if gs < s: s, sem, sep = gs, gl_, gu
        b = 1.0
        ufd = (r["mv"] is not None and r["mv"] > -7.7)
        if binmode == "free": b = arr_free.get(r["name"], med_free if (ufd or not mvrule) else 1.0)
        elif binmode == "f07": b = arr_f07.get(r["name"], med_f07 if (ufd or not mvrule) else 1.0)
        fD = 10 ** (split_normal(rng, 0.0, r["dmem"], r["dmep"], NMC) / 5.0)
        sig = np.abs(split_normal(rng, s, sem, sep, NMC)) * b
        rh = np.abs(split_normal(rng, r["rh"], r["rhem"], r["rhep"], NMC)) * fD
        ms = ups / 2.0 * 10 ** r["logms"] * fD ** 2
        r12 = R12 * rh * PC
        gobs = 3.0 * (sig * 1e3) ** 2 / r12; gbar = G * (ms / 2) * MSUN / r12 ** 2
        lb[i] = np.log10(gobs / gbar); Md[i] = gobs * r12 ** 2 / G / MSUN; Ms_[i] = ms
        ly[i] = np.log10(G * ms * MSUN / ((rh * PC) ** 2 * a0)); la[i] = np.log10(rh)
    return dict(lb=lb, ly=ly, la=la, Md=Md, Ms=Ms_, rows=keep)
def lin3(x, xs, v):
    x = np.asarray(x, float)
    s0 = (v[1] - v[0]) / (xs[1] - xs[0]); s1 = (v[2] - v[1]) / (xs[2] - xs[1])
    return np.where(x < xs[1], v[1] + s0 * (x - xs[1]), v[1] + s1 * (x - xs[1]))
def interp2(ly, lL, ys, Ls, T):
    rows = [lin3(lL, Ls, T[i]) for i in range(3)]
    s0 = (rows[1] - rows[0]) / (ys[1] - ys[0]); s1 = (rows[2] - rows[1]) / (ys[2] - ys[1])
    return np.where(ly < ys[1], rows[1] + s0 * (ly - ys[1]), rows[1] + s1 * (ly - ys[1]))
def pred_draws_one(t, X, i, key, est, Lst=None):
    """X1's pred_draws for one system (copied; loop body)."""
    if key in ("iso0", "emb0"):
        return lin3(X["ly"][i], t["ys"], np.asarray(t[key])[:, est])
    lab = key.split("_", 1)[1]
    lL = math.log10(Lst) - X["la"][i]
    return interp2(X["ly"][i], lL, t["ys"], t[f"Ls_{lab}"], np.asarray(t[key])[:, :, est])
def Rh_X1(r):
    if r["host"] == "field":
        return r["dist"] * KPC
    if r["dhost"]:
        return r["dhost"] * KPC
    if r["host"] == "M31" and r["dm31"]:
        return r["dm31"] * KPC
    return r["dist"] * KPC
CLASSICAL = {"Carina", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans", "Ursa Minor"}
INDIV = ["Crater II", "Antlia II", "Canes Venatici I", "Sagittarius"]
EXCL = {"LMC", "SMC", "M 32"}
DES = {"NGC 147", "NGC 185", "NGC 205"}
def klass(r):
    n = r["name"]
    if n in EXCL: return None
    if r["host"] == "MW":
        if n in CLASSICAL: return "MW classical"
        if n in INDIV: return "indiv:" + n
        if r["mv"] is not None and r["mv"] > -7.7: return "MW ultra-faint"
        return "MW other"
    if r["host"] == "M31":
        if n in DES: return "M31 dE"
        return "bright M31" if r["logms"] >= 5.0 else "M31 others"
    return "LG field"
SMP = [r for r in ALL if klass(r) is not None]
X1CSV = list(csv.DictReader(open(os.path.join(X1D, "x1_per_system.csv"))))
X1TAB = {f: json.load(open(os.path.join(X1D, f"x1_stage_tables_{f}.json")))["tables"] for f in FOOTS}

# =============================================================================== XF1's boot_median (copied)
def boot_median(vals, sds, nb=4000, seed=11):
    rng = np.random.default_rng(seed); vals = np.asarray(vals); sds = np.asarray(sds); n = len(vals); meds = np.empty(nb)
    for b in range(nb):
        ix = rng.integers(0, n, n); meds[b] = np.median(vals[ix] + rng.normal(0, 1, n) * sds[ix])
    q = np.percentile(meds, [2.5, 50, 97.5])
    return dict(median=float(q[1]), ci95=[float(q[0]), float(q[2])], contains0=bool(q[0] <= 0 <= q[2]), n=int(n))
XF1J = json.load(open(os.path.join(CL, "..", "closure_2026_11_08", "XF1_moving_host_field", "xf1.json")))

# =============================================================================== form B: the law, the cut, the estimators
def gl(gN):
    """isolated law, a0 units: g = nu(gN) gN with nu(y) = 1/2 + sqrt(1/4 + 1/y)."""
    gN = np.asarray(gN, float); return 0.5 * gN + np.sqrt(0.25 * gN * gN + gN)
def gNp(r, y):
    return y * r / (1.0 + r * r) ** 1.5
def solve_rJ(hfun, K, lo=-12.0, hi=12.0, it=90):
    """largest r with hfun(r) = K for a decreasing hfun (vectorised bisection in log10 r); K <= 0 -> inf."""
    K = np.asarray(K, float); lo = np.full(K.shape, lo); hi = np.full(K.shape, hi)
    for _ in range(it):
        mid = 0.5 * (lo + hi); above = hfun(10 ** mid) > K
        lo = np.where(above, mid, lo); hi = np.where(above, hi, mid)
    return np.where(K > 0, 10 ** (0.5 * (lo + hi)), np.inf)
def rJ_iso(y, K):
    y = np.asarray(y, float); K = np.broadcast_to(np.asarray(K, float), y.shape)
    return solve_rJ(lambda r: gl(gNp(r, y)) / r, K)
def gB(r, y, rJ):
    """B's radial field at r (a = 1, a0 = 1): isolated law inside r_J, baryons + the phantom kept inside r_J outside it."""
    y = np.asarray(y, float); rJ = np.broadcast_to(np.asarray(rJ, float), y.shape)
    gi = gl(gNp(r, y))
    fin = np.isfinite(rJ); rJs = np.where(fin, rJ, 1.0)
    gt = gNp(r, y) + (gl(gNp(rJs, y)) - gNp(rJs, y)) * rJs ** 2 / r ** 2
    return np.where(fin & (rJs < r), gt, gi)
RV = np.geomspace(1e-5, 1e5, 24000); RHO = (3 / (4 * np.pi)) * (1 + RV * RV) ** -2.5
def vir_B(y, rJ):
    """global virial sigma^2 (Plummer tracer, a = 1, a0 = 1) for B's field: int rho r g dV / 3."""
    g = gB(RV, np.full(RV.shape, float(y)), np.full(RV.shape, float(rJ)))
    return float(np.trapz(RHO * RV * g * 4 * np.pi * RV * RV, RV) / 3.0)

# =============================================================================== known-answer helpers
KA = {}
def ka5():
    out = {}
    y = np.geomspace(1e-6, 1e3, 50)
    out["a_rJ_inf_is_iso"] = float(np.max(np.abs(gB(R12, y, np.inf) - gl(gNp(R12, y)))))
    out["b_rJ_0_is_newton"] = float(np.max(np.abs(np.log10(gB(R12, y, 1e-30) / gNp(R12, y)))))
    out["c_newton_EW_ratio_vs_FW_N"] = float(np.max(np.abs(gNp(R12, y) / (y / (2 * R12 ** 2)) - FW_N)))
    yd = 1e-9; out["d_deep_virial_rel"] = abs(vir_B(yd, np.inf) / ((2.0 / 9.0) * math.sqrt(yd)) - 1)
    m, Mh, d = 3.0e7, 1.0e12, 80.0     # point-mass Newtonian satellite: h = m / r^3 ; K = 3 Mh / d^3
    rj = float(solve_rJ(lambda r: m / r ** 3, np.array(3 * Mh / d ** 3)))
    out["e_point_mass_rel"] = abs(rj / (d * (m / (3 * Mh)) ** (1 / 3)) - 1)
    rs, gs, st = S.iso_1d(1e-2, 1e-3)
    out["f_iso1d_L0_rel"] = abs(float(np.interp(math.log(R12), np.log(rs), gs)) / float(gl(gNp(R12, 1e-2))) - 1)
    ok = (out["a_rJ_inf_is_iso"] == 0.0 and out["b_rJ_0_is_newton"] < 1e-12 and out["c_newton_EW_ratio_vs_FW_N"] < 1e-12
          and out["d_deep_virial_rel"] < 1e-3 and out["e_point_mass_rel"] < 1e-8 and out["f_iso1d_L0_rel"] < 1e-3)
    return ok, out

# =============================================================================== Coma (S1 copied: data, constants, beta model)
G_, MSUN_, PC_ = 6.674e-11, 1.989e30, 3.0857e16
KPC_C = 3.0857e19
KEV, MP = 1.602176634e-16, 1.67262e-27
BETA = dict(kT=8.6, rc=276.0, beta=0.71, mu=0.6)
CB = 3 * BETA["beta"] * BETA["kT"] * KEV / (BETA["mu"] * MP)
def g_beta(d_kpc):
    r = d_kpc * KPC_C; rc = BETA["rc"] * KPC_C
    return CB * r / (r * r + rc * rc)
_rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "freundlich2022_coma_udgs.tsv"), encoding="utf-8")
         if l.strip() and not l.startswith("#")]
_hd = {h: i for i, h in enumerate(_rows[0])}
COMA = []
for r in _rows[1:]:
    g_ = lambda k: float(r[_hd[k]])
    Ms = g_("L_1e8") * 1e8 * g_("ML"); Re = g_("Re_kpc")
    adm = (Re >= 1.5) and (3e7 <= Ms <= 3e8)
    COMA.append(dict(name=r[_hd["name"]], Ms=Ms, Re=Re, sig=g_("sig"), esig=g_("esig"), dproj=g_("d_kpc"), dmean=g_("dmean_kpc"), admit=adm))
ADM = [c for c in COMA if c["admit"]]
S1D = os.path.join(REPO, "rebuild_2026_10_22", "S1_v3_hosted_small")
UROWS = list(csv.DictReader(open(os.path.join(S1D, "s1_coma_per_galaxy.csv"))))
R1 = json.load(open(os.path.join(S1D, "s1_v3_hosted_small_results.json")))["coma"]
GR2 = None; SOLVE_CACHE = {}
def s1_solve(y, xe, Lam):
    """S1's solve() (copied): D10 Solver2D on S1's grid, monopole field, Jeans -> (wo, vir)."""
    global GR2
    key = (float(y), float(xe), float(Lam))
    if key in SOLVE_CACHE: return SOLVE_CACHE[key]
    if GR2 is None: GR2 = S.Grid2D(nper=24, Nt=16)
    iso = xe <= 0
    sv = S.Solver2D(GR2, y, 0.0 if iso else xe, Lam, isolated=iso)
    U, res, it = sv.solve(tol=1e-10)
    rf, gr = sv.field_monopole()
    _, vir, wo = S.jeans(rf, gr, [])
    SOLVE_CACHE[key] = (wo, vir, res)
    return wo, vir, res
def coma_kfac(d_kpc, edge):
    if edge == "weak": return 2 * d_kpc ** 2 / (d_kpc ** 2 + BETA["rc"] ** 2)
    return 3.0
def coma_E(c, a0, edge="prim", est=0, mfac=1.0, dfac=1.0, sfac=1.0, field="B", Lst=0.0):
    """E = 2 ln(sigma_obs / sigma_pred) (S1's estimator) under B (field 'B') or the static external field (field 'EFE')."""
    Ms = c["Ms"] * mfac * dfac ** 2; Re = c["Re"] * dfac; a = Re * 1e3 * PC_
    y = G_ * Ms * MSUN_ / (a * a * a0)
    pos = "dproj" if edge == "strong" else "dmean"
    dk = c[pos] * dfac
    rJ = np.inf
    if field == "EFE":
        xe = g_beta(dk) / a0
        wo, vir, res = s1_solve(y, xe, Lst * PC_ / a if Lst else 0.0)
        s2 = (wo, vir)[est]
    else:
        if edge != "iso":
            K = coma_kfac(dk, edge) * g_beta(dk) / (dk * KPC_C) * a / a0
            rJ = float(rJ_iso(np.array([y]), np.array([K]))[0])
        s2 = float(R12 * gB(R12, np.array([y]), rJ)[0] / 3.0) if est == 0 else vir_B(y, rJ)
    sp = math.sqrt(s2 * a0 * a) / 1e3
    so = c["sig"] * sfac; e = c["esig"] * sfac
    return 2 * math.log(so / sp), 2 * e / so, rJ / R12, y
def coma_sk(a0, edge="prim", field="B", Lst=0.0):
    """S1's / SE2's knob recipe applied to the given prediction (means over the 9 admitted, ln units)."""
    mv = lambda smp=ADM, **kw: float(np.mean([coma_E(c, a0, **kw)[0] for c in smp]))
    base = mv(edge=edge, field=field, Lst=Lst)
    sk = dict(s_M=abs(mv(edge=edge, field=field, Lst=Lst, mfac=10 ** 0.2) - mv(edge=edge, field=field, Lst=Lst, mfac=10 ** -0.2)) / 2,
              s_A=abs(mv(edge=edge, field=field, Lst=Lst, sfac=1.15) - mv(edge=edge, field=field, Lst=Lst, sfac=1 / 1.15)) / 2,
              s_D=abs(mv(edge=edge, field=field, Lst=Lst, dfac=1.05) - mv(edge=edge, field=field, Lst=Lst, dfac=0.95)) / 2,
              s_aniso=abs(mv(edge=edge, field=field, Lst=Lst, est=1) - base),
              s_mem=abs(mv(COMA, edge=edge, field=field, Lst=Lst) - base),
              s_pos=abs(mv(edge="strong", field=field, Lst=Lst) - base))
    return sk, base
# SE2 copied: admissibility, se_conv, post_udg (seeds), summ
NDRAW = 20000
def udg_admiss(r, a0, scale=1.0):
    Re = float(r["Re_kpc"]) * KPC_C; sg = float(r["sigma"]) * 1e3; d = float(r["d_mean_kpc"]) * KPC_C; g = float(r["x_e_dmean"]) * a0
    tau = Re / (d * (4 * sg ** 2 * Re / (3 * g * d * d)) ** (1 / 3)); V = math.sqrt(g * d); tc = (4 / 3) * Re / sg; to = 2 * math.pi * d / V
    return dict(A1=bool(tau * scale < 0.375), A2=bool(tc <= 0.1 * to), tau=tau, tc_to=tc / to)
def se_conv(E, sE):
    n = len(E); return max(float(np.std(E, ddof=1) / math.sqrt(n)), float(math.sqrt(np.sum(np.asarray(sE) ** 2)) / n))
def rngs_coma(f):
    b = 110 * 10 + (0 if f == "canonical" else 1); return np.random.default_rng(b), np.random.default_rng(b + 500000)
def post_udg(rows, sk, f, udgw, nominal=False):
    rs, rn = rngs_coma(f); R = [r for r in rows if r["_adm"]["A1"] and r["_adm"]["A2"]]
    n = len(R)
    E = np.array([float(r["E_v3_dmean"]) for r in R]); sE = np.array([float(r["sE"]) for r in R]); mE = float(E.mean()); se = se_conv(E, sE)
    shift = np.zeros(NDRAW)
    if not nominal:
        for k in ("s_M", "s_A", "s_D", "s_aniso", "s_mem", "s_pos"): shift += rn.normal(0, 1, NDRAW) * sk[k] * udgw
    return (mE + shift + rs.normal(0, se, NDRAW)) / LN10, dict(n=n, meanE_ln=mE, se_ln=se)
def summ(x):
    q = np.percentile(x, [2.5, 16, 50, 84, 97.5]); sd = float(np.std(x))
    return dict(median=float(q[2]), ci68=[float(q[1]), float(q[3])], ci95=[float(q[0]), float(q[4])], sd=sd,
                contains0=bool(q[0] <= 0 <= q[4]))
def coma_rows(f, Es):
    rows = []
    for r in UROWS:
        if r["footing"] != f: continue
        r2 = dict(r); r2["_adm"] = udg_admiss(r, A0[f])
        if Es is not None: r2["E_v3_dmean"] = Es[r["name"]]
        rows.append(r2)
    return rows
def record_sk(f):
    base = R1[f"{f}|S4 v3 dmean L*floor E-W"]
    return dict(s_M=base["s_M"], s_A=base["s_A"], s_D=base["s_D"],
                s_aniso=abs(R1[f"{f}|v3 dmean L*floor E-V"]["meanE"] - base["meanE"]),
                s_mem=abs(R1[f"{f}|v3 all 11 Coma dmean L*floor"]["meanE"] - base["meanE"]),
                s_pos=abs(R1[f"{f}|S4 v3 dproj L*floor E-W"]["meanE"] - base["meanE"]))
def coma_post(f, Es, sk):
    rows = coma_rows(f, Es); o = {}
    for kind, w in (("main", 1.0), ("half", 0.5)):
        x, info = post_udg(rows, sk, f, w); xn, _ = post_udg(rows, sk, f, w, nominal=True)
        o[kind] = dict(post=summ(x), raw_stat_only=summ(xn), n=info["n"], meanE_dex=info["meanE_ln"] / LN10, se_dex=info["se_ln"] / LN10)
    return o

# =============================================================================== U1 DF2/DF4 (copied inputs and geometry)
G_U, MSUN_U, KPC_U = 6.674e-11, 1.989e30, 3.0857e19
DFG = {"DF2": dict(Ms=2.0e8, Re=2.0, D=20.0, obs=(8.5, 2.3, 3.1), pos=(40.4451, -8.4028)),
       "DF4": dict(Ms=1.5e8, Re=1.6, D=20.0, obs=(6.3, 2.5, 1.6), pos=(39.8128, -8.1160))}
HOSTS = {"NGC1052": (40.2700, -8.2558), "NGC1035": (39.8713, -8.1328)}
MH_1052 = 1e11
U1J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "U1_v3_dust_content", "u1_v3_dust_content_results.json")))
def df_geom(nm):
    gg_ = DFG[nm]; p, q = gg_["pos"], HOSTS["NGC1052"]
    ra1, d1, ra2, d2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    cc = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(ra1 - ra2)
    return gg_["D"] * 1000 * math.acos(min(1.0, cc)) * KPC_U       # projected distance to NGC 1052 (m)
def df_E(nm, a0, mode, Mh_fac=1.0):
    """mode 'N' (U1's B0, Newton), 'iso' (B uncut), 'B' (B cut at r_J, k = 3, host = law mass of Mh_fac x 1e11 at d_proj)."""
    gg_ = DFG[nm]
    r12 = R12 * gg_["Re"] * KPC_U; aP = r12 / 1.30477; rev = 1.30477
    yv = G_U * gg_["Ms"] * MSUN_U / (aP ** 2 * a0)
    rJ = np.inf
    if mode == "N":
        g = float(gNp(rev, yv))
    else:
        if mode == "B":
            d = df_geom(nm); gh = float(gl(G_U * MH_1052 * Mh_fac * MSUN_U / d ** 2 / a0))   # host law field, a0 units
            K = 3.0 * gh / d * aP
            rJ = float(rJ_iso(np.array([yv]), np.array([K]))[0])
        g = float(gB(rev, np.array([yv]), rJ)[0])
    sp = math.sqrt(r12 * g * a0 / 3) / 1e3
    so, up, lo = gg_["obs"]; e = lo if so > sp else up
    return 2 * math.log(so / sp), 2 * e / so, sp, rJ / rev

# =============================================================================== edges: orbits (MW) and projected distances (M31)
VC = {"MW": 200.0, "M31": 230.0}
M31_RADEC = (10.6847, 41.2690)
def sky_angle(ra1, de1, ra2, de2):
    ra1, de1, ra2, de2 = map(math.radians, (ra1, de1, ra2, de2))
    c = math.sin(de1) * math.sin(de2) + math.cos(de1) * math.cos(de2) * math.cos(ra1 - ra2)
    return math.acos(max(-1.0, min(1.0, c)))
def m31_distance():
    cands = []
    for r in SMP:
        if r["host"] != "M31" or not r["dm31"] or not r["dist"]: continue
        R = r["_raw"]; th = sky_angle(float(R["ra"]), float(R["dec"]), *M31_RADEC)
        D, dm = r["dist"], r["dm31"]; disc = dm * dm - (D * math.sin(th)) ** 2
        if disc < 0: continue
        cands.append((D * math.cos(th) - math.sqrt(disc), D * math.cos(th) + math.sqrt(disc)))
    grid = np.arange(600.0, 1000.0, 0.1)
    cost = [sum(min(abs(a - g), abs(b - g)) for a, b in cands) for g in grid]
    return float(grid[int(np.argmin(cost))]), len(cands)
def mw_pericentres(nmc=500, seed=20261109):
    """pericentre (kpc) in the flat V_c = 200 km/s log potential from LVD kinematics; astropy's default Galactocentric frame."""
    import astropy.units as u
    from astropy.coordinates import SkyCoord, Galactocentric
    rng = np.random.default_rng(seed); out = {}
    Vc = VC["MW"]
    for r in SMP:
        if r["host"] != "MW": continue
        R = r["_raw"]; v = {k: fl(R.get(k)) for k in ("ra", "dec", "distance_modulus", "pmra", "pmdec", "vlos_systemic")}
        if any(v[k] is None for k in v):
            out[r["name"]] = None; continue
        e = lambda k: 0.5 * ((fl(R.get(k + "_em")) or 0.0) + (fl(R.get(k + "_ep")) or 0.0))
        dm = split_normal(rng, v["distance_modulus"], fl(R.get("distance_modulus_em")) or 0.0, fl(R.get("distance_modulus_ep")) or 0.0, nmc)
        D = 10 ** ((dm + 5) / 5) / 1e3
        pmra = v["pmra"] + rng.normal(0, 1, nmc) * e("pmra"); pmdec = v["pmdec"] + rng.normal(0, 1, nmc) * e("pmdec")
        vl = v["vlos_systemic"] + rng.normal(0, 1, nmc) * e("vlos_systemic")
        D = np.concatenate([[10 ** ((v["distance_modulus"] + 5) / 5) / 1e3], D]); pmra = np.concatenate([[v["pmra"]], pmra])
        pmdec = np.concatenate([[v["pmdec"]], pmdec]); vl = np.concatenate([[v["vlos_systemic"]], vl])
        c = SkyCoord(ra=np.full(D.shape, v["ra"]) * u.deg, dec=np.full(D.shape, v["dec"]) * u.deg, distance=D * u.kpc,
                     pm_ra_cosdec=pmra * u.mas / u.yr, pm_dec=pmdec * u.mas / u.yr, radial_velocity=vl * u.km / u.s, frame="icrs")
        gc = c.transform_to(Galactocentric())
        x = np.vstack([gc.x.to_value(u.kpc), gc.y.to_value(u.kpc), gc.z.to_value(u.kpc)]).T
        w = np.vstack([gc.v_x.to_value(u.km / u.s), gc.v_y.to_value(u.km / u.s), gc.v_z.to_value(u.km / u.s)]).T
        rn = np.linalg.norm(x, axis=1); L = np.linalg.norm(np.cross(x, w), axis=1); E = 0.5 * np.sum(w * w, axis=1) + Vc ** 2 * np.log(rn)
        f = lambda rr: Vc ** 2 * np.log(rr) + L ** 2 / (2 * rr * rr) - E
        lo = np.full(rn.shape, 1e-3); hi = np.minimum(rn, np.maximum(L / Vc, 1e-3))
        for _ in range(80):
            mid = np.sqrt(lo * hi); pos = f(mid) > 0
            lo = np.where(pos, mid, lo); hi = np.where(pos, hi, mid)
        peri = np.sqrt(lo * hi); peri = np.where(f(np.full(rn.shape, 1e-3)) <= 0, 1e-3, peri)
        out[r["name"]] = dict(central=float(peri[0]), r_now_gc=float(rn[0]), p16=float(np.percentile(peri[1:], 16)),
                              p50=float(np.percentile(peri[1:], 50)), p84=float(np.percentile(peri[1:], 84)))
    return out

# =============================================================================== dSph readings
def K_dsph(k, d_m, a_m, Vc_kms, a0):
    return k * (Vc_kms * 1e3) ** 2 / d_m ** 2 * a_m / a0
def dsph_reading(X, i, r, f, reading, EDGE):
    """per-draw Delta under a reading: 'iso', 'prim', 'weak', 'strong'."""
    a0 = A0[f]; y = 10 ** X["ly"][i]; a_m = 10 ** X["la"][i] * PC
    rJ = np.full(y.shape, np.inf)
    if r["host"] in VC and reading != "iso":
        d = Rh_X1(r); Vc = VC[r["host"]]
        if reading in ("prim", "strong"): rJ = rJ_iso(y, K_dsph(3.0, d, a_m, Vc, a0))
        if reading == "weak": rJ = rJ_iso(y, K_dsph(2.0, d, a_m, Vc, a0))
        if reading == "strong":
            e = EDGE[r["name"]]; cand = rJ / 3 ** (2 / 3)
            if e.get("d_strong_kpc") is not None:
                cand2 = rJ_iso(y, K_dsph(3.0, e["d_strong_kpc"] * KPC, a_m, Vc, a0))
                cand = np.minimum(cand2, rJ) if e["kind"] == "orbit" else np.minimum(cand, cand2)
            rJ = cand
    pred = np.log10(gB(R12, y, rJ) / (y / (2 * R12 ** 2)))
    return X["lb"][i] - pred, rJ / R12

# =============================================================================== main
RES = dict(lane="RB2", tag=TAG, criteria="3d752864ef", note="TEST lane: relabels nothing; kappa = 1/2 FITTED; not theory closed",
           footings={}, KA={}, MUTATE={})
P(f"RB2 form B on the hosted rows {'MUTATE' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# --- X1's build, same seed and call order (the W builds consume the stream and are discarded)
RNG = np.random.default_rng(20261031); DS = {}
for f in FOOTS:
    DS[f] = build(SMP, A0[f], RNG, mvrule=True)
    build(SMP, A0[f], RNG, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True, mvrule=True)
CLS = {r["name"]: klass(r) for r in SMP}
X1ROW = {(r["footing"], r["name"]): r for r in X1CSV}

# --- edges
M31D, nM31 = m31_distance()
PERI = mw_pericentres()
EDGE = {}
for r in SMP:
    e = dict(kind=None, d_strong_kpc=None)
    if r["host"] == "MW":
        p = PERI.get(r["name"])
        if p is not None: e = dict(kind="orbit", d_strong_kpc=p["p16"], peri=p)
        else: e = dict(kind="SE2 r_J/3^(2/3)", d_strong_kpc=None)
    elif r["host"] == "M31":
        R = r["_raw"]; th = sky_angle(float(R["ra"]), float(R["dec"]), *M31_RADEC)
        e = dict(kind="projected or SE2 r_J/3^(2/3)", d_strong_kpc=M31D * math.sin(th))
    EDGE[r["name"]] = e
P(f"edges: M31 distance from {nM31} LVD rows (consensus root) {M31D:.1f} kpc; MW orbits from LVD kinematics: "
  f"{sum(1 for v in PERI.values() if v)} of {len(PERI)} MW rows")

def per_system(f, reading_fn):
    """per-system medians and sds (X1's convention) for every row of the sample."""
    X = DS[f]; o = {}
    for i, r in enumerate(X["rows"]):
        v = reading_fn(X, i, r)
        o[r["name"]] = (float(np.median(v)), float(np.std(v)))
    return o

GRADED = ("MW classical", "MW ultra-faint", "bright M31")
REPORTED = ("M31 others",)
def class_stat(per, cls):
    names = [r["name"] for r in DS["canonical"]["rows"] if CLS[r["name"]] == cls]
    return boot_median([per[n][0] for n in names], [per[n][1] for n in names])
def label(st):
    lo, hi = st["ci95"]
    if lo <= 0 <= hi: return "B CONSISTENT"
    return "B FAILS HIGH" if lo > 0 else "B FAILS LOW"

if not MUT:
    # ================================================================ KNOWN ANSWERS
    P("\n=== KNOWN ANSWERS ===")
    # KA1: X1 per-system reproduced
    dmax = {"Newton": 0.0, "iso AQUAL L*0": 0.0, "v3 L*floor": 0.0}; nrow = 0
    for f in FOOTS:
        X = DS[f]; TB = X1TAB[f]
        for i, r in enumerate(X["rows"]):
            xr = X1ROW[(f, r["name"])]; nrow += 1
            vals = {"Newton": X["lb"][i] - math.log10(FW_N),
                    "iso AQUAL L*0": X["lb"][i] - pred_draws_one(TB[r["name"]], X, i, "iso0", 0),
                    "v3 L*floor": X["lb"][i] - pred_draws_one(TB[r["name"]], X, i, "emb_floor", 0, LFLOOR[f])}
            for k, v in vals.items():
                dmax[k] = max(dmax[k], abs(float(np.median(v)) - float(xr[f"Delta[{k}]"])), abs(float(np.std(v)) - float(xr[f"sdMC[{k}]"])))
    KA["KA1"] = dict(rows=nrow, max_abs=dmax)
    check("KA1", nrow == len(X1CSV) and max(dmax.values()) <= 1e-9,
          f"X1 per-system Delta and sdMC reproduced over {nrow} rows (copied loader/build, seed 20261031): max |d| Newton {dmax['Newton']:.1e}, "
          f"iso {dmax['iso AQUAL L*0']:.1e}, v3 floor {dmax['v3 L*floor']:.1e} (line 1e-9)")
    # KA2: XF1's C2 numbers
    k2 = []
    for f in FOOTS:
        eps = XF1J["footings"][f]["C2"]["MW classical"]["eps_used"]
        for cls in ("MW classical", "bright M31"):
            rr = [r for r in X1CSV if r["footing"] == f and r["cls"] == cls]
            rec = boot_median([float(r["Delta[v3 L*floor]"]) for r in rr], [float(r["sdMC[v3 L*floor]"]) for r in rr])
            mov = boot_median([float(r["Delta[Newton]"]) - math.log10(1 + eps) for r in rr], [float(r["sdMC[Newton]"]) for r in rr])
            ref = XF1J["footings"][f]["C2"][cls]
            k2.append((f, cls, rec["median"], ref["record"]["median"], mov["median"], ref["regraded"]["median"]))
    d2 = max(max(abs(a - b), abs(c - d)) for _, _, a, b, c, d in k2)
    KA["KA2"] = dict(rows=k2, max_abs=d2)
    check("KA2", d2 <= 1e-9, "XF1 C2 from X1's CSV: " + "; ".join(f"{f[:3]} {c} static {a:+.3f} moving {c2:+.3f}" for f, c, a, _, c2, _ in k2)
          + f"; max |d| vs xf1.json {d2:.1e} (line 1e-9)")
    # KA3: SE2 / XF1 Coma posteriors
    k3 = []
    for f in FOOTS:
        ref = XF1J["footings"][f]["C2"]["Coma_UDGs"]
        rec = coma_post(f, None, record_sk(f))
        mov = coma_post(f, {r["name"]: float(r["E_v3_dmean"]) + ref["shifts_ln"][r["name"]] for r in UROWS if r["footing"] == f}, record_sk(f))
        k3.append((f, rec["main"]["post"]["median"], ref["record"]["main"]["post"]["median"], rec["half"]["post"]["median"],
                   ref["record"]["half"]["post"]["median"], mov["half"]["post"]["median"], ref["regraded"]["half"]["post"]["median"]))
    d3 = max(max(abs(a - b), abs(c - d), abs(e - g)) for _, a, b, c, d, e, g in k3)
    KA["KA3"] = dict(rows=k3, max_abs=d3)
    check("KA3", d3 <= 1e-9, "Coma (SE2 post_udg copied): " + "; ".join(f"{f[:3]} main {a:+.3f} half {c:+.3f} moving {e:+.3f}" for f, a, _, c, _, e, _ in k3)
          + f"; max |d| vs xf1.json {d3:.1e} (line 1e-9)")
    # KA4: B's analytic law against the record's solver
    d4 = 0.0; k4c = {}
    for f in FOOTS:
        X = DS[f]; a0 = A0[f]
        for i, r in enumerate(X["rows"]):
            y = 10 ** X["ly"][i]
            v = X["lb"][i] - np.log10(gl(gNp(R12, y)) / (y / (2 * R12 ** 2)))
            d4 = max(d4, abs(float(np.median(v)) - float(X1ROW[(f, r["name"])]["Delta[iso AQUAL L*0]"])))
        mE = float(np.mean([coma_E(c, a0, edge="iso")[0] for c in ADM])) / LN10
        k4c[f] = (mE, R1[f"{f}|S2 AQUAL isolated L*0 E-W"]["meanE"] / LN10)
    dc4 = max(abs(a - b) for a, b in k4c.values())
    KA["KA4"] = dict(dsph_max_abs=d4, coma=k4c, coma_max_abs=dc4)
    check("KA4", d4 <= 0.01 and dc4 <= 0.005, f"analytic isolated law vs X1's iso AQUAL L*0 per-system medians: max |d| {d4:.4f} dex (line 0.01); "
          f"Coma mean: " + ", ".join(f"{f[:3]} {a:+.4f} vs S1 {b:+.4f}" for f, (a, b) in k4c.items()) + f" (|d| {dc4:.4f}, line 0.005)")
    # KA5
    ok5, o5 = ka5(); KA["KA5"] = o5
    check("KA5", ok5, "estimator and cut: " + ", ".join(f"{k} {v:.1e}" for k, v in o5.items()))
    # KA6
    d6 = 0.0
    for f in FOOTS:
        ref = U1J["numbers"]["N5"]["tdg"][f]["DF_B0"]
        for j, nm in enumerate(("DF2", "DF4")):
            E, e, sp, _ = df_E(nm, A0[f], "N")
            d6 = max(d6, abs(E - ref["r"][j]), abs(sp - ref["sigma_pred"][j]))
    KA["KA6"] = dict(max_abs=d6)
    check("KA6", d6 <= 1e-6, f"U1 DF2/DF4 Newtonian (B0) r and sigma_pred reproduced: max |d| {d6:.1e} (line 1e-6)")
    KA_OK = all(CHK[k]["ok"] for k in ("KA1", "KA2", "KA3", "KA4", "KA5", "KA6"))
    RES["KA"] = KA; RES["KA_ok"] = KA_OK
    if not KA_OK:
        P("A KNOWN ANSWER FAILED: grading stops (FROZEN section 5).")
    else:
        # ================================================================ GRADING
        for f in FOOTS:
            a0 = A0[f]; FR = dict(classes={}, per_system=[], coma={}, df={}, low_rows=[])
            P(f"\n================ [{f}] a0 {a0:.4e}")
            PER = {rd: per_system(f, lambda X, i, r, rd=rd: dsph_reading(X, i, r, f, rd, EDGE)[0]) for rd in ("iso", "prim", "weak", "strong")}
            # central-value r_J / r12 and k_i; screened reading shift
            X = DS[f]
            for i, r in enumerate(X["rows"]):
                n = r["name"]; y0 = X1TAB[f][n]["y0"]; a_m = r["rh"] * PC
                cen = {}
                for rd in ("prim", "weak", "strong"):
                    Xc = dict(ly=np.array([[math.log10(y0)]] * (i + 1)), la=np.array([[math.log10(r["rh"])]] * (i + 1)), lb=np.zeros((i + 1, 1)))
                    _, rr = dsph_reading(Xc, i, r, f, rd, EDGE); cen[rd] = float(rr[0])
                h = 1e-4
                ki = (math.log10(gl(gNp(R12, y0 * 10 ** h))) - math.log10(gl(gNp(R12, y0 * 10 ** -h)))) / (2 * h)
                # screened isolated (reported): D10 iso_1d at the floor, central values, B's primary cut
                Lam = LFLOOR[f] / r["rh"]; rs, gs, st = S.iso_1d(y0, Lam)
                rJp = cen["prim"] * R12
                def g_scr(rr_): return float(np.exp(np.interp(math.log(rr_), np.log(rs), np.log(gs))))
                if r["host"] in VC:
                    Kc = 3.0 * (VC[r["host"]] * 1e3) ** 2 / Rh_X1(r) ** 2 * a_m / a0
                    hs = gs / rs; idx = np.where(hs > Kc)[0]
                    rJs = float(rs[idx[-1]]) if len(idx) else float(rs[0])
                else:
                    rJs = np.inf
                gBs = g_scr(R12) if not (rJs < R12) else float(gNp(R12, y0) + (g_scr(rJs) - gNp(rJs, y0)) * rJs ** 2 / R12 ** 2)
                gBu = float(gB(R12, np.array([y0]), rJp)[0])
                shift = math.log10(gBs / gBu)
                d_iso, sd_iso = PER["iso"][n]; s_i = math.hypot(sd_iso, UPS_PRIOR * ki)
                row = dict(name=n, cls=CLS[n], host=r["host"], ul=r["ul"], logMstar=r["logms"], rh_pc=r["rh"], r12_pc=R12 * r["rh"],
                           sigma=r["sigma"], d_kpc=Rh_X1(r) / KPC, edge_kind=EDGE[n]["kind"], d_strong_kpc=EDGE[n].get("d_strong_kpc"),
                           peri=EDGE[n].get("peri"), rJ_over_r12={rd: cen[rd] for rd in cen},
                           Delta={rd: PER[rd][n][0] for rd in PER}, sd={rd: PER[rd][n][1] for rd in PER},
                           Delta_screened=PER["prim"][n][0] - shift, screen_shift=shift, iso1d_status=int(st),
                           k_i=ki, s_i=s_i, LOW=bool(d_iso + 2 * s_i < 0))
                if row["LOW"]:
                    s_str = math.hypot(PER["strong"][n][1], UPS_PRIOR * ki)
                    row["reach"] = "TIDES CAN REACH" if PER["strong"][n][0] + 2 * s_str >= 0 else "TIDES CANNOT REACH"
                    row["s_strong"] = s_str
                FR["per_system"].append(row)
            pers = {rd: {n: PER[rd][n] for n in PER[rd]} for rd in PER}
            pers["screened"] = {row["name"]: (row["Delta_screened"], row["sd"]["prim"]) for row in FR["per_system"]}
            eps = XF1J["footings"][f]["C2"]["MW classical"]["eps_used"]
            csvf = {r_["name"]: r_ for r_ in X1CSV if r_["footing"] == f}
            pers["law static (X1 v3 L*floor)"] = {n: (float(csvf[n]["Delta[v3 L*floor]"]), float(csvf[n]["sdMC[v3 L*floor]"])) for n in csvf}
            pers["law moving (XF1, Newton)"] = {n: (float(csvf[n]["Delta[Newton]"]) - math.log10(1 + eps), float(csvf[n]["sdMC[Newton]"])) for n in csvf}
            for cls in GRADED + REPORTED + ("LG field",):
                st = {rd: class_stat(pers[rd], cls) for rd in ("iso", "prim", "weak", "strong", "screened", "law static (X1 v3 L*floor)", "law moving (XF1, Newton)")}
                labs = {rd: label(st[rd]) for rd in st}
                P(f"  {cls:15s} law alone (XF1 statistic): static {st['law static (X1 v3 L*floor)']['median']:+.3f} [{st['law static (X1 v3 L*floor)']['ci95'][0]:+.3f}, "
                  f"{st['law static (X1 v3 L*floor)']['ci95'][1]:+.3f}], moving {st['law moving (XF1, Newton)']['median']:+.3f}")
                FR["classes"][cls] = dict(stats=st, labels=labs, n=st["prim"]["n"], graded=cls in GRADED)
                P(f"  {cls:15s} N {st['prim']['n']:2d}: B prim {st['prim']['median']:+.3f} [{st['prim']['ci95'][0]:+.3f}, {st['prim']['ci95'][1]:+.3f}] {labs['prim']}"
                  f" | iso {st['iso']['median']:+.3f} | weak {st['weak']['median']:+.3f} {labs['weak']} | strong {st['strong']['median']:+.3f} "
                  f"[{st['strong']['ci95'][0]:+.3f}, {st['strong']['ci95'][1]:+.3f}] {labs['strong']} | screened {st['screened']['median']:+.3f} {labs['screened']}")
            # ---------------- Coma UDGs
            Ec = {}; cper = []
            for rd in ("iso", "prim", "weak", "strong"):
                Ec[rd] = {c["name"]: coma_E(c, a0, edge=rd) for c in ADM}
            Escr = {}
            for c in ADM:
                a = c["Re"] * 1e3 * PC_; y = G_ * c["Ms"] * MSUN_ / (a * a * a0); rs, gs, st = S.iso_1d(y, LFLOOR[f] * PC_ / a)
                gsr = float(np.exp(np.interp(math.log(R12), np.log(rs), np.log(gs))))
                rJp = Ec["prim"][c["name"]][2] * R12
                gBu = float(gB(R12, np.array([y]), rJp)[0])
                gBs = gsr if not (rJp < R12) else gBu * gsr / float(gl(gNp(R12, y)))
                Escr[c["name"]] = Ec["prim"][c["name"]][0] + math.log(gBs / gBu) * -1.0
            skB, baseB = coma_sk(a0, "prim")
            skR = record_sk(f)
            cm = {}
            for rd in ("iso", "prim", "weak", "strong"):
                cm[rd] = coma_post(f, {n: v[0] for n, v in Ec[rd].items()}, skB)
            cm["prim_record_sk"] = coma_post(f, {n: v[0] for n, v in Ec["prim"].items()}, skR)
            cm["screened"] = coma_post(f, Escr, skB)
            labsC = {rd: label(cm[rd]["main"]["post"]) for rd in cm}
            for c in ADM:
                n = c["name"]; Ei, sEi = Ec["iso"][n][0], Ec["iso"][n][1]
                row = dict(name=n, Ms=c["Ms"], Re_kpc=c["Re"], sigma=c["sig"], d_mean=c["dmean"], d_proj=c["dproj"],
                           E={rd: Ec[rd][n][0] for rd in Ec}, E_dex={rd: Ec[rd][n][0] / LN10 for rd in Ec}, sE=sEi,
                           rJ_over_r12={rd: Ec[rd][n][2] for rd in ("prim", "weak", "strong")}, LOW=bool(Ei + 2 * sEi < 0))
                if row["LOW"]:
                    row["reach"] = "TIDES CAN REACH" if Ec["strong"][n][0] + 2 * sEi >= 0 else "TIDES CANNOT REACH"
                cper.append(row)
            FR["coma"] = dict(post=cm, labels=labsC, sk_B=skB, sk_record=skR, per_galaxy=cper, meanE_dex_prim=baseB / LN10)
            P(f"  Coma UDGs       N  {cm['prim']['main']['n']}: B prim main {cm['prim']['main']['post']['median']:+.3f} "
              f"[{cm['prim']['main']['post']['ci95'][0]:+.3f}, {cm['prim']['main']['post']['ci95'][1]:+.3f}] {labsC['prim']} | half "
              f"{cm['prim']['half']['post']['median']:+.3f} [{cm['prim']['half']['post']['ci95'][0]:+.3f}, {cm['prim']['half']['post']['ci95'][1]:+.3f}]"
              f" | record s_k {cm['prim_record_sk']['main']['post']['median']:+.3f} [{cm['prim_record_sk']['main']['post']['ci95'][0]:+.3f}, "
              f"{cm['prim_record_sk']['main']['post']['ci95'][1]:+.3f}] {labsC['prim_record_sk']} | iso {cm['iso']['main']['post']['median']:+.3f} | weak "
              f"{cm['weak']['main']['post']['median']:+.3f} {labsC['weak']} | strong {cm['strong']['main']['post']['median']:+.3f} {labsC['strong']} | screened "
              f"{cm['screened']['main']['post']['median']:+.3f} {labsC['screened']}")
            P(f"     s_k under B (ln): " + ", ".join(f"{k} {v:.4f}" for k, v in skB.items()) + " | record: " + ", ".join(f"{k} {v:.4f}" for k, v in skR.items()))
            # ---------------- DF2 / DF4
            for nm in ("DF2", "DF4"):
                Eiso, eiso, spi, _ = df_E(nm, a0, "iso"); EB, eB, spB, rjr = df_E(nm, a0, "B"); EN, eN, spN, _ = df_E(nm, a0, "N")
                low = Eiso + 2 * eiso < 0
                reach = ("TIDES CAN REACH" if EB + 2 * eB >= 0 else "TIDES CANNOT REACH") if low else None
                # host mass B would need (k = 3, projected distance) for E_B + 2 e = 0
                need = None
                if low and reach == "TIDES CANNOT REACH":
                    if EN + 2 * eN < 0:
                        need = "none: even Newton on the baryons (r_J -> 0) lies above the measured sigma by more than 2 e"
                    else:
                        lo_, hi_ = 0.0, 8.0
                        for _ in range(80):
                            mid = 0.5 * (lo_ + hi_); Em, em, _, _ = df_E(nm, a0, "B", 10 ** mid)
                            if Em + 2 * em >= 0: hi_ = mid
                            else: lo_ = mid
                        d = df_geom(nm); fac = 10 ** hi_
                        Em8, em8, _, _ = df_E(nm, a0, "B", fac)
                        if Em8 + 2 * em8 < 0: fac = float("nan")
                        Mneed = d ** 2 * float(gl(G_U * MH_1052 * fac * MSUN_U / d ** 2 / a0)) * a0 / G_U / MSUN_U
                        Mhave = d ** 2 * float(gl(G_U * MH_1052 * MSUN_U / d ** 2 / a0)) * a0 / G_U / MSUN_U
                        need = dict(baryon_factor=fac, M_host_lt_d_needed=Mneed, M_host_lt_d_B=Mhave, ratio=Mneed / Mhave)
                FR["df"][nm] = dict(E_iso=Eiso, e_iso=eiso, E_B=EB, e_B=eB, E_N=EN, e_N=eN, sigma_pred_iso=spi, sigma_pred_B=spB,
                                    sigma_pred_N=spN, rJ_over_r12=rjr, d_proj_kpc=df_geom(nm) / KPC_U, LOW=bool(low), reach=reach, need=need)
                P(f"  {nm}: E_iso {Eiso / LN10:+.3f} dex (sigma_pred {spi:.2f} km/s), E_B {EB / LN10:+.3f} (sigma_pred {spB:.2f}; r_J/r12 {rjr:.2f}, "
                  f"d_proj {df_geom(nm) / KPC_U:.1f} kpc), Newton {EN / LN10:+.3f} ({spN:.2f}); e {eB / LN10:.3f} dex; LOW {low}; {reach}; need {need}")
            # ---------------- LOW rows
            lows = [dict(kind="dSph", name=r_["name"], cls=r_["cls"], Delta_iso=r_["Delta"]["iso"], s_i=r_["s_i"], Delta_strong=r_["Delta"]["strong"],
                         s_strong=r_.get("s_strong"), rJ_over_r12=r_["rJ_over_r12"], edge_kind=r_["edge_kind"], d_strong_kpc=r_["d_strong_kpc"],
                         ul=r_["ul"], reach=r_["reach"]) for r_ in FR["per_system"] if r_["LOW"]]
            lows += [dict(kind="Coma UDG", name=r_["name"], E_iso_dex=r_["E_dex"]["iso"], reach=r_["reach"]) for r_ in cper if r_["LOW"]]
            lows += [dict(kind="NGC 1052", name=nm, E_iso_dex=FR["df"][nm]["E_iso"] / LN10, E_B_dex=FR["df"][nm]["E_B"] / LN10,
                          e_dex=FR["df"][nm]["e_B"] / LN10, rJ_over_r12=FR["df"][nm]["rJ_over_r12"], reach=FR["df"][nm]["reach"], need=FR["df"][nm]["need"])
                     for nm in FR["df"] if FR["df"][nm]["LOW"]]
            FR["low_rows"] = lows
            P(f"  LOW rows ({len(lows)}): " + "; ".join(f"{l['name']} ({l.get('cls', l['kind'])}) {l['reach']}" for l in lows))
            inside = [(r_["name"], r_["cls"], round(r_["rJ_over_r12"]["prim"], 3)) for r_ in FR["per_system"] if r_["rJ_over_r12"]["prim"] < 1]
            inside += [(r_["name"], "Coma UDG", round(r_["rJ_over_r12"]["prim"], 3)) for r_ in cper if r_["rJ_over_r12"]["prim"] < 1]
            FR["rJ_inside_r12_primary"] = inside
            P(f"  rows with primary r_J inside r_1/2: {inside}")
            RES["footings"][f] = FR
            P(f"  peak RSS {rss_gb():.3f} GB, {time.time() - T0:.0f} s")
        # ================================================================ labels
        P("\n=== LABELS ===")
        CL_LAB = {}
        for f in FOOTS:
            FR = RES["footings"][f]
            CL_LAB[f] = {c: FR["classes"][c]["labels"] for c in GRADED}
            CL_LAB[f]["Coma UDGs"] = {"prim": FR["coma"]["labels"]["prim"], "weak": FR["coma"]["labels"]["weak"],
                                      "strong": FR["coma"]["labels"]["strong"], "screened": FR["coma"]["labels"]["screened"],
                                      "record_sk": FR["coma"]["labels"]["prim_record_sk"]}
        CLASS_LABEL = {}
        for c in ("Coma UDGs",) + GRADED:
            parts = []
            for f in FOOTS:
                L = CL_LAB[f][c]; s = L["prim"]
                if L["weak"] != s or L["strong"] != s: s += f" (bracket-sensitive: weak {L['weak']} / strong {L['strong']})"
                if L["screened"] != L["prim"]: s += f" (screening-sensitive: {L['screened']})"
                parts.append(s)
            CLASS_LABEL[c] = dict(canonical=parts[0], alt=parts[1])
            P(f"  {c:15s} canonical: {parts[0]} | alt: {parts[1]}")
        cannot = {f: [l["name"] for l in RES["footings"][f]["low_rows"] if l["reach"] == "TIDES CANNOT REACH"] for f in FOOTS}
        fail_cls = {f: [c for c in ("Coma UDGs",) + GRADED if CL_LAB[f][c]["prim"] != "B CONSISTENT"] for f in FOOTS}
        both_fail = [c for c in fail_cls["canonical"] if c in fail_cls["alt"]]
        both_cannot = [n for n in cannot["canonical"] if n in cannot["alt"]]
        if both_fail or both_cannot:
            lane = "B FAILS ON THE HOSTED ROWS"
        elif not any(fail_cls.values()) and not any(cannot.values()):
            lane = "B HOLDS ON THE HOSTED ROWS"
        else:
            lane = "SPLIT"
        RES["class_labels"] = CLASS_LABEL; RES["lane_label"] = lane
        RES["against_B"] = dict(classes_failing_both=both_fail, low_rows_cannot_reach_both=both_cannot, per_footing=dict(classes=fail_cls, low=cannot))
        P(f"  LOW rows TIDES CANNOT REACH: canonical {cannot['canonical']} | alt {cannot['alt']}")
        P(f"LANE LABEL: {lane}")
else:
    # ================================================================ MUTATE
    P("\n=== MUTATE ===")
    for f in FOOTS:
        a0 = A0[f]; MU = {}
        X = DS[f]; TB = X1TAB[f]
        # M1 dSphs: external field back on (X1's emb_floor tables), no cut, same per-system and class statistic
        per = {}
        for i, r in enumerate(X["rows"]):
            v = X["lb"][i] - pred_draws_one(TB[r["name"]], X, i, "emb_floor", 0, LFLOOR[f])
            per[r["name"]] = (float(np.median(v)), float(np.std(v)))
        m1 = {}
        for cls in ("MW classical", "bright M31"):
            st = class_stat(per, cls); ref = XF1J["footings"][f]["C2"][cls]["record"]["median"]
            m1[cls] = dict(median=st["median"], ci95=st["ci95"], ref=ref, d=abs(st["median"] - ref))
        # M1 Coma: D10 static solve with the host field (copied solver), S1's estimator; s_k re-derived by the same recipe
        Ee = {c["name"]: coma_E(c, a0, field="EFE", Lst=LFLOOR[f]) for c in ADM}
        dE = max(abs(Ee[r["name"]][0] - float(r["E_v3_dmean"])) for r in UROWS if r["footing"] == f)
        mv = lambda smp=ADM, **kw: float(np.mean([coma_E(c, a0, field="EFE", Lst=LFLOOR[f], **kw)[0] for c in smp]))
        base = mv()
        skE = dict(s_M=abs(mv(mfac=10 ** 0.2) - mv(mfac=10 ** -0.2)) / 2, s_A=abs(mv(sfac=1.15) - mv(sfac=1 / 1.15)) / 2,
                   s_D=abs(mv(dfac=1.05) - mv(dfac=0.95)) / 2, s_aniso=abs(mv(est=1) - base), s_mem=abs(mv(COMA) - base),
                   s_pos=abs(float(np.mean([coma_E(c, a0, edge="strong", field="EFE", Lst=LFLOOR[f])[0] for c in ADM])) - base))
        skR = record_sk(f); dsk = max(abs(skE[k] - skR[k]) for k in skR)
        cm = coma_post(f, {n: v[0] for n, v in Ee.items()}, skE)
        refC = XF1J["footings"][f]["C2"]["Coma_UDGs"]["record"]
        m1["Coma UDGs"] = dict(main=cm["main"]["post"]["median"], half=cm["half"]["post"]["median"], ref_main=refC["main"]["post"]["median"],
                               ref_half=refC["half"]["post"]["median"], dE_per_galaxy=dE, d_sk=dsk, sk=skE,
                               d=max(abs(cm["main"]["post"]["median"] - refC["main"]["post"]["median"]), abs(cm["half"]["post"]["median"] - refC["half"]["post"]["median"])))
        bites1 = all(m1[c]["d"] <= 1e-6 for c in m1)
        MU["M1"] = dict(rows=m1, bites=bites1)
        P(f"[{f}] M1 external field back on: MW classical {m1['MW classical']['median']:+.4f} (record {m1['MW classical']['ref']:+.4f}), bright M31 "
          f"{m1['bright M31']['median']:+.4f} (record {m1['bright M31']['ref']:+.4f}), Coma main {m1['Coma UDGs']['main']:+.4f} (record {m1['Coma UDGs']['ref_main']:+.4f}) "
          f"half {m1['Coma UDGs']['half']:+.4f} (record {m1['Coma UDGs']['ref_half']:+.4f}); per-galaxy |dE| {dE:.1e}, s_k |d| {dsk:.1e} -> "
          f"{'BITES (returns the law-alone shortfall)' if bites1 else 'DOES NOT BITE'}")
        # M2: masses scrambled within each class
        def deltas_B(perm):
            o = {}
            for i, r in enumerate(X["rows"]):
                dl = perm.get(r["name"], 0.0)       # log10 M*_perm - log10 M*_true
                y = 10 ** (X["ly"][i] + dl); a_m = 10 ** X["la"][i] * PC; lbp = X["lb"][i] - dl
                rJ = np.full(y.shape, np.inf)
                if r["host"] in VC:
                    rJ = rJ_iso(y, K_dsph(3.0, Rh_X1(r), a_m, VC[r["host"]], a0))
                v = lbp - np.log10(gB(R12, y, rJ) / (y / (2 * R12 ** 2)))
                o[r["name"]] = float(np.median(v))
            return o
        DCL = ("MW classical", "MW ultra-faint", "bright M31", "M31 others")
        members = {c: [r for r in X["rows"] if CLS[r["name"]] == c] for c in DCL}
        def rms(o):
            res = {}; allr = []
            for c in DCL:
                v = np.array([o[r["name"]] for r in members[c]]); d = v - np.median(v); res[c] = float(np.sqrt(np.mean(d * d))); allr += list(d)
            res["pooled"] = float(np.sqrt(np.mean(np.square(allr)))); return res
        true = rms(deltas_B({})); prng = np.random.default_rng(424242 + (0 if f == "canonical" else 1)); scr = []
        for _ in range(20):
            perm = {}
            for c in DCL:
                ms = [r["logms"] for r in members[c]]; p = prng.permutation(len(ms))
                for j, r in enumerate(members[c]): perm[r["name"]] = ms[p[j]] - ms[j]
            scr.append(rms(deltas_B(perm)))
        med = {k: float(np.median([s[k] for s in scr])) for k in true}
        # Coma: masses permuted among the 9 (reported)
        cs = []
        for _ in range(20):
            p = prng.permutation(len(ADM)); Ev = []
            for j, c in enumerate(ADM):
                c2 = dict(c); c2["Ms"] = ADM[p[j]]["Ms"]; Ev.append(coma_E(c2, a0, edge="prim")[0])
            cs.append(float(np.std(Ev)))
        Ct = float(np.std([coma_E(c, a0, edge="prim")[0] for c in ADM]))
        bites2 = med["pooled"] > true["pooled"]
        MU["M2"] = dict(true_rms=true, scrambled_median_rms=med, coma_sd_true_ln=Ct, coma_sd_scrambled_median_ln=float(np.median(cs)), bites=bites2)
        P(f"[{f}] M2 masses scrambled (20 permutations within class): pooled rms {true['pooled']:.3f} -> {med['pooled']:.3f} dex; "
          + ", ".join(f"{c} {true[c]:.3f}->{med[c]:.3f}" for c in DCL) + f"; Coma sd(E) {Ct:.3f} -> {float(np.median(cs)):.3f} ln (reported) -> "
          f"{'BITES' if bites2 else 'DOES NOT BITE'}")
        RES["MUTATE"][f] = MU
    RES["MUTATE_ok"] = all(RES["MUTATE"][f]["M1"]["bites"] and RES["MUTATE"][f]["M2"]["bites"] for f in FOOTS)
    P(f"MUTATE: M1 {'BITES' if all(RES['MUTATE'][f]['M1']['bites'] for f in FOOTS) else 'FAILS'} on both footings; "
      f"M2 {'BITES' if all(RES['MUTATE'][f]['M2']['bites'] for f in FOOTS) else 'FAILS'} on both footings")

RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0; RES["peak_rss_gb"] = rss_gb()
P(f"\nruntime {time.time() - T0:.0f} s, peak RSS {rss_gb():.3f} GB. kappa = 1/2 FITTED; not theory closed. Relabels nothing.")
RES["out"] = OUT
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (bool, np.bool_)): return bool(o)
    if isinstance(o, (int, np.integer)): return int(o)
    if isinstance(o, (float, np.floating)): return float(o) if math.isfinite(float(o)) else None
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
