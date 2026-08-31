#!/usr/bin/env python3
"""
EXACT symbolic certificate that dY^(1) = 0 (first-order variation of Y vanishes
on the FLRW/Y=0 background), so the divergent F_YY and non-analytic Y^{3/2}
term never enter the LINEAR cosmological action.

We expand Y = (g^{mn} + A^mu A^nu) dphi_mu dphi_nu to O(eps) with fully general
first-order perturbations of g^{mn}, A^mu, dphi_mu, enforcing A^2=-1 to O(eps).
"""
import sympy as sp

eps = sp.symbols('epsilon')
Qb  = sp.symbols('Qbar', real=True)   # background phidot

# background local frame: g^{mn}=eta, A^mu=(1,0,0,0), grad_mu phi=(Qb,0,0,0)=-Qb A_mu
eta = sp.diag(-1,1,1,1)

# generic symmetric first-order perturbation of the inverse metric
hg = sp.zeros(4,4)
for i in range(4):
    for j in range(i,4):
        s = sp.Symbol(f'hg{i}{j}'); hg[i,j]=s; hg[j,i]=s
ginv = eta + eps*hg
g = ginv.inv()                                   # lower metric = inverse of ginv, exact

# generic first-order perturbation of A^mu
dA = sp.Matrix([sp.Symbol(f'dA{i}') for i in range(4)])
Aup = sp.Matrix([1,0,0,0]) + eps*dA

# enforce A^mu A_mu = -1 to O(eps):  d(A^mu A^nu g_{mn}) = 0
# background A_mu = eta.(1,0,0,0)=(-1,0,0,0)
norm = (Aup.T*g*Aup)[0]
norm1 = sp.series(norm, eps, 0, 2).removeO()
c1 = sp.expand(norm1).coeff(eps,1)               # first-order constraint = 0
# solve for dA[0]
sol0 = sp.solve(sp.Eq(c1,0), dA[0])[0]
Aup = Aup.subs(dA[0], sol0)

# generic first-order perturbation of grad_mu phi (lower index)
dphi = sp.Matrix([Qb,0,0,0]) + eps*sp.Matrix([sp.Symbol(f'dp{i}') for i in range(4)])

qinv = ginv + Aup*Aup.T
Y = (dphi.T*qinv*dphi)[0]
Yser = sp.series(Y, eps, 0, 3).removeO()
Y0 = sp.expand(Yser).coeff(eps,0)
Y1 = sp.expand(Yser).coeff(eps,1)
Y2 = sp.expand(Yser).coeff(eps,2)
print("Y^(0) (background)      =", sp.simplify(Y0), "   (must be 0)")
print("Y^(1) (first order)     =", sp.simplify(Y1), "   (must be 0 for ANY perturbation)")
print("Y^(2) not-identically-0 =", sp.simplify(Y2) != 0)
print()
print("=> dY is purely second order. In the quadratic action:")
print("   F_Y|bg * dY^(2) = 0*(...) = 0   and   F_YY|bg * (dY^(1))^2 = (oo)*0 = 0.")
print("   The J/MOND sector is INVISIBLE to linear cosmological perturbations;")
print("   the linear delta-phi spatial gradient term is the explicit (2-K_B) Y.")
