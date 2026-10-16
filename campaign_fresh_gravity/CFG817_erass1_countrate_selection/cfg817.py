"""CFG817 -- eRASS1 count-rate selection forward model for M_gas Eddington bias.  Criteria: FROZEN_CRITERIA.md (07feacacc).
Run: python3 cfg817.py   (CFG817_MUTATE=1: C = 1, no selection; CFG817_K1=1: C = 1 and sigma_meas = 0).  ~1 min.
kappa = 1/2 FITTED; not theory closed."""
import os, json, math, numpy as np
from scipy.optimize import curve_fit
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
EXT = os.path.abspath(os.path.join(LANES, "..", "..", "_external_data"))
MUT = os.environ.get("CFG817_MUTATE") == "1"; K1 = os.environ.get("CFG817_K1") == "1"; COND_N = os.environ.get("CFG817_CONDN") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def fl(x):
    try: return float(x)
    except: return np.nan
R = []
for l in open(os.path.join(EXT, "cfg817_erass1_selection", "erass1_sel.tsv")):
    if not l.startswith("1eRASS"): continue
    p = l.rstrip("\n").split("\t"); R.append([fl(x) for x in p[1:]])
A = np.array(R)   # RAX DEX z ExtLike DetLike0 Exp CTS bCTS BCTS CR Mg bMg BMg R500 L500
ra, de, z, el, dl0, ex, N, bN, BN, cr, Mg, bMg, BMg = [A[:, k] for k in range(13)]
P(f"CFG817  eRASS1 count-rate selection model" + ("  [POST-FREEZE: conditioned on observed counts too]" if COND_N else "") + ("  [MUTATE C=1]" if MUT else "") + ("  [K1 null]" if K1 else "") + f"; rows {len(A)}")
# distances (flux only)
zz = np.linspace(0, 1.5, 3001); Ez = np.sqrt(0.315 * (1 + zz) ** 3 + 0.685)
Dc = np.r_[0, np.cumsum(0.5 * (1 / Ez[1:] + 1 / Ez[:-1]) * np.diff(zz))] * 299792.458 / 67.4
dL = lambda zv: np.interp(zv, zz, Dc) * (1 + zv)
# 1 completeness in counts
ok = np.isfinite(N) & (N > 0); lN = np.log(N[ok])
h, e = np.histogram(lN, bins=50); c = 0.5 * (e[1:] + e[:-1]); k0 = int(np.argmax(h))
hi = (np.arange(50) > k0 + 1) & (h >= 10)
gam_p = np.polyfit(c[hi], np.log(h[hi]), 1); ext = np.exp(np.polyval(gam_p, c))
ratio = np.clip(h / ext, 0, 1.2); use = np.arange(50) <= k0 + 4
logistic = lambda x, mu, w: 1 / (1 + np.exp(-(x - mu) / w))
(mu, w), _ = curve_fit(logistic, c[use], np.minimum(ratio[use], 1.0), p0=[c[k0], 0.3], maxfev=20000)
Cfun = (lambda lnN: np.ones_like(lnN)) if (MUT or K1) else (lambda lnN: logistic(lnN, mu, w))
N90 = math.exp(mu + w * math.log(9))
P(f"  1 completeness: dN/dlnN slope {gam_p[0]:.3f}; logistic mu {mu:.3f} (N50 {math.exp(mu):.1f} cts), w {w:.3f}; N90 {N90:.1f} cts")
# 2 counts-mass relation on complete sample
m2 = ok & np.isfinite(Mg) & (Mg > 0) & np.isfinite(ex) & (ex > 0) & np.isfinite(z) & (z > 0.02) & (N > N90)
y = np.log(N[m2] / ex[m2]) + 2 * np.log(dL(z[m2])); X = np.c_[np.ones(m2.sum()), np.log(Mg[m2] * 1e11), z[m2]]
coef, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ coef; sint = float(np.std(res))
P(f"  2 ln(N/Exp) = {coef[0]:.3f} + {coef[1]:.3f} ln Mgas - 2 ln dL + {coef[2]:.3f} z; sigma_int {sint:.3f} (n {m2.sum()})")
# 3 measurement error vs counts
m3 = ok & np.isfinite(bMg) & np.isfinite(BMg) & (bMg > 0) & (BMg > bMg)
sm = 0.5 * (np.log(BMg[m3]) - np.log(bMg[m3])); pm = np.polyfit(np.log(N[m3]), np.log(sm), 1)
smeas = (lambda lnN: np.zeros_like(lnN)) if K1 else (lambda lnN: np.exp(np.polyval(pm, lnN)))
P(f"  3 sigma_meas(lnMgas) = exp({pm[1]:.3f} + {pm[0]:.3f} ln N)  (e.g. N=20: {float(np.exp(np.polyval(pm, math.log(20)))):.2f}, N=300: {float(np.exp(np.polyval(pm, math.log(300)))):.2f})")
# 4 alpha with completeness weights
m4 = ok & np.isfinite(Mg) & (Mg > 0) & (z >= 0.05) & (z <= 0.5)
wts = 1 / np.maximum(logistic(np.log(N[m4]), mu, w), 0.05)
h4, e4 = np.histogram(np.log(Mg[m4] * 1e11), bins=40, weights=wts); c4 = 0.5 * (e4[1:] + e4[:-1]); k4 = int(np.argmax(h4))
u4 = (np.arange(40) > k4) & (h4 > 5); alpha = float(-np.polyfit(c4[u4], np.log(h4[u4]), 1)[0])
P(f"  4 alpha (completeness-weighted) = {alpha:.3f}")
# 5 per-target simulation
d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz")); n = len(d["mg"])
rng = np.random.default_rng(817); corr = np.ones(n); nd = np.zeros(n)
for i in range(n):
    jj = int(np.argmin((ra - d["ra"][i]) ** 2 * math.cos(math.radians(d["dec"][i])) ** 2 + (de - d["dec"][i]) ** 2))
    zi, exi = float(d["z"][i]), float(ex[jj]); lmo = math.log(float(d["mg"][i])); lNo = math.log(max(float(N[jj]), 1.0))
    S = 400000; lmt = rng.uniform(lmo - 4.0, lmo + 2.0, S); wprior = np.exp(-alpha * (lmt - lmo))
    lnNexp = coef[0] + coef[1] * lmt - 2 * math.log(dL(zi)) + coef[2] * zi + math.log(exi) + rng.normal(0, sint, S)
    Nobs = rng.poisson(np.exp(np.minimum(lnNexp, 20))); good = Nobs > 0
    det = good & (rng.random(S) < Cfun(np.log(np.maximum(Nobs, 1))))
    lmobs = lmt + rng.normal(0, 1, S) * smeas(np.log(np.maximum(Nobs, 1)))
    win = det & (np.abs(lmobs - lmo) < 0.05)
    if COND_N:
        win = win & (np.abs(np.log(np.maximum(Nobs, 1)) - lNo) < 0.15)
    nd[i] = win.sum()
    if win.sum() > 20:
        ww = wprior[win]; corr[i] = math.exp(float((ww * lmt[win]).sum() / ww.sum()) - lmo)
mg = d["mg"]; q = np.quantile(mg, [1 / 3, 2 / 3]); T0 = [mg <= q[0], (mg > q[0]) & (mg <= q[1]), mg > q[1]]
P(f"  clusters with <= 20 window draws (correction left at 1): {int((nd <= 20).sum())}; per tercile: " + " / ".join(str(int((nd[t] <= 20).sum())) for t in T0))
P("  5 median correction M_true/M_obs per tercile: " + " / ".join(f"{np.median(corr[t]):.3f}" for t in T0) + f"  (CFG816 -asig^2: 0.29 / 0.84 / 0.95); min window draws {int(nd.min())}")
if K1:
    P(f"  K1 null: max |corr - 1| = {np.max(np.abs(corr - 1)):.4f} -> {'PASS' if np.max(np.abs(corr - 1)) < 0.01 else 'FAIL'}")
RES = dict(lane="CFG817", mutate=MUT, k1run=K1, mu=float(mu), w=float(w), N90=N90, coef=coef.tolist(), sigma_int=sint, pm=pm.tolist(), alpha=alpha,
           corr_terciles=[float(np.median(corr[t])) for t in T0])
if not (MUT or K1):
    D, E = d["D"], d["E"]; W = np.where(E > 0, 1 / E ** 2, 0)
    order = np.argsort(d["ra"]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
    A_of = lambda s_, Pm: (W[s_][:, 3:6] * D[s_][:, 3:6]).sum() / (W[s_][:, 3:6] * Pm[s_][:, 3:6]).sum()
    def jk(s_, Pm):
        f = A_of(s_, Pm); reps = [A_of(s_ & (patch != qq), Pm) for qq in range(30)]
        return f, float(np.sqrt(29 / 30 * np.sum((np.array(reps) - np.mean(reps)) ** 2)))
    mgt = mg * corr; q1 = np.quantile(mgt, [1 / 3, 2 / 3]); T1 = [mgt <= q1[0], (mgt > q1[0]) & (mgt <= q1[1]), mgt > q1[1]]
    ER9 = list(np.load(os.path.join(EXT, "cfg809_work", "erass.npy"), allow_pickle=True)); ER15 = list(np.load(os.path.join(EXT, "cfg815_work_P", "erass.npy"), allow_pickle=True))
    k = "s|canonical|EX"; MODELS = {"plain law": d["PL"], "CFG809 H-EX": np.array([o[k]["base"] + o[k]["res"] for o in ER9]), "CFG815 P": np.array([o[k]["base"] + o[k]["res"] for o in ER15])}
    def mono(v):
        up = all(v[j + 1][0] - v[j][0] >= -np.hypot(v[j][1], v[j + 1][1]) for j in range(2)); dn = all(v[j + 1][0] - v[j][0] <= np.hypot(v[j][1], v[j + 1][1]) for j in range(2))
        return up or dn
    for name, Pm in MODELS.items():
        b = [jk(t, Pm) for t in T0]; a = [jk(t, Pm * (corr ** 0.47)[:, None]) for t in T1]
        RES[name] = dict(before=b, after=a, mono_after=mono(a))
        P(f"  {name:12s} MID terciles before: " + " / ".join(f"{x[0]:.2f}+-{x[1]:.2f}" for x in b) + "   after: " + " / ".join(f"{x[0]:.2f}+-{x[1]:.2f}" for x in a))
    ct = RES["corr_terciles"]; ref = [0.29, 0.84, 0.95]
    agree = all(1 / 1.5 <= ct[j] / ref[j] <= 1.5 for j in range(3)); mon = RES["CFG815 P"]["mono_after"]
    cls = "CONFIRMS CFG816" if (agree and mon) else "REVISES"
    P(f"\n  corrections agree with CFG816 within x1.5: {agree}; CFG815 P monotonic after: {mon} -> {cls}")
    RES["cls"] = cls
sfx = ("_MUTATE" if MUT else ("_K1" if K1 else "")) + ("_CONDN" if COND_N else "")
json.dump(RES, open(os.path.join(HERE, f"cfg817_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg817{sfx}.out"), "w").write("\n".join(OUT) + "\n")
