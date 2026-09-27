#!/usr/bin/env python3
"""MC1 -- c0(q) linearity decision (Z6-wave; owns MC1_*).
Door: M05_FIRST_FLIGHT_MOMENTS.md "the remaining open piece is c0(q) itself -- if
c0(q) is also linear (c0 = a + bq), the entire thin window is a rational curve in q."
Engine: J02_moment_hierarchy.simulate (loaded, never transcribed). Budget fixed
BEFORE any run (house rule 3): q in {0,1,3,6,10}, tau0=1e-3, n=6e6 per point,
seeds 901..905, single pass, no re-tuning.
Gates (Z6-WAVE_BRIEF.md, fixed before any run):
  P0: parse M05_geometric_anchors.out stored c0 at q in {0,3,10}; fresh |z| <= 3 each.
  M1: weighted LS fit a+bq on {0,1,3}; PREDICT {6,10}. Any |z_pred| > 3 ->
      c0-NOT-LINEAR (kill, honest). Else CONSISTENT-LINEAR (with honest MDE:
      smallest per-point deviation detectable at 3 sigma, reported, NOT banked as
      exact linearity beyond that power).
exit 0 iff P0 pass AND no kill fired."""
import json, os, re, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from J02_moment_hierarchy import simulate

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "MC1_c0_linearity.out")
RESF = os.path.join(HERE, "MC1_results.json")
_T0 = time.time()
LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="MC1 c0(q) linearity", pre_registration="Z6-WAVE_BRIEF.md MC1 gates",
               verdict=verdict, exit=rc, elapsed_s=round(time.time() - _T0, 1), log=LOG)
    if extra: RES.update(extra)
    with open(RESF, "w") as f: json.dump(RES, f, indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

QS = [0.0, 1.0, 3.0, 6.0, 10.0]
N, TAU0 = 6_000_000, 1e-3

# ---- P0: parity vs M05 stored ----
txt = open(os.path.join(HERE, "M05_geometric_anchors.out")).read()
m05 = {}
for q in ("0", "3", "10"):
    mm = re.search(r"c0_q%s[^}]*?['\"]c['\"]:\s*([0-9.]+)[^}]*?['\"]s['\"]:\s*([0-9.]+)" % q, txt)
    if mm: m05[float(q)] = (float(mm.group(1)), float(mm.group(2)))
log("P0: parsed M05 stored c0: %s" % m05)
if len(m05) < 3:
    finish(1, "P0-FAIL: could not parse M05 stored c0 from M05_geometric_anchors.out")

meas = {}
for i, q in enumerate(QS):
    r = simulate(N, TAU0, q, "volume", seed=901 + i)
    D = np.asarray(r["D"])
    c = float(D.mean()) / TAU0; s = float(D.std(ddof=1) / np.sqrt(len(D))) / TAU0
    meas[q] = (c, s)
    del r, D
    log("M1: q=%g: c0 = %.5f +- %.5f" % (q, c, s))
p0 = []
for q, (c0, s0) in m05.items():
    if q in meas:
        z = (meas[q][0] - c0) / np.sqrt(meas[q][1] ** 2 + s0 ** 2)
        p0.append(abs(z) <= 3)
        log("P0: q=%g fresh vs stored z = %+.2f" % (q, z))
p0_pass = all(p0) and len(p0) >= 2
log("P0 %s" % ("PASS" if p0_pass else "FAIL"))

# ---- M1: weighted LS on {0,1,3}, predict {6,10} ----
fit_q = [0.0, 1.0, 3.0]
A = np.array([[1.0, q] for q in fit_q]); y = np.array([meas[q][0] for q in fit_q])
w = np.array([1.0 / meas[q][1] ** 2 for q in fit_q])
W = np.diag(w)
ata = A.T @ W @ A; aty = A.T @ W @ y
a, b = np.linalg.solve(ata, aty)
cov = np.linalg.inv(ata)
log("M1: fit c0(q) = %.5f + %.5f q (b/sigma_b = %.1f)" % (a, b, abs(b) / np.sqrt(cov[1, 1])))
preds = {}
for q in (6.0, 10.0):
    c0, s0 = meas[q]
    z = ((a + b * q) - c0) / s0
    preds[q] = z
    log("M1: predict q=%g: pred %.5f vs meas %.5f +- %.5f, z = %+.2f" % (q, a + b * q, c0, s0, z))
killed = any(abs(z) > 3 for z in preds.values())
mde = {q: 3 * s0 for q, (c0, s0) in meas.items()}
if killed:
    finish(1, "c0-NOT-LINEAR (kill fired: |z_pred| > 3; M05-I thin window stays per-q MC)", dict(meas=meas, fit=dict(a=a, b=b), preds=preds, mde_3sigma=mde))
if not p0_pass:
    finish(1, "P0-FAIL (parity vs M05 stored c0 broken; no linearity claim)", dict(meas=meas))
finish(0, "CONSISTENT-LINEAR at registered power (no kill fired; MDE 3-sigma per point reported; exact-linearity banked only at this power)", dict(meas=meas, fit=dict(a=float(a), b=float(b)), preds={str(k): v for k, v in preds.items()}, mde_3sigma=mde))
