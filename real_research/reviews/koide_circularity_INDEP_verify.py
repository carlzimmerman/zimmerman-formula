#!/usr/bin/env python3
"""
INDEPENDENT verification of the swing's two headline claims (separate from the workflow's scripts).
Per the committed-script rule: I re-derive the load-bearing facts myself rather than trust the agents' prose.

  CLAIM 1 (circularity theorem): for the Koide parametrization sqrt(m_i) = M(1 + r cos(theta + 2pi k/3)),
           Q := (sum m)/(sum sqrt m)^2 = 1/3 + r^2/6  -- depends ONLY on r, not on theta or M.
           => Q=2/3 <=> r=sqrt2 EXACTLY. So "force r=sqrt2" and "assume Q=2/3" are the SAME statement.
  CLAIM 2 (flavor-blindness = scale-invariance): Q is invariant under sqrt(m_i) -> w*sqrt(m_i) for any common w.
           => a flavor-blind scalar response (one w for all 3 generations, e.g. mu_fw) CANNOT change Q.

If both hold, the swing's WHIFF verdict is sound: the framework's own (flavor-blind) response cannot supply the
Koide amplitude, and r=sqrt2 only ever appears by fitting the masses (smuggling 2/3 in).
"""
import sympy as sp

M, r, th, w = sp.symbols('M r theta w', positive=True)
k = [0,1,2]
phi = [th + 2*sp.pi*j/3 for j in k]
sm  = [M*(1 + r*sp.cos(p)) for p in phi]          # sqrt-mass components
m   = [s**2 for s in sm]

print("="*78); print("CLAIM 1 — circularity theorem  Q = 1/3 + r^2/6"); print("="*78)
sum_sm = sp.simplify(sum(sm))
sum_m  = sp.simplify(sum(m))
Q = sp.simplify(sum_m/sum_sm**2)
print(f"  sum sqrt(m)      = {sum_sm}        (theta-dependence cancels: Sum cos = 0)")
print(f"  sum m            = {sp.expand_trig(sp.simplify(sum_m))}")
print(f"  Q = sum m/(sum sqrt m)^2 = {Q}")
target = sp.Rational(1,3) + r**2/6
print(f"  1/3 + r^2/6      = {target}")
ok1 = sp.simplify(Q - target) == 0
print(f"  [{'PASS' if ok1 else 'FAIL'}] Q == 1/3 + r^2/6 exactly (independent of theta and M)")
# solve Q = 2/3 for r
rsol = sp.solve(sp.Eq(target, sp.Rational(2,3)), r)
print(f"  Q=2/3  =>  r = {rsol}   (sqrt2 = {float(sp.sqrt(2)):.6f})")
ok1b = sp.sqrt(2) in rsol
print(f"  [{'PASS' if ok1b else 'FAIL'}] Q=2/3 <=> r=sqrt2  => 'force r=sqrt2' IS 'assume Q=2/3' (circular)")

print("\n"+"="*78); print("CLAIM 2 — flavor-blindness = scale-invariance (a common w cannot move Q)"); print("="*78)
sm_w = [w*s for s in sm]                            # flavor-blind rescale: same w on every generation
Q_w = sp.simplify(sum(s**2 for s in sm_w)/sum(sm_w)**2)
print(f"  Q after sqrt(m_i) -> w*sqrt(m_i)  = {Q_w}")
ok2 = sp.simplify(Q_w - Q) == 0
print(f"  [{'PASS' if ok2 else 'FAIL'}] Q unchanged by any common w  => a flavor-blind scalar leaves Q (and r) fixed")
# numeric cross-check on the REAL leptons
import numpy as np
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
def Qn(v): v=np.asarray(v); return v.sum()/np.sqrt(v).sum()**2
base = Qn([me,mmu,mtau])
scaled = [Qn([w0*me, w0*mmu, w0*mtau]) for w0 in (0.5, 2.0, 137.0)]
print(f"  real leptons: Q={base:.8f}; after common rescale x{{0.5,2,137}}: {[f'{q:.8f}' for q in scaled]}")
ok2b = all(abs(q-base) < 1e-12 for q in scaled)
print(f"  [{'PASS' if ok2b else 'FAIL'}] real-lepton Q invariant under common rescale (to 1e-12)")

print("\n"+"="*78)
allok = ok1 and ok1b and ok2 and ok2b
print(f"OVERALL: {'ALL PASS — swing WHIFF verdict is sound' if allok else 'CHECK FAILED'}")
print("="*78)
print("""  => The framework's mu_fw is flavor-blind (one response for all generations = a common w), and Q is
     scale-invariant, so mu_fw CANNOT change Q. r=sqrt2 enters only by fitting the masses, and by the
     circularity theorem that is identical to assuming Q=2/3. The framework hosts the Koide SHAPE; its own
     response does not force the amplitude. Same number field (reframe correct), structurally wrong slot.""")
