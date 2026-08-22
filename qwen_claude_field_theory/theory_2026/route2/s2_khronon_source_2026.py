#!/usr/bin/env python3
r"""ROUTE 2 DECISIVE -- STEP 2: khronon source S_T(r) = delta S/delta T |_{T=t}, MOND sector.

Shift symmetry T->T+const => EOM d_mu J^mu=0, J^mu=delta L/delta(d_mu T).
Perturb T=t+eps*psi(r,t); expand L_M=-(2K^2/Z^2)F(X), X=(Z^2/K^2)a_mu a^mu to O(eps);
Euler-Lagrange source at psi=0.  Psi=0 (does not enter a_mu / MOND structure).  F abstract.
c=1; physical numbers restored later.
"""
import sympy as sp
t, r, th = sp.symbols('t r theta', real=True)
H, Z, eps = sp.symbols('H Z epsilon', positive=True)
Phi = sp.Function('Phi')(r); a = sp.Function('a')(t); psi = sp.Function('psi')(r, t)
F = sp.Function('F')
XX = [t, r, th, sp.Symbol('ph')]
N2 = 1 + 2*Phi
g = sp.diag(-N2, a**2, a**2*r**2, a**2*r**2*sp.sin(th)**2)
gi = g.inv()
def christoffel(g, gi, X):
    n=len(X); G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                s=sum(gi[l,p]*(sp.diff(g[p,m],X[k])+sp.diff(g[p,k],X[m])-sp.diff(g[m,k],X[p])) for p in range(n))
                G[l][m][k]=sp.together(s/2)
    return G
Gam = christoffel(g, gi, XX)
sqrtmg = sp.sqrt(-g.det())
T = t + eps*psi
wl = [sp.diff(T, XX[i]) for i in range(4)]
Ncal = sp.sqrt(-sum(gi[m,n]*wl[m]*wl[n] for m in range(4) for n in range(4)))
u_l = [-wl[m]/Ncal for m in range(4)]
u_u = [sum(gi[m,n]*u_l[n] for n in range(4)) for m in range(4)]
K = sum(sp.diff(sqrtmg*u_u[m], XX[m]) for m in range(4))/sqrtmg
nab = [[sp.diff(u_l[mu],XX[nu]) - sum(Gam[l][nu][mu]*u_l[l] for l in range(4)) for mu in range(4)] for nu in range(4)]
a_l = [sum(u_u[nu]*nab[nu][mu] for nu in range(4)) for mu in range(4)]
a2 = sum(gi[m,n]*a_l[m]*a_l[n] for m in range(4) for n in range(4))
adot = sp.Derivative(a, t)
sub_H = lambda e: e.subs(adot, H*a)
print("linearize K...", flush=True)
K0 = sub_H(K.subs(eps,0)); K1 = sub_H(sp.diff(K, eps).subs(eps,0))
print("linearize a2...", flush=True)
a2_0 = sub_H(a2.subs(eps,0)); a2_1 = sub_H(sp.diff(a2, eps).subs(eps,0))
K0=sp.simplify(K0); K1=sp.simplify(K1); a2_0=sp.simplify(a2_0); a2_1=sp.simplify(a2_1)
print("K0  =", K0)
print("K1  =", K1)
print("a2_0=", a2_0)
print("a2_1=", a2_1)
X0 = sp.simplify(Z**2/K0**2 * a2_0)
X1 = sp.simplify(Z**2*(a2_1/K0**2 - 2*a2_0*K1/K0**3))
print("X0  =", X0)
print("X1  =", X1)
Xs = sp.Symbol('Xs')
L1 = -(2/Z**2)*(2*K0*K1*F(X0) + K0**2*sp.Derivative(F(Xs),Xs).subs(Xs,X0)*X1)
mu_meas = sp.sqrt(N2)*a**3*r**2
Ldens1 = sp.expand(mu_meas*L1)
pr=sp.Derivative(psi,r); prr=sp.Derivative(psi,r,2); pt=sp.Derivative(psi,t)
prt=sp.Derivative(psi,r,t); ptt=sp.Derivative(psi,t,2)
S_T = ( sp.diff(Ldens1,psi) - sp.diff(sp.diff(Ldens1,pr),r) + sp.diff(sp.diff(Ldens1,prr),r,2)
        - sp.diff(sp.diff(Ldens1,pt),t) + sp.diff(sp.diff(Ldens1,ptt),t,2)
        + sp.diff(sp.diff(Ldens1,prt),r,t) )
S_T = sub_H(S_T)
zero = {psi:0, pr:0, prr:0, pt:0, prt:0, ptt:0, sp.Derivative(psi,r,3):0,
        sp.Derivative(psi,r,2,t):0, sp.Derivative(psi,r,t,2):0, sp.Derivative(psi,t,3):0}
S_T = sub_H(S_T.subs(zero))
S_T_red = sp.simplify(S_T/mu_meas)
print("\n===== S_T / measure  (MOND-sector khronon source) =====")
sp.pprint(S_T_red)
with open('S_T_raw.txt','w') as f: f.write(str(S_T_red))
print("\n[written S_T_raw.txt]")
