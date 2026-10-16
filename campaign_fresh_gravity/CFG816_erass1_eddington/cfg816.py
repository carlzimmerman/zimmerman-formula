"""CFG816 -- Eddington bias in eRASS1 gas masses (data side).  Criteria: FROZEN_CRITERIA.md (4eef19bc8).  Seconds.
Run: python3 cfg816.py   (CFG816_MUTATE=1: sigma shuffled).  kappa = 1/2 FITTED; not theory closed."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
EXT = os.path.abspath(os.path.join(LANES, "..", "..", "_external_data"))
MUT = os.environ.get("CFG816_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
rows = []
for l in open(os.path.join(EXT, "cfg687_inputs", "erass1_main.tsv")):
    r = l.rstrip("\n").split("\t")
    try:
        ra, de, z, mg, lo, hi = float(r[1]), float(r[2]), float(r[3]), float(r[5]), float(r[6]), float(r[7])
    except Exception:
        continue
    if mg > 0 and lo > 0 and hi > 0: rows.append((ra, de, z, mg, lo, hi))
C = np.array(rows); P(f"CFG816  Eddington bias check" + ("  [MUTATE]" if MUT else "") + f"; catalogue rows with Mgas + bounds: {len(C)}")
# alpha from full catalogue, 0.05 <= z <= 0.5
sel = (C[:, 2] >= 0.05) & (C[:, 2] <= 0.5); lm = np.log(C[sel, 3] * 1e11)
h, e = np.histogram(lm, bins=40); c = 0.5 * (e[1:] + e[:-1]); k0 = int(np.argmax(h))
use = (np.arange(len(h)) > k0) & (h >= 5)
def fit_alpha(hh):
    m = use & (hh > 0); return -np.polyfit(c[m], np.log(hh[m]), 1)[0]
alpha = fit_alpha(h)
rng = np.random.default_rng(816); boots = []
for _ in range(500):
    bb = rng.choice(lm, len(lm)); hb, _ = np.histogram(bb, bins=e); boots.append(fit_alpha(hb))
P(f"  alpha (dN/dlnM ~ M^-alpha above the peak) = {alpha:.3f} +- {np.std(boots):.3f} ({use.sum()} bins)")
# match CFG687's 318
d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz")); n = len(d["mg"])
sig = np.zeros(n)
for i in range(n):
    dd = (C[:, 0] - d["ra"][i]) ** 2 * np.cos(np.radians(d["dec"][i])) ** 2 + (C[:, 1] - d["dec"][i]) ** 2
    j = int(np.argmin(dd)); sig[i] = 0.5 * (np.log(C[j, 5]) - np.log(C[j, 4]))
if MUT:
    sig = rng.permutation(sig)
corr = np.exp(-alpha * sig ** 2)                         # M_true / M_obs
mg_t = d["mg"] * corr
D, E = d["D"], d["E"]; W = np.where(E > 0, 1 / E ** 2, 0)
order = np.argsort(d["ra"]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
A_of = lambda s_, Pm: (W[s_][:, 3:6] * D[s_][:, 3:6]).sum() / (W[s_][:, 3:6] * Pm[s_][:, 3:6]).sum()
def jk(s_, Pm):
    f = A_of(s_, Pm); reps = [A_of(s_ & (patch != q), Pm) for q in range(30)]
    return f, float(np.sqrt(29 / 30 * np.sum((np.array(reps) - np.mean(reps)) ** 2)))
def terc(mgv):
    q = np.quantile(mgv, [1 / 3, 2 / 3]); return [mgv <= q[0], (mgv > q[0]) & (mgv <= q[1]), mgv > q[1]]
T0, T1 = terc(d["mg"]), terc(mg_t)
P("  median sigma per (observed) tercile: " + " / ".join(f"{np.median(sig[t]):.3f}" for t in T0) + "; median M_true/M_obs: " + " / ".join(f"{np.median(corr[t]):.3f}" for t in T0))
ER9 = list(np.load(os.path.join(EXT, "cfg809_work", "erass.npy"), allow_pickle=True)); ER15 = list(np.load(os.path.join(EXT, "cfg815_work_P", "erass.npy"), allow_pickle=True))
k = "s|canonical|EX"
MODELS = {"plain law": d["PL"], "CFG809 H-EX": np.array([o[k]["base"] + o[k]["res"] for o in ER9]), "CFG815 P": np.array([o[k]["base"] + o[k]["res"] for o in ER15])}
s_slope = 0.47
RES = dict(lane="CFG816", mutate=MUT, alpha=float(alpha), alpha_err=float(np.std(boots)))
mono_flag = {}
for name, Pm in MODELS.items():
    Pc = Pm * (corr ** s_slope)[:, None]
    b = [jk(t, Pm) for t in T0]; a = [jk(t, Pc) for t in T1]
    P(f"  {name:12s} MID terciles before: " + " / ".join(f"{x[0]:.2f}+-{x[1]:.2f}" for x in b) + "   after: " + " / ".join(f"{x[0]:.2f}+-{x[1]:.2f}" for x in a))
    def mono(v):
        ok_up = all(v[j + 1][0] - v[j][0] >= -np.hypot(v[j][1], v[j + 1][1]) for j in range(2))
        ok_dn = all(v[j + 1][0] - v[j][0] <= np.hypot(v[j][1], v[j + 1][1]) for j in range(2))
        return ok_up or ok_dn
    mono_flag[name] = (mono(b), mono(a)); RES[name] = dict(before=b, after=a, mono_before=mono(b), mono_after=mono(a))
k1 = all(abs(jk(t, MODELS["CFG815 P"])[0] - jk(t, MODELS["CFG815 P"])[0]) < 1e-12 for t in T0)
P(f"  K1 (sigma = 0 is the identity on terciles/models): {'PASS' if k1 else 'FAIL'}")
mb, ma = mono_flag["CFG815 P"]
cls = "SELECTION EXPLAINS PATTERN" if (ma and not mb) else ("ALREADY MONOTONIC" if mb else "NOT EXPLAINED")
P(f"\n  CFG815 P monotonic before {mb}, after {ma} -> {cls}")
RES["cls"] = cls
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg816_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg816{sfx}.out"), "w").write("\n".join(OUT) + "\n")
