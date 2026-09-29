#!/usr/bin/env python3
"""MC7 -- c00(q) thin-window determination (Z9 successor door; owns MC7_*).
Door: MC6 (exit 1, honest) refuted the MC4 line c0(q)=a+bq as the tau0->0
thin-window limit at q in {3,6} (z=4.75/7.19) with a quadratic diagnostic
that did not resolve. This lane decides, at independent seeds and a 2x denser
tau0 grid, with an extrapolation model SELECTED BY MEASURED SE, between:
  (a) MC6's fire was extrapolation-model-limited -> MC4 line restored as the
      thin-window limit (MC5 R_v CONFIRMED status restored, correction row);
  (b) the refutation stands -> c00(q) is a NEW structure, R_v(0,q) gets its
      denominator from c00(q) directly.
Budget (fixed before any run, Z9-WAVE_BRIEF.md MC7 door): q in {0,1,3,6,10};
tau0 grid 8 values {1e-2,6e-3,4e-3,2e-3,1e-3,6e-4,4e-4,2e-4}; n=4e6 x 6
reps/cell, seeds 7101.., single pass, no re-tuning.
KILLS pre-registered:
  P0: fresh pooled c0 at tau0=1e-3 vs MC4 stored pooled:
      |diff| <= 3*sqrt(se_fresh^2+se_stored^2). FIRED -> exit 1.
  M1: weighted linear + quadratic fits of c0(tau0), 8 points, both
      intercepts + SEs recorded.
  M2: model selection by |c2|/se(c2) > 3 -> quadratic; else linear.
  M3: selected intercept vs MC4 line: any q |z|>3 -> refutation CONFIRMED
      (exit 0); all q within 3 SE -> line restored (exit 0).
  M4: R_v(0,q) = (3/4+5q/12)/c00(q) re-adjudicated vs the CANDIDATE curve;
      recorded either way.
Exit 0 iff P0 passes and M1-M4 complete; exit 1 only on P0 fire or
execution failure.
"""
import json, os, re, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate

OUT = os.path.join(HERE, "MC7_c00_determination.out")
RESF = os.path.join(HERE, "MC7_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="MC7 c00(q) thin-window determination",
               pre_registration="Z9-WAVE_BRIEF.md MC7 door",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF,"w"), indent=1, default=str)
    with open(OUT,"a") as f: f.write("\n".join(LOG)+"\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

QS = [0.0, 1.0, 3.0, 6.0, 10.0]
TAUS = [1e-2, 6e-3, 4e-3, 2e-3, 1e-3, 6e-4, 4e-4, 2e-4]
N, REPS = 4_000_000, 6

m4 = json.load(open(os.path.join(HERE, "MC4_results.json")))
m = re.search(r"c0 = ([0-9.]+) \+ ([0-9.]+) q", m4["verdict"])
a4, b4 = float(m.group(1)), float(m.group(2))
line4 = {q: a4 + b4*q for q in QS}
log("P0 setup: MC4 line a=%.6f b=%.6f" % (a4, b4))

def wfit(ts, ys, ses, deg):
    ts = np.array(ts); ys = np.array(ys); ws = 1/np.array(ses)**2
    W = np.diag(ws)
    A = np.vstack([ts**k for k in range(deg+1)]).T
    ata = A.T@W@A; aty = A.T@W@ys
    sol = np.linalg.solve(ata, aty); cov = np.linalg.inv(ata)
    return sol, cov

meas = {}; seed = 7101
for q in QS:
    pts = []
    for t in TAUS:
        cs = []
        for rep in range(REPS):
            r = simulate(N, t, q, "volume", seed=seed); seed += 1
            D = np.asarray(r["D"])
            cs.append(float(D.mean())/t)
            del r, D
        pts.append((t, float(np.mean(cs)), float(np.std(cs, ddof=1)/np.sqrt(len(cs)))))
    meas[q] = dict(points=[(p[0], p[1], p[2]) for p in pts])
    log("run: q=%g done (8 tau0 x 6 reps)" % q)

# P0: fresh pooled c0 at tau0=1e-3 vs MC4 stored pooled
m4p = m4["meas"][str(0.0) if "0.0" in m4["meas"] else "0"]
stored_1e3 = None
for k in ("0.0", "0"):
    if k in m4["meas"]:
        stored_1e3 = m4["meas"][k]["pooled_c0"]; stored_se = m4["meas"][k]["rep_se"]
        break
fresh_1e3 = [p for p in meas[0.0]["points"] if p[0] == 1e-3][0]
comb = np.sqrt(fresh_1e3[2]**2 + stored_se**2)
z0 = abs(fresh_1e3[1] - stored_1e3)/comb
log("P0: tau0=1e-3 q=0: fresh %.6f+-%.6f vs MC4 stored %.6f+-%.6f, z=%.2f"
    % (fresh_1e3[1], fresh_1e3[2], stored_1e3, stored_se, z0))
if z0 > 3:
    finish(1, "P0 FIRED: fresh c0(tau0=1e-3) vs MC4 stored z=%.2f > 3 (kill pre-registered)" % z0,
           extra=dict(meas=meas))
log("P0 PASS")

# M1/M2/M3
m3_fired = []; sel = {}
for q in QS:
    ts = [p[0] for p in meas[q]["points"]]
    ys = [p[1] for p in meas[q]["points"]]
    ses = [p[2] for p in meas[q]["points"]]
    sol1, cov1 = wfit(ts, ys, ses, 1)
    sol2, cov2 = wfit(ts, ys, ses, 2)
    c2, se_c2 = float(sol2[2]), float(np.sqrt(cov2[2, 2]))
    zq2 = abs(c2)/se_c2 if se_c2 > 0 else float("inf")
    use_quad = zq2 > 3
    c00 = float(sol2[0]) if use_quad else float(sol1[0])
    se00 = float(np.sqrt(cov2[0, 0])) if use_quad else float(np.sqrt(cov1[0, 0]))
    z_line = abs(c00 - line4[q])/se00
    sel[q] = dict(model="quadratic" if use_quad else "linear", z_c2=float(zq2),
                  c2=c2, c00=c00, se00=se00, z_line=float(z_line),
                  lin_int=float(sol1[0]), quad_int=float(sol2[0]))
    log("M1/M2: q=%g: c2=%.3e+-%.1e (z=%.2f) -> %s; c00=%.6f+-%.6f vs line %.6f, z=%.2f %s"
        % (q, c2, se_c2, zq2, sel[q]["model"], c00, se00, line4[q], z_line,
           "FIRE" if z_line > 3 else "ok"))
    if z_line > 3: m3_fired.append(q)

# M4: R_v(0,q) re-adjudication
rv = {}
for q in QS:
    num = 3/4 + 5*q/12
    rv_meas = num/sel[q]["c00"]
    cand = num/line4[q]
    rv[q] = dict(rv_meas=float(rv_meas), candidate=float(cand),
                 rel_dev=float(abs(rv_meas-cand)/cand))
    log("M4: q=%g: R_v meas %.6f vs candidate %.6f (rel dev %.2e)"
        % (q, rv_meas, cand, rv[q]["rel_dev"]))

if m3_fired:
    finish(0, "RESULT: MC6 refutation CONFIRMED at independent seeds and 2x denser grid "
              "(c00(q) deviates from the MC4 line at q=%s; MC4 line stays a tau0=1e-3 "
              "object; R_v(0,q) denominator must come from c00(q) — MC5 CONFIRMED "
              "status stays DOWNGRADED)" % m3_fired,
           extra=dict(meas=meas, sel=sel, rv=rv))
finish(0, "RESULT: MC6 fire was extrapolation-model-limited — c00(q) = MC4 line a+bq "
          "restored as the thin-window limit at 2x denser grid + independent seeds "
          "(max z %.2f); MC5 R_v(0,q) CONFIRMED status RESTORED (append-only correction "
          "row follows in the register)" % max(sel[q]["z_line"] for q in QS),
       extra=dict(meas=meas, sel=sel, rv=rv))
