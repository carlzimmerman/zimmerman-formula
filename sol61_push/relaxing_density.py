import argparse
import json
import math
import sympy as s
from scipy.optimize import brentq

checks=[]
def check(name, condition): checks.append({'name':name,'passed':bool(condition)})
A,B,K,G,q,P=s.symbols('A B K G q P',positive=True)
U=A/q**2+B*q**2
q0=(A/B)**s.Rational(1,4)
U0=2*s.sqrt(A*B)
check('vacuum stationarity',s.simplify(s.diff(U,q).subs(q,q0))==0)
check('positive vacuum minimum',s.simplify(U.subs(q,q0)-U0)==0)
check('vacuum stiffness',s.simplify(s.diff(U,q,2).subs(q,q0)-8*B)==0)
qprime=-3*K*P**2/s.diff(U,q,2)
bprime=12*s.pi*G*K*(2*P*q+P**2*qprime)
on_shell=s.simplify(bprime.subs(K*P**3,2*A/q**3-2*B*q))
expected=12*s.pi*G*K*P*(6*A/q**3+10*B*q)/s.diff(U,q,2)
check('monotonic force exact expression',s.simplify(on_shell-expected)==0)
a0=1/(12*s.pi*G*K*q0)
D3=(12*s.pi*G)**3*2*A*K**2
C0=s.simplify(8*s.pi*G*U0/a0**2)
check('proxy ratio bridge',s.simplify(C0-s.Rational(2,3)*D3)==0)
D=s.symbols('D',positive=True)
mu=D/(1+D)
check('Newton-calibrated bridge',s.simplify((s.Rational(2,3)*D**3)/mu**2-s.Rational(2,3)*D*(1+D)**2)==0)
shift=s.symbols('rho_constant',real=True)
check('independent vacuum shift changes ratio',s.diff(8*s.pi*G*(U0+shift)/a0**2,shift)==8*s.pi*G/a0**2)
pressure=-U+q*s.diff(U,q)/3
check('pressure at stationary density is minus energy',s.simplify((pressure+U).subs(q,q0))==0)
check('explicit pressure',s.simplify(pressure+5*A/(3*q**2)+B*q**2/3)==0)
H=s.symbols('H',positive=True)
check('expansion conservation',s.simplify(-H*q*s.diff(U,q)+3*H*(U+pressure))==0)
check('density stationarity not maintained in expansion',(-H*q0).is_negative)
eps,w=s.symbols('eps w',real=True)
moving_q=q*(1-eps**2*w**2)**s.Rational(1,6)
moving_L=-A/moving_q**2-B*moving_q**2
kinetic=s.expand(s.series(moving_L,eps,0,3).removeO()).coeff(eps,2)/w**2
check('direct determinant expansion kinetic coefficient',s.simplify(kinetic-q*s.diff(U,q)/6)==0)
check('kinetic equals half rho plus pressure',s.simplify(kinetic-(U+pressure)/2)==0)
check('stationary density has no phonon time kinetic',s.simplify(kinetic.subs(q,q0))==0)
check('kinetic sign around stationary density',kinetic.subs({A:1,B:1,q:s.Rational(1,2)})<0 and kinetic.subs({A:1,B:1,q:2})>0)

rows=[]
for av,bv,kv in ((0.5,0.25,0.1),(2.,3.,0.7)):
    gv=0.1
    initial=(av/bv)**0.25
    def density(p):
        u=kv*p**3/(2*bv*initial)
        return initial*brentq(lambda t:t**4+u*t**3-1,0,1,xtol=1e-15,rtol=1e-14)
    def force(p): return 12*math.pi*gv*kv*density(p)*p*p
    for pv in (1e-4,0.01,1.,10.,1e4):
        qv=density(pv)
        uv=kv*pv**3/(2*bv*initial)
        tv=qv/initial
        residual=abs(tv**4+uv*tv**3-1)
        check('density root '+str((av,bv,kv,pv)),residual<1e-9)
        stiffness=6*av/qv**4+2*bv
        slope=12*math.pi*gv*kv*pv*(6*av/qv**3+10*bv*qv)/stiffness
        step=pv*1e-5
        slope_fd=(force(pv+step)-force(pv-step))/(2*step)
        check('independent positive force slope '+str((av,bv,kv,pv)),slope>0 and abs(slope_fd/slope-1)<1e-5)
        rows.append({'A':av,'B':bv,'K':kv,'P':pv,'q':qv,'root_residual':residual,'force':force(pv),'force_slope':slope,'slope_relative_error':abs(slope_fd/slope-1)})
target_D=brentq(lambda d:d*(1+d)**2-48*math.pi,0,10)
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
result={'passed':all(c['passed'] for c in checks),'checks':checks,'rows':rows,'D_required_by_target_not_selected':target_D}
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
raise SystemExit(0 if result['passed'] else 1)
