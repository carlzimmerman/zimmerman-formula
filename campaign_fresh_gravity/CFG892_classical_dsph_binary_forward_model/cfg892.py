"""CFG892 -- can UNDETECTED binaries make the classical dSphs' excess?  Criteria: FROZEN_CRITERIA.md (5b5da1665), block 890-899.
Pick-up of CFG861's open caveats (delta is a lower bound; no instrument zero point; the 4.5 km/s bound not re-checked).
Data path = CFG861's: Walker+2023 per-epoch catalogue through CFG51's reduce_walker.py (imported UNCHANGED as a module), classical =
LVD-matched and M_V <= -7.7, M = members with >= 2 quality epochs.  Per-epoch arrays rebuilt with build_stars' filter, row order and
stable HJD sort.  Delta_LVD from CFG852's delta_ups2 (ast extraction, CFG860/861's method), sigma_law^2 = law(g_bar) r_1/2 / 3.
Forward model per realization: v_ij = u_i + b_i(t_ij) + z_k + e_ij n_ij at each M star's real epochs and quoted errors; u ~ N(0, sigma_law);
b = Keplerian RV with probability f; then CFG51's velocity window (two passes, sigma_seed = max(sigma_LVD, 3)), chi2 p < 0.01 cleaning,
Gaussian MLE (known errors) on first epochs (single) and on the all-epoch means of the unflagged stars (clean).  Paired no-binary twin.
Graded: per dwarf (CFG861's five), Q95 = max over P1-P5 x f {0.3, 0.5, 0.7} of the 95th percentile of
sigma_ex = sgn(sc^2 - sigma_law^2) sqrt|sc^2 - sigma_law^2|, against sigma_need = sqrt(max(sigma_obs^2 - sigma_law^2, 0)),
sigma_obs = min(Walker sigma_clean(M), sigma_LVD sigma_clean(M)/sigma_single(M)).  Classes as frozen.
Run: python3 cfg892.py -> cfg892.out, cfg892_results.json;  CFG892_MUTATE=1 -> cfg892_MUTATE.out, cfg892_results_MUTATE.json.
Implementation notes (fixed before the first full run):
  * the chi2 flag in the simulations is chi2 > chi2.isf(0.01, n-1), identical to p < 0.01 except on a measure-zero boundary;
    K1 uses the reducer's own p values.
  * the simulation MLE is a vectorised profile-likelihood fit (64-point grid on CFG51's [0, top] range, then 48 bisections on the
    derivative); K1b checks it against reduce_walker.mle_sigma on the 20 real sets.
  * Kepler: mean anomaly reduced mod 2 pi, Danby start E0 = M + 0.85 e sgn(sin M), 30 Newton steps (K3 checks the residual).
  * epoch times are HJD minus the system's earliest HJD (equivalent under the random mean anomaly).
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, json, math, ast, time, resource, importlib.util, numpy as np
from scipy.stats import chi2 as chi2dist

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG892_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt")
PCUT, R, RSUN_AU, KCONST = 0.01, 1000, 0.00465047, 29.78
GRADED_NAMES = ("Crater II", "Sextans", "Ursa Minor", "Draco", "Carina")
OTHER_NAMES = ("Antlia II", "Leo II", "Sculptor", "Fornax", "Leo I")
INSTR = {"hectocat.dat.gz": 0, "m2fshi.dat.gz": 1, "m2fsmed.dat.gz": 2}; INAME = ("Hectochelle", "M2FS HiRes", "M2FS MedRes")
F_ALL = (0.0, 0.3, 0.5, 0.7, 1.0); F_GRADED = (0.3, 0.5, 0.7)
# binary populations (FROZEN_CRITERIA.md); common: q ~ U[qlo, 1], M1 0.8, e ~ U[0, 0.8] for P > 10 d (e = 0 below), cut a(1-e) >= 3 R1
POPS = {
    "P1": dict(per=("lognormal", 5.03, 2.28), ecc=("uniform", 0.8), qlo=0.1, R1=10.0, label="lognormal 5.03/2.28 (CFG93's values; Raghavan+10)"),
    "P2": dict(per=("lognormal", 4.8, 2.3), ecc=("uniform", 0.8), qlo=0.1, R1=10.0, label="lognormal 4.8/2.3 (DM91, as in CFG334)"),
    "P3": dict(per=("lognormal", 4.0, 2.28), ecc=("uniform", 0.8), qlo=0.1, R1=10.0, label="lognormal 4.0/2.28 (CFG93 short-period-heavy)"),
    "P4": dict(per=("flat", 0.5, 8.0), ecc=("uniform", 0.8), qlo=0.1, R1=10.0, label="flat log P 0.5-8 (CFG93)"),
    "P5": dict(per=("lognormal", 5.03, 2.28), ecc=("thermal", 0.95), qlo=0.1, R1=10.0, label="P1 with thermal e (bracket)"),
    "P6": dict(per=("lognormal", 5.03, 2.28), ecc=("uniform", 0.8), qlo=0.1, R1=None, label="P1, NO periastron cut (unphysical upper bracket)"),
    "P1R15": dict(per=("lognormal", 5.03, 2.28), ecc=("uniform", 0.8), qlo=0.1, R1=15.0, label="P1 with R1 = 15 Rsun (CFG93 setting)"),
    "MUT": dict(per=("lognormal", 1.5, 0.3), ecc=("zero",), qlo=0.5, R1=None, label="MUTATE: lognormal 1.5/0.3, q U[0.5,1], e 0, no cut"),
}
POP_IDX = {k: i for i, k in enumerate(POPS)}; GRADED_POPS = ("P1", "P2", "P3", "P4", "P5")

# ---- CFG51's reducer, imported unchanged
spec = importlib.util.spec_from_file_location("cfg51_reduce_walker", os.path.join(LANES, "CFG51_walker_multiepoch", "reduce_walker.py"))
RW = importlib.util.module_from_spec(spec); spec.loader.exec_module(RW)
# ---- CFG852's delta_ups2 and constants via ast (CFG860/CFG861's method); alt = same function with module a0 swapped
src = ast.parse(open(os.path.join(LANES, "CFG852_gas_loss_metallicity", "cfg852.py")).read()); keep = []
for n in src.body:
    if isinstance(n, ast.FunctionDef) and n.name in ("fnum", "delta_ups2"): keep.append(n)
    elif isinstance(n, ast.Assign):
        ids = {t.id for t in n.targets if isinstance(t, ast.Name)} | {e.id for t in n.targets if isinstance(t, ast.Tuple) for e in t.elts if isinstance(e, ast.Name)}
        if ids & {"G", "Msun", "PC", "a0", "nu", "law"}: keep.append(n)
NS = {}
for ft in FOOT:
    ns = {"math": math}; exec(compile(ast.Module(body=keep, type_ignores=[]), "cfg852_subset", "exec"), ns)
    if ft == "alt": ns["a0"] = A0["alt"]
    assert abs(ns["a0"] - A0[ft]) == 0.0
    NS[ft] = ns
def sigma_law(lv, ft):
    ns = NS[ft]; fn = ns["fnum"]
    MV, rh = fn(lv.get("M_V")), fn(lv.get("rhalf_sph_physical")) or fn(lv.get("rhalf_physical"))
    r12 = (4 / 3) * rh * ns["PC"]; Ms = 2.0 * 10 ** (0.4 * (4.83 - MV)); gb = ns["G"] * (Ms / 2) * ns["Msun"] / r12 ** 2
    return math.sqrt(ns["law"](gb) * r12 / 3) / 1e3

C861 = json.load(open(os.path.join(LANES, "CFG861_classical_dsph_binaries", "cfg861_results.json")))
C861S = {r["name"]: r for r in C861["systems"]}

# ================================================================ Kepler machinery
def sample_orbits(rng, n, pop):
    """P (d), e, K (km/s), omega, M0 for n binaries with a giant primary M1 = 0.8; failed periastron draws are redrawn (CFG93)."""
    out = {k: np.empty(0) for k in ("P", "e", "K", "w", "M0")}; M1 = 0.8; cut = pop["R1"]
    while len(out["P"]) < n:
        m = 4 * (n - len(out["P"])) + 16
        kind = pop["per"][0]
        lp = rng.normal(pop["per"][1], pop["per"][2], m) if kind == "lognormal" else rng.uniform(pop["per"][1], pop["per"][2], m)
        Pd = 10 ** lp; q = rng.uniform(pop["qlo"], 1.0, m); M2 = q * M1
        ek = pop["ecc"][0]
        if ek == "uniform": e = np.where(lp > 1.0, rng.uniform(0, pop["ecc"][1], m), 0.0)
        elif ek == "thermal": e = np.where(lp > 1.0, pop["ecc"][1] * np.sqrt(rng.uniform(0, 1, m)), 0.0)
        else: e = np.zeros(m)
        a = ((M1 + M2) * (Pd / 365.25) ** 2) ** (1 / 3)
        ok = (Pd > 1.0) & (Pd < 1e10)
        if cut is not None: ok &= (a * (1 - e) >= 3 * cut * RSUN_AU)
        cosi = rng.uniform(-1, 1, m); sini = np.sqrt(1 - cosi ** 2)
        K = KCONST * M2 * sini / (M1 + M2) ** (2 / 3) / (Pd / 365.25) ** (1 / 3) / np.sqrt(1 - e ** 2)
        w = rng.uniform(0, 2 * np.pi, m); M0 = rng.uniform(0, 2 * np.pi, m)
        for k, x in zip(("P", "e", "K", "w", "M0"), (Pd, e, K, w, M0)): out[k] = np.concatenate([out[k], x[ok]])
    return {k: v[:n] for k, v in out.items()}

def kepler_E(Mm, e, nit=30):
    Mm = np.mod(Mm, 2 * np.pi); E = Mm + 0.85 * e * np.sign(np.sin(Mm))
    for _ in range(nit): E = E - (E - e * np.sin(E) - Mm) / (1 - e * np.cos(E))
    return E, Mm
def kepler_rv(t, P_, e, K, w, M0):
    E, _ = kepler_E(M0 + 2 * np.pi * t / P_, e)
    nu_ = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    return K * (np.cos(nu_ + w) + e * np.cos(w))

# ================================================================ vectorised MLE (CFG51's likelihood)
def fit_batch(X, E2, Mk, G=64, nbis=48, rchunk=64):
    X = np.asarray(X, float); Rr, N = X.shape; E2 = np.broadcast_to(np.asarray(E2, float), (Rr, N)); out = np.empty(Rr)
    lin = np.linspace(0, 1, G)
    for a in range(0, Rr, rchunk):
        x = X[a:a + rchunk]; e2 = E2[a:a + rchunk]; m = Mk[a:a + rchunk].astype(float); r = len(x); ar = np.arange(r)
        n = m.sum(1); mean = (x * m).sum(1) / n; std = np.sqrt((((x - mean[:, None]) ** 2) * m).sum(1) / n)
        emax = np.sqrt(np.where(m > 0, e2, 0.0).max(1))
        top = np.maximum(np.maximum(3 * std, 5 * emax), 1.0) * 3
        s = top[:, None] * lin[None, :]
        V2 = s[:, :, None] ** 2 + e2[:, None, :]; w = m[:, None, :] / V2
        sw = w.sum(-1); mu = (w * x[:, None, :]).sum(-1) / sw
        F = (m[:, None, :] * np.log(V2)).sum(-1) + (w * (x[:, None, :] - mu[:, :, None]) ** 2).sum(-1)
        k = F.argmin(1); del V2, w
        def h(sv):
            v2 = sv[:, None] ** 2 + e2; ww = m / v2; mu_ = (ww * x).sum(1) / ww.sum(1)
            return (ww - ww * ww * (x - mu_[:, None]) ** 2).sum(1)
        lo = s[ar, np.maximum(k - 1, 0)]; hi = s[ar, np.minimum(k + 1, G - 1)]
        for _ in range(nbis):
            mid = 0.5 * (lo + hi); neg = h(mid) < 0; lo = np.where(neg, mid, lo); hi = np.where(neg, hi, mid)
        sh = 0.5 * (lo + hi); h0 = h(np.zeros(r)); sh = np.where((k == 0) & (h0 >= 0), 0.0, sh); sh[sh < 1e-3] = 0.0
        out[a:a + r] = sh
    return out

# ================================================================ data (CFG861's path)
P("CFG892  classical dSphs: forward model of UNDETECTED binaries at the real epochs (Walker+2023 via CFG51's reducer)" + ("  [MUTATE]" if MUT else ""))
rows = []
for f in ("hectocat.dat.gz", "m2fshi.dat.gz", "m2fsmed.dat.gz"): rows += RW.parse(RW.IN + f)
stars_all = RW.build_stars(rows); lvd = RW.load_lvd()
EP = {}
for r in rows:   # build_stars' filter, row order and stable HJD sort
    if r["Gaia"] == "": continue
    if not (r["Goodobs"] > 0 and r["RRL"] == 0 and r["AGN"] == 0 and r["eVlos"] > 0 and np.isfinite(r["Vlos"])): continue
    EP.setdefault((r["Target"], r["Gaia"]), []).append(r)
for k in EP: EP[k].sort(key=lambda r: r["HJD"])
nrow = {}
for r in rows: nrow[r["Target"]] = nrow.get(r["Target"], 0) + 1
CLASSICAL = []
for n in sorted(nrow):
    x = lvd.get(n.lower()); mv = RW.fnum(x["M_V"]) if x else float("nan")
    if x is not None and mv <= -7.7: CLASSICAL.append(n)
P(f"  rows {len(rows)}, quality Gaia stars {len(stars_all)}, classical systems {len(CLASSICAL)}")

def star_stats_exact(v, e):
    """build_stars' expressions, element for element"""
    w = 1 / e ** 2; vm = np.sum(w * v) / np.sum(w); em = 1 / math.sqrt(np.sum(w))
    chi2 = float(np.sum(w * (v - vm) ** 2)); dof = len(v) - 1
    return vm, em, chi2, (chi2dist.sf(chi2, dof) if dof > 0 else float("nan"))

SYSD = {}
for si, n in enumerate(CLASSICAL):
    lv = lvd[n.lower()]; nm = lv["name"]
    stars = {k: s for k, s in stars_all.items() if s["target"] == n}
    mem, nvrej, vc, sw = RW.membership(stars, lv); mem = sorted(mem, key=lambda s: s["gaia"]); M = [s for s in mem if s["n"] >= 2]
    sl = RW.fnum(lv["vlos_sigma"])
    d = dict(name=nm, target=n, si=si, lv=lv, mem=mem, M=M, vc=vc, sig_seed=sw, sig_lvd=sl,
             D={ft: NS[ft]["delta_ups2"](lv)[0] for ft in FOOT}, lg={ft: NS[ft]["delta_ups2"](lv)[1] for ft in FOOT},
             slaw={ft: sigma_law(lv, ft) for ft in FOOT})
    if M:
        ep = [EP[(n, s["gaia"])] for s in M]; ne = np.array([len(x) for x in ep]); hj = np.concatenate([[r["HJD"] for r in x] for x in ep])
        d.update(ne=ne, starts=np.concatenate([[0], np.cumsum(ne)[:-1]]), sid=np.repeat(np.arange(len(M)), ne),
                 T=hj - hj.min(), V=np.concatenate([[r["Vlos"] for r in x] for x in ep]), E=np.concatenate([[r["eVlos"] for r in x] for x in ep]),
                 INST=np.concatenate([[INSTR[r["file"]] for r in x] for x in ep]), ep=ep)
        d["W"] = 1 / d["E"] ** 2; d["em"] = 1 / np.sqrt(np.add.reduceat(d["W"], d["starts"])); d["thr"] = chi2dist.isf(PCUT, ne - 1)
    SYSD[nm] = d

# ================================================================ K1: binary fraction 0 reproduces CFG861 (exact)
def pipeline_exact(d, vel_by_star, vc, sig_seed):
    """the lane's pipeline on given per-star epoch velocities (no binaries): window (real v_c), chi2 cleaning, CFG51's mle_sigma"""
    st = []
    for s, vv in zip(d["M"], vel_by_star):
        e = np.array([r["eVlos"] for r in d["ep"][len(st)]]); vm, em, c2, p = star_stats_exact(np.asarray(vv, float), e)
        st.append(dict(v1=float(vv[0]), e1=float(e[0]), vm=vm, em=em, p=p, inwin=bool(abs(vm - vc) < 4 * math.sqrt(sig_seed ** 2 + em ** 2))))
    K = [s for s in st if s["inwin"]]; C = [s for s in K if not (s["p"] < PCUT)]
    a = RW.mle_sigma([s["v1"] for s in K], [s["e1"] for s in K]); c = RW.mle_sigma([s["vm"] for s in C], [s["em"] for s in C])
    return dict(n_win=len(K), n_rm=len(K) - len(C), single=a, clean=c, stars=st)

P("\n  K1 (binary fraction 0, real velocities): the pipeline vs cfg861_results.json")
K1 = {}; k1ok = True; K1B = {}; k1bmax = 0.0
for nm, d in SYSD.items():
    if not d["M"]: continue
    vel = [[r["Vlos"] for r in x] for x in d["ep"]]
    res = pipeline_exact(d, vel, d["vc"], d["sig_seed"]); c = C861S[nm]
    stat_ok = all(abs(s["vm"] - m["vm"]) == 0 and abs(s["em"] - m["em"]) == 0 and abs(s["p"] - m["p"]) == 0 for s, m in zip(res["stars"], d["M"]))
    diffs = [abs(res["single"][k] - c["sig_single_M"][k]) for k in ("sig", "ep", "em")] + [abs(res["clean"][k] - c["sig_clean_M"][k]) for k in ("sig", "ep", "em")]
    ok = (res["n_win"] == len(d["M"]) == c["nM"]) and res["n_rm"] == c["n_rm"] and max(diffs) == 0.0 and stat_ok
    dok = abs(d["D"]["canonical"] - c["D_can"]) == 0 and abs(d["D"]["alt"] - c["D_alt"]) == 0
    lawrel = max(abs(d["slaw"][ft] / (d["sig_lvd"] * 10 ** (-d["D"][ft] / 2)) - 1) for ft in FOOT)
    k1ok &= ok and dok and lawrel <= 1e-12
    # K1b: the vectorised fitter on the same real sets
    st = res["stars"]; Cm = np.array([[not (s["p"] < PCUT) for s in st]])
    fs = fit_batch(np.array([[s["v1"] for s in st]]), np.array([[s["e1"] ** 2 for s in st]]), np.ones((1, len(st)), bool))[0]
    fc = fit_batch(np.array([[s["vm"] for s in st]]), np.array([[s["em"] ** 2 for s in st]]), Cm)[0]
    db = max(abs(fs - res["single"]["sig"]), abs(fc - res["clean"]["sig"])); k1bmax = max(k1bmax, db)
    K1[nm] = dict(nM=len(d["M"]), n_win=res["n_win"], n_rm=res["n_rm"], single=res["single"]["sig"], clean=res["clean"]["sig"],
                  max_abs_diff=max(diffs), star_stats_identical=stat_ok, Delta_identical=dok, sigma_law_identity_rel=lawrel, passed=ok and dok and lawrel <= 1e-12)
    K1B[nm] = dict(fast_single=fs, fast_clean=fc, max_diff=db)
    P(f"    {nm:17s} |M| {len(d['M']):4d} window-kept {res['n_win']:4d}  rm {res['n_rm']:3d} (CFG861 {c['n_rm']})  single {res['single']['sig']:.6f}  clean {res['clean']['sig']:.6f}"
      f"  max|diff| {max(diffs):.1e}  Delta {'=' if dok else '!='}  sigma_law identity {lawrel:.1e}  fast-MLE diff {db:.1e}  -> {'PASS' if K1[nm]['passed'] else 'FAIL'}")
k1bok = k1bmax <= 1e-4
P(f"  K1 {'PASS' if k1ok else 'FAIL'} (all systems exact);  K1b {'PASS' if k1bok else 'FAIL'} (fast MLE max diff {k1bmax:.2e} km/s, tolerance 1e-4)")

# ---- K3 Kepler
AU, YR = 1.495978707e11, 365.25 * 86400
kc = 2 * np.pi * AU / YR / 1e3; k3a = abs(KCONST / kc - 1) <= 1e-3
tt = np.linspace(0, 100.0, 20001)[:-1]
rv0 = kepler_rv(tt, 100.0, 0.0, 7.0, 0.3, 1.1); tpk = np.mod(-0.3 - 1.1, 2 * np.pi) * 100.0 / (2 * np.pi)
rvpk = float(kepler_rv(np.array([tpk]), 100.0, 0.0, 7.0, 0.3, 1.1)[0]); k3b = abs(rvpk - 7.0) <= 1e-9 * 7 and rv0.max() <= 7.0 * (1 + 1e-12) and rv0.min() >= -7.0 * (1 + 1e-12)
rv6 = kepler_rv(tt, 100.0, 0.6, 7.0, 0.3, 1.1); k3c = abs(rv6.mean()) <= 1e-6 * 7   # uniform-in-time sampling of an eccentric orbit
Mt = np.linspace(0, 2 * np.pi, 10001); Et, Mr = kepler_E(Mt, np.full_like(Mt, 0.95)); k3d = float(np.max(np.abs(Et - 0.95 * np.sin(Et) - Mr)))
k3ok = k3a and k3b and k3c and k3d < 1e-10
P(f"  K3 Kepler: 2 pi AU/yr = {kc:.4f} km/s vs {KCONST} (rel {abs(KCONST / kc - 1):.1e}); circular RV at the analytic peak {rvpk:.12f} vs 7, sampled range within +-K;"
  f" e=0.6 period-mean RV {rv6.mean():+.2e} km/s; Kepler residual at e=0.95 {k3d:.1e} -> {'PASS' if k3ok else 'FAIL'}")

# ================================================================ simulation
def measure(Vv, d, isb=None):
    W, st, sid, em, thr = d["W"], d["starts"], d["sid"], d["em"], d["thr"]
    sw = np.add.reduceat(W, st); vm = np.add.reduceat(W[None, :] * Vv, st, axis=1) / sw
    c2 = np.add.reduceat(W[None, :] * (Vv - vm[:, sid]) ** 2, st, axis=1); flag = c2 > thr[None, :]
    lim = 4 * np.sqrt(d["sig_seed"] ** 2 + em ** 2)[None, :]
    w1 = np.abs(vm) < lim; vc = np.nanmedian(np.where(w1, vm, np.nan), axis=1); vc = np.where(np.isfinite(vc), vc, 0.0)
    K = np.abs(vm - vc[:, None]) < lim; C = K & ~flag
    ss = fit_batch(Vv[:, st], (d["E"][st] ** 2)[None, :], K); sc = fit_batch(vm, (em ** 2)[None, :], C)
    r = dict(ss=ss, sc=sc, nK=K.sum(1), nflag=(K & flag).sum(1))
    if isb is not None: r.update(nbK=(K & isb).sum(1), ncatch=(K & isb & flag).sum(1))
    return r

def run_cell(d, sig_true, f, popk, seed_key, zoff=None, nrep=R, chunk=250):
    rng = np.random.default_rng(np.random.SeedSequence([892] + list(seed_key)))
    N = len(d["M"]); Nt = len(d["V"]); sid, T, E = d["sid"], d["T"], d["E"]; acc = {}
    for c0 in range(0, nrep, chunk):
        r = min(chunk, nrep - c0)
        base = rng.normal(0, sig_true, (r, N))[:, sid] + rng.normal(size=(r, Nt)) * E[None, :]
        if zoff is not None: base = base + np.asarray(zoff, float)[d["INST"]][None, :]
        isb = rng.random((r, N)) < f; nb = int(isb.sum()); B = np.zeros((r, Nt))
        if nb:
            o = sample_orbits(rng, nb, POPS[popk]); omap = -np.ones((r, N), int); omap[isb] = np.arange(nb)
            mk = isb[:, sid]; k = omap[:, sid][mk]; tt_ = np.broadcast_to(T[None, :], (r, Nt))[mk]
            B[mk] = kepler_rv(tt_, o["P"][k], o["e"][k], o["K"][k], o["w"][k], o["M0"][k])
        rb = measure(base + B, d, isb); r0 = measure(base, d)
        for kk, v in list(rb.items()) + [(kk + "0", v) for kk, v in r0.items()]: acc.setdefault(kk, []).append(v)
    return {k: np.concatenate(v) for k, v in acc.items()}

sq = lambda x: np.sign(x) * np.sqrt(np.abs(x))
def summarize(a, d, ft, sig_true, sig_obs_g):
    sl = sig_true; sc, ss, sc0, ss0 = a["sc"], a["ss"], a["sc0"], a["ss0"]
    exc, exs = sq(sc ** 2 - sl ** 2), sq(ss ** 2 - sl ** 2); i2c, i2s = sq(sc ** 2 - sc0 ** 2), sq(ss ** 2 - ss0 ** 2)
    with np.errstate(divide="ignore", invalid="ignore"):
        dl = np.where((sc > 0) & (ss > 0), 2 * np.log10(sc / ss), np.nan)
        catch = a["ncatch"] / a["nbK"] if "ncatch" in a else None
    q = lambda x, p: float(np.nanquantile(x, p))
    s = dict(sc_q05=q(sc, .05), sc_q50=q(sc, .5), sc_q95=q(sc, .95), ss_q50=q(ss, .5), ss_q95=q(ss, .95),
             ex_clean_q50=q(exc, .5), ex_clean_q95=q(exc, .95), ex_single_q50=q(exs, .5), ex_single_q95=q(exs, .95),
             I2_clean_q50=q(i2c, .5), I2_clean_q95=q(i2c, .95), I2_single_q50=q(i2s, .5), I2_single_q95=q(i2s, .95),
             flag_frac_med=q(a["nflag"] / a["nK"], .5), flag_frac_pooled=float(a["nflag"].sum() / a["nK"].sum()),
             flag_frac0_pooled=float(a["nflag0"].sum() / a["nK0"].sum()), win_rej_med=q(len(d["M"]) - a["nK"], .5),
             delta_q50=q(dl, .5), sc0_over_sl_med=q(sc0 / sl, .5) if sl > 0 else None,
             P_sc_ge_obs=float(np.mean(sc >= sig_obs_g)) if sig_obs_g is not None else None)
    if catch is not None:
        s.update(catch_med=q(catch, .5), catch_pooled=float(a["ncatch"].sum() / max(a["nbK"].sum(), 1)))
    d861 = C861S[d["name"]]["delta"]
    if d861 is not None: s["P_delta_le_obs"] = float(np.nanmean(dl <= d861))
    return s

def needs(d, ft, sc_M=None, ss_M=None):
    c = C861S[d["name"]]; scM = c["sig_clean_M"]["sig"] if sc_M is None else sc_M; ssM = c["sig_single_M"]["sig"] if ss_M is None else ss_M
    sW, sL = scM, d["sig_lvd"] * scM / ssM; sg = min(sW, sL); sl = d["slaw"][ft]
    nd = lambda so: math.sqrt(max(so ** 2 - sl ** 2, 0.0))
    return dict(sig_obs_W=sW, sig_obs_L=sL, sig_obs=sg, need=nd(sg), need_W=nd(sW), need_L=nd(sL),
                need_single=nd(ssM), sig_bin_861=d["sig_lvd"] * math.sqrt(1 - 10 ** (-d["D"][ft])) if d["D"][ft] > 0 else 0.0)

def classify(items):
    """items: list of (name, need, Q95) -> class, reached names"""
    nz = [(n, nd, q) for n, nd, q in items if nd > 0]
    if len(nz) < 3: return "NOT DIAGNOSTIC", []
    reached = [n for n, nd, q in nz if q >= nd]
    if not reached: return "BINARIES CANNOT EXPLAIN", reached
    if len(reached) == len(nz): return "BINARIES COULD EXPLAIN", reached
    return "PARTIAL", reached

f_idx = {f: i for i, f in enumerate(F_ALL)}
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6   # bytes on macOS

GR = [SYSD[n] for n in GRADED_NAMES]
if MUT:
    # ================================================================ MUTATE
    P("\n  MUTATE: " + POPS["MUT"]["label"] + "; f 0.7; sigma_true = sigma_law canonical; R 1000")
    MR = {}; ok_a = ok_b = True; items = []
    for d in GR:
        nd = needs(d, "canonical"); sl = d["slaw"]["canonical"]
        a = run_cell(d, sl, 0.7, "MUT", (d["si"], POP_IDX["MUT"], f_idx[0.7], 0, 0)); s = summarize(a, d, "canonical", sl, nd["sig_obs"])
        exc_med = s["ex_clean_q50"]; exs_med = s["ex_single_q50"]
        ok_a &= s["catch_med"] >= 0.70; ok_b &= exc_med < exs_med
        items.append((d["name"], nd["need_single"], s["ex_single_q95"]))
        MR[d["name"]] = dict(summary=s, needs=nd, sigma_law=sl)
        P(f"    {d['name']:12s} catch median {s['catch_med']:.3f} (pooled {s['catch_pooled']:.3f})  excess single q50 {exs_med:6.2f} q95 {s['ex_single_q95']:6.2f}"
          f"  excess clean q50 {exc_med:6.2f} q95 {s['ex_clean_q95']:6.2f}  need_single {nd['need_single']:5.2f}  need(clean) {nd['need']:5.2f}"
          f"  flag frac {s['flag_frac_med']:.3f}  window rejections {s['win_rej_med']:.0f}")
    cls_single, reached_single = classify(items)
    cls_clean, reached_clean = classify([(n, MR[n]["needs"]["need"], MR[n]["summary"]["ex_clean_q95"]) for n in MR])
    ok_c = cls_single == "BINARIES COULD EXPLAIN"
    P(f"  (a) median catch >= 0.70 in every graded dwarf -> {'PASS' if ok_a else 'FAIL'}")
    P(f"  (b) median excess(clean) < median excess(single) in every graded dwarf -> {'PASS' if ok_b else 'FAIL'}")
    P(f"  (c) single-epoch class {cls_single} (reached: {', '.join(reached_single)}) -> {'PASS' if ok_c else 'FAIL'}")
    P(f"  (info) cleaned-estimator class under the MUTATE population: {cls_clean} (reached: {', '.join(reached_clean) or 'none'})")
    P(f"  MUTATE {'BITES (3/3)' if (ok_a and ok_b and ok_c) else 'DOES NOT BITE'}")
    RES = dict(lane="CFG892", criteria_commit="5b5da1665", mutate=True, population=POPS["MUT"], per_system=MR, a_pass=bool(ok_a), b_pass=bool(ok_b),
               c_pass=bool(ok_c), class_single=cls_single, class_clean_info=cls_clean, bites=bool(ok_a and ok_b and ok_c), K1_pass=bool(k1ok), K1b_pass=bool(k1bok))
else:
    # ---- K2: f = 0
    P("\n  K2 (f = 0, sigma_true = sigma_law canonical, R 1000)")
    K2 = {}; k2ok = True
    for d in GR:
        sl = d["slaw"]["canonical"]; a = run_cell(d, sl, 0.0, "P1", (d["si"], POP_IDX["P1"], f_idx[0.0], 0, 0))
        med = float(np.median(a["sc"] / sl)); ff = float(a["nflag"].sum() / a["nK"].sum()); ok = abs(med - 1) <= 0.05 and 0.003 <= ff <= 0.03
        k2ok &= ok; K2[d["name"]] = dict(median_ratio=med, false_flag=ff, passed=ok)
        P(f"    {d['name']:12s} |M| {len(d['M']):4d}  median sigma_clean/sigma_law {med:.4f}  false-flag fraction {ff:.4f}  -> {'PASS' if ok else 'FAIL'}")
    P(f"  K2 {'PASS' if k2ok else 'FAIL'}   [{time.time() - T0:.0f} s]")

    # ---- graded grid (+ extensions) for graded and other systems, both footings
    CELLS = {}
    def cell(d, ft, popk, f, var=0, zoff=None, sig_true=None, obs=None):
        key = (d["name"], ft, popk, f, var)
        if key in CELLS: return CELLS[key]
        sl = d["slaw"][ft] if sig_true is None else sig_true
        a = run_cell(d, sl, f, popk, (d["si"], POP_IDX[popk], f_idx[f], FOOT.index(ft), var), zoff=zoff)
        nd = needs(d, ft); s = summarize(a, d, ft, sl, nd["sig_obs"] if obs is None else obs); CELLS[key] = s
        return s
    TABLE = {}
    for ft in FOOT:
        for d in GR + [SYSD[n] for n in OTHER_NAMES]:
            for popk in GRADED_POPS:
                for f in F_GRADED + (1.0,): cell(d, ft, popk, f)
            for f in (0.7, 1.0): cell(d, ft, "P6", f)
            cell(d, ft, "P1R15", 0.5)
        P(f"  grid done for {ft}   [{time.time() - T0:.0f} s, max RSS {rss_mb():.0f} MB]")

    def q95_over(d, ft, keys, field="ex_clean_q95"):
        best = max(keys, key=lambda k: CELLS[(d["name"], ft, k[0], k[1], 0)][field])
        return CELLS[(d["name"], ft, best[0], best[1], 0)][field], best
    GKEYS = [(p, f) for p in GRADED_POPS for f in F_GRADED]
    EXT_F1 = GKEYS + [(p, 1.0) for p in GRADED_POPS]; EXT_P6 = GKEYS + [("P6", 0.7), ("P6", 1.0)]; R15 = [("P1R15", 0.5)]

    PER = {}
    for ft in FOOT:
        for d in GR + [SYSD[n] for n in OTHER_NAMES]:
            nd = needs(d, ft); Q, best = q95_over(d, ft, GKEYS); Qs, bests = q95_over(d, ft, GKEYS, "ex_single_q95")
            pmax = max(CELLS[(d["name"], ft, p, f, 0)]["P_sc_ge_obs"] for p, f in GKEYS)
            PER[(d["name"], ft)] = dict(name=d["name"], footing=ft, nM=len(d["M"]), sigma_law=d["slaw"][ft], Delta_LVD=d["D"][ft], lg_gbar=d["lg"][ft],
                                        needs=nd, Q95=Q, Q95_cell=best, Q95_single=Qs, Q95_single_cell=bests, P_max=pmax,
                                        reached=bool(nd["need"] > 0 and Q >= nd["need"]),
                                        Q95_ext_f1=q95_over(d, ft, EXT_F1)[0], Q95_ext_P6=q95_over(d, ft, EXT_P6)[0], Q95_R15=q95_over(d, ft, R15)[0],
                                        primary=CELLS[(d["name"], ft, "P1", 0.5, 0)])

    def cls_for(ft, needkey="need", qkey="Q95", names=GRADED_NAMES):
        return classify([(n, PER[(n, ft)]["needs"][needkey], PER[(n, ft)][qkey]) for n in names])

    P("\n  PER DWARF (sigma in km/s; Q95 = max over P1-P5 x f 0.3/0.5/0.7 of the 95th-percentile simulated excess over the law, cleaned estimator)")
    for ft in FOOT:
        P(f"  [{ft} a0 {A0[ft]:.4e}]")
        P("  system        |M|  sig_law  sig_obs(W/L -> used)      need   Q95  (cell)        P_max  reached | primary P1 f0.5: sc q50/q95  I2 q50/q95  catch  flag sim/obs"
          "  delta sim/obs  P(d<=obs) | single: Q95 vs sig_bin(861)")
        for d in GR + [SYSD[n] for n in OTHER_NAMES]:
            x = PER[(d["name"], ft)]; nd = x["needs"]; pr = x["primary"]; c = C861S[d["name"]]
            P(f"  {d['name']:12s} {x['nM']:4d}  {x['sigma_law']:6.3f}  {nd['sig_obs_W']:5.2f}/{nd['sig_obs_L']:5.2f} -> {nd['sig_obs']:5.2f}"
              f"   {nd['need']:6.3f} {x['Q95']:6.3f} ({x['Q95_cell'][0]},{x['Q95_cell'][1]})  {x['P_max']:.3f}  {'YES' if x['reached'] else ('n/a' if nd['need'] == 0 else 'no '):3s}"
              f" | {pr['sc_q50']:5.2f}/{pr['sc_q95']:5.2f}  {pr['I2_clean_q50']:5.2f}/{pr['I2_clean_q95']:5.2f}  {pr['catch_med']:.3f}  {pr['flag_frac_pooled']:.3f}/{c['n_rm'] / c['nM']:.3f}"
              f"  {pr['delta_q50']:+.3f}/{c['delta']:+.3f}  {pr.get('P_delta_le_obs', float('nan')):.3f}"
              f" | {x['Q95_single']:6.3f} vs {nd['sig_bin_861']:5.2f}  {'GRADED' if d['name'] in GRADED_NAMES else 'reported'}")
    CLS = {ft: cls_for(ft) for ft in FOOT}
    P(f"\n  GRADED (canonical): CLASS {CLS['canonical'][0]}" + (f"  (reached: {', '.join(CLS['canonical'][1])})" if CLS['canonical'][1] else ""))
    P("\n  REPORTED VARIANTS (not graded)")
    VAR = {}
    VAR["alt footing"] = CLS["alt"]
    for ft in FOOT:
        VAR[f"{ft}: sigma_obs = Walker sigma_clean(M) only"] = cls_for(ft, "need_W")
        VAR[f"{ft}: sigma_obs = LVD-scaled only"] = cls_for(ft, "need_L")
        VAR[f"{ft}: bracket + f 1.0"] = cls_for(ft, qkey="Q95_ext_f1")
        VAR[f"{ft}: bracket + P6 no-cut (f 0.7, 1.0)"] = cls_for(ft, qkey="Q95_ext_P6")
        VAR[f"{ft}: P1 R1 15 Rsun f 0.5 alone (CFG93 setting)"] = cls_for(ft, qkey="Q95_R15")
        VAR[f"{ft}: single-epoch (no cleaning) Q95 vs CFG861 sig_bin"] = cls_for(ft, "sig_bin_861", "Q95_single")
    for k, v in VAR.items(): P(f"    {k:62s} -> {v[0]}" + (f" (reached: {', '.join(v[1])})" if v[1] else ""))
    for ft in FOOT:
        P(f"    [{ft}] per-dwarf Q95 under the extensions (need / graded Q95 / +f1.0 / +P6 / R15):  " + "; ".join(
            f"{n} {PER[(n, ft)]['needs']['need']:.2f}/{PER[(n, ft)]['Q95']:.2f}/{PER[(n, ft)]['Q95_ext_f1']:.2f}/{PER[(n, ft)]['Q95_ext_P6']:.2f}/{PER[(n, ft)]['Q95_R15']:.2f}" for n in GRADED_NAMES))
    P(f"    other classical systems (reported): " + "; ".join(
        f"{n} [{ft[:3]}] need {PER[(n, ft)]['needs']['need']:.2f} Q95 {PER[(n, ft)]['Q95']:.2f}" for n in OTHER_NAMES for ft in FOOT))
    P("\n  CATCH RATES (median over realizations; graded dwarfs, canonical)  pop: f0.3 / f0.5 / f0.7")
    for d in GR:
        P(f"    {d['name']:12s} " + "  ".join(f"{p}: " + "/".join(f"{CELLS[(d['name'], 'canonical', p, f, 0)]['catch_med']:.3f}" for f in F_GRADED) for p in GRADED_POPS)
          + f"  R15 f0.5: {CELLS[(d['name'], 'canonical', 'P1R15', 0.5, 0)]['catch_med']:.3f}")
    P("  FLAG FRACTION sim (pooled) vs observed n_rm/|M| (diagnostic only)  pop: f0.3 / f0.5 / f0.7 / f1.0")
    for d in GR:
        c = C861S[d["name"]]
        P(f"    {d['name']:12s} obs {c['n_rm'] / c['nM']:.3f} | " + "  ".join(f"{p}: " + "/".join(f"{CELLS[(d['name'], 'canonical', p, f, 0)]['flag_frac_pooled']:.3f}" for f in F_GRADED + (1.0,)) for p in GRADED_POPS)
          + f" | no-binary twin {CELLS[(d['name'], 'canonical', 'P1', 0.5, 0)]['flag_frac0_pooled']:.3f}")
    P(f"  [{time.time() - T0:.0f} s]")

    # ---- binary-only single-epoch dispersion at sigma_true = 0.2 km/s (the McConnachie & Cote-type number)
    P("\n  BINARY-ONLY single-epoch dispersion (sigma_true 0.2 km/s, f 0.7, each graded dwarf's M epochs and errors): sigma_single q50 / q95")
    BO = {}
    for d in GR:
        BO[d["name"]] = {}
        for p in GRADED_POPS:
            a = run_cell(d, 0.2, 0.7, p, (d["si"], POP_IDX[p], f_idx[0.7], 0, 1)); BO[d["name"]][p] = dict(q50=float(np.median(a["ss"])), q95=float(np.quantile(a["ss"], .95)))
        P(f"    {d['name']:12s} |M| {len(d['M']):4d}  " + "  ".join(f"{p} {BO[d['name']][p]['q50']:.2f}/{BO[d['name']][p]['q95']:.2f}" for p in GRADED_POPS))
    P(f"  [{time.time() - T0:.0f} s]")

    # ---- Sextans zero point
    P("\n  SEXTANS INSTRUMENT ZERO POINT")
    dS = SYSD["Sextans"]
    def offset_pair(A, B):
        ds_, es_ = [], []
        for x in dS["ep"]:
            ins = np.array([INSTR[r["file"]] for r in x]); v = np.array([r["Vlos"] for r in x]); e = np.array([r["eVlos"] for r in x])
            if (ins == A).any() and (ins == B).any():
                wa, wb = 1 / e[ins == A] ** 2, 1 / e[ins == B] ** 2
                ds_.append(np.sum(wb * v[ins == B]) / wb.sum() - np.sum(wa * v[ins == A]) / wa.sum()); es_.append(math.sqrt(1 / wa.sum() + 1 / wb.sum()))
        ds_, es_ = np.array(ds_), np.array(es_); keepm = np.ones(len(ds_), bool); off = 0.0
        for _ in range(20):
            w = 1 / es_[keepm] ** 2; off_new = float(np.sum(w * ds_[keepm]) / w.sum())
            km = np.abs(ds_ - off_new) <= 3 * es_
            if np.array_equal(km, keepm) and off_new == off: break
            keepm, off = km, off_new
        w = 1 / es_[keepm] ** 2; off = float(np.sum(w * ds_[keepm]) / w.sum()); chi = float(np.sum(w * (ds_[keepm] - off) ** 2)); dof = max(int(keepm.sum()) - 1, 1)
        err = (1 / math.sqrt(w.sum())) * max(1.0, math.sqrt(chi / dof))
        return dict(offset=off, err=err, n=int(len(ds_)), n_kept=int(keepm.sum()), chi2_dof=chi / dof)
    o01 = offset_pair(0, 1); o12 = offset_pair(1, 2)
    zmeas = np.array([0.0, o01["offset"], o01["offset"] + o12["offset"]])
    P(f"    measured: HiRes - Hectochelle {o01['offset']:+.3f} +- {o01['err']:.3f} km/s (stars {o01['n']}, kept {o01['n_kept']}, chi2/dof {o01['chi2_dof']:.2f});"
      f"  MedRes - HiRes {o12['offset']:+.3f} +- {o12['err']:.3f} (stars {o12['n']}, kept {o12['n_kept']}, chi2/dof {o12['chi2_dof']:.2f});  MedRes - Hecto {zmeas[2]:+.3f}")
    velc = [[r["Vlos"] - zmeas[INSTR[r["file"]]] for r in x] for x in dS["ep"]]
    rz = pipeline_exact(dS, velc, dS["vc"], dS["sig_seed"])
    dz = 2 * math.log10(rz["clean"]["sig"] / rz["single"]["sig"])
    # membership re-run with corrected rows
    rows_c = []
    for r in rows:
        if r["Target"] == dS["target"]:
            r = dict(r); r["Vlos"] = r["Vlos"] - zmeas[INSTR[r["file"]]]
            rows_c.append(r)
    stc = RW.build_stars(rows_c); memc, _, _, _ = RW.membership(stc, dS["lv"]); Mc = {s["gaia"] for s in memc if s["n"] >= 2}; M0 = {s["gaia"] for s in dS["M"]}
    Z1 = dict(offsets=dict(hires_minus_hecto=o01, medres_minus_hires=o12, medres_minus_hecto=float(zmeas[2])),
              sig_single_M=rz["single"]["sig"], sig_clean_M=rz["clean"]["sig"], n_rm=rz["n_rm"], delta=dz, membership_changes=len(Mc ^ M0))
    P(f"    Z1 corrected (same M): sigma_single(M) {rz['single']['sig']:.3f} (was {C861S['Sextans']['sig_single_M']['sig']:.3f}), sigma_clean(M) {rz['clean']['sig']:.3f}"
      f" (was {C861S['Sextans']['sig_clean_M']['sig']:.3f}), removed {rz['n_rm']} (was {C861S['Sextans']['n_rm']}), delta {dz:+.3f} (was {C861S['Sextans']['delta']:+.3f});"
      f" membership re-run changes {len(Mc ^ M0)} M stars")
    for ft in FOOT:
        nd = needs(dS, ft, sc_M=rz["clean"]["sig"], ss_M=rz["single"]["sig"]); x = PER[("Sextans", ft)]
        Z1[ft] = dict(needs=nd, Delta_clean=dS["D"][ft] + dz, Q95=x["Q95"], reached=bool(nd["need"] > 0 and x["Q95"] >= nd["need"]))
        items = [(n, PER[(n, ft)]["needs"]["need"], PER[(n, ft)]["Q95"]) if n != "Sextans" else (n, nd["need"], x["Q95"]) for n in GRADED_NAMES]
        Z1[ft]["class"] = classify(items)
        P(f"    Z1 [{ft}] Delta_clean {dS['D'][ft] + dz:+.3f} (CFG861 {dS['D'][ft] + C861S['Sextans']['delta']:+.3f}); sigma_obs W/L {nd['sig_obs_W']:.2f}/{nd['sig_obs_L']:.2f} -> {nd['sig_obs']:.2f};"
          f" need {nd['need']:.3f} vs Q95 {x['Q95']:.3f} -> {'reached' if Z1[ft]['reached'] else 'not reached'}; class with Z1 Sextans: {Z1[ft]['class'][0]}")
    # Z2 bracket
    Z2 = {}
    for ft in FOOT:
        bestc = PER[("Sextans", ft)]["Q95_cell"]; ndg = needs(dS, ft)
        zlist = [("x0.5", [0, 0.5, -0.5]), ("x1", [0, 1, -1]), ("x2", [0, 2, -2]), ("x3", [0, 3, -3]), ("measured", list(zmeas))]
        Z2[ft] = {}
        for zi, (zn, zv) in enumerate(zlist):
            for (p, f) in (bestc, ("P1", 0.5)):
                s = cell(dS, ft, p, f, var=10 + zi, zoff=zv)
                Z2[ft][f"{zn}|{p}|{f}"] = dict(zoff=[float(v) for v in zv], ex_clean_q95=s["ex_clean_q95"], flag_frac=s["flag_frac_pooled"], delta_q50=s["delta_q50"],
                                              reached=bool(ndg["need"] > 0 and s["ex_clean_q95"] >= ndg["need"]), P_sc_ge_obs=s["P_sc_ge_obs"])
        P(f"    Z2 [{ft}] need {ndg['need']:.3f} (uncorrected); most generous cell {bestc}: " + "; ".join(
            f"{k.split('|')[0]} {v['ex_clean_q95']:.2f} (flag {v['flag_frac']:.3f}, delta {v['delta_q50']:+.3f})" for k, v in Z2[ft].items() if k.split('|')[1] == bestc[0] and float(k.split('|')[2]) == bestc[1])
          + " | P1 f0.5: " + "; ".join(f"{k.split('|')[0]} {v['ex_clean_q95']:.2f} (flag {v['flag_frac']:.3f})" for k, v in Z2[ft].items() if k.split('|')[1] == "P1" and float(k.split('|')[2]) == 0.5))
        P(f"    Z2 [{ft}] any offset reaches Sextans' need: {any(v['reached'] for v in Z2[ft].values())}")
    P(f"  [{time.time() - T0:.0f} s, max RSS {rss_mb():.0f} MB]")
    P(f"\n  CLASS (canonical, graded): {CLS['canonical'][0]}" + (f" (reached: {', '.join(CLS['canonical'][1])})" if CLS['canonical'][1] else "")
      + f";  alt footing: {CLS['alt'][0]};  K1 {'PASS' if k1ok else 'FAIL'}, K1b {'PASS' if k1bok else 'FAIL'}, K2 {'PASS' if k2ok else 'FAIL'}, K3 {'PASS' if k3ok else 'FAIL'}")
    RES = dict(lane="CFG892", criteria_commit="5b5da1665", mutate=False, R=R, populations=POPS, graded_dwarfs=GRADED_NAMES,
               per_dwarf={f"{k[0]}|{k[1]}": v for k, v in PER.items()}, cls={ft: dict(cls=CLS[ft][0], reached=CLS[ft][1]) for ft in FOOT},
               variants={k: dict(cls=v[0], reached=v[1]) for k, v in VAR.items()}, binary_only=BO, sextans_Z1=Z1, sextans_Z2=Z2,
               cells={"|".join(map(str, k)): v for k, v in CELLS.items()}, K1=dict(passed=bool(k1ok), systems=K1), K1b=dict(passed=bool(k1bok), max_diff=k1bmax, systems=K1B),
               K2=dict(passed=bool(k2ok), systems=K2), K3=dict(passed=bool(k3ok), kconst_rel=abs(KCONST / kc - 1), kepler_residual=k3d))
P(f"  runtime {time.time() - T0:.0f} s, max RSS {rss_mb():.0f} MB")

def clean_json(o):
    if isinstance(o, dict): return {str(k): clean_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean_json(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
sfx = "_MUTATE" if MUT else ""
json.dump(clean_json(RES), open(os.path.join(HERE, f"cfg892_results{sfx}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg892{sfx}.out"), "w").write("\n".join(OUT) + "\n")
