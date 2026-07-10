#!/usr/bin/env python3
"""Diagnose the l=2 indicial exponents. Build P from the second-order Navier operator
directly (constant moduli) via the known coupled ODE, and cross-check the first-order P."""
import numpy as np, sympy as sp

lam,mu,r,p=sp.symbols('lam mu r p',positive=True)
n=6  # l=2
M2=lam+2*mu
# u = U P2 er + V dP2 eth ; try U=A r^p, V=B r^p
A,B=sp.symbols('A B')
U=A*r**p; V=B*r**p
J=sp.diff(U,r)+2*U/r-n*V/r
# Navier for constant moduli: (lam+mu) grad(divu) + mu lap(u) + rho f =0, f=0 homogeneous.
# radial component operator on the (U,V,P2) ansatz (standard spherical elasticity):
#   r-comp: (lam+2mu)(dJ/dr)  - 2 mu n /r * ( dV/dr + (U - V)/r )  ... use vector-Laplacian identities.
# Use the exact componentwise vector Laplacian for spheroidal field:
# (lap u)_r = U'' + 2U'/r - 2U/r^2 - n/r^2*(U... ) -> use the identity:
# For u = U(r)Y er + V(r) grad_1 Y (grad_1 = surface grad), with Y=P_l:
#  (lap u)_r        = U'' + (2/r)U' - (2/r^2)U - (n/r^2)U + (2n/r^2)V
#  (lap u)_horiz    = V'' + (2/r)V' - (n/r^2)V + (2/r^2)U        [coefficient of grad_1 Y]
# grad(divu)_r      = J'
# grad(divu)_horiz  = J/r
lapU=sp.diff(U,r,2)+2/r*sp.diff(U,r)-2/r**2*U-n/r**2*U+2*n/r**2*V
lapV=sp.diff(V,r,2)+2/r*sp.diff(V,r)-n/r**2*V+2/r**2*U
eqr=sp.expand((lam+mu)*sp.diff(J,r)+mu*lapU)
eqh=sp.expand((lam+mu)*J/r+mu*lapV)
# both ~ r^(p-2); collect coefficient matrix in (A,B)
cr=sp.Poly(sp.expand(eqr*r**(2-p)),A,B).coeffs() if False else None
M=sp.Matrix([[sp.simplify(eqr.coeff(A)*r**(2-p)).subs(A,0).subs(B,0)+0,0]])
# extract 2x2 by differentiating
Mmat=sp.zeros(2,2)
Mmat[0,0]=sp.simplify(sp.diff(eqr,A)*r**(2-p))
Mmat[0,1]=sp.simplify(sp.diff(eqr,B)*r**(2-p))
Mmat[1,0]=sp.simplify(sp.diff(eqh,A)*r**(2-p))
Mmat[1,1]=sp.simplify(sp.diff(eqh,B)*r**(2-p))
det=sp.simplify(Mmat.det())
sols=sp.solve(sp.Eq(det,0),p)
print("2nd-order Navier indicial det -> p =",sorted(set(sols),key=lambda z:sp.re(z)))
print("Mmat=",Mmat)
