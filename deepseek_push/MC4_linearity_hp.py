#!/usr/bin/env python3
"""MC4 -- c0(q) full-grid linearity re-run under the MC3-resolved SE model
(Z7 successor; owns MC4_*).  Door: MC2 banked nothing (SE1 fire, register
Z7 MC2 row); MC3 proved the SE model is clean at 8 reps (ratios 0.81/1.04,
MC3_results.json exit 0).  This lane re-runs the FULL grid at higher power
with an SE gate that 8 replicates can actually resolve.
Budget fixed BEFORE any run (house rule 3): q in {0,1,3,6,10}, tau0=1e-3,
6 replicates x n=4e6 per point (n_eff=2.4e7 = MC2's power), seeds 3101..3130,
Pool(8), single pass, no re-tuning.
Gates:
  P0: pooled c0 vs MC1 stored per-q, |z| <= 3 each (else PARITY-FAIL -> exit 1).
  SE1': replicate SE vs analytic s/sqrt(6): ratio > 1.5 at ANY point ->
        SE-ANOMALY record, do NOT bank (MC3 says this should not happen).
  M2': weighted LS a+bq on {0,1,3}, predict {6,10}; any |z_pred| > 3 ->
        kill c0-NOT-LINEAR-HIGHPOWER, exit 1.
  SE-weighted fit only if all SE1' ratios <= 1.5.
Exit 0 (BANKED-LINEAR-HIGHPOWER) iff P0 pass AND no SE1' anomaly AND M2' no kill.
The thin-window curve R_v(0,q) = (3/4 + 5q/12)/(a+bq) is then CANDIDATE-only
(recorded in results, never banked without its own door)."""
import json, os, sys, time
import numpy as np
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "MC4_linearity_hp.out")
RESF = os.path.join(HERE, "MC4_results.json")
_T0 = time.time()
LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="MC4 c0(q) full-grid linearity re-run (high power)",
               pre_registration="Z7-WAVE_BRIEF.md amendment 2 / MC4 docstring",
               verdict=verdict, exit=rc, elapsed_s=round(time.time() - _T0, 1), log=LOG)
    if extra: RES.update(extra)
    with open(RESF, "w") as f: json.dump(RES, f, indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate as S

def one(job):
    q, tau0, seed = job
    r = S(4_000_000, tau0, q, "volume", seed=seed)
    D = np.asarray(r["D"])
    return float(D.mean()) / tau0, (float(D.std(ddof=1) / np.sqrt(len(D)))) / tau0

QS = [0.0, 1.0, 3.0, 6.0, 10.0]
TAU0 = 1e-3
SEED0 = 3101
REPS = 6
jobs = [(q, TAU0, SEED0 + REPS * i + j) for i, q in enumerate(QS) for j in range(REPS)]
log("P0: %d jobs, n=4e6 x %d reps/point, seeds %d.." % (len(jobs), REPS, SEED0))
with get_context("fork").Pool(8) as p:
    res = p.map(one, jobs)

meas = {}
se_anom = []
for i, q in enumerate(QS):
    means = [res[REPS * i + j][0] for j in range(REPS)]
    ses   = [res[REPS * i + j][1] for j in range(REPS)]
    pooled = float(np.mean(means))
    rep_se = float(np.std(means, ddof=1) / np.sqrt(REPS))
    s_pool = float(np.mean(ses))
    ana_se = s_pool / np.sqrt(float(REPS))
    ratio = rep_se / ana_se
    meas[str(q)] = dict(pooled_c0=pooled, rep_se=rep_se, ana_se=ana_se, ratio=ratio,
                        rep_means=means)
    log("P0: q=%g: c0 = %.6f  rep_se=%.6f ana_se=%.6f ratio=%.2f" % (q, pooled, rep_se, ana_se, ratio))
    if ratio > 1.5:
        se_anom.append((q, ratio))
if se_anom:
    finish(1, "SE-ANOMALY: replicate/analytic > 1.5 at %s; NOT banked (record only)" % se_anom,
           dict(meas=meas))

mc1 = json.load(open(os.path.join(HERE, "MC1_results.json")))["meas"]
for q in QS:
    val = mc1[str(q)]
    c0s, s0 = float(val[0]), float(val[1])
    z = (meas[str(q)]["pooled_c0"] - c0s) / np.sqrt(meas[str(q)]["ana_se"] ** 2 + s0 ** 2)
    log("P0: q=%g vs MC1 stored %.6f: z = %+.2f" % (q, c0s, z))
    if abs(z) > 3:
        finish(1, "P0-PARITY-FAIL vs MC1 stored at q=%g (z=%+.2f)" % (q, z))

fit_q = [0.0, 1.0, 3.0]
A = np.array([[1.0, q] for q in fit_q])
y = np.array([meas[str(q)]["pooled_c0"] for q in fit_q])
w = np.array([1.0 / meas[str(q)]["rep_se"] ** 2 for q in fit_q])
W = np.diag(w)
ata = A.T @ W @ A; aty = A.T @ W @ y
a, b = np.linalg.solve(ata, aty)
cov = np.linalg.inv(ata)
sig_b = float(np.sqrt(cov[1, 1]))
log("M2': fit c0(q) = %.6f + %.6f q (b/sigma_b = %.1f)" % (a, b, abs(b) / sig_b))
preds = {}
for q in (6.0, 10.0):
    c0m = meas[str(q)]["pooled_c0"]
    sm = meas[str(q)]["rep_se"]
    z = ((a + b * q) - c0m) / sm
    preds[str(q)] = z
    log("M2': predict q=%g: pred %.6f vs meas %.6f +- %.6f, z = %+.2f" % (q, a + b * q, c0m, sm, z))
if any(abs(z) > 3 for z in preds.values()):
    finish(1, "c0-NOT-LINEAR-HIGHPOWER: held-out kill fired %s" % preds, dict(meas=meas, fit=dict(a=a, b=b, sig_b=sig_b), preds=preds))
Rv = {str(q): (0.75 + 5.0 * q / 12.0) / (a + b * q) for q in QS}
log("CANDIDATE curve R_v(0,q) = (3/4 + 5q/12)/(a+bq): %s" % Rv)
finish(0, "BANKED-LINEAR-HIGHPOWER: c0 = %.6f + %.6f q at n_eff=2.4e7 (b/sigma_b=%.1f); "
          "P0 pass, SE clean (max ratio %.2f), M2' no kill; R_v(0,q) recorded CANDIDATE-only"
          % (a, b, abs(b) / sig_b, max(meas[str(q)]["ratio"] for q in QS)),
      dict(meas=meas, fit=dict(a=a, b=b, sig_b=sig_b), preds=preds, Rv_candidate=Rv))
