#!/usr/bin/env python3
"""
wf_flat_validation.py  (v2 -- Euler-Lagrange route, unambiguous dispersion)
---------------------------------------------------------------------------
VALIDATE the ADM machinery against Bonetti-Barausse PRD 91,084053.
Pure khronometric high-acceleration limit: acceleration term = alpha a_i a^i
(f=alpha a^2), expanded about MINKOWSKI (isotropic scalar).

Method: build 2nd-order Lagrangian L2(phi,B,Psi); get exact Euler-Lagrange
equations (sympy.euler_equations); substitute plane wave exp(i(k z - w t));
dispersion = det(coefficient matrix)=0.  This is free of Hermitian-kernel
sign ambiguities.

Compare c_s^2 to BB Eq(14):
   c_s^2 = (alpha-2)(beta_BB+lambda)/[alpha(beta_BB-1)(2+beta_BB+3lambda)]
   c_t^2 = 1/(1-beta_BB)
with candidate (1+beta)K_ijK^ij  =>  beta_cand = -beta_BB.
"""
import sympy as sp
from sympy.calculus.euler import euler_equations

t,zz = sp.symbols('t zz', real=True)
beta,lam,alpha = sp.symbols('beta lambda alpha', real=True)
phi=sp.Function('phi'); B=sp.Function('B'); Psi=sp.Function('Psi')
ph=phi(t,zz); Bb=B(t,zz); Ps=Psi(t,zz)
dt=lambda f: sp.diff(f,t); dz=lambda f: sp.diff(f,zz)

# K_ij^(1) = dPsi/dt delta_ij - d_i d_j B  (only zz second-deriv of B nonzero)
K1={}
for i in 'xyz':
  for j in 'xyz':
    d2B = dz(dz(Bb)) if (i=='z' and j=='z') else 0
    K1[(i,j)]=(dt(Ps) if i==j else 0)-d2B
KK=sum(K1[(i,j)]**2 for i in 'xyz' for j in 'xyz')
Ktr=sum(K1[(i,i)] for i in 'xyz')
Ksec=(1+beta)*KK-(1+lam)*Ktr**2
# (3)R sector
R3_1=-4*dz(dz(Ps)); R3_2=8*Ps*dz(dz(Ps))-2*dz(Ps)**2
Rsec=R3_2+(ph+3*Ps)*R3_1
# acceleration alpha a_i a^i, a_i=d_i phi
Asec=alpha*(dz(ph))**2
L2=sp.expand(Ksec+Rsec+Asec)

# Euler-Lagrange equations for phi, B, Psi
eqs=euler_equations(L2,[ph,Bb,Ps],[t,zz])
eqs=[sp.expand(e.lhs-e.rhs) if isinstance(e,sp.Equality) else sp.expand(e) for e in eqs]

# plane-wave substitution
k,w=sp.symbols('k omega',real=True)
P0,B0,S0=sp.symbols('P0 B0 S0')
I=sp.I
def planewave(expr):
    # replace fields and derivatives by amplitude*(i k)^m (-i w)^n
    reps={}
    for F,amp in [(ph,P0),(Bb,B0),(Ps,S0)]:
        # all derivatives up to order 4
        for a in range(5):
            for b in range(5):
                if a+b==0:
                    reps[F]=amp
                else:
                    d=F
                    if a: d=sp.Derivative(F,(t,a)) if a>1 else sp.Derivative(F,t)
                    # build mixed derivative properly
        # simpler: use replace on Derivative nodes below
    return expr
def pw(expr):
    expr=sp.expand(expr)
    def rep(node):
        if isinstance(node,sp.Derivative):
            base=node.expr; amp={ph:P0,Bb:B0,Ps:S0}[base]; m=1
            for v,n in node.variable_count:
                if v==t: m*=(-I*w)**n
                elif v==zz: m*=(I*k)**n
            return amp*m
        return node
    # apply to all Derivative subexpressions
    expr=expr.replace(lambda e: isinstance(e,sp.Derivative), rep)
    expr=expr.subs({ph:P0,Bb:B0,Ps:S0})
    return sp.expand(expr)

rows=[pw(e) for e in eqs]
Mmat=sp.Matrix([[sp.simplify(sp.diff(r,amp)) for amp in (P0,B0,S0)] for r in rows])
print("EL coefficient matrix (rows: EOM phi,B,Psi ; cols: P0,B0,S0):")
sp.pprint(Mmat)
Ddet=sp.simplify(Mmat.det())
w2=sp.symbols('w2',real=True)
Dw2=sp.expand(Ddet.subs(w,sp.sqrt(w2)))
Pw2=sp.Poly(Dw2,w2)
print("\ndet degree in w2:",Pw2.degree())
# physical branch: nonzero w2 root
roots=sp.solve(sp.Eq(Ddet,0),w)
# instead factor det and pick w^2 ~ k^2 branch
Dfact=sp.factor(Ddet)
print("det(M) factored:")
print(Dfact)
# solve for w^2
sol=sp.solve(sp.Eq(Ddet,0),w2) if Pw2.degree()>=1 else []
# Get c_s^2 from the branch proportional to k^2
csq=None
# Extract: write Ddet = A2*w^4 + A1*w^2 + A0 (in w2). The scalar branch:
Pw2c=sp.Poly(sp.expand(Ddet.subs(w,sp.sqrt(w2))),w2)
coeffs={m[0]:c for m,c in Pw2c.terms()}
print("\nw2-polynomial coeffs:",{kk:sp.factor(vv) for kk,vv in coeffs.items()})
if set(coeffs.keys())=={0,1}:
    w2sol=sp.simplify(-coeffs[0]/coeffs[1])
    csq=sp.simplify(w2sol/k**2)
    print("\nc_s^2 (candidate conv) =",sp.factor(csq))
    bBB=sp.symbols('beta_BB',real=True)
    cs_BB=sp.factor(csq.subs(beta,-bBB))
    print("c_s^2 in BB conv (beta->-beta_BB) =",cs_BB)
    BB14=(alpha-2)*(bBB+lam)/(alpha*(bBB-1)*(2+bBB+3*lam))
    print("BB Eq(14)                         =",sp.factor(BB14))
    print("MATCH (difference==0)?",sp.simplify(cs_BB-BB14)==0)
    print("ratio:",sp.simplify(cs_BB/BB14))
else:
    print("Unexpected w2 structure; coeffs keys:",coeffs.keys())
