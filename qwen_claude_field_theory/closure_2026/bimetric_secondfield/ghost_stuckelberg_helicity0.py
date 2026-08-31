#!/usr/bin/env python3
"""Gauge-ROBUST ghost test: Stuckelberg helicity-0 analysis of the ghost-free-tuned derivative-bimetric
subspace. The interaction breaks the RELATIVE diff (eps_mn -> eps_mn + k_m xi_n + k_n xi_m); restore it
with Stuckelberg eps_mn = eps^phys_mn + k_m A_n + k_n A_m + k_m k_n pi. The Boulware-Deser ghost appears
as a higher-derivative / wrong-sign helicity-0 (pi) kinetic term. Two decisive gates:
  GATE-L (leading): the pure pi replacement eps=k_m k_n pi gives Int ~ (Sum c_i)(k^2)^3 pi^2 -- a
     6-derivative Ostrogradsky term. Ghost-free needs it to VANISH.
  GATE-N (next order): the pi kinetic term from A-pi demixing must be healthy (2-derivative, right sign)."""
import sympy as sp

eta=sp.diag(-1,1,1,1); etaI=eta.inv()
k=sp.Matrix(sp.symbols('k0 k1 k2 k3', real=True))
u0,u1=sp.symbols('u0 u1', real=True)

def Cconn(E):
    C=[[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
     for m in range(4):
      for n in range(4):
       v=sp.Integer(0)
       for s in range(4): v+=etaI[l,s]*(k[m]*E[s,n]+k[n]*E[s,m]-k[s]*E[m,n])
       C[l][m][n]=sp.expand(v/2)
    return C
def invs(C):
    T1=sum(C[a][m][n]*C[b][r][s]*eta[a,b]*etaI[m,r]*etaI[n,s] for a in range(4) for b in range(4) for m in range(4) for n in range(4) for r in range(4) for s in range(4))
    P=[sum(etaI[m,n]*C[a][m][n] for m in range(4) for n in range(4)) for a in range(4)]
    T2=sum(eta[a,b]*P[a]*P[b] for a in range(4) for b in range(4))
    V=[sum(C[a][a][mu] for a in range(4)) for mu in range(4)]
    T3=sum(etaI[m,n]*V[m]*V[n] for m in range(4) for n in range(4))
    T4=sum(etaI[m,n]*C[a][m][b]*C[b][n][a] for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    T5=sum(P[a]*V[a] for a in range(4))
    return [sp.expand(x) for x in (T1,T2,T3,T4,T5)]
cvec=[-u0,-u1/2,-u1/2,u0,u1]
def Int(E):
    T=invs(Cconn(E)); return sp.expand(sum(cvec[i]*T[i] for i in range(5)))

# ---------- GATE-L: pure helicity-0  eps_mn = k_m k_n * pi ----------
pi=sp.Symbol('pi', real=True)
Epi=sp.Matrix(4,4, lambda m,n: k[m]*k[n]*pi)
IL=sp.expand(Int(Epi))
k2=sum(etaI[i,i]*k[i]**2 for i in range(4))   # not used; keep k explicit
print("=== GATE-L: pure helicity-0 (eps=k k pi) ===")
print("  Int(kk pi) =", sp.factor(IL))
print("  => coefficient structure ~ (Sum c_i)*(k^2)^3 ; on ghost-free subspace Sum c_i =",
      sp.simplify(sum(cvec)), "=> leading 6-derivative helicity-0 term =", sp.simplify(IL))

# ---------- GATE-N: full Stuckelberg helicity 0+1: eps = k_m A_n + k_n A_m + k_m k_n pi ----------
A=sp.Matrix(sp.symbols('A0 A1 A2 A3', real=True))
Est=sp.Matrix(4,4, lambda m,n: k[m]*A[n]+k[n]*A[m]+k[m]*k[n]*pi)
IN=sp.expand(Int(Est))
# frame k=(w,0,0,kap)
w,kap=sp.symbols('omega kappa', real=True)
ksub={k[0]:w,k[1]:0,k[2]:0,k[3]:kap}
INs=sp.expand(IN.subs(ksub))
fields=[A[0],A[1],A[2],A[3],pi]
print("\n=== GATE-N: Stuckelberg (A_mu, pi) sector on the ghost-free subspace ===")
# pi^2 coefficient (should be 0 by GATE-L), A-pi and A-A
cpi2=sp.simplify(INs.coeff(pi,2))
print("  coeff pi^2 (expect 0):", cpi2)
# helicity-0 decouples into transverse vector (A1,A2) and longitudinal (A0,A3,pi). Extract longitudinal block.
long_fields=[A[0],A[3],pi]
H=sp.hessian(INs, long_fields)
print("  longitudinal (A0,A3,pi) Hessian H(omega,kappa):"); sp.pprint(sp.simplify(H))
# integrate out A0,A3 (they are the constraint/multiplier vector comps); reduced pi kinetic operator
eqs=[sp.diff(INs,A[0]), sp.diff(INs,A[3])]
sol=sp.solve(eqs,[A[0],A[3]],dict=True)
if sol:
    Lpi=sp.expand(INs.subs(sol[0]))
    Lpi=sp.expand(Lpi.subs({A[1]:0,A[2]:0}))
    print("  after integrating out A0,A3: effective L(pi) =", sp.factor(sp.simplify(Lpi)))
    # order in derivatives = degree in (w,kap); healthy=2, ghost=4 or 6
    poly=sp.Poly(sp.simplify(Lpi), w, kap) if Lpi!=0 else None
    if Lpi==0:
        print("  => effective pi Lagrangian VANISHES on the ghost-free subspace (helicity-0 fully constrained).")
    else:
        deg=sp.total_degree(sp.numer(sp.together(Lpi)), w, kap)
        print("  => effective pi kinetic term is degree", deg, "in (omega,kappa):",
              "HEALTHY (2)" if deg==2 else f"HIGHER-DERIVATIVE ghost ({deg})" if deg and deg>2 else "check")
else:
    print("  (A0,A3 not both solvable -- they carry genuine kinetic terms; helicity-1 or mixed dynamics)")
