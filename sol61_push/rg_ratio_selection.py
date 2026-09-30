"""Scoped one-loop GNY ratio selection; no MOND or gravity identification."""
import argparse,json,math
from pathlib import Path
import sympy as s
from scipy.integrate import solve_ivp

p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
checks=[]
def check(name,passed,details=None):
    checks.append(dict(name=name,passed=bool(passed),details=details))
N,Y,L,r=s.symbols('N Y L r',positive=True)
loop=16*s.pi**2
betaY=(N+6)*Y**2/loop
betaL=(3*L**2+2*N*Y*L-12*N*Y**2)/loop
P=3*r**2+(N-6)*r-12*N
check('ratio beta derived from both coupling betas',s.simplify((betaL/Y-L*betaY/Y**2).subs(L,r*Y)-Y*P/loop)==0)
rp=(6-N+s.sqrt(N**2+132*N+36))/6
check('positive root solves ratio polynomial',s.simplify(P.subs(r,rp))==0)
check('polynomial at upper bound 12 is positive constant',s.expand(P.subs(r,12))==360)
check('polynomial at zero negative for N positive',P.subs(r,0)==-12*N)
check('four dimensional nonzero Yukawa fixed point absent',s.simplify(betaY/Y**2)==(N+6)/loop)
rows=[]
for n in (4,8,40,400):
    root=float(rp.subs(N,n));minus=(6-n-math.sqrt(n*n+132*n+36))/6
    check('root bounds N='+str(n),0<root<12,root)
    for initial in (.5,10.):
        y0=.05
        def rhs(t,state):
            yy,ll=state
            return [(n+6)*yy*yy/(16*math.pi**2),(3*ll*ll+2*n*yy*ll-12*n*yy*yy)/(16*math.pi**2)]
        sol=solve_ivp(rhs,(0,-100000),[y0,initial*y0],method='DOP853',rtol=2e-11,atol=2e-13)
        yy,ll=sol.y[:,-1];u=math.log(y0/yy)
        z=(initial-root)/(initial-minus)*math.exp(-3*(root-minus)*u/(n+6))
        predicted=(root-z*minus)/(1-z)
        err=abs(ll/yy-predicted)
        exactY=y0/(1+(n+6)*y0*100000/(16*math.pi**2))
        check('direct coupling integration versus analytic ratio N=%s initial=%s'%(n,initial),sol.success and err<2e-8 and abs(yy-exactY)/exactY<2e-8 and min(sol.y.flatten())>0,dict(error=err,u=u,final_ratio=ll/yy))
        check('infrared distance decreases N=%s initial=%s'%(n,initial),abs(ll/yy-root)<abs(initial-root))
        rows.append(dict(N=n,Nf=n/4,initial_ratio=initial,final_ratio=ll/yy,selected_ratio=root,u=u,hypothetical_C_xi_one_sixth=root/4,xi_required_for_32pi=root/(768*math.pi)))
check('fixed ratio does not fix gravity coefficient',s.diff(r/(24*s.Symbol('xi',positive=True)),s.Symbol('xi',positive=True))==-r/(24*s.Symbol('xi',positive=True)**2))
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),rows=rows,source='https://arxiv.org/html/1607.05316v3 equations 1.4 and 2.1; one-loop terms only',ratio_polynomial=str(P),scope='Independent massless flat-space GNY model at d=4. Positive quartic/Yukawa infrared ratio; full couplings approach Gaussian fixed point.',non_claims=['Not beta functions of shared_scale_closure.py','No derived MOND acceleration','No nonminimal gravitational running','No nonzero d=4 interacting fixed point','No 32pi prediction'],hypothetical_dictionary='lambda_vac=lambda4/24, gamma=y, fixed xi: C=r/(24xi); xi=1/6 is illustrative, not a conformal selection')
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print('%s: %s/%s checks'%(result['status'],result['passed'],result['total']))
raise SystemExit(0 if result['status']=='PASS' else 1)
