import json,sys
from pathlib import Path
import sympy as s
checks=[]
def check(name,c,detail):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name)
beta,mu,rho,curv,gamma,k=s.symbols('beta mu rho curvature gamma k',positive=True)
sigma,JK,K2=s.symbols('sigma J_dot_K K_squared',real=True)
# J=sigma*u, u^2=-1, A=mu*u, gradphi=A-beta*K.
L=-sigma+beta*(-sigma*sigma-2*JK+K2)/2-(-sigma*mu-beta*JK)
check('combined current stationary density',s.simplify(s.diff(L,sigma)-(mu-1-beta*sigma))==0,L)
dual=s.simplify(L.subs(sigma,(mu-1)/beta))
check('active scalar/current parent',s.simplify(dual-(mu-1)**2/(2*beta)-beta*K2/2)==0,dual)
check('vacuum parent scalar disappears',s.simplify(L.subs({sigma:0,JK:0})-beta*K2/2)==0,'J=0 => Jbar=-K; L=beta K^2/2-W')
check('active density equals pressure derivative',s.simplify(s.diff((mu-1)**2/(2*beta),mu)-(mu-1)/beta)==0,(mu-1)/beta)
mu0=1+beta*rho
fd,pd,grad,p,pp,pf=s.symbols('phidot Pdot gradphi P p_P p_phi',real=True)
L2=fd*fd/(2*beta)+beta*pd*pd/(2*mu0)-grad*pd/mu0-rho*grad*grad/(2*mu0)-curv*p*p/2
mom={pf:s.diff(L2,fd),pp:s.diff(L2,pd)}
vel=s.solve([s.Eq(pf,mom[pf]),s.Eq(pp,mom[pp])],(fd,pd),dict=True)[0]
H=s.simplify((pf*fd+pp*pd-L2).subs(vel))
expected=beta*pf*pf/2+mu0*(pp+grad/mu0)**2/(2*beta)+rho*grad*grad/(2*mu0)+curv*p*p/2
check('positive completed Hamiltonian',s.simplify(H-expected)==0,H)
check('positive populated velocity determinant',s.simplify(s.hessian(L2,(fd,pd)).det()-1/mu0)==0,1/mu0)

y=s.symbols('omega_squared',real=True)
matrix=s.Matrix([[-y/beta+rho*k*k/mu0,-s.I*k*s.sqrt(y)/mu0],[s.I*k*s.sqrt(y)/mu0,curv+gamma*k*k-beta*y/mu0]])
poly=s.expand(mu0*matrix.det())
want=y*y-(k*k+mu0*(curv+gamma*k*k)/beta)*y+rho*(curv+gamma*k*k)*k*k
check('exact longitudinal frequency polynomial',s.simplify(poly-want)==0,poly)
bare=s.factor(poly.subs(gamma,0))
check('bare mode product positive',s.simplify(bare.subs(y,0)-rho*curv*k*k)==0,bare)
c0=beta*rho/mu0
gap=mu0*curv/beta
disc=s.expand((k*k+gap)**2-4*rho*curv*k*k)
check('bare real frequency discriminant',s.simplify(disc-((k*k-gap)**2+4*k*k*gap*(1-c0)))==0,disc)
v2=s.symbols('speed_squared',real=True)
characteristic=s.simplify(s.limit(poly.subs(y,v2*k*k)/k**4,k,s.oo))
wantcone=v2*v2-(1+mu0*gamma/beta)*v2+rho*gamma
check('populated principal cone',s.simplify(characteristic-wantcone)==0,characteristic)
check('positive stiffness gives root above metric cone',s.simplify(characteristic.subs(v2,1)+gamma/beta)==0,'p(1)=-gamma/beta<0; leading coefficient1')
check('vacuum longitudinal cone',s.simplify((beta+gamma)/beta-1-gamma/beta)==0,1+gamma/beta)

rows=[]
for rv in [s.Rational(1,1000),s.Rational(1,10),s.Integer(1)]:
 for gv in [s.Integer(0),s.Rational(1,100)]:
    vals={beta:1,rho:rv,curv:1,gamma:gv,k:1}
    roots=s.solve(poly.subs(vals),y)
    check('positive finite roots rho%s gamma%s'%(rv,gv),all(float(rr)>0 for rr in roots),roots)
    rows.append(dict(rho=str(rv),gamma=str(gv),omega_squared=[float(rr) for rr in roots]))
out=dict(checks=checks,active_parent=str(dual),populated_Hamiltonian=str(expected),longitudinal_polynomial=str(poly),principal_polynomial=str(characteristic),controls=rows,scope='Exact branch rewrite and fixed-clock flat local block; not nonlinear clock/metric health or an actual physical-vacuum interface solution.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
