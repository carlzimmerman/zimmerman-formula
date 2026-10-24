"""X11_cross_shear_diagnosis analysis (criteria 9a105431c9): is X7's cross-shear MID offset a systematic (named by a
pre-declared split or correlation) or consistent with a fluctuation; nulls; E-mode systematics; Z_MID re-derived.
Inputs: the step-0 products (X7's code on the rebuilt cache: scratch x7_measure_percluster.npz, x7_measure_extras.npz,
this lane's x11_s0_x7_psf_regression_results.json), x11_measure_classes.npz, x11_randoms.npz (scratch), the edges JSON,
X7's committed analysis JSON (K1), X2's functions (C* model; exec'd read-only via X7's analysis source text, sha-checked).
Usage: x11_analysis.py <scratch dir> <x11 cache> [--mutate]
--mutate: the tangential data replace the cross in the split machinery (K1 must FAIL).
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, math, time, hashlib, resource
sys.dont_write_bytecode = True
import numpy as np
from scipy.stats import chi2 as CHI2
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; SOUT, CACHE = ARGS[0], ARGS[1]
OUTF = open(os.path.join(HERE, f"x11_analysis{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
# ============================================================== X7's setup + statistic machinery, exec'd read-only (sha-checked)
X7DIR = os.path.join(REB, "X7_cluster_core_significance"); X7SRC = os.path.join(X7DIR, "x7_analysis.py"); X7RAW = open(X7SRC, "rb").read()
assert hashlib.sha256(X7RAW).hexdigest() == "0acb1574c1cd6f44762598635490d218c410caaddb90ea4b5f4088b28d03a7f9", "X7 analysis source changed"
TX7 = X7RAW.decode(); RES["x7_analysis_sha256"] = hashlib.sha256(X7RAW).hexdigest()
def cut7(a, b): i = TX7.index(a); j = TX7.index(b, i); return TX7[i:j]
SEG1 = cut7("# ============================================================== X2's own functions", "# ============================================================== K0: X2 reproduction")
SEG2 = cut7("# ============================================================== my data (this lane's replay)", "# ============================================================== implementation checks K2")
for old, new, n in (('os.path.join(HERE, "x7_measure_percluster.npz")', 'os.path.join(SOUT, "x7_measure_percluster.npz")', 2),
                    ('os.path.join(HERE, "x7_psf_regression_results.json")', 'os.path.join(HERE, "x11_s0_x7_psf_regression_results.json")', 1)):
    assert SEG2.count(old) == n, old; SEG2 = SEG2.replace(old, new)
def check_s0(name, ok, val, thr): check("S0-" + name, ok, val, thr)
NS7 = {"np": np, "os": os, "sys": sys, "math": math, "json": json, "time": time, "hashlib": hashlib, "REB": REB, "REPO": REPO, "HERE": HERE, "SOUT": SOUT,
       "MUT": False, "RES": {}, "say": say, "check": check_s0, "sha": sha, "rss": rss, "T0": T0, "CHI2": CHI2}
exec(compile(SEG1, X7SRC, "exec"), NS7); exec(compile(SEG2, X7SRC, "exec"), NS7)
for k in ("x2_source_sha256", "f1_source_sha256", "f2_aqual_sha256", "my_npz_sha256", "extras_sha256"): RES["step0_" + k] = NS7["RES"].get(k)
FEET, HK, CELLS, BN = NS7["FEET"], NS7["HK"], NS7["CELLS"], NS7["BN"]; MY = NS7["MY"]; XE = NS7["XE"]; DAT = NS7["DAT"]; PM = NS7["PM"]
ROT = NS7["ROT"]; R = NS7["R"]; N = NS7["N"]; PATCH = NS7["PATCH"]; ALL = NS7["ALL"]; Cell = NS7["Cell"]; summ = NS7["summ"]; NS2 = NS7["NS2"]; CSTAR = NS7["CSTAR"]
HXI = {"h0672": 0, "h0686": 1}; HI = {"h070": 0, "h0672": 1, "h0686": 2}; MIDJ = [3, 4, 5]
X7J = json.load(open(os.path.join(X7DIR, "x7_analysis_results.json")))
# ============================================================== this lane's products
_XM = np.load(os.path.join(SOUT, "x11_measure_classes.npz")); XM = {k: _XM[k] for k in _XM.files if k != "rotRx"}; del _XM
_RX = np.load(os.path.join(SOUT, "x11_randoms.npz")); RX = {k: _RX[k] for k in _RX.files}; del _RX
RES["classes_npz_sha256"] = sha(os.path.join(SOUT, "x11_measure_classes.npz")); RES["randoms_npz_sha256"] = sha(os.path.join(SOUT, "x11_randoms.npz"))
assert [str(s) for s in XM["name"]] == [str(s) for s in MY["name"]] == [str(s) for s in RX["name"]], "cluster order"
VN = [str(v) for v in XM["varnames"]]; VK = [int(k) for k in XM["varsizes"]]; OFF = {}; _o = 0
for v, k in zip(VN, VK): OFF[v] = _o; _o += k
EDG = json.load(open(os.path.join(CACHE, "x11_edges.json")))
SRCV = [v for v in VN if v != "ALL"]                                                          # 12 source variables
z = np.asarray(MY["z"], float); Mg = np.asarray(MY["Mgas500"], float); ra = np.asarray(MY["ra"], float)
fm = np.asarray(XM["f_main"], float); m2a = np.asarray(XM["m2"], float); off = np.asarray(XM["off_deg"], float)
# A3 (POST-RESULT bug fix): 14 clusters have no MID source at h 0.672, so f_main and m2 are NaN there and np.median returned NaN
# (one class only). The medians are now taken over the defined values (nanmedian); the 14 clusters (zero MID weight) go to class 0.
CLV = {"patch": np.where((ra > 100) & (ra < 260), 0, 1), "z2": (z > np.median(z)).astype(int),
       "mass3": np.digitize(Mg, np.quantile(Mg, [1/3, 2/3])), "straddle2": (np.nan_to_num(fm, nan=-1.0) >= np.nanmedian(fm)).astype(int),
       "aniso2": (np.nan_to_num(m2a, nan=-1.0) >= np.nanmedian(m2a)).astype(int), "off2": (off >= np.median(off)).astype(int)}
RES["n_clusters_without_MID_h0672"] = int(np.isnan(fm).sum())
VARLIST = SRCV + ["radial3"] + list(CLV)                                                      # 19 graded variables
VIDX = {v: i for i, v in enumerate(VARLIST)}
RES["cluster_split_medians"] = dict(z=float(np.median(z)), f_main=float(np.nanmedian(fm)), m2=float(np.nanmedian(m2a)), off_deg=float(np.median(off)),
                                    mass_edges=np.quantile(Mg, [1/3, 2/3]).tolist(), n_per_class={k: np.bincount(v).tolist() for k, v in CLV.items()})
say(f"\nclusters {N}; source variables {SRCV}; cluster variables {list(CLV)} (+ radial3); per-class cluster counts {RES['cluster_split_medians']['n_per_class']}")
# ============================================================== split machinery
NB = 2000
def bidx(key):
    return np.random.default_rng([20261024, key]).integers(0, N, size=(NB, N))
BIDX = {v: bidx(900 + VIDX[v]) for v in VARLIST}
def hart(n, K): return (n - K - 2)/(n - 1)
def src_split(f, hk, conv, var, chan):
    """per-class MID statistic for a source variable: a (K,), rotations (K, R), per-cluster numerators/denominators (N, K)."""
    hi = HXI[hk]; sl = slice(OFF[var], OFF[var] + VK[VN.index(var)])
    key = "Dx" if chan == "x" else "D"
    if MUT and chan == "x": key = "D"
    D = XM[key][:, hi, sl][:, :, MIDJ]; Et = XM["E"][:, hi, sl][:, :, MIDJ]; W = np.where(Et < 1e8, 1/Et**2, 0)
    if conv == "boost":
        with np.errstate(invalid="ignore", divide="ignore"): B = np.nan_to_num(XM["den"][:, hi, sl].sum(0)/XM["den_r"][:, hi, sl].sum(0))[:, MIDJ]
    else: B = np.ones((sl.stop - sl.start, 3))
    P = PM[("C*", f, hk)][:, MIDJ]; WB = W*B[None]
    num = (WB*D).sum(-1); den = (W*P[:, None, :]).sum(-1)
    rot = np.einsum("nkj,nkjr->kr", WB, XM["rot"][:, hi, sl].astype(np.float64)) if chan == "x" else None
    with np.errstate(invalid="ignore", divide="ignore"):
        a = num.sum(0)/den.sum(0); ar = rot/den.sum(0)[:, None] if rot is not None else None
    return a, ar, num, den
CELLOBJ = {}
def cellobj(f, hk, conv):
    if (f, hk, conv) not in CELLOBJ: CELLOBJ[(f, hk, conv)] = Cell("C*", f, hk, conv)
    return CELLOBJ[(f, hk, conv)]
def cl_split(f, hk, conv, var, chan):
    """per-class MID statistic for a cluster variable (X7's Cell arrays and rotations) or the radial bins."""
    ce = cellobj(f, hk, conv)
    if var == "radial3":
        d = DAT[hk]; Bc = d["B"] if conv == "boost" else np.ones(8); W = d["W"]; P = PM[("C*", f, hk)]
        Dd = d["Dx"] if (chan == "x" and not MUT) else d["D"]
        num = (W*Bc[None]*Dd)[:, MIDJ]; den = (W*P)[:, MIDJ]
        rot = np.einsum("nj,nrj->jr", (W*Bc[None])[:, MIDJ], ROT[:, HXI[hk], :, 1][:, :, MIDJ].astype(np.float64)) if chan == "x" else None
        return num.sum(0)/den.sum(0), (rot/den.sum(0)[:, None] if rot is not None else None), num, den
    cls = CLV[var]; K = int(cls.max()) + 1; ch = "x" if (chan == "x" and not MUT) else "t"
    numc = ce.num[ch][:, 1]; denc = ce.den[:, 1]
    num = np.stack([np.where(cls == k, numc, 0.0) for k in range(K)], 1); den = np.stack([np.where(cls == k, denc, 0.0) for k in range(K)], 1)
    rot = np.stack([ce.rot[cls == k][:, :, 1, 1].sum(0) for k in range(K)], 0) if chan == "x" else None
    return num.sum(0)/den.sum(0), (rot/den.sum(0)[:, None] if rot is not None else None), num, den
def split(f, hk, conv, var, chan):
    return cl_split(f, hk, conv, var, chan) if (var in CLV or var == "radial3") else src_split(f, hk, conv, var, chan)
def boot_cov(num, den, var):
    I = BIDX[var]; ab = num[I].sum(1)/den[I].sum(1); return np.cov(ab.T, ddof=1).reshape(num.shape[1], num.shape[1]), ab
def gls_tests(a, C, nreal):
    K = len(a); Ci = np.linalg.inv(C)*hart(nreal, K)
    def fit(X):
        F = X.T @ Ci @ X; th = np.linalg.solve(F, X.T @ Ci @ a); r = a - X @ th; return th, float(r @ Ci @ r)
    th0, c0 = fit(np.ones((K, 1)))
    if K >= 3: th1, c1 = fit(np.stack([np.ones(K), np.arange(K) - (K - 1)/2], 1)); dch = c0 - c1
    else: th1, dch = None, c0
    p = float(CHI2.sf(c0, K - 1))
    return dict(const=float(th0[0]), chi2_const=c0, p_const=p, dchi2=float(dch), slope=(float(th1[1]) if th1 is not None else None),
                cand=bool(dch >= 9 or p < 0.0027))
def zstat_class(f, hk, v, classes, conv="boost"):
    a, _, num, den = split(f, hk, conv, v, "t"); n_ = num[:, classes].sum(1); d_ = den[:, classes].sum(1); A = n_.sum()/d_.sum()
    I = BIDX[v]; sb = float(np.std(n_[I].sum(1)/d_[I].sum(1), ddof=1))
    reps = [n_[PATCH != p].sum()/d_[PATCH != p].sum() for p in range(30)]; sj = float(np.sqrt(29/30*np.sum((np.array(reps) - np.mean(reps))**2)))
    s = max(sb, sj); return dict(A=float(A), s_boot=sb, s_jk=sj, s_STAT=s, Z_STAT=float((A - 1)/s))
# ============================================================== K1: ALL class / cluster machinery = X7
k1 = []
for f, hk in CELLS:
    xj = X7J["all"][f"C*|boost|{f}|{hk}"]["MID"]
    a, ar, _, _ = src_split(f, hk, "boost", "ALL", "x"); k1.append(abs(a[0] - xj["A_x"]))
    so = summ(cellobj(f, hk, "boost"), ALL, 0)["MID"]; k1 += [abs(so["s_n_x"] - xj["s_n_x"]), abs(so["p_x"] - xj["p_x"]), abs(so["A_x"] - xj["A_x"]),
                                                             abs(so["Z_STAT"] - xj["Z_STAT"]), abs(so["Z_CAL"] - xj["Z_CAL"])]
    RES.setdefault("all_source_class_rot_sigma_vs_x7", {})[f"{f}|{hk}"] = [float(ar[0].std(ddof=1)), xj["s_n_x"]]
check("K1", max(k1) <= 1e-9, f"ALL source class A_x and X7's machinery (A_x, s_n_x, p_x, Z_STAT, Z_CAL) vs X7's committed JSON: max|diff| {max(k1):.1e}"
      f" (ALL-class own-rotation sigma vs X7: {[[round(v, 5) for v in x] for x in RES['all_source_class_rot_sigma_vs_x7'].values()]})", "<= 1e-9")
# ============================================================== K2: injection tests of the GLS machinery
a0, ar0, _, _ = src_split("canonical", "h0672", "boost", "mag4", "x"); C0 = np.cov(ar0, ddof=1)
t0 = gls_tests(a0, C0, R); t1 = gls_tests(a0 + 0.5, C0, R); sg = np.sqrt(np.diag(C0)); ai = a0.copy(); ai[0] += 10*sg[0]; t2 = gls_tests(ai, C0, R)
k2 = max(abs(t1["dchi2"] - t0["dchi2"]), abs(t1["chi2_const"] - t0["chi2_const"]))
check("K2", k2 <= 1e-9 and t2["cand"], f"constant added: |d dchi2|, |d chi2_const| {k2:.1e}; 10 sigma in one class -> candidate {t2['cand']} (dchi2 {t2['dchi2']:.1f})", "<= 1e-9; True")
RJ = json.load(open(os.path.join(HERE, "x11_randoms_results.json"))); MJ = json.load(open(os.path.join(HERE, "x11_measure_results.json")))
check("K3", RJ["checks"]["R1"]["pass_"], f"x11_randoms R1 (F1 randoms re-measured, this code path): {RJ['checks']['R1']['value']}", "PASS")
# ============================================================== STEP 1-2: the cross-offset splits, tests, candidates
say("\n=== STEP 1-2: cross-shear MID offset by split (A units; C*, boost; rotated-noise sigma; p two-sided from 200 rotations) ===")
SPL = {}
for f, hk in CELLS:
    for v in VARLIST:
        a, ar, num, den = split(f, hk, "boost", v, "x"); ok = np.isfinite(a) & (den.sum(0) > 0)
        a, ar, num, den = a[ok], ar[ok], num[:, ok], den[:, ok]
        Cr = np.cov(ar, ddof=1).reshape(len(a), len(a)); sg = np.sqrt(np.diag(Cr)); Cb, ab = boot_cov(num, den, v)
        tr = gls_tests(a, Cr, R); tb = gls_tests(a, Cb, NB)
        pk = [float(np.mean(np.abs(ar[k]) >= abs(a[k]))) for k in range(len(a))]
        SPL[(f, hk, v)] = dict(a=a.tolist(), sig=sg.tolist(), Z=(a/sg).tolist(), p=pk, sig_boot=np.sqrt(np.diag(Cb)).tolist(), rot=tr, boot=tb,
                               cand_rot=tr["cand"], cand_boot=tb["cand"], classes_used=np.nonzero(ok)[0].tolist(), _ar=ar, _Cr=Cr)
for v in VARLIST:
    rows = []
    for f, hk in CELLS:
        s = SPL[(f, hk, v)]
        rows.append(f"{f[:3]} {hk}: " + " ".join(f"{a:+.3f}+-{g:.3f}" for a, g in zip(s["a"], s["sig"])) +
                    f" | chi2c {s['rot']['chi2_const']:.2f} p {s['rot']['p_const']:.3f} dchi2 {s['rot']['dchi2']:.2f}{' CAND' if s['cand_rot'] else ''}"
                    f" (boot dchi2 {s['boot']['dchi2']:.2f}{' CAND' if s['cand_boot'] else ''})")
    say(f"-- {v}"); [say("   " + r) for r in rows]
CAND4 = {v: all(SPL[(f, hk, v)]["cand_rot"] for f, hk in CELLS) for v in VARLIST}
ROB4 = {v: all(SPL[(f, hk, v)]["cand_rot"] and SPL[(f, hk, v)]["cand_boot"] for f, hk in CELLS) for v in VARLIST}
ANY = {v: [f"{f}|{hk}" for f, hk in CELLS if SPL[(f, hk, v)]["cand_rot"]] for v in VARLIST}
say("candidates (rotation covariance) per variable, cells: " + "; ".join(f"{v}: {c}" for v, c in ANY.items() if c) if any(ANY.values()) else "candidates: none in any cell")
# look-elsewhere: the candidate rule on each rotated realisation (C_rot fixed)
LE = {}
for f, hk in CELLS:
    hit = np.zeros(R, bool)
    for v in VARLIST:
        s = SPL[(f, hk, v)]
        for r in range(R): hit[r] |= gls_tests(s["_ar"][:, r], s["_Cr"], R)["cand"]
    LE[f"{f}|{hk}"] = float(hit.mean())
say(f"empirical look-elsewhere rate (fraction of the 200 rotated realisations with >= 1 candidate among {len(VARLIST)} variables): {LE}")
# ============================================================== nulls
say("\n=== nulls ===")
NUL = {}
for f, hk in CELLS:
    so = summ(cellobj(f, hk, "boost"), ALL, 0)["MID"]; d = DAT[hk]; W = d["W"]; Bc = d["B"]; P = PM[("C*", f, hk)]; hi = HXI[hk]
    den = (W*P)[:, MIDJ].sum(); WB = (W*Bc[None])[:, MIDJ]
    ae = float((WB*RX["Rx"][:, hi][:, MIDJ]).sum()/den); aer = np.einsum("nj,njr->r", WB, RX["rot"][:, hi].astype(np.float64))/den
    at_e = float((WB*RX["Rt"][:, hi][:, MIDJ]).sum()/den)
    # cluster raw cross minus the extended random mean (reported): cluster-only rotations = ROT x + ROT random-mean x
    craw = MY["Drawx"][:, HI[hk]][:, MIDJ]; ac = float((WB*(craw - RX["Rx"][:, hi][:, MIDJ])).sum()/den)
    crot = (ROT[:, hi, :, 1] + ROT[:, hi, :, 4])[:, :, MIDJ].astype(np.float64); acr = (np.einsum("nj,nrj->r", WB, crot) - np.einsum("nj,njr->r", WB, RX["rot"][:, hi].astype(np.float64)))/den
    # N3 excess variance (per-cluster MID cross, rotation sigma)
    wbs = WB.sum(1); xi = (WB*d["Dx"][:, MIDJ]).sum(1)/wbs; xr = np.einsum("nj,nrj->nr", WB, ROT[:, hi, :, 1][:, :, MIDJ].astype(np.float64))/wbs[:, None]
    si = xr.std(1, ddof=1); okc = (si > 0) & np.isfinite(xi) & np.all(np.isfinite(xr), 1); c2 = float(np.sum(xi[okc]**2/si[okc]**2)); dist = np.sum(xr[okc]**2/si[okc, None]**2, 0)
    NUL[f"{f}|{hk}"] = dict(rand_F1=so["rand_x"], Z_rand_F1=so["Z_rand_x"], rand_ext=ae, sig_rand_ext=float(aer.std(ddof=1)), Z_rand_ext=ae/float(aer.std(ddof=1)),
                            rand_ext_t=at_e, cluster_minus_ext=ac, sig_cluster_minus_ext=float(acr.std(ddof=1)), p_cluster_minus_ext=float(np.mean(np.abs(acr) >= abs(ac))),
                            A_x=so["A_x"], s_n_x=so["s_n_x"], p_x=so["p_x"], chi2_cl=c2, n_cl=int(okc.sum()), p_var=float(np.mean(dist >= c2)), chi2_cl_null_mean=float(dist.mean()))
    q = NUL[f"{f}|{hk}"]
    say(f"  {f[:3]} {hk}: N1 F1 randoms x {q['rand_F1']:+.4f} (Z {q['Z_rand_F1']:+.2f}); extended randoms x {q['rand_ext']:+.4f}+-{q['sig_rand_ext']:.4f} (Z {q['Z_rand_ext']:+.2f}), t {q['rand_ext_t']:+.4f}"
        f" | cluster - extended randoms x {q['cluster_minus_ext']:+.4f}+-{q['sig_cluster_minus_ext']:.4f} (p {q['p_cluster_minus_ext']:.3f}) vs graded A_x {q['A_x']:+.4f}+-{q['s_n_x']:.4f} (p {q['p_x']:.3f})"
        f" | N3 chi2_cl {q['chi2_cl']:.1f} / {q['n_cl']} (rotations mean {q['chi2_cl_null_mean']:.1f}), p_var {q['p_var']:.3f}")
N1 = all(abs(q["Z_rand_F1"]) < 3 and abs(q["Z_rand_ext"]) < 3 for q in NUL.values())
N2 = MJ["checks"]["M4"]["pass_"]; N3 = all(q["p_var"] >= 0.0027 for q in NUL.values())
say(f"  N1 random points |Z| < 3: {N1}; N2 90-degree identity: {N2} ({MJ['checks']['M4']['value']}); N3 excess variance p >= 0.0027: {N3}")
RES["nulls"] = NUL; RES["N1"], RES["N2"], RES["N3"] = N1, N2, N3
# ============================================================== E-mode systematics
say("\n=== E-mode systematics (reported sub-verdicts) ===")
hi0 = HXI["h0672"]
def qratio(k, hi=hi0):
    c = XM["cnt"][:, hi, k][:, MIDJ].sum(1); cr = XM["cnt_r"][:, hi, k][:, MIDJ].sum(1); I = bidx(950)
    return float(c.sum()/cr.sum() - 1), float(np.std(c[I].sum(1)/cr[I].sum(1), ddof=1))
EM = {"deficit": {}}
for lab, k in [("ALL", 0)] + [(f"mag2_{c}", OFF["mag2"] + c) for c in range(2)] + [(f"nbr2_{c}", OFF["nbr2"] + c) for c in range(2)]:
    d_, s_ = qratio(k); EM["deficit"][lab] = dict(Q_minus_1=d_, sig=s_)
    bins = (XM["cnt"][:, hi0, k].sum(0)/XM["cnt_r"][:, hi0, k].sum(0) - 1).tolist(); EM["deficit"][lab]["per_bin"] = bins
B672 = DAT["h0672"]["B"]; EM["weighted_boost_B_h0672"] = B672.tolist()
say("  E1 count deficit Q-1 (MID, h 0.672): " + "; ".join(f"{k} {v['Q_minus_1']:+.4f}+-{v['sig']:.4f}" for k, v in EM["deficit"].items())
    + f" | per bin (ALL) {np.round(EM['deficit']['ALL']['per_bin'], 4).tolist()} | X7 weighted boost B-1 {np.round(B672 - 1, 4).tolist()}")
SLP = EDG["count_slope"]; EM["mag"] = {}
for f, hk in CELLS:
    hi = HXI[hk]; KAP = NS2["stack_model"](f, hk, **CSTAR)[3]; m3 = MY["m3to8"][:, HI[hk], 0]; m2 = MY["den"][:, HI[hk]]
    with np.errstate(invalid="ignore", divide="ignore"):
        Sb = np.nan_to_num(KAP*m2/m3); misc = np.nan_to_num(XM["sisc"][:, hi, 0]/XM["cnt"][:, hi, 0])
    kap = Sb*misc; w_ = XM["cnt_r"][:, hi, 0][:, MIDJ]; kbar = float((w_*kap[:, MIDJ]).sum()/w_.sum())
    A = summ(cellobj(f, hk, "boost"), ALL, 0)["MID"]["A"]
    preds = {f"{al}|{sc}": 2*(SLP[al]["alpha"] - 1)*kbar*(A if sc == "xA" else 1.0) for al in SLP for sc in ("law", "xA")}
    dm, sg = qratio(0, hi); lo, hi_ = min(preds.values()), max(preds.values())
    sub = "CONSISTENT WITH MAGNIFICATION" if lo - 2*sg <= dm <= hi_ + 2*sg else ("EXCESS DEFICIT" if dm < lo - 2*sg else "EXCESS COUNTS")
    EM["mag"][f"{f}|{hk}"] = dict(kappa_law_MID=kbar, A_MID=A, pred=preds, bracket=[lo, hi_], measured=dm, sig=sg, sub=sub,
                                   f_obs=(float(lo - dm) if sub == "EXCESS DEFICIT" else 0.0), central=preds["central|xA"])
    say(f"  E2 {f[:3]} {hk}: kappa(law, MID, count-weighted) {kbar:.4f}, x A_MID {A:.3f}; magnification prediction central {preds['central|xA']:+.4f}, bracket [{lo:+.4f}, {hi_:+.4f}]"
        f" vs measured {dm:+.4f}+-{sg:.4f} -> {sub}")
# E3 tangential splits (paired bootstrap covariance)
TSP = {}
for f, hk in CELLS:
    for v in VARLIST:
        a, _, num, den = split(f, hk, "boost", v, "t"); ok = np.isfinite(a) & (den.sum(0) > 0); a, num, den = a[ok], num[:, ok], den[:, ok]
        Cb, ab = boot_cov(num, den, v); tb = gls_tests(a, Cb, NB); TSP[(f, hk, v)] = dict(a=a.tolist(), sig=np.sqrt(np.diag(Cb)).tolist(), boot=tb, cand=tb["cand"])
E3 = {v: all(TSP[(f, hk, v)]["cand"] for f, hk in CELLS) for v in VARLIST}
for v in VARLIST:
    say(f"  E3 {v:9s}: " + " | ".join(f"{f[:3]} {hk[1:]} " + " ".join(f"{a:.3f}" for a in TSP[(f, hk, v)]["a"]) +
                                    f" (dchi2 {TSP[(f, hk, v)]['boot']['dchi2']:.2f}, p {TSP[(f, hk, v)]['boot']['p_const']:.3f}{', CAND' if TSP[(f, hk, v)]['cand'] else ''})" for f, hk in CELLS))
# A4 (POST-RESULT, reporting only, no verdict weight): E3 under the clipped boost; per-class boost and count ratio (MID);
# per-class tangential Z_STAT for the size and magnitude classes.
TSPc = {}
for f, hk in CELLS:
    for v in VARLIST:
        a, _, num, den = split(f, hk, "clip", v, "t"); ok = np.isfinite(a) & (den.sum(0) > 0); a, num, den = a[ok], num[:, ok], den[:, ok]
        Cb, ab = boot_cov(num, den, v); TSPc[(f, hk, v)] = dict(a=a.tolist(), sig=np.sqrt(np.diag(Cb)).tolist(), boot=gls_tests(a, Cb, NB))
for v in ("size2", "size4", "mag2", "nbr2", "tomo"):
    say(f"  E3 clip {v:6s}: " + " | ".join(f"{f[:3]} {hk[1:]} " + " ".join(f"{a:.3f}" for a in TSPc[(f, hk, v)]["a"]) + f" (dchi2 {TSPc[(f, hk, v)]['boot']['dchi2']:.2f}, p {TSPc[(f, hk, v)]['boot']['p_const']:.4f})" for f, hk in CELLS))
PCB = {}
for v in SRCV:
    sl = slice(OFF[v], OFF[v] + VK[VN.index(v)])
    with np.errstate(invalid="ignore", divide="ignore"):
        PCB[v] = dict(B_MID=(XM["den"][:, 0, sl][:, :, MIDJ].sum((0, 2))/XM["den_r"][:, 0, sl][:, :, MIDJ].sum((0, 2))).tolist(),
                      Q_MID=(XM["cnt"][:, 0, sl][:, :, MIDJ].sum((0, 2))/XM["cnt_r"][:, 0, sl][:, :, MIDJ].sum((0, 2))).tolist())
say("  per-class MID boost B and count ratio Q (h 0.672): " + "; ".join(f"{v} B {np.round(q['B_MID'], 3).tolist()} Q {np.round(q['Q_MID'], 3).tolist()}" for v, q in PCB.items()))
ZCL = {f"{f}|{hk}|{v}|{c}": zstat_class(f, hk, v, [c]) for f, hk in CELLS for v in ("size2", "mag2") for c in range(2)}
for v in ("size2", "mag2"):
    say(f"  tangential Z_MID,STAT per {v} class: " + "; ".join(f"{f[:3]} {hk}: " + " / ".join(f"A {ZCL[f'{f}|{hk}|{v}|{c}']['A']:.3f}+-{ZCL[f'{f}|{hk}|{v}|{c}']['s_STAT']:.3f} Z {ZCL[f'{f}|{hk}|{v}|{c}']['Z_STAT']:+.2f}" for c in range(2)) for f, hk in CELLS))
RES["E3_clip"] = {f"{f}|{hk}|{v}": TSPc[(f, hk, v)] for f, hk in CELLS for v in VARLIST}; RES["per_class_boost_count"] = PCB; RES["tangential_Z_per_class"] = ZCL
E3N = [v for v, c in E3.items() if c]; E3SUB = ("E-MODE SOURCE/CLUSTER DEPENDENCE FOUND: " + ", ".join(E3N)) if E3N else "NONE"
say(f"  E3 sub-verdict: {E3SUB}")
# nbr2 far half (class 1) Z_STAT; E4 clipped boost
EM["nbr_far"] = {f"{f}|{hk}": zstat_class(f, hk, "nbr2", [1]) for f, hk in CELLS}
EM["clip"] = {f"{f}|{hk}": {k: summ(cellobj(f, hk, "clip"), ALL, 0)["MID"][k] for k in ("A", "Z_STAT", "A_CAL", "Z_CAL")} for f, hk in CELLS}
say("  nbr2 far-neighbour half Z_MID,STAT: " + "; ".join(f"{k} A {v['A']:.3f}+-{v['s_STAT']:.3f} Z {v['Z_STAT']:+.2f}" for k, v in EM["nbr_far"].items()))
say("  E4 clipped boost (B = 1): " + "; ".join(f"{k} A {v['A']:.3f} Z_STAT {v['Z_STAT']:+.2f} Z_CAL {v['Z_CAL']:+.2f}" for k, v in EM["clip"].items()))
RES["emode"] = EM; RES["E3"] = {f"{f}|{hk}|{v}": TSP[(f, hk, v)] for f, hk in CELLS for v in VARLIST}; RES["E3_sub"] = E3SUB
# ============================================================== verdict and Z_MID
say("\n=== verdict ===")
def v1(zs): return "REAL" if min(zs) >= 3 else ("NOT SIGNIFICANT" if min(zs) < 2 else "MARGINAL")
ALLS = {f"{f}|{hk}": summ(cellobj(f, hk, "boost"), ALL, 0)["MID"] for f, hk in CELLS}
named = [v for v in VARLIST if ROB4[v]]; anyc = any(len(c) > 0 for c in ANY.values())
pre = all(ok for _, ok in CHECKS)
if not pre: VERD = "UNDECIDED"; why = "a precondition check failed"
elif named: VERD = "SYSTEMATIC IDENTIFIED"; why = f"robust candidate(s) in all 4 cells: {named}"
elif not anyc and N1 and N2 and N3: VERD = "CONSISTENT WITH A FLUCTUATION"; why = "no candidate in any cell; N1, N2, N3 pass"
else: VERD = "UNDECIDED"; why = f"candidates {dict((v, c) for v, c in ANY.items() if c)}; N1 {N1} N2 {N2} N3 {N3}"
ZM = {}
if VERD == "SYSTEMATIC IDENTIFIED":
    v = named[0]
    for f, hk in CELLS:
        s = SPL[(f, hk, v)]; cu = s["classes_used"]; Zk = np.array(s["Z"]); clean = [cu[k] for k in range(len(cu)) if abs(Zk[k]) < 2] or [cu[int(np.argmin(np.abs(s["a"])))]]
        if v in CLV:
            sel = np.isin(CLV[v], clean)
            q = summ(cellobj(f, hk, "boost"), sel, 7000 + VIDX[v])["MID"]; A_cl, sST = q["A"], q["s_STAT"]
            ax = q["A_x"]; sn = q["s_n_x"]
        elif v == "radial3":                                         # clean radial bins: tangential and cross over those bins only
            _, _, nt, dd = cl_split(f, hk, "boost", v, "t"); n_ = nt[:, clean].sum(1); d_ = dd[:, clean].sum(1); A_cl = float(n_.sum()/d_.sum())
            I = BIDX[v]; sb = float(np.std(n_[I].sum(1)/d_[I].sum(1), ddof=1))
            reps = [n_[PATCH != p].sum()/d_[PATCH != p].sum() for p in range(30)]; sST = max(sb, float(np.sqrt(29/30*np.sum((np.array(reps) - np.mean(reps))**2))))
            idx = [cu.index(c) for c in clean]; Cr = s["_Cr"][np.ix_(idx, idx)]; Ci = np.linalg.inv(Cr); wv = Ci.sum(1)/Ci.sum()
            ax = float(wv @ np.array(s["a"])[idx]); sn = float(np.sqrt(1/Ci.sum()))
        else:
            zz = zstat_class(f, hk, v, clean); A_cl, sST = zz["A"], zz["s_STAT"]
            idx = [cu.index(c) for c in clean]; Cr = s["_Cr"][np.ix_(idx, idx)]; Ci = np.linalg.inv(Cr); wv = Ci.sum(1)/Ci.sum()
            ax = float(wv @ np.array(s["a"])[idx]); sn = float(np.sqrt(1/Ci.sum()))
        so = ALLS[f"{f}|{hk}"]; sx = math.sqrt(max(0.0, ax**2 - sn**2))
        sCAL = math.sqrt(sST**2 + sx**2 + so["s_leak"]**2 + so["s_RR_exc"]**2); ZM[f"{f}|{hk}"] = dict(variable=v, clean=clean, A=A_cl, s_STAT=sST, Z_STAT=(A_cl - 1)/sST,
                                                                                               a_x_clean=ax, s_x_clean=sx, A_CAL=A_cl - so["leak_t"], s_CAL=sCAL, Z_CAL=(A_cl - so["leak_t"] - 1)/sCAL,
                                                                                               counterpart=so["A"] - A_cl)
    ZCLS = v1([q["Z_CAL"] for q in ZM.values()]); GRADEDZ = {k: q["Z_CAL"] for k, q in ZM.items()}
elif VERD == "CONSISTENT WITH A FLUCTUATION":
    GRADEDZ = {k: q["Z_STAT"] for k, q in ALLS.items()}; ZCLS = v1(list(GRADEDZ.values()))
else:
    GRADEDZ = {k: {"Z_STAT": q["Z_STAT"], "Z_CAL": q["Z_CAL"]} for k, q in ALLS.items()}; ZCLS = f"STAT {v1([q['Z_STAT'] for q in ALLS.values()])} / CAL {v1([q['Z_CAL'] for q in ALLS.values()])} (X7's MARGINAL unchanged)"
say(f"VERDICT: {VERD} ({why})")
say(f"Z_MID: {GRADEDZ} -> {ZCLS}; cross-offset p_x (rotations) {[round(ALLS[k]['p_x'], 3) for k in ALLS]}; A_x {[round(ALLS[k]['A_x'], 4) for k in ALLS]}")
if ZM: say(f"re-derived on the clean subset: {ZM}")
RES.update(verdict=VERD, verdict_reason=why, Z_MID=GRADEDZ, Z_MID_class=ZCLS, Z_MID_clean=ZM, candidates_any_cell=ANY, candidates_all4=CAND4, robust_all4=ROB4,
           look_elsewhere=LE, all_MID={k: {q: ALLS[k][q] for q in ("A", "A_x", "s_n_x", "p_x", "s_STAT", "Z_STAT", "A_CAL", "s_CAL", "Z_CAL", "s_x_exc", "leak_x", "rand_x")} for k in ALLS},
           splits={f"{f}|{hk}|{v}": {k: val for k, val in SPL[(f, hk, v)].items() if not k.startswith("_")} for f, hk in CELLS for v in VARLIST})
pk = rss(); check("K4", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
npass = sum(ok for _, ok in CHECKS); RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk, N=N, R=R)
say(f"X11_ANALYSIS COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x11_analysis_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else (bool(o) if isinstance(o, np.bool_) else str(o))))
sys.exit(0 if npass == len(CHECKS) else 1)
