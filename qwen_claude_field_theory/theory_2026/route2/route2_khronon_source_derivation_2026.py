#!/usr/bin/env python3
r"""
DECISIVE Route-2 calculation -- ACTION-LEVEL variation, no scaling estimates.

Khronometric MOND with a DYNAMICAL a0 = a0(K),  a0(K)^2 = c^2 K^2 / Z^2.
eps = 0, eta_K = 0.  F(X) = -2 sqrt(X) + 2 ln(1+sqrt(X)),  X = c^4 a_mu a^mu / a0(K)^2.

Restore the khronon Stuckelberg mode  T = t + psi(r).  Compute, EXACTLY to linear
order in psi, the khronon Euler-Lagrange SOURCE  S_T(r) = delta S / delta psi |_{psi=0}
for the F-sector (the only sector carrying a0(K)), then the quadratic operator W(X).

CONVENTION: c = 1 in the line element (t carries length units, Phi is Phi_phys/c^2, a0 is
a0_phys/c^2).  This removes ALL factor-of-c bookkeeping; the ratio X = (g/a0)^2 is exactly
the physical (g_phys/a0_phys)^2, and whether the SOURCE VANISHES is convention independent.
Physical numbers are restored at the end from g/a0 directly.  In c=1:
   a0^2 = K^2 / Z^2 ,   X = a_mu a^mu / a0^2 = Z^2 a_mu a^mu / K^2 .

Labels: DERIVED (sympy here) / ASSUMED (background ansatz) / IMPORTED (prior repo result).
"""
import sympy as sp

def head(t): print("\n"+"="*94+f"\n{t}\n"+"="*94)
def ok(c,l,d=""):
    print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else "")); return c

PASS=[True]
def gate(c,l,d=""):
    r=ok(c,l,d); PASS[0]=PASS[0] and r; return r

# ------------------------------------------------------------------ symbols (c=1)
t,r,th,ph = sp.symbols('t r theta phi', real=True)
Z         = sp.symbols('Z', positive=True)
eps       = sp.symbols('epsilon', real=True)          # bookkeeping: linear order in psi
a         = sp.Function('a', positive=True)(t)        # FLRW scale factor
Phi       = sp.Function('Phi')(r)                     # static potential (= Phi_phys/c^2)
psi       = sp.Function('psi')(r)                     # khronon Stuckelberg mode
Hs        = sp.Symbol('H', positive=True)
X4        = [t,r,th,ph]

# ASSUMED trial geometry, c=1 (Psi -> 0: corrects a^2 and measure one order beyond the source)
N2 = 1 + 2*Phi
g  = sp.diag(-N2, a**2, a**2*r**2, a**2*r**2*sp.sin(th)**2)
gi = g.inv()
sqrtg = sp.sqrt(-g.det())

head("0 -- setup: metric (c=1), khronon T = t + eps*psi(r)   [ASSUMED ansatz]")
print("  g_tt = -(1+2Phi) ,  g_rr = a(t)^2 ,  Psi -> 0 (leading order)")
T  = t + eps*psi
dT = [sp.diff(T,X4[i]) for i in range(4)]

# u_mu = - d_mu T / sqrt(-(dT)^2)   (unit: u.u = -1)
normsq = sum(gi[i,j]*dT[i]*dT[j] for i in range(4) for j in range(4))
Nphi   = sp.sqrt(-normsq)
u_lo   = [sp.simplify(-dT[i]/Nphi) for i in range(4)]
u_up   = [sp.simplify(sum(gi[i,j]*u_lo[j] for j in range(4))) for i in range(4)]

def christoffel(g,gi,X):
    n=4; G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                G[l][m][k]=sp.Rational(1,2)*sum(
                    gi[l,s]*(sp.diff(g[s,m],X[k])+sp.diff(g[s,k],X[m])-sp.diff(g[m,k],X[s]))
                    for s in range(n))
    return G
Gam = christoffel(g,gi,X4)

# a_mu = u^nu nabla_nu u_mu
nab=[[sp.diff(u_lo[mu],X4[nu])-sum(Gam[l][nu][mu]*u_lo[l] for l in range(4))
      for mu in range(4)] for nu in range(4)]
a_lo=[sp.simplify(sum(u_up[nu]*nab[nu][mu] for nu in range(4))) for mu in range(4)]
a2  = sp.simplify(sum(gi[i,j]*a_lo[i]*a_lo[j] for i in range(4) for j in range(4)))

# K = nabla_mu u^mu
K = sp.simplify(sum(sp.diff(sqrtg*u_up[i],X4[i]) for i in range(4))/sqrtg)

# ------------------------------------------------------------------ background checks
head("1 -- background checks at psi=0  [DERIVED here, must match IMPORTED repo identities]")
sub_adot = {sp.Derivative(a,t): Hs*a}
K0 = sp.powsimp(sp.simplify(K.subs(eps,0)).subs(sub_adot), force=True)
print("  K(psi=0)   =", K0)
_diff = (K0 - 3*Hs/sp.sqrt(1+2*Phi))
_num  = complex(_diff.subs({Phi:sp.Rational(1,10), Hs:1}))
gate(abs(_num) < 1e-12, "K|_{psi=0} = 3H/sqrt(1+2Phi) = 3H(1-Phi+..)   (IMPORTED: isotropy script)")

a_r0 = sp.simplify(a_lo[1].subs(eps,0))
print("  a_r(psi=0) =", a_r0)
gate(sp.simplify(a_r0 - sp.diff(Phi,r)/(1+2*Phi))==0,
     "a_r|_{psi=0} = Phi'/(1+2Phi) = Phi'(1-2Phi+..) = D_r ln N  (a_i = d_iPhi/c^2 phys)")

Klin = sp.simplify(sp.diff(K,eps).subs(eps,0).subs(sub_adot))
lap  = lambda f: sp.diff(f,r,2)+2*sp.diff(f,r)/r
# leading (Phi->0) piece of delta K:
Klin0 = sp.simplify(Klin.subs(Phi,0).doit())
gate(sp.simplify(Klin0 + lap(psi)/a**2)==0,
     "delta K = -lap(psi)/a^2   (IMPORTED: khronon_K script B1)", f"exact-at-Phi0 = {Klin0}")
print("\n  [checkpoint] three IMPORTED identities reproduced from the metric.\n")

print("STAGE-1", "PASS" if PASS[0] else "FAIL")

# =====================================================================================
head("2 -- F-sector reduced Lagrangian and the khronon SOURCE  S_T(r)=dS/dpsi|_{psi=0}")
# =====================================================================================
# Action F-term (c=1):  S_F = -(1/16piG) INT sqrt(-g) (2 a0^2) F(X),  a0^2=K^2/Z^2,
#   X = Z^2 a_mu a^mu / K^2.   sqrt(-g)=sqrtg has NO psi dependence.
#   Drop overall -(1/16piG) and the angular 4pi; keep the radial density.
F  = sp.Function('F')                                  # keep FULL X-dependence symbolic
Xe = sp.simplify(Z**2 * a2 / K**2)                     # X(eps), exact
pre= -sqrtg * (2*K**2/Z**2)                            # prefactor -sqrt(-g)*2 a0^2, exact eps
rhoF = pre * F(Xe)                                     # radial Lagrangian density (F-sector)

# linear-in-eps piece  L1(r) = A psi + B psi' + C psi''  (chain rule hits F automatically)
L1 = sp.diff(rhoF, eps).subs(eps,0)
L1 = L1.subs(sub_adot).doit()
# strip the sin(theta) from sqrtg (angular integral) -> radial measure a^3 r^2 * sqrt(N2)
L1 = sp.simplify(L1 / sp.sin(th))

psi1=sp.Derivative(psi,r); psi2=sp.Derivative(psi,r,2)
A = sp.simplify(sp.diff(L1, psi))
B = sp.simplify(sp.diff(L1, psi1))
C = sp.simplify(sp.diff(L1, psi2))
# guard: no higher derivatives leaked
gate(sp.simplify(L1 - (A*psi + B*psi1 + C*psi2))==0, "L1 is (at most) 2nd order in psi")

# Euler-Lagrange source:  S_T = A - d/dr B + d^2/dr^2 C
S_T = sp.simplify(A - sp.diff(B,r) + sp.diff(C,r,2))
print("  built S_T(r) (F-sector). Substituting an explicit VACUUM solution Phi=-M/r ...")

# X0 (background X) in terms of r,M,H,Z for reporting
M,Hn = sp.symbols('M H', positive=True)
Phifun = -M/r
def vac(expr):
    return expr.subs({sp.Derivative(Phi,(r,3)): sp.diff(Phifun,r,3),
                      sp.Derivative(Phi,(r,2)): sp.diff(Phifun,r,2),
                      sp.Derivative(Phi,r):     sp.diff(Phifun,r),
                      Phi: Phifun})
S_T_vac = sp.simplify(vac(S_T))

# --- joint weak-field/slow expansion: Phi ~ O(d), H ~ O(d); X0 ~ O(1) held via F symbolic
d = sp.symbols('delta', positive=True)
scale = {M: d*M, Hs: d*Hn}
# X0 with the scaling (delta-independent at leading order):
X0 = sp.simplify((Z**2*a2/K**2).subs(eps,0).subs(sub_adot))
X0_vac = sp.simplify(vac(X0))
X0_lead = sp.simplify(sp.series(X0_vac.subs(scale), d, 0, 1).removeO())
print("  X0(r) [leading] =", X0_lead, "   (= (g/a0)^2, a0=3H/Z)")

S_T_scaled = S_T_vac.subs(scale)
# leading order in delta
ser = sp.series(S_T_scaled, d, 0, 4)
print("\n  S_T(r) series in the joint smallness delta (Phi,H ~ delta):")
sp.pprint(ser)
lead = sp.simplify(sp.series(S_T_scaled, d, 0, 4).removeO())
gate(True, "S_T(r) computed")
print("\n  Leading S_T(r) =")
sp.pprint(sp.simplify(lead))

with open(os.path.join(os.path.dirname(__file__),'_ST.txt'),'w') as f:
    f.write("S_T_vac = "+str(S_T_vac)+"\n\nleading = "+str(lead)+"\nX0_lead="+str(X0_lead)+"\n")

# vanishing test
is_zero = sp.simplify(lead)==0
print("\n  >>> F-sector source vanishes in vacuum? ", "YES (Outcome A)" if is_zero else "NO (Outcome B)")

import os
print("\nSTAGE-2", "PASS" if PASS[0] else "FAIL")
