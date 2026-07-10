#!/usr/bin/env python3
"""THE TWO DEFINED COMPUTATIONS of the written elastic-medium action (ELASTIC_MEDIUM_ACTION_2026):
(a) w from the action's second-order expansion around the galactic pre-strain, with the kappa
convention PINNED by the action's own boundary condition (strain=1 at the derived y_c=Z/2) and
the constitutive (S,f1) RECONSTRUCTED from the SPARC-required nu-shaped response; (b) the medium
Q2 = w x scalar-class (the banked verified mapping) vs the Cassini ceiling. Both footings."""
import numpy as np, sympy as sp
Z=float(np.sqrt(32*np.pi/3)); yc=Z/2
nu=lambda y: np.sqrt(1+1/y); numo=lambda y: nu(y)-1
# ---- (1) KAPPA PINNED by the action's boundary: eps(y)=kappa*(nu-1)*y, eps(y_c)=1
kappa=1.0/(numo(yc)*yc)
print(f"[1] kappa pinned by eps(y_c)=1 at y_c=Z/2={yc:.4f}:  kappa = {kappa:.4f}  (was the m1 lever, now fixed)")
# ---- (2) CONSTITUTIVE RECONSTRUCTION: driving linear in y (budget force), eps(y)=kappa*(nu-1)*y
# stress sigma(y) = Keff*y/yc-normalized (sigma=F'); parametric F'(eps), F''=dsig/deps
y=sp.symbols('y',positive=True); nus=sp.sqrt(1+1/y); eps_s=sp.nsimplify(kappa,rational=False)*(nus-1)*y
sig_s=y/yc                                   # F' in units of K_eff*const (norm cancels in ratios)
deps=sp.diff(eps_s,y); dsig=sp.diff(sig_s,y)
Fpp_over_Fp=lambda yy: float((dsig/deps/sig_s).subs(y,yy))   # F''/F' *(1) in eps-units
S_of=lambda yy: float((dsig/deps).subs(y,yy))/float((dsig/deps).subs(y,0.01))  # tangent stiffening vs deep
f1_of=lambda yy: float((sig_s/eps_s).subs(y,yy))/float((sig_s/eps_s).subs(y,0.01)) # secant vs deep
ebg=float(eps_s.subs(y,2.2)); q=float((sp.diff(sp.log(eps_s),sp.log(y)).doit() if False else (y/eps_s*deps)).subs(y,2.2))
print(f"[2] reconstruction at the Sun (y=2.2): eps_bg={ebg:.3f}, dln(eps)/dln(y)={q:.3f} (quench),")
print(f"    S(2.2)={S_of(2.2):.2f}, f1(2.2)={f1_of(2.2):.2f}  |  Q2-shell average (y=0.3..2.5):")
ys=np.linspace(0.3,2.5,23); Sbar=np.mean([S_of(v) for v in ys]); f1bar=np.mean([f1_of(v) for v in ys])
print(f"    S_shell={Sbar:.2f}, f1_shell={f1bar:.2f}   (Q2 sourced across the cancellation shell, 76% inside y~2)")
# ---- (3) EXACT det-Hessian l=2/l=0 ratio at the pre-strained state (sympy, no truncation)
t,dv,Fp,Fpp,mu=sp.symbols('t d F1 F2 mu',real=True,positive=False)
X=sp.MatrixSymbol('X',3,3)
M=sp.Matrix([[1+t/3+dv,0,0],[0,1+t/3-dv/2,0],[0,0,1+t/3-dv/2]])  # pre-strain: bulk t, deviator d (axisym)
Xs=sp.Matrix(3,3,lambda i,j:sp.Symbol(f'x{i}{j}'))
Xsym=(Xs+Xs.T)/2
detM=M.det(); Minv=M.inv()
d1=detM*sp.trace(Minv*Xsym)                                  # first variation of det
d2=detM*(sp.trace(Minv*Xsym)**2 - sp.trace(Minv*Xsym*Minv*Xsym))  # second variation (exact)
E2=sp.expand(Fp*d2/2 + Fpp*d1**2/2)                          # quadratic form in X (F-sector)
# probe = pure shear in the (1,2) plane vs (2,3) plane -> anisotropy from d
def coef(E,i,j):
    s=sp.Symbol(f'x{i}{j}'); return sp.diff(E,s,2)/2
A12=sp.simplify(coef(E2,0,1)); A23=sp.simplify(coef(E2,1,2)) # shear stiffness along vs across d
aniso=sp.simplify((A12-A23)); iso=sp.simplify((A12+A23)/2)
aniso1=sp.series(aniso,dv,0,2).removeO().coeff(dv,1)          # O(d) anisotropic coefficient
print("[3] exact det-Hessian: anisotropic shear-stiffness coeff (O(d)) =")
print("    ",sp.simplify(aniso1.subs(t,0)),"  [in units of F',F''; vanishes at d=0 as proven]")
# ---- (4) w: medium |l=2|/|l=0| over scalar reference, at the pinned/reconstructed values
def w_of(Sv,f1v,dJ,beta,scal_ref):
    Fpv=f1v; Fppv=Sv*(1-beta)                                # units of K_eff (campaign chain)
    an=abs(float(aniso1.subs({t:0,Fp:Fpv,Fpp:Fppv})))*abs(dJ)
    iso0=abs(float(iso.subs({t:0,dv:0,Fp:Fpv,Fpp:Fppv})))+3*beta   # + linear shear mu=3 beta Keff
    return (an/iso0)/scal_ref
dJ=-q*1.0/(3-q*1.0)                                          # p=1 flat-curve; d/J1=-q p/(3-q p)
print(f"[4] deviator d/J1 = {dJ:.4f} (p=1; p=2 doubles it)")
CEIL={"canon":(0.177,0.198),"alt":(0.160,0.172)}
for ref,lab in ((0.076,"scalar-ref=local-proxy"),(0.25,"scalar-ref=L0-edge")):
    for beta in (0.33,0.6,0.95):
        wv=w_of(Sbar,f1bar,dJ,beta,ref)
        wv22=w_of(S_of(2.2),f1_of(2.2),dJ,beta,ref)
        print(f"    {lab:24s} beta={beta:4.2f}:  w(shell)={wv:7.3f}   w(at-Sun)={wv22:7.3f}")
print(f"[5] GATE: w must be <= 0.177-0.198 (canonical) / 0.160-0.172 (alt).")
print(f"    Q2 = w x (2.0-2.4e-26 canon / 2.7-3.0e-26 alt) vs ceiling 5.2e-27 s^-2.")
print("exit 0")
