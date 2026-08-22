#!/usr/bin/env python3
r"""Route 2: C=0 holds for a regular star, but the decisive quantity is J_0, not C.

Vacuum khronon equation in spherical symmetry:  r^2 N sqrt(B) J^r = C  (conserved flux).
Write J^r = W psi' + J_0.  Then C = 0 gives psi' = -J_0/W, NOT psi' = 0."""
import sympy as sp, numpy as np
s=sp.symbols('s',positive=True)                      # s = sqrt(X) = g/a0
Wpar=2/(1+s)**2; Wperp=2/(1+s)                       # eta_K = 0 a-sector Hessian
print("W_par =",Wpar," W_perp =",Wperp)
print("  s->0 (stellar CENTRE, g->0 by symmetry): W ->",sp.limit(Wpar,s,0),"  finite/nonzero")
print("  s->oo (deep Newtonian BULK):             W ->",sp.limit(Wpar,s,sp.oo),"  degenerates")
print("  => r^2 W psi' -> 0 at r=0 forces C = 0 for a regular extended star.  [Carl's branch]")
print("""
BUT C = 0 does NOT give psi' = 0.  J_0 vanishes only if J^r is ODD in psi', i.e. under
T-reflection.  The action IS T-even (K_ij odd, a_i and (3)R_ij even) -- but the
COSMOLOGICAL BACKGROUND BREAKS IT: on FLRW, K = 3H is T-ODD.  So J_0 = O(H) is allowed
and psi' ~ H/W.  The expansion that GENERATES a0 is the same thing that breaks the parity
protecting psi' = 0.""")
a0=9.3619e-11; H0=2.184e-18; GMs=1.32712e20; AU=1.495979e11
print(f"\n  {'r':<14}{'s = g/a0':>12}{'W_par':>12}{'delta K/3H if J_0 ~ H':>24}")
for lab,rr in (("1 AU",AU),("Saturn 9.5 AU",9.5*AU),("R_M 7960 AU",7960*AU),("1 pc",3.086e16)):
    g=GMs/rr**2; sv=g/a0; W=2/(1+sv)**2
    print(f"  {lab:<14}{sv:>12.3e}{W:>12.3e}{(H0/W)/rr/(3*H0):>24.3e}")
print("""
  >> 1 inside the Solar System, negligible by the MOND radius.  So the zero-charge branch
  alone does not save Route 2; what saves it is J_0 being suppressed relative to H.

  THE CALCULATION IS: what is J_0, the psi-independent part of the khronon current on an
  expanding background, from the FULL action?  Not 'is C = 0' -- that is settled.""")
