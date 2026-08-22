#!/usr/bin/env python3
r"""ROUTE 2 DECISIVE -- STEP 1: validate the covariant khronon machinery (geometric c=1).

Reproduce the ESTABLISHED results before the variation:
   K|_{T=t} = 3H(1 - Phi)          [Phi = phi/c^2 dimensionless potential]
   d_r K    = -3H d_r Phi          (static)
   a_i      = d_i Phi              (leading)
All DERIVED here from full 4D Christoffels.  c=1; physical c restored only in a0,X later.
"""
import sympy as sp
t, r, th, ph = sp.symbols('t r theta phi', real=True)
H = sp.symbols('H', positive=True)
Phi = sp.Function('Phi')(r); Psi = sp.Function('Psi')(r); a = sp.Function('a')(t)
X = [t, r, th, ph]
N2 = 1 + 2*Phi; Bf = 1 - 2*Psi
g = sp.diag(-N2, a**2*Bf, a**2*Bf*r**2, a**2*Bf*r**2*sp.sin(th)**2)
gi = g.inv(); sqrtmg = sp.sqrt(-sp.simplify(g.det()))

def christoffel(g, gi, X):
    n=len(X); G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                s=sum(gi[l,p]*(sp.diff(g[p,m],X[k])+sp.diff(g[p,k],X[m])-sp.diff(g[m,k],X[p])) for p in range(n))
                G[l][m][k]=sp.simplify(s/2)
    return G
Gam=christoffel(g,gi,X)
wl=[sp.Integer(1),0,0,0]
Ncal=sp.sqrt(-sum(gi[m,n]*wl[m]*wl[n] for m in range(4) for n in range(4)))
u_l=[sp.simplify(-wl[m]/Ncal) for m in range(4)]
u_u=[sp.simplify(sum(gi[m,n]*u_l[n] for n in range(4))) for m in range(4)]
print("u.u =", sp.simplify(sum(g[m,n]*u_u[m]*u_u[n] for m in range(4) for n in range(4))), "(expect -1)")
K=sp.simplify(sum(sp.diff(sqrtmg*u_u[m],X[m]) for m in range(4))/sqrtmg).subs(sp.Derivative(a,t),H*a)
K=sp.simplify(K)
print("\nK|_{T=t} =", K)
print("K - 3H(1-Phi) =", sp.simplify(K-3*H*(1-Phi)))
print("d_r K =", sp.simplify(sp.diff(K,r)), "  [expect -3H Phi']")
nab=[[sp.simplify(sp.diff(u_l[mu],X[nu])-sum(Gam[l][nu][mu]*u_l[l] for l in range(4))) for mu in range(4)] for nu in range(4)]
a_l=[sp.simplify(sum(u_u[nu]*nab[nu][mu] for nu in range(4))) for mu in range(4)]
print("\na_mu =", a_l, "  [expect a_r=Phi']")
a2=sp.simplify(sum(gi[m,n]*a_l[m]*a_l[n] for m in range(4) for n in range(4)))
print("a_mu a^mu =", sp.simplify(a2), "  [expect (Phi')^2/(a^2 (1+2Phi)) ~ (Phi')^2/a^2]")
