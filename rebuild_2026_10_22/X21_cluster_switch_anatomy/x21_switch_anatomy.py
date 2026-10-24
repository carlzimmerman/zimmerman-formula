"""X21_cluster_switch_anatomy (criteria a48f6d5e08): is the cluster-core "switch" a threshold, a smooth trend or an artefact of
binning on MGAS500, what does the per-cluster MID excess track, and can omitted known baryons supply it?
Inputs (read-only): X7's committed per-cluster npz and results JSON, X13's results JSON, X2's source (functions exec'd exactly as
x7_analysis.py does), the eRASS1 FITS, CFG688's redMaPPer TSV, CFG687's npz (positions for the CFG922 join), CFG922's A1 census.
Usage: OMP_NUM_THREADS=1 nice -n 15 python3 x21_switch_anatomy.py      (X21_MUTATE=1 for the MUTATE twin: cluster labels shuffled)
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
import json, math, time, hashlib, resource
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.stats import spearmanr
from astropy.io import fits
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("X21_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"x21_switch_anatomy{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
# ============================================================== X2's own functions (exec'd read-only, as x7_analysis.py)
X2DIR = os.path.join(REB, "X2_cluster_outskirts"); X2SRC = os.path.join(X2DIR, "x2_cluster_outskirts.py"); TX = open(X2SRC).read()
RES["x2_source_sha256"] = sha(X2SRC)
def cutx(a, b): i = TX.index(a); j = TX.index(b, i); return TX[i:j]
NS2 = {"np": np, "os": os, "sys": sys, "math": math, "json": json, "time": time, "REB": REB, "REPO": REPO, "HERE": X2DIR,
       "LANES": LANES, "MUT": False, "RES": {}, "say": (lambda *a: None), "check": (lambda *a: None),
       "sha": sha, "rss": rss, "guard": (lambda tag: None)}
exec(cutx("# ============================================================== F1's own functions", "# ============================================================== data: the replay"), NS2)
exec(cutx("# ============================================================== data: the replay", "# ============================================================== statistics"), NS2)
exec(cutx("# ============================================================== statistics", "# ============================================================== EFE"), NS2)
exec(cutx('sys.path.insert(0, os.path.join(REB, "F2_outer_lensing"))', 'for f in FEET:\n    for k in ("noclu", "maxclu", "p2cat"):'), NS2)
exec(cutx("# ============================================================== the model", "# ============================================================== K2, K3, K7"), NS2)
FEET, HK = ("canonical", "alt"), ("h0672", "h0686"); CELLS = [(f, h) for f in FEET for h in HK]; BANDS = NS2["BANDS"]
for f in FEET:
    t1 = time.time(); NS2["CTAB"][(f, "noclu")] = NS2["ctable"](NS2["AQ"].solve_efe(NS2["YE"][f]["noclu"], maxit=3000))
    say(f"EFE solve (X2's) {f} noclu [{time.time()-t1:.0f} s]")
CSTAR = dict(gasshape="P", efe="noclu", red=True)
# ============================================================== X7's committed per-cluster arrays (never re-measured)
X7DIR = os.path.join(REB, "X7_cluster_core_significance"); NPZ = os.path.join(X7DIR, "x7_measure_percluster.npz")
MY = np.load(NPZ); RES["x7_npz_sha256"] = sha(NPZ); N = len(MY["name"])
X7J = json.load(open(os.path.join(X7DIR, "x7_analysis_results.json"))); X13J = json.load(open(os.path.join(REB, "X13_source_size_test", "x13_analysis_results.json")))
HI = {"h070": 0, "h0672": 1, "h0686": 2}; HXI = {"h0672": 0, "h0686": 1}
DAT = {}
for hk in HK:
    i = HI[hk]; W = np.where(MY["E"][:, i] < 1e8, 1/MY["E"][:, i]**2, 0); B = MY["den"][:, i].sum(0)/MY["den_r"][:, i].sum(0)
    DAT[hk] = dict(D=MY["D"][:, i], W=W, B=B, Dx=MY["Dx"][:, i], Wx=W, DRR=MY["DRR"][:, i], m2=MY["den"][:, i], m=MY["m3to8"][:, i])
NS2["DAT"] = DAT; NS2["PRED"].clear(); PATCH = NS2["PATCH"]; JM = BANDS["MID"]
assert all(str(a) == str(b) for a, b in zip(NS2["CL"], NS2["CL"])) and [c["name"] for c in NS2["CL"]] == [str(x) for x in MY["name"]]
t1 = time.time(); PM = {(f, hk): NS2["stack_model"](f, hk, **CSTAR)[0].copy() for f, hk in CELLS}; NS2["PRED"].clear()
say(f"C* model built for 4 cells [{time.time()-t1:.0f} s]")
CELLD = {}
for f, hk in CELLS:
    d_ = DAT[hk]; WB = d_["W"]*d_["B"][None, :]; P = PM[(f, hk)]; h = HXI[hk]
    CELLD[(f, hk)] = dict(n=(WB[:, JM]*(d_["D"][:, JM] - MY["leakP"][:, h, 0][:, JM])).sum(1), nraw=(WB[:, JM]*d_["D"][:, JM]).sum(1),
                          d=(d_["W"][:, JM]*P[:, JM]).sum(1), wsum=WB[:, JM].sum(1))
# ============================================================== labels: eRASS1 (by NAME), redMaPPer (CFG688 rule), CFG922 census (via CFG687 positions)
EF = os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"); RES["erass1_sha256"] = sha(EF)
E = fits.open(EF)[1].data; nm = [str(x).strip() for x in E["NAME"]]; idx = {s: k for k, s in enumerate(nm)}
JI = np.array([idx[str(x).strip()] for x in MY["name"]])
def col(c): return np.asarray(E[c], float)[JI]
LAB = dict(Mg=np.asarray(MY["Mgas500"], float), Mg_fits=col("MGAS500")*1e11, KT=col("KT"), Z=col("BEST_Z"), L500=col("L500"),
           L300=col("L300kpc"), M500=np.asarray(MY["M500"], float))
rm = np.loadtxt(os.path.join(LANES, "CFG688_richness_split", "redmapper_z004_06.tsv")); RES["redmapper_sha256"] = sha(os.path.join(LANES, "CFG688_richness_split", "redmapper_z004_06.tsv"))
lam = np.full(N, np.nan)
for i in range(N):
    ra, de, z = MY["ra"][i], MY["dec"][i], MY["z"][i]
    dd = np.degrees(np.arccos(np.clip(np.sin(np.radians(de))*np.sin(np.radians(rm[:, 1])) + np.cos(np.radians(de))*np.cos(np.radians(rm[:, 1]))*np.cos(np.radians(ra - rm[:, 0])), -1, 1)))*60
    ok = (dd < 2.0) & (np.abs(rm[:, 2] - z) < 0.04)
    if ok.any(): lam[i] = rm[ok][np.argmin(dd[ok]), 3]
LAB["LAM"] = lam
P687 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
CEN = json.load(open(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json")))["eRASS1"]
RES["cfg922_census_sha256"] = sha(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json"))
J9 = np.full(N, -1); dzmax = 0.0
for i in range(N):
    dd = np.hypot((P687["ra"] - MY["ra"][i])*np.cos(np.radians(MY["dec"][i])), P687["dec"] - MY["dec"][i])*3600; j = int(np.argmin(dd))
    if dd[j] < 5 and abs(P687["z"][j] - MY["z"][i]) < 1e-3: J9[i] = j; dzmax = max(dzmax, abs(float(CEN[j]["z"]) - MY["z"][i]))
def cen(k): return np.array([float(CEN[j][k]) if j >= 0 else np.nan for j in J9])
meas = np.array([j >= 0 and not CEN[j].get("not_measured", False) for j in J9])
LAB.update(S_up=cen("S_up"), S_cen=cen("S_cen"), gcyl=cen("gas_cyl"), bcg=cen("bcg_med"), matched=(J9 >= 0), meas=meas)
LAB["BCG"] = np.where(meas & (LAB["bcg"] > 0), LAB["bcg"], np.nan); LAB["FSC"] = np.where(meas & (LAB["S_cen"] > 0), LAB["S_cen"]/LAB["gcyl"], np.nan)
LAB["CX"] = LAB["L300"]/LAB["L500"]
if MUT:                                                                       # MUTATE: every catalogue label shuffled across clusters
    perm = np.random.default_rng(2121).permutation(N)
    for k in list(LAB): LAB[k] = LAB[k][perm]
say(f"labels: KT>0 {int(np.sum(LAB['KT'] > 0))}, redMaPPer {int(np.isfinite(LAB['LAM']).sum())}, CFG922 matched {int(LAB['matched'].sum())} "
    f"(measured {int(LAB['meas'].sum())}, BCG>0 {int(np.isfinite(LAB['BCG']).sum())}, S_cen/gas {int(np.isfinite(LAB['FSC']).sum())})")
k1a = float(np.max(np.abs(LAB["Mg_fits"]/np.asarray(MY["Mgas500"], float) - 1)))
check("K1", k1a <= 1e-12 and dzmax <= 1e-3, f"eRASS1 MGAS500 by NAME vs npz rel {k1a:.1e}; CFG922 join max|dz| {dzmax:.1e} ({int((J9 >= 0).sum())} joined)", "<= 1e-12; <= 1e-3")
# ============================================================== statistics machinery (X7's bootstrap / jackknife conventions)
RB = 20261024; NB = 2000
def bidx(nsel, key): return np.random.default_rng([RB, key]).integers(0, nsel, size=(NB, nsel))
def counts(ix, nsel): return np.stack([np.bincount(r, minlength=nsel) for r in ix]).astype(float)
def jkreps(I):
    """weights (n_rep, len(I)) for X2's 30-patch jackknife restricted to I (patches present in I only)."""
    p = PATCH[I]; return np.array([(p != q).astype(float) for q in range(30) if np.any(p == q)])
def jsig(v): v = np.asarray(v); n = len(v); return float(np.sqrt((n - 1)/n*np.sum((v - v.mean())**2)))
def ratio_w(Wt, n, d): return (Wt @ n)/(Wt @ d)
def sstat(fun, I, key):
    """sigma_STAT = max(bootstrap sd ddof=1, jackknife) of a statistic fun(weights (R, n)) -> (R,) or (R, k)."""
    C = counts(bidx(len(I), key), len(I)); sb = np.std(fun(C), axis=0, ddof=1); J = jkreps(I); vj = fun(J)
    sj = np.sqrt((len(J) - 1)/len(J)*np.sum((vj - vj.mean(0))**2, axis=0)); return np.maximum(sb, sj), sb, sj
def wls(Wt, X, n, d):
    """minimise sum_i w_i (n_i - X_i.theta d_i)^2 / d_i, vectorised over weight rows: returns (R, k)."""
    F = np.einsum("ri,i,ij,ik->rjk", Wt, d, X, X); g = np.einsum("ri,ij,i->rj", Wt, X, n); return np.linalg.solve(F, g[..., None])[..., 0]
# ============================================================== STEP 0: X7 bins and X13 all-source (stop rule)
say("\n=== STEP 0: reproduce X7 (all, terciles, quintiles; A_CAL, sigma_STAT, CAL dchi2) and X13 (all-source) ===")
Mgl = LAB["Mg"]; q5 = np.quantile(Mgl, [0.2, 0.4, 0.6, 0.8]); q3 = np.quantile(Mgl, [1/3, 2/3])
BINS7 = {"quintiles": (np.digitize(Mgl, q5), 100), "terciles": (np.digitize(Mgl, q3), 200)}
ALLI = np.arange(N); dev_a, dev_s, dch, s0rows = [], [], [], {}
def bin_rows(c, ids, key0, nb):
    rows = []
    for k in range(nb):
        I = np.where(ids == k)[0]; n, d = c["n"][I], c["d"][I]
        nr = c["nraw"][I]                                                          # A1: X7's sigma_STAT is the bootstrap/jackknife of the uncalibrated A
        A = float(n.sum()/d.sum()); s, sb, sj = sstat(lambda Wt: ratio_w(Wt, nr, d), I, key0 + k)
        rows.append(dict(I=I, n_cl=len(I), A=A, s=float(s), sb=float(sb), sj=float(sj), kap=float(c["wsum"][I].sum()/d.sum()), dsum=float(d.sum())))
    return rows
def gls_cal(rows, allq, xb_fun, lo_fun, d):
    """X7's GLS (S0, S1, S2) with X7's CAL covariance; sigma_leak,b scaled from the all-cluster value (declared approximation)."""
    y = np.array([r["A"] for r in rows]); st = np.array([r["s"] for r in rows]); dall = d.sum()
    sl = np.array([allq["s_leak"]*math.sqrt(dall/r["dsum"]) for r in rows]); kap = np.array([r["kap"] for r in rows])/allq["kappa_scale"]
    v = allq["s_x_exc"]*kap; u = allq["s_RR_exc"]*kap; Cv = np.diag(st**2 + sl**2) + np.outer(v, v) + np.outer(u, u); Ci = np.linalg.inv(Cv)
    out = {}
    for shp, k in (("S0", 1), ("S1", 2), ("S2", 2)):
        X = []
        for r in rows:
            w = d[r["I"]]
            X.append([1.0] if shp == "S0" else ([1.0, float((w*xb_fun(r["I"])).sum()/w.sum())] if shp == "S1" else
                                                 [float((w*lo_fun(r["I"])).sum()/w.sum()), 1 - float((w*lo_fun(r["I"])).sum()/w.sum())]))
        X = np.array(X); th = np.linalg.solve(X.T @ Ci @ X, X.T @ Ci @ y); res = y - X @ th; c2 = float(res @ Ci @ res)
        out[shp] = dict(theta=th.tolist(), chi2=c2, BIC=c2 + k*math.log(len(y)))
    out["dchi2_S1"] = out["S0"]["chi2"] - out["S1"]["chi2"]; out["dchi2_S2"] = out["S0"]["chi2"] - out["S2"]["chi2"]
    mn = min(out[s]["BIC"] for s in ("S0", "S1", "S2")); out["preferred"] = next(s for s in ("S0", "S1", "S2") if out[s]["BIC"] <= mn + 1e-12)
    out["A"] = y.tolist(); out["sig"] = np.sqrt(np.diag(Cv)).tolist(); return out
XLOG7 = np.log10(Mgl/np.median(Mgl)); LO7 = Mgl < q3[0]
S0 = {}
for f, hk in CELLS:
    c = CELLD[(f, hk)]; cl = f"{f}|{hk}"; allq = X7J["all"][f"C*|boost|{cl}"]["MID"]
    A_all = float(c["nraw"].sum()/c["d"].sum()); Ac_all = float(c["n"].sum()/c["d"].sum())
    s_all, _, _ = sstat(lambda Wt: ratio_w(Wt, c["nraw"], c["d"]), ALLI, 0)
    dev_a += [abs(A_all - allq["A"]), abs(Ac_all - allq["A_CAL"])]; dev_s.append(abs(float(s_all) - allq["s_STAT"]))
    x13 = X13J["reference"][cl]; dx13 = max(abs(A_all - x13["A_ALL"]), abs((A_all - 1)/float(s_all) - x13["Z_ALL_STAT"]))
    S0[cl] = dict(A=A_all, A_CAL=Ac_all, s_STAT=float(s_all), Z_STAT=(A_all - 1)/float(s_all), Z_CAL_x7=allq["Z_CAL"], x13_dev=dx13,
                  x13_sel=X13J["corrections"][cl]["sel"])
    for bn, (ids, k0) in BINS7.items():
        rows = bin_rows(c, ids, k0, int(ids.max()) + 1); ref = X7J["bins"][f"{bn}|{cl}"]
        for r, q in zip(rows, ref): dev_a.append(abs(r["A"] - q["MID"]["A_CAL"])); dev_s.append(abs(r["s"] - q["MID"]["s_STAT"]))
        g = gls_cal(rows, allq, lambda I: XLOG7[I], lambda I: LO7[I].astype(float), c["d"]); tr = X7J["trend"][f"{bn}|{cl}|MID|CAL"]
        dch.append(max(abs(g["dchi2_S1"] - tr["dchi2_S1"]), abs(g["dchi2_S2"] - tr["dchi2_S2"])))
        S0[cl][bn] = dict(A=[r["A"] for r in rows], s=[r["s"] for r in rows], dchi2_S1=g["dchi2_S1"], dchi2_S2=g["dchi2_S2"],
                          x7_dchi2_S1=tr["dchi2_S1"], x7_dchi2_S2=tr["dchi2_S2"])
    say(f"  {f[:3]} {hk}: all A {A_all:.4f} A_CAL {Ac_all:.4f} +-{s_all:.4f} (Z_STAT {(A_all-1)/s_all:+.2f}; X7 Z_CAL {allq['Z_CAL']:+.2f}); X13 all-source dev {dx13:.1e};"
        f" X13 sel-corrected halves (quoted) {S0[cl]['x13_sel']['A']:.3f}+-{S0[cl]['x13_sel']['s']:.3f} (Z {S0[cl]['x13_sel']['Z']:+.2f})")
    for bn in BINS7:
        q = S0[cl][bn]; say(f"     {bn}: A_CAL " + " / ".join(f"{a:.3f}+-{s:.3f}" for a, s in zip(q["A"], q["s"]))
                           + f"  | CAL dchi2 S1 {q['dchi2_S1']:.2f} (X7 {q['x7_dchi2_S1']:.2f}) S2 {q['dchi2_S2']:.2f} (X7 {q['x7_dchi2_S2']:.2f})")
x13dev = max(S0[c]["x13_dev"] for c in S0)
check("K0", max(dev_a + dev_s) <= 1e-9 and x13dev <= 1e-6, f"X7 all/tercile/quintile A_CAL and sigma_STAT max|dev| {max(dev_a + dev_s):.1e} ({len(dev_a + dev_s)} numbers); X13 all-source {x13dev:.1e}",
      "<= 1e-9; <= 1e-6")
say(f"S0-b (reported, not a check): X7 CAL dchi2 S1/S2 reproduced to max |dev| {max(dch):.3f} (line 0.05; per-bin sigma_leak approximated) -> {'OK' if max(dch) <= 0.05 else 'FLAG'}")
RES["step0"] = dict(cells=S0, max_dev=max(dev_a + dev_s), x13_dev=x13dev, S0b_max_dchi2_dev=max(dch), S0b_ok=max(dch) <= 0.05)
STOP = not CHECKS[-1][1] and not MUT
if STOP: say("STOP RULE: step 0 failed; the lane stops here.")
# ============================================================== K2: synthetic plants (real d_i, noiseless)
c0 = CELLD[("canonical", "h0672")]; xs = np.log10(Mgl/np.median(Mgl)); H = (xs >= np.median(xs)).astype(float)
Xj = np.c_[np.ones(N), xs - 0, H]; one = np.ones((1, N))
ns = (1 + 0.8*H)*c0["d"]; th_s = wls(one, Xj, ns, c0["d"])[0]; dstep = float(ns[H == 1].sum()/c0["d"][H == 1].sum() - ns[H == 0].sum()/c0["d"][H == 0].sum())
nl = (1.3 + 0.4*xs)*c0["d"]; th_l = wls(one, Xj, nl, c0["d"])[0]; th_l2 = wls(one, Xj[:, :2], nl, c0["d"])[0]
k2 = max(abs(dstep - 0.8), abs(th_s[2] - 0.8), abs(th_s[1]), abs(th_l[1] - 0.4), abs(th_l[2]), abs(th_l2[1] - 0.4), abs(th_l2[0] - 1.3))
check("K2", k2 <= 1e-9, f"step plant (median step, joint c, b=0) and linear plant (linear b, joint b, c=0) recovered to {k2:.1e}", "<= 1e-9")
# ============================================================== STEP 2: unbinned tests per variable
QG = np.round(np.arange(0.20, 0.8001, 0.05), 2)
VARS = [("V0", "MGAS500 (control)", "Mg", "log"), ("V1", "KT", "KT", "log"), ("V2", "redshift", "Z", "lin"), ("V3", "L500", "L500", "log"),
        ("V4", "c_X = L300kpc/L500", "CX", "lin"), ("V5", "redMaPPer lambda", "LAM", "log"), ("V6", "BCG stellar mass", "BCG", "log"),
        ("V7", "S_cen/gas_cyl", "FSC", "log")]
TEST = {}; BINT = {}
if not STOP:
    say("\n=== STEP 2: unbinned tests per variable (C*, CAL, boost; sigma_STAT = max(boot, jk); permutation p) ===")
    for code, (vk, vname, lk, tr) in enumerate(VARS):
        v = LAB[lk]; okv = np.isfinite(v) & (v > 0); I = np.where(okv)[0]; nI = len(I); vv = v[I]
        x = np.log10(vv/np.median(vv)) if tr == "log" else vv - np.median(vv); xmed = np.median(x); Hm = (x >= xmed).astype(float)
        xM = np.log10(Mgl[I]/np.median(Mgl[I])); rho_s = float(spearmanr(vv, Mgl[I])[0])
        thr = np.quantile(x, QG); HQ = (x[:, None] >= thr[None, :]).astype(float)                # (n, 13)
        rng = np.random.default_rng([RB, 7000 + code]); PI = np.argsort(rng.random((NB, nI)), axis=1)  # 2000 permutations
        TEST[vk] = dict(name=vname, n=nI, spearman_Mgas=rho_s, cells={})
        for f, hk in CELLS:
            c = CELLD[(f, hk)]; n, d = c["n"][I], c["d"][I]; key = 5000 + 10*code
            X1 = np.c_[np.ones(nI), x]; X3 = np.c_[np.ones(nI), x, Hm]; XP = np.c_[np.ones(nI), x, xM]
            b = float(wls(np.ones((1, nI)), X1, n, d)[0, 1]); sb_, _, _ = sstat(lambda Wt: wls(Wt, X1, n, d)[:, 1], I, key)
            def dmed(Wt): return ratio_w(Wt*Hm, n, d) - ratio_w(Wt*(1 - Hm), n, d)
            Dm = float(dmed(np.ones((1, nI)))[0]); sm_, _, _ = sstat(dmed, I, key)
            th3 = wls(np.ones((1, nI)), X3, n, d)[0]; s3, _, _ = sstat(lambda Wt: wls(Wt, X3, n, d), I, key)
            if vk != "V0":
                thp = wls(np.ones((1, nI)), XP, n, d)[0]; sp_, _, _ = sstat(lambda Wt: wls(Wt, XP, n, d), I, key); Zpart = float(thp[1]/sp_[1])
            else: Zpart = float("nan")
            # scanned step, permutation null
            Dq = (HQ.T @ n)/(HQ.T @ d) - ((1 - HQ).T @ n)/((1 - HQ).T @ d)
            nP, dP = n[PI], d[PI]                                                              # permuting labels = permuting (n, d) against fixed x
            DqP = np.stack([(nP*HQ[:, k]).sum(1)/(dP*HQ[:, k]).sum(1) - (nP*(1 - HQ[:, k])).sum(1)/(dP*(1 - HQ[:, k])).sum(1) for k in range(len(QG))], 1)
            sP = DqP.std(0, ddof=1); T = float(np.max(np.abs(Dq)/sP)); kst = int(np.argmax(np.abs(Dq)/sP)); TP = np.max(np.abs(DqP)/sP[None, :], 1)
            p_scan = float(np.mean(TP >= T - 1e-12))
            FPm = np.einsum("ri,ij,ik->rjk", dP, X1, X1); gPm = np.einsum("ri,ij->rj", nP, X1); bP = np.linalg.solve(FPm, gPm[..., None])[:, 1, 0]
            p_lin = float(np.mean(np.abs(bP) >= abs(b) - 1e-15))
            vstar = float(np.quantile(vv, QG[kst]))
            o = dict(b=b, s_b=float(sb_), Z_lin=b/float(sb_), D_med=Dm, s_med=float(sm_), Z_med=Dm/float(sm_), joint=th3.tolist(), s_joint=np.asarray(s3).tolist(),
                     Z_b=float(th3[1]/s3[1]), Z_c=float(th3[2]/s3[2]), p_lin=p_lin, T_scan=T, p_scan=p_scan, q_star=float(QG[kst]), V_star=vstar,
                     D_star=float(Dq[kst]), Z_b_fixed_mass=Zpart, A_sub=float(n.sum()/d.sum()))
            o["dchi2_max"] = max(o["Z_lin"]**2, o["Z_med"]**2); TEST[vk]["cells"][f"{f}|{hk}"] = o
            say(f"  {vk} {vname[:20]:20s} n {nI:3d} {f[:3]} {hk}: A {o['A_sub']:.3f} | lin b {b:+.3f}+-{sb_:.3f} (Z {o['Z_lin']:+.2f}, p_perm {p_lin:.3f}) | med step {Dm:+.3f}+-{sm_:.3f} (Z {o['Z_med']:+.2f})"
                f" | joint Z_b {o['Z_b']:+.2f} Z_c {o['Z_c']:+.2f} | scan T {T:.2f} p {p_scan:.3f} at q {QG[kst]:.2f} (V* {vstar:.3g}, D {Dq[kst]:+.3f}) | Z_b|M {Zpart:+.2f}")
        dmx = [TEST[vk]["cells"][c]["dchi2_max"] for c in TEST[vk]["cells"]]
        cls = "DETECTED" if min(dmx) >= 9 else ("NONE" if max(dmx) < 4 else "WEAK"); shape = None
        if cls == "DETECTED":
            cc = TEST[vk]["cells"].values()
            if all(abs(o["Z_c"]) >= 2 and abs(o["Z_b"]) < 2 and o["p_scan"] <= 0.01 for o in cc): shape = "THRESHOLD"
            elif all(abs(o["Z_b"]) >= 2 and abs(o["Z_c"]) < 2 for o in cc): shape = "SMOOTH"
            else: shape = "SHAPE UNRESOLVED"
        TEST[vk].update(cls=cls, shape=shape, spearman=rho_s); say(f"  -> {vk} {vname}: {cls}" + (f" ({shape})" if shape else "") + f"; Spearman with MGAS500 {rho_s:+.2f}; max dchi2 per cell {[round(z, 2) for z in dmx]}")
        # binned tables (reported, never graded): terciles; quintiles when n >= 300
        BINT[vk] = {}
        for bn, qq in (("terciles", [1/3, 2/3]), ("quintiles", [0.2, 0.4, 0.6, 0.8])):
            if bn == "quintiles" and nI < 300: continue
            ids = np.full(N, -1); ids[I] = np.digitize(x, np.quantile(x, qq)); nb = len(qq) + 1; edges = np.quantile(vv, qq).tolist()
            BINT[vk][bn] = dict(edges=edges, cells={})
            for f, hk in CELLS:
                c = CELLD[(f, hk)]; cl = f"{f}|{hk}"; allq = X7J["all"][f"C*|boost|{cl}"]["MID"]
                rows = bin_rows(c, ids, 20000 + 100*code + (0 if bn == "terciles" else 50), nb)
                xfull = np.full(N, np.nan); xfull[I] = x; lo = np.zeros(N); lo[I] = (x < np.quantile(x, 1/3)).astype(float)
                g = gls_cal(rows, allq, lambda J_: xfull[J_], lambda J_: lo[J_], c["d"])
                BINT[vk][bn]["cells"][cl] = dict(A=[r["A"] for r in rows], s=[r["s"] for r in rows], Z=[(r["A"] - 1)/r["s"] for r in rows], n=[r["n_cl"] for r in rows],
                                                 med=[float(np.median(v[r["I"]])) for r in rows], dchi2_S1=g["dchi2_S1"], dchi2_S2=g["dchi2_S2"], preferred=g["preferred"])
                q = BINT[vk][bn]["cells"][cl]
                say(f"     {bn} {f[:3]} {hk}: " + " / ".join(f"{a:.2f}+-{s:.2f}" for a, s in zip(q["A"], q["s"])) + f"  (medians {', '.join(f'{m:.3g}' for m in q['med'])})"
                    f"  GLS CAL dchi2 S1 {q['dchi2_S1']:.2f} S2 {q['dchi2_S2']:.2f} pref {q['preferred']}")
        say(f"  [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
    NON = [k for k in TEST if k != "V0"]
    thr_v = [k for k in NON if TEST[k]["shape"] == "THRESHOLD"]; smo_v = [k for k in NON if TEST[k]["shape"] == "SMOOTH"]
    if thr_v: TV = "REAL THRESHOLD at " + ", ".join(f"{TEST[k]['name']} V* " + "/".join(f"{TEST[k]['cells'][c]['V_star']:.3g}" for c in TEST[k]["cells"]) for k in thr_v)
    elif smo_v: TV = "SMOOTH TREND in " + ", ".join(TEST[k]["name"] for k in smo_v)
    elif all(TEST[k]["cls"] == "NONE" for k in NON) and TEST["V0"]["cls"] != "DETECTED": TV = "BINNING ARTEFACT"
    else:
        TV = "UNDECIDED"
        if TEST["V0"]["cls"] == "DETECTED" and all(TEST[k]["cls"] == "NONE" for k in NON): TV += " (MGAS500-specific)"
    say(f"\nTREND VERDICT: {TV}   classes: " + "; ".join(f"{k} {TEST[k]['name']}: {TEST[k]['cls']}" + (f" ({TEST[k]['shape']})" if TEST[k]["shape"] else "") for k in TEST))
    RES.update(tests=TEST, binned=BINT, trend_verdict=TV)
# ============================================================== STEP 3: baryon budget
if not STOP:
    say("\n=== STEP 3: baryon budget (needed extra baryons for A_MID,CAL = 1; X2's GS / PS components on C*) ===")
    T3ID = np.digitize(Mgl, q3); SELS = {"all": np.ones(N, bool), "T1": T3ID == 0, "T2": T3ID == 1, "T3": T3ID == 2}
    GRID = {"PS": np.array([0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]), "GS": np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0])}
    CLs = NS2["CL"]; RGm = NS2["RG"]; MSUN = NS2["MSUN"]
    def qfac(cl, hk): h = NS2["HV"][hk]; return (float(NS2["DM"](cl["z"], h))/(1 + cl["z"]))/NS2["DA_lcdm"](cl["z"])
    def dsum(f, hk, comp, lam):
        P = NS2["stack_model"](f, hk, comp=comp, lam=float(lam), **CSTAR)[0]; NS2["PRED"].clear(); return (DAT[hk]["W"][:, JM]*P[:, JM]).sum(1)
    BUD = {}; k3 = []
    for f, hk in CELLS:
        c = CELLD[(f, hk)]; cl = f"{f}|{hk}"; q = np.array([qfac(o, hk) for o in CLs]); Mg5 = np.array([o["Mgas500"] for o in CLs])*q**2.5
        Mg05 = np.array([float(np.interp(0.5, RGm, NS2["gas"](Mg5[i], CLs[i]["R500"]*q[i], "P")[0]))/MSUN for i in range(N)])
        BUD[cl] = {}
        for comp in ("PS", "GS"):
            t1 = time.time(); G_ = np.array([dsum(f, hk, comp, l) if l > 0 else c["d"] for l in GRID[comp]])           # (n_grid, N)
            if comp == "PS":                                                   # A2: clusters with no MID weight have d = 0 exactly; compare absolute there
                d0 = dsum(f, hk, "PS", 0.0); pos = c["d"] > 0
                k3.append(max(float(np.max(np.abs(d0[pos] - c["d"][pos])/c["d"][pos])), float(np.max(np.abs(d0[~pos] - c["d"][~pos]), initial=0.0))))
            for sn, S in SELS.items():
                tgt = float(c["n"][S].sum()); fg = G_[:, S].sum(1)
                if tgt <= fg[0]: BUD[cl].setdefault(sn, {})[comp] = dict(lam=0.0, A=float(tgt/fg[0])); continue
                if tgt > fg[-1]: BUD[cl].setdefault(sn, {})[comp] = dict(lam=float("inf"), A=float(tgt/fg[0])); continue
                k = int(np.searchsorted(fg, tgt)); la, lb, sa, sb2 = GRID[comp][k - 1], GRID[comp][k], fg[k - 1], fg[k]
                lam_ = la + (tgt - sa)*(lb - la)/(sb2 - sa)
                for it in range(6):                                                                    # secant refinement on the true model sum
                    sc = float(dsum(f, hk, comp, lam_)[S].sum())
                    if abs(sc/tgt - 1) < 1e-5: break
                    if sc < tgt: la, sa = lam_, sc
                    else: lb, sb2 = lam_, sc
                    lam_ = la + (tgt - sa)*(lb - la)/(sb2 - sa)
                sc = float(dsum(f, hk, comp, lam_)[S].sum()); k3.append(abs(sc/tgt - 1))
                BUD[cl].setdefault(sn, {})[comp] = dict(lam=float(lam_), A=float(tgt/fg[0]))
            say(f"  {f[:3]} {hk} {comp}: " + "  ".join(f"{sn} A {BUD[cl][sn][comp]['A']:.3f} -> lam {BUD[cl][sn][comp]['lam']:.3f}" for sn in SELS) + f" [{time.time()-t1:.0f} s]")
        # bracket vs need (matched clusters of each selection)
        mt = LAB["matched"]
        for sn, S in SELS.items():
            Sm = S & mt; lps = BUD[cl][sn]["PS"]["lam"]; lgs = BUD[cl][sn]["GS"]["lam"]
            needPS = lps*Mg5[Sm]; needGS = lgs*Mg05[Sm]; Bup = 2.12*LAB["S_up"][Sm]*(1 + 0.196 + 0.196); Bcen = LAB["S_cen"][Sm] - 0.20*LAB["gcyl"][Sm]
            o = BUD[cl][sn]; o.update(n_matched=int(Sm.sum()), need_PS_sum=float(needPS.sum()), need_GS_sum=float(needGS.sum()), need_PS_med=float(np.median(needPS)) if Sm.any() else 0.0,
                                      B_up_sum=float(Bup.sum()), B_cen_sum=float(Bcen.sum()), S_up_sum=float(LAB["S_up"][Sm].sum()),
                                      ratio_need_over_Bup=float(needPS.sum()/Bup.sum()) if Bup.sum() > 0 else float("inf"),
                                      k_ICL=float((needPS.sum() - Bup.sum())/LAB["S_up"][Sm].sum()))
            say(f"     {sn}: matched {o['n_matched']}; need PS sum {o['need_PS_sum']:.3e} (median {o['need_PS_med']:.2e}/cluster), GS sum {o['need_GS_sum']:.3e} | "
                f"bracket generous {o['B_up_sum']:.3e}, central {o['B_cen_sum']:.3e} | need/B_up {o['ratio_need_over_Bup']:.1f} | k_ICL {o['k_ICL']:.1f}")
    check("K3", max(k3) <= 1e-4, f"lambda solver: max rel |model sum - target| {max(k3):.1e}; lambda = 0 reproduces C* (included)", "<= 1e-4")
    # mass dependence (measured clusters only, not imputed)
    MD = {}
    for sn in ("T1", "T2", "T3"):
        S = SELS[sn] & LAB["meas"]
        MD[sn] = dict(n=int(S.sum()), Scen_over_gas=float(np.median(LAB["S_cen"][S]/LAB["gcyl"][S])), Sup_over_gas=float(np.median(LAB["S_up"][S]/LAB["gcyl"][S])),
                      lam_PS={c: BUD[c][sn]["PS"]["lam"] for c in BUD}, lam_GS={c: BUD[c][sn]["GS"]["lam"] for c in BUD}, Mgas500_med=float(np.median(Mgl[SELS[sn]])))
        say(f"  mass dependence {sn}: median Mgas500 {MD[sn]['Mgas500_med']:.2e}; measured {MD[sn]['n']}: S_cen/gas_cyl {MD[sn]['Scen_over_gas']:.3f}, S_up/gas_cyl {MD[sn]['Sup_over_gas']:.3f};"
            f" needed PS lam (need/Mg500) " + " / ".join(f"{v:.3f}" for v in MD[sn]["lam_PS"].values()) + "; GS lam " + " / ".join(f"{v:.3f}" for v in MD[sn]["lam_GS"].values()))
    match = {}
    for cl in BUD:
        dn = BUD[cl]["T3"]["PS"]["lam"] - BUD[cl]["T1"]["PS"]["lam"]; db = MD["T3"]["Sup_over_gas"] - MD["T1"]["Sup_over_gas"]
        match[cl] = "MATCH" if np.sign(dn) == np.sign(db) else "MISMATCH"
    closes = all(all(BUD[cl][t]["B_up_sum"] >= BUD[cl][t]["need_PS_sum"] for t in ("T2", "T3")) and match[cl] == "MATCH" for cl in BUD)
    insuff = all(any(BUD[cl][t]["B_up_sum"] < BUD[cl][t]["need_PS_sum"] and BUD[cl][t]["k_ICL"] > 10 for t in ("T2", "T3")) for cl in BUD)
    BV = "BARYON BUDGET CLOSES IT" if closes else ("BARYON BUDGET INSUFFICIENT" if insuff else "UNDECIDED")
    say(f"\nBUDGET VERDICT: {BV}   mass dependence {match}; need/B_up T2 " + " / ".join(f"{BUD[c]['T2']['ratio_need_over_Bup']:.1f}" for c in BUD)
        + " T3 " + " / ".join(f"{BUD[c]['T3']['ratio_need_over_Bup']:.1f}" for c in BUD) + "; k_ICL T2 " + " / ".join(f"{BUD[c]['T2']['k_ICL']:.1f}" for c in BUD)
        + " T3 " + " / ".join(f"{BUD[c]['T3']['k_ICL']:.1f}" for c in BUD))
    RES.update(budget=BUD, mass_dependence=MD, mass_dependence_match=match, budget_verdict=BV)
pk = rss(); check("K4", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
npass = sum(ok for _, ok in CHECKS); RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk, N=N)
say(f"X21 COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x21_switch_anatomy_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
sys.exit(0 if npass == len(CHECKS) else 1)
