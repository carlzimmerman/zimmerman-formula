#!/usr/bin/env python3
"""MC2 -- c0(q) linearity at higher power (Z7-wave; owns MC2_*).
Door: MC1's honest MDE note (pred-SE 0.019/0.023 at q=6/10) -- bank the line
or kill it at n_eff = 4x MC1. Engine: J02_moment_hierarchy.simulate (loaded,
never transcribed). Budget fixed BEFORE any run (house rule 3): q in
{0,1,3,6,10}, tau0=1e-3, 4 replicates x n=6e6 per point (n_eff=2.4e7), seeds
1101..1120, Pool(8), single pass, no re-tuning.
Gates (Z7-WAVE_BRIEF.md, fixed before any run):
  P0: pooled c0 vs MC1_results.json stored per-q c0, |z| <= 3 each.
  SE1: replicate-based SE vs analytic s/sqrt(n_eff); replicate > 2x analytic
       -> SE-MODEL-MISMATCH flag, record, do NOT bank.
  M2: weighted LS a+bq on {0,1,3}, predict {6,10}; any |z_pred| > 3 ->
      c0-NOT-LINEAR-HIGHPOWER (kill, exit 1). Else BANKED-LINEAR at n_eff=2.4e7
      with honest MDE; curve R_v(0,q) recorded as CANDIDATE only.
exit 0 iff P0 pass AND SE1 not mismatched AND M2 no kill fired."""
import json, os, sys, time
import numpy as np
from multiprocessing import get_context
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "MC2_c0_highpower.out")
RESF = os.path.join(HERE, "MC2_results.json")
_T0 = time.time()
LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="MC2 c0(q) higher power", pre_registration="Z7-WAVE_BRIEF.md MC2 gates",
               verdict=verdict, exit=rc, elapsed_s=round(time.time() - _T0, 1), log=LOG)
    if extra: RES.update(extra)
    with open(RESF, "w") as f: json.dump(RES, f, indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

def one(job):
    from J02_moment_hierarchy import simulate
    q, tau0, seed = job
    from J02_moment_hierarchy import simulate as S
    r = S(6_000_000, tau0, q, "volume", seed=seed)
    D = np.asarray(r["D"])
    return float(D.mean()), float(D.std(ddof=1) / np.sqrt(len(D)))

QS = [0.0, 1.0, 3.0, 6.0, 10.0]
TAU0 = 1e-3
SEED0 = 1101

jobs = [(q, TAU0, SEED0 + 5 * i + j) for i, q in enumerate(QS) for j in range(4)]
log("P0: %d jobs, n=6e6 x 4 reps/point, seeds %d.." % (len(jobs), SEED0))
with get_context("fork").Pool(8) as p:  # fork: macOS spawn re-imports module (no __main__ guard) and would fork-bomb
    res = p.map(one, jobs)

meas = {}
for i, q in enumerate(QS):
    means = [res[4 * i + j][0] for j in range(4)]
    ses   = [res[4 * i + j][1] for j in range(4)]
    pooled = float(np.mean(means))
    rep_se = float(np.std(means, ddof=1) / np.sqrt(4))     # replicate-based SE of pooled mean
    s_pool = float(np.mean(ses))                            # mean per-rep analytic SE
    ana_se = s_pool / 2.0                                   # analytic SE at n_eff = 4x6e6
    meas[q] = dict(pooled_c0=pooled / TAU0, rep_se=rep_se / TAU0, ana_se=ana_se / TAU0,
                   rep_means=[m / TAU0 for m in means])
    log("P0: q=%g: c0 = %.6f  rep_se=%.6f ana_se=%.6f" % (q, meas[q]["pooled_c0"], meas[q]["rep_se"], meas[q]["ana_se"]))

# ---- P0 parity vs MC1 stored ----
mc1 = json.load(open(os.path.join(HERE, "MC1_results.json")))
stored = mc1.get("measurements") or mc1.get("meas") or {}
p0 = []
for q in (0.0, 3.0, 10.0):
    key = next((k for k in (str(q), str(int(q)), "c0_q%d" % int(q)) if k in stored), None)
    if key is not None:
        val = stored[key]
        if isinstance(val, (list, tuple)):
            c0s, s0 = float(val[0]), float(val[1])
        else:
            c0s = val.get("c0") or val.get("c") or val.get("mean")
            s0 = val.get("se") or val.get("s")
            if c0s is None: continue
        z = (meas[q]["pooled_c0"] - float(c0s)) / np.sqrt(meas[q]["ana_se"] ** 2 + (float(s0) if s0 else 0.0) ** 2)
        p0.append((q, float(c0s), float(z)))
        log("P0: q=%g vs MC1 stored %.6f: z = %+.2f" % (q, float(c0s), z))
if len(p0) < 3 or any(abs(z) > 3 for _, _, z in p0):
    finish(1, "P0-FAIL: parity vs MC1 stored not met", dict(p0=p0))

# ---- SE1 split-SE honesty ----
se1_bad = [q for q in QS if meas[q]["rep_se"] > 2.0 * meas[q]["ana_se"]]
if se1_bad:
    finish(1, "SE-MODEL-MISMATCH: replicate SE > 2x analytic at q=%s; NOT banked" % se1_bad,
           dict(meas={str(k): v for k, v in meas.items()}))
log("SE1: replicate SE consistent with analytic at all points (no mismatch)")

# ---- M2 weighted LS on {0,1,3}, predict {6,10} ----
fit_qs = [0.0, 1.0, 3.0]
x = np.array(fit_qs); y = np.array([meas[q]["pooled_c0"] for q in fit_qs])
w = 1.0 / np.array([meas[q]["rep_se"] ** 2 for q in fit_qs])
A = np.vstack([np.ones_like(x), x]).T
W = np.diag(w)
cov = np.linalg.inv(A.T @ W @ A)
coef = cov @ (A.T @ W @ y)
a, b = float(coef[0]), float(coef[1])
sa = float(np.sqrt(cov[0, 0])); sb = float(np.sqrt(cov[1, 1]))
log("M2: fit c0(q) = %.6f + %.6f q  (sa=%.6f sb=%.6f, b/sb=%.1f)" % (a, b, sa, sb, b / sb if sb else 0.0))
pred = {}
for q in (6.0, 10.0):
    mu = a + b * q
    s = float(np.sqrt(cov[0, 0] + q * q * cov[1, 1] + 2 * q * cov[0, 1] + meas[q]["rep_se"] ** 2))
    z = (meas[q]["pooled_c0"] - mu) / s
    pred[q] = (mu, s, float(z))
    log("M2: predict q=%g: %+.4f +- %.4f vs measured %+.4f -> z = %+.2f" % (q, mu, s, meas[q]["pooled_c0"], z))
if any(abs(z[2]) > 3 for z in pred.values()):
    finish(1, "c0-NOT-LINEAR-HIGHPOWER (pre-registered kill fired)", dict(coef=[a, b], pred={str(k): v for k, v in pred.items()}))
mde = 3.0 * max(meas[q]["rep_se"] for q in (6.0, 10.0))
finish(0, "BANKED-LINEAR at n_eff=2.4e7 (no kill fired); curve R_v(0,q)=(3/4+5q/12)/(a+bq) recorded CANDIDATE",
       dict(coef=dict(a=a, b=b, sa=sa, sb=sb), pred={str(k): v for k, v in pred.items()},
            mde=mde, meas={str(k): v for k, v in meas.items()},
            candidate_curve="R_v(0,q) = (3/4 + 5*q/12)/(a + b*q), a=%.6f b=%.6f -- CANDIDATE, not banked as exact law" % (a, b)))
