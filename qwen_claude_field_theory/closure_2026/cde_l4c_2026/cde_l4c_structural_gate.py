#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cde_l4c_structural_gate.py -- structural gates for CDE-L4C MOND (Cuscuton DE + Laplacian 4-constraint MOND).
Checks the load-bearing STRUCTURAL claims (each can fail); the full 4x4 Dirac closure with inverse-designed
C_2,3,4 is the owed heavy follow-on and is flagged NOT-COMPUTED, not asserted.
GATES:
  1. F(y) correction (Einstein supplies Newtonian y^2, so MOND ADDS F with (y^2+F)'/2y = mu):
     F'(y) = -2 y e^{-y},  F(y)=2(1+y)e^{-y}+C,  1 + F'/2y = 1 - e^{-y} = mu.  Deep-MOND cubic; GR recovery.
  2. Velocity-freeness of the MOND term: y = c^2 |D_i lnN| / a0(chi) has NO time derivative (spatial gradient
     of lnN + algebraic chi), so a0^2(chi)F(y) adds ZERO to the kinetic Hessian -> cannot create a scalar graviton
     or a chi-kinetic term. (The key 'does a0(chi) spoil the DOF count' question.)
  3. Cuscuton claim audit: a finite large-velocity momentum asymptote is not an inhomogeneous primary constraint. The full coupled
     cuscuton/gravity Dirac chain is required; algebraic a0(chi) only leaves its Hessian unchanged.
  4. No-slip weak field: C_slip = 3R - 4 D^2 lnN -> (4/c^2) nabla^2 (Psi - Phi); =0 on FLRW automatically.
  5. a0 promotion: a0^2(chi)=G V(chi)/4 -> a0 = (1/2) c sqrt(G rho_Lambda) when V=rho_Lambda c^2; a0(z) ~ sqrt(rho_DE).
"""
import sympy as sp, sys
P=lambda *a: print(*a, flush=True); FAILS=[]
def check(n, ok, d=''):
    P(f"  [{'PASS' if ok else 'FAIL'}] {n}"+(f"  ({d})" if d else ''))
    if not ok: FAILS.append(n)
y=sp.symbols('y', positive=True); C=sp.symbols('C', real=True)

P("="*74); P("GATE 1: the F(y) correction (no Newtonian double-counting)"); P("="*74)
Fp = -2*y*sp.exp(-y)                       # proposed F'(y)
Fy = 2*(1+y)*sp.exp(-y) + C                 # proposed F(y)
check("F(y)=2(1+y)e^{-y}+C integrates F'=-2y e^{-y}", sp.simplify(sp.diff(Fy,y)-Fp)==0)
mu = 1 + Fp/(2*y)                           # Einstein Newtonian (1) + correction
check("1 + F'/(2y) = mu = 1 - e^{-y}", sp.simplify(mu-(1-sp.exp(-y)))==0, f"got {sp.simplify(mu)}")
# full primitive Einstein+MOND = y^2 + F ; check G(y)=y^2+2(1+y)e^{-y}-2 recovered at C=-2 and G'/2y=mu
Gtot = y**2 + Fy.subs(C,-2)
check("y^2 + F(C=-2) = the exact primitive G(y)=y^2+2(1+y)e^{-y}-2", sp.simplify(Gtot-(y**2+2*(1+y)*sp.exp(-y)-2))==0)
check("G'(y)/(2y) = mu", sp.simplify(sp.diff(Gtot,y)/(2*y)-(1-sp.exp(-y)))==0)
deep = sp.series(Gtot, y, 0, 5).removeO()
c3 = deep.coeff(y,3); c2 = deep.coeff(y,2)
check("deep-MOND: Newtonian y^2 CANCELS, leading term is cubic (2/3)y^3 (AQUAL |gradPhi|^3)", c2==0 and c3==sp.Rational(2,3), f"y^2 coeff={c2}, y^3 coeff={c3}")
check("GR recovery: F'(y)->0 exponentially at large y (mu->1)", sp.limit(Fp, y, sp.oo)==0 and sp.limit(mu,y,sp.oo)==1)

P(""); P("="*74); P("GATE 2: velocity-freeness of the MOND term (structural)"); P("="*74)
t=sp.symbols('t'); N=sp.Function('N'); chi=sp.Function('chi')
lnN=sp.Function('lnN'); a0chi=sp.Function('a0')
# y symbol depends on SPATIAL gradient of lnN and algebraically on chi via a0(chi): build a token and check no t-derivative
c=sp.symbols('c',positive=True); DlnN=sp.symbols('DlnN', positive=True)   # |D_i lnN|, a SPATIAL scalar (no t-deriv)
a0v=sp.Function('a0')(chi(t))
y_expr = c**2 * DlnN / a0v
dy_dNdot = sp.diff(y_expr, sp.Derivative(N(t), t))
dy_dchidot = sp.diff(y_expr, sp.Derivative(chi(t), t))
check("y has NO d/dt(N) dependence (spatial gradient only)", dy_dNdot==0)
check("y has NO d/dt(chi) dependence (chi enters only algebraically via a0(chi))", dy_dchidot==0)
P("  => the MOND Lagrangian a0^2(chi)F(y) is velocity-free: it contributes 0 to the kinetic Hessian,")
P("     so it cannot add a propagating scalar graviton nor a chi-kinetic term. (structural, SOLID)")

P(""); P("="*74); P("GATE 3 CORRECTION: a momentum asymptote is not a primary constraint"); P("="*74)
# Include the ADM measure N: L_c = N mu_c^2 sqrt(chidot^2/N^2-(Dchi)^2).
muc, Dchi2 = sp.symbols('mu_c Dchi2', positive=True); chidot, Nv = sp.symbols('chidot N', positive=True)
Lc = Nv*muc**2*sp.sqrt(chidot**2/Nv**2 - Dchi2)
p_chi = sp.diff(Lc, chidot)
Hess = sp.simplify(sp.diff(p_chi, chidot))
p_chi_limit = sp.limit(p_chi, chidot, sp.oo)
check("correct ADM cuscuton momentum has large-velocity limit p_chi=mu_c^2",
      p_chi_limit == muc**2, f"lim p_chi = {sp.simplify(p_chi_limit)}")
check("inhomogeneous Hessian is NONZERO for Dchi2>0 (no primary from this variable alone)",
      Hess != 0, f"Hessian={Hess}")
margin=sp.symbols('margin', positive=True)
p_near_null=sp.simplify(p_chi.subs(chidot, Nv*sp.sqrt(Dchi2+margin**2)))
check("p_chi is not globally bounded: it diverges at the null boundary",
      sp.limit(p_near_null, margin, 0, dir='+').is_infinite,
      f"lim={sp.limit(p_near_null, margin, 0, dir='+')}")
check("homogeneous Dchi2=0 branch alone has zero Hessian",
      sp.simplify(Hess.subs(Dchi2,0)) == 0)
# a0^2(chi) coupling has NO chidot -> adds nothing to p_chi or the Hessian
a0sq = sp.Function('a0sq')(sp.symbols('chi_'))
check("a0^2(chi) coupling contributes 0 to d/d(chidot) (algebraic in chi, no chidot)",
      sp.diff(a0sq, chidot)==0)
P("  => a0(chi) adds no velocity term, but the inhomogeneous cuscuton Hessian remains nonzero.")
P("     Standard cuscuton nonpropagation, if retained, must follow from the FULL coupled Dirac chain.")
P("     It is NOT certified by a finite asymptote or by this one-variable Hessian.")

P(""); P("="*74); P("GATE 4: no-slip weak field  C_slip = 3R - 4 D^2 lnN -> (4/c^2) lap(Psi-Phi)"); P("="*74)
x1,x2,x3=sp.symbols('x1 x2 x3', real=True); Psi=sp.Function('Psi'); Phi=sp.Function('Phi')
epsp=sp.symbols('epsp', positive=True)   # linear-order bookkeeping
# gamma_ij = (1 - 2 Psi/c^2) delta_ij ; compute 3R to linear order
Ps=Psi(x1,x2,x3)
g=sp.Matrix(3,3, lambda i,j: (1 - 2*epsp*Ps/c**2)*(1 if i==j else 0))
gi=g.inv()
def christ(a,b,cc):
    return sp.Rational(1,2)*sum(gi[a,d]*(sp.diff(g[d,b],[x1,x2,x3][cc])+sp.diff(g[d,cc],[x1,x2,x3][b])-sp.diff(g[b,cc],[x1,x2,x3][d])) for d in range(3))
Ga=[[[christ(a,b,cc) for cc in range(3)] for b in range(3)] for a in range(3)]
X=[x1,x2,x3]
def Ric(b,cc):
    o=0
    for a in range(3):
        o+=sp.diff(Ga[a][b][cc],X[a])-sp.diff(Ga[a][a][cc],X[b])
        for e in range(3): o+=Ga[a][a][e]*Ga[e][b][cc]-Ga[a][b][e]*Ga[e][a][cc]
    return o
R3=sum(gi[b,cc]*Ric(b,cc) for b in range(3) for cc in range(3))
R3_lin=sp.expand(sp.series(R3, epsp, 0, 2).removeO()).coeff(epsp,1)
lap=lambda f: sum(sp.diff(f,xx,2) for xx in X)
check("3R (linear) = (4/c^2) nabla^2 Psi", sp.simplify(R3_lin - 4*lap(Ps)/c**2)==0, f"got {sp.simplify(R3_lin)}")
# D^2 lnN with lnN ~ Phi/c^2 : flat-space Laplacian at linear order
Ph=Phi(x1,x2,x3); D2lnN_lin = lap(Ph)/c**2
Cslip_lin = R3_lin - 4*D2lnN_lin
check("C_slip = 3R - 4 D^2 lnN -> (4/c^2) nabla^2 (Psi - Phi)", sp.simplify(Cslip_lin - 4*lap(Ps-Ph)/c**2)==0)
P("  => D^2 C_slip = 0 gives nabla^2(Psi-Phi)=0 => Phi=Psi for k!=0; and on FLRW (Psi=Phi=0, D_iN=0)")
P("     C_slip=0 automatically => does NOT freeze H. (SOLID weak-field; nonlinear completion owed)")

P(""); P("="*74); P("GATE 5: a0 promotion  a0^2(chi) = G V(chi)/4"); P("="*74)
G,rhoL,cc2,Lam,pi=sp.symbols('G rho_Lambda c Lambda pi', positive=True)
V=rhoL*cc2**2                          # V as energy density * c^2 (dimensions)
a0_from_V=sp.sqrt(G*V/4)               # = (1/2) c sqrt(G rho_Lambda) ?
check("a0=sqrt(G V/4) with V=rho_L c^2 gives (1/2) c sqrt(G rho_Lambda)",
      sp.simplify(a0_from_V - sp.Rational(1,2)*cc2*sp.sqrt(G*rhoL))==0, f"got {sp.simplify(a0_from_V)}")
# and c^2 sqrt(Lambda/32pi) with rho_Lambda = Lambda c^2/(8 pi G):
a0_lam=sp.Rational(1,2)*cc2*sp.sqrt(G*(Lam*cc2**2/(8*pi*G)))
check("= c^2 sqrt(Lambda/32pi)", sp.simplify(a0_lam - cc2**2*sp.sqrt(Lam/(32*pi)))==0)
P("  => a0(z) proportional to sqrt(V[chi(z)]) = sqrt(rho_DE(z)); NOT forced to be H(z) unless rho_DE ~ H^2.")

P(""); P("="*74); P("OWED (NOT-COMPUTED, flagged honestly):"); P("="*74)
P("  - The full Dirac matrix including the inhomogeneous cuscuton pair plus the four ACs.")
P("  - The existing 4x4 subsystem rank does NOT establish full-action N_grav=2.")
P("  - Then MOND+no-slip full field eqs (Gate B) and boosted PPN alpha_1,alpha_2,alpha_3 (Gate C).")
P("  - PREDICTION (to be tested, NOT assumed): being a preferred-foliation theory with an elliptic (Laplacian)")
P("    k!=0 constraint, alpha_3 is the likely killer (DC-019/York wall). The Laplacian trick fixes FLRW, not instantaneity.")
P(""); P("STRUCTURAL DIAGNOSTICS:", "REPRODUCED; FULL DOF CERTIFICATION OPEN" if not FAILS else f"FAILED {FAILS}")
sys.exit(1 if FAILS else 0)
