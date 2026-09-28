#!/usr/bin/env python3
"""MC3 -- SE-model audit at q in {6,10} (Z7 successor; owns MC3_*).
Door: MC2's pre-registered SE1 gate fired (rep_se 2.04x analytic at q=10,
MC2_results.json exit 1). Resolve whether the replicate-SE inflation at q=10
is a real heavy-tail effect (c0 estimator variance >> CLT s/sqrt(n) at tau0=1e-3)
or a small-replicate artifact (4 reps cannot resolve a SE).
Budget fixed BEFORE any run (house rule 3): q in {6.0, 10.0}, tau0=1e-3,
8 replicates x n=3e6 per point (n_eff=2.4e7, same as MC2's total per point),
seeds 2101..2116, Pool(8), single pass, no re-tuning.
Gates:
  S1: per point, replicate SE vs analytic s/sqrt(8): ratio recorded; the two
      points' ratios must agree within 2x of each other for a SE-DEFECT claim.
  S2: pooled c0 vs MC2 stored per-q, |z| <= 3 each (else PARITY-FAIL kill).
  S3: pooled c0 vs MC1 stored per-q, |z| <= 3 each (else PARITY-FAIL kill).
Pre-registered verdicts:
  - If rep_se/ana <= 1.5 at BOTH q: SE was 4-rep noise -> MC2's non-bank was
    over-conservative; verdict SE-CLEAN (record; MC2 stays non-banked -- the
    line claim itself needs its own re-run under the resolved SE model).
  - If rep_se/ana > 1.5 at BOTH q with consistent ratios: SE-DEFECT-CONFIRMED
    (heavy-tail estimator; analytic SE model wrong at tau0=1e-3, q>=6);
    record ratio as the corrected SE inflation factor.
  - Mixed (one point <= 1.5, other > 1.5): SE-INCONSISTENT (record, no claim).
Kills: parity (S2/S3) fail -> exit 1 with the z's. Both clean-exit branches
record, do NOT re-open MC2's bank. No budget tuning."""
import json, os, sys, time
import numpy as np
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "fable_independent_2026"))
OUT = os.path.join(HERE, "MC3_se_audit.out")
RESF = os.path.join(HERE, "MC3_results.json")
_T0 = time.time()
LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="MC3 SE-model audit q in {6,10}",
               pre_registration="Z7-WAVE_BRIEF.md amendment 2 / MC3 docstring",
               verdict=verdict, exit=rc, elapsed_s=round(time.time() - _T0, 1), log=LOG)
    if extra: RES.update(extra)
    with open(RESF, "w") as f: json.dump(RES, f, indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

from J02_moment_hierarchy import simulate as S

def one(job):
    q, tau0, seed = job
    r = S(3_000_000, tau0, q, "volume", seed=seed)
    D = np.asarray(r["D"])
    # c0 normalization per MC1/MC2 convention: (mean D)/tau0, SE/tau0
    return float(D.mean()) / tau0, (float(D.std(ddof=1) / np.sqrt(len(D)))) / tau0

QS = [6.0, 10.0]
TAU0 = 1e-3
SEED0 = 2101
jobs = [(q, TAU0, SEED0 + 8 * i + j) for i, q in enumerate(QS) for j in range(8)]
log("S1: %d jobs, n=3e6 x 8 reps/point, seeds %d.." % (len(jobs), SEED0))
with get_context("fork").Pool(8) as p:
    res = p.map(one, jobs)

meas = {}
for i, q in enumerate(QS):
    means = [res[8 * i + j][0] for j in range(8)]
    ses   = [res[8 * i + j][1] for j in range(8)]
    pooled = float(np.mean(means))
    rep_se = float(np.std(means, ddof=1) / np.sqrt(8))
    s_pool = float(np.mean(ses))
    ana_se = s_pool / np.sqrt(8.0)
    ratio = rep_se / ana_se
    meas[q] = dict(pooled_c0=pooled, rep_se=rep_se, ana_se=ana_se,
                   ratio=ratio, rep_means=means)
    log("S1: q=%g: c0 = %.6f  rep_se=%.6f ana_se=%.6f ratio=%.2f" % (q, pooled, rep_se, ana_se, ratio))

r6, r10 = meas[6.0]["ratio"], meas[10.0]["ratio"]

# S2/S3 parity
mc2 = json.load(open(os.path.join(HERE, "MC2_results.json")))["meas"]
mc1 = json.load(open(os.path.join(HERE, "MC1_results.json")))["meas"]
for tag, src, pts in (("S2", mc2, (6.0, 10.0)), ("S3", mc1, (6.0, 10.0))):
    for q in pts:
        val = src[str(q)]
        c0s, s0 = (float(val[0]), float(val[1])) if isinstance(val, (list, tuple)) \
                  else (float(val["pooled_c0"]), float(val["rep_se"]))
        z = (meas[q]["pooled_c0"] - c0s) / np.sqrt(meas[q]["ana_se"] ** 2 + s0 ** 2)
        log("%s: q=%g vs %s stored %.6f: z = %+.2f" % (tag, q, tag, c0s, z))
        if abs(z) > 3:
            finish(1, "%s-PARITY-FAIL vs %s stored (z=%+.2f)" % (tag, tag, z))

clean6, clean10 = r6 <= 1.5, r10 <= 1.5
if clean6 and clean10:
    finish(0, "SE-CLEAN: replicate/analytic <= 1.5 at both q (%.2f, %.2f) -- MC2's SE1 fire was 4-rep noise; MC2 non-bank stands; line unbanked pending re-run" % (r6, r10))
elif (not clean6) and (not clean10) and max(r6, r10) / min(r6, r10) <= 2.0:
    finish(0, "SE-DEFECT-CONFIRMED: replicate/analytic = %.2f/%.2f consistent heavy-tail inflation at q>=6 (analytic SE model wrong at tau0=1e-3); recorded as corrected inflation factor; MC2 non-bank stands" % (r6, r10))
else:
    finish(0, "SE-INCONSISTENT: ratios %.2f/%.2f disagree (mixed/2x-inconsistent); no SE claim; MC2 non-bank stands" % (r6, r10))
