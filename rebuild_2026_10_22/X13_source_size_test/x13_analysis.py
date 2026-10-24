"""X13_source_size_test analysis (criteria c4e5a5a064): is X11's source-size dependence of the cluster-core tangential excess
source-side or cluster-specific? Tests (a)-(f), the frozen decision, and the frozen correction with Z_MID on both footings.
Inputs: the step-0 X7 products (scratch x7_measure_percluster.npz, x7_measure_extras.npz; this lane's
x13_s0_x7_psf_regression_results.json) for X7's statistic machinery (X7's analysis source exec'd read-only, sha-checked, as X11
does); this lane's x13_measure_classes.npz and x13_galaxy_sums.npz (work dir); the cache (edges, catalogue means); the SOM n(z)
(extracted to scratch from ../_external_data/kids_lensing_zsplit/KiDS1000_SOM_N_of_Z.tar.gz); X11's committed JSON (K1).
Usage: x13_analysis.py <step-0 scratch> <work dir> <cache> <SOM n(z) dir> [--mutate]
--mutate: the cross shear replaces the tangential in every class amplitude (K1 must FAIL).
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, math, time, hashlib, resource, glob
sys.dont_write_bytecode = True
import numpy as np
from scipy.stats import chi2 as CHI2
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
SOUT, WORK, CACHE, SOMD = ARGS[0], ARGS[1], ARGS[2], ARGS[3]
OUTF = open(os.path.join(HERE, f"x13_analysis{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
def _gls(y, X, Ci):
    F = X.T @ Ci @ X; th = np.linalg.solve(F, X.T @ Ci @ y); r = y - X @ th; return th, float(r @ Ci @ r)
# K2/K3 run first (they use no data), so their arrays are freed before the data are loaded (RSS); numbers unchanged
# ============================================================== K2, K3: injection checks
rngk = np.random.default_rng(20261027); NSY = 4_000_000; g = 0.02; CHK = 500_000
M = np.linalg.inv(np.array([[1 - g, 0.0], [0.0, 1 + g]]))                                              # image = A^-1 source (tangential g along axis 1)
la = np.empty(NSY, np.float64); eps = np.empty(NSY); e1s = np.empty(NSY); rab_s = np.empty(NSY)
for c0 in range(0, NSY, CHK):                                                                          # chunked (RSS); one generator stream
    n_ = min(CHK, NSY - c0)
    lr = rngk.normal(0.6, 0.45, n_); em0 = np.clip(np.abs(rngk.normal(0, 0.3, n_)), 0, 0.9); ang0 = rngk.uniform(0, np.pi, n_)
    rc0 = np.exp(lr); qax = (1 - em0)/(1 + em0); a_ = rc0/np.sqrt(qax); b_ = rc0*np.sqrt(qax); ca, sa = np.cos(ang0), np.sin(ang0)
    Q11 = a_**2*ca**2 + b_**2*sa**2; Q22 = a_**2*sa**2 + b_**2*ca**2; Q12 = (a_**2 - b_**2)*ca*sa                  # source second moments
    I11 = M[0, 0]**2*Q11; I22 = M[1, 1]**2*Q22; I12 = M[0, 0]*M[1, 1]*Q12
    tr = I11 + I22; dd = np.sqrt((I11 - I22)**2 + 4*I12**2); l1 = np.sqrt((tr + dd)/2); l2 = np.sqrt((tr - dd)/2)
    ep = (l1 - l2)/(l1 + l2); ph = 0.5*np.arctan2(2*I12, I11 - I22)                                     # epsilon = (a-b)/(a+b)
    la[c0:c0 + n_] = l1; eps[c0:c0 + n_] = ep; e1s[c0:c0 + n_] = ep*np.cos(2*ph); rab_s[c0:c0 + n_] = l1*np.sqrt((1 - ep)/(1 + ep))
del lr, em0, ang0, rc0, qax, a_, b_, ca, sa, Q11, Q22, Q12, I11, I22, I12, tr, dd, l1, l2, ep, ph
med = np.median(la); Sm = la < med; Lm = ~Sm; band_ = np.abs(np.log(la) - np.log(med)) < 0.05
Dsy = np.sum(eps[band_])/0.1; Rp_L = 0.5*Dsy/Lm.sum(); Rp_S = -0.5*Dsy/Sm.sum()
Rm_L = e1s[Lm].mean()/g - 1; Rm_S = e1s[Sm].mean()/g - 1; smc = 0.3/np.sqrt(NSY/2)/g
medc = np.median(rab_s); Rm_cL = e1s[rab_s >= medc].mean()/g - 1; Rm_cS = e1s[rab_s < medc].mean()/g - 1
k2 = abs(Rm_L - Rp_L) < 3*smc and abs(Rm_S - Rp_S) < 3*smc and abs(Rm_cL) < 3*smc and abs(Rm_cS) < 3*smc
check("K2", k2, f"exact-transform injection (g {g}, {NSY:,} sources): measured response L {Rm_L:+.4f} S {Rm_S:+.4f} vs formula {Rp_L:+.4f} {Rp_S:+.4f}; circularised split L {Rm_cL:+.4f} S {Rm_cS:+.4f}"
      f" (MC sigma {smc:.4f}; all-sample mean e/g - 1 {e1s.mean()/g - 1:+.4f})", "|meas - formula| < 3 sigma; circularised |R| < 3 sigma")
RES["K2_injection"] = dict(R_meas=[Rm_S, Rm_L], R_formula=[Rp_S, Rp_L], R_circ=[Rm_cS, Rm_cL], mc_sigma=smc)
del la, eps, e1s, rab_s, Sm, Lm, band_
xs_ = np.array([0.1, 0.1, 0.4, 0.4, 0.7, 0.7, 1.0, 1.0]); ps_ = np.array([0.3, 0.5, 0.32, 0.48, 0.31, 0.52, 0.29, 0.5]); Cs = np.diag(np.linspace(0.01, 0.03, 8))
k3 = 0.0
for bs, bp in ((0.8, -0.8), (0.8, 0.0), (0.5, -0.2)):
    ys = 1.0 + bs*xs_ + bp*ps_; th_, c2_ = _gls(ys, np.stack([np.ones(8), xs_, ps_], 1), np.linalg.inv(Cs)); k3 = max(k3, float(np.max(np.abs(th_ - [1.0, bs, bp]))), c2_)
check("K3", k3 <= 1e-9, f"GLS injection: exact class amplitudes recover (a, beta_s, beta_v) and chi2 0 to {k3:.1e}", "<= 1e-9")
import gc; gc.collect()
# ============================================================== X7's setup + statistic machinery, exec'd read-only (sha-checked; as X11)
X7DIR = os.path.join(REB, "X7_cluster_core_significance"); X7SRC = os.path.join(X7DIR, "x7_analysis.py"); X7RAW = open(X7SRC, "rb").read()
assert hashlib.sha256(X7RAW).hexdigest() == "0acb1574c1cd6f44762598635490d218c410caaddb90ea4b5f4088b28d03a7f9", "X7 analysis source changed"
TX7 = X7RAW.decode()
def cut7(a, b): i = TX7.index(a); j = TX7.index(b, i); return TX7[i:j]
SEG1 = cut7("# ============================================================== X2's own functions", "# ============================================================== K0: X2 reproduction")
SEG2 = cut7("# ============================================================== my data (this lane's replay)", "# ============================================================== implementation checks K2")
for old, new, n in (('os.path.join(HERE, "x7_measure_percluster.npz")', 'os.path.join(SOUT, "x7_measure_percluster.npz")', 2),
                    ('os.path.join(HERE, "x7_psf_regression_results.json")', 'os.path.join(HERE, "x13_s0_x7_psf_regression_results.json")', 1)):
    assert SEG2.count(old) == n, old; SEG2 = SEG2.replace(old, new)
def check_x7(name, ok, val, thr): check("X7-" + name, ok, val, thr)
NS7 = {"np": np, "os": os, "sys": sys, "math": math, "json": json, "time": time, "hashlib": hashlib, "REB": REB, "REPO": REPO, "HERE": HERE, "SOUT": SOUT,
       "MUT": False, "RES": {}, "say": say, "check": check_x7, "sha": sha, "rss": rss, "T0": T0, "CHI2": CHI2}
exec(compile(SEG1, X7SRC, "exec"), NS7); exec(compile(SEG2, X7SRC, "exec"), NS7)
FEET, HK, CELLS = NS7["FEET"], NS7["HK"], NS7["CELLS"]; MY = NS7["MY"]; DAT = NS7["DAT"]; PM = NS7["PM"]; N = NS7["N"]; PATCH = NS7["PATCH"]
ALL = NS7["ALL"]; Cell = NS7["Cell"]; summ = NS7["summ"]
HXI = {"h0672": 0, "h0686": 1}; BJ = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}; MIDJ = BJ["MID"]
KG_PC2 = 1.989e30/(3.0857e16)**2
# ============================================================== this lane's products
_XM = np.load(os.path.join(WORK, "x13_measure_classes.npz")); XM = {k: _XM[k] for k in _XM.files if k not in ("rot",)}; del _XM
RES["classes_npz_sha256"] = sha(os.path.join(WORK, "x13_measure_classes.npz"))
assert [str(s) for s in XM["name"]] == [str(s) for s in MY["name"]], "cluster order"
VN = [str(v) for v in XM["varnames"]]; VK = {v: int(k) for v, k in zip(VN, XM["varsizes"])}; OFF = {}; _o = 0
for v in VN: OFF[v] = _o; _o += VK[v]
def C_(var, c=0): return OFF[var] + c
X11C = os.popen(f"cd '{REPO}' && git show c1cd5455a5:rebuild_2026_10_22/X11_cross_shear_diagnosis/x11_analysis_results.json").read()
X11J = json.loads(X11C); RES["x11_json_source"] = "git blob c1cd5455a5 (committed X11 result; the working tree may be under a rerun)"
E11 = json.load(open(os.path.join(CACHE, "x11_edges.json")))["edges"]; E13 = json.load(open(os.path.join(CACHE, "x13_edges.json")))["edges"]
NB = 2000
def BI(key): return np.random.default_rng([20261024, key]).integers(0, N, size=(NB, N))
def hart(n, K): return (n - K - 2)/(n - 1)
# ============================================================== per-class amplitude machinery (X11's src_split, any band, any class list)
def classamp(f, hk, cls, band="MID", conv="boost", field="D"):
    """per class (combined index list cls): per-cluster numerators num (N, K) and denominators den (N, K), plus the WBP weights
    (N, K, J) for class means. X11's src_split: W = 1/E_k^2, B = class boost (all clusters), P = X2's C* model."""
    hi = HXI[hk]; J = BJ[band]; cls = list(cls)
    if MUT and field == "D": field = "Dx"                                                   # MUTATE: cross shear as tangential data
    D = XM[field][:, hi][:, cls][:, :, J]; Et = XM["E"][:, hi][:, cls][:, :, J]; W = np.where(Et < 1e8, 1/Et**2, 0)
    if conv == "boost":
        with np.errstate(invalid="ignore", divide="ignore"): B = np.nan_to_num(XM["den"][:, hi][:, cls].sum(0)/XM["den_r"][:, hi][:, cls].sum(0))[:, J]
    else: B = np.ones((len(cls), len(J)))
    P = PM[("C*", f, hk)][:, J]; WB = W*B[None]
    num = (WB*D).sum(-1); den = (W*P[:, None, :]).sum(-1)
    return num, den, WB*P[:, None, :]
def ratio_draws(num, den, I): return num[I].sum(1)/den[I].sum(1)                            # (NB, K)
def jk30(num, den):
    reps = np.array([num[PATCH != p].sum(0)/den[PATCH != p].sum(0) for p in range(30)]); return np.sqrt(29/30*np.sum((reps - reps.mean(0))**2, 0))
def cmean(wbp, val, den_k):
    """per-cluster numerator / denominator of a class mean: v_ijk = val/den_k (per cluster, bin), weights WBP."""
    with np.errstate(invalid="ignore", divide="ignore"): v = np.nan_to_num(val/den_k)
    return (wbp*v).sum(-1), wbp.sum(-1)
def sizecls(): return [C_("size2", 0), C_("size2", 1)]
def XSf(hk, q, cls, J):
    """extra sums XS[q] (0 w, 1 w*zb, 2 w*s_B, 3 ww ln size, 4 ww ln r_psf, 5 ww ln snr, 6 ww|e|) for classes cls, bins J: (N, K, J)."""
    return XM["XS"][:, HXI[hk], q][:, list(cls)][:, :, J]
def DENf(hk, cls, J): return XM["den"][:, HXI[hk]][:, list(cls)][:, :, J]
def ALLA(f, hk): return summ(Cell("C*", f, hk, "boost"), ALL, 0)["MID"]
AALL = {f"{f}|{hk}": ALLA(f, hk) for f, hk in CELLS}
# ============================================================== K1: reproduction of X11's size numbers
k1 = []
for f, hk in CELLS:
    c = f"{f}|{hk}"
    for v, k in (("size2", 2), ("size4", 4)):
        num, den, _ = classamp(f, hk, [C_(v, j) for j in range(k)]); a = num.sum(0)/den.sum(0)
        k1 += list(np.abs(a - np.array(X11J["E3"][f"{c}|{v}"]["a"])))
    num, den, _ = classamp(f, hk, sizecls()); I11 = np.random.default_rng([20261024, 903]).integers(0, N, size=(2000, N))
    for j in range(2):
        q = X11J["tangential_Z_per_class"][f"{c}|size2|{j}"]; A = num[:, j].sum()/den[:, j].sum(); sb = float(np.std(num[I11, j].sum(1)/den[I11, j].sum(1), ddof=1))
        reps = [num[PATCH != p, j].sum()/den[PATCH != p, j].sum() for p in range(30)]; sj = float(np.sqrt(29/30*np.sum((np.array(reps) - np.mean(reps))**2)))
        k1 += [abs(A - q["A"]), abs(sb - q["s_boot"]), abs(sj - q["s_jk"]), abs((A - 1)/max(sb, sj) - q["Z_STAT"])]
check("K1", max(k1) <= 1e-9, f"size2/size4 tangential A (E3) and size2 A, s_boot (X11's draws), s_jk, Z_STAT vs X11's committed JSON: max|diff| {max(k1):.1e} ({len(k1)} numbers)", "<= 1e-9")
# ============================================================== reference: the size2 effect in MID
say("\n=== reference: size2 halves, MID, C*, boost (paired bootstrap 2000, key 1300) ===")
REF = {}; I0 = BI(1300)
for f, hk in CELLS:
    c = f"{f}|{hk}"; num, den, _ = classamp(f, hk, sizecls()); a = num.sum(0)/den.sum(0); ad = ratio_draws(num, den, I0); sj = jk30(num, den)
    rho_d = ad[:, 1]/ad[:, 0]; dl_d = ad[:, 1] - ad[:, 0]
    REF[c] = dict(A_S=float(a[0]), A_L=float(a[1]), s_S=float(max(ad[:, 0].std(ddof=1), sj[0])), s_L=float(max(ad[:, 1].std(ddof=1), sj[1])),
                  rho=float(a[1]/a[0]), s_rho=float(rho_d.std(ddof=1)), delta=float(a[1] - a[0]), s_delta=float(dl_d.std(ddof=1)), A_ALL=AALL[c]["A"], Z_ALL_STAT=AALL[c]["Z_STAT"])
    q = REF[c]; say(f"  {c}: A_S {q['A_S']:.3f}+-{q['s_S']:.3f}  A_L {q['A_L']:.3f}+-{q['s_L']:.3f}  rho {q['rho']:.3f}+-{q['s_rho']:.3f}  Delta {q['delta']:+.3f}+-{q['s_delta']:.3f}"
                    f"  | all-source A_MID {q['A_ALL']:.3f} (Z_STAT {q['Z_ALL_STAT']:+.2f})")
RES["reference"] = REF
def frac_stats(fc, fd):
    lo, hi = np.percentile(fd, [16, 84]); hw = float((hi - lo)/2); return dict(f=float(fc), s_f=hw, f16=float(lo), f84=float(hi), determined=bool(hw <= 0.40))
# ============================================================== (a) bands
say("\n=== (a) the size2 split in INNER (0.15-0.46 Mpc) and OUTER (1.42-3.0 Mpc) vs MID (bootstrap key 1301) ===")
TA = {}; Ia = BI(1301)
for f, hk in CELLS:
    c = f"{f}|{hk}"; out = {}; rd = {}
    for band in ("INNER", "MID", "OUTER"):
        num, den, _ = classamp(f, hk, sizecls(), band=band); a = num.sum(0)/den.sum(0); ad = ratio_draws(num, den, Ia); sj = jk30(num, den)
        rd[band] = ad[:, 1]/ad[:, 0]
        out[band] = dict(A_S=float(a[0]), A_L=float(a[1]), s_S=float(max(ad[:, 0].std(ddof=1), sj[0])), s_L=float(max(ad[:, 1].std(ddof=1), sj[1])),
                         rho=float(a[1]/a[0]), s_rho=float(rd[band].std(ddof=1)), delta=float(a[1] - a[0]), s_delta=float((ad[:, 1] - ad[:, 0]).std(ddof=1)))
    for band in ("INNER", "OUTER"):
        o = out[band]; dd = rd[band] - rd["MID"]; o["rho_minus_MID"] = o["rho"] - out["MID"]["rho"]; o["s_rho_minus_MID"] = float(dd.std(ddof=1))
        same = abs(o["rho_minus_MID"]) < 2*o["s_rho_minus_MID"]; one = abs(o["rho"] - 1) < 2*o["s_rho"]
        o["sub"] = "SAME AS MID" if (same and not one) else ("NONE" if (one and not same) else "NOT DECISIVE")
    TA[c] = out
    say(f"  {c}: " + " | ".join(f"{b} A_S {out[b]['A_S']:.3f}+-{out[b]['s_S']:.3f} A_L {out[b]['A_L']:.3f}+-{out[b]['s_L']:.3f} rho {out[b]['rho']:.2f}+-{out[b]['s_rho']:.2f}"
                                + (f" (vs MID {out[b]['rho_minus_MID']:+.2f}+-{out[b]['s_rho_minus_MID']:.2f}: {out[b]['sub']})" if b != "MID" else "") for b in ("INNER", "MID", "OUTER")))
RES["a_bands"] = TA
# ============================================================== (b) random points
say("\n=== (b) tangential stack of F1's random points per size2 class (A units; rotated random-mean cross noise, MID) ===")
TB_ = {}; Ib = BI(1302); ROTRX = XM["rotRx"]
for f, hk in CELLS:
    c = f"{f}|{hk}"; hi = HXI[hk]; cls = sizecls(); out = {}
    fld = "Rx" if MUT else "Rt"
    for band in ("MID", "INNER", "OUTER"):
        numR, den, _ = classamp(f, hk, cls, band=band, field=fld); a = numR.sum(0)/den.sum(0); ad = ratio_draws(numR, den, Ib)
        o = dict(a_S=float(a[0]), a_L=float(a[1]), boot_S=float(ad[:, 0].std(ddof=1)), boot_L=float(ad[:, 1].std(ddof=1)), d=float(a[1] - a[0]), boot_d=float((ad[:, 1] - ad[:, 0]).std(ddof=1)))
        if band == "MID":
            J = BJ["MID"]; Et = XM["E"][:, hi][:, cls][:, :, J]; W = np.where(Et < 1e8, 1/Et**2, 0)
            with np.errstate(invalid="ignore", divide="ignore"): B = np.nan_to_num(XM["den"][:, hi][:, cls].sum(0)/XM["den_r"][:, hi][:, cls].sum(0))[:, J]
            rv = np.einsum("nkj,nkjr->kr", W*B[None], ROTRX[:, hi][:, cls].astype(np.float64))/den.sum(0)[:, None]
            o.update(rot_S=float(rv[0].std(ddof=1)), rot_L=float(rv[1].std(ddof=1)), rot_d=float((rv[1] - rv[0]).std(ddof=1)))
            o.update(Z_S=o["a_S"]/o["rot_S"], Z_L=o["a_L"]/o["rot_L"], Z_d=o["d"]/o["rot_d"])
        out[band] = o
    TB_[c] = out; m = out["MID"]
    say(f"  {c}: MID S {m['a_S']:+.4f} (Z {m['Z_S']:+.2f}) L {m['a_L']:+.4f} (Z {m['Z_L']:+.2f}) L-S {m['d']:+.4f} (Z {m['Z_d']:+.2f}) | "
        + " | ".join(f"{b} S {out[b]['a_S']:+.3f}+-{out[b]['boot_S']:.3f} L {out[b]['a_L']:+.3f}+-{out[b]['boot_L']:.3f}" for b in ("INNER", "OUTER")))
NULLB = all(abs(TB_[c]["MID"][z]) < 3 for c in TB_ for z in ("Z_S", "Z_L", "Z_d"))
say(f"  (b) null {'PASSES' if NULLB else 'FAILS'} (|Z| < 3 for S, L, L-S in all 4 cells)")
del ROTRX; XM.pop("rotRx"); gc.collect()                                                         # RSS
RES["b_randoms"] = TB_; RES["b_null"] = "PASSES" if NULLB else "FAILS"
# ============================================================== (c) resolution and SNR at fixed size
say("\n=== (c) PSF size and SNR halves inside each size quartile (8 classes each; GLS with bootstrap covariance, key 1303) ===")
def gls(y, X, Ci):
    F = X.T @ Ci @ X; th = np.linalg.solve(F, X.T @ Ci @ y); r = y - X @ th; return th, float(r @ Ci @ r)
TC = {}; Ic = BI(1303)
for f, hk in CELLS:
    c = f"{f}|{hk}"; out = {}
    nS, dS, wS = classamp(f, hk, sizecls()); J = BJ["MID"]
    dlt_d = ratio_draws(nS, dS, Ic); dlt_d = dlt_d[:, 1] - dlt_d[:, 0]; dlt = float(nS[:, 1].sum()/dS[:, 1].sum() - nS[:, 0].sum()/dS[:, 0].sum())
    dsz = DENf(hk, sizecls(), J)
    for var, qv, lab in (("spsf", 4, "res"), ("ssnr", 5, "snr")):
        cls = [C_(var, j) for j in range(8)]; num, den, wbp = classamp(f, hk, cls); a = num.sum(0)/den.sum(0); ad = ratio_draws(num, den, Ic)
        dcl = DENf(hk, cls, J)
        nx, dx = cmean(wbp, XSf(hk, 3, cls, J), dcl); nv, dv = cmean(wbp, XSf(hk, qv, cls, J), dcl)
        xs_n, xs_d = cmean(wS, XSf(hk, 3, sizecls(), J), dsz); vs_n, vs_d = cmean(wS, XSf(hk, qv, sizecls(), J), dsz)
        Cb = np.cov(ad.T, ddof=1); Ci = np.linalg.inv(Cb)*hart(NB, 8)
        def fit_f(a_, x_, v_, xh, vh, dl):
            X = np.stack([np.ones(8), x_, v_], 1); th, c2 = gls(a_, X, Ci)
            if lab == "res": bV = -th[2]; dV = (xh[1] - xh[0]) - (vh[1] - vh[0])
            else: bV = th[2]; dV = vh[1] - vh[0]
            return th, c2, bV, dV, bV*dV/dl
        xm = nx.sum(0)/dx.sum(0); vm = nv.sum(0)/dv.sum(0); xh = xs_n.sum(0)/xs_d.sum(0); vh = vs_n.sum(0)/vs_d.sum(0)
        th, c2, bV, dV, fc = fit_f(a, xm, vm, xh, vh, dlt)
        fd = np.empty(NB)
        for b in range(NB):
            I = Ic[b]; fd[b] = fit_f(ad[b], nx[I].sum(0)/dx[I].sum(0), nv[I].sum(0)/dv[I].sum(0), xs_n[I].sum(0)/xs_d[I].sum(0), vs_n[I].sum(0)/vs_d[I].sum(0), dlt_d[b])[4]
        within = [float(a[2*q + 1] - a[2*q]) for q in range(4)]; s_within = [float((ad[:, 2*q + 1] - ad[:, 2*q]).std(ddof=1)) for q in range(4)]
        out[lab] = dict(A=a.tolist(), sig=np.sqrt(np.diag(Cb)).tolist(), x=xm.tolist(), v=vm.tolist(), beta=th.tolist(), chi2=c2, b_V=float(bV), dV_halves=float(dV),
                        delta_obs=dlt, within_q_diff=within, s_within_q_diff=s_within, **frac_stats(fc, fd))
        o = out[lab]
        say(f"  {c} {lab}: classes A " + " ".join(f"{x_:.2f}" for x_ in a) + f" | beta_s {th[1]:+.3f} beta_{'p' if lab == 'res' else 'n'} {th[2]:+.3f} (chi2 {c2:.1f}/5)"
            f" | b_V {bV:+.3f} x dV {dV:+.3f} / Delta_obs {dlt:+.3f} -> f_{lab} {o['f']:+.2f} (16-84 % {o['f16']:+.2f} .. {o['f84']:+.2f}; {'DETERMINED' if o['determined'] else 'not determined'})"
            f" | within-quartile hi-lo " + " ".join(f"{d_:+.2f}+-{s_:.2f}" for d_, s_ in zip(within, s_within)))
    TC[c] = out
RES["c_res_snr"] = TC
# ============================================================== (d) redshift calibration: SOM n(z) per tomographic bin (H_SOM)
say("\n=== (d) photo-z: per tomographic bin and size half; H_SOM factors (bootstrap key 1304) ===")
NZ = []
for t in range(1, 6):
    fn = glob.glob(os.path.join(SOMD, f"*TOMO{t}_Nz.asc")); assert len(fn) == 1, fn
    a_ = np.loadtxt(fn[0]); NZ.append(a_)
ZG = NZ[0][:, 0] + 0.025; assert all(np.allclose(n_[:, 0] + 0.025, ZG) for n_ in NZ); NZD = np.array([n_[:, 1] for n_ in NZ])            # (5, nz)
RES["som_nz_files_sha256"] = [sha(p) for p in sorted(glob.glob(os.path.join(SOMD, "*_Nz.asc")))]
G = 6.674e-11; Cc = 2.998e8; MPC = 3.0857e22
from scipy.interpolate import PchipInterpolator
_zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; _DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]                       # F1 / X7 / X11 distances (verbatim)
_DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); _DMb = np.sqrt(7.942**3/(0.295*_DHb))
_PCH = PchipInterpolator(np.r_[0, 0.295, _zb], np.r_[0, _DMb, _DMr])
def DM(z, h): return _PCH(np.minimum(np.asarray(z, float), 2.33))*101.54/h
HV = {"h0672": 0.672, "h0686": 0.686}; zl = np.asarray(XM["z"], float)
def sT(hk):
    """s_T,t(z_l, h): SOM n(z)-averaged Sigma_crit^-1 per cluster and tomographic bin (N, 5); s = 0 for z <= z_l."""
    h = HV[hk]; DlM = DM(zl, h); Dl = DlM/(1 + zl); DMs = DM(ZG, h)
    s = np.clip(4*np.pi*G/Cc**2*(Dl[:, None]*MPC)*(1 - DlM[:, None]/DMs[None, :]), 0, None)                         # (N, nz)
    with np.errstate(all="ignore"): out = (s @ NZD.T)/NZD.sum(1)[None, :]                          # Accelerate BLAS emits spurious FP warnings
    assert np.all(np.isfinite(out)); return out
TD = {}; Id = BI(1304); TBE = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.2])
for f, hk in CELLS:
    c = f"{f}|{hk}"; J = BJ["MID"]; st = sT(hk)                                                                       # (N, 5)
    tcls = [C_("tsz", t*2 + s) for t in range(5) for s in range(2)]
    U = XSf(hk, 2, tcls, J).reshape(N, 5, 2, 3); V = DENf(hk, tcls, J).reshape(N, 5, 2, 3); Wt = XSf(hk, 0, tcls, J).reshape(N, 5, 2, 3); Wz = XSf(hk, 1, tcls, J).reshape(N, 5, 2, 3)
    with np.errstate(invalid="ignore", divide="ignore"):
        b_s = np.nan_to_num((st[:, :, None, None]*U).sum(1)/V.sum(1))                                                   # (N, 2 halves, 3 bins)
        b_a = np.nan_to_num((st[:, :, None, None]*U).sum((1, 2))/V.sum((1, 2)))                                          # (N, 3)
    nS, dS, wS = classamp(f, hk, sizecls()); nA, dA, wA = classamp(f, hk, [C_("ALL")])
    nb_s = (wS*b_s).sum(-1); db_s = wS.sum(-1); nb_a = (wA[:, 0]*b_a).sum(-1); db_a = wA[:, 0].sum(-1)
    def fd_(I, nS_, dS_):
        bS = nb_s[I].sum(0)/db_s[I].sum(0); bA = nb_a[I].sum()/db_a[I].sum(); aS = nS_[I].sum(0)/dS_[I].sum(0)
        return bS, bA, AALL[c]["A"]*(bS[1] - bS[0])/bA/(aS[1] - aS[0])
    allI = np.arange(N); bS, bA, fc = fd_(allI, nS, dS)
    fdd = np.array([fd_(Id[b], nS, dS)[2] for b in range(NB)])
    # reported: per tomographic bin and half (MID apertures at this h): w-mean Z_B, w-mean s_B, weight share; cut-bin share
    tab = []
    for t in range(5):
        for s in range(2):
            wsum = Wt[:, t, s].sum(); tab.append(dict(tomo=t + 1, half="S" if s == 0 else "L", wmean_ZB=float(Wz[:, t, s].sum()/wsum) if wsum > 0 else None,
                                                   wmean_sB=float(U[:, t, s].sum()/wsum) if wsum > 0 else None, ww_share=float(V[:, t, s].sum()/V[:, :, s].sum())))
    cut = (TBE[:5][None, :] < zl[:, None] + 0.2)                                                                       # bin lower edge below the Z_B cut
    cutshare = [float((V[:, :, s].sum(-1)*cut).sum()/V[:, :, s].sum()) for s in range(2)]
    naive = float((U[:, :, 1].sum()/Wt[:, :, 1].sum())/(U[:, :, 0].sum()/Wt[:, :, 0].sum()))
    TD[c] = dict(b_S=float(bS[0]), b_L=float(bS[1]), b_ALL=float(bA), rho_d=float(bS[1]/bS[0]), delta_d=float(AALL[c]["A"]*(bS[1] - bS[0])/bA), table=tab,
                 cut_bin_ww_share=cutshare, naive_sB_ratio_L_over_S=naive, **frac_stats(fc, fdd))
    o = TD[c]
    say(f"  {c}: H_SOM b_S {o['b_S']:.4f} b_L {o['b_L']:.4f} b_ALL {o['b_ALL']:.4f} -> ratio {o['rho_d']:.4f}; Delta_d {o['delta_d']:+.4f} / Delta_obs -> f_d {o['f']:+.3f}"
        f" (16-84 % {o['f16']:+.3f} .. {o['f84']:+.3f}; {'DETERMINED' if o['determined'] else 'not determined'}) | naive mean-s_B ratio L/S {naive:.4f} | cut-bin ww share S/L {cutshare[0]:.3f}/{cutshare[1]:.3f}")
    if hk == "h0672" and f == "canonical":
        say("    per tomographic bin (MID, h 0.672): " + "; ".join(f"t{q['tomo']}{q['half']}: <Z_B> {q['wmean_ZB']:.3f} <s_B> {q['wmean_sB']:.3e} share {q['ww_share']:.3f}" for q in tab if q["wmean_ZB"] is not None))
RES["d_photoz"] = TD
# catalogue-wide w-mean Z_B per tomographic bin and size half (reported)
def npy_chunk(path, a, b):
    """rows a..b of a 1-D .npy file with a plain read (no memory map, no whole-array load: RSS)."""
    with open(path, "rb") as fh:
        ver = np.lib.format.read_magic(fh); shape, fo, dt = np.lib.format._read_array_header(fh, ver); off = fh.tell()
        b = min(b, shape[0]); fh.seek(off + a*dt.itemsize); return np.fromfile(fh, dtype=dt, count=max(0, b - a)), shape[0]
acc_w = np.zeros((5, 2)); acc_z = np.zeros((5, 2)); a0 = 0; NROWS = npy_chunk(os.path.join(CACHE, "zb.npy"), 0, 0)[1]
while a0 < NROWS:
    zz = npy_chunk(os.path.join(CACHE, "zb.npy"), a0, a0 + 2_000_000)[0].astype(np.float64); ss = npy_chunk(os.path.join(CACHE, "size.npy"), a0, a0 + 2_000_000)[0].astype(np.float64)
    ww_ = npy_chunk(os.path.join(CACHE, "w.npy"), a0, a0 + 2_000_000)[0].astype(np.float64)
    vs = np.isfinite(ss) & (ss > 0); tt = np.searchsorted(TBE, zz, side="left") - 1; ok = vs & (tt >= 0) & (tt <= 4)
    hh = (ss >= E11["size2"][0]).astype(int)
    np.add.at(acc_w, (tt[ok], hh[ok]), ww_[ok]); np.add.at(acc_z, (tt[ok], hh[ok]), (ww_*zz)[ok]); a0 += 2_000_000
del zz, ss, ww_
RES["d_catalogue_wmean_ZB"] = (acc_z/acc_w).tolist(); RES["d_catalogue_w_share"] = (acc_w/acc_w.sum(0)).tolist()
say("  catalogue-wide w-mean Z_B per tomographic bin (S / L): " + "; ".join(f"t{t+1} {acc_z[t, 0]/acc_w[t, 0]:.3f}/{acc_z[t, 1]/acc_w[t, 1]:.3f}" for t in range(5))
    + " | w share per bin (S / L): " + "; ".join(f"t{t+1} {acc_w[t, 0]/acc_w[:, 0].sum():.3f}/{acc_w[t, 1]/acc_w[:, 1].sum():.3f}" for t in range(5)))
# ============================================================== (f) shear-induced size selection
say("\n=== (f) shear-induced size selection: catalogue-predicted response vs measured; circularised-size gate (bootstrap key 1305) ===")
TF = {}; If = BI(1305); BW2 = 2*0.05
for f, hk in CELLS:
    c = f"{f}|{hk}"; J = BJ["MID"]
    bandc = [C_("band", j) for j in range(3)]; Dband = XSf(hk, 6, bandc, J)/BW2                                       # (N, 3 edges, 3 bins): D(E) per cluster-bin
    nS, dS, wS = classamp(f, hk, sizecls()); denS = DENf(hk, sizecls(), J)
    with np.errstate(invalid="ignore", divide="ignore"):
        R_S = np.nan_to_num(-0.5*Dband[:, 1]/denS[:, 0]); R_L = np.nan_to_num(0.5*Dband[:, 1]/denS[:, 1])
    nR = np.stack([(wS[:, 0]*R_S).sum(-1), (wS[:, 1]*R_L).sum(-1)], 1); dR = wS.sum(-1)
    def ff(I):
        Rk = nR[I].sum(0)/dR[I].sum(0); aS = nS[I].sum(0)/dS[I].sum(0); return Rk, AALL[c]["A"]*(Rk[1] - Rk[0])/(aS[1] - aS[0])
    Rk, fc = ff(np.arange(N)); fdd = np.array([ff(If[b])[1] for b in range(NB)])
    # size4 predictions (reported)
    n4, d4, w4 = classamp(f, hk, [C_("size4", j) for j in range(4)]); den4 = DENf(hk, [C_("size4", j) for j in range(4)], J); a4 = n4.sum(0)/d4.sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        R4 = [np.nan_to_num(-0.5*Dband[:, 0]/den4[:, 0]), np.nan_to_num(0.5*(Dband[:, 0] - Dband[:, 1])/den4[:, 1]),
              np.nan_to_num(0.5*(Dband[:, 1] - Dband[:, 2])/den4[:, 2]), np.nan_to_num(0.5*Dband[:, 2]/den4[:, 3])]
    R4k = [float((w4[:, q]*R4[q]).sum()/w4[:, q].sum()) for q in range(4)]
    a4d = ratio_draws(n4, d4, If); s4 = [float(max(a4d[:, q].std(ddof=1), jk30(n4, d4)[q])) for q in range(4)]
    # circularised split (gate) and alternative-convention prediction; FLUX_RADIUS split
    nc, dc_, wc_ = classamp(f, hk, [C_("circ2", 0), C_("circ2", 1)]); ac = nc.sum(0)/dc_.sum(0); acd = ratio_draws(nc, dc_, If); rc_d = acd[:, 1]/acd[:, 0]
    rho_c = float(ac[1]/ac[0]); s_rho_c = float(rc_d.std(ddof=1)); gate = abs(rho_c - 1) < 2*s_rho_c
    Dc = XSf(hk, 6, [C_("cband")], J)[:, 0]/BW2; denc = DENf(hk, [C_("circ2", 0), C_("circ2", 1)], J)
    with np.errstate(invalid="ignore", divide="ignore"):
        Rc_alt = [float((wc_[:, 0]*np.nan_to_num(0.5*Dc/denc[:, 0])).sum()/wc_[:, 0].sum()), float((wc_[:, 1]*np.nan_to_num(-0.5*Dc/denc[:, 1])).sum()/wc_[:, 1].sum())]
    nfr, dfr, _ = classamp(f, hk, [C_("frad2", 0), C_("frad2", 1)]); afr = nfr.sum(0)/dfr.sum(0); afd = ratio_draws(nfr, dfr, If)
    TF[c] = dict(R_S=float(Rk[0]), R_L=float(Rk[1]), rho_sel=float((1 + Rk[1])/(1 + Rk[0])), delta_sel=float(AALL[c]["A"]*(Rk[1] - Rk[0])),
                 size4_R=R4k, size4_pred=[AALL[c]["A"]*(1 + r) for r in R4k], size4_meas=a4.tolist(), size4_sig=s4,
                 circ2_A=ac.tolist(), circ2_sig=[float(acd[:, 0].std(ddof=1)), float(acd[:, 1].std(ddof=1))], rho_circ=rho_c, s_rho_circ=s_rho_c, gate=bool(gate),
                 circ2_alt_R=Rc_alt, rho_circ_alt=float((1 + Rc_alt[1])/(1 + Rc_alt[0])),
                 frad2_A=afr.tolist(), rho_frad=float(afr[1]/afr[0]), s_rho_frad=float((afd[:, 1]/afd[:, 0]).std(ddof=1)), **frac_stats(fc, fdd))
    o = TF[c]
    say(f"  {c}: R_S {o['R_S']:+.3f} R_L {o['R_L']:+.3f} -> predicted rho {o['rho_sel']:.3f} (measured {REF[c]['rho']:.3f}+-{REF[c]['s_rho']:.3f}); Delta_sel {o['delta_sel']:+.3f}"
        f" -> f_sel {o['f']:+.2f} (16-84 % {o['f16']:+.2f} .. {o['f84']:+.2f}; {'DETERMINED' if o['determined'] else 'not determined'})")
    say(f"      size4 predicted " + " ".join(f"{p:.2f}" for p in o["size4_pred"]) + " vs measured " + " ".join(f"{m_:.2f}+-{s_:.2f}" for m_, s_ in zip(o["size4_meas"], s4))
        + f" | circ2 A {ac[0]:.3f} / {ac[1]:.3f}, rho {rho_c:.3f}+-{s_rho_c:.3f} -> gate {'PASSED' if gate else 'FAILED'}"
        f" (alt-convention prediction {o['rho_circ_alt']:.3f}) | FLUX_RADIUS rho {o['rho_frad']:.3f}+-{o['s_rho_frad']:.3f}")
RES["f_selection"] = TF
# ============================================================== (e) independent lens sample (galaxies)
say("\n=== (e) F2's galaxy lenses, P2's estimator and bins: size2 split ('in' 0.03-0.35 Mpc; 50-patch jackknife) ===")
GZ = np.load(os.path.join(WORK, "x13_galaxy_sums.npz")); RES["galaxy_npz_sha256"] = sha(os.path.join(WORK, "x13_galaxy_sums.npz"))
GL, GR, NL, NR = GZ["PT_L"], GZ["PT_R"], GZ["NP_L"], GZ["NP_R"]; RC_ = GZ["rcen"][:int(GZ["nbm"])]; T_ = 1/RC_
GJ = {"in": np.arange(0, 8), "O1": np.arange(8, 12), "inO1": np.arange(0, 12)}
iG, iX = (1, 0) if MUT else (0, 1)
def gamp(sel, cls, J, clip=False):
    L = GL[sel].sum(0); Rr = GR[sel].sum(0); nl = NL[sel].sum(); nr = NR[sel].sum()
    out = []
    for k in cls:
        with np.errstate(invalid="ignore", divide="ignore"):
            dS = (L[k, iG]/L[k, 2] - Rr[k, iG]/Rr[k, 2])/KG_PC2; B = np.ones_like(dS) if clip else (L[k, 2]/nl)/(Rr[k, 2]/nr)
        w = L[k, 2][J]*T_[J]; out.append(float(np.nansum(w*B[J]*dS[J])/np.sum(w*T_[J])))
    return np.array(out)
def gjk(fun):
    full = fun(np.ones(50, bool)); reps = np.array([fun(np.arange(50) != p) for p in range(50)])
    return full, np.sqrt(49/50*np.sum((reps - reps.mean(0))**2, 0)), reps
TE = {}
for rng_ in ("in", "O1", "inO1"):
    for clip in (False, True):
        a, s, reps = gjk(lambda m: gamp(m, [0, 1, 2, 3, 4], GJ[rng_], clip))
        rho = a[2]/a[1]; s_rho = float(np.sqrt(49/50*np.sum((reps[:, 2]/reps[:, 1] - np.mean(reps[:, 2]/reps[:, 1]))**2)))
        rhoc = a[4]/a[3]; s_rhoc = float(np.sqrt(49/50*np.sum((reps[:, 4]/reps[:, 3] - np.mean(reps[:, 4]/reps[:, 3]))**2)))
        cS = reps[:, 1]/reps[:, 0]; cL = reps[:, 2]/reps[:, 0]
        TE[f"{rng_}|{'clip' if clip else 'boost'}"] = dict(A=a.tolist(), sig=s.tolist(), rho=float(rho), s_rho=s_rho, rho_circ=float(rhoc), s_rho_circ=s_rhoc,
                                                         c_S=float(a[1]/a[0]), c_L=float(a[2]/a[0]), cov_c=(np.cov(np.stack([cS, cL]), ddof=0)*49).tolist())
L_ = GL.sum(0)
with np.errstate(invalid="ignore", divide="ignore"):
    Dg = L_[5, 5]/BW2; Rg_S = -0.5*Dg/L_[1, 2]; Rg_L = 0.5*Dg/L_[2, 2]
J = GJ["in"]; wS_ = L_[1, 2][J]*T_[J]**2; wL_ = L_[2, 2][J]*T_[J]**2
RgS = float(np.sum(wS_*Rg_S[J])/wS_.sum()); RgL = float(np.sum(wL_*Rg_L[J])/wL_.sum()); TE["pred_sel"] = dict(R_S=RgS, R_L=RgL, rho_sel=(1 + RgL)/(1 + RgS))
G0 = TE["in|boost"]; RES["e_galaxy"] = TE; RES["galaxy_counts"] = dict(N_lens=float(NL.sum()), N_rand=float(NR.sum()))
say(f"  'in': A_ALL {G0['A'][0]:.4f}+-{G0['sig'][0]:.4f} (1/R template units), A_S {G0['A'][1]:.4f}+-{G0['sig'][1]:.4f}, A_L {G0['A'][2]:.4f}+-{G0['sig'][2]:.4f}"
    f" -> rho_gal {G0['rho']:.3f}+-{G0['s_rho']:.3f}; circ2 rho {G0['rho_circ']:.3f}+-{G0['s_rho_circ']:.3f}; predicted selection rho {TE['pred_sel']['rho_sel']:.3f}")
for k_ in ("O1|boost", "inO1|boost", "in|clip"):
    say(f"  {k_}: rho_gal {TE[k_]['rho']:.3f}+-{TE[k_]['s_rho']:.3f}; circ2 rho {TE[k_]['rho_circ']:.3f}+-{TE[k_]['s_rho_circ']:.3f}")
ECL = {}
for f, hk in CELLS:
    c = f"{f}|{hk}"; rc, sc = REF[c]["rho"], REF[c]["s_rho"]; rg, sg = G0["rho"], G0["s_rho"]; sd = math.hypot(sg, sc)
    match = abs(rg - rc) < 2*sd; one = abs(rg - 1) < 2*sg; det = (rg - 1)/sg >= 2
    cls = "E-MATCH" if (match and det) else ("E-NULL" if (one and not match) else ("E-AMBIGUOUS" if (match and one) else "E-OTHER"))
    ECL[c] = dict(rho_cl=rc, s_rho_cl=sc, rho_gal=rg, s_rho_gal=sg, diff_sigma=(rg - rc)/sd, Z_gal_vs_1=(rg - 1)/sg, cls=cls)
    say(f"  {c}: rho_cl {rc:.3f}+-{sc:.3f} vs rho_gal {rg:.3f}+-{sg:.3f}: diff {(rg - rc)/sd:+.2f} sigma, galaxy vs 1 {(rg - 1)/sg:+.2f} sigma -> {cls}")
EC = set(q["cls"] for q in ECL.values()); ECLASS = EC.pop() if len(EC) == 1 else "MIXED"
say(f"  (e) class: {ECLASS}"); RES["e_classes"] = ECL; RES["e_class"] = ECLASS
# ============================================================== decision
say("\n=== decision (frozen §6) ===")
def mech(name, T, gate=True):
    fs = [T[f"{f}|{hk}"]["f"] if (name != "sel" or T[f"{f}|{hk}"]["gate"]) else 0.0 for f, hk in CELLS]
    det = [T[f"{f}|{hk}"]["determined"] for f, hk in CELLS]
    gate_ok = all(T[f"{f}|{hk}"]["gate"] for f, hk in CELLS) if name == "sel" else True
    if name == "sel" and not gate_ok: fs = [0.0]*4; det = [True]*4
    ge70 = all(d and v >= 0.70 for d, v in zip(det, fs)); lt30 = all(d and v < 0.30 for d, v in zip(det, fs))
    return dict(f=fs, determined=det, gate=gate_ok, ge70=ge70, lt30=lt30, fmin=min(fs))
MECH = {"res": mech("res", {c: TC[c]["res"] for c in TC}), "snr": mech("snr", {c: TC[c]["snr"] for c in TC}), "d": mech("d", TD), "sel": mech("sel", TF)}
for k_, m_ in MECH.items():
    say(f"  {k_}: f {[round(v, 3) for v in m_['f']]} determined {m_['determined']}{' gate ' + str(m_['gate']) if k_ == 'sel' else ''} -> >= 70 %: {m_['ge70']}; < 30 %: {m_['lt30']}")
pre = all(ok for _, ok in CHECKS)
S0J = os.path.join(HERE, "x13_s0_check_results.json"); s0ok = os.path.exists(S0J) and all(v["pass_"] for v in json.load(open(S0J))["checks"].values())
q70 = [k_ for k_, m_ in MECH.items() if m_["ge70"]]
if not (pre and s0ok): VERD = "UNDECIDED"; why = f"precondition failed (lane checks {pre}, S0 {s0ok})"
elif ECLASS == "E-MATCH" or q70: VERD = "SOURCE-SIDE SYSTEMATIC"; why = f"(e) {ECLASS}; mechanisms >= 70 %: {q70 or 'none'}"
elif ECLASS == "E-NULL" and all(m_["lt30"] for m_ in MECH.values()): VERD = "CLUSTER-SPECIFIC"; why = "(e) E-NULL and every mechanism < 30 %"
else: VERD = "UNDECIDED"; why = f"(e) {ECLASS}; mechanisms >= 70 %: none; all < 30 %: {all(m_['lt30'] for m_ in MECH.values())}"
say(f"VERDICT: {VERD} ({why})"); RES.update(verdict=VERD, verdict_reason=why, mechanisms=MECH)
# ============================================================== correction (frozen §7): all variants computed, the frozen one graded
say("\n=== correction (frozen §7) and Z_MID on both footings (bootstrap key 1307, X2's 30-patch jackknife) ===")
Ik = BI(1307); CORR = {}
for f, hk in CELLS:
    c = f"{f}|{hk}"; J = BJ["MID"]; nS, dS, wS = classamp(f, hk, sizecls()); denS = DENf(hk, sizecls(), J)
    bandc = C_("band", 1); Dm = XSf(hk, 6, [bandc], J)[:, 0]/BW2
    with np.errstate(invalid="ignore", divide="ignore"):
        RS = np.nan_to_num(-0.5*Dm/denS[:, 0]); RL = np.nan_to_num(0.5*Dm/denS[:, 1])
    nR = np.stack([(wS[:, 0]*RS).sum(-1), (wS[:, 1]*RL).sum(-1)], 1); dR = wS.sum(-1)
    st = sT(hk); tcls = [C_("tsz", t*2 + s) for t in range(5) for s in range(2)]
    U = XSf(hk, 2, tcls, J).reshape(N, 5, 2, 3); V = DENf(hk, tcls, J).reshape(N, 5, 2, 3)
    with np.errstate(invalid="ignore", divide="ignore"): bsij = np.nan_to_num((st[:, :, None, None]*U).sum(1)/V.sum(1))
    nbk = (wS*bsij).sum(-1); dbk = wS.sum(-1)
    var_res = TC[c]["res"]; var_snr = TC[c]["snr"]
    xsn = {lab: cmean(wS, XSf(hk, q, sizecls(), J), denS) for lab, q in (("x", 3), ("p", 4), ("n", 5))}
    def corrA(sel_or_I, kind, I_is_idx=True):
        I = sel_or_I
        num = nS[I]; den = dS[I]
        if kind == "none": return num.sum()/den.sum()
        if kind == "sel": ck = 1 + nR[I].sum(0)/dR[I].sum(0); return (num.sum(0)/ck).sum()/den.sum()
        if kind == "d": ck = nbk[I].sum(0)/dbk[I].sum(0); return (num.sum(0)/ck).sum()/den.sum()
        if kind == "galaxy": ck = np.array([G0["c_S"], G0["c_L"]]); return (num.sum(0)/ck).sum()/den.sum()
        if kind in ("res", "snr"):
            Tv = var_res if kind == "res" else var_snr; bV = Tv["b_V"]
            if kind == "res": Vh = xsn["x"][0][I].sum(0)/xsn["x"][1][I].sum(0) - xsn["p"][0][I].sum(0)/xsn["p"][1][I].sum(0)
            else: Vh = xsn["n"][0][I].sum(0)/xsn["n"][1][I].sum(0)
            dk = den.sum(0); Vp = (Vh*dk).sum()/dk.sum()
            return (num.sum(0) - bV*(Vh - Vp)*dk).sum()/den.sum()
    out = {}
    for kind in ("none", "sel", "d", "res", "snr", "galaxy"):
        A = corrA(np.arange(N), kind); bd = np.array([corrA(Ik[b], kind) for b in range(NB)]); sb = float(bd.std(ddof=1))
        reps = np.array([corrA(np.where(PATCH != p)[0], kind) for p in range(30)]); sj = float(np.sqrt(29/30*np.sum((reps - reps.mean())**2)))
        s = max(sb, sj)
        if kind == "galaxy":
            gS = -nS[:, 0].sum()/G0["c_S"]**2/dS.sum(); gL = -nS[:, 1].sum()/G0["c_L"]**2/dS.sum(); gv = np.array([gS, gL])
            s = float(np.sqrt(s**2 + gv @ np.array(G0["cov_c"]) @ gv))
        out[kind] = dict(A=float(A), s_boot=sb, s_jk=sj, s=float(s), Z=float((A - 1)/s))
    CORR[c] = out
    say(f"  {c}: " + " | ".join(f"{k_} A {v['A']:.3f}+-{v['s']:.3f} Z {v['Z']:+.2f}" for k_, v in out.items()) + f" | X11 all-source Z_STAT {AALL[c]['Z_STAT']:+.2f} (A {AALL[c]['A']:.3f})")
RES["corrections"] = CORR
def v1(zs): return "REAL" if min(zs) >= 3 else ("NOT SIGNIFICANT" if min(zs) < 2 else "MARGINAL")
if VERD == "SOURCE-SIDE SYSTEMATIC":
    if q70: KIND = max(q70, key=lambda k_: MECH[k_]["fmin"])
    else: KIND = "galaxy"
    ZC = {c: CORR[c][KIND] for c in CORR}; ZCLS = v1([q["Z"] for q in ZC.values()])
    say(f"graded correction: {KIND}; Z_MID,corr " + ", ".join(f"{c} {q['A']:.3f}+-{q['s']:.3f} Z {q['Z']:+.2f}" for c, q in ZC.items()) + f" -> {ZCLS}")
    RES.update(correction=KIND, Z_MID_corr=ZC, Z_MID_corr_class=ZCLS)
else:
    say(f"no correction applied ({VERD}); X11's all-source Z_STAT stands with its size caveat: " + ", ".join(f"{c} {AALL[c]['Z_STAT']:+.2f}" for c in AALL))
    RES.update(correction=None, Z_MID_corr=None, Z_MID_corr_class=None)
pk = rss(); check("K4", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
npass = sum(ok for _, ok in CHECKS); RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk, N=N)
say(f"X13_ANALYSIS COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x13_analysis_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else (bool(o) if isinstance(o, np.bool_) else str(o))))
sys.exit(0 if npass == len(CHECKS) else 1)
