#!/usr/bin/env python3
"""
wf_adm_scalar_reduction.py  (v2 -- Euler-Lagrange, validated machinery)
-----------------------------------------------------------------------
Quadratic khronon action of the candidate around a locally-constant static MOND
background  a_i = g \hat z, y0 = g/a0, in unitary gauge.  EL + plane-wave dispersion.

Action density: L = N sqrt(g3)[ (3)R + (1+beta)K_ijK^ij - (1+lambda)K^2 + a0^2 W(a/a0) ].
Perturbations: N=exp(phi), N_i=d_iB, gamma_ij=exp(2Psi)delta_ij; fields of (t,x,z).
Background W-data symbolic: W0=W(y0), W1=W'(y0), W2=W''(y0), mu=W1/y0.

Outputs the exact anisotropic dispersion omega^2(kx,kz) and the propagating
speeds cs_par^2 (kz, along a), cs_perp^2 (kx, transverse). Machinery validated in
wf_flat_validation.py against Bonetti-Barausse PRD91,084053 Eq.(14).
"""
import sympy as sp
from sympy.calculus.euler import euler_equations

t,xx,zz=sp.symbols('t xx zz',real=True)
beta,lam,a0=sp.symbols('beta lambda a0',real=True)
y0=sp.symbols('y0',positive=True)
W0,W1,W2=sp.symbols('W0 W1 W2',real=True)
g=a0*y0
phi=sp.Function('phi'); B=sp.Function('B'); Psi=sp.Function('Psi')
ph=phi(t,xx,zz); Bb=B(t,xx,zz); Ps=Psi(t,xx,zz)
dt=lambda f: sp.diff(f,t); dx=lambda f: sp.diff(f,xx); dz=lambda f: sp.diff(f,zz)

# --- K-sector (2nd order): K_ij^(1)=dPsi/dt delta_ij - d_i d_j B ---
def dd(i,j,f):
    D={'x':dx,'y':(lambda q:0),'z':dz}; return D[i](D[j](f))
K1={(i,j):((dt(Ps) if i==j else 0)-dd(i,j,Bb)) for i in 'xyz' for j in 'xyz'}
KK=sum(K1[(i,j)]**2 for i in 'xyz' for j in 'xyz')
Ktr=sum(K1[(i,i)] for i in 'xyz')
Ksec=(1+beta)*KK-(1+lam)*Ktr**2

# --- (3)R-sector (2nd order) with measure exp(phi+3Psi) ---
lap=lambda f: dx(dx(f))+dz(dz(f))
R3_1=-4*lap(Ps); R3_2=8*Ps*lap(Ps)-2*(dx(Ps)**2+dz(Ps)**2)
Rsec=R3_2+(ph+3*Ps)*R3_1

# --- acceleration sector (2nd order), a_i=g\hat z + d_i phi, gamma^ij=e^-2Psi ---
a2_1=2*g*dz(ph)-2*g**2*Ps
a2_2=dx(ph)**2+dz(ph)**2-4*g*Ps*dz(ph)+2*g**2*Ps**2
delta_1=a2_1/(2*g*a0)
delta_2=a2_2/(2*g*a0)-a2_1**2/(8*g**3*a0)
W_eps1=W1*delta_1
W_eps2=W1*delta_2+sp.Rational(1,2)*W2*delta_1**2
Accel=a0**2*(W_eps2+(ph+3*Ps)*W_eps1+(ph+3*Ps)**2*sp.Rational(1,2)*W0)

L2=sp.expand(Ksec+Rsec+Accel)

# --- Euler-Lagrange eqs ---
eqs=euler_equations(L2,[ph,Bb,Ps],[t,xx,zz])
eqs=[sp.expand(e.lhs-e.rhs) for e in eqs]

# --- plane wave exp(i(kx x + kz z - w t)) ---
kx,kz,w=sp.symbols('k_x k_z omega',real=True); I=sp.I
P0,B0,S0=sp.symbols('P0 B0 S0')
amp={ph:P0,Bb:B0,Ps:S0}
def pw(expr):
    expr=sp.expand(expr)
    def rep(node):
        if isinstance(node,sp.Derivative):
            m=1
            for v,n in node.variable_count:
                if v==t: m*=(-I*w)**n
                elif v==xx: m*=(I*kx)**n
                elif v==zz: m*=(I*kz)**n
            return amp[node.expr]*m
        return node
    return sp.expand(expr.replace(lambda e:isinstance(e,sp.Derivative),rep).subs(amp))
rows=[pw(e) for e in eqs]
M=sp.Matrix([[sp.simplify(sp.diff(r,a)) for a in (P0,B0,S0)] for r in rows])
Ddet=sp.simplify(sp.expand(M.det()))
w2=sp.symbols('w2',real=True)
Pw2=sp.Poly(sp.expand(Ddet.subs(w,sp.sqrt(w2))),w2)
print("det degree in w2:",Pw2.degree())
cf={m[0]:sp.factor(c) for m,c in Pw2.terms()}
for kk in sorted(cf): print("  (w2)^%d coeff:"%kk, cf[kk])

D0=cf.get(0,0); D1=cf.get(1,0)
w2sol=sp.simplify(-D0/D1)
print("\nomega^2(kx,kz) = -D0/D1 =")
w2sol=sp.simplify(sp.cancel(w2sol))
sp.pprint(w2sol)

# ---- extract speeds: propagating (UV) coefficients of kz^2, kx^2 ----
# Full dispersion may carry a W0 background 'mass'. The propagating gradient/kinetic
# structure is the k^2 -to- w^2 ratio. Read speeds two ways:
print("\n============ SPEEDS ============")
# (A) small-k with W0 kept: omega^2 = mass + c^2 k^2 ; c^2 = d(omega^2)/d(k^2)|_{k->0}
for label,other in [('PAR (kz, kx=0)',{kx:0}),('PERP (kx, kz=0)',{kz:0})]:
    expr=sp.simplify(w2sol.subs(other))
    kk = kz if 'PAR' in label else kx
    # series in kk about 0
    ser=sp.series(expr,kk,0,3).removeO()
    mass=sp.simplify(ser.subs(kk,0))
    c2=sp.simplify(sp.diff(ser,kk,2)/2)
    print("\n%s :"%label)
    print("   gap(omega^2 at k=0) =",sp.factor(mass))
    print("   d(omega^2)/d(k^2)|0 =",sp.factor(c2))

# (B) W0=0 isolation (background-subtracted propagating sector)
print("\n---- W0=0 (background-subtracted propagating sector) ----")
w2s0=sp.simplify(w2sol.subs(W0,0))
for label,other in [('PAR',{kx:0}),('PERP',{kz:0})]:
    expr=sp.simplify(w2s0.subs(other))
    kk=kz if label=='PAR' else kx
    c2=sp.simplify(sp.cancel(expr/kk**2))
    print("  cs_%s^2 ="%label, sp.factor(c2))

import pickle
pickle.dump({'w2sol':sp.srepr(w2sol),'Ddet':sp.srepr(Ddet)},open('adm_mond.pkl','wb'))
print("\nsaved adm_mond.pkl")
