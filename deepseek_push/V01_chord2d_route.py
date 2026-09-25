#!/usr/bin/env python3
"""
V01 -- 2D CHORD-MOMENT 3/4: mathlib-gap ROUTE (V-WAVE_BRIEF.md, kills pre-registered)
2026-09-25.  Conductor-run lane.

Door: M01's single CONJECTURED item chordMomentVol = 3/4, blocked in Lean only
because its natural proof used a 2D change of variables.  This lane verifies the
1D-substitution + triangle-Fubini route:
  (1) odd part:  integral of r*mu over mu in [-1,1] is 0.
  (2) per-r substitution v = r*mu (1D):  r^2 * int_{-1}^{1} sqrt(1-r^2+r^2 mu^2) dmu
      = r * int_{-r}^{r} sqrt(1-r^2+v^2) dv   (r=0: both sides 0).
  (3) Fubini on the triangle T = {(r,v): 0<=r<=1, |v|<=r}:
      int_0^1 int_{-r}^{r} f dv dr = int_{-1}^{1} int_{|v|}^{1} f dr dv.
  (4) antiderivative: d/dr [-(1/3)(1-r^2+v^2)^{3/2}] = r*sqrt(1-r^2+v^2),
      so int_{|v|}^1 r sqrt(1-r^2+v^2) dr = (1-|v|^3)/3  and  I = 2*int_0^1 (1-v^3)/3 dv = 1/2.
  chordMomentVol = 3 * 1/2 * I = 3/4.  NO 2D change of variables anywhere.

Kills (pre-registered):
  K1 numeric machinery: direct 60-dps nested quadrature vs the triangle-chain
     quadrature agree <= 1e-30 abs; sympy exact on steps (2)-identity form,
     (4)-antiderivative and the final v-integral; MC 1e7 z <= 3 vs 0.75.
  K2 Lean cert: exit 0, zero sorry, axioms {propext, Classical.choice,
     Quot.sound}.  INCOMPLETE recorded honestly if the assembly does not close.
  K3 route/channel claim only.
"""
import json, math, sys
import numpy as np
from mpmath import mp, mpf, quad, sqrt as msqrt
import sympy as sp

mp.dps = 60
res = {"lane": "V01_chord2d_route", "prereg": "V-WAVE_BRIEF.md", "checks": {},
       "kill_events": []}

def chord_vol(r, mu):
    return r * mu + msqrt(1 - r**2 * (1 - mu**2))

# K1a: direct nested quadrature of the M01 def
direct = 3 * quad(lambda r: r**2 * (mpf(1)/2 * quad(lambda mu: chord_vol(r, mu), [-1, 1], maxdegree=14)), [0, 1], maxdegree=14)

# K1b: triangle chain:  I = int_{-1}^{1} (1-|v|^3)/3 dv ; total = 3*(1/2)*I
I_chain = quad(lambda v: (1 - abs(v)**3) / 3, [-1, 0, 1], maxdegree=14)
chain = 3 * (mpf(1)/2) * I_chain

res["direct_60dps"] = sp.N(str(direct), 25)
res["chain_60dps"] = sp.N(str(chain), 25)
res["checks"]["K1_direct_vs_chain_1e-30"] = bool(abs(direct - chain) <= mpf('1e-30')
    and abs(direct - mpf(3)/4) <= mpf('1e-30') and abs(chain - mpf(3)/4) <= mpf('1e-30'))
print("direct   = %s" % mp.nstr(direct, 30))
print("chain    = %s" % mp.nstr(chain, 30))
print("abs diff = %s" % mp.nstr(abs(direct - chain), 5))

# K1c: per-r substitution identity (step 2) at 40 dps on a grid
ok2 = True
for r in [mpf('0.1'), mpf('0.3'), mpf('0.5'), mpf('0.7'), mpf('0.9'), mpf('0.99')]:
    lhs = quad(lambda mu: msqrt(1 - r**2 + r**2 * mu**2), [-1, 1], maxdegree=12)
    rhs = (1/r) * quad(lambda v: msqrt(1 - r**2 + v**2), [-r, r], maxdegree=12)
    if abs(lhs - rhs) > mpf('1e-30'):
        ok2 = False
        print("step-2 identity FAILS at r=%s: %s vs %s" % (r, lhs, rhs))
res["checks"]["K1_step2_substitution_identity"] = ok2
print("step-2 substitution identity (r grid, 40dps):", ok2)

# K1d: triangle Fubini (step 3): direct double integral vs flipped iterated
f = lambda r, v: r * msqrt(1 - r**2 + v**2)
I_direct = quad(lambda r: quad(lambda v: f(r, v), [-r, r], maxdegree=12), [0, 1], maxdegree=12)
I_flip = quad(lambda v: quad(lambda rr: f(rr, v), [abs(v), 1], maxdegree=12), [-1, 0, 1], maxdegree=12)
res["checks"]["K1_triangle_fubini_1e-30"] = bool(abs(I_direct - I_flip) <= mpf('1e-30')
    and abs(I_direct - mpf(1)/2) <= mpf('1e-30') and abs(I_flip - mpf(1)/2) <= mpf('1e-30'))
res["I_direct"] = sp.N(str(I_direct), 25); res["I_flip"] = sp.N(str(I_flip), 25)
print("I_direct = %s   I_flip = %s" % (mp.nstr(I_direct, 30), mp.nstr(I_flip, 30)))

# K1e: sympy exact pieces
r, v, mu = sp.symbols('r v mu', real=True)
anti = -(sp.Rational(1,3)) * (1 - r**2 + v**2)**sp.Rational(3,2)
d = sp.simplify(sp.diff(anti, r) - r * sp.sqrt(1 - r**2 + v**2))
res["checks"]["K1_sympy_antiderivative_exact"] = bool(d == 0)
final = sp.integrate((1 - sp.Abs(v)**3) / 3, (v, -1, 1))
res["checks"]["K1_sympy_final_v_integral_exact"] = bool(sp.simplify(final - sp.Rational(1,2)) == 0)
res["sympy_final"] = str(final)
print("sympy: antiderivative residual =", d, " ; final v-integral =", final)

# K1f: MC 1e7 vs 0.75
rng = np.random.default_rng(20260925)
n = 10_000_000
rr = rng.random(n); mm = rng.random(n) * 2 - 1
est = 3.0 * np.mean(rr**2 * 0.5 * (rr*mm + np.sqrt(1 - rr**2 * (1 - mm**2)))) * 2.0
se = float(np.std(rr**2 * 0.5 * (rr*mm + np.sqrt(1 - rr**2*(1-mm**2)))) / math.sqrt(n)) * 6.0
z = (est - 0.75) / se
res["mc"] = dict(n=n, seed=20260925, estimate=float(est), se=float(se), z=float(z))
res["checks"]["K1_mc_z_le_3"] = bool(abs(z) <= 3.0)
print("MC 1e7: estimate = %.6f +- %.6f  z vs 0.75 = %+.2f" % (est, se, z))

res["ALL_PASSED"] = all(v for v in res["checks"].values())
out = "V01_chord2d_route_results.json"
json.dump(res, open(out, "w"), indent=1, default=str)
print("WROTE", out)
print("ALL V01 NUMERIC CHECKS PASSED" if res["ALL_PASSED"] else "V01 NUMERIC KILL/FAIL")
sys.exit(0 if res["ALL_PASSED"] else 1)
