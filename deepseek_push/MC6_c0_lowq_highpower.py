#!/usr/bin/env python3
"""MC6 -- c0 low-q parity at 4x power (Z9-wave; owns MC6_*).
Door: MC5 K2 stored c0(0)-extrapolations vs the MC4-banked line a+bq sit at
z = 1.51 (q=0), 1.83 (q=1) (others <= 1.32) at n=2e6 x 4 reps -- inside
noise at that power; Z8 ops note: resolvable only at ~4x power.
Budget (fixed before any run): q in {0,1,3,6,10}; tau0 in {1e-2,3e-3,1e-3,
3e-4}; n=8e6 x 4 reps/point, seeds 6101.., single pass, no re-tuning.
Engines loaded-not-transcribed: J02 simulate (volume); MC4 line parsed from
MC4_results.json verdict string; MC5 stored points for P0.
KILLS pre-registered in Z9-WAVE_BRIEF.md:
  P0: fresh pooled c0_extrap per q vs MC5 stored pooled:
      |diff| <= 3*sqrt(se_fresh^2 + se_stored^2). FIRED -> exit 1.
  K1: |c0_extrap - (a+bq)| <= 3*SE_extrap at every q. FIRED at any q ->
      PRE-DECLARED diagnostic BEFORE any kill verdict: quadratic-in-tau0 fit
      of c0(tau0); if the quadratic intercept clears 3 SE ->
      EXTRAPOLATION-MODEL-LIMITED (amended estimator recorded, house rule 3;
      amended intercept banks, exit 0); if still > 3 SE -> MC4 line REFUTED
      as thin-window limit, exit 1.
Exit 0 iff P0 and (K1 clean or diagnostic-resolved).
"""
import json, os, re, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate

OUT = os.path.join(HERE, "MC6_c0_lowq_highpower.out")
RESF = os.path.join(HERE, "MC6_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="MC6 c0 low-q parity at 4x power",
               pre_registration="Z9-WAVE_BRIEF.md MC6 gates",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF,"w"), indent=1, default=str)
    with open(OUT,"a") as f: f.write("\n".join(LOG)+"\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

QS = [0.0, 1.0, 3.0, 6.0, 10.0]
TAUS = [1e-2, 3e-3, 1e-3, 3e-4]
N, REPS = 8_000_000, 4

m5 = json.load(open(os.path.join(HERE, "MC5_results.json")))["c0"]
m = re.search(r"c0 = ([0-9.]+) \+ ([0-9.]+) q",
              json.load(open(os.path.join(HERE, "MC4_results.json")))["verdict"])
a4, b4 = float(m.group(1)), float(m.group(2))
log("P0 setup: loaded MC4 line a=%.6f b=%.6f; MC5 stored 5 points" % (a4, b4))

# ---- P0 parity vs MC5 stored pooled intercepts ----
def linfit_extrap(pts):
    ts = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    ws = 1/np.array([p[2] for p in pts])**2
    W = np.diag(ws); Am = np.vstack([np.ones_like(ts), ts]).T
    ata = Am.T@W@Am; aty = Am.T@W@ys
    sol = np.linalg.solve(ata, aty); cov = np.linalg.inv(ata)
    return float(sol[0]), float(sol[1]), float(np.sqrt(cov[0,0]))

p0_fired = []
for q in QS:
    stored = m5[str(q) if str(q) in m5 else ("%g" % q)]
    zc = abs(stored["c0_extrap"] - (a4 + b4*q))/stored["se"]
    if zc > 3: p0_fired.append((q, "stored-vs-line pre-check z=%.2f" % zc))
log("P0 stored sanity: MC5 stored intercepts vs line z max = %.2f (informational)"
    % max(abs(m5[str(q)]["c0_extrap"] - (a4+b4*q))/m5[str(q)]["se"] for q in QS))

# ---- fresh runs at 4x power ----
meas = {}; seed = 6101
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
    c0_0, slope, se_ex = linfit_extrap(pts)
    meas[q] = dict(c0_extrap=c0_0, slope=slope, se=se_ex,
                   points=[(p[0], p[1], p[2]) for p in pts])
    log("run: q=%g: c0(0)=%.6f+-%.6f (slope %.3f)" % (q, c0_0, se_ex, slope))
    # P0 cell parity vs MC5 stored pooled intercept
    stored = m5[str(q) if str(q) in m5 else ("%g" % q)]
    d = abs(c0_0 - stored["c0_extrap"])
    comb = 3*np.sqrt(se_ex**2 + stored["se"]**2)
    ok = d <= comb
    meas[q]["p0_z"] = float(d/np.sqrt(se_ex**2 + stored["se"]**2))
    log("P0: q=%g: fresh-vs-MC5-stored diff=%.6f tol=%.6f %s"
        % (q, d, comb, "KILL" if not ok else "ok"))
    if not ok: p0_fired.append((q, "fresh-vs-stored"))
if p0_fired:
    finish(1, "P0 FIRED at %s (kill pre-registered)" % p0_fired, extra=dict(meas=meas))
log("P0 PASS (fresh 4x-power intercepts reproduce MC5 stored within combined SE)")

# ---- K1 line parity, with the pre-declared quadratic diagnostic ----
k1_fired = []; diag_used = []
for q in QS:
    unb = a4 + b4*q
    z = abs(meas[q]["c0_extrap"] - unb)/meas[q]["se"]
    meas[q]["z_line"] = float(z)
    log("K1: q=%g: c0(0)=%.6f+-%.6f vs a+bq %.6f, z=%.2f %s"
        % (q, meas[q]["c0_extrap"], meas[q]["se"], unb, z, "FIRE" if z > 3 else "ok"))
    if z > 3: k1_fired.append(q)
if k1_fired:
    for q in k1_fired:
        ts = np.array([p[0] for p in meas[q]["points"]])
        ys = np.array([p[1] for p in meas[q]["points"]])
        ws = 1/np.array([p[2] for p in meas[q]["points"]])**2
        W = np.diag(ws); Am = np.vstack([np.ones_like(ts), ts, ts**2]).T
        ata = Am.T@W@Am; aty = Am.T@W@ys
        sol = np.linalg.solve(ata, aty); cov = np.linalg.inv(ata)
        c0q, s1, s2 = sol; se_q = float(np.sqrt(cov[0,0]))
        unb = a4 + b4*q
        zq = abs(c0q - unb)/se_q
        meas[q]["quad_diag"] = dict(c0_quad=float(c0q), se=float(se_q),
                                    tau_coef=float(s1), tau2_coef=float(s2), z=float(zq))
        log("DIAG: q=%g: quadratic intercept %.6f+-%.6f vs line %.6f, z=%.2f"
            % (q, c0q, se_q, unb, zq))
        if zq <= 3:
            diag_used.append(q)
            log("DIAG: q=%g: EXTRAPOLATION-MODEL-LIMITED (quadratic resolves; amended "
                "intercept banks, estimator change recorded per house rule 3)" % q)
        else:
            finish(1, "K1 FIRED at q=%s and quadratic diagnostic does NOT resolve: "
                   "MC4 line REFUTED as thin-window limit (honest FAIL)" % k1_fired,
                   extra=dict(meas=meas))
    finish(0, "EXTRAPOLATION-MODEL-LIMITED at q=%s: linear-in-tau0 intercept z>3 at 4x "
              "power but the pre-declared quadratic intercept clears 3 SE -- MC4 line "
              "survives as the tau0->0 limit; amended estimator recorded (house rule 3)",
           extra=dict(meas=meas, diag_resolved=diag_used))
log("K1 no kill (c0(0) parity with the MC4 line at 4x power, all q)")
finish(0, "BANKED: c0 thin-window limit = MC4 line a+bq confirmed at 4x power "
          "(max z %.2f); MC5 low-q tension was noise" % max(meas[q]["z_line"] for q in QS),
       extra=dict(meas=meas))
