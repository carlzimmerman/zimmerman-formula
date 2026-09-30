"""Uniform-background one-loop kernel; no nonuniform galaxy solution."""
import argparse,json,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
q,m=s.symbols('q m',positive=True);checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail))
I=s.atan(q/(2*m))/(4*s.pi*q)
# Four-band trace dimension=4, coupling y=1; subtract q=0 value.
longitudinal=s.simplify(2*((q*q+4*m*m)*I-4*m*m/(8*s.pi*m)))
transverse=2*q*q*I
check('longitudinal massless limit',s.limit(longitudinal,m,0)==q/4)
check('transverse massless limit',s.limit(transverse,m,0)==q/4)
check('longitudinal derivative limit',s.limit(longitudinal/q**2,q,0)==1/(6*s.pi*m))
check('transverse derivative limit',s.limit(transverse/q**2,q,0)==1/(4*s.pi*m))
rows=[]
for ratio in (.01,.1,1,10,100):
 mass=1.;momentum=ratio
 numeric=quad(lambda x:1/(8*math.pi*math.sqrt(mass*mass+x*(1-x)*momentum*momentum)),0,1,epsabs=1e-12,epsrel=1e-12)[0]
 exact=math.atan(momentum/(2*mass))/(4*math.pi*momentum)
 check('Feynman parameter bubble q/m='+str(ratio),abs(numeric-exact)<1e-12)
 l=float(longitudinal.subs({m:mass,q:momentum}));t=float(transverse.subs({m:mass,q:momentum}))
 check('both momentum corrections positive q/m='+str(ratio),l>0 and t>0)
 rows.append(dict(q_over_m=ratio,longitudinal=l,transverse=t,bubble_error=abs(numeric-exact)))
result=dict(status='PASS' if all(x['passed'] for x in checks) else 'FAIL',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,rows=rows,longitudinal=str(longitudinal),transverse=str(transverse),scope='One four-band flavor, y=1, zero temperature, static q, uniform nonzero mass; q=0 curvature subtracted. Multiply by flavor count and y² for polarization vertices.',non_claims=['No nonuniform determinant or galaxy force solution','No sheet formation or vacuum energy selection','No 32pi solution'])
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print('%s %s/%s'%(result['status'],result['passed'],result['total']));raise SystemExit(result['status']!='PASS')
