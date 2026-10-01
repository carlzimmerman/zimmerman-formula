"""b04: Horndeski with a constant vacuum background: the Babichev-Charmousis theory  L = zeta R - eta (dphi)^2 + beta G^{mn} phi_m phi_n - 2 zeta Lb
(zeta,eta,beta constants; phi = q t + psi(r)).  Reduced action in (A,B,psi) with J^r = dL/dpsi' = 0 (the tr equation).
Claims checked symbolically on the explicit field equations:
 (H1) A=B=f= 1 - mu/r - Le r^2/3 with Le = -eta/beta  and  q^2 = (zeta eta + beta zeta Lb)/(beta eta)  [BC relation, convention here: bare term -2 zeta Lb]  solves all three equations
      with  psi' = +- (q/f) sqrt(1-f)... (checked) -> EXACT SdS form (K2 applies): kappa, r_h, Lambda_e obey 1-2 kappa r_h = Le r_h^2 for every coupling.
 (H2) Le is fixed by the ratio -eta/beta, independent of the bare Lb (self-tuning of the vacuum), so Lambda_e IS a free dimensionful ratio of couplings; T needs Le r_h^2=8pi and kappa r_h=1/2
      simultaneously, still impossible (K2).
 (H3) negative control: a metric A=f, B=f(1+eps) with eps != 0 is not a solution.
"""
import sympy as sp, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
r=sp.symbols('r',positive=True); t,th,ph=sp.symbols('t theta phi'); X=[t,r,th,ph]
A=sp.Function('A')(r); B=sp.Function('B')(r); psi=sp.Function('psi')(r)
zeta,eta,beta,Lb,q,mu=sp.symbols('zeta eta beta Lambda_b q mu')
g=sp.diag(-A,1/B,r**2,r**2*sp.sin(th)**2); gi=g.inv()
Gam=lambda a,b,c: sum(gi[a,d]*(sp.diff(g[d,b],X[c])+sp.diff(g[d,c],X[b])-sp.diff(g[b,c],X[d])) for d in range(4))/2
def Ric(b,c): return sp.simplify(sum(sp.diff(Gam(a,b,c),X[a])-sp.diff(Gam(a,b,a),X[c])+sum(Gam(a,a,d)*Gam(d,b,c)-Gam(a,c,d)*Gam(d,b,a) for d in range(4)) for a in range(4)))
Rm=sp.Matrix(4,4,lambda i,j:Ric(i,j) if i==j else 0); Rs=sp.simplify(sum(gi[i,i]*Rm[i,i] for i in range(4)))
Gmn=lambda i,j: Rm[i,j]-g[i,j]*Rs/2
Gtt_up=gi[0,0]**2*Gmn(0,0); Grr_up=gi[1,1]**2*Gmn(1,1)
sqrtg=sp.sqrt(A/B)*r**2   # sin(theta) stripped
phi_t=q; phi_r=sp.diff(psi,r)
kin=gi[0,0]*phi_t**2+gi[1,1]*phi_r**2
L=sqrtg*(zeta*Rs-eta*kin+beta*(Gtt_up*phi_t**2+Grr_up*phi_r**2)-2*zeta*Lb)
from sympy.calculus.euler import euler_equations
eqs=euler_equations(L,[A,B,psi],r)
EA,EB,Epsi=[e.lhs for e in eqs]
Jr=sp.diff(L,sp.diff(psi,r))
Le=-eta/beta
f=1-mu/r-Le*r**2/3
q2=(zeta*eta+beta*zeta*Lb)/(beta*eta)
psip=sp.sqrt(q2)/f*sp.sqrt(1-f)*sp.sign(1)   # BC branch (+)
def evalres(e,fA=f,fB=f,pp=psip):
    e=e.subs(sp.Derivative(psi,r),pp) if False else e
    return e
def subst(e,fA,fB,pp):
    e=e.subs(q,sp.sqrt(q2))
    e=e.subs(sp.Derivative(psi,(r,2)),sp.diff(pp,r)).subs(sp.Derivative(psi,r),pp)
    e=e.subs({A:fA,B:fB}).doit()
    return e
import random
vals={zeta:1,eta:sp.Rational(3,7),beta:sp.Rational(5,3),Lb:sp.Rational(2,5),mu:sp.Rational(1,3)}
def numres(e,fA,fB,pp):
    ee=subst(e,fA,fB,pp).subs(vals)
    return [sp.N(ee.subs(r,x),30) for x in (sp.Rational(7,5),sp.Rational(5,2),4)]
# the (A,B) variation equations contain psi' only via psi'^2 (and q^2): use psip^2 exactly
for nm,e in (("E_A (vary g_tt)",EA),("E_B (vary g_rr)",EB),("J^r=dL/dpsi'",Jr)):
    res=numres(e,f,f,psip)
    chk("H1 %s vanishes on the stealth SdS solution (residuals %s)"%(nm,["%.1e"%abs(x) for x in res]), all(abs(x)<1e-20 for x in res))
Epsi_res=numres(Epsi,f,f,psip)
chk("H1 psi equation vanishes (residuals %s)"%["%.1e"%abs(x) for x in Epsi_res], all(abs(x)<1e-20 for x in Epsi_res))
# H3 control: B != A  (and wrong q^2, wrong Le)
fB2=f*(1+sp.Rational(1,10))
bad=[numres(e,f,fB2,psip) for e in (EA,EB,Jr)]
chk("H3 control: B=1.1 A is NOT a solution (some residual > 1e-3)", any(abs(x)>1e-3 for res in bad for x in res))
f_wrong=1-mu/r-(-Le)*r**2/3
badL=[numres(e,f_wrong,f_wrong,psip) for e in (EA,EB,Jr)]
chk("H3 control: sign-flipped Lambda_e = +eta/beta is NOT a solution", any(abs(x)>1e-3 for res in badL for x in res))
q2w=sp.Symbol('q2w')
vals2=dict(vals)
psip_w=sp.sqrt(q2*sp.Rational(11,10))/f*sp.sqrt(1-f)
# wrong q^2 : subst uses q2 for q; emulate by changing q symbol separately
def numres_q(e,qval):
    ee=e.subs(q,qval)
    ee=ee.subs(sp.Derivative(psi,(r,2)),sp.diff(psip,r)).subs(sp.Derivative(psi,r),psip).subs({A:f,B:f}).doit().subs(vals)
    return [sp.N(ee.subs(r,x),30) for x in (sp.Rational(7,5),sp.Rational(5,2),4)]
badq=[numres_q(e,sp.sqrt(q2)*sp.Rational(11,10)) for e in (EA,EB,Jr)]
chk("H3 control: q^2 off by 21% is NOT a solution", any(abs(x)>1e-3 for res in badq for x in res))
# H2: Lambda_e independent of Lb
chk("H2 Lambda_e = -eta/beta does not contain the bare Lambda_b; Lb only sets q^2", sp.diff(Le,Lb)==0 and sp.diff(q2,Lb)!=0)
# K2 consequence
rh=sp.symbols('r_h',positive=True); Mh=sp.solve(f.subs(r,rh),mu)[0]
kap=sp.simplify((sp.diff(f,r)/2).subs(mu,Mh).subs(r,rh))
chk("H1 horizon relation: 2 kappa r_h = 1 - Lambda_e r_h^2 with Lambda_e=-eta/beta (K2): T=(1/2,8 pi) impossible for every eta,beta,zeta,Lb", sp.simplify(2*kap*rh-(1-Le*rh**2))==0 and sp.solve([sp.Eq(2*kap*rh,1),sp.Eq(Le*rh**2,8*sp.pi)],[eta],dict=True)==[])
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
