#!/usr/bin/env python3
"""LE1_lensing_estimator_audit (FROZEN_CRITERIA.md). Reads graders, never edits them.
  PYTHONHASHSEED=0 nice -n 10 python3 -I le1.py controls      G1/G2-projector/G3 known answers, R1, R3, MUT for G1 and G3
  PYTHONHASHSEED=0 nice -n 10 python3 -I le1.py keys_controls R2, KA2c (replica), MUT for G2 (key chain runs, cache_keys/)
  PYTHONHASHSEED=0 nice -n 10 python3 -I le1.py real          G1 base + swap ladder S1-S7 + A1, G3 (+ mapped variant), law / NP1 real L3 / Newton
  PYTHONHASHSEED=0 nice -n 10 python3 -I le1.py keys_real     G2 base, K1 no miscentring, K2 no reduced shear, law and NP1 real L3
  PYTHONHASHSEED=0 nice -n 10 python3 -I le1.py verdict       label from the four JSONs
Outputs le1_<mode>.{json,out}. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import importlib.util, json, math, os, subprocess, sys, types
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True; os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import numpy as np
from scipy.integrate import quad
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CRG = os.path.join(RB, "CRG1_clean_room_regrade"); RQ3 = os.path.join(RB, "RQ3_acceptance_v2"); NP1 = os.path.join(RB, "NP1_nonparametric_rule")
MODE = sys.argv[1] if len(sys.argv) > 1 else "controls"
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt"); ZL = 2.0
OUT = []; RES = {"lane": "LE1_lensing_estimator_audit", "mode": MODE}
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def save():
    json.dump(RES, open(os.path.join(HERE, f"le1_{MODE}.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"le1_{MODE}.out"), "w").write("\n".join(OUT) + "\n")
def zchi(c, dof): return (c - dof) / math.sqrt(2 * dof)

# ---------- CRG1 core patched to read its inputs and write only into this lane's cache_crg (as RQ3 does, own dirs)
def crg():
    if "crg1_core" in sys.modules: return
    p = os.path.join(CRG, "v1", "crg1_core.py"); s = open(p).read()
    for a, b in (('INP = os.path.join(HERE, "inputs")', f'INP = {os.path.join(CRG, "inputs")!r}'),
                 ('PART = os.path.join(HERE, os.environ.get("CRG1_PARTIALS", "partials"))', f'PART = {os.path.join(HERE, "cache_crg", "p")!r}'),
                 ('CACHE = os.path.join(HERE, os.environ.get("CRG1_CACHE", "cache"))', f'CACHE = {os.path.join(HERE, "cache_crg", "c")!r}')):
        assert s.count(a) == 1, a; s = s.replace(a, b)
    m = types.ModuleType("crg1_core"); m.__file__ = p; sys.modules["crg1_core"] = m; exec(compile(s, p, "exec"), m.__dict__); sys.path.insert(0, os.path.join(CRG, "v1"))
crg()
_sp = importlib.util.spec_from_file_location("rq3acc", os.path.join(RQ3, "acceptance.py")); ACC = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(ACC)
import crg1_lens as Le
def cand(path):
    sp = importlib.util.spec_from_file_location("cand_" + os.path.basename(path)[:-3], path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
CANDS = {"law": os.path.join(RQ3, "candidates", "law.py"), "newton": os.path.join(RQ3, "candidates", "newton.py"), "np1_L3": os.path.join(NP1, "candidates", "np1_real_L3.py"),
         "law_x2": os.path.join(HERE, "candidates", "le1_law_x2.py")}
RGRID = Le.RGRID; SIk = 1e6 / 3.0857e16; REX = [.343, .442, .433, .429]

# ============================================================== G1: RQ3 A30 (CRG1 Ln) and its swaps
_TH = {}
class G1:
    def __init__(s, native=True):
        L = Le.load(); s.native = native
        if not native:
            d = np.load(os.path.join(CRG, "inputs", "lensing", "lens_inventory.npz")); lm = d["logM"]; w = d["WLENS"]; bins = np.digitize(lm, [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1
            Wg = np.zeros((4, len(Le.LMG))); dl = Le.LMG[1] - Le.LMG[0]; lens = []
            for b in range(4):
                sb = bins == b; li = lm[sb]; wb = w[sb]; t = np.clip((li - Le.LMG[0]) / dl, 0, len(Le.LMG) - 1 - 1e-12); k = t.astype(int); fr = t - k
                np.add.at(Wg[b], k, wb * (1 - fr)); np.add.at(Wg[b], k + 1, wb * fr); Wg[b] /= wb.sum(); lens.append((li, wb))
            L = dict(L, Rn=L["R"].copy(), Yn=L["Y"].copy(), Cn=L["C"].copy(), Wg=Wg, lens=lens)
        s.L = L; s.st = Le.Stencil(L["Rn"] * 1e6)
        if "th" not in _TH: _TH["th"] = Le.TwoHalo(Le.load())
        s.T0 = np.array([_TH["th"].esd2h(L["R"][b], REX[b]) * (Le.FF if native else 1.0) for b in range(4)])
        s.IP = [j for j in range(15) if L["R"][0][j] <= 0.31]
        s.lme = [math.log10(float(np.sum(wb * 10 ** li) / np.sum(wb))) for li, wb in L["lens"]]
    def table(s, c, foot, bary="A30"):
        Tb = np.zeros((len(Le.LMG), 60)); a0 = A0[foot]
        for i, lm in enumerate(Le.LMG):
            if bary == "A30": MB, _ = Le.baryon(float(lm)); gg = Le.Gpc * (MB - 10 ** float(lm)) / RGRID ** 2
            else: Ms = 10 ** float(lm); MB = 1.25 * Ms * np.ones_like(RGRID); gg = Le.Gpc * 0.25 * Ms / RGRID ** 2
            gb = Le.Gpc * MB / RGRID ** 2
            v = ACC.call(c, gb=gb * SIk, gg=gg * SIk, gs=(gb - gg) * SIk, r=RGRID * 3.0857e16, a0=a0, sample="lens"); Tb[i] = s.st.dsig(MB * v / (gb * SIk), "linear")
        return Tb
    def model(s, Tb, single=False):
        if not single: return Le.stack(s.L, Tb)
        t = Tb.reshape(len(Le.LMG), 4, 15); return np.concatenate([np.array([np.interp(s.lme[b], Le.LMG, t[:, b, j]) for j in range(15)]) for b in range(4)])
    def grade(s, m, prim=False, twoh=True, diag=False):
        L = s.L if not diag else dict(s.L, Cn=np.diag(np.diag(s.L["Cn"])))
        idx = s.IP if prim else list(range(15)); T = s.T0 if twoh else np.zeros_like(s.T0)
        ch, b = Le.fit(L, m, idx, T); dof = 4 * len(idx) - (4 if twoh else 0); return dict(chi2=float(ch), dof=dof, Z=float(zchi(ch, dof)), b=[float(x) for x in b])
    def amp(s, m, rows=None):
        """G3's statistic on G1's model: inverse-variance mean of log10(Y/model), diagonal sigma, R <= 0.31 (A1)."""
        idx = Le.sel(s.IP); y = s.L["Yn"].ravel()[idx]; mm = m[idx]; sg = np.sqrt(np.diag(s.L["Cn"]))[idx]; ok = (y > 0) & (mm > 0)
        d = np.log10(y[ok] / mm[ok]); w = (y[ok] * math.log(10) / sg[ok]) ** 2; mu = float((w * d).sum() / w.sum()); se = float(1 / math.sqrt(w.sum())); return dict(mean=mu, se=se, z=mu / se, n=int(ok.sum()))

# ============================================================== G2 projector (F1's functions + X2's floored projector, exec'd read-only as X2/X30 do)
def g2_ns():
    F1 = open(os.path.join(RB, "F1_cluster_cores", "f1_cluster_cores.py")).read(); X2 = open(os.path.join(RB, "X2_cluster_outskirts", "x2_cluster_outskirts.py")).read()
    def cut(t, a, b): i = t.index(a); j = t.index(b, i); return t[i:j]
    from scipy.interpolate import PchipInterpolator
    N = {"np": np, "os": os, "sys": sys, "REPO": os.path.dirname(RB), "_trap": np.trapz, "PchipInterpolator": PchipInterpolator, "math": math}
    exec(cut(F1, "G = 6.674e-11", "# ---------------------------------------------------------------- sources"), N)
    exec(cut(F1, "EDGES = np.logspace", "def gather("), N); exec(cut(F1, "RG = np.logspace(-3", "# SIS self-test (K4)"), N)
    exec(cut(X2, "def project_floor(", "# ============================================================== gas profiles"), N); return N

# ============================================================== G3: CX1's lensing line through NP1's cx_rows
def g3_rows(foot):
    sys.path.insert(0, NP1); import np1_core as NC
    R = [q for q in NC.cx_rows(foot) if q["line"] == "L"]; C = sys.modules["cx1_rows"]; return R, NC, C
def g3_z(R, NC, foot, c=None, gmodel=None):
    """d = log10(g_obs / g_model) per L row; g_model = candidate g (default) or a supplied array; NP1's weighted mean and z."""
    a0 = A0[foot]; y = np.array([q["y"] for q in R]); ell = np.array([q["ell"] for q in R]); f = np.array([q["f"] for q in R]); lb = np.array([q["logB"] for q in R]); sd = np.array([q["sd"] for q in R])
    gb = y * NC.A0C; r = ell * NC.CL ** 2 / NC.A0C; gobs = 10 ** lb * NC.law(gb, NC.FOOT[foot])
    gm = gmodel if gmodel is not None else ACC.call(c, gb=gb, gg=f * gb, gs=(1 - f) * gb, r=r, a0=NC.FOOT[foot], sample="lens")
    d = np.log10(gobs / gm); w = 1 / sd ** 2; mu = float((w * d).sum() / w.sum()); se = float(1 / math.sqrt(w.sum())); return dict(mean=mu, se=se, z=mu / se, n=len(d), label="PASS" if abs(mu / se) <= ZL else "FAIL")
def cx1_masses():
    d = np.load(os.path.join(CRG, "inputs", "lensing", "lens_inventory.npz")); bins = np.digitize(d["logM"], [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1
    return [float(np.average(10 ** d["logM"][bins == b], weights=d["WLENS"][bins == b])) for b in range(4)]
def g3_lens_gmodel(R, NC, C, foot, c):
    """4 G DeltaSigma of the model's own spherical lensing mass on CX1's baryons (M* + 0.25 M*), at each L row: the conversion's known answer."""
    Ms = cx1_masses(); out = np.zeros(len(R)); a0 = A0[foot]
    for b in range(4):
        idx = [i for i, q in enumerate(R) if q["name"] == f"bin{b + 1}"]
        if not idx: continue
        Rpc = np.array([R[i]["ell"] * NC.CL ** 2 / NC.A0C / C.PC for i in idx]); st = Le.Stencil(Rpc); MB = 1.25 * Ms[b]; gb = Le.Gpc * MB / RGRID ** 2
        v = ACC.call(c, gb=gb * SIk, gg=0.2 * gb * SIk, gs=0.8 * gb * SIk, r=RGRID * 3.0857e16, a0=a0, sample="lens"); ds = st.dsig(MB * v / (gb * SIk), "linear")
        out[idx] = 4 * C.G * ds * C.MS / C.PC ** 2
    return out

# ============================================================== analytic profiles
def nfw_pars(M200, c, h=0.7):
    rc = 2.775e11 * h ** 2; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3); rs = R200 / c; rhos = M200 / (4 * math.pi * rs ** 3 * (math.log(1 + c) - c / (1 + c))); return rs, rhos   # Msun, Mpc
def nfw_M(r, rs, rhos): x = r / rs; return 4 * math.pi * rhos * rs ** 3 * (np.log(1 + x) - x / (1 + x))
def nfw_ds(R, rs, rhos):
    x = np.asarray(R, float) / rs; out = np.empty_like(x)
    for i, xi in enumerate(x):
        if xi < 1: F = 2 / math.sqrt(1 - xi * xi) * math.atanh(math.sqrt((1 - xi) / (1 + xi)))
        elif xi > 1: F = 2 / math.sqrt(xi * xi - 1) * math.atan(math.sqrt((xi - 1) / (1 + xi)))
        else: F = 1.0
        Sig = 2 * rs * rhos / (xi * xi - 1) * (1 - F) if abs(xi - 1) > 1e-9 else 2 * rs * rhos / 3; Sbar = 4 * rs * rhos / xi ** 2 * (F + math.log(xi / 2)); out[i] = Sbar - Sig
    return out
def trunc_ds(rho, R, rt):
    """DeltaSigma of a sphere truncated at rt, independent quadrature (any units consistent)."""
    out = []
    for Rv in np.atleast_1d(R):
        Sig = 2 * quad(lambda u: rho(math.sqrt(Rv * Rv + u * u)), 0, math.sqrt(rt * rt - Rv * Rv), limit=400, epsabs=0)[0]
        Mtot = quad(lambda r: 4 * math.pi * r * r * rho(r), 0, rt, limit=400, points=[Rv], epsabs=0)[0]
        Mout = quad(lambda r: 4 * math.pi * r * r * rho(r) * math.sqrt(1 - Rv * Rv / (r * r)), Rv, rt, limit=400, epsabs=0)[0]
        out.append((Mtot - Mout) / (math.pi * Rv * Rv) - Sig)
    return np.array(out)

# ============================================================== key chain (RQ3's run_keys, own cache, HERE -> run dir, swap hook)
HOOK = '''_LE1SW = os.environ.get("LE1_KSWAP", "base")
if _LE1SW != "base":
    def dvecN(i, foot, hk, Msrc):
        pp = prep(i, foot, hk); rho = np.gradient(Msrc, RM) / (4 * np.pi * RM ** 2)
        So = O_(P_(rho), 0.0 if _LE1SW == "nomis" else pp["dmpc"]); Pp = A_(DS_(So)) / KG
        fr = np.ones_like(Pp) if _LE1SW == "nored" else RF(hk, i, SB(So))[0]
        return DAT[hk]["W"][i] * (Pp * fr)
'''
KTAGS = (("g005_f034", .005, "0.034"), ("g005_f0615", .005, "0.0615"))
KS = ACC.KS; HH = ACC.HH
def keys_run(name, swap):
    L, T = ACC.keys_tail(); a = "_LAW = dict(on=False"; assert T.count(a) == 1; T = T.replace(a, HOOK + a); res = {}
    for tag, dex, fs in KTAGS:
        W = os.path.join(HERE, "cache_keys", f"{name}_{swap}_{tag}"); os.makedirs(W, exist_ok=True); O = os.path.join(W, "keys.json")
        if not (os.path.exists(O) and json.load(open(O)).get("done")):
            TL = os.path.join(W, "tail.py"); open(TL, "w").write(T); d = open(os.path.join(L.SL1, "sl1_harvest.py")).read()
            for x, y in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(L.GAS % dex if dex else "") + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'),
                         ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {W!r}; RB = {RB!r}'), ('X73_FSTAR="0.034"', f'X73_FSTAR="{fs}"')):
                assert d.count(x) == 1, x; d = d.replace(x, y)
            df = os.path.join(W, "driver.py"); open(df, "w").write(d)
            env = dict(os.environ, UR1_SL1=L.SL1, SL1_OUT=O, CN1_FORCE="1", LW1_A0X="1.0", RQ2_CAND=os.path.abspath(CANDS[name]), DR1_RUN=json.dumps(dict(rows=L.ROWS, k2=False)), LE1_KSWAP=swap, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
            subprocess.run(["nice", "-n", "10", sys.executable, "-B", df], env=env, stdout=open(os.path.join(W, "run.log"), "w"), stderr=subprocess.STDOUT)
        if not os.path.exists(O) or not json.load(open(O)).get("done"): P(f"  keys {name} {swap} {tag}: NOT COMPUTABLE (run did not finish)"); return None
        res[tag] = json.load(open(O))
    return res
def keys_rows(K, foot):
    """RQ3's rows_keys B4-B18: worst Z over both h and both f*."""
    o = {}; rk = f"R1|c0|{foot}"
    for i, k in enumerate(KS):
        vals = [K[t][rk]["Z"][h][k] for t, _, _ in KTAGS for h in HH]; w = max(vals, key=abs); o[k] = dict(Z=float(w), label="PASS" if max(abs(v) for v in vals) <= ZL else "FAIL", pred=float(K["g005_f034"][rk]["preds"]["h0672"][k]))
    return o
def keys_summary(o): return dict(nfail=sum(v["label"] == "FAIL" for v in o.values()), fails=[k for k, v in o.items() if v["label"] == "FAIL"])

# ============================================================== modes
def controls():
    P("LE1 controls: known answers, reproduction, MUTATE. kappa = 1/2 FITTED; not theory closed.")
    # KA1a Stencil
    g = G1(True); Rpc = g.L["Rn"].ravel() * 1e6; st = Le.Stencil(Rpc); sig = 150.0
    sis = st.dsig(2 * sig ** 2 * RGRID / Le.Gpc, "linear") / (sig ** 2 / (2 * Le.Gpc * Rpc))
    pm = st.dsig(np.full_like(RGRID, 1e11), "const") / (1e11 / (math.pi * Rpc ** 2))
    rs, rhos = nfw_pars(1e12, 8.0, 0.679); nf = st.dsig(nfw_M(RGRID / 1e6, rs, rhos), "linear") / (nfw_ds(Rpc / 1e6, rs, rhos) / 1e12)
    ka1a = {k: float(np.max(np.abs(v - 1))) for k, v in (("SIS", sis), ("point", pm), ("NFW", nf))}; ok1a = max(ka1a.values()) <= 0.01
    P(f"KA1a G1 Stencil vs closed forms, max |ratio-1|: {json.dumps({k: round(v, 6) for k, v in ka1a.items()})} -> {'PASS' if ok1a else 'FAIL'}")
    # KA1b/c self-recovery, chi2 calibration
    c = cand(CANDS["law"]); Tb = g.table(c, "canonical"); m = g.model(Tb); bt = np.array([0, 0, .15, .07]); Af = np.zeros((60, 4))
    for b in range(4): Af[15 * b:15 * (b + 1), b] = g.T0[b]
    Lm = dict(g.L, Yn=(m + Af @ bt).reshape(4, 15)); ch, bb = Le.fit(Lm, m, list(range(15)), g.T0); ok1b = ch <= 1e-6 and float(np.max(np.abs(bb - bt))) <= 1e-4
    P(f"KA1b G1 noise-free self-recovery: chi2 {ch:.2e}, max |b - b_true| {float(np.max(np.abs(bb - bt))):.2e} -> {'PASS' if ok1b else 'FAIL'}")
    rng = np.random.default_rng(20261103); Lc = np.linalg.cholesky(g.L["Cn"]); chs = []
    for _ in range(300): chs.append(Le.fit(dict(g.L, Yn=(m + Af @ bt + Lc @ rng.standard_normal(60)).reshape(4, 15)), m, list(range(15)), g.T0)[0])
    mc = float(np.mean(chs)); ok1c = 52 <= mc <= 60; P(f"KA1c G1 chi2 calibration, 300 mocks: mean {mc:.2f}, sd {float(np.std(chs)):.2f} (line [52, 60]) -> {'PASS' if ok1c else 'FAIL'}")
    # KA1d covariance assembly
    cv = np.loadtxt(os.path.join(CRG, "inputs", "lensing", "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#"); u0 = np.unique(cv[:, 0]); u1 = np.unique(cv[:, 1])
    mm = np.searchsorted(u0, cv[:, 0]); nn = np.searchsorted(u1, cv[:, 1]); R0 = g.L["R"][0]; ii = np.abs(R0[None, :] - cv[:, 2][:, None]).argmin(1); jj = np.abs(R0[None, :] - cv[:, 3][:, None]).argmin(1)
    cell = 15 * mm + ii, 15 * nn + jj; cnt = np.zeros((60, 60), int); np.add.at(cnt, cell, 1); C = g.L["C"]
    sym = float(np.max(np.abs(C - C.T)) / np.max(np.abs(C))); pd = bool(np.all(np.linalg.eigvalsh(C) > 0)); rad = float(np.max(np.abs(g.L["R"] / g.L["R"][0][None, :] - 1)))
    rmis = float(np.max(np.abs(R0[ii] / cv[:, 2] - 1))); ok1d = bool(cnt.min() == 1 and cnt.max() == 1 and sym <= 1e-10 and pd and rad <= 1e-6)
    P(f"KA1d covariance assembly: cells filled once {cnt.min()}..{cnt.max()}, asym {sym:.1e}, pos. def. {pd}, bin radii max rel diff {rad:.1e}, cov-radius match max rel {rmis:.1e} -> {'PASS' if ok1d else 'FAIL'}")
    # KA1e cross ESD against the covariance
    X = np.array([np.loadtxt(os.path.join(CRG, "inputs", "lensing", f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"), comments="#") for b in range(1, 5)]); ex = (X[:, :, 2] / X[:, :, 4]).ravel()
    cx60 = float(ex @ np.linalg.solve(C, ex)); sp = Le.sel(g.IP); cx32 = float(ex[sp] @ np.linalg.solve(C[np.ix_(sp, sp)], ex[sp])); n32 = len(sp)
    lo60, hi60 = 60 - 3 * math.sqrt(120), 60 + 3 * math.sqrt(120); lo32, hi32 = n32 - 3 * math.sqrt(2 * n32), n32 + 3 * math.sqrt(2 * n32)
    perbin = [float(ex[15 * b:15 * b + 15] @ np.linalg.solve(C[15 * b:15 * b + 15, 15 * b:15 * b + 15], ex[15 * b:15 * b + 15])) for b in range(4)]
    ok1e = lo60 <= cx60 <= hi60 and lo32 <= cx32 <= hi32
    P(f"KA1e cross ESD vs covariance: chi2_x {cx60:.1f}/60 [{lo60:.1f}, {hi60:.1f}], R <= 0.31 {cx32:.1f}/{n32} [{lo32:.1f}, {hi32:.1f}]; per bin {[round(x, 1) for x in perbin]} -> {'PASS' if ok1e else 'FAIL'}")
    # KA2a/b G2 projector
    N = g2_ns(); RG, RF, RC, MPC, G, KG = N["RG"], N["RF"], N["RC"], N["MPC"], N["G"], N["KG_PC2"]; pf, of, dfs, ab = N["project_floor"], N["offset_floor"], N["dsig_from_sig"], N["at_bins"]
    s_ = 1e6; rho_sis = s_ ** 2 / (2 * math.pi * G * (RG * MPC) ** 2); k_sis = ab(dfs(pf(rho_sis))) / (s_ ** 2 / (2 * G * RC * MPC))
    rs2, rh2 = nfw_pars(1e14, 4.0, 0.7); rt = float(RG[-1]); rho_n = lambda r: rh2 / ((r / rs2) * (1 + r / rs2) ** 2)
    MS = N["MSUN"]; rhoN = np.where(RG <= rt, rho_n(RG), 0) * MS / MPC ** 3; ref_n = trunc_ds(rho_n, RC, rt) * MS / MPC ** 2; k_nfw = ab(dfs(pf(rhoN))) / ref_n
    ap, Mp = 0.01, 1e14; rho_p = 3 * Mp / (4 * math.pi * ap ** 3) * (1 + (RG / ap) ** 2) ** -2.5 * MS / MPC ** 3; ref_p = (Mp / (math.pi * (ap ** 2 + RC ** 2)) - Mp * ap ** 2 / (math.pi * (ap ** 2 + RC ** 2) ** 2)) * MS / MPC ** 2
    k_pl = ab(dfs(pf(rho_p))) / ref_p
    ka2a = {"SIS": [float(x) for x in k_sis], "NFW": [float(x) for x in k_nfw], "Plummer": [float(x) for x in k_pl]}; dev2a = {k: float(np.max(np.abs(np.array(v) - 1))) for k, v in ka2a.items()}; ok2a = max(dev2a.values()) <= 0.01
    P(f"KA2a G2 projector at 8 bins, ratio to closed form: " + "; ".join(f"{k} {np.round(v, 4).tolist()}" for k, v in ka2a.items()) + f" -> max dev {json.dumps({k: round(v, 5) for k, v in dev2a.items()})} {'PASS' if ok2a else 'FAIL'}")
    Sg = s_ ** 2 / (2 * G * RF * MPC); ka2b = {}
    for dd in (0.05, 0.2):
        ref = np.array([quad(lambda ph: s_ ** 2 / (2 * G * MPC * math.sqrt(R * R + dd * dd + 2 * R * dd * math.cos(ph))), 0, math.pi, limit=500)[0] / math.pi for R in RF])
        ka2b[str(dd)] = [float(x) for x in ab(dfs(of(Sg, dd))) / ab(dfs(ref))]
    dev2b = max(float(np.max(np.abs(np.array(v) - 1))) for v in ka2b.values()); ok2b = dev2b <= 0.01
    P(f"KA2b G2 offset_floor vs direct phi-average (SIS): " + "; ".join(f"d {k}: {np.round(v, 4).tolist()}" for k, v in ka2b.items()) + f" -> max dev {dev2b:.4f} {'PASS' if ok2b else 'FAIL'}")
    # KA3 G3 conversion
    ka3b = st.dsig(2 * sig ** 2 * RGRID / Le.Gpc, "linear") * 4 * Le.Gpc / (2 * sig ** 2 / Rpc); dev3b = float(np.max(np.abs(ka3b - 1))); ok3b = dev3b <= 1e-3
    P(f"KA3b G3 SIS: max |4 G DeltaSigma / g - 1| {dev3b:.2e} -> {'PASS' if ok3b else 'FAIL'}")
    G3 = {}; R3 = {}; ka3a = {}
    for f in FEET:
        R, NC, C3 = g3_rows(f); law_c = cand(CANDS["law"]); g4 = g3_lens_gmodel(R, NC, C3, f, law_c)
        y = np.array([q["y"] for q in R]); gb = y * NC.A0C; glaw = NC.law(gb, NC.FOOT[f]); sd = np.array([q["sd"] for q in R]); lr = np.log10(g4 / glaw); w = 1 / sd ** 2
        mu = float((w * lr).sum() / w.sum()); rowsr = [dict(bin=q["name"], R_kpc=float(q["ell"] * NC.CL ** 2 / NC.A0C / C3.PC / 1e3), log_ratio=float(x)) for q, x in zip(R, lr)]
        ka3a[f] = dict(wmean_log_ratio=mu, max_abs=float(np.max(np.abs(lr))), rows=rowsr, ok=abs(mu) <= 0.02)
        P(f"KA3a G3 conversion [{f}]: law on CX1 baryons, 4 G DeltaSigma / g_law: weighted mean log10 {mu:+.4f}, max |row| {float(np.max(np.abs(lr))):.4f} (line 0.02) -> {'PASS' if abs(mu) <= 0.02 else 'FAIL'}")
        P("   by row (bin, R kpc, log ratio): " + "; ".join(f"{r_['bin']} {r_['R_kpc']:.0f} {r_['log_ratio']:+.3f}" for r_ in rowsr))
        G3[f] = {k: g3_z(R, NC, f, cand(CANDS[k])) for k in ("law", "np1_L3")}
        R3[f] = dict(z=G3[f]["np1_L3"]["z"], ref={"canonical": 1.6864242477836013, "alt": 0.9180395923631183}[f]); R3[f]["ok"] = abs(R3[f]["z"] - R3[f]["ref"]) <= 0.01
        P(f"R3 [{f}] NP1 real L3 G3 lensing z {R3[f]['z']:+.4f} (record {R3[f]['ref']:+.4f}) -> {'PASS' if R3[f]['ok'] else 'FAIL'}; law z {G3[f]['law']['z']:+.3f}")
        mu_ = G3[f]["law"]; P(f"MUT G3 [{f}]: g_obs/2 moves law z {mu_['z']:+.2f} -> {(mu_['mean'] - math.log10(2)) / mu_['se']:+.2f} (needs |dz| >= {math.log10(2) / mu_['se']:.1f})")
    # R1 and MUT G1
    R1 = {}; refs = {("law", "canonical"): 9.27416886540268, ("law", "alt"): None, ("np1_L3", "canonical"): None, ("np1_L3", "alt"): None}
    rec = {("law", f): json.load(open(os.path.join(RQ3, "results", "law.json")))["footings"][f]["rows"]["A30"]["Z"] for f in FEET}
    rec.update({("np1_L3", f): json.load(open(os.path.join(NP1, "results", "np1_real_L3.json")))["footings"][f]["rows"]["A30"]["Z"] for f in FEET})
    mut = {}
    for k in ("law", "np1_L3"):
        c = cand(CANDS[k])
        for f in FEET:
            a = ACC.rows_lens(c, f)["A30"]; mine = g.grade(g.model(g.table(c, f))); ok = abs(a["Z"] - rec[(k, f)]) <= 0.01 and abs(mine["Z"] - a["Z"]) <= 1e-9
            R1[f"{k}|{f}"] = dict(rq3_path=a["Z"], lane_path=mine["Z"], record=rec[(k, f)], chi2=mine["chi2"], ok=ok)
            P(f"R1 {k} [{f}]: RQ3 rows_lens Z {a['Z']:+.4f}, this lane's G1 {mine['Z']:+.4f} (chi2 {mine['chi2']:.1f}), record {rec[(k, f)]:+.4f} -> {'PASS' if ok else 'FAIL'}")
            if k == "law":
                m2 = g.grade(2 * g.model(g.table(c, f))); mut[f] = dict(chi2=m2["chi2"], dchi2=m2["chi2"] - mine["chi2"], ok=m2["chi2"] - mine["chi2"] >= 50)
                P(f"MUT G1 [{f}]: model DeltaSigma x 2: chi2 {mine['chi2']:.1f} -> {m2['chi2']:.1f} -> {'BITES' if mut[f]['ok'] else 'DOES NOT BITE'}")
    RES.update(KA1a=dict(dev=ka1a, ok=ok1a), KA1b=dict(chi2=float(ch), ok=ok1b), KA1c=dict(mean=mc, sd=float(np.std(chs)), ok=ok1c), KA1d=dict(ok=ok1d, asym=sym, posdef=pd), KA1e=dict(chi2_60=cx60, chi2_32=cx32, n32=n32, perbin=perbin, ok=ok1e),
               KA2a=dict(ratios=ka2a, dev=dev2a, ok=ok2a), KA2b=dict(ratios=ka2b, dev=dev2b, ok=ok2b), KA3a=ka3a, KA3b=dict(dev=dev3b, ok=ok3b), R1=R1, R3=R3, G3_base=G3, MUT_G1=mut)
    save()

def real():
    P("LE1 real: G1 base + swaps, A1, G3 (+ mapped), law / NP1 real L3 / Newton. kappa = 1/2 FITTED; not theory closed.")
    gn, gr = G1(True), G1(False); out = {}
    for k in ("law", "np1_L3", "newton"):
        c = cand(CANDS[k]); out[k] = {}
        for f in FEET:
            TA = gn.table(c, f); TC = gn.table(c, f, "CX1"); TAr = gr.table(c, f); TCr = gr.table(c, f, "CX1"); mA = gn.model(TA); o = {}
            o["S0 base"] = gn.grade(mA); o["S1 R<=0.31"] = gn.grade(mA, prim=True); o["S2 no two-halo"] = gn.grade(mA, twoh=False); o["S3 CX1 baryons"] = gn.grade(gn.model(TC))
            o["S4 diagonal cov"] = gn.grade(mA, diag=True); o["S5 no native conversion"] = gr.grade(gr.model(TAr)); o["S6 one mass per bin"] = gn.grade(gn.model(TA, True))
            o["S7 all CX1-like"] = gr.grade(gr.model(TCr, True), prim=True, twoh=False, diag=True)
            o["A1 G1 model, G3 statistic"] = gn.amp(mA); o["A1 raw, CX1 baryons, one mass"] = gr.amp(gr.model(TCr, True))
            o["S1+S2 R<=0.31, no two-halo"] = gn.grade(mA, prim=True, twoh=False)
            out[k][f] = o
            P(f"\n[{k} | {f}] G1 swap ladder (Z = (chi2 - dof)/sqrt(2 dof)):")
            for nm, v in o.items():
                if "chi2" in v: P(f"   {nm:32s} chi2 {v['chi2']:8.1f}/{v['dof']:3d}  Z {v['Z']:+7.2f}  {'PASS' if abs(v['Z']) <= ZL else 'FAIL'}  b {np.round(v['b'], 3).tolist()}")
                else: P(f"   {nm:32s} mean log10(Y/model) {v['mean']:+.4f} +- {v['se']:.4f}  z {v['z']:+.2f}  n {v['n']}")
    g3 = {}
    for f in FEET:
        R, NC, C3 = g3_rows(f); g3[f] = {}
        for k in ("law", "np1_L3", "newton"):
            c = cand(CANDS[k]); b_ = g3_z(R, NC, f, c); mp = g3_z(R, NC, f, gmodel=g3_lens_gmodel(R, NC, C3, f, c)); g3[f][k] = dict(base=b_, mapped_4GDS=mp)
            P(f"G3 [{f}] {k}: z {b_['z']:+.2f} (mean {b_['mean']:+.4f} +- {b_['se']:.4f}) {b_['label']}; model mapped to 4 G DeltaSigma: z {mp['z']:+.2f} {mp['label']}")
    RES.update(G1=out, G3=g3); save()

def keys_controls():
    P("LE1 keys controls: R2 (law base vs RQ3's cache), KA2c (replica hook), MUT (g x 2). kappa = 1/2 FITTED; not theory closed.")
    base = keys_run("law", "base"); rep = keys_run("law", "replica"); mu = keys_run("law_x2", "base"); R = {}
    if base is None: P("R2: NOT COMPUTABLE"); RES["R2"] = dict(ok=False); save(); return
    d = 0.0
    for tag, _, _ in KTAGS:
        ref = json.load(open(os.path.join(RQ3, "cache_keys", f"law_{tag}", "keys.json")))
        for f in FEET:
            for h in HH:
                for k in KS: d = max(d, abs(base[tag][f"R1|c0|{f}"]["Z"][h][k] - ref[f"R1|c0|{f}"]["Z"][h][k]))
    LJ = json.load(open(os.path.join(RQ3, "results", "law.json"))); d2 = 0.0; rows = {}
    for f in FEET:
        rows[f] = keys_rows(base, f)
        for i, k in enumerate(KS): d2 = max(d2, abs(rows[f][k]["Z"] - LJ["footings"][f]["rows"][f"B{i + 4}:{k}"]["Z"]))
    ok2 = d <= 1e-6 and d2 <= 1e-6; P(f"R2 law keys: max |dZ| vs RQ3 cache {d:.1e}, worst-cell rows vs law.json {d2:.1e} -> {'PASS' if ok2 else 'FAIL'}")
    for f in FEET: P(f"   [{f}] " + " ".join(f"{k} {v['Z']:+.2f}" for k, v in rows[f].items()) + f"  fails {keys_summary(rows[f])['nfail']}")
    dr = max(abs(rep[t][f"R1|c0|{f}"]["Z"][h][k] - base[t][f"R1|c0|{f}"]["Z"][h][k]) for t, _, _ in KTAGS for f in FEET for h in HH for k in KS) if rep else float("nan")
    okc = dr <= 1e-9; P(f"KA2c replica hook: max |dZ| {dr:.1e} -> {'PASS' if okc else 'FAIL'}")
    mut = {}
    if mu:
        for f in FEET:
            mr = keys_rows(mu, f); ch = sum(mr[k]["label"] != rows[f][k]["label"] for k in KS); dz = min(abs(mr[k]["Z"] - rows[f][k]["Z"]) for k in KS)
            pr = [mu["g005_f034"][f"R1|c0|{f}"]["preds"]["h0672"][k] / base["g005_f034"][f"R1|c0|{f}"]["preds"]["h0672"][k] for k in KS if "-b" not in k]
            mut[f] = dict(label_changes=ch, min_dz=dz, pred_ratio=[float(min(pr)), float(max(pr))], ok=ch >= 5 or dz >= 1)
            P(f"MUT G2 [{f}] g x 2: {ch} of 15 keys change label, min |dZ| {dz:.2f}; amplitude-key pred ratio {min(pr):.3f}..{max(pr):.3f} -> {'BITES' if mut[f]['ok'] else 'DOES NOT BITE'}")
    RES.update(R2=dict(ok=ok2, dZ_cache=d, dZ_rows=d2, rows=rows), KA2c=dict(ok=okc, dZ=dr), MUT_G2=mut); save()

def keys_real():
    P("LE1 keys real: G2 base / K1 no miscentring / K2 no reduced-shear factor, law and NP1 real L3. kappa = 1/2 FITTED; not theory closed.")
    o = {}
    for k in ("law", "np1_L3"):
        o[k] = {}
        for sw, nm in (("base", "base"), ("nomis", "K1 no miscentring"), ("nored", "K2 no reduced shear")):
            K = keys_run(k, sw)
            if K is None: o[k][nm] = "NOT COMPUTABLE"; continue
            o[k][nm] = {f: keys_rows(K, f) for f in FEET}
            for f in FEET: s = keys_summary(o[k][nm][f]); P(f"[{k} | {nm} | {f}] fails {s['nfail']}: " + " ".join(f"{q} {v['Z']:+.2f}" for q, v in o[k][nm][f].items()))
    RES["G2"] = o; save()

def verdict():
    J = {m: json.load(open(os.path.join(HERE, f"le1_{m}.json"))) for m in ("controls", "keys_controls", "real", "keys_real")}
    P("LE1 verdict (frozen precedence). kappa = 1/2 FITTED; not theory closed."); RES["inputs"] = list(J)
    c, kc, r, kr = J["controls"], J["keys_controls"], J["real"], J["keys_real"]
    repro = all(v["ok"] for v in c["R1"].values()) and kc["R2"]["ok"] and all(v["ok"] for v in c["R3"].values())
    kas = {k: bool(c[k]["ok"]) for k in ("KA1a", "KA1b", "KA1c", "KA1d", "KA1e", "KA2a", "KA2b", "KA3b")}; kas["KA2c"] = bool(kc["KA2c"]["ok"]); kas["KA3a"] = all(c["KA3a"][f]["ok"] for f in FEET)
    P("reproduction R1, R2, R3:", repro); P("known answers:", json.dumps(kas))
    RES.update(repro=repro, kas=kas); save()

if __name__ == "__main__":
    {"controls": controls, "real": real, "keys_controls": keys_controls, "keys_real": keys_real, "verdict": verdict}[MODE]()
