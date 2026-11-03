"""LAM4 grade (criteria 1023fbaae9, amendment A1): K1, models B0/B4/S4/SF, G1-G3, E1-E2, M1, rows.
Run: python3 -I lam4_grade.py [MUTATE|DRYRUN]. DRYRUN permutes labels (code test; outputs not kept). Single thread."""
import os, sys, json, math, warnings
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.stats import spearmanr
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning); np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); L2 = os.path.join(os.path.dirname(HERE), "LAM2_gas_poor_lambda_estimator")
MODE = sys.argv[1] if len(sys.argv) > 1 else "REAL"; SEED = 20261103; OUT = []; RES = {"lane": "LAM4", "mode": MODE}
def P(s=""): print(s, flush=True); OUT.append(s)
sys.argv = ["lam2_grade.py"]; src = open(os.path.join(L2, "lam2_grade.py")).read().split("# ---- K1")[0]
G = {"__file__": os.path.join(L2, "lam2_grade.py"), "__name__": "lam2"}; exec(compile(src, "lam2_grade.py", "exec"), G)
S = [l.strip().split(",") for l in open(os.path.join(HERE, "lam4_sample.csv")).readlines()[1:]]
F = {}
for l in open(os.path.join(HERE, "lam4_fit.jsonl")): r = json.loads(l); F[r["plateifu"]] = r
idx = np.array([int(s[1]) for s in S]); pifu = [s[3] for s in S]
ok = np.array([p in F and F[p]["status"] == "ok" for p in pifu])
P(f"LAM4 grade, mode {MODE}. Sample {len(S)}; integrated fits ok {int(ok.sum())}, errors {sum(1 for p in pifu if p in F and F[p]['status'] != 'ok')}, missing {sum(1 for p in pifu if p not in F)}")
idx, pifu = idx[ok], [p for p, o in zip(pifu, ok) if o]
fv = lambda k: np.array([F[p][k] for p in pifu], float)
X = {k: G["X"][k][idx] for k in G["X"]}
lam, eps, slow = G["lam"][idx], G["eps"][idx], G["slow"][idx]
sigRe = G["dp"]["Sigma_Re"][G["row"][idx]].astype(float)
if MODE == "DRYRUN":
    pm = np.random.default_rng(1).permutation(len(lam)); lam, eps, slow = lam[pm], eps[pm], slow[pm]
X.update(logsi=np.log10(fv("sigma")), h4i=fv("h4"), h6i=fv("h6"))
B0 = ["logm", "ur", "n", "eps", "logre"]; B4 = B0 + ["logsi"]; S4 = B4 + ["h4i", "h6i"]; SF = G["B"] + G["SH"]
fin = np.ones(len(lam), bool)
for k in set(S4 + SF): fin &= np.isfinite(X[k])
P(f"graded N {int(fin.sum())} (dropped non-finite {int((~fin).sum())}), slow {int(slow[fin].sum())}")
lr = np.log10(fv("sigma") / sigRe)[fin]; med, rms = float(np.median(lr)), float(np.sqrt(np.mean(lr**2))); k1 = abs(med) <= 0.03 and rms <= 0.06
P(f"K1: median log(sigma_int/Sigma_Re) {med:+.4f} (|.| <= 0.03), rms about zero {rms:.4f} (<= 0.06): {'PASS' if k1 else 'FAIL -> NO VERDICT'}")
k2p = os.path.join(HERE, "lam4_k2.json"); K2 = json.load(open(k2p)) if os.path.exists(k2p) else None
P(f"K2: {'NOT RUN' if K2 is None else ('PASS' if K2['pass_'] else 'FAIL')}" + ("" if K2 is None else f" (rms {K2['rms']:.4f})"))
RES.update(K1=dict(median=med, rms=rms, pass_=bool(k1)), N=int(fin.sum()), n_slow=int(slow[fin].sum()))
y = slow[fin]; e = eps[fin]; L = lam[fin]
def oof(names, Xs=None):
    Z = np.c_[[(Xs or X)[k][fin] for k in names]].T; pred = np.full(len(y), np.nan)
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=SEED).split(Z, y):
        sc = StandardScaler().fit(Z[tr])
        m = MLPRegressor((128, 128), activation="logistic", solver="adam", early_stopping=True, validation_fraction=0.1,
                         max_iter=2000, random_state=SEED).fit(sc.transform(Z[tr]), L[tr])
        pred[te] = m.predict(sc.transform(Z[te]))
    return pred
score = lambda pr: 0.31 * np.sqrt(np.clip(e, 0, None)) - pr
def boot(s1, s0, n=1000):
    rng = np.random.default_rng(SEED); g = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].all() or not y[i].any(): continue
        g.append(roc_auc_score(y[i], s1[i]) - roc_auc_score(y[i], s0[i]))
    return float(np.percentile(g, 2.5)), float(np.percentile(g, 97.5))
if MODE == "MUTATE":
    j = np.flatnonzero(fin); rng = np.random.default_rng(SEED)
    cell = sum(np.digitize(X[k][j], np.percentile(X[k][j], [100 / 3, 200 / 3])) * w for k, w in (("logm", 9), ("logsi", 3), ("eps", 1)))
    Xm = {k: v.copy() for k, v in X.items()}
    for c in np.unique(cell):
        jj = j[cell == c]; pm = rng.permutation(len(jj))
        for k in ("h4i", "h6i"): Xm[k][jj] = X[k][jj][pm]
    g = roc_auc_score(y, score(oof(S4, Xm))) - roc_auc_score(y, score(oof(B4))); m1 = abs(g) <= 0.02
    P(f"M1 MUTATE: AUC(S4_mut) - AUC(B4) {g:+.4f}, need within +-0.02: {'PASS' if m1 else 'FAIL -> NO VERDICT'}"); RES["M1"] = dict(gain=float(g), pass_=bool(m1))
else:
    Sc, R = {}, {}; fs = y.mean(); ws, wf = 0.168 / fs, (1 - 0.168) / (1 - fs)
    for k, names in (("B0", B0), ("B4", B4), ("S4", S4), ("SF", SF)):
        pr = oof(names); s = score(pr); Sc[k] = s; ps = s > 0; tp, fp = (ps & y).sum(), (ps & ~y).sum()
        pur = float(tp * ws / (tp * ws + fp * wf)) if ps.any() else float("nan")
        R[k] = dict(auc=float(roc_auc_score(y, s)), rms=float(np.sqrt(np.mean((pr - L)**2))), purity_reweighted=pur, n_pred_slow=int(ps.sum()))
        P(f"  {k:2s} AUC {R[k]['auc']:.4f}  rms {R[k]['rms']:.4f}  purity (reweighted to 0.168) {pur:.3f}  pred slow {int(ps.sum())}")
    gates = {}
    for gname, a, b, bar in (("G1", "S4", "B0", 0.05), ("G2", "S4", "B4", 0.03), ("G3", "S4", "SF", 0.03)):
        d = R[a]["auc"] - R[b]["auc"]; lo, hi = boot(Sc[a], Sc[b]); ps = d >= bar and lo > 0; gates[gname] = dict(gain=d, lo=lo, hi=hi, pass_=bool(ps))
        P(f"{gname} AUC({a}) - AUC({b}) {d:+.4f} [95 % {lo:+.4f}, {hi:+.4f}], need >= {bar}, lo > 0: {'PASS' if ps else 'FAIL'}")
    for gname, a, b in (("row width", "B4", "B0"), ("row fibre vs photometry", "SF", "B0")):
        d = R[a]["auc"] - R[b]["auc"]; lo, hi = boot(Sc[a], Sc[b]); P(f"{gname}: AUC({a}) - AUC({b}) {d:+.4f} [{lo:+.4f}, {hi:+.4f}]")
    e1, e2 = R["S4"]["rms"] <= 0.10, R["S4"]["purity_reweighted"] >= 0.70
    P(f"E1 rms(S4) {R['S4']['rms']:.4f} <= 0.10: {'PASS' if e1 else 'FAIL'}; E2 purity {R['S4']['purity_reweighted']:.3f} >= 0.70: {'PASS' if e2 else 'FAIL'}")
    P("rows:")
    v = X["logm"][fin]; t = np.percentile(v, [100 / 3, 200 / 3])
    for i, m in enumerate((v < t[0], (v >= t[0]) & (v < t[1]), v >= t[1])):
        if y[m].any() and not y[m].all():
            P(f"  log M* tercile {i} [{v[m].min():.2f}, {v[m].max():.2f}] N {int(m.sum())} slow {int(y[m].sum())}: S4-B0 {roc_auc_score(y[m], Sc['S4'][m]) - roc_auc_score(y[m], Sc['B0'][m]):+.4f}, "
              f"S4-B4 {roc_auc_score(y[m], Sc['S4'][m]) - roc_auc_score(y[m], Sc['B4'][m]):+.4f}, S4-SF {roc_auc_score(y[m], Sc['S4'][m]) - roc_auc_score(y[m], Sc['SF'][m]):+.4f}")
    h4 = X["h4i"][fin]
    for c, m in (("slow", y), ("fast", ~y)): P(f"  h4_int {c}: median {np.median(h4[m]):+.4f} +- {1.2533 * np.std(h4[m]) / math.sqrt(m.sum()):.4f}, n {int(m.sum())}")
    rho = spearmanr(h4, L); P(f"  Spearman(h4_int, lambda_Re) {rho.statistic:+.3f} (p {rho.pvalue:.2g}); Spearman(h4_fibre, lambda_Re) {spearmanr(X['h4'][fin], L).statistic:+.3f} on the same galaxies")
    st = fv("start")[fin]; P(f"  fit window start: median {np.median(st):.0f} A, > 3950 A for {int((st > 3950).sum())}")
    m1p = os.path.join(HERE, "lam4_grade_MUTATE.json"); M1 = json.load(open(m1p))["M1"] if os.path.exists(m1p) else None
    if not k1 or (M1 is not None and not M1["pass_"]): lab = "NO VERDICT"
    elif K2 is not None and not K2["pass_"]: lab = "h4 NOT MEASURABLE"
    elif not gates["G1"]["pass_"]: lab = "NO GAIN FROM THE WHOLE GALAXY"
    else:
        q = [n for n, c in (("SHAPE BEYOND WIDTH", gates["G2"]["pass_"]), ("BEATS THE FIBRE", gates["G3"]["pass_"]), ("PRECISE", e1 and e2)) if c]
        lab = "WHOLE-GALAXY SPECTRUM READS SPIN" + (" (" + ", ".join(q) + ")" if q else "")
    if K2 is None or M1 is None: lab += " (PROVISIONAL: " + ", ".join(x for x, v in (("K2", K2), ("M1", M1)) if v is None) + " not run)"
    P(f"\nLABEL: {lab}"); RES.update(models=R, gates=gates, E1=bool(e1), E2=bool(e2), label=lab)
sfx = "" if MODE == "REAL" else f"_{MODE}"
open(os.path.join(HERE, f"lam4_grade{sfx}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"lam4_grade{sfx}.json"), "w"), indent=1, default=float)
