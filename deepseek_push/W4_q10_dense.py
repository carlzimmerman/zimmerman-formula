#!/usr/bin/env python3
"""W4 -- q=10 scope-tension dense-grid MC (Z13 door; owns W4_*).

Door: W3 (exit 0) recorded the q=10 SCOPE tension: predicted c1(10) =
-S(10) + E2(10) = -12.428571 + 26.309547 = +13.880976 vs W3's anchored
measured c1(10) = -2.6495 +- 1.2212 (MC7's own LOO-unstable,
quadratic-selected point). Whether MC7 extrapolation bias at the
quadratic-selected q or real structure beyond O(tau0) is OPEN.

Budget (fixed before any run, Z13-WAVE_BRIEF.md W4 door): q = 10 ONLY;
tau0 grid 6 values {1e-3, 6e-4, 4e-4, 2.5e-4, 1.5e-4, 1e-4}; n = 8e6 x 5
reps/cell (n_eff 4e7/cell), seeds 8101.., single pass, no re-tuning.
Engine: J02 simulate (loaded, not transcribed).
KILLS pre-registered:
  M2: parity vs MC7's stored tau0=1e-3 q=10 point |z| <= 3 combined SE,
      else exit 1.
  Execution failure -> exit 1.
M3 branches (pre-registered, all exit-0 outcomes):
  (a) |c1_meas - 13.880976| <= 3 sqrt(se^2 + se_pred^2), se_pred = 0.0145
      (W3 E2 MC SE): W3 decomposition HOLDS at q=10; MC7 q=10 point
      recorded as extrapolation-bias-limited.
  (b) c1_meas <= 0 at >= 3 combined SE: REAL structure beyond c1 = -S + E2;
      successor door W5 registered in the ops note.
  (c) otherwise UNRESOLVED at this power (recorded).
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate

OUT = os.path.join(HERE, "W4_q10_dense.out")
RESF = os.path.join(HERE, "W4_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="W4 q=10 dense-grid MC: scope-tension adjudication",
               pre_registration="Z13-WAVE_BRIEF.md W4 door",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF,"w"), indent=1, default=str)
    with open(OUT,"a") as f: f.write("\n".join(LOG)+"\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

Q = 10.0
TAUS = [1e-3, 6e-4, 4e-4, 2.5e-4, 1.5e-4, 1e-4]
N, REPS = 8_000_000, 5
C00_10 = 2/5 + (8/35)*10.0          # 2.685714..., W2/LR8-certified anchor
C1_PRED = -12.428571 + 26.309547    # -S(10) + E2(10), W3 banked
E2_SE = 0.0145
log("anchor c00_exact(10) = %.6f ; W3 pred c1(10) = %+.4f (se_pred %.4f)" % (C00_10, C1_PRED, E2_SE))

pts = []; seed = 8101
for t in TAUS:
    cs = []
    for rep in range(REPS):
        r = simulate(N, t, Q, "volume", seed=seed); seed += 1
        D = np.asarray(r["D"])
        cs.append(float(D.mean())/t)
        del r, D
    pts.append((t, float(np.mean(cs)), float(np.std(cs, ddof=1)/np.sqrt(len(cs)))))
    log("run: tau0=%g: c0 = %.6f +- %.6f" % pts[-1])

# M2: parity vs MC7 stored tau0=1e-3 q=10 point (loaded)
m7 = json.load(open(os.path.join(HERE, "MC7_results.json")))
st = [p for p in m7["meas"]["10.0"]["points"] if abs(p[0]-1e-3) < 1e-12]
if not st:
    finish(1, "M2 SETUP FAIL: MC7 stored tau0=1e-3 q=10 point not found", dict(meas=pts))
st = st[0]
fresh = [p for p in pts if abs(p[0]-1e-3) < 1e-12][0]
comb = np.sqrt(fresh[2]**2 + st[2]**2)
z2 = abs(fresh[1] - st[1])/comb
log("M2: fresh %.6f+-%.6f vs MC7 stored %.6f+-%.6f, z=%.2f (gate 3)" % (fresh[1], fresh[2], st[1], st[2], z2))
if z2 > 3:
    finish(1, "M2 FIRED: fresh vs MC7 stored q=10 tau0=1e-3 z=%.2f > 3" % z2, dict(meas=pts))
log("M2 PASS")

# M1: anchored quadratic fit on all 6 points
t = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts]) - C00_10
se = np.array([p[2] for p in pts])
Wd = np.diag(1/se**2); A = np.vstack([t, t*t]).T
ata = A.T@Wd@A; cov = np.linalg.inv(ata); sol = np.linalg.solve(ata, A.T@Wd@y)
c1, c2 = float(sol[0]), float(sol[1]); se1, se2 = float(np.sqrt(np.diag(cov))[0]), float(np.sqrt(np.diag(cov))[1])
loo = []
for j in range(len(t)):
    m = np.ones(len(t), bool); m[j] = False
    Wj = np.diag(1/se[m]**2); Aj = A[m]
    sol_j = np.linalg.solve(Aj.T@Wj@Aj, Aj.T@Wj@y[m])
    loo.append(float(sol_j[0]))
log("M1: c1(10) = %+.4f +- %.4f  (c2 = %+.2f +- %.2f; LOO %s)"
    % (c1, se1, c2, se2, " ".join("%+.2f" % v for v in loo)))

# M3 adjudication
zp = abs(c1 - C1_PRED)/np.sqrt(se1**2 + E2_SE**2)
log("M3: |c1_meas - pred| z = %.2f (pred %+.4f)" % (zp, C1_PRED))
if abs(c1 - C1_PRED) <= 3*np.sqrt(se1**2 + E2_SE**2):
    branch = "(a) HOLDS: W3 decomposition confirmed at q=10; MC7 q=10 quadratic-selection recorded as extrapolation-bias-limited"
elif c1 <= 0 and abs(c1)/se1 >= 3:
    branch = "(b) REAL STRUCTURE: c1(10) <= 0 at >=3 SE vs pred +13.88 -> successor door W5 (exact c2 / higher-cumulant leg) registered"
else:
    branch = "(c) UNRESOLVED at this power (recorded)"
finish(0, "LANDED: %s" % branch, dict(meas=pts, c1=c1, se1=se1, c2=c2, se2=se2, loo=loo,
        z_parity=z2, z_pred=float(zp), pred=C1_PRED, branch=branch))
