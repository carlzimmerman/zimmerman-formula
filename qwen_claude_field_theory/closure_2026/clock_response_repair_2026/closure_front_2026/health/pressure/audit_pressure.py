#!/usr/bin/env python3
"""Independent arbitrary-lapse homogeneous variation and L206 counterterm audit."""
import importlib.util
from pathlib import Path
import sympy as S

checks=[]
def eq(name,lhs,rhs=0):
    residual=S.simplify(lhs-rhs)
    assert residual==0,(name,residual)
    checks.append(name);print('PASS',name)

a,N,ad,add,v,vd,td,tdd,Nd,g,tau=S.symbols('a N adot addot chidot chiddot taudot tauddot Ndot gamma tau', real=True)
x=S.symbols('X',real=True)
P=S.Function('P')(x,tau);V=S.Function('V')(tau);W=S.Function('W0')(tau)
Q=v/N;H=ad/(a*N);clock=td/N;Qdot=(vd*N-v*Nd)/N**3
p=P.subs(x,Q**2);px=S.diff(P,x).subs(x,Q**2)
def dt(expr):
    return sum(S.diff(expr,z)*zd for z,zd in ((a,ad),(ad,add),(N,Nd),(v,vd),(td,tdd),(tau,td)))
L=N*a**3*(p-V)+a**3*td*W-2*g*a**2*ad*v**3/N**3
rho=-S.diff(L,N)/a**3
pressure=(S.diff(L,a)-dt(S.diff(L,ad)))/(3*N*a**2)
current=S.diff(L,v)/a**3
clock_eq=(S.diff(L,tau)-dt(S.diff(L,td)))/(N*a**3)
eq('arbitrary lapse variation density',rho,2*Q**2*px-p+V-6*g*H*Q**3)
eq('arbitrary lapse scale variation pressure',pressure,p-V+clock*W+2*g*Q**2*Qdot)
eq('arbitrary lapse velocity variation current',current,2*Q*px-6*g*H*Q**2)
eq('clock Euler equation independent of clock rate',clock_eq,S.diff(P,tau).subs(x,Q**2)-S.diff(V,tau)-3*H*W)
# Raw gamma X Box chi = -gamma a^3 Q^2 Q_t -3gamma a^2 adot Q^3.
raw=-g*a**3*Q**2*dt(Q)-3*g*a**2*ad*Q**3
boundary=dt(-g*a**3*Q**3/3)
eq('cubic integration by parts with arbitrary lapse',raw-boundary,-2*g*a**2*ad*Q**3)

U,d,q,qp,h,hb,s,mrel,w,Qd,A=S.symbols('U d q qprime H Href s mrel w Qdot A',real=True)
margin=U-2*d*q**2
PX=U*d/margin+3*g*q*hb
W0=U-2*g*q**2*qp
rho_branch=2*q*q*PX+U-6*g*h*q**3
j_branch=2*q*PX-6*g*h*q*q
p_branch=-U+s*W0+2*g*q*q*Qd
eq('pressure retains chain residual before tracking substitution',p_branch,U*(s-1)+2*g*q*q*(Qd-s*qp))
eq('tracking chain rule cancels cubic pressure exactly',p_branch.subs(Qd,s*qp),U*(s-1))
eq('actual H distinct from reference density',rho_branch,U**2/margin+6*g*q**3*(hb-h))
eq('actual H distinct from reference current',j_branch,2*q*U*d/margin+6*g*q**2*(hb-h))
eq('L206 pressure missing W counterterm',U*(s-1)+2*g*q*q*Qd-p_branch,2*g*s*q*q*qp)
eq('proper reference reconstruction clock equation',(-2*q*qp*PX-(-A*qp-3*hb*U)-3*h*W0).subs(A,2*q*U*d/margin),3*(hb-h)*W0)
eq('tracked conserved reference current forces clock match',s*(-3*hb*A)+3*hb*A,3*hb*A*(1-s))
eq('corrected equation of state solved',S.solve(S.Eq(w*U/mrel,U*(s-1)),s)[0],1+w/mrel)

# Read-only evaluation of the canonical implementation, at frozen coefficients.
root=Path(__file__).resolve().parents[6]
source=root/'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py'
spec=importlib.util.spec_from_file_location('pressure_constitutive',source)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
model=module.Model(.02,gamma=1e-6)
charge_expr=2*q*U*d/(U-2*d*q*q)
charge_partial=S.lambdify((q,U,d),[S.diff(charge_expr,z) for z in (q,U,d)],'numpy')
for t in (0.,.01,.02):
    b=model.background(t);jets=model.jets(t,b['q']**2,0.)
    actual_A=2*b['q']*b['U']*b['d']/(b['U']-2*b['d']*b['q']**2)
    Aprime=sum(float(c)*float(z) for c,z in zip(charge_partial(b['q'],b['U'],b['d']),b['raw'][5:8]))
    Uprime=float(b['raw'][6])
    charge_residual=Aprime+3*b['H']*actual_A
    U_residual=Uprime+actual_A*b['qdot']+3*b['H']*b['U']
    assert abs(charge_residual)<1e-13 and abs(U_residual)<1e-13
    checks.extend(['canonical charge derivative identity','canonical U derivative identity'])
    print('PASS canonical derivative identities',t,'charge',charge_residual,'U',U_residual)
    for rate in (1.,1.2):
        proper_qdot=rate*b['qdot']
        actual=jets['P']-jets['V']+rate*jets['W']+2*model.gamma*b['q']**2*proper_qdot
        expected=b['U']*(rate-1)
        assert abs(actual-expected)<1e-13
        print('PASS canonical jets pressure',t,rate,'residual',actual-expected)
        checks.append('canonical jets pressure')
    assert abs(jets['W']-(b['U']-2*model.gamma*b['q']**2*b['qdot']))<1e-14
    checks.append('canonical W0 counterterm')
t=.01;eps=1e-6
numeric=(model.background(t+eps)['q']-model.background(t-eps)['q'])/(2*eps)
analytic=model.background(t)['qdot']
assert abs(numeric-analytic)<1e-8
checks.append('coefficient argument derivative numeric check')
print('PASS coefficient argument derivative',numeric,analytic)
print('ALL',len(checks),'CHECKS PASSED')
