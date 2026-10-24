"""X7_cluster_core_significance analysis (criteria 40ae8ff09f + amendments): is the eRASS1 x KiDS core excess significant once
the additive shear systematics are CALIBRATED, and does it depend on cluster mass?
Inputs: this lane's x7_measure_percluster.npz (replay, equal to X2's npz), the scratch extras npz (per-group leakage templates,
200 rotated-source realisations), x7_psf_regression_results.json (LK-P coefficients and covariances), X2's functions exec'd
read-only from its source text (statistics, gas, EFE tables, model, reduced shear), X2's npz and JSON and F1's JSON (K0).
Usage: x7_analysis.py <scratch dir with x7_measure_extras.npz> [--mutate]
--mutate: the cross shear replaces the tangential data in the X2 reproduction (K0 must FAIL) and the shape fits use unweighted
bin means (K3 must FAIL). kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":                                # macOS medium zone keeps freed temporaries resident
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
import json, math, time, hashlib, resource
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.stats import chi2 as CHI2
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; SOUT = [a for a in sys.argv[1:] if not a.startswith("--")][0]
OUTF = open(os.path.join(HERE, f"x7_analysis{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
# ============================================================== X2's own functions (exec'd read-only from its source text)
X2DIR = os.path.join(REB, "X2_cluster_outskirts"); X2SRC = os.path.join(X2DIR, "x2_cluster_outskirts.py"); TX = open(X2SRC).read()
RES["x2_source_sha256"] = sha(X2SRC)
def cutx(a, b): i = TX.index(a); j = TX.index(b, i); return TX[i:j]
NS2 = {"np": np, "os": os, "sys": sys, "math": math, "json": json, "time": time, "REB": REB, "REPO": REPO, "HERE": X2DIR,
       "LANES": os.path.join(REPO, "campaign_fresh_gravity"), "MUT": False, "RES": {}, "say": (lambda *a: None), "check": (lambda *a: None),
       "sha": sha, "rss": rss, "guard": (lambda tag: None)}
exec(cutx("# ============================================================== F1's own functions", "# ============================================================== data: the replay"), NS2)
exec(cutx("# ============================================================== data: the replay", "# ============================================================== statistics"), NS2)
exec(cutx("# ============================================================== statistics", "# ============================================================== EFE"), NS2)
exec(cutx('sys.path.insert(0, os.path.join(REB, "F2_outer_lensing"))', 'for f in FEET:\n    for k in ("noclu", "maxclu", "p2cat"):'), NS2)
exec(cutx("# ============================================================== the model", "# ============================================================== K2, K3, K7"), NS2)
RES["f1_source_sha256"] = NS2["RES"]["f1_source_sha256"]; RES["x2_npz_sha256"] = NS2["RES"]["replay_npz_sha256"]; RES["f2_aqual_sha256"] = NS2["RES"]["f2_aqual_sha256"]
FEET, HK = ("canonical", "alt"), ("h0672", "h0686"); CELLS = [(f, h) for f in FEET for h in HK]; BANDS = NS2["BANDS"]; BN = ("INNER", "MID", "OUTER")
for f in FEET:
    t1 = time.time(); NS2["CTAB"][(f, "noclu")] = NS2["ctable"](NS2["AQ"].solve_efe(NS2["YE"][f]["noclu"], maxit=3000))     # X2 A3 cap
    tb = NS2["CTAB"][(f, "noclu")]; say(f"EFE solve (X2's) {f} noclu: y_e {NS2['YE'][f]['noclu']:.3e} iters {tb['iters']} last change {tb['resid']:.1e} [{time.time()-t1:.0f} s]")
CSTAR = dict(gasshape="P", efe="noclu", red=True)
X2J = json.load(open(os.path.join(X2DIR, "x2_cluster_outskirts_results.json")))
F1J = json.load(open(os.path.join(REB, "F1_cluster_cores", "f1_cluster_cores_results.json")))
# ============================================================== K0: X2 reproduction (X2's npz, X2's code)
if MUT:
    for hk in HK: NS2["DAT"][hk]["D"] = NS2["DAT"][hk]["Dx"]; NS2["DAT"][hk]["W"] = NS2["DAT"][hk]["Wx"]
dev = []; ALLX = NS2["ALL"]
say("\n=== STEP 0: reproduction of X2 (C0, C*, terciles) and F1 PRIMARY with the record's code ===")
for f, hk in CELLS:
    c = f"{f}|{hk}"
    for conv in ("boost", "clip"):
        for lab, kw, sx in (("C0 (F1 PRIMARY)", {}, False), ("C* corrected baseline", CSTAR, True)):
            s = NS2["stats"](hk, NS2["stack_model"](f, hk, **kw)[0], conv, ALLX, sx); ref = X2J["rows"][lab][conv][c]
            for b in ("MID", "OUTER"):
                dev += [abs(s[b][q] - ref[b][q]) for q in ("A", "s_jk", "s_tot", "A_x", "A_RR")]
            dev.append(abs(s["Z_MID"] - ref["Z_MID"]))
            if conv == "boost":
                say(f"  {lab[:2]} {f[:3]} {hk}: MID {s['MID']['A']:.4f} s_jk {s['MID']['s_jk']:.4f} s_tot {s['MID']['s_tot']:.4f} (Z {s['Z_MID']:+.2f})"
                    f"  OUT {s['OUTER']['A']:.4f}  | X2 JSON MID {ref['MID']['A']:.4f} s_tot {ref['MID']['s_tot']:.4f}")
    s0 = NS2["stats"](hk, NS2["stack_model"](f, hk)[0], "boost", ALLX, False); r1 = F1J["rows"][f"PRIMARY {hk}"][f]
    dev += [abs(s0["MID"]["A"] - r1["MID"][0]), abs(s0["MID"]["s_jk"] - r1["MID"][1]), abs(s0["OUTER"]["A"] - r1["OUTER"][0])]
    for lab, kw, sx in (("C0", {}, False), ("C*", CSTAR, True)):
        for t, sel in NS2["TERC"].items():
            s = NS2["stats"](hk, NS2["stack_model"](f, hk, **kw)[0], "boost", sel, sx); ref = X2J["terciles"][lab][t]["boost"][c]
            dev += [abs(s["MID"]["A"] - ref["MID"]["A"]), abs(s["OUTER"]["A"] - ref["OUTER"]["A"])]
check("K0", max(dev) <= 1e-4, f"max|X2 code on X2 npz - X2 JSON / F1 JSON| over C0, C*, terciles, F1 PRIMARY: {max(dev):.1e} ({len(dev)} numbers)", "<= 1e-4")
# ============================================================== my data (this lane's replay) swapped into X2's functions
MY = np.load(os.path.join(HERE, "x7_measure_percluster.npz")); XE = np.load(os.path.join(SOUT, "x7_measure_extras.npz"))
RES["my_npz_sha256"] = sha(os.path.join(HERE, "x7_measure_percluster.npz")); RES["extras_sha256"] = sha(os.path.join(SOUT, "x7_measure_extras.npz"))
X2N = np.load(os.path.join(X2DIR, "x2_replay_percluster.npz"))
scale = float(np.max(np.abs(X2N["D"]))); k1 = max(float(np.max(np.abs(MY[k] - X2N[k]))) for k in ("D", "Dx", "DRR", "E"))
k1n = all(str(a) == str(b) for a, b in zip(MY["name"], X2N["name"])) and len(MY["name"]) == len(X2N["name"]) and all(str(a) == str(b) for a, b in zip(XE["name"], MY["name"]))
check("K1", k1 <= 1e-9*scale and k1n, f"my replay vs X2 npz: max|diff| D/Dx/DRR/E {k1:.1e}; names equal {k1n}", "<= 1e-9 x max|D|")
N = len(MY["name"]); HI = {"h070": 0, "h0672": 1, "h0686": 2}; HXI = {"h0672": 0, "h0686": 1}
DAT = {}
for hk in HK:
    i = HI[hk]; Dt = MY["D"][:, i]; Et = MY["E"][:, i]
    if MUT: Dt, Et = MY["Dx"][:, i], MY["Ex"][:, i]
    W = np.where(Et < 1e8, 1/Et**2, 0); Wx = np.where(MY["Ex"][:, i] < 1e8, 1/MY["Ex"][:, i]**2, 0); B = MY["den"][:, i].sum(0)/MY["den_r"][:, i].sum(0)
    DAT[hk] = dict(D=Dt, W=W, B=B, Dx=MY["Dx"][:, i], Wx=Wx, DRR=MY["DRR"][:, i], m2=MY["den"][:, i], m=MY["m3to8"][:, i])
NS2["DAT"] = DAT; NS2["PRED"].clear()
PATCH = NS2["PATCH"]; ALL = np.ones(N, bool)
PM = {}
for f, hk in CELLS:
    PM[("C0", f, hk)] = NS2["stack_model"](f, hk)[0].copy(); PM[("C*", f, hk)] = NS2["stack_model"](f, hk, **CSTAR)[0].copy()
say(f"model predictions C0 and C* built for 4 cells [{time.time()-T0:.0f} s]")
# ============================================================== leakage coefficients and covariances (this lane's regression)
REG = json.load(open(os.path.join(HERE, "x7_psf_regression_results.json"))); GN = sorted(REG["LKP"], key=lambda g: REG["LKP"][g]["group"])
LKPc = np.array([[REG["LKP"][g][c] for c in ("c1", "alpha1", "c2", "alpha2")] for g in GN]); LKPcov = np.array([REG["LKP"][g]["cov"] for g in GN])
PT = XE["P"]                                                                              # (N, 2h, 4 types, 2 ch, 10 groups, 8)
ROT = XE["rot"]                                                                           # (N, 2h, R, 5 [t, x, RR, rand t, rand x], 8)
R = ROT.shape[2]
lk_chk = float(np.max(np.abs(np.einsum("nhtcgb,gt->nhcb", PT, LKPc) - MY["leakP"]))); lk_sc = float(np.max(np.abs(MY["leakP"])))
# ============================================================== the statistic machinery
RNGBASE = 20261024
def bands_sum(X, Wb):
    """per-cluster band sums of X*Wb over each band's bins: X (..., 8) with leading cluster axis -> (..., 3)."""
    return np.stack([(X[..., j]*Wb[..., j]).sum(-1) for j in (BANDS[b] for b in BN)], -1)
class Cell:
    def __init__(self, model, f, hk, conv):
        d = DAT[hk]; P = PM[(model, f, hk)]; h = HXI[hk]; Bc = d["B"] if conv == "boost" else np.ones(8)
        WB = d["W"]*Bc[None, :]
        self.den = bands_sum(P, d["W"]); self.wsum = bands_sum(np.ones_like(P), WB)
        self.num = {"t": bands_sum(d["D"], WB), "x": bands_sum(d["Dx"], WB), "RR": bands_sum(d["DRR"], WB),
                    "leak_t": bands_sum(MY["leakP"][:, h, 0], WB), "leak_x": bands_sum(MY["leakP"][:, h, 1], WB),
                    "leakT_t": bands_sum(MY["leakT"][:, h, 0], WB), "leakT_x": bands_sum(MY["leakT"][:, h, 1], WB),
                    "psf_t": bands_sum(MY["psfpat"][:, h, 0], WB), "psf_x": bands_sum(MY["psfpat"][:, h, 1], WB),
                    "rand_t": bands_sum(MY["Rmean"][:, HI[hk]], WB), "rand_x": bands_sum(MY["Rmeanx"][:, HI[hk]], WB)}
        self.rot = bands_sum(ROT[:, h].astype(np.float64), WB[:, None, None, :])         # (N, R, 5, 3)
        self.tmpl = bands_sum(PT[:, h, :, 0], WB[:, None, None, :])                      # (N, 4 types, 10 groups, 3) tangential
        self.WB, self.P, self.d, self.h, self.Bc = WB, P, d, h, Bc
def ratio(num, den, sel): return float(num[sel].sum()/den[sel].sum())
def jk(num, den, sel):
    reps = [ratio(num, den, sel & (PATCH != p)) for p in range(30) if (sel & (PATCH != p)).sum() < sel.sum()]
    n = len(reps); return float(np.sqrt((n - 1)/n*np.sum((np.array(reps) - np.mean(reps))**2)))
BOOTIDX = {}
def boot(num, den, sel, key):
    if key not in BOOTIDX:
        rng = np.random.default_rng([RNGBASE, key]); BOOTIDX[key] = rng.integers(0, int(sel.sum()), size=(2000, int(sel.sum())))
    nn, dd = num[sel][BOOTIDX[key]], den[sel][BOOTIDX[key]]
    return float(np.std(nn.sum(1)/dd.sum(1), ddof=1))
def summ(cell, sel, key):
    """all band quantities of one selection; bands MID and OUTER (INNER: A only)."""
    out = {}
    for bi, b in enumerate(BN):
        den = cell.den[:, bi]; nm = {k: v[:, bi] for k, v in cell.num.items()}
        o = {k: ratio(nm[k], den, sel) for k in nm}; o["A"] = o.pop("t"); o["A_x"] = o.pop("x"); o["A_RR"] = o.pop("RR")
        if b == "INNER": out[b] = {"A": o["A"]}; continue
        o["s_jk"] = jk(nm["t"], den, sel); o["s_boot"] = boot(nm["t"], den, sel, key); o["s_STAT"] = max(o["s_jk"], o["s_boot"])
        o["s_jk_x"] = jk(nm["x"], den, sel)
        rv = cell.rot[sel][:, :, :, bi].sum(0)/den[sel].sum()                           # (R, 5)
        for ci, nmc in enumerate(("t", "x", "RR", "rand_t", "rand_x")): o[f"s_n_{nmc}"] = float(np.std(rv[:, ci], ddof=1))
        o["mean_n_t"] = float(rv[:, 0].mean())
        rx = o["A_x"] - o["leak_x"]; o["resid_x"] = rx; o["p_x"] = float(np.mean(np.abs(rv[:, 1]) >= abs(rx)))
        grad = cell.tmpl[sel][:, :, :, bi].sum(0)/den[sel].sum()                       # (4 types, 10 groups)
        o["s_leak"] = float(np.sqrt(sum(grad[:, g] @ LKPcov[g] @ grad[:, g] for g in range(10))))
        o["s_x_exc"] = float(np.sqrt(max(0.0, rx**2 - o["s_n_x"]**2))); o["s_RR_exc"] = float(np.sqrt(max(0.0, o["A_RR"]**2 - o["s_n_RR"]**2)))
        o["A_CAL"] = o["A"] - o["leak_t"]
        o["s_CAL"] = float(np.sqrt(o["s_STAT"]**2 + o["s_leak"]**2 + o["s_x_exc"]**2 + o["s_RR_exc"]**2))
        o["s_CONS"] = float(np.sqrt(o["s_jk"]**2 + o["A_x"]**2 + o["A_RR"]**2))
        o["Z_STAT"] = (o["A"] - 1)/o["s_STAT"]; o["Z_CAL"] = (o["A_CAL"] - 1)/o["s_CAL"]; o["Z_CONS"] = (o["A"] - 1)/o["s_CONS"]
        o["A_CAL_T"] = o["A"] - o["leakT_t"]; o["Z_CAL_T"] = (o["A_CAL_T"] - 1)/float(np.sqrt(o["s_STAT"]**2 + o["s_x_exc"]**2 + o["s_RR_exc"]**2))
        o["kappa_scale"] = float(cell.wsum[sel, bi].sum()/den[sel].sum())
        o["Z_rand_t"] = o["rand_t"]/o["s_n_rand_t"]; o["Z_rand_x"] = o["rand_x"]/o["s_n_rand_x"]
        out[b] = o
    return out
# ============================================================== implementation checks K2 (bootstrap), K4 (leakage propagation)
cz = Cell("C*", "canonical", "h0672", "boost")
den = cz.den[:, 1]; k2a = boot(2*den, den, ALL, 999)
rngt = np.random.default_rng(7); vv = rngt.normal(1.0, 0.3, N)
k2pop = boot(vv, np.ones(N), ALL, 998)/(0.3/np.sqrt(N))                          # frozen form (population sigma): RUN1 FAILED at 0.882
k2b = boot(vv, np.ones(N), ALL, 998)/(vv.std(ddof=0)/np.sqrt(N))                 # A4 (POST-RESULT): the sample's own sigma/sqrt n, the bootstrap's target
RES["K2_population_ratio"] = k2pop; RES["K2_sample_std"] = float(vv.std(ddof=0))
g0 = cz.tmpl[:, :, :, 1].sum(0)/den.sum(); LK2 = LKPc.copy(); eps = 1e-3; LK2[3, 1] += eps
a_lk = lambda C_: float((bands_sum(np.einsum("ntgb,gt->nb", PT[:, 0, :, 0], C_), cz.WB)[:, 1]).sum()/den.sum())
fd = (a_lk(LK2) - a_lk(LKPc))/eps; k4 = abs(fd/g0[1, 3] - 1)
check("K2", k2a <= 1e-12 and abs(k2b - 1) <= 0.10, f"sigma_boot(D = 2P) {k2a:.1e}; synthetic sigma_boot/(sample sigma/sqrt n) {k2b:.3f} "
      f"(vs population sigma {k2pop:.3f}; the draw's sample sigma is {vv.std(ddof=0):.4f} for population 0.3)", "<= 1e-12; within 10 %")
check("K4", k4 <= 1e-6 and lk_chk <= 1e-9*max(lk_sc, 1e-30), f"finite-difference vs gradient (group 3, alpha1) rel {k4:.1e}; stored leakP = templates x coefficients {lk_chk:.1e} (scale {lk_sc:.2e})", "<= 1e-6; <= 1e-9 rel")
# ============================================================== STEP 1-2: all clusters, three treatments
say("\n=== STEP 1: calibration (all 326 clusters; C* model; boost convention unless stated) ===")
g = REG["global"]; say(f"global leakage: alpha1 {g['alpha1']:+.4f}+-{g['sig'][1]:.4f}  alpha2 {g['alpha2']:+.4f}+-{g['sig'][3]:.4f}  c1 {g['c1']:+.1e}  c2 {g['c2']:+.1e}")
SUM = {}
for model in ("C*", "C0"):
    for conv in ("boost", "clip"):
        for f, hk in CELLS:
            SUM[(model, conv, f, hk)] = summ(Cell(model, f, hk, conv), ALL, 0)
for f, hk in CELLS:
    o = SUM[("C*", "boost", f, hk)]
    for b in ("MID", "OUTER"):
        q = o[b]
        say(f"  {f[:3]} {hk} {b:5s}: leak LK-P t {q['leak_t']:+.4f}+-{q['s_leak']:.4f} x {q['leak_x']:+.4f} | LK-T t {q['leakT_t']:+.4f} x {q['leakT_x']:+.4f}"
            f" | PSF pattern (alpha=1) t {q['psf_t']:+.3f} x {q['psf_x']:+.3f}")
        say(f"       cross A_x {q['A_x']:+.4f} (jk {q['s_jk_x']:.4f}, rotated noise {q['s_n_x']:.4f}, p {q['p_x']:.3f}) -> excess s_x {q['s_x_exc']:.4f};"
            f"  R-R {q['A_RR']:+.4f} (noise {q['s_n_RR']:.4f}) -> s_RR {q['s_RR_exc']:.4f};  random-point raw t {q['rand_t']:+.4f} (Z {q['Z_rand_t']:+.2f}) x {q['rand_x']:+.4f} (Z {q['Z_rand_x']:+.2f})")
        say(f"       sigma: jk {q['s_jk']:.4f} boot {q['s_boot']:.4f} rotated-noise(t) {q['s_n_t']:.4f} (mean {q['mean_n_t']:+.4f})")
# reporting only (POST-RESULT addition, no verdict weight): analytic shape noise for independent clusters, sqrt(sum W B^2 (1 + 1/n_rand))/sum W P
AN = {}
for f, hk in CELLS:
    ce = Cell("C*", f, hk, "boost"); d = DAT[hk]; v = bands_sum((1 + 1/MY["nrand"])[:, None]*np.ones((N, 8)), d["W"]*d["B"][None, :]**2)
    AN[f"{f}|{hk}"] = {b: float(np.sqrt(v[:, bi].sum())/ce.den[:, bi].sum()) for bi, b in enumerate(BN) if b != "INNER"}
    o = SUM[("C*", "boost", f, hk)]
    say(f"  analytic shape noise {f[:3]} {hk}: MID {AN[f'{f}|{hk}']['MID']:.4f} (rotations t {o['MID']['s_n_t']:.4f} x {o['MID']['s_n_x']:.4f}; jackknife t {o['MID']['s_jk']:.4f} x {o['MID']['s_jk_x']:.4f})"
        f"  OUTER {AN[f'{f}|{hk}']['OUTER']:.4f} (rotations t {o['OUTER']['s_n_t']:.4f} x {o['OUTER']['s_n_x']:.4f}; jackknife t {o['OUTER']['s_jk']:.4f} x {o['OUTER']['s_jk_x']:.4f})")
RES["analytic_shape_noise"] = AN
# cross-shear profile chi2 against the rotation covariance (bins 0-7), C* not needed (Delta Sigma units)
XPROF = {}
for hk in HK:
    for conv in ("boost", "clip"):
        d = DAT[hk]; Bc = d["B"] if conv == "boost" else np.ones(8); W = d["W"]; h = HXI[hk]
        sx = (W*d["Dx"]*Bc).sum(0)/W.sum(0); rs = np.einsum("nj,nrj->rj", W*Bc, ROT[:, h, :, 1].astype(np.float64))/W.sum(0)
        Cr = np.cov(rs.T); H = (R - 8 - 2)/(R - 1); c2 = float(H*sx @ np.linalg.solve(Cr, sx)); XPROF[f"{hk}|{conv}"] = dict(chi2=c2, p=float(CHI2.sf(c2, 8)), stack=sx.tolist(), sig=np.sqrt(np.diag(Cr)).tolist())
        if conv == "boost": say(f"  cross-shear profile {hk}: chi2 {c2:.2f} / 8 vs rotation covariance (Hartlap {H:.3f}), p {CHI2.sf(c2, 8):.3f}; stack/sigma " + " ".join(f"{a/b:+.2f}" for a, b in zip(sx, np.sqrt(np.diag(Cr)))))
RES["cross_profile"] = XPROF
say("\n=== STEP 2: Z_MID and Z_OUT under the three treatments (STAT = max(boot, jk); CAL = calibrated; CONS = X2's (e)) ===")
def zline(o, b):
    q = o[b]; return (f"A {q['A']:.3f} | STAT +-{q['s_STAT']:.3f} Z {q['Z_STAT']:+.2f} | CAL A {q['A_CAL']:.3f} +-{q['s_CAL']:.3f} Z {q['Z_CAL']:+.2f}"
                      f" | CONS +-{q['s_CONS']:.3f} Z {q['Z_CONS']:+.2f}")
for model in ("C*", "C0"):
    for conv in ("boost", "clip"):
        say(f"-- {model} model, {conv} convention" + ("  [GRADED]" if (model, conv) == ("C*", "boost") else ""))
        for f, hk in CELLS:
            o = SUM[(model, conv, f, hk)]; say(f"  {f[:3]} {hk} MID  : {zline(o, 'MID')}"); say(f"  {f[:3]} {hk} OUTER: {zline(o, 'OUTER')}")
RES["all"] = {f"{m}|{c}|{f}|{h}": v for (m, c, f, h), v in SUM.items()}
def v1(z):
    return "REAL" if min(z) >= 3 else ("NOT SIGNIFICANT" if min(z) < 2 else "MARGINAL")
ZC = [SUM[("C*", "boost", f, hk)]["MID"]["Z_CAL"] for f, hk in CELLS]
V1 = v1(ZC)
QUAL = {"STAT": v1([SUM[("C*", "boost", f, hk)]["MID"]["Z_STAT"] for f, hk in CELLS]), "CONS": v1([SUM[("C*", "boost", f, hk)]["MID"]["Z_CONS"] for f, hk in CELLS]),
        "clip": v1([SUM[("C*", "clip", f, hk)]["MID"]["Z_CAL"] for f, hk in CELLS]), "C0": v1([SUM[("C0", "boost", f, hk)]["MID"]["Z_CAL"] for f, hk in CELLS]),
        "LK-T": v1([SUM[("C*", "boost", f, hk)]["MID"]["Z_CAL_T"] for f, hk in CELLS])}
LMD = any(abs(SUM[("C*", "boost", f, hk)]["MID"]["leakT_t"] - SUM[("C*", "boost", f, hk)]["MID"]["leak_t"]) > SUM[("C*", "boost", f, hk)]["MID"]["s_STAT"]/2 for f, hk in CELLS)
# ============================================================== STEP 3: mass trend
say("\n=== STEP 3: mass trend (catalogue MGAS500, the record's proxy) ===")
Mg = np.asarray(MY["Mgas500"], float); M5 = np.asarray(MY["M500"], float)
q5 = np.quantile(Mg, [0.2, 0.4, 0.6, 0.8]); q3 = np.quantile(Mg, [1/3, 2/3]); MT = float(q3[0]); MMED = float(np.median(Mg))
BINS = {"quintiles": np.digitize(Mg, q5), "terciles": np.digitize(Mg, q3)}
q5m = np.quantile(M5, [0.2, 0.4, 0.6, 0.8]); q3m = np.quantile(M5, [1/3, 2/3])
BINS_M500 = {"quintiles": np.digitize(M5, q5m), "terciles": np.digitize(M5, q3m)}
XLOG = np.log10(Mg/MMED); LO = Mg < MT
RES["mass"] = dict(q5=q5.tolist(), q3=q3.tolist(), M_T=MT, M_med=MMED, n_q=[int((BINS["quintiles"] == k).sum()) for k in range(5)])
say(f"quintile edges {np.round(q5/1e12, 2).tolist()} e12 Msun; tercile edges {np.round(q3/1e12, 2).tolist()} e12 (step at M_T {MT:.3e}); pivot {MMED:.3e}")
BS = {}
def bin_summ(model, conv, f, hk, binning, ids, keyoff):
    cell = Cell(model, f, hk, conv); nb = int(ids.max()) + 1
    return cell, [summ(cell, ids == k, keyoff + k) for k in range(nb)]
def design(cell, ids, band, shape, weighted=True):
    bi = BN.index(band); w = cell.den[:, bi]; nb = int(ids.max()) + 1; rows = []
    for k in range(nb):
        s = ids == k; ww = w[s] if weighted else np.ones(int(s.sum()))
        if shape == "S0": rows.append([1.0])
        elif shape == "S1": rows.append([1.0, float((ww*XLOG[s]).sum()/ww.sum())])
        else: fl = float((ww*LO[s]).sum()/ww.sum()); rows.append([fl, 1 - fl])
    return np.array(rows)
def gls(X, y, C):
    Ci = np.linalg.inv(C); F = X.T @ Ci @ X; th = np.linalg.solve(F, X.T @ Ci @ y); r = y - X @ th
    return th, float(r @ Ci @ r)
def vec_cov(cell, sm, allq, band, treat):
    y = np.array([q[band]["A_CAL" if treat.startswith("CAL") else "A"] for q in sm]); st = np.array([q[band]["s_STAT"] for q in sm])
    if treat == "STAT": C = np.diag(st**2)
    elif treat == "CONS": C = np.diag(np.array([q[band]["s_CONS"] for q in sm])**2)
    elif treat == "CAL":
        kap = np.array([q[band]["kappa_scale"] for q in sm])/allq[band]["kappa_scale"]
        v = allq[band]["s_x_exc"]*kap; u = allq[band]["s_RR_exc"]*kap
        C = np.diag(st**2 + np.array([q[band]["s_leak"] for q in sm])**2) + np.outer(v, v) + np.outer(u, u)
    else:
        C = np.diag(st**2 + np.array([q[band]["s_leak"]**2 + q[band]["s_x_exc"]**2 + q[band]["s_RR_exc"]**2 for q in sm]))
    return y, C
def fits(cell, ids, sm, allq, band, treat):
    y, C = vec_cov(cell, sm, allq, band, treat); n = len(y); out = {}
    for shp, k in (("S0", 1), ("S1", 2), ("S2", 2)):
        th, c2 = gls(design(cell, ids, band, shp, weighted=not MUT), y, C); out[shp] = dict(theta=th.tolist(), chi2=c2, BIC=c2 + k*np.log(n))
    out["dchi2_S1"] = out["S0"]["chi2"] - out["S1"]["chi2"]; out["dchi2_S2"] = out["S0"]["chi2"] - out["S2"]["chi2"]
    bic = {s: out[s]["BIC"] for s in ("S0", "S1", "S2")}; mn = min(bic.values())
    out["preferred"] = next(s for s in ("S0", "S1", "S2") if bic[s] <= mn + 1e-12)
    out["Z_lightest"] = float((y[0] - 1)/np.sqrt(C[0, 0])); out["A"] = y.tolist(); out["sig"] = np.sqrt(np.diag(C)).tolist()
    return out
# K3: synthetic exact shapes with the real weights (C* canonical h0672 boost, quintiles)
c3 = Cell("C*", "canonical", "h0672", "boost"); ids3 = BINS["quintiles"]; Csyn = np.diag(np.linspace(0.05, 0.2, 5)**2) + 0.01
k3c, k3t = 0.0, 0.0
for shp, th0 in (("S1", np.array([1.3, 0.4])), ("S2", np.array([1.0, 1.8]))):
    ysyn = design(c3, ids3, "MID", shp, True) @ th0; th, c2 = gls(design(c3, ids3, "MID", shp, weighted=not MUT), ysyn, Csyn)
    k3c = max(k3c, c2); k3t = max(k3t, float(np.max(np.abs(th - th0))))
check("K3", k3c <= 1e-10 and k3t <= 1e-8, f"synthetic S1/S2 with the statistic's weights: max chi2 {k3c:.1e}, max|param - true| {k3t:.1e}", "chi2 <= 1e-10, params <= 1e-8")
# noise rule for the graded binning
TR = {}
for binning, ids in BINS.items():
    for f, hk in CELLS:
        TR[(binning, f, hk)] = bin_summ("C*", "boost", f, hk, binning, ids, 100 if binning == "quintiles" else 200)
smax = max(q["MID"]["s_STAT"] for f, hk in CELLS for q in TR[("quintiles", f, hk)][1])
GRADED = "quintiles" if smax <= 0.40 else "terciles"
say(f"noise rule: max quintile sigma_STAT,MID over 4 cells = {smax:.3f} (line 0.40) -> graded binning: {GRADED}")
RES["binning_rule"] = dict(max_quintile_sSTAT_MID=smax, graded=GRADED)
TREND = {}
for binning, ids in BINS.items():
    for f, hk in CELLS:
        cell, sm = TR[(binning, f, hk)]; allq = SUM[("C*", "boost", f, hk)]
        say(f"-- {binning} {f[:3]} {hk}" + ("  [GRADED]" if binning == GRADED else ""))
        for k, q in enumerate(sm):
            s = ids == k
            say(f"   bin {k+1} n {int(s.sum()):3d} median Mgas500 {np.median(Mg[s]):.2e}: MID {q['MID']['A']:.3f} (CAL {q['MID']['A_CAL']:.3f}) STAT +-{q['MID']['s_STAT']:.3f} "
                f"CAL Z {q['MID']['Z_CAL']:+.2f} CONS Z {q['MID']['Z_CONS']:+.2f} | OUT {q['OUTER']['A']:.3f} (CAL {q['OUTER']['A_CAL']:.3f}) STAT +-{q['OUTER']['s_STAT']:.3f} CAL Z {q['OUTER']['Z_CAL']:+.2f}"
                f" | A_x MID {q['MID']['A_x']:+.3f} (noise {q['MID']['s_n_x']:.3f})")
        for band in ("MID", "OUTER"):
            for treat in ("CAL", "STAT", "CONS", "CAL-own"):
                ft = fits(cell, ids, sm, allq, band, treat); TREND[(binning, f, hk, band, treat)] = ft
                if treat in ("CAL", "STAT", "CONS"):
                    say(f"   {band:5s} {treat:4s}: chi2 S0 {ft['S0']['chi2']:.2f} S1 {ft['S1']['chi2']:.2f} (b {ft['S1']['theta'][1]:+.3f}) S2 {ft['S2']['chi2']:.2f} "
                        f"(lo {ft['S2']['theta'][0]:.3f} hi {ft['S2']['theta'][1]:.3f}) | dchi2 S1 {ft['dchi2_S1']:.2f} S2 {ft['dchi2_S2']:.2f} | preferred {ft['preferred']} | Z_lightest {ft['Z_lightest']:+.2f}")
# clipped convention, graded binning (reported)
TRc = {}
for f, hk in CELLS:
    cell, sm = bin_summ("C*", "clip", f, hk, GRADED, BINS[GRADED], 300 if GRADED == "quintiles" else 400)
    allq = SUM[("C*", "clip", f, hk)]
    for band in ("MID", "OUTER"): TRc[(f, hk, band)] = fits(cell, BINS[GRADED], sm, allq, band, "CAL")
say("clipped boost, graded binning, CAL: " + "  ".join(f"{f[:3]} {hk} {b}: dchi2 S1 {TRc[(f, hk, b)]['dchi2_S1']:.2f} S2 {TRc[(f, hk, b)]['dchi2_S2']:.2f} Z1 {TRc[(f, hk, b)]['Z_lightest']:+.2f}"
                                          for f, hk in CELLS for b in ("MID", "OUTER")))
# M500 binning (LCDM-processed proxy; reported only), same rule as graded
M5R = {}
for f, hk in CELLS:
    cell, sm = bin_summ("C*", "boost", f, hk, GRADED, BINS_M500[GRADED], 500 if GRADED == "quintiles" else 600)
    allq = SUM[("C*", "boost", f, hk)]
    M5R[(f, hk)] = dict(A_MID=[q["MID"]["A_CAL"] for q in sm], Z_MID=[q["MID"]["Z_CAL"] for q in sm], A_OUT=[q["OUTER"]["A_CAL"] for q in sm], Z_OUT=[q["OUTER"]["Z_CAL"] for q in sm])
    say(f"M500 {GRADED} {f[:3]} {hk} (reported): CAL A_MID " + " ".join(f"{a:.2f}" for a in M5R[(f, hk)]["A_MID"]) + " | A_OUT " + " ".join(f"{a:.2f}" for a in M5R[(f, hk)]["A_OUT"]))
# C0 graded binning (reported)
for f, hk in CELLS:
    cell, sm = bin_summ("C0", "boost", f, hk, GRADED, BINS[GRADED], 700 if GRADED == "quintiles" else 800)
    say(f"C0 {GRADED} {f[:3]} {hk} (reported): A_MID " + " ".join(f"{q['MID']['A']:.2f}" for q in sm) + " | A_OUT " + " ".join(f"{q['OUTER']['A']:.2f}" for q in sm))
def vtrend(band):
    d = [max(TREND[(GRADED, f, hk, band, "CAL")]["dchi2_S1"], TREND[(GRADED, f, hk, band, "CAL")]["dchi2_S2"]) for f, hk in CELLS]
    prefs = sorted({TREND[(GRADED, f, hk, band, "CAL")]["preferred"] for f, hk in CELLS}); zl = [TREND[(GRADED, f, hk, band, "CAL")]["Z_lightest"] for f, hk in CELLS]
    if min(d) >= 9: cls = "PRESENT (" + ("/".join(prefs) if len(prefs) == 1 else "SPLIT shape " + "/".join(prefs)) + ")"
    elif max(d) < 4: cls = "ABSENT"
    else: cls = "UNDECIDED"
    lb = "CONSISTENT WITH A = 1" if max(abs(z) for z in zl) < 2 else ("INCONSISTENT" if min(abs(z) for z in zl) >= 2 else "SPLIT")
    return cls, lb, d, zl, prefs
V2, L2, d2, z2, p2 = vtrend("MID"); V3, L3, d3, z3, p3 = vtrend("OUTER")
# ============================================================== verdicts
say(f"\nV1 core excess (C*, CAL, boost): {V1}   Z_MID,CAL {[round(z, 2) for z in ZC]} (cells {[f'{f[:3]}|{h}' for f, h in CELLS]})")
say(f"   same rule under STAT: {QUAL['STAT']}; CONS (X2): {QUAL['CONS']}; clipped boost: {QUAL['clip']}; C0: {QUAL['C0']}; LK-T bracket: {QUAL['LK-T']}"
    + ("; LEAKAGE-MODEL-DEPENDENT" if LMD else ""))
say(f"V2 mass trend of A_MID ({GRADED}, CAL): {V2}; max dchi2 per cell {[round(x, 2) for x in d2]}; preferred {p2}; lightest bin {L2} (Z {[round(z, 2) for z in z2]})")
say(f"V3 mass trend of A_OUTER ({GRADED}, CAL): {V3}; max dchi2 per cell {[round(x, 2) for x in d3]}; preferred {p3}; lightest bin {L3} (Z {[round(z, 2) for z in z3]})")
RES.update(V1=V1, V1_qualifiers=QUAL, leakage_model_dependent=LMD, Z_MID_CAL=ZC, V2=V2, V2_lightest=L2, V2_dchi2=d2, V2_Z_lightest=z2, V3=V3, V3_lightest=L3,
           V3_dchi2=d3, V3_Z_lightest=z3, graded_binning=GRADED,
           trend={"|".join(k): v for k, v in TREND.items()}, trend_clip={"|".join(k): v for k, v in TRc.items()}, m500={"|".join(k): v for k, v in M5R.items()},
           bins={f"{b}|{f}|{h}": [q for q in TR[(b, f, h)][1]] for b in BINS for f, h in CELLS}, regression_global=REG["global"])
pk = rss(); check("K5", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
npass = sum(ok for _, ok in CHECKS); RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk, N=N, R=R)
say(f"X7_ANALYSIS COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x7_analysis_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
sys.exit(0 if npass == len(CHECKS) else 1)
