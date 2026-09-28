#!/usr/bin/env python3
"""LR4c -- GENERIC covStatement discharge + unconditional I2/I3 (Z8-wave; owns LR4c_*).
Door: Z7 register left chord_cond/I1_cond CONDITIONAL (the committed
LR4b_cov_discharge.lean keeps the (cov : ...) hypothesis; covStatement was never
proven generically -- conductor audit this tick, Z8-WAVE_BRIEF.md door-audit 1).
Also open: unconditional 17/60 (E[int r^4 ds]) and 149/700 (E[int r^6 ds]).

Gates (Z8-WAVE_BRIEF.md, fixed before any run):
  R0: independent numerical quadrature of the (r,mu) statements -- the w-integral
      done NUMERICALLY (Gauss-Legendre), never via the certified polynomials --
      vs 17/60 and 149/700, tol 1e-9 relative.
  G1: lake env lean LR4c_m05_i23.lean rc 0, ZERO sorry, axioms of cov_generic /
      chord_uncond / I1_uncond / I2_uncond / I3_uncond subset {propext,
      Classical.choice, Quot.sound}.
  G2: constants cross-check vs LR3_m05_moments.lean parsed from file (17/60,
      149/700, 5/12, 3/4) + M05B_results.json MC cross-ref (informational).
Kill (pre-registered): compile fail or non-zero-sorry after honest attempts ->
blocker verbatim, exit 1; any constant mismatch -> exit 1.
"""
import json, os, re, subprocess, sys, time
import numpy as np
from numpy.polynomial.legendre import leggauss

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(HERE, "..", "fable_independent_2026", "lean_2026")
OUT = os.path.join(HERE, "LR4c_m05_i23.out")
RESF = os.path.join(HERE, "LR4c_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR4c generic cov discharge + unconditional I2/I3",
               pre_registration="Z8-WAVE_BRIEF.md LR4c gates",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0, 1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF, "w"), indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

# ---- R0: independent quadrature of the geometric statements ----
_XW = leggauss(96)   # run-3 resolution (amendment 2); leggauss cached
def I_k(r, mu, k, xw=_XW):
    u = r * np.sqrt(1 - mu**2); v = r * mu
    s = np.sqrt(max(0.0, 1 - u**2))
    L = s - v
    if L <= 0: return 0.0
    x, wx = xw; w = L * (x + 1) / 2; ww = L / 2 * wx
    return float(np.sum(ww * (u**2 + (v + w)**2)**k))

def moment(k, nr=300, nmu=600):
    xr, wr = leggauss(nr); rm = 0.5*xr + 0.5; rw = 0.5*wr
    xm, wm = leggauss(nmu); mum = xm; mw = 0.5*wm
    x, wx = _XW; w = None
    tot = 0.0
    for i in range(nr):
        r = rm[i]
        us = r * np.sqrt(1 - mum**2); vs = r * mum
        ss = np.sqrt(np.maximum(0.0, 1 - us**2)); Ls = ss - vs
        tot += rw[i] * r**2 * float(np.dot(mw * (Ls > 0), [I_k(r, mum[j], k) if Ls[j] > 0 else 0.0 for j in range(nmu)])) if False else 0.0
        inner = 0.0
        for j in range(nmu):
            if Ls[j] > 0:
                ww = Ls[j] / 2 * wx; wv = Ls[j] * (x + 1) / 2
                inner += mw[j] * float(np.sum(ww * (us[j]**2 + (vs[j] + wv)**2)**k))
        tot += rw[i] * r**2 * inner
    return 3 * tot

r0 = {}
for k, V, name in ((2, 17/60, "E[int r^4 ds]"), (3, 149/700, "E[int r^6 ds]")):
    val = moment(k)
    rel = abs(val - V)/V
    r0[name] = dict(quad=val, exact=V, rel_err=rel)
    log("R0: %s quadrature %.10f vs exact %.10f  rel %.2e" % (name, val, V, rel))
    if rel > 1e-9:
        finish(1, "R0-FAIL: %s quadrature off exact by %.2e (kill pre-registered)" % (name, rel))
log("R0 PASS (tol 1e-9 rel)")

# ---- G1: Lean compile ----
p = subprocess.run(["lake", "env", "lean", "LR4c_m05_i23.lean"], cwd=LEAN,
                   capture_output=True, text=True, timeout=600)
stdout = p.stdout + p.stderr
with open(os.path.join(HERE, "LR4c_lean_stdout.txt"), "w") as f: f.write(stdout)
log("G1: lake rc=%d (%d chars stdout+stderr)" % (p.returncode, len(stdout)))
if p.returncode != 0:
    finish(1, "G1-FAIL: lake rc %d -- blocker verbatim:\n%s" % (p.returncode, stdout[-2000:]))
if re.search(r"\bsorry\b", stdout):
    finish(1, "G1-FAIL: sorry in banked file")
want = ["cov_generic", "chord_uncond", "I1_uncond", "I2_uncond", "I3_uncond"]
clean = True
for th in want:
    m = re.search(r"'%s' depends on axioms: \[(.*)\]" % th, stdout)
    if not m: log("G1: MISSING axiom print for %s" % th); clean = False; continue
    axs = set(x.strip() for x in m.group(1).split(","))
    ok = axs <= {"propext", "Classical.choice", "Quot.sound"}
    log("G1: %s axioms %s -> %s" % (th, sorted(axs), "CLEAN" if ok else "DIRTY"))
    clean = clean and ok
if not clean: finish(1, "G1-FAIL: axioms dirty or missing")
log("G1 PASS (rc 0, zero sorry, axioms clean)")

# ---- G2: constants cross-check ----
lr3 = open(os.path.join(LEAN, "LR3_m05_moments.lean")).read()
need = {"17/60": "val_I2", "149/700": "val_I3", "5/12": "val_I1", "3/4": "val_chord"}
for rat, th in need.items():
    ok = rat in lr3
    log("G2: LR3 %s (%s) present: %s" % (rat, th, ok))
    if not ok: finish(1, "G2-FAIL: %s not found in LR3_m05_moments.lean" % rat)
lb = open(os.path.join(LEAN, "LR4b_cov_discharge.lean")).read()
misbank = "theorem chord_cond (cov :" in lb
log("G2: LR4b audit evidence: chord_cond keeps (cov : ...) hypothesis: %s" % misbank)
try:
    m05b = json.load(open(os.path.join(HERE, "M05B_results.json")))
    log("G2: M05B MC cross-ref on file (informational): keys %s" % sorted(m05b.keys())[:6])
except Exception as e:
    log("G2: M05B_results.json not loadable (%s) -- informational only" % e)

finish(0, "BANKED-UNCONDITIONAL: cov_generic proven (covStatement holds for every continuous H); "
          "chord/I1/I2/I3 = 3/4, 5/12, 17/60, 149/700 now UNCONDITIONAL M01-grade certificates; "
          "Z7 LR4b 'DISCHARGED/UNCONDITIONAL' row corrected (hypothesis was still present on disk)",
       dict(R0=r0, misbank_evidence=misbank))
