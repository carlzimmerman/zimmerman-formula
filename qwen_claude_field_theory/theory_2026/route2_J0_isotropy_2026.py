#!/usr/bin/env python3
r"""RETRACTION of the J_0 ~ H estimate, and the structure isotropy actually permits.

In EXACT FLRW isotropy forces J^i = 0 -- there is no radial vector available.  A radial
khronon current therefore requires the mass, so J_0^r ~ H x (local inhomogeneity), NOT
J_0^r ~ H.  The previous delta K/3H ~ 4.5e3 at 1 AU rested entirely on the unsuppressed
form and is VOID."""
import sympy as sp
t,r,th,ph=sp.symbols('t r theta phi',real=True)
a=sp.Function('a',positive=True)(t); Phi=sp.Function('Phi')(r); Psi=sp.Function('Psi')(r)
c=sp.Symbol('c',positive=True); H=sp.Function('H')(t)
N=sp.sqrt(1+2*Phi/c**2); A2=a**2*(1-2*Psi/c**2)
g=sp.diag(-N**2*c**2,A2,A2*r**2,A2*r**2*sp.sin(th)**2); X=[t,r,th,ph]
sq=sp.sqrt(-sp.simplify(g.det())); u=[1/N,0,0,0]
K=sp.simplify(sum(sp.diff(sq*u[i],X[i]) for i in range(4))/sq)
K=sp.simplify(sp.series(K.rewrite(sp.sqrt),c,sp.oo,3).removeO()).subs(sp.Derivative(a,t),H*a)
print("  K(psi=0) =",sp.simplify(K),"   [static mass, Psi_dot = 0]")
print("  d_r K    =",sp.simplify(sp.diff(K,r)),"  = -(3H/c^2) d_r Phi")
print("""
  So the leading radial structures are d_r K and d_r Phi, both O(H x weak-field gradient).

  POSSIBLE EXACT VACUUM CANCELLATION: if J_0^r is proportional to d_r K (hence d_r Phi),
      div J_0 ~ (H/c^2) lap Phi = 0   outside matter,
  the khronon source vanishes identically in vacuum, lap psi = 0, and K = 3H EXACTLY there
  -- the strongest possible outcome for Route 2.

  NOT ASSERTED.  Whether J_0^r carries that structure is the delta S/delta T calculation
  on the full action, which is what must be done next.  No estimate substitutes for it.""")
