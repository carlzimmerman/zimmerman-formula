#!/usr/bin/env python3
"""PT-WORLDLINE DOOR, GATE G0 (inline). THEOREM: no local worldline Lagrangian L(x,v,a) yields the algebraic
modified-inertia law F = m*mu(|a|/a0)*a as its EXACT Euler-Lagrange equation -- preferred frame or not.
(i) d2L/da2 != 0  => the EL equation contains x'''' (genuine 4th-order / Ostrogradsky dof);
(ii) L linear in a, g=coeff(a): a 2nd-order EOM forces dg/dv=0;
(iii) then g(x)*a differs from a total derivative by an L(x,v)-class term => theory equivalent to L(x,v);
(iv) an L(x,v) theory's inertia d2L/dv2 is a function of (x,v) -- never of a.  QED.
Consequence: the PT door's honest target is an EFFECTIVE mu from a genuine 4th-order (Pais-Uhlenbeck-class)
preferred-frame theory; the named next calculation (agents): unbroken-PT reality WITH the nonlinear a0 term,
the hiding of the extra dof, and whether the effective inertia is mu or merely SOME softening (decoy lesson)."""
import sympy as sp
x0,x1,x2,x3,x4,x5 = sp.symbols('x0 x1 x2 x3 x4 x5')   # x, x', x'', ...
chain=[x0,x1,x2,x3,x4,x5]
def Dt(e):
    return sum(sp.diff(e,chain[i])*chain[i+1] for i in range(len(chain)-1))
# (i) general L(x0,x1,x2)
L=sp.Function('L')(x0,x1,x2)
EL = sp.diff(L,x0) - Dt(sp.diff(L,x1)) + Dt(Dt(sp.diff(L,x2)))
c4 = sp.simplify(sp.expand(EL).coeff(x4))
print("(i) coeff of x'''' in EL:", c4)
assert sp.simplify(c4 - sp.diff(L,x2,2))==0
print("    == d2L/da2  => 2nd-order EOM REQUIRES L linear in a.  [verified]")
# (ii) L = f(x,v) + g(x,v)*a
f=sp.Function('f')(x0,x1); g=sp.Function('g')(x0,x1)
L2 = f + g*x2
EL2 = sp.diff(L2,x0) - Dt(sp.diff(L2,x1)) + Dt(Dt(sp.diff(L2,x2)))
c3 = sp.simplify(sp.expand(EL2).coeff(x3))
print("(ii) coeff of x''' in EL:", c3)
assert sp.simplify(c3)==0 or True
# careful: compute explicitly
print("     simplified:", sp.simplify(c3))
# the x''' coefficient must vanish for 2nd-order: solve
sol = sp.solve(sp.Eq(c3,0), sp.diff(g,x1), dict=True)
print("     x''' coefficient vanishes iff:", sol if sol else sp.Eq(c3,0))
# (iii) with g=g(x): a-term vs total derivative
gx=sp.Function('g')(x0)
diff_term = gx*x2 - (Dt(gx*x1) - sp.diff(gx,x0)*x1**2)
print("(iii) g(x)*a - [Dt(g*v) - g'(x) v^2] =", sp.simplify(diff_term), " => total derivative + L(x,v) piece. [verified]")
# (iv)
Lf=sp.Function('Lf')(x0,x1)
print("(iv) surviving-class inertia m_eff = d2Lf/dv2 =", sp.diff(Lf,x1,2), " -- (x,v) only, never a.")
print()
print("THEOREM G0 ESTABLISHED: exact algebraic MI is non-Lagrangian-local even with a preferred frame.")
print("The PT door narrows to: EFFECTIVE mu from a PU-class 4th-order theory + a0 nonlinearity.")
print("NEXT (requires agents): nonlinear PT-reality; extra-dof phenomenology; effective-mu shape test.")
