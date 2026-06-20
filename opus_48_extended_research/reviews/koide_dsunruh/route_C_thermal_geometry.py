#!/usr/bin/env python3
"""
ROUTE C -- dS-Unruh THERMAL-SPECTRUM route to Koide Q=2/3 (key dsunruh_thermal_spectrum).

Question: does an EQUAL-WEIGHT (democratic) dS-Unruh thermal occupation of three
family states naturally put the sqrt-mass vector at the Koide angle cos^2 theta = 3/4
(r = sqrt(2), theta=45deg)?  Or is r FREE?

BOTH-WAYS + QUARANTINE:
  - A "derivation" is VALID only if (1) FORCED (does not input 2/3 or r=sqrt(2) by hand
    or by a re-labeling), AND (2) passes the CROSS-FERMION falsification (must explain
    why charged leptons obey Koide and quarks/neutrinos do NOT).
  - We never assert a0/Z/kappa derived; Q=2/3 must not be smuggled.

This script establishes the EXACT geometry (Foot/Koide), the circulant parametrization,
the Q = 1/3 + r^2/6 identity, and then tests each candidate dS-Unruh THERMAL amplitude
that could FORCE r=sqrt(2): (a) 2-dof quadrature sqrt(2); (b) Bose thermal-occupation
amplitude; (c) sqrt(2/Z) geometry; (d) fluctuation-dissipation amplitude.
"""

import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("ROUTE C: dS-Unruh thermal-spectrum -> Koide angle  (FORCED r=sqrt2 or FREE?)")
print("="*78)

# ----------------------------------------------------------------------------
# 1. EXACT GEOMETRY (Foot hep-ph/9402242, verified from the source PDF):
#    Q = (sum m) / [ (2/3)(sum sqrt m)^2 ]  ;  Koide <=> Q=2/3 <=> cos^2 theta = 3/4
#    where cos theta = (v . n)/(|v||n|), v=(sqrt m_i), n=(1,1,1).
# ----------------------------------------------------------------------------
print("\n[1] Foot geometry: Q = 1/(2 cos^2 theta); Koide Q=2/3 <=> cos^2 theta = 3/4 <=> theta=45deg")

se, smu, stau = sp.symbols('s_e s_mu s_tau', positive=True)  # sqrt-masses
v = sp.Matrix([se, smu, stau])
n = sp.Matrix([1,1,1])
cos2 = (v.dot(n))**2 / (v.dot(v) * n.dot(n))
# Q in terms of cos^2:
Q_geo = (v.dot(v)) / (sp.Rational(2,3) * (v.dot(n))**2)
# show Q = 1/(2 cos^2 theta) * (1/3)*3 ... do it cleanly:
Q_in_cos2 = sp.simplify( (v.dot(v))*3 / (2*(v.dot(n))**2) )
relation = sp.simplify(Q_in_cos2 - 1/(2*cos2))
print("    Q - 1/(2 cos^2 theta) simplifies to:", relation, " (0 => identity holds)")
# So Q=2/3 <=> cos^2 theta = 3/4.
print("    => Koide content is the ANGLE cos^2 theta = 3/4  (equivalently theta=45deg).")

# ----------------------------------------------------------------------------
# 2. CIRCULANT PARAMETRIZATION (Koide's ansatz):
#    sqrt(m_i) = M (1 + r cos(delta + 2 pi i/3)),  i=0,1,2
#    => Q = 1/3 + r^2/6  for ANY M, delta.  (phase delta drops out of Q.)
# ----------------------------------------------------------------------------
print("\n[2] Circulant ansatz sqrt(m_i)=M(1 + r cos(delta + 2 pi i/3)): Q depends ONLY on r")

M, r, delta = sp.symbols('M r delta', real=True, positive=True)
i = sp.symbols('i', integer=True)
sm = [M*(1 + r*sp.cos(delta + 2*sp.pi*k/3)) for k in range(3)]
m  = [s**2 for s in sm]
sum_m   = sp.simplify(sum(m))
sum_sm  = sp.simplify(sum(sm))
Q_ansatz = sp.simplify(sum_m / (sp.Rational(2,3) * sum_sm**2))
Q_ansatz = sp.simplify(Q_ansatz)
print("    Q(r,delta) =", Q_ansatz)
# Check it equals 1/3 + r^2/6 independent of delta:
target = sp.Rational(1,3) + r**2/6
diff = sp.simplify(Q_ansatz - target)
print("    Q - (1/3 + r^2/6) =", diff, "  (0 => Q INDEPENDENT of delta, only r matters)")
print("    => Koide Q=2/3 <=>  1/3 + r^2/6 = 2/3  <=>  r^2 = 2  <=>  r = sqrt(2).")
r_for_koide = sp.solve(sp.Eq(target, sp.Rational(2,3)), r)
print("    r solving Q=2/3:", r_for_koide, " => r = sqrt(2) is THE content (45deg, cos^2=3/4).")

# ----------------------------------------------------------------------------
# 3. The banked machine-exact identity: sqrt(2/Z) = (3/8pi)^(1/4), Z=sqrt(32pi/3).
#    Note this is sqrt(2/Z) NOT r=sqrt(2). Test whether dS geometry hands r=sqrt2.
# ----------------------------------------------------------------------------
print("\n[3] Banked geometry: sqrt(2/Z) = (3/8pi)^(1/4) ;  Z = sqrt(32 pi/3)")
Zsym = sp.sqrt(sp.Rational(32,1)*sp.pi/3)
lhs = sp.sqrt(2/Zsym)
rhs = (sp.Rational(3,1)/(8*sp.pi))**sp.Rational(1,4)
print("    sqrt(2/Z) - (3/8pi)^(1/4) =", sp.simplify(lhs - rhs), " (0 => machine-exact)")
print("    Z numeric      =", mp.mpf(sp.N(Zsym, 40)))
print("    sqrt(2/Z)      =", mp.mpf(sp.N(lhs, 40)))
print("    NOTE: r=sqrt(2) = 1.41421...; sqrt(2/Z)=0.5878...; these are DIFFERENT numbers.")
print("    The dS geometry hands sqrt(2/Z)=0.588, NOT the Koide amplitude r=sqrt(2)=1.414.")

print("\n" + "="*78)
print("DONE part 1 (geometry).  Part 2 = the thermal-amplitude FORCING tests.")
print("="*78)
