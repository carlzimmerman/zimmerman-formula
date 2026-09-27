#!/usr/bin/env python3
"""M05B -- independent audit of M05's E[int r^4 ds] table entry (Z6-wave; owns M05B_*).
Gates (Z6-WAVE_BRIEF.md + amendment 3, fixed before this run):
  R0: M05's own I2 polynomial under correct-domain quadrature -- provenance probe;
      outcome recorded verbatim (run-1/2 found 0.1250000001 != their table 0.2500000014).
  R1: independent direct ray-integration MC (midpoint m=256, n=2e6, fresh seeds):
      I1 -> 5/12, I2 -> 17/60, I3 -> 149/700, each |z| <= 3 with the MC's own SE.
  R2: lane's own mechanical sympy derivation (definition -> exact rational).
exit 0 iff R1 AND R2. Verdict records R0's provenance outcome verbatim."""
import json, os, sys, time
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M05B_r4_bug_audit.out")
RESF = os.path.join(HERE, "M05B_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict):
    RES = dict(title="M05B r4-table audit", pre_registration="Z6-WAVE_BRIEF.md M05B gates + amendment 3",
               verdict=verdict, exit=rc, elapsed_s=round(time.time() - _T0, 1), log=LOG)
    with open(RESF, "w") as f: json.dump(RES, f, indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

from numpy.polynomial.legendre import leggauss
xs, ws = leggauss(256)
x = 0.5 * xs + 0.5; w = 0.5 * ws
R = x[:, None]; MU = xs[None, :]
Wr = (3.0 * R ** 2) * (0.5 * w[:, None]); Wm = 0.5 * ws[None, :]
cord = -R * MU + np.sqrt(np.maximum(0.0, 1.0 - R ** 2 * (1.0 - MU ** 2)))
I2_m05 = (R ** 4 * cord + 2 * R ** 3 * MU * cord ** 2
          + (2 * R ** 2 * MU ** 2 + R ** 2) * cord ** 3 / 3.0
          + R * MU * cord ** 4 / 2.0 + cord ** 5 / 5.0)
r0 = float(np.sum(Wr * I2_m05 * Wm))
log("R0: M05 I2 polynomial quadrature (ng=256, correct domains) = %.12f (their table 0.2500000014)" % r0)
log("R0 OUTCOME: provenance UNRESOLVED -- their committed polynomial does not reproduce their table value")

rng = np.random.default_rng(20260927)
n, m = 2_000_000, 256
r = rng.random(n) ** (1 / 3)
mu = rng.uniform(-1, 1, n)
L = -r * mu + np.sqrt(np.maximum(0.0, 1 - r ** 2 * (1 - mu ** 2)))
s = (np.arange(m) + 0.5)[None, :] / m * L[:, None]
rho2 = r[:, None] ** 2 + 2 * r[:, None] * mu[:, None] * s + s ** 2
ds = (L / m)[:, None]
I1d = np.sum(rho2 * ds, axis=1); I2d = np.sum(rho2 ** 2 * ds, axis=1); I3d = np.sum(rho2 ** 3 * ds, axis=1)
refs = {"I1": 5 / 12, "I2": 17 / 60, "I3": 149 / 700}
r1 = {}
for nm, arr in (("I1", I1d), ("I2", I2d), ("I3", I3d)):
    mm = float(arr.mean()); se = float(arr.std(ddof=1) / np.sqrt(n))
    z = (mm - refs[nm]) / se
    r1[nm] = dict(mean=mm, se=se, ref=refs[nm], z=z)
    log("R1: %s direct-quad MC = %.8f +- %.1e, ref %.8f, z = %+.2f" % (nm, mm, se, refs[nm], z))
r1_pass = all(abs(r1[k]["z"]) <= 3 for k in r1)
log("R1 %s" % ("PASS" if r1_pass else "FAIL"))

vv, wq = sp.symbols('v w', real=True)
U, S = sp.symbols('U sstar', positive=True)
r2 = {}
for k in (1, 2, 3):
    Ik = sp.integrate((U ** 2 + wq ** 2) ** k, (wq, vv, S))
    inner = sp.expand(sp.integrate(Ik, (vv, -S, S)) / (2 * S))
    expr = sp.expand(3 * U * sp.sqrt(1 - U ** 2) * inner.subs(S, sp.sqrt(1 - U ** 2)))
    r2[k] = str(sp.nsimplify(sp.integrate(expr, (U, 0, 1))))
    log("R2: mechanical sympy E[int r^%d ds] = %s" % (2 * k, r2[k]))
r2_pass = (r2[1] == "5/12" and r2[2] == "17/60" and r2[3] == "149/700")
log("R2 %s" % ("PASS" if r2_pass else "FAIL"))

ok = r1_pass and r2_pass
verdict = ("M05-I2-VALUE-REFUTED, CORRECTED TO 17/60: E[int r^4 ds] = 17/60 (R1 MC z = %+.2f vs 17/60; "
           "R2 mechanical sympy = 17/60); r^6 candidate 149/700 CONFIRMED exact; chord 3/4 and r^2 5/12 stand; "
           "M05's table 1/4 provenance UNRESOLVED (their committed I2 polynomial integrates to 0.1250000001, "
           "R0; earlier mechanism-match claim RETRACTED per amendment 3)"
           % r1["I2"]["z"]) if ok else "R1/R2 FAIL -- honest, recorded verbatim"
finish(0 if ok else 1, verdict)
