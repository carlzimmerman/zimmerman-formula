#!/usr/bin/env python3
"""
GROUND-B Part 1: rest-frame (w=0) reconstruction of the PUBLISHED AeST quadratic
action (arXiv:2109.13287) and verification of the 4 self-checks.
POSITION-SPACE Euler-Lagrange -> Fourier (sign-safe).

Blocks (published; spatial i,j = 1,2,3, flat delta-norm for the scalar sector;
Maxwell kept fully covariant so the transverse magnetic (grad beta)^2 appears):
   E_i  = F_{0i} = Adot_i - (1/2) d_i h00        (aether electric)
   B_i  = d_i phi + Q0 A_i                         (MOND "slip" vector)
   dQ   = A^mu d_mu phi - Q0 = phidot + (1/2)Q0 h00
   L2 = -(K_B/2)F_{mn}F^{mn}                        [electric K_B E^2 + magnetic]
        + 2(2-K_B) dij E_i B_j - (2-K_B)(1+lam_s) dij B_i B_j
        + 2 K2 (dQ)^2
Fields depend on (t,z); k along z; transverse polarizations a1,a2. Sig(-,+,+,+).
"""
import sympy as sp
KB,lam_s,Q0,K2 = sp.symbols('K_B lambda_s Q0 K2', real=True)
k,om,eps = sp.symbols('k omega eps', real=True)
t,z = sp.symbols('t z', real=True)
I = sp.I
eta = sp.diag(-1,1,1,1); ginv = sp.diag(-1,1,1,1)

a1=sp.Function('a1')(t,z); a2=sp.Function('a2')(t,z); a3=sp.Function('a3')(t,z)
vf=sp.Function('vf')(t,z); h00=sp.Function('h00')(t,z)
a0 = h00/2                       # aether unit-norm constraint, rest frame

def d(f,mu):
    if mu==0: return sp.diff(f,t)
    if mu==3: return sp.diff(f,z)
    return sp.Integer(0)

Aup=[1+eps*a0, eps*a1, eps*a2, eps*a3]
g=sp.Matrix(eta); g[0,0]=-1+eps*h00
Alow=[sum(g[m,n]*Aup[n] for n in range(4)) for m in range(4)]
dphi=[Q0+d(eps*vf,0),0,0,d(eps*vf,3)]

# covariant Maxwell
F=sp.Matrix(4,4, lambda nu,mu: d(Alow[mu],nu)-d(Alow[nu],mu))
Fup=ginv*F*ginv
Lmax=-(KB/2)*sum(F[m,n]*Fup[m,n] for m in range(4) for n in range(4))
# published scalar blocks (spatial delta-norm)
Ei=[F[0,i] for i in range(4)]                       # E_i = F_{0i}
Bi=[dphi[i]+Q0*Alow[i] for i in range(4)]           # B_i = d_i phi + Q0 A_i (lower)
EdotB=sum(Ei[i]*Bi[i] for i in range(1,4))          # delta^{ij} E_i B_j
B2   =sum(Bi[i]*Bi[i] for i in range(1,4))
dQ=sum(Aup[m]*dphi[m] for m in range(4))-Q0
Lscal=2*(2-KB)*EdotB-(2-KB)*(1+lam_s)*B2+2*K2*dQ**2
Lag=Lmax+Lscal
Lag2=sp.expand(sp.series(Lag,eps,0,3).removeO()).coeff(eps,2)
Lag2=sp.expand(Lag2)
print("quadratic Lagrangian built")

def EL(L,f):
    ft=sp.diff(f,t); fz=sp.diff(f,z)
    return sp.diff(L,f)-sp.diff(sp.diff(L,ft),t)-sp.diff(sp.diff(L,fz),z)
amps={a1:sp.Symbol('A1'),a2:sp.Symbol('A2'),a3:sp.Symbol('A3'),vf:sp.Symbol('V'),h00:sp.Symbol('H')}
ph=sp.exp(I*(k*z-om*t))
def fourier(expr):
    e=expr
    for f,A in amps.items(): e=e.subs(f,A*ph)
    e=sp.expand(e.doit())
    e=sp.simplify(e/ph)
    return sp.expand(e)
def eom_matrix(fu):
    rows=[]
    for f in fu:
        ef=fourier(EL(Lag2,f))
        rows.append([sp.expand(ef).coeff(amps[g_]) for g_ in fu])
    return sp.Matrix(rows)

print("="*66); print("SELF-CHECK 1  transverse a1"); print("="*66)
M1=eom_matrix([a1]); disp=sp.factor(M1[0,0])
tgt1=KB*(om**2-k**2)-(2-KB)*(1+lam_s)*Q0**2
print("EOM(a1) =",disp)
ok1=sp.simplify(disp-tgt1)==0 or sp.simplify(disp+tgt1)==0
print("match(+/-) ->",ok1,"  M^2=",sp.simplify((2-KB)*(1+lam_s)*Q0**2/KB))

print("="*66); print("SELF-CHECK 3  scalar c_s^2 (a3,vf; h00=0)"); print("="*66)
M3=eom_matrix([a3,vf]); det3=sp.factor(M3.det())
print("det(a3,vf) =",det3)
sols=sp.solve(sp.Eq(sp.expand(M3.det()),0),om**2)
cs2_t=sp.expand((2-KB)/(K2*KB)*(1+sp.Rational(1,2)*KB*lam_s))
print("c_s^2 target =",cs2_t)
for s in sols:
    s=sp.simplify(s)
    if s!=0:
        c=sp.simplify(sp.limit(s/k**2,k,sp.oo))
        print("  om^2=",sp.simplify(s)," coeff_k2=",c," MATCH->",sp.simplify(c-cs2_t)==0)

print("="*66); print("SELF-CHECK 2  full scalar determinant (a3,vf,h00)"); print("="*66)
M2=eom_matrix([a3,vf,h00]); det2=sp.factor(M2.det())
brace=(2-KB)*((2+KB*lam_s)*k**2+2*K2*Q0**2*(1+lam_s))-2*K2*KB*om**2
print("det(3x3) =",det2)
print("target brace =",sp.expand(brace))
print("det/brace =",sp.simplify(det2/brace))
