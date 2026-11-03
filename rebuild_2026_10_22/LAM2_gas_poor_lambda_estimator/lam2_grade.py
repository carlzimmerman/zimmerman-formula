"""LAM2 stage 1-2 grade (criteria fa14da563a, amendments A1-A3): K1 fit check, models B/P/S/SP, E1-E4, M1 MUTATE, reported rows.
Run: python3 -I lam2_grade.py [MUTATE]   (writes lam2_grade.out/.json, or lam2_grade_MUTATE.* for the M1 control alone)
Single thread. kappa = 1/2 FITTED; not theory closed."""
import os, sys, glob, json, math, warnings
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
from scipy.stats import spearmanr
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning); np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "_external_data")
SEED = 20261103; MODE = sys.argv[1] if len(sys.argv) > 1 else "REAL"; OUT = []; RES = {"lane": "LAM2", "mode": MODE}
def P(s=""): print(s, flush=True); OUT.append(s)

# ---- data ----
a = np.loadtxt(os.path.join(HERE, "lam2_sample.csv"), delimiter=",", skiprows=1, dtype=str)
row = a[:, 0].astype(int); sid = a[:, 1]; poor = a[:, 5] == "1"; slow = a[:, 6] == "1"
dp = fits.open(os.path.join(EXT, "lam1_dynpop_2026_11_03", "SDSSDR17_MaNGA_JAM_v2.fits"))[1].data
L = {}
for fn in sorted(glob.glob(os.path.join(EXT, "lam2_sdss_lines_2026_11_03", "lines_*.csv"))):
    lines = open(fn).read().splitlines(); hdr = lines[1].split(",")
    for l in lines[2:]:
        c = l.split(","); L[c[0]] = {k: float(v) if v not in ("", "null") else np.nan for k, v in zip(hdr[1:], c[1:])}
F = {}
for l in open(os.path.join(HERE, "lam2_fit.jsonl")):
    r = json.loads(l); F[r["specobjid"]] = r
col = lambda k: np.array([L[s][k] for s in sid])
fitok = np.array([s in F and F[s]["status"] == "ok" for s in sid])
fv = lambda k: np.array([F[s][k] if s in F and F[s]["status"] == "ok" else np.nan for s in sid])
lam, eps = dp["Lambda_Re"][row].astype(float), dp["Eps_MGE"][row].astype(float)
if MODE == "DRYRUN":  # code test only: labels shuffled across galaxies so no real answer can be read
    pm = np.random.default_rng(1).permutation(len(lam)); lam, eps, slow = lam[pm], eps[pm], slow[pm]
vd = col("velDisp"); sp = fv("sigma"); h4, h6 = fv("h4"), fv("h6")
mass = dp["nsa_sersic_mass"][row].astype(float); logm = np.where(mass > 100, np.log10(np.clip(mass, 1, None)), mass) + 0.310
am = dp["nsa_sersic_absmag"][row].astype(float); ur = am[:, 2] - am[:, 4]
re_as = dp["Re_arcsec_MGE"][row].astype(float); re_kpc = re_as * dp["DA"][row].astype(float) * 1e3 * math.pi / 648000
X = dict(logm=logm, ur=ur, n=dp["nsa_sersic_n"][row].astype(float), eps=eps, logre=np.log10(re_kpc), fib=1.5 / re_as, logvd=np.log10(vd),
         d4000=col("d4000_n"), mgb=col("lick_mgb"), fe5270=col("lick_fe5270"), hda=col("lick_hd_a"),
         h4=h4, h6=h6, sigrat=np.log10(sp / vd), sbal=col("sigma_balmer"))
B = ["logm", "ur", "n", "eps", "logre", "fib", "logvd"]; POP = ["d4000", "mgb", "fe5270", "hda"]; SH = ["h4", "h6", "sigrat"]
MODELS = {"B": B, "P": B + POP, "S": B + SH, "SP": B + POP + SH}
ew = -col("h_alpha_eqw")
P(f"LAM2 grade, mode {MODE}. Sample rows {len(a)}; pPXF ok {int(fitok.sum())}, error rows {int(sum(1 for s in sid if s in F and F[s]['status'] != 'ok'))}, missing {int(sum(1 for s in sid if s not in F))}")

def finite(names, m):
    ok = m.copy()
    for k in names: ok &= np.isfinite(X[k]) & (X[k] > -999)  # A3: MPA-JHU sentinels (-9999) count as missing
    return ok

# ---- K1: pPXF sigma vs SDSS velDisp, gas-poor ----
k1s = poor & fitok & np.isfinite(sp) & (sp > 0)
lr = np.log10(sp[k1s] / vd[k1s]); med, rms = float(np.median(lr)), float(np.sqrt(np.mean(lr**2)))
k1 = abs(med) <= 0.03 and rms <= 0.06
P(f"K1 (gas-poor, n {int(k1s.sum())}): median log(sigma_pPXF/velDisp) {med:+.4f} (|.| <= 0.03), rms about zero {rms:.4f} (<= 0.06): {'PASS' if k1 else 'FAIL -> NO VERDICT'}")
RES["K1"] = dict(n=int(k1s.sum()), median=med, rms=rms, pass_=bool(k1))
k2p = os.path.join(HERE, "lam2_k2.json"); K2 = json.load(open(k2p)) if os.path.exists(k2p) else None
P(f"K2 (from lam2_k2.json): {'NOT RUN' if K2 is None else ('PASS' if K2['pass_'] else 'FAIL')}" + ("" if K2 is None else f", rms {K2['rms']:.4f}"))

# ---- models ----
def oof(names, sel, Xover=None):
    """Out-of-fold predicted lambda_Re for rows in sel (5-fold stratified by slow, fixed seed)."""
    Z = np.c_[[(Xover or X)[k][sel] for k in names]].T; y = lam[sel]; pred = np.full(sel.sum(), np.nan); fold = np.zeros(sel.sum(), int)
    for f, (tr, te) in enumerate(StratifiedKFold(5, shuffle=True, random_state=SEED).split(Z, slow[sel])):
        sc = StandardScaler().fit(Z[tr])
        m = MLPRegressor((128, 128), activation="logistic", solver="adam", early_stopping=True, validation_fraction=0.1,
                         max_iter=2000, random_state=SEED).fit(sc.transform(Z[tr]), y[tr])
        pred[te] = m.predict(sc.transform(Z[te])); fold[te] = f
    return pred
def score(pred, sel): return 0.31 * np.sqrt(np.clip(eps[sel], 0, None)) - pred
def boot_gain(y, s1, s0, n=1000):
    rng = np.random.default_rng(SEED); g = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].all() or not y[i].any(): continue
        g.append(roc_auc_score(y[i], s1[i]) - roc_auc_score(y[i], s0[i]))
    return float(np.percentile(g, 2.5)), float(np.percentile(g, 97.5))

def run_sample(tag, base, graded, extra=None):
    sel = finite(B + POP + SH + (extra or []), base & fitok); y = slow[sel]
    P(f"\n== {tag}: N {int(sel.sum())} (dropped for missing features {int((base & fitok).sum() - sel.sum())}), slow {int(y.sum())}")
    R = {"n": int(sel.sum()), "n_slow": int(y.sum())}; S = {}
    models = dict(MODELS, **({"Bsb": B + ["sbal"]} if extra else {}))
    for k, names in models.items():
        pr = oof(names, sel); s = score(pr, sel); S[k] = s
        auc = roc_auc_score(y, s); rmsl = float(np.sqrt(np.mean((pr - lam[sel])**2))); ps = s > 0
        pur = float(y[ps].mean()) if ps.any() else float("nan")
        R[k] = dict(auc=float(auc), rms=rmsl, purity=pur, n_pred_slow=int(ps.sum()))
        P(f"  {k:3s} AUC {auc:.4f}  rms {rmsl:.4f}  purity {pur:.3f} (pred slow {int(ps.sum())})")
    g3 = R["S"]["auc"] - R["B"]["auc"]; lo3, hi3 = boot_gain(y, S["S"], S["B"])
    g4 = R["SP"]["auc"] - R["P"]["auc"]; lo4, hi4 = boot_gain(y, S["SP"], S["P"])
    gp = R["P"]["auc"] - R["B"]["auc"]; lop, hip = boot_gain(y, S["P"], S["B"])
    e1, e2 = R["S"]["rms"] <= 0.10, R["S"]["purity"] >= 0.70; e3 = g3 >= 0.05 and lo3 > 0; e4 = g4 >= 0.03 and lo4 > 0
    lab = "" if graded else " (row, not graded)"
    P(f"  E1 rms(S) {R['S']['rms']:.4f} <= 0.10: {'PASS' if e1 else 'FAIL'}{lab}")
    P(f"  E2 purity(S) {R['S']['purity']:.3f} >= 0.70: {'PASS' if e2 else 'FAIL'}{lab}")
    P(f"  E3 AUC(S)-AUC(B) {g3:+.4f} [95 % {lo3:+.4f}, {hi3:+.4f}] need >= 0.05, lo > 0: {'PASS' if e3 else 'FAIL'}{lab}")
    P(f"  E4 AUC(SP)-AUC(P) {g4:+.4f} [95 % {lo4:+.4f}, {hi4:+.4f}] need >= 0.03, lo > 0: {'PASS' if e4 else 'FAIL'}{lab}")
    P(f"  row: populations alone AUC(P)-AUC(B) {gp:+.4f} [{lop:+.4f}, {hip:+.4f}]")
    R.update(E1=bool(e1), E2=bool(e2), E3=dict(gain=g3, lo=lo3, hi=hi3, pass_=bool(e3)), E4=dict(gain=g4, lo=lo4, hi=hi4, pass_=bool(e4)),
             pop_gain=dict(gain=gp, lo=lop, hi=hip))
    if extra:
        gs = R["S"]["auc"] - R["Bsb"]["auc"]; P(f"  row: AUC(S)-AUC(B+sigma_balmer) {gs:+.4f}; AUC(B+sigma_balmer)-AUC(B) {R['Bsb']['auc'] - R['B']['auc']:+.4f}")
    return sel, S, R

if MODE == "MUTATE":
    # M1: shuffle (h4, h6, sigrat) together within M* x velDisp x Eps_MGE tercile cells of the gas-poor graded sample
    sel = finite(B + POP + SH, poor & fitok); idx = np.flatnonzero(sel); rng = np.random.default_rng(SEED)
    cell = sum(np.digitize(X[k][idx], np.percentile(X[k][idx], [100 / 3, 200 / 3])) * w for k, w in (("logm", 9), ("logvd", 3), ("eps", 1)))
    Xm = {k: v.copy() for k, v in X.items()}
    for c in np.unique(cell):
        j = idx[cell == c]; perm = rng.permutation(len(j))
        for k in SH: Xm[k][j] = X[k][j][perm]
    y = slow[sel]; sB = score(oof(B, sel), sel); sM = score(oof(B + SH, sel, Xm), sel)
    g = roc_auc_score(y, sM) - roc_auc_score(y, sB); m1 = abs(g) <= 0.02
    P(f"M1 MUTATE (gas-poor N {int(sel.sum())}): AUC(S_mut)-AUC(B) {g:+.4f}, need within +-0.02: {'PASS' if m1 else 'FAIL -> NO VERDICT'}")
    RES["M1"] = dict(gain=float(g), pass_=bool(m1))
else:
    selp, Sp, Rp = run_sample("GAS-POOR (graded)", poor, True); RES["gas_poor"] = Rp
    selr, Sr, Rr = run_sample("GAS-BEARING (rows)", ~poor, False, extra=["sbal"]); RES["gas_bearing"] = Rr
    # ---- reported rows, gas-poor ----
    y = slow[selp]; P("\n== rows, gas-poor")
    def sub_gain(m, name):
        if m.sum() < 30 or y[m].all() or not y[m].any(): P(f"  {name}: too few"); return None
        g = roc_auc_score(y[m], Sp["S"][m]) - roc_auc_score(y[m], Sp["B"][m]); P(f"  {name}: N {int(m.sum())}, slow {int(y[m].sum())}, AUC gain S-B {g:+.4f}"); return float(g)
    RES["rows"] = {}
    for k in ("logm", "logvd", "eps", "fib"):
        v = X[k][selp]; e = np.percentile(v, [100 / 3, 200 / 3])
        for t, m in enumerate((v < e[0], (v >= e[0]) & (v < e[1]), v >= e[1])):
            RES["rows"][f"{k}_t{t}"] = sub_gain(m, f"{k} tercile {t} [{v[m].min():.3f}, {v[m].max():.3f}]")
    for lo, hi in ((-99, 1), (1, 2), (2, 3)):
        RES["rows"][f"ew_{lo}_{hi}"] = sub_gain((ew[selp] >= lo) & (ew[selp] < hi), f"EW(Ha) [{max(lo, -99)}, {hi}) A")
    for cls, m in (("slow", y), ("fast", ~y)):
        hv = h4[selp][m]; se = 1.2533 * np.std(hv) / math.sqrt(len(hv)); rho = spearmanr(hv, lam[selp][m])
        P(f"  h4 {cls}: median {np.median(hv):+.4f} +- {se:.4f}, Spearman(h4, lambda_Re) {rho.statistic:+.3f} (p {rho.pvalue:.2g}), n {int(m.sum())}")
        RES["rows"][f"h4_{cls}"] = dict(median=float(np.median(hv)), se=float(se), rho=float(rho.statistic), p=float(rho.pvalue))
    rho = spearmanr(h4[selp], lam[selp]); P(f"  h4 all: Spearman(h4, lambda_Re) {rho.statistic:+.3f} (p {rho.pvalue:.2g})")
    base = roc_auc_score(y, Sp["S"]); rng = np.random.default_rng(SEED); Z = {k: X[k].copy() for k in X}
    # permutation importance on the out-of-fold S scores needs refits; reported as AUC drop when one input is shuffled and S is refit
    for k in B + SH:
        Z = {kk: X[kk].copy() for kk in X}; j = np.flatnonzero(selp); Z[k][j] = X[k][j][rng.permutation(len(j))]
        d = base - roc_auc_score(y, score(oof(B + SH, selp, Z), selp)); P(f"  permutation importance {k}: AUC drop {d:+.4f}"); RES["rows"][f"perm_{k}"] = float(d)
    e = np.arange(9.0, 12.01, 0.25); mm = logm[selp]
    P("  f_slow vs log M*: " + ", ".join(f"[{e[i]:.2f},{e[i + 1]:.2f}) {y[(mm >= e[i]) & (mm < e[i + 1])].mean():.2f} (n {int(((mm >= e[i]) & (mm < e[i + 1])).sum())})"
                                       for i in range(len(e) - 1) if ((mm >= e[i]) & (mm < e[i + 1])).sum() >= 20))
    P("  ATLAS3D: NOT RUN (positions table not fetched)" if not os.path.exists(os.path.join(EXT, "atlas3d_emsellem11", "cappellari11_atlas3d.tsv")) else "  ATLAS3D: see lam2_atlas3d.out")
    # ---- label ----
    m1p = os.path.join(HERE, "lam2_grade_MUTATE.json"); M1 = json.load(open(m1p))["M1"] if os.path.exists(m1p) else None
    R = Rp
    if not RES["K1"]["pass_"] or (M1 is not None and not M1["pass_"]): lab = "NO VERDICT"
    elif K2 is not None and not K2["pass_"]: lab = "h4 NOT MEASURABLE"
    elif not R["E3"]["pass_"]: lab = "NO KINEMATIC AXIS BEYOND PHOTOMETRY"
    elif not R["E4"]["pass_"]: lab = "SPECTRAL, AGE-DEGENERATE"
    elif not (R["E1"] and R["E2"]): lab = "KINEMATIC AXIS, TOO NOISY TO LABEL"
    else: lab = "KINEMATIC ESTIMATOR"
    if K2 is None or M1 is None: lab += " (PROVISIONAL: " + ", ".join(x for x, v in (("K2", K2), ("M1", M1)) if v is None) + " not run)"
    P(f"\nLABEL (gas-poor): {lab}"); RES["label"] = lab
sfx = "" if MODE == "REAL" else f"_{MODE}"
open(os.path.join(HERE, f"lam2_grade{sfx}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"lam2_grade{sfx}.json"), "w"), indent=1, default=float)
