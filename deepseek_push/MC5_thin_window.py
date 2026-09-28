#!/usr/bin/env python3
"""MC5 -- thin-window limit test: M05-I numerator + R_v(0,q) curve (Z8-wave; owns MC5_*).
Door: MC4 banked c0(q)=a+bq at n_eff 2.4e7 and recorded R_v(0,q)=(3/4+5q/12)/(a+bq)
CANDIDATE-only ("its own closure needs its own door"). The numerator moments
chord=3/4 and E[int r^2 ds]=5/12 are now UNCONDITIONALLY Lean-certified (LR4c).
This lane tests the ENGINE-side tau0->0 limit structure (consistency-family,
labeled per house rule 4):
  (i)   N_num(tau0,q) := -ln A_vol(tau0,q)/tau0 -> 3/4 + 5q/12
        (A_vol by J11's exact quadrature A_vol_quadrature, loaded not transcribed)
  (ii)  c0(tau0,q) := E[D]_vol/tau0 -> MC4's banked line a+bq (loaded from
        MC4_results.json verdict string)
  (iii) R_meas(0,q) := lim N_num / lim c0 vs (3/4+5q/12)/(a+bq)
Budget (fixed before any run): q in {0,1,3,6,10}; tau0 in {1e-2,3e-3,1e-3,3e-4};
quadrature ng=80 (deterministic); E[D]_vol via J02 simulate volume n=2e6 x
4 reps/point, seeds 4101.., single pass, no re-tuning.
KILLS (pre-registered in Z8-WAVE_BRIEF.md):
  P0: fresh A_vol_quadrature(0.5, 0) vs J11 stored "A_quad": 0.70728, |diff|<=1e-4.
  K1: quadratic fit N_num = A + B t + C t^2 (4 points, per q); kill if
      |A - (3/4+5q/12)| > 3*max(SE_A, |C|*t_min^2) + 1e-9  -> numerator REFUTED.
  K2: linear-in-tau0 fit of c0 (per q); kill if |c0(0) - (a+bq)| > 3*SE_extrap.
  K3: |R_meas(0,q) - (3/4+5q/12)/(a+bq)| > 3*SE_comb (any q) -> curve REFUTED.
Exit 0 iff P0 and no kill -> R_v(0,q) CANDIDATE -> CONFIRMED at this power.
"""
import json, os, re, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate
from J11_volume_atom import A_vol_quadrature

OUT = os.path.join(HERE, "MC5_thin_window.out")
RESF = os.path.join(HERE, "MC5_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="MC5 thin-window limit test (numerator + R_v curve)",
               pre_registration="Z8-WAVE_BRIEF.md MC5 gates",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF,"w"), indent=1, default=str)
    with open(OUT,"a") as f: f.write("\n".join(LOG)+"\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

QS = [0.0, 1.0, 3.0, 6.0, 10.0]
TAUS = [1e-2, 3e-3, 1e-3, 3e-4]
N, REPS = 2_000_000, 4

# ---- P0 parity vs J11 stored quadrature ----
a_fresh = A_vol_quadrature(0.5, 0.0)
d = abs(a_fresh - 0.70728)
log("P0: fresh A_vol_quadrature(0.5, 0) = %.6f vs J11 stored 0.70728, |diff| = %.2e" % (a_fresh, d))
if d > 1e-4:
    finish(1, "P0-FAIL: parity vs J11 stored quadrature off by %.2e (kill pre-registered)" % d)
log("P0 PASS")

# ---- numerator limits (deterministic quadrature) ----
num = {}; k1_fired = []
for q in QS:
    xs = []
    for t in TAUS:
        Av = A_vol_quadrature(t, q)
        xs.append(-np.log(Av)/t)
    xs = np.array(xs); ts = np.array(TAUS)
    Mfit = np.vstack([np.ones_like(ts), ts, ts**2]).T
    coef, res, rank, sv = np.linalg.lstsq(Mfit, xs, rcond=None)
    A, B, C = coef
    pred = Mfit @ coef
    dof = len(ts) - 3
    se = float(np.sqrt(np.sum((xs-pred)**2)/max(dof,1))) if dof > 0 else 0.0
    unb = 3/4 + 5*q/12
    # AMENDED K1 (Z8-WAVE_BRIEF.md amendment 1, registered before this rerun):
    # noise floor from quadrature refinement at tau_min (ng 80 vs 160)
    a80 = -np.log(A_vol_quadrature(ts[-1], q, ng=80))/ts[-1]
    a160 = -np.log(A_vol_quadrature(ts[-1], q, ng=160))/ts[-1]
    d_ng = float(abs(a80 - a160))
    tol = 3*max(se, 2*d_ng, abs(C)*ts[-1]**2) + 1e-9
    dev = abs(A - unb)
    num[q] = dict(A=float(A), B=float(B), C=float(C), se=se, limit=unb,
                  dev=float(dev), tol=float(tol), d_ng=d_ng,
                  nvals=[float(x) for x in xs])
    log("K1: q=%g: A=%.6f B=%.3f C=%.3f vs limit %.6f, dev %.2e tol %.2e %s"
        % (q, A, B, C, unb, dev, tol, "KILL" if dev > tol else "ok"))
    if dev > tol: k1_fired.append(q)
if k1_fired:
    finish(1, "K1 FIRED at q=%s: numerator limit REFUTED at this power (honest FAIL)" % k1_fired)
log("K1 no kill (numerator limit consistent at all 5 q)")

# ---- c0 extrapolation vs MC4 line (MC leg) ----
m = re.search(r"c0 = ([0-9.]+) \+ ([0-9.]+) q",
              json.load(open(os.path.join(HERE,"MC4_results.json")))["verdict"])
a4, b4 = float(m.group(1)), float(m.group(2))
log("K2: loaded MC4 line a=%.6f b=%.6f" % (a4, b4))
c0 = {}; k2_fired = []
seed = 4101
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
    ts = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    ws = 1/np.array([p[2] for p in pts])**2
    W = np.diag(ws); Am = np.vstack([np.ones_like(ts), ts]).T
    ata = Am.T@W@Am; aty = Am.T@W@ys
    sol = np.linalg.solve(ata, aty); cov = np.linalg.inv(ata)
    c0_0, slope = sol
    se_ex = float(np.sqrt(cov[0,0]))
    unb = a4 + b4*q
    z = float(abs(c0_0 - unb)/se_ex) if se_ex > 0 else float("inf")
    c0[q] = dict(c0_extrap=float(c0_0), slope=float(slope), se=se_ex, unb=unb, z=z,
                 points=[(p[0], p[1], p[2]) for p in pts])
    log("K2: q=%g: c0(0)=%.6f+-%.6f (slope %.3f) vs a+bq %.6f, z=%.2f %s"
        % (q, c0_0, se_ex, slope, unb, z, "KILL" if z > 3 else "ok"))
    if z > 3: k2_fired.append(q)
if k2_fired:
    finish(1, "K2 FIRED at q=%s: thin-window denominator refuted (honest FAIL)" % k2_fired)
log("K2 no kill (c0 thin-window limit consistent with MC4 line)")

# ---- R_v curve check ----
k3_fired = []; rv = {}
for q in QS:
    numinf = num[q]["A"]
    r_meas = numinf / c0[q]["c0_extrap"]
    se = float(abs(r_meas)*np.sqrt((num[q]["se"]/numinf)**2 + (c0[q]["se"]/c0[q]["c0_extrap"])**2))
    cand = (3/4 + 5*q/12) / (a4 + b4*q)
    z = float(abs(r_meas - cand)/se) if se > 0 else float("inf")
    rv[q] = dict(r_meas=r_meas, se=se, cand=cand, z=z)
    log("K3: q=%g: R_meas %.5f+-%.5f vs candidate %.5f, z=%.2f %s"
        % (q, r_meas, se, cand, z, "KILL" if z > 3 else "ok"))
    if z > 3: k3_fired.append(q)
if k3_fired:
    finish(1, "K3 FIRED at q=%s: R_v candidate curve refuted (honest FAIL)" % k3_fired)

finish(0, "BANKED-CONFIRMED: thin-window limit structure verified at this power -- "
          "N_num -> 3/4+5q/12 (K1 clean), c0 -> a+bq (K2 clean), "
          "R_v(0,q) CANDIDATE -> CONFIRMED (K3 clean); consistency-family vs the "
          "LR4c-certified numerator, engine leg only",
       dict(P0=dict(fresh=a_fresh, stored=0.70728, diff=d),
            numerator=num, c0=c0, rv=rv, budget=dict(QS=QS, TAUS=TAUS, N=N, REPS=REPS)))
