"""CFG929 (criteria f91c25f33): four small reframings of the cluster-core (MID 0.5-1.2 Mpc) lensing excess, zero new constants.
  (a) every interpolation function declared in the record (nu_s, nu_e = nu_RAR, nu_mono, P2, nu_2, nu_beta at the record's SPARC beta);
  (b) superposition / clumpiness of member baryons in the record's QUMOND field (b-QUMOND), with the algebraic own-halo bracket (b-ALG);
  (c) line-of-sight structure: eRASS1 X-ray neighbours (c-X) and a KiDS-galaxy upper bound (c-G);
  (d) the record's CFG640 / M2 cooling + condensed-source module.
Modes (one process at a time, OMP_NUM_THREADS=1, nice 10; run from this directory):
  CFG929_MODE=K    python3 cfg929.py   -> cfg929_K.out, cfg929_K.json
  CFG929_MUTATE=1  python3 cfg929.py   -> cfg929_MUTATE.out, cfg929_results_MUTATE.json
                   python3 cfg929.py   -> cfg929.out, cfg929_results.json
Read-only inputs: the CFG922 engine (exec'd slices of cfg922.py, never its output lines), CFG686/687/916/922 stored results and
cfg922_census_A1.json, the CFG4 SPARC statistic (exec'd slice of CFG4_galaxy_law.py), the CFG640 cooling rule (exec'd slices of the
engine's source text), the eRASS1 main table, the KiDS DR4 bright sample + LePhare (CFG922's A1 masses), CFG727 / CFG640 stored
results. Nothing downloaded. kappa = 1/2 FITTED; footings never pooled; cold energy mass still required; not theory closed."""
import os, sys, io, json, math, time, contextlib, resource, re, gc
import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import brentq
from scipy.special import erfc

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data")); DATA = os.path.join(REPO, "real_research", "data")
MODE = os.environ.get("CFG929_MODE", "MAIN"); MUT = os.environ.get("CFG929_MUTATE", "") == "1"
assert not (MUT and MODE == "K"), "choose one mode"
PART = os.environ.get("CFG929_PART", "") if (MODE == "MAIN" and not MUT) else ""
assert MODE == "K" or MUT or PART in ("a", "b", "c", "d", "assemble"), "MAIN runs as CFG929_PART=a|b|c|d, then CFG929_PART=assemble"
TAG = "_K" if MODE == "K" else ("_MUTATE" if MUT else ("" if PART == "assemble" else f"_part_{PART}"))
OUT = open(os.path.join(HERE, "cfg929" + TAG + ".out"), "w")
CRIT = "f91c25f33"
T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9            # bytes on macOS


sys.path.insert(0, LANES)
os.environ.pop("MUTATE", None)
import CFG4_common as C4                                                       # noqa: E402  kernels + both a0 footings
A0 = {"canonical": float(C4.A0["canonical"]), "alt": float(C4.A0["alt"])}
FEET = ("canonical", "alt")


def exec_slice(path, a, b, ns):
    src = open(path).read(); i = src.index(a); j = src.index(b, i)
    exec(compile("\n" * src[:i].count("\n") + src[i:j], path, "exec"), ns)
    return ns


# ---------------------------------------------------------------------------------------------------------------- record code
SRC922 = os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922.py")
NS = dict(os=os, sys=sys, io=io, json=json, math=math, time=time, contextlib=contextlib, np=np, cKDTree=cKDTree, brentq=brentq,
          erfc=erfc, LANES=LANES, REPO=REPO, EXT=EXT, DATA=DATA, C4=C4, A0=A0, FEET=FEET, MODE="CFG929", MUT=False, P=P, AMEND="A1")
exec_slice(SRC922, "def nu_s(y):", "# ---- KiDS bright census ----", NS)       # engine, gas, bands, inputs (no output lines)
exec_slice(SRC922, "def members_template(gas):", "def solve(fun", NS)            # CFG922's census star placement
exec_slice(SRC922, "def read_erass_tsv():", "def xcop_list():", NS)
nu_s, dsig, proj_cyl, gas_beta = NS["nu_s"], NS["dsig"], NS["proj_cyl"], NS["gas_beta"]
G, MSUN, MPC, KG, R, RM, RC, PRE = NS["G"], NS["MSUN"], NS["MPC"], NS["KG"], NS["R"], NS["RM"], NS["RC"], NS["PRE"]
H15, P15, unit, DA, zsc = NS["H15"], NS["P15"], NS["unit"], NS["DA"], NS["zsc"]
STE, STA, GAS_E, GAS_A, ER, NE, NA, AC, ACD = NS["STE"], NS["STA"], NS["GAS_E"], NS["GAS_A"], NS["ER"], NS["NE"], NS["NA"], NS["AC"], NS["ACD"]
NS686 = NS["NS"]; LR = np.log(R); NR = len(R)
TRAPZ = np.trapz
R7, R916 = NS["R7"], NS["R916"]
R922 = json.load(open(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_results_A1.json")))
CEN922 = json.load(open(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json")))
J4 = json.load(open(os.path.join(LANES, "CFG4_galaxy_law_results.json")))["numbers"]
BSTAR = {f: float(J4["H3"][f]["best_beta"]) for f in FEET}; BAND = {f: [float(x) for x in J4["H3"][f]["ci95"]] for f in FEET}

# CFG4's SPARC statistic (data arrays + sums/best), exec'd read-only
NS4 = dict(C=C4, np=np, math=math, P=lambda *a, **k: None)
exec_slice(os.path.join(LANES, "CFG4_galaxy_law.py"), "GAL = C.load_sparc()", 'banner("K  CONTROLS', NS4)

# CFG640's cooling rule (constants, a0_code, E(a), fret_of, M_ta, lam_cool, chi_cool), exec'd from the engine's source text
SRC640 = os.path.join(LANES, "CFG640_phase_source_pm", "cfg640_pm.py")
NS640 = dict(math=math, np=np, os=os)
exec_slice(SRC640, "h = 0.6736", "def h_rar(y):", NS640)
NS640["FRET_MODE"] = "census"
exec_slice(SRC640, "def fret_of(lM):", "def x_supply(", NS640)


# ---------------------------------------------------------------------------------------------------------------- helpers
def NU2(y):                                                                   # CFG468 nu_2 'standard'
    y = np.maximum(np.asarray(y, float), 1e-300); return np.exp(0.5 * np.arcsinh(0.5 * y)) / np.sqrt(y)


def nub(b):
    return lambda y: C4.nu_beta(y, b)


def law_ML(Mb, a0, nu):
    gb = G * Mb / RM ** 2
    return gb * nu(gb / a0) * RM ** 2 / G if a0 > 0 else np.array(Mb, float)


def dsig_ML(ML, chunk=40):
    """CFG922's dsig() tail with the lensing mass given directly (kg, N x NR) -> DeltaSigma (N x 8, Msun/pc^2)."""
    ML = np.atleast_2d(ML)
    if ML.shape[0] > chunk:
        return np.vstack([dsig_ML(ML[i:i + chunk], chunk) for i in range(0, ML.shape[0], chunk)])
    rhoL = np.gradient(ML, RM, axis=1) / (4 * np.pi * RM ** 2)
    out = np.empty((ML.shape[0], len(RC))); bad = ~(rhoL > 0).all(1)
    lrho = np.log(np.where(rhoL > 0, rhoL, 1e-300))
    for j, (u, rr, i0, f, sel, fac) in enumerate(PRE):
        lr_u = (1 - f) * lrho[:, i0] + f * lrho[:, i0 + 1]
        Sig = 2 * TRAPZ(np.exp(lr_u) * rr * MPC, u, axis=1)
        M2 = np.array([np.interp(RC[j], R, m) for m in ML]) + TRAPZ(rhoL[:, sel] * fac, R[sel] * MPC, axis=1)
        out[:, j] = (M2 / (np.pi * (RC[j] * MPC) ** 2) - Sig) / KG
    for i in np.where(bad)[0]:
        Sig = np.array([NS686["sigma_proj"](rhoL[i], R, Rj) for Rj in RC])
        M2 = np.array([np.interp(Rj, R, ML[i]) + TRAPZ(4 * np.pi * (R[R > Rj] * MPC) ** 2 * rhoL[i][R > Rj] * (1 - np.sqrt(1 - (Rj / R[R > Rj]) ** 2)), R[R > Rj] * MPC) for Rj in RC])
        out[i] = (M2 / (np.pi * (RC * MPC) ** 2) - Sig) / KG
    dsig_ML.nbad = getattr(dsig_ML, "nbad", 0) + int(bad.sum())
    return out


def fprime(nu, a0):
    def fp(g):
        g = np.maximum(np.asarray(g, float), 1e-300); e = 1e-6
        return (g * (1 + e) * nu(g * (1 + e) / a0) - g * (1 - e) * nu(g * (1 - e) / a0)) / (2 * g * e)
    return fp


def cum_trapz(y, x):
    return np.concatenate([np.zeros(y.shape[:-1] + (1,)), np.cumsum(0.5 * (y[..., 1:] + y[..., :-1]) * np.diff(x), axis=-1)], axis=-1)


def brow(b):
    return dict(MID=list(b["MID"]), OUTER=list(b["OUTER"]), INNER=list(b["INNER"]), Z_MID=zsc(b, "MID"), Z_OUTER=zsc(b, "OUTER"))


def classify(aB, b, sparc_ok=True, bound=False):
    aN, sN = b["MID"]; zM = (aN - 1) / sN; zO = (b["OUTER"][0] - 1) / b["OUTER"][1]; fr = (aB - aN) / (aB - 1); ook = abs(zO) < 2
    if bound:
        if fr >= 0.25: c = "NOT DECIDED (bound only)"
        elif not ook: c = "NO EFFECT on MID (bound; OUTER broken at the bound)"
        else: c = "NO EFFECT" if fr > -0.25 else "WORSENS"
    elif not ook or not sparc_ok: c = "BREAKS SOMETHING"
    elif abs(zM) < 2: c = "RESOLVES"
    elif fr >= 0.25: c = "PARTIAL"
    elif fr <= -0.25: c = "WORSENS"
    else: c = "NO EFFECT"
    return dict(cls=c, f_rem=fr, Z_MID=zM, Z_OUTER=zO, outer_ok=bool(ook), sparc_ok=bool(sparc_ok), A_MID=[aN, sN], A_OUTER=list(b["OUTER"]))


def combine(cc, ca):
    return cc if cc == ca else f"SPLIT (canonical: {cc}; alt: {ca})"


RANK = ["RESOLVES", "PARTIAL", "NO EFFECT", "WORSENS", "BREAKS SOMETHING"]


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else str(float(o))
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o


def line(lab, b, c=None):
    s = f"  {lab:34s} MID {b['MID'][0]:.4f}±{b['MID'][1]:.4f} (Z {zsc(b, 'MID'):+.2f})  OUTER {b['OUTER'][0]:.4f}±{b['OUTER'][1]:.4f} (Z {zsc(b, 'OUTER'):+.2f})"
    if c is not None: s += f"  f_rem {c['f_rem']:+.3f} -> {c['cls']}"
    P(s)


# ---------------------------------------------------------------------------------------------------------------- samples
SAMP = {"eRASS1": dict(gas=GAS_E, st=STE, cen=CEN922["eRASS1"]), "ACCEPT": dict(gas=GAS_A, st=STA, cen=CEN922["ACCEPT"])}
for nm, s in SAMP.items():
    s["Mb"] = s["gas"] * 1.2
    s["gcyl"] = proj_cyl(s["gas"], 0.5) / MSUN
    c = s["cen"]
    s["Scen"] = np.array([x["S_cen"] for x in c]); s["Sup"] = np.array([x["S_up"] for x in c])
    s["Bcen"] = np.array([x["bcg_med"] for x in c]); s["Bup"] = np.array([x["bcg_sup"] for x in c]); s["mlim"] = np.array([x["mlim"] for x in c])
    s["stars_cen"] = NS["stars_profile"](s["gas"], s["Bcen"], s["Scen"]); s["stars_up"] = NS["stars_profile"](s["gas"], s["Bup"], s["Sup"])


def bands(nm, Pm): return SAMP[nm]["st"].band(Pm)


def base_band(nm, foot, nu): return bands(nm, dsig(SAMP[nm]["Mb"], A0[foot], nu))


# ---------------------------------------------------------------------------------------------------------------- (a) kernels + SPARC
def kernels(foot, with_brackets=True):
    k = {"nu_s": nu_s, "nu_e": C4.nu_rar, "nu_mono": C4.nu_mono, "P2": C4.nu_p2, "nu_2": NU2, "nu_beta_best": nub(BSTAR[foot])}
    if with_brackets: k.update(nu_beta_lo=nub(BAND[foot][0]), nu_beta_hi=nub(BAND[foot][1]))
    return k


def sparc(nu, a0):
    S, W = NS4["sums"](nu, a0); mse = S.sum(0) / W.sum(0); U = NS4["UPS"]; win = (U >= 0.50 - 1e-9) & (U <= 0.80 + 1e-9)
    iw = int(np.argmin(np.where(win, mse, np.inf))); ib = int(np.argmin(mse))
    rw = math.sqrt(mse[iw])
    return dict(rms_window=rw, U_window=float(U[iw]), rms_best=math.sqrt(mse[ib]), U_best=float(U[ib]), kept=bool(rw <= 0.110))


CFG468 = {"nu_s": "fail T-free (+12.8) / pass T-fix (-7.0)", "nu_2": "fail (+242 / +408)", "nu_e": "pass (-30.2 / -1.1)",
          "P2": "fail (+138 / +139)", "nu_mono": "reference (0 / 0)"}


# ---------------------------------------------------------------------------------------------------------------- (b) superposition
A_H = 0.015 / 1.8153                                                         # Mpc: Hernquist a for R_e = 15 kpc (CFG922's A_BCG)
RQ = np.geomspace(0.02, 30.0, 360); TD = np.linspace(0.0, 1.0, 360)


def q_clump(m, ri, gh_q, fp_q, nu, a0):
    """exact nonlinear flux correction (Msun) through cluster-centred spheres r = RQ of one Hernquist clump (m Msun) at 3D radius ri
    (Mpc) in a host of field gh_q (SI, on RQ): (r^2/G) 1/2 int [F(host+clump) - F(host) - f'(g_h) g_c,r] dmu, F = nu(|g|/a0) g_r."""
    r = RQ[:, None]; dmin = np.maximum(np.abs(RQ - ri), 1e-4)[:, None]; dmax = (RQ + ri)[:, None]
    d = dmin * (dmax / dmin) ** TD[None, :]
    mu = np.clip((r * r + ri * ri - d * d) / (2 * r * ri), -1.0, 1.0)
    gc = G * m * MSUN / ((d + A_H) * MPC) ** 2                                 # Hernquist: G m(<d)/d^2 = G m/(d + a)^2
    cr = (r - ri * mu) / d; ct = ri * np.sqrt(np.maximum(1 - mu * mu, 0.0)) / d
    gh = gh_q[:, None]; gr = gh + gc * cr; gm = np.sqrt(gr * gr + (gc * ct) ** 2)
    X = nu(gm / a0) * gr - nu(gh / a0) * gh - fp_q[:, None] * gc * cr
    avg = TRAPZ(X * d * d, np.log(d), axis=1) / (2 * RQ * ri)
    return (RQ * MPC) ** 2 * avg / G / MSUN


def draw_masses(rng, total, mlim_log, alpha, mchar=1e11):
    """number-weighted Schechter (CFG922's declared shape) above M_lim until the clump total is reached; last clump weighted."""
    if total <= 0: return np.zeros(0), np.zeros(0)
    xl = 10 ** mlim_log / mchar
    if xl >= 50: return np.zeros(0), np.zeros(0)
    lx = np.linspace(math.log(xl), math.log(50.0), 4000); x = np.exp(lx); pdf = x ** (alpha + 1) * np.exp(-x)
    cdf = cum_trapz(pdf, lx); cdf /= cdf[-1]
    ms = []; tot = 0.0
    while tot < total:
        m = mchar * math.exp(np.interp(rng.uniform(), cdf, lx)); ms.append(m); tot += m
    ms = np.array(ms); w = np.ones(len(ms)); w[-1] = (total - (tot - ms[-1])) / ms[-1]
    return ms, w


def member_sets(nm):
    """per cluster lists (m Msun, r_i Mpc, w) for the declared member sets; positions ~ the gas template (CFG922), 3D to 3 Mpc."""
    s = SAMP[nm]; gas = s["gas"]; n = gas.shape[0]; sel = R <= 3.0
    out = {"central": [], "upper": [], "MAX": []}
    rngs = {"central": np.random.default_rng(929), "upper": np.random.default_rng(9291), "MAX": np.random.default_rng(9292)}
    g3 = gas[:, sel][:, -1] / MSUN
    for i in range(n):
        cdf = gas[i, sel] / gas[i, sel][-1]; ok = np.r_[True, np.diff(cdf) > 0]; cdf_i, r_i = cdf[ok], R[sel][ok]
        xl = 10 ** s["mlim"][i] / 1e11
        for key, mem, alpha, F in (("central", max(s["Scen"][i] - s["Bcen"][i], 0.0), -1.0, math.exp(-xl)),
                                   ("upper", max(s["Sup"][i] - s["Bup"][i], 0.0), -1.5, float(erfc(math.sqrt(xl))))):
            M3 = mem * g3[i] / s["gcyl"][i]
            ms, w = draw_masses(rngs[key], F * M3, s["mlim"][i], alpha)
            rr = np.interp(rngs[key].uniform(size=len(ms)), cdf_i, r_i)
            out[key].append(np.c_[ms, rr, w] if len(ms) else np.zeros((0, 3)))
        T = 0.2 * g3[i]; nfull = int(T // 1e11); frac = T / 1e11 - nfull
        ms = np.full(nfull + (1 if frac > 0 else 0), 1e11); w = np.ones(len(ms))
        if frac > 0: w[-1] = frac
        rr = np.interp(rngs["MAX"].uniform(size=len(ms)), cdf_i, r_i)
        out["MAX"].append(np.c_[ms, rr, w])
    return out


def overlap_frac(cl, gh_row):
    """fraction of clumps whose equality-radius zone overlaps another's (isotropic directions, seed 9293)."""
    if len(cl) < 2: return 0.0
    rng = np.random.default_rng(9293); v = rng.normal(size=(len(cl), 3)); v /= np.linalg.norm(v, axis=1)[:, None]
    x = v * cl[:, 1][:, None]; gh = np.interp(cl[:, 1], R, gh_row)
    re = np.sqrt(G * cl[:, 0] * MSUN / np.maximum(gh, 1e-300)) / MPC
    tree = cKDTree(x); rmax = float(re.max()); hit = np.zeros(len(cl), bool)      # KD-tree (no N x N array; memory)
    for i in range(len(cl)):
        for j in tree.query_ball_point(x[i], re[i] + rmax):
            if j != i and np.linalg.norm(x[i] - x[j]) < re[i] + re[j]: hit[i] = True; break
    return float(np.mean(hit))


def guard(tag):
    """hard memory guard (machine rule: each process < 1 GB): stop before the limit, never after."""
    if rss_gb() > 0.95:
        P(f"ABORT (memory guard): peak RSS {rss_gb():.2f} GB > 0.95 GB at {tag}"); OUT.flush(); sys.exit(3)


def qumond_dML(nm, sets_key, SETS, foot, nu, scale=1.0, idx=None):
    """Delta M_L (kg, N x NR) from the members' nonlinear flux corrections; scale multiplies every clump mass (weights / scale)."""
    s = SAMP[nm]; a0 = A0[foot]; Mb = s["Mb"]; n = Mb.shape[0]; fp = fprime(nu, a0); idx = range(n) if idx is None else idx
    dML = np.zeros_like(Mb); nclump = 0; ovl = []
    for i in idx:
        cl = SETS[sets_key][i]
        if len(cl) == 0: continue
        gh_q = G * np.interp(RQ, R, Mb[i]) / (RQ * MPC) ** 2; fp_q = fp(gh_q); tot = np.zeros(len(RQ))
        for m, ri, w in cl:
            if ri < RQ[0]: continue
            tot += (w / scale) * q_clump(m * scale, ri, gh_q, fp_q, nu, a0); nclump += 1
        dML[i] = np.interp(LR, np.log(RQ), tot, left=0.0, right=0.0) * MSUN
        ovl.append(overlap_frac(cl, G * Mb[i] / RM ** 2)); guard(f"b-QUMOND {sets_key} {nm} cluster {i}")
    return dML, dict(n_clumps=nclump, overlap_frac_mean=float(np.mean(ovl)) if ovl else 0.0)


def alg_ML(Mb, Mmem, a0, nu, chunk=40):
    """b-ALG: each member keeps its own isolated law halo (m nu(g_h)) instead of the smooth response f'(g_h) m."""
    if Mb.shape[0] > chunk:                                                   # chunked over clusters (memory only)
        return np.vstack([alg_ML(Mb[i:i + chunk], Mmem[i:i + chunk], a0, nu, chunk) for i in range(0, Mb.shape[0], chunk)])
    gh = G * Mb / RM ** 2; ML = law_ML(Mb, a0, nu); fp = fprime(nu, a0)
    I = np.where(gh > 0, nu(np.maximum(gh, 1e-300) / a0) - fp(gh), 0.0)
    dM = np.gradient(Mmem, RM, axis=1)
    return ML + cum_trapz(I * dM, RM)


# ---------------------------------------------------------------------------------------------------------------- (c) line of sight
RG = np.geomspace(0.005, 10.0, 120)                                           # projected radii (Mpc) for neighbour Sigma
PREG = []
for Rj in RG:
    umax = np.arccosh(R[-1] / Rj); u = NS686["U_GRID"] * umax; rr = Rj * np.cosh(u)
    idxf = np.interp(np.log(rr), LR, np.arange(NR, dtype=float)); i0 = np.clip(np.floor(idxf).astype(int), 0, NR - 2)
    PREG.append((u, rr, i0, idxf - i0))
RAZ = np.r_[0.0, np.geomspace(1e-3, 3.0, 300)]; PHI = np.linspace(0, np.pi, 181)


def sigma_rg(ML_row):
    rhoL = np.gradient(ML_row, RM) / (4 * np.pi * RM ** 2); lrho = np.log(np.where(rhoL > 0, rhoL, 1e-300))
    return np.array([2 * TRAPZ(np.exp((1 - f) * lrho[i0] + f * lrho[i0 + 1]) * rr * MPC, u) for (u, rr, i0, f) in PREG])


def offset_dsig(Sig_n, d, s):
    """azimuthally averaged DeltaSigma (Msun/pc^2 at RC) around the target from one neighbour of projected profile Sig_n (kg/m^2 on
    RG, its own physical scale) at offset d (Mpc, target frame), s = D_A(neighbour)/D_A(target)."""
    rr = np.sqrt(RAZ[:, None] ** 2 + d * d - 2 * RAZ[:, None] * d * np.cos(PHI)[None, :]) * s
    lS = np.interp(np.log(np.maximum(rr, RG[0])), np.log(RG), np.log(np.maximum(Sig_n, 1e-300)))
    Sg = np.where(rr > RG[-1], 0.0, np.exp(lS)); Saz = TRAPZ(Sg, PHI, axis=1) / np.pi
    M2 = cum_trapz(2 * np.pi * RAZ * Saz, RAZ)
    return (np.interp(RC, RAZ, M2) / (np.pi * RC ** 2) - np.interp(RC, RAZ, Saz)) / KG


def erass_rows():
    rows = NS["read_erass_tsv"](); ra = np.array([r[1] for r in rows]); de = np.array([r[2] for r in rows])
    return rows, unit(ra, de), np.array([r[3] for r in rows]), np.array([r[4] for r in rows]), np.array([r[5] for r in rows])


def neighbours():
    rows, ex, ez, emg, er5 = erass_rows(); tree = cKDTree(ex); ch01 = 2 * math.sin(math.radians(0.1 / 60) / 2)
    out = []; nself = 0
    for t in range(NE):
        c0 = unit(np.array([ER["ra"][t]]), np.array([ER["dec"][t]]))[0]; zt = float(ER["z"][t])
        selfs = {i for i in tree.query_ball_point(c0, ch01) if abs(ez[i] - zt) < 1e-3}; nself += bool(selfs)
        Dt = DA(zt); th = 5.0 / Dt; ii = tree.query_ball_point(c0, 2 * math.sin(th / 2))
        nb = []
        for i in ii:
            if i in selfs or abs(ez[i] - zt) > 0.05 * (1 + zt) or not (emg[i] > 0 and er5[i] > 0): continue
            ang = math.acos(min(1.0, float(ex[i] @ c0))); nb.append((ang * Dt, DA(float(ez[i])) / Dt, emg[i], er5[i], float(ez[i])))
        out.append(nb)
    return out, dict(n_rows=len(rows), n_targets_matched=nself)


def cX_dsig(NB, foot, nu, plant=None):
    """c-X DeltaSigma per target (N x 8). plant = offset (Mpc) of a planted copy of the target itself (MUTATE Mc1)."""
    a0 = A0[foot]; out = np.zeros((NE, len(RC))); cache = {}
    for t in range(NE):
        lst = NB[t] if plant is None else [(plant, 1.0, ER["mg"][t], ER["R500"][t], float(ER["z"][t]))]
        for (d, s, mg, r5, zn) in lst:
            key = (round(mg, 6), round(r5, 6))
            if key not in cache:
                Mb = gas_beta(np.array([mg]), np.array([r5]))[0] * 1.2
                cache[key] = sigma_rg(law_ML(Mb[None, :], a0, nu)[0])
            out[t] += offset_dsig(cache[key], d, s)
        guard(f"c-X target {t}")
    return out


# KiDS bright sample: plain FITS-header parser + chunked reads (no memory map), then CFG922's A1 load_bright / mlim / Census
def _fits_layout(path):
    def val(card):
        v = card[10:].strip()
        if v.startswith("'"):
            j = v.index("'", 1); return v[1:j].strip()
        return v.split("/")[0].strip()
    with open(path, "rb") as f:
        def header():
            h = {}
            while True:
                blk = f.read(2880)
                if len(blk) < 2880: raise IOError("truncated FITS header")
                for k in range(36):
                    card = blk[80 * k:80 * k + 80].decode("ascii", "replace")
                    if card[:8].strip() == "END": return h
                    if card[8:10] == "= ": h[card[:8].strip()] = val(card)
        h0 = header(); size = 0
        if int(h0.get("NAXIS", "0")) > 0:
            size = abs(int(h0["BITPIX"])) // 8
            for k in range(1, int(h0["NAXIS"]) + 1): size *= int(h0[f"NAXIS{k}"])
        f.seek(f.tell() + ((size + 2879) // 2880) * 2880)
        h1 = header(); loc = f.tell()
    code = {"L": "i1", "B": "u1", "I": ">i2", "J": ">i4", "K": ">i8", "E": ">f4", "D": ">f8"}
    fields = []
    for k in range(1, int(h1["TFIELDS"]) + 1):
        mt = re.match(r"(\d*)([LXBIJKAED])", h1[f"TFORM{k}"]); rep = int(mt.group(1) or 1); t = mt.group(2); nm = h1[f"TTYPE{k}"]
        if t == "A": fields.append((nm, f"S{rep}"))
        elif t == "X": fields.append((nm, "u1", ((rep + 7) // 8,)))
        else: fields.append((nm, code[t]) if rep == 1 else (nm, code[t], (rep,)))
    dt = np.dtype(fields); assert dt.itemsize == int(h1["NAXIS1"]), (dt.itemsize, h1["NAXIS1"])
    return dt, int(h1["NAXIS2"]), loc


def read_cols(path, names, chunk=20000):
    dt, n, loc = _fits_layout(path); rl = dt.itemsize
    out = {k: np.empty(n, "f8") for k in names}; buf = bytearray(chunk * rl)
    with open(path, "rb") as f:
        f.seek(loc)
        for i0 in range(0, n, chunk):
            m = min(chunk, n - i0); mv = memoryview(buf)[:m * rl]; f.readinto(mv); rec = np.frombuffer(mv, dtype=dt)
            for k in names: out[k][i0:i0 + m] = rec[k]
            del rec, mv
    return out


NS["read_cols"] = read_cols
exec_slice(SRC922, "def load_bright():", "def census_652(", NS)                # A1 masses, M_lim(z) table, Census (unit metric)


def census_profile(CEN, ra, dec, z, radii):
    """CFG922 Census.run algebra (A1 masses, masked kept) for several apertures; background = the 2.5-5.0 Mpc annulus."""
    B = CEN.B; Da = DA(z); c0 = unit(np.array([ra]), np.array([dec]))[0]
    ii = np.array(CEN.tree.query_ball_point(c0, 2 * math.sin(5.0 / Da / 2) * 1.0001), int)
    xyz = CEN.xyz[ii]; zz = B["z"][ii]; mk = B["masked"][ii]; ok = B["ok"][ii]; Mm, Ms = 10 ** B["mmed"][ii], 10 ** B["msup"][ii]
    Rg = np.arccos(np.clip(np.einsum('ij,j->i', xyz, c0), -1, 1)) * Da
    win = ok & (np.abs(zz - z) <= 0.05 * (1 + z)); ann = win & (Rg >= 2.5) & (Rg <= 5.0); bc = win & (Rg <= 0.15); um = mk == 0
    bcg_med = Mm[bc & um].max() if (bc & um).any() else 0.0; bcg_sup = Ms[bc].max() if bc.any() else 0.0
    c_cen, c_up, _ = CEN.comp(z); n_ann_allz = int(((Rg >= 2.5) & (Rg <= 5.0)).sum()); out = []
    for Rap in radii:
        ap = win & (Rg <= Rap); ratio = (np.pi * Rap ** 2) / (np.pi * (5.0 ** 2 - 2.5 ** 2))
        net_med = Mm[ap & um].sum() - Mm[ann & um].sum() * ratio
        sig_sup = math.sqrt((Ms[ann] ** 2).sum() * ratio); net_sup = Ms[ap].sum() - Ms[ann].sum() * ratio
        S_up = bcg_sup + c_up * max(net_sup + 2 * sig_sup - bcg_sup, 0.0); S_cen = bcg_med + c_cen * max(net_med - bcg_med, 0.0)
        n_ap_allz = int((Rg <= Rap).sum()); cov = n_ap_allz / (n_ann_allz * ratio) if n_ann_allz > 0 else 0.0
        out.append(dict(R=Rap, net_med=float(net_med), net_sup=float(net_sup), sig_sup=float(sig_sup), bcg_med=float(bcg_med),
                        bcg_sup=float(bcg_sup), S_up=float(S_up), S_cen=float(S_cen), coverage=float(cov), n_ann_allz=n_ann_allz))
    return out


def kids_census():
    t = time.time(); B = NS["load_bright"](); CEN = NS["Census"](B)
    P(f"  KiDS bright (A1 masses): {len(B['ra']):,} rows, census ready ({time.time() - t:.0f} s); peak RSS so far {rss_gb():.2f} GB")
    return CEN


RAPS = (0.5, 0.556, 0.808, 1.175)

# ---------------------------------------------------------------------------------------------------------------- (d) cooling
C640 = NS640


def tcool(nH, T):
    return 3 * C640["C_N_NH"] * C640["CKB"] * T / (2 * C640["C_NE_NH"] * nH * C640["lam_cool"](T))


def rcool(rho_fn, T, tref_fn, rmin, rmax, n=2000):
    """largest r (cm) in [rmin, rmax] with t_cool(r) <= t_ref(r); 0 if none; rho_fn(r_cm) in g/cm^3."""
    rr = np.geomspace(rmin, rmax, n); mu_n = C640["C_MU"] * C640["CMP"] * C640["C_N_NH"]
    g = lambda x: tcool(rho_fn(x) / mu_n, T) / tref_fn(x) - 1.0
    v = np.array([g(x) for x in rr]); ok = v <= 0
    if not ok.any(): return 0.0
    k = int(np.where(ok)[0][-1])
    if k == n - 1: return rmax
    return brentq(g, rr[k], rr[k + 1], xtol=1e-300, rtol=1e-14, maxiter=500)


def cooling_sample(nm, foot, tref="dyn"):
    """per cluster r_cool (Mpc) and M_cool (Msun) from the measured gas with the record's cooling inputs."""
    s = SAMP[nm]; gas = s["gas"]; a0 = A0[foot] * 100.0; CMPC = C640["CMPC"]; rc_out = []; mc_out = []; kT = []
    for i in range(gas.shape[0]):
        Mret = 1.2 * gas[i][R <= 3.0][-1] * 1e3                                 # g
        V = (C640["CG"] * Mret * a0) ** 0.25; T = C640["C_MU"] * C640["CMP"] * V * V / (2 * C640["CKB"])
        if nm == "eRASS1":
            rcb = 0.15 * ER["R500"][i]; dm = 4 * np.pi * RM ** 2 * (1 + (R / rcb) ** 2) ** -1.0; dm[R > 3.0] = 0
            Msh = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RM))]; norm = ER["mg"][i] * MSUN / np.interp(ER["R500"][i], R, Msh)
            rho_fn = (lambda x, rcb=rcb, norm=norm: norm * 1e-3 * (1 + (x / CMPC / rcb) ** 2) ** -1.0 if x / CMPC <= 3.0 else 1e-300)
        else:
            rho = np.gradient(gas[i], RM) / (4 * np.pi * RM ** 2); pos = rho > 0
            rho_fn = (lambda x, lr=LR[pos], lrho=np.log(rho[pos]): float(np.exp(np.interp(math.log(x / CMPC), lr, lrho))) * 1e-3 if x / CMPC <= 3.0 else 1e-300)
        if tref == "dyn": tf = (lambda x, V=V: x / V)
        else:
            a = 1.0 / (1.0 + float(ER["z"][i] if nm == "eRASS1" else ACD["z"][i])); H = 100 * 0.674 * 1e5 / CMPC * C640["E"](a)
            tf = (lambda x, H=H: 1.0 / H)
        rc = rcool(rho_fn, T, tf, 1e-3 * CMPC, 3.0 * CMPC) / CMPC
        guard(f"cooling {nm} {i}"); rc_out.append(rc); mc_out.append(float(np.interp(rc, R, gas[i])) / MSUN if rc > 0 else 0.0); kT.append(C640["CKB"] * T / C640["CKEV"])
    return np.array(rc_out), np.array(mc_out), np.array(kT)


def m2_ML(nm, foot, nu, rc, stars="f020", chi=None):
    """d-M2: M_L = M_b,all + M_c [nu(G M_c/r^2 a0) - 1], condensed = stars + gas inside r_cool (chi=1: all gas; chi=0: none)."""
    s = SAMP[nm]; gas = s["gas"]; a0 = A0[foot]
    st = 0.2 * gas if stars == "f020" else s["stars_cen"]; Mall = gas + st
    if chi == 1: cool = gas
    elif chi == 0: cool = np.zeros_like(gas)
    else: cool = np.array([np.where(R <= rc[i], gas[i], np.interp(rc[i], R, gas[i])) for i in range(gas.shape[0])])
    Mc = st + cool; gc = G * Mc / RM ** 2
    return Mall + Mc * (np.where(Mc > 0, nu(np.maximum(gc, 1e-300) / a0), 1.0) - 1.0), Mc, Mall


RES = {"lane": "CFG929", "criteria": CRIT, "mode": MODE, "mutate": MUT}
P(f"CFG929 {'K' if MODE == 'K' else ('MUTATE' if MUT else 'MAIN')} (criteria {CRIT}). eRASS1 {NE} (decisive), ACCEPT {NA} (reported). "
  f"kappa = 1/2 FITTED; footings never pooled.")

# =============================================================================================================== K
if MODE == "K":
    K = {}
    # K1 CFG687 nu_mono
    d1 = 0.0; k1 = {}
    for f in FEET:
        b = base_band("eRASS1", f, C4.nu_mono); st = R7["A"][f"{f}|b0.67|rc0.15|f0.20"]
        d1 = max(d1, max(abs(b[k][i] - st[k][i]) for k in ("MID", "OUTER") for i in (0, 1))); k1[f] = brow(b)
    K["K1"] = dict(A=k1, maxdiff=d1, pass_=bool(d1 < 1e-6))
    P(f"K1 CFG687 nu_mono: MID {k1['canonical']['MID'][0]:.4f}±{k1['canonical']['MID'][1]:.4f} / {k1['alt']['MID'][0]:.4f}±{k1['alt']['MID'][1]:.4f}; "
      f"OUTER {k1['canonical']['OUTER'][0]:.4f} / {k1['alt']['OUTER'][0]:.4f}; max |dA| {d1:.1e} -> {'PASS' if K['K1']['pass_'] else 'FAIL'}")
    # K2 CFG916 LR-c (nu_s) eRASS1 + ACCEPT, and the dsig_ML identity
    d2 = 0.0; k2 = {}; did = 0.0
    for f in FEET:
        st = R916["readings"]["LR-c"]["M"]["can" if f == "canonical" else "alt"]["peri"]
        for nm in ("eRASS1", "ACCEPT"):
            Pm = dsig(SAMP[nm]["Mb"], A0[f], nu_s); b = bands(nm, Pm); k2[f"{nm}|{f}"] = brow(b)
            d2 = max(d2, max(abs(b["MID"][i] - st[nm]["A_MID"][i]) for i in (0, 1)), max(abs(b["OUTER"][i] - st[nm]["A_OUTER"][i]) for i in (0, 1)))
            did = max(did, float(np.max(np.abs(dsig_ML(law_ML(SAMP[nm]["Mb"], A0[f], nu_s)) / Pm - 1))))
    K["K2"] = dict(A=k2, maxdiff=d2, dsigML_identity=did, pass_=bool(d2 < 1e-6 and did < 1e-12))
    P(f"K2 CFG916 LR-c nu_s: eRASS1 MID {k2['eRASS1|canonical']['MID'][0]:.4f} / {k2['eRASS1|alt']['MID'][0]:.4f}, OUTER "
      f"{k2['eRASS1|canonical']['OUTER'][0]:.4f} / {k2['eRASS1|alt']['OUTER'][0]:.4f}; ACCEPT MID {k2['ACCEPT|canonical']['MID'][0]:.4f} / "
      f"{k2['ACCEPT|alt']['MID'][0]:.4f}; max |dA| {d2:.1e}; dsig_ML identity {did:.1e} -> {'PASS' if K['K2']['pass_'] else 'FAIL'}")
    # K3 CFG922 A1 stored values
    d3 = 0.0; k3 = {}; s = SAMP["eRASS1"]
    for f in FEET:
        r = R922["results"][f"eRASS1|s|{f}"]
        for lab, Mb in (("baseline_f020", s["Mb"]), ("census_central", s["gas"] + s["stars_cen"])):
            b = bands("eRASS1", dsig(Mb, A0[f], nu_s)); k3[f"{lab}|{f}"] = brow(b)
            d3 = max(d3, max(abs(b[k][i] - r[lab][k][i]) for k in ("MID", "OUTER") for i in (0, 1)))
        lam = r["U_lambda_conc_on_gascyl"]["A1"]["value"]
        bU = bands("eRASS1", dsig(s["gas"] + s["stars_cen"] + (lam * s["gcyl"] / P15)[:, None] * H15[None, :] * MSUN, A0[f], nu_s))
        k3[f"U_lambda|{f}"] = dict(lam=lam, A_MID=bU["MID"][0]); d3 = max(d3, abs(bU["MID"][0] - 1.0))
    K["K3"] = dict(v=k3, maxdiff=d3, pass_=bool(d3 < 1e-6))
    P(f"K3 CFG922 A1: census_central MID {k3['census_central|canonical']['MID'][0]:.4f} / {k3['census_central|alt']['MID'][0]:.4f}; "
      f"U-lambda {k3['U_lambda|canonical']['lam']:.4f} -> A_MID {k3['U_lambda|canonical']['A_MID']:.7f}, {k3['U_lambda|alt']['lam']:.4f} -> "
      f"{k3['U_lambda|alt']['A_MID']:.7f}; max |d| {d3:.1e} -> {'PASS' if K['K3']['pass_'] else 'FAIL'}")
    # K4 CFG4 SPARC
    d4 = 0.0; k4 = {}
    for f in FEET:
        for kn, kf in (("P2", C4.nu_p2), ("nu_mono", C4.nu_mono)):
            S_, W_ = NS4["sums"](kf, A0[f]); rr_, uu_, _ = NS4["best"](S_, W_); st = J4["H2"][f"{f}|{kn}"]
            k4[f"{f}|{kn}"] = (rr_, uu_); d4 = max(d4, abs(rr_ - st["rms"]), abs(uu_ - st["U"]))
        S_, W_ = NS4["sums"](nub(BSTAR[f]), A0[f]); rr_, uu_, _ = NS4["best"](S_, W_)
        k4[f"{f}|nu_beta_best"] = (rr_, uu_); d4 = max(d4, abs(rr_ - J4["H3"][f]["best_rms"]), abs(uu_ - J4["H3"][f]["U_best"]))
    K["K4"] = dict(v=k4, maxdiff=d4, pass_=bool(d4 < 1e-9))
    P(f"K4 CFG4 SPARC: " + "; ".join(f"{k} {v[0]:.6f}@{v[1]:.2f}" for k, v in k4.items()) + f"; max |d| {d4:.1e} -> {'PASS' if K['K4']['pass_'] else 'FAIL'}")
    # K5 cooling code vs the record's chi_cool
    E = C640; d5 = 0.0; n5 = 0
    for f in FEET:
        for z in (0.0, 0.5, 1.0, 2.0):
            a = 1 / (1 + z)
            for Dta in (150.0, 300.0):
                for lM in (13.0, 13.5, 14.0, 14.5, 15.0):
                    Rr = (10 ** lM / ((4 * math.pi / 3) * Dta * 0.315 * 2.775e11)) ** (1 / 3)
                    chi_rec = E["chi_cool"](Rr, Dta, a, "FLAT", f)
                    Mta = E["M_ta"](Rr, Dta); fr = E["fret_of"](math.log10(Mta))
                    Mret = fr * E["FB"] * Mta / 0.674 * E["CMSUN"]; Mhot = (fr - E["F_FLOOR"]) * E["FB"] * Mta / 0.674 * E["CMSUN"]
                    a0c = E["a0_code"](a, "FLAT", f) * E["ACC_UNIT"] * 100.0; V = (E["CG"] * Mret * a0c) ** 0.25
                    T = E["C_MU"] * E["CMP"] * V * V / (2 * E["CKB"]); Rp = a * Rr / 0.674 * E["CMPC"]
                    rc = rcool(lambda x: Mhot / (4 * math.pi * Rp * x * x), T, lambda x: x / V, 1e-6 * Rp, Rp)
                    chi_me = min(1.0, rc / Rp); n5 += 1
                    d5 = max(d5, abs(chi_me - chi_rec) / max(chi_rec, 1e-300))
    K["K5"] = dict(n=n5, maxrel=d5, pass_=bool(d5 < 1e-9))
    P(f"K5 cooling: this lane's r_cool on CFG640's isothermal catchment vs the record's chi_cool, {n5} cells: max rel {d5:.1e} -> "
      f"{'PASS' if K['K5']['pass_'] else 'FAIL'}")
    # K6 kernels vs CFG468's printed ratios
    yv = np.array([0.05, 1.0, 3.0]); rat = {"nu_s": (nu_s(yv) / C4.nu_mono(yv)), "nu_2": (NU2(yv) / C4.nu_mono(yv)), "nu_e": (C4.nu_rar(yv) / C4.nu_mono(yv))}
    ref = {"nu_s": [1.002, 1.023, 1.038], "nu_2": [0.907, 0.804, 0.862], "nu_e": [1.000, 1.000, 0.998]}
    d6 = max(float(np.max(np.abs(rat[k] - np.array(ref[k])))) for k in ref)
    K["K6"] = dict(ratios={k: v.tolist() for k, v in rat.items()}, ref=ref, maxdiff=d6, pass_=bool(d6 <= 0.0005 + 1e-12))
    P(f"K6 kernels: " + "; ".join(f"{k} {np.round(v, 4).tolist()}" for k, v in rat.items()) + f" vs CFG468 {ref}; max |d| {d6:.4f} -> "
      f"{'PASS' if K['K6']['pass_'] else 'FAIL'}")
    # K7 census profile code at R = 0.5 vs stored A1 raw values
    CEN = kids_census(); d7 = 0.0; nb7 = 0
    for nm, ra_, de_, z_ in (("eRASS1", ER["ra"], ER["dec"], ER["z"]), ("ACCEPT", ACD["ra"], ACD["dec"], ACD["z"])):
        for i in range(len(z_)):
            p = census_profile(CEN, float(ra_[i]), float(de_[i]), float(z_[i]), (0.5,))[0]; st = SAMP[nm]["cen"][i]
            for k in ("net_sup", "sig_sup", "net_med"): d7 = max(d7, abs(p[k] - st[k]) / max(abs(st[k]), 1.0))
            if st["coverage"] >= 0.5:
                nb7 += 1
                for k in ("bcg_sup", "bcg_med"): d7 = max(d7, abs(p[k] - st[k]) / max(abs(st[k]), 1.0))
    K["K7"] = dict(maxrel=d7, n_bcg_checked=nb7, peak_rss_gb=rss_gb(), pass_=bool(d7 < 1e-9))
    P(f"K7 census profile at R = 0.5 Mpc vs stored A1 (net_sup, sig_sup, net_med all; bcg for {nb7} covered): max rel {d7:.1e} -> "
      f"{'PASS' if K['K7']['pass_'] else 'FAIL'}")
    allp = all(v["pass_"] for v in K.values())
    P(f"\nK overall: {'ALL PASS' if allp else 'FAILURES PRESENT'} ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    json.dump(clean(dict(RES, K=K, all_pass=allp)), open(os.path.join(HERE, "cfg929_K.json"), "w"), indent=1)
    sys.exit(0 if allp else 1)

# =============================================================================================================== MUTATE
if MUT:
    M = {}; ok_all = True
    # Mc2: c-G at random positions (run first so the catalogue is freed before the clump sums; memory only)
    CEN = kids_census(); rr = np.random.default_rng(9290); rnet = {0.5: [], 1.175: []}
    for i in range(NE):
        p0 = census_profile(CEN, float(ER["ra"][i]), float(ER["dec"][i]), float(ER["z"][i]), (0.5,))[0]
        for _ in range(20):
            a_ = rr.uniform(0, 2 * np.pi); sh = rr.uniform(1, 3); ra_ = (ER["ra"][i] + sh * np.cos(a_) / np.cos(np.radians(ER["dec"][i]))) % 360
            de_ = ER["dec"][i] + sh * np.sin(a_); pr = census_profile(CEN, float(ra_), float(de_), float(ER["z"][i]), (0.5, 1.175))
            if pr[0]["n_ann_allz"] >= 0.5 * p0["n_ann_allz"]:
                rnet[0.5].append(pr[0]["net_med"]); rnet[1.175].append(pr[1]["net_med"]); break
    mc2 = {str(k): dict(n=len(v), mean=float(np.mean(v)), sem=float(np.std(v, ddof=1) / math.sqrt(len(v)))) for k, v in rnet.items()}
    pc2 = all(abs(v["mean"]) < 3 * v["sem"] for v in mc2.values()); M["Mc2"] = dict(v=mc2, pass_=bool(pc2)); ok_all &= pc2
    P(f"Mc2 random positions: net member mass " + "; ".join(f"R {k}: {v['mean']:.3e} ± {v['sem']:.2e} (N {v['n']})" for k, v in mc2.items()) +
      f" -> {'HOLDS' if pc2 else 'FAIL'}")
    del CEN; gc.collect(); guard("Mc2")
    # Ma: a0 x 10 moves every kernel; a0 -> 0 gives the stored Newtonian A_MID
    ma = {}
    for f in FEET:
        for kn, nu in kernels(f, with_brackets=False).items():
            b0 = base_band("eRASS1", f, nu); b10 = bands("eRASS1", dsig(SAMP["eRASS1"]["Mb"], 10 * A0[f], nu))
            ma[f"{kn}|{f}"] = dict(A_MID=b0["MID"][0], A_MID_a0x10=b10["MID"][0], shift_sigma=abs(b10["MID"][0] - b0["MID"][0]) / b0["MID"][1])
    bN = bands("eRASS1", dsig(SAMP["eRASS1"]["Mb"], 0.0, nu_s)); stN = R7["A"]["newton"]["MID"][0]
    pa = all(v["shift_sigma"] > 5 for v in ma.values()) and abs(bN["MID"][0] / stN - 1) < 1e-3
    M["Ma"] = dict(kernels=ma, newton_MID=bN["MID"][0], newton_stored=stN, pass_=bool(pa)); ok_all &= pa
    P(f"Ma a0 x 10: min shift {min(v['shift_sigma'] for v in ma.values()):.1f} sigma over {len(ma)} kernel-footings; a0 -> 0 MID {bN['MID'][0]:.4f} "
      f"(stored {stN:.4f}) -> {'BITES' if pa else 'FAIL'}")
    # Mb1: b-ALG with the members smoothed (own-halo term off) = the plain law
    s = SAMP["eRASS1"]; d_b1 = 0.0
    for f in FEET:
        ML0 = law_ML(s["Mb"], A0[f], nu_s); MLs = alg_ML(s["Mb"], np.zeros_like(s["Mb"]), A0[f], nu_s)
        d_b1 = max(d_b1, float(np.max(np.abs(dsig_ML(MLs) / dsig_ML(ML0) - 1))))
    pb1 = d_b1 < 1e-12; M["Mb1"] = dict(maxrel=d_b1, pass_=bool(pb1)); ok_all &= pb1
    P(f"Mb1 b-ALG with members smoothed = plain law: max rel {d_b1:.1e} -> {'HOLDS' if pb1 else 'FAIL'}")
    # Mb2: clump masses x 1e-3 (weights x 1e3) -> |Delta M_L(0.8 Mpc)| shrinks >= x10
    SETS = member_sets("eRASS1"); i08 = int(np.searchsorted(R, 0.808)); mb2 = {}
    for f in FEET:
        dA, _ = qumond_dML("eRASS1", "central", SETS, f, nu_s); dB, _ = qumond_dML("eRASS1", "central", SETS, f, nu_s, scale=1e-3)
        a_, b_ = float(np.sum(np.abs(dA[:, i08]))), float(np.sum(np.abs(dB[:, i08])))
        mb2[f] = dict(sum_abs_dML_08=a_ / MSUN, scaled=b_ / MSUN, ratio=a_ / max(b_, 1e-300))
    pb2 = all(v["ratio"] >= 10 for v in mb2.values()); M["Mb2"] = dict(v=mb2, pass_=bool(pb2)); ok_all &= pb2
    P(f"Mb2 smooth limit: sum|dM_L(0.81 Mpc)| {mb2['canonical']['sum_abs_dML_08']:.3e} -> {mb2['canonical']['scaled']:.3e} Msun (x{mb2['canonical']['ratio']:.0f}); alt "
      f"x{mb2['alt']['ratio']:.0f} -> {'BITES' if pb2 else 'FAIL'}")
    # Mb3: tiny clump linear cancellation; heavy clump bites
    f = "canonical"; a0 = A0[f]; gh_q = G * np.interp(RQ, R, s["Mb"][0]) / (RQ * MPC) ** 2; fp_q = fprime(nu_s, a0)(gh_q)
    qt = q_clump(1e6, 0.8, gh_q, fp_q, nu_s, a0); lin = fp_q * 1e6; rt = float(np.max(np.abs(qt) / lin))
    qh = q_clump(10 ** 12.5, 0.8, gh_q, fp_q, nu_s, a0); jn = int(np.argmin(np.abs(RQ - 0.8))); rh = float(abs(qh[jn]) / (fp_q[jn] * 10 ** 12.5))
    pb3 = rt < 1e-3 and rh > 1e-3; M["Mb3"] = dict(tiny_max_ratio=rt, heavy_ratio_at_08=rh, heavy_q_at_08=float(qh[jn]), pass_=bool(pb3)); ok_all &= pb3
    P(f"Mb3 tiny 1e6 clump |q|/(f'm) max {rt:.1e} (< 1e-3); heavy 10^12.5 clump at 0.8 Mpc: q {qh[jn]:.3e} Msun = {rh:.3f} f'm -> {'BITES' if pb3 else 'FAIL'}")
    # Mc1: planted self-copy at 2 Mpc (shell sign) and 0.1 Mpc (bites)
    mc1 = {}
    for f in FEET:
        D2 = cX_dsig(None, f, nu_s, plant=2.0); D01 = cX_dsig(None, f, nu_s, plant=0.1)
        inner = RC < 2.0; mc1[f] = dict(frac_le0_inside=float(np.mean(D2[:, inner] <= 1e-12)), frac_pos_outside=float(np.mean(D2[:, ~inner] > 0)),
                                        frac_mid_up_01=float(np.mean((D01[:, 3:6] > 0).all(1))), max_inside=float(D2[:, inner].max()))
    pc1 = all(v["frac_le0_inside"] == 1.0 and v["frac_pos_outside"] == 1.0 and v["frac_mid_up_01"] == 1.0 for v in mc1.values())
    M["Mc1"] = dict(v=mc1, pass_=bool(pc1)); ok_all &= pc1
    P(f"Mc1 planted copy: at 2 Mpc DeltaSigma <= 0 inside in {mc1['canonical']['frac_le0_inside']:.3f} of bins (max {mc1['canonical']['max_inside']:.2e}), > 0 beyond "
      f"in {mc1['canonical']['frac_pos_outside']:.3f}; at 0.1 Mpc MID up in {mc1['canonical']['frac_mid_up_01']:.3f} -> {'BITES' if pc1 else 'FAIL'}")
    # Md: chi = 1 and r_cool = 3 Mpc reproduce the plain law; chi = 0 gives stars only
    dmd1 = dmd3 = dmdb = 0.0; r_next = float(R[np.searchsorted(R, 3.0, side="right")])
    for f in FEET:
        PL = dsig_ML(law_ML(s["Mb"], A0[f], nu_s))
        ML1, _, _ = m2_ML("eRASS1", f, nu_s, None, chi=1); ML3, _, _ = m2_ML("eRASS1", f, nu_s, np.full(NE, 3.0))
        MLb, _, _ = m2_ML("eRASS1", f, nu_s, np.full(NE, r_next))
        dmd1 = max(dmd1, float(np.max(np.abs(dsig_ML(ML1) / PL - 1)))); dmd3 = max(dmd3, float(np.max(np.abs(dsig_ML(ML3) / PL - 1))))
        dmdb = max(dmdb, float(np.max(np.abs(dsig_ML(MLb) / PL - 1))))
    _, Mc0, _ = m2_ML("eRASS1", "canonical", nu_s, None, chi=0); d0 = float(np.max(np.abs(Mc0 - 0.2 * s["gas"])))
    pmd = dmd1 < 1e-12 and dmd3 < 1e-12 and d0 == 0.0
    # Md-b (POST-HOC AMENDMENT 2026-10-20, no class weight): CFG687's gas is cumulated by trapezoid, so half a grid step of gas lies
    # beyond the 3 Mpc cut (between the last node <= 3 Mpc and the next). r_cool = 3.0 leaves it uncooled; the next node does not.
    pmdb = dmd1 < 1e-12 and dmdb < 1e-12 and d0 == 0.0
    M["Md"] = dict(maxrel_chi1=dmd1, maxrel_rcool3=dmd3, chi0_maxdiff=d0, pass_=bool(pmd),
                   Md_b_posthoc=dict(r_next_Mpc=r_next, maxrel=dmdb, pass_=bool(pmdb))); ok_all &= pmd
    P(f"Md chi = 1 vs plain law max rel {dmd1:.1e}; r_cool = 3 Mpc max rel {dmd3:.1e}; chi = 0 condensed = 0.20 gas (max diff {d0:.1e}) -> "
      f"{'HOLDS' if pmd else 'FAIL (as frozen)'}")
    P(f"Md-b (post hoc) r_cool = first grid node beyond 3 Mpc ({r_next:.5f} Mpc): max rel {dmdb:.1e} -> {'HOLDS' if pmdb else 'FAIL'}")
    amended = bool(all(v["pass_"] for k, v in M.items() if k != "Md") and pmdb)
    P(f"\nMUTATE as frozen: {'every arm bites / holds' if ok_all else 'FAILURES PRESENT (Md r_cool = 3 Mpc leg)'}; with the post-hoc Md-b in "
      f"place of that leg: {'every arm bites / holds' if amended else 'FAILURES PRESENT'} ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    json.dump(clean(dict(RES, MUTATE=M, all_pass_frozen=ok_all, all_pass_with_Md_b_posthoc=amended)),
              open(os.path.join(HERE, "cfg929_results_MUTATE.json"), "w"), indent=1)
    sys.exit(0 if ok_all else 1)

# =============================================================================================================== MAIN
if PART == "assemble":
    parts = {x: json.load(open(os.path.join(HERE, f"cfg929_part_{x}.json"))) for x in "abcd"}
    for x in "abcd":
        for l in open(os.path.join(HERE, f"cfg929_part_{x}.out")).read().splitlines()[1:]: P(l)
    RESULTS = {x: parts[x]["results"][x] for x in "abcd"}
    P("\n== Summary (eRASS1, nu_s decides; classes per footing canonical | alt)")
    SUM = {x: RESULTS[x]["overall"] for x in "abcd"}
    for k, v in SUM.items(): P(f"  ({k}) {v}")
    PEAK = {x: parts[x]["peak_rss_gb"] for x in "abcd"}
    P(f"\nDone; per-part peak RSS (GB) {PEAK}. kappa = 1/2 FITTED; footings never pooled; cold energy mass still required; not theory closed.")
    json.dump(clean(dict(RES, summary=SUM, results=RESULTS, part_peak_rss_gb=PEAK)), open(os.path.join(HERE, "cfg929_results.json"), "w"), indent=1)
    sys.exit(0)

RESULTS = {}
BASE = {(nm, f, k): base_band(nm, f, nu) for nm in SAMP for f in FEET for k, nu in (("s", nu_s), ("mono", C4.nu_mono))}
if PART == "a":
    P("\n== Baselines (gas x 1.2)")
    for (nm, f, k), b in BASE.items(): line(f"{nm} nu_{k} {f}", b)

if PART == "c":
    # ---- KiDS census profiles for (c-G), first, so the catalogue is freed before the clump sums (memory; no number depends on order)
    import gc
    P("\n== KiDS census profiles for (c-G) (computed first; the catalogue is then freed)")
    CEN = kids_census(); CG_ = [census_profile(CEN, float(ER["ra"][i]), float(ER["dec"][i]), float(ER["z"][i]), RAPS) for i in range(NE)]
    del CEN; gc.collect(); guard("KiDS census"); P(f"  done; peak RSS so far {rss_gb():.2f} GB")

if PART == "a":
    # ---- (a)
    P("\n== (a) interpolation-function family (each kernel replaces nu_s; SPARC = CFG4 statistic, H2 threshold, Upsilon in 0.50-0.80)")
    RA = {}
    for f in FEET:
        aB = BASE[("eRASS1", f, "s")]["MID"][0]
        for kn, nu in kernels(f).items():
            b = base_band("eRASS1", f, nu); ba = base_band("ACCEPT", f, nu); sp = sparc(nu, A0[f])
            c = classify(aB, b, sp["kept"]); ca = classify(BASE[("ACCEPT", f, "s")]["MID"][0], ba, sp["kept"])
            beta = BSTAR[f] if kn == "nu_beta_best" else (BAND[f][0] if kn == "nu_beta_lo" else (BAND[f][1] if kn == "nu_beta_hi" else None))
            RA[f"{kn}|{f}"] = dict(beta=beta, eRASS1=brow(b), ACCEPT=brow(ba), sparc=sp, cls=c, cls_ACCEPT=ca, cfg468=CFG468.get(kn, "-"))
            line(f"{kn}{'' if beta is None else f'({beta:.4f})'} {f}", b, c)
            P(f"      SPARC rms {sp['rms_window']:.4f}@{sp['U_window']:.2f} in window (best {sp['rms_best']:.4f}@{sp['U_best']:.2f}) -> "
              f"{'kept' if sp['kept'] else 'NOT kept'}; CFG468 {CFG468.get(kn, '-')}; ACCEPT MID {ba['MID'][0]:.3f}, OUTER {ba['OUTER'][0]:.3f} -> {ca['cls']}")
    CAND = ["nu_e", "nu_mono", "P2", "nu_2", "nu_beta_best"]
    fam = {}
    for f in FEET:
        best = min(CAND, key=lambda k: (RANK.index(RA[f"{k}|{f}"]["cls"]["cls"]), -RA[f"{k}|{f}"]["cls"]["f_rem"]))
        fam[f] = dict(best_kernel=best, cls=RA[f"{best}|{f}"]["cls"]["cls"])
    beta_cls = {f: [RA[f"{k}|{f}"]["cls"]["cls"] for k in ("nu_beta_best", "nu_beta_lo", "nu_beta_hi")] for f in FEET}
    beta_dep = {f: len(set(v)) > 1 for f, v in beta_cls.items()}
    ova = combine(fam["canonical"]["cls"], fam["alt"]["cls"]) + (" [BRACKET-DEPENDENT: nu_beta band edges " + json.dumps(beta_cls) + "]" if any(beta_dep.values()) else "")
    RESULTS["a"] = dict(rows=RA, best_per_footing=fam, beta_classes=beta_cls, beta_bracket_dependent=beta_dep, overall=ova,
                        per_kernel={k: combine(RA[f"{k}|canonical"]["cls"]["cls"], RA[f"{k}|alt"]["cls"]["cls"]) for k in CAND})
    P(f"  (a) per kernel: {RESULTS['a']['per_kernel']}")
    P(f"  (a) best per footing: {fam}; nu_beta classes (best, lo, hi): {beta_cls} -> bracket-dependent {beta_dep}")
    P(f"  (a) OVERALL: {ova}")

if PART == "b":
    # ---- (b)
    P("\n== (b) superposition / clumpiness")
    RB = {}; SETS = {nm: member_sets(nm) for nm in SAMP}
    for nm in SAMP:
        for key in ("central", "upper", "MAX"):
            nc = [len(x) for x in SETS[nm][key]]
            P(f"  {nm} member set {key}: clumps per cluster median {np.median(nc):.0f} (max {max(nc)}), total {sum(nc)}; clump mass "
              f"median {np.median(np.concatenate([x[:, 0] for x in SETS[nm][key] if len(x)])):.2e} Msun")
    for nm in SAMP:
        for kk, nu in (("s", nu_s), ("mono", C4.nu_mono)):
            for f in FEET:
                aB = BASE[(nm, f, kk)]["MID"][0]; s = SAMP[nm]; ML0 = law_ML(s["Mb"], A0[f], nu)
                keys = ("central", "upper", "MAX") if kk == "s" else ("central",)
                for key in keys:
                    t = time.time(); dML, info = qumond_dML(nm, key, SETS[nm], f, nu)
                    b = bands(nm, dsig_ML(ML0 + dML)); c = classify(aB, b)
                    i08 = int(np.searchsorted(R, 0.808))
                    RB[f"QUMOND|{key}|{nm}|{kk}|{f}"] = dict(band=brow(b), cls=c, info=info, rel_dML_08_median=float(np.median(dML[:, i08] / ML0[:, i08])))
                    del dML; gc.collect()
                    line(f"b-QUMOND {key} {nm} nu_{kk} {f}", b, c)
                    P(f"      clumps {info['n_clumps']}, overlap fraction {info['overlap_frac_mean']:.3f}, median dM_L/M_L at 0.81 Mpc "
                      f"{RB[f'QUMOND|{key}|{nm}|{kk}|{f}']['rel_dML_08_median']:+.2e} ({time.time() - t:.0f} s; RSS {rss_gb():.2f} GB)")
                # b-ALG: baseline stars (primary of the bracket) and census sets
                mems = {"f020": s["Mb"] / 6.0,
                        "census_central": (np.maximum(s["Scen"] - s["Bcen"], 0)[:, None] * NS["members_template"](s["gas"]) * MSUN),
                        "census_upper": (np.maximum(s["Sup"] - s["Bup"], 0)[:, None] * NS["members_template"](s["gas"]) * MSUN)}
                for mk, Mmem in mems.items():
                    Mb = s["Mb"] if mk == "f020" else s["gas"] + (s["stars_cen"] if mk == "census_central" else s["stars_up"])
                    aBm = aB if mk == "f020" else bands(nm, dsig(Mb, A0[f], nu))["MID"][0]
                    b = bands(nm, dsig_ML(alg_ML(Mb, Mmem, A0[f], nu))); c = classify(aBm, b)
                    RB[f"ALG|{mk}|{nm}|{kk}|{f}"] = dict(band=brow(b), cls=c, A_MID_base=aBm); line(f"b-ALG {mk} {nm} nu_{kk} {f}", b, c)
        gh08 = G * np.array([np.interp(0.808, R, m) for m in SAMP[nm]["Mb"]]) / (0.808 * MPC) ** 2
        RB[f"r_e|{nm}"] = {lab: float(np.median(np.sqrt(G * m * MSUN / gh08) / MPC * 1e3)) for lab, m in (("1e10.5", 10 ** 10.5), ("1e11", 1e11))}
        P(f"  {nm} equality radius at 0.81 Mpc (median, kpc): {RB[f'r_e|{nm}']} (CFG726 supply edges 175-886 kpc)")
    cb = {f: RB[f"QUMOND|central|eRASS1|s|{f}"]["cls"]["cls"] for f in FEET}
    cb_br = {f: {k: RB[f"QUMOND|{k}|eRASS1|s|{f}"]["cls"]["cls"] for k in ("upper", "MAX")} for f in FEET}
    cb_alg = {f: RB[f"ALG|f020|eRASS1|s|{f}"]["cls"]["cls"] for f in FEET}
    cb_mono = {f: RB[f"QUMOND|central|eRASS1|mono|{f}"]["cls"]["cls"] for f in FEET}
    dep_b = any(cb_alg[f] != cb[f] or any(v != cb[f] for v in cb_br[f].values()) for f in FEET)
    frag_b = any(cb_mono[f] != cb[f] for f in FEET)
    ovb = combine(cb["canonical"], cb["alt"]) + (" [BRACKET-DEPENDENT]" if dep_b else "") + (" [FRAGILE (kernel)]" if frag_b else "")
    RESULTS["b"] = dict(rows=RB, primary=cb, brackets=cb_br, alg=cb_alg, mono=cb_mono, bracket_dependent=dep_b, fragile_kernel=frag_b, overall=ovb)
    P(f"  (b) OVERALL: {ovb}  (primary {cb}; brackets {cb_br}; b-ALG {cb_alg}; nu_mono {cb_mono})")

if PART == "c":
    # ---- (c)
    P("\n== (c) line-of-sight structure")
    RCc = {}; NB, nbinfo = neighbours(); nnb = np.array([len(x) for x in NB])
    P(f"  eRASS1 main rows {nbinfo['n_rows']}; targets matched to themselves {nbinfo['n_targets_matched']}/{NE}; neighbours per target: mean {nnb.mean():.2f}, "
      f"max {nnb.max()}, targets with >= 1: {int((nnb > 0).sum())}")
    s = SAMP["eRASS1"]; gcylR = {Rap: proj_cyl(s["gas"], Rap) / MSUN for Rap in RAPS}
    SupR = {}
    for j, Rap in enumerate(RAPS):
        S = np.array([c[j]["S_up"] for c in CG_]); cov = np.array([c[j]["coverage"] for c in CG_]); meas = cov >= 0.5
        S = np.where((cov >= 0.5) & (cov < 1.0), S / np.maximum(cov, 1e-9), S)
        p84 = float(np.percentile(S[meas] / gcylR[Rap][meas], 84)); S = np.where(meas, S, p84 * gcylR[Rap]); SupR[Rap] = S
        P(f"  KiDS S_up(<{Rap} Mpc) / (0.20 gas_cyl): median {np.median(S / (0.2 * gcylR[Rap])):.3f}, 84th {np.percentile(S / (0.2 * gcylR[Rap]), 84):.3f}, "
          f"max {np.max(S / (0.2 * gcylR[Rap])):.2f}; not measured {int((~meas).sum())}")
    X = np.max(np.array([np.maximum(SupR[Rap] - 0.2 * gcylR[Rap], 0.0) for Rap in RAPS]), axis=0)
    P(f"  LOS stellar extra X = max_R max(0, S_up - 0.20 gas_cyl): clusters with X > 0: {int((X > 0).sum())}/{NE}; median {np.median(X):.3e}, "
      f"84th {np.percentile(X, 84):.3e}, max {X.max():.3e} Msun; (needed concentrated: lambda x gas_cyl, median {np.median(2.2369 * s['gcyl']):.2e})")
    RCc["X"] = dict(n_pos=int((X > 0).sum()), median=float(np.median(X)), p84=float(np.percentile(X, 84)), max=float(X.max()),
                    ratio_Sup_to_model={str(Rap): float(np.median(SupR[Rap] / (0.2 * gcylR[Rap]))) for Rap in RAPS})
    for kk, nu in (("s", nu_s), ("mono", C4.nu_mono)):
        for f in FEET:
            aB = BASE[("eRASS1", f, kk)]["MID"][0]; PL = dsig(s["Mb"], A0[f], nu)
            DX = cX_dsig(NB, f, nu); bX = bands("eRASS1", PL + DX); cX = classify(aB, bX)
            out = {"cX": dict(band=brow(bX), cls=cX, mean_dsig=DX.mean(0).tolist())}
            line(f"c-X nu_{kk} {f}", bX, cX)
            for fac in (6.0, 1.0):
                PG = dsig(s["Mb"] + (fac * X / P15)[:, None] * H15[None, :] * MSUN, A0[f], nu)
                bG = bands("eRASS1", PG); cG = classify(aB, bG, bound=True); out[f"cG_x{fac:.0f}"] = dict(band=brow(bG), cls=cG)
                line(f"c-G (bound) x{fac:.0f} nu_{kk} {f}", bG, cG)
                if fac == 6.0:
                    bXG = bands("eRASS1", PG + DX); cXG = classify(aB, bXG, bound=True); out["cX+cG"] = dict(band=brow(bXG), cls=cXG)
                    line(f"c-X + c-G x6 (primary) nu_{kk} {f}", bXG, cXG)
                    TG = PG - PL
            # shape bound: largest scale before OUTER Z = -2
            for tl, T in (("cX", DX), ("cG", TG)):
                def zo(sc): b_ = bands("eRASS1", PL + sc * T); return zsc(b_, "OUTER") + 2.0
                if np.abs(T).max() == 0 or zo(0.0) < 0: out[f"shape_{tl}"] = dict(scale=None); continue
                hi = 1.0
                while zo(hi) > 0 and hi < 1e6: hi *= 2
                sc = brentq(zo, 0.0, hi, xtol=1e-8) if zo(hi) <= 0 else float("inf")
                b_ = bands("eRASS1", PL + sc * T) if np.isfinite(sc) else None
                fr_ = (aB - b_["MID"][0]) / (aB - 1) if b_ else None
                out[f"shape_{tl}"] = dict(scale=sc, f_rem=fr_)
                P(f"      shape bound {tl}: OUTER reaches Z = -2 at x{sc:.3g} of the computed term; MID removal there " + (f"{fr_:+.3f}" if fr_ is not None else "n/a (never)"))
            RCc[f"{kk}|{f}"] = out
    cc = {f: RCc[f"s|{f}"]["cX+cG"]["cls"]["cls"] for f in FEET}; ccX = {f: RCc[f"s|{f}"]["cX"]["cls"]["cls"] for f in FEET}
    cc_mono = {f: RCc[f"mono|{f}"]["cX+cG"]["cls"]["cls"] for f in FEET}
    frag_c = any(cc_mono[f] != cc[f] for f in FEET)
    ovc = combine(cc["canonical"], cc["alt"]) + (" [FRAGILE (kernel)]" if frag_c else "")
    RESULTS["c"] = dict(rows=RCc, neighbours=dict(nbinfo, mean=float(nnb.mean()), max=int(nnb.max()), n_with=int((nnb > 0).sum())),
                        primary=cc, cX_alone=ccX, mono=cc_mono, overall=ovc)
    P(f"  (c) OVERALL: {ovc}  (c-X alone {ccX}; nu_mono {cc_mono})")

if PART == "d":
    # ---- (d)
    P("\n== (d) the record's CFG640 / M2 cooling + condensed-source module")
    RD = {}; sp640 = json.load(open(os.path.join(LANES, "CFG640_phase_source_pm", "cfg640_split.json")))
    P(f"  CFG640 design table (stored): max (f_c - 0.10) {sp640['max_fc_minus_floor']:.2e}; largest bracket (f_ret - 0.10) chi {sp640['max_bracket_fc_minus_floor']:.2e}")
    r727 = json.load(open(os.path.join(LANES, "CFG727_hot_gas_untethered", "cfg727_results.json")))
    RD["cfg727_stored"] = {k: r727["T_R"][k] for k in r727["T_R"] if k.endswith("|P") or k.endswith("ALL")}
    P(f"  CFG727 stored (reservoir reading, not re-run): " + "; ".join(f"{k}: " + json.dumps(v, default=str)[:140] for k, v in list(RD["cfg727_stored"].items())[:3]))
    for nm in SAMP:
        for f in FEET:
            for tref in ("dyn", "age"):
                t = time.time(); rc, mc, kT = cooling_sample(nm, f, tref); s = SAMP[nm]
                cyl = np.array([proj_cyl(np.where(R <= rc[i], s["gas"][i], np.interp(rc[i], R, s["gas"][i]))[None, :], 0.5)[0] for i in range(len(rc))]) / MSUN
                lam = R922["results"][f"eRASS1|s|{f}"]["U_lambda_conc_on_gascyl"]["A1"]["value"]
                RD[f"cool|{nm}|{f}|{tref}"] = dict(rc_kpc_median=float(np.median(rc) * 1e3), rc_kpc_max=float(rc.max() * 1e3), frac_cooling=float(np.mean(rc > 0)),
                                                   Mcool_median=float(np.median(mc)), Mcool_p84=float(np.percentile(mc, 84)), Mcool_max=float(mc.max()),
                                                   cyl_over_needed_median=float(np.median(cyl / (lam * s["gcyl"]))), cyl_over_needed_max=float(np.max(cyl / (lam * s["gcyl"]))),
                                                   kT_keV_median=float(np.median(kT)), chi_median=float(np.median(mc / (s["gas"][:, R <= 3.0][:, -1] / MSUN))))
                P(f"  {nm} {f} t_ref={tref}: kT median {np.median(kT):.2f} keV; cooling in {np.mean(rc > 0):.3f} of clusters; r_cool median "
                  f"{np.median(rc) * 1e3:.1f} kpc (max {rc.max() * 1e3:.1f}); M_cool median {np.median(mc):.2e} (84th {np.percentile(mc, 84):.2e}, max {mc.max():.2e}) Msun; "
                  f"cooled cylinder mass / needed lambda gas_cyl: median {np.median(cyl / (lam * s['gcyl'])):.2e}, max {np.max(cyl / (lam * s['gcyl'])):.2e} ({time.time() - t:.0f} s)")
                if True:
                    for kk, nu in (("s", nu_s), ("mono", C4.nu_mono)):
                        aB = BASE[(nm, f, kk)]["MID"][0]
                        for stars in ("f020", "census"):
                            ML, Mc, Mall = m2_ML(nm, f, nu, rc, stars=stars); b = bands(nm, dsig_ML(ML))
                            aBs = aB if stars == "f020" else bands(nm, dsig(Mall, A0[f], nu))["MID"][0]
                            c = classify(aBs, b); RD[f"M2|{nm}|{f}|{tref}|{kk}|{stars}"] = dict(band=brow(b), cls=c, A_MID_base=aBs)
                            line(f"d-M2 {nm} {tref} nu_{kk} stars={stars} {f}", b, c)
                        bp = bands(nm, dsig_ML(law_ML(SAMP[nm]["Mb"], A0[f], nu))); RD[f"plain|{nm}|{f}|{tref}|{kk}"] = dict(band=brow(bp), diff_MID=bp["MID"][0] - aB)
    cd = {f: RD[f"M2|eRASS1|{f}|dyn|s|f020"]["cls"]["cls"] for f in FEET}
    cd_age = {f: RD[f"M2|eRASS1|{f}|age|s|f020"]["cls"]["cls"] for f in FEET}
    cd_mono = {f: RD[f"M2|eRASS1|{f}|dyn|mono|f020"]["cls"]["cls"] for f in FEET}
    dep_d = any(cd_age[f] != cd[f] for f in FEET); frag_d = any(cd_mono[f] != cd[f] for f in FEET)
    ovd = combine(cd["canonical"], cd["alt"]) + (" [BRACKET-DEPENDENT]" if dep_d else "") + (" [FRAGILE (kernel)]" if frag_d else "")
    RESULTS["d"] = dict(rows=RD, primary=cd, age_bracket=cd_age, mono=cd_mono, overall=ovd,
                        plain_identity_maxdiff=max(abs(v["diff_MID"]) for k, v in RD.items() if k.startswith("plain|")))
    P(f"  d-plain (all-baryon source, cooling relabels phase): max |dA_MID| {RESULTS['d']['plain_identity_maxdiff']:.1e} (identity)")
    P(f"  (d) OVERALL: {ovd}  (age bracket {cd_age}; nu_mono {cd_mono})")

json.dump(clean(dict(RES, part=PART, results=RESULTS, peak_rss_gb=rss_gb(), dsig_ML_fallbacks=getattr(dsig_ML, "nbad", 0))),
          open(os.path.join(HERE, f"cfg929_part_{PART}.json"), "w"), indent=1)
P(f"part {PART} done ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
