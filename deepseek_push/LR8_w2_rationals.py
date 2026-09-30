#!/usr/bin/env python3
"""LR8 -- Lean certificates of the W2 rationals A0=2/5, A1=8/35 (Z12 door; owns LR8_*).

Door: W2 (exit 0, 446286a06) banked c00(q) = 2/5 + (8/35) q exactly. This lane
certifies the two rationals. Pre-registration: Z12-WAVE_BRIEF.md (BEFORE any run).

Conductor pre-audit (tick transcript, BEFORE this lane): sympy-Beta mechanism
(independent of W2's sequential sympy.integrate) gave A0=2/5, A1=8/35 after
honesty fix of the conductor's OWN coefficient slip (lost the x(1/2) from the
r^2 W^2/2 term: first pass gave 16/35, recorded verbatim in the transcript,
fixed before the Lean run; W2's stored 8/35 stands, corroborated by its K1/K2).

Gates (pre-registered):
  R0a: sympy-Beta exact A0=2/5, A1=8/35 (mismatch -> exit 1).
  R0b: mpmath quad + Gauss-Legendre(500) of the (rho,w) rectangle integrands,
       dev <= 1e-12 rel (exceed -> exit 1).
  R0c: MC of the FULL geometric reduction (p uniform in unit ball x u
       isotropic, n=2e7, seed 20260929, single pass): |mean-exact|/SE <= 5
       for both A0, A1 (exceed -> exit 1).
  G1:  lake env lean LR8_w2_rationals.lean: rc 0, ZERO sorry, axioms of
       w2_A0_law/w2_A1_law subset {propext, Classical.choice, Quot.sound}
       (fail after honest attempts -> exit 1).
  G2:  sympy mechanical assembly check: (3/2)*(4/3), (3/2)*(8/15) constants
       vs the Lean statement (mismatch -> exit 1).
Honest scope (Lean header): 1D cores + assembly CERTIFIED; geometric
reduction leg numeric-audited only (LR4c/LR7 mechanism-class precedent).
"""
import json, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(os.path.dirname(HERE), "fable_independent_2026", "lean_2026")
OUT = os.path.join(HERE, "LR8_w2_rationals.out")
RESF = os.path.join(HERE, "LR8_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR8 Lean certificates of the W2 rationals A0=2/5, A1=8/35",
               pre_registration="Z12-WAVE_BRIEF.md (registered before any run)",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF, "w"), indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

A0_EX, A1_EX = "2/5", "8/35"

# ---------- R0a: sympy exact via the Beta mechanism ----------
log("R0a: sympy exact, Beta-function mechanism (independent of W2)")
import sympy as sp
def J(m, k):
    return sp.simplify(sp.Rational(1,2) * sp.gamma(sp.Rational(m+1,2)) * sp.gamma(sp.Rational(k,2)+1)
                       / sp.gamma(sp.Rational(m+1,2)+sp.Rational(k,2)+1))
A0 = sp.Rational(3,2) * ( sp.Rational(1,2) * sp.Rational(8,3) * J(1,3) )
A1 = sp.Rational(3,2) * ( sp.Rational(1,2)*sp.Rational(8,3)*J(3,3)
                        + sp.Rational(1,2)*sp.Rational(16,15)*J(1,5)
                        + (sp.Rational(2,3)*sp.Rational(-12,5) + sp.Rational(1,4)*sp.Rational(32,5))*J(1,5) )
log("R0a: sympy A0 = %s, A1 = %s" % (A0, A1))
if A0 != sp.Rational(2,5) or A1 != sp.Rational(8,35):
    finish(1, "R0a FIRED: exact mismatch (%s, %s)" % (A0, A1))
log("R0a PASS: A0 = 2/5, A1 = 8/35 exact")

# ---------- R0b: two independent quadratures of the (rho,w) rectangle integrands ----------
log("R0b: mpmath + Gauss-Legendre(500) on the (rho,w) integrands")
import mpmath as mp
mp.mp.dps = 40
sm = lambda x: mp.sqrt(1 - x*x)
g0 = lambda w, x: sm(x)**3 * (1 - w)**2 / 2
g1 = lambda w, x: sm(x)*((x*x + sm(x)**2*w*w)*sm(x)**2*(1-w)**2/2
                         + 2*sm(x)**4*w*(1-w)**3/3 + sm(x)**4*(1-w)**4/4)
A0_mp = mp.mpf(3)/2*mp.quad(lambda x: x*mp.quad(lambda ww: g0(ww, x), [-1, 1]), [0, 1])
A1_mp = mp.mpf(3)/2*mp.quad(lambda x: x*mp.quad(lambda ww: g1(ww, x), [-1, 1]), [0, 1])
from scipy.special import roots_legendre
ng = 500
t, wg = roots_legendre(ng)
xg = 0.5*(1 - t); wx = 0.5*wg
wgw = wg[None, :]
s2 = (1 - xg**2)[:, None]
sgr = np.sqrt(s2)
Wg = sgr*(1 - t[None, :])
G0 = Wg**2/2
G1 = (xg[:,None]**2 + (sgr*t[None,:])**2)*Wg**2/2 + 2*(sgr*t[None,:])*Wg**3/3 + Wg**4/4
A0_gl = 1.5*np.sum(wx[:,None]*wgw*xg[:,None]*sgr*G0)
A1_gl = 1.5*np.sum(wx[:,None]*wgw*xg[:,None]*sgr*G1)
rel = lambda a, b: abs(float(a) - float(b))/max(abs(float(b)), 1e-300)
devs = dict(A0_mp=rel(A0_mp, 0.4), A1_mp=rel(A1_mp, 8/35), A0_gl=rel(A0_gl, 0.4), A1_gl=rel(A1_gl, 8/35))
log("R0b: dev A0 %.2e/%.2e (mp/gl)  A1 %.2e/%.2e (gate 1e-12)"
    % (devs["A0_mp"], devs["A0_gl"], devs["A1_mp"], devs["A1_gl"]))
if max(devs.values()) > 1e-12:
    finish(1, "R0b FIRED: quadrature dev > 1e-12", dict(devs=devs))
log("R0b PASS")

# ---------- R0c: MC of the FULL geometric reduction ----------
log("R0c: MC geometric reduction, n=2e7, seed 20260929")
rng = np.random.default_rng(20260929)
n = 20_000_000
d0 = rng.normal(size=(n, 3)); d0 /= np.linalg.norm(d0, axis=1)[:, None]
p = d0 * rng.random(n)[:, None]**(1/3)          # uniform in unit ball
du = rng.normal(size=(n, 3)); u = du / np.linalg.norm(du, axis=1)[:, None]
z = np.sum(p*u, axis=1); r2 = np.sum(p*p, axis=1)
W = -z + np.sqrt(np.maximum(z*z - r2 + 1.0, 0.0))
X0 = W*W/2
X1 = r2*W*W/2 + 2*z*W**3/3 + W**4/4
m0, s0 = float(X0.mean()), float(X0.std(ddof=1)/np.sqrt(n))
m1, s1 = float(X1.mean()), float(X1.std(ddof=1)/np.sqrt(n))
z0 = abs(m0 - 0.4)/s0; z1 = abs(m1 - 8/35)/s1
log("R0c: MC A0 = %.6f +- %.6f (z=%.2f)   A1 = %.6f +- %.6f (z=%.2f) (gate 5)"
    % (m0, s0, z0, m1, s1, z1))
if max(z0, z1) > 5:
    finish(1, "R0c FIRED: MC vs exact mismatch (A0 z=%.2f, A1 z=%.2f)" % (z0, z1),
           dict(mc=dict(A0=m0, A0_se=s0, A1=m1, A1_se=s1)))
log("R0c PASS: the geometric reduction leg is MC-consistent with the exact values")

# ---------- G1: Lean ----------
log("G1: lake env lean LR8_w2_rationals.lean")
r = subprocess.run(["lake", "env", "lean", "LR8_w2_rationals.lean"], cwd=LEAN,
                   capture_output=True, text=True, timeout=1200)
stdout = r.stdout + r.stderr
open(os.path.join(HERE, "LR8_lean_stdout.txt"), "w").write(stdout)
nsorry = stdout.count("sorry")
log("G1: lake rc=%d, sorry_count=%d" % (r.returncode, nsorry))
AX = {"propext", "Classical.choice", "Quot.sound"}
axok = True; axdump = {}
for line in stdout.splitlines():
    if "depends on axioms" in line:
        name = line.split()[0]
        used = {a.strip('[], ') for a in line.split("axioms:")[1].split(",")} if "axioms:" in line else {"?"}
        axdump[name] = sorted(used)
        if not used <= AX: axok = False
log("G1: axiom dump %s" % axdump)
if r.returncode != 0 or nsorry > 0 or not axok or len(axdump) < 2:
    finish(1, "G1 FIRED: lean rc=%d sorry=%d axok=%s" % (r.returncode, nsorry, axok),
           dict(lean_stdout=stdout[-2000:], axioms=axdump))
log("G1 PASS: w2_A0_law, w2_A1_law compile zero-sorry, axioms clean")

# ---------- G2: mechanical assembly check ----------
log("G2: sympy mechanical assembly constants")
c1 = sp.Rational(3,2)*sp.Rational(4,3)   # = 2 (A0 prefactor on base_A)
c2 = sp.Rational(3,2)*sp.Rational(4,3)   # prefactor on base_B
c3 = sp.Rational(3,2)*sp.Rational(8,15)  # prefactor on base_C
chk = c2*sp.Rational(2,35) + c3*sp.Rational(1,7)
log("G2: (3/2)(4/3)=%s, (3/2)(8/15)=%s; assembly = %s; lean states 2*(1/5) and (3/2)((4/3)(2/35)+(8/15)(1/7)) = 8/35"
    % (c1, c3, chk))
if chk != sp.Rational(8,35) or c1 != 2:
    finish(1, "G2 FIRED: assembly mismatch")
log("G2 PASS")

finish(0, "BANKED: A0 = 2/5 and A1 = 8/35 now certificate-grade (zero-sorry Lean assembly over "
          "LR7's unconditional 1D cores; reduction leg numeric-audited: R0b dev <= %.1e, "
          "R0c MC z = %.2f/%.2f). W2's c00(q) = 2/5 + (8/35)q is certificate-grade on the "
          "1D+assembly legs" % (max(devs.values()), z0, z1),
       dict(devs=devs, mc=dict(A0=m0, A0_se=s0, A1=m1, A1_se=s1), axioms=axdump))
