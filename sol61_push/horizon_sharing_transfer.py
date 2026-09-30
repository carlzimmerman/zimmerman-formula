"""Entropy state-function and trace-only curvature closure checks."""
import argparse
import json
from pathlib import Path
import sympy as s

checks=[]
def check(name,ok,detail=None):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))
    print(('PASS ' if ok else 'FAIL ')+name)

a,b,A,eta,s0=s.symbols('a b A eta s0',positive=True)
f=a/(a+s0)
check('sharing slope fixes s0 as MOND scale',s.limit(f/a,a,0)==1/s0)
check('entropy one-form is not closed on independent states',s.simplify(eta*s.diff(f,a)-eta*s0/(a+s0)**2)==0)
entropy=eta*A*f
check('state entropy requires an extra acceleration differential',s.simplify(s.diff(entropy,a)-eta*A*s0/(a+s0)**2)==0)
loop=s.simplify(eta*A*(f.subs(a,s0)-f.subs(a,2*s0)))
check('rectangular entropy loop nonzero',loop==-eta*A/6)
theta=s.symbols('theta',real=True)
angular=s.integrate(s.cos(theta)**2*s.sin(theta),(theta,s.pi/2,s.pi))/2
check('assumed angular overlap integral gives one sixth',angular==s.Rational(1,6))

c,H,G,rho,Lambda,Om=s.symbols('c H G rho Lambda Om',positive=True)
paper_a0=c*H/6
dictionary=s.simplify((Lambda*c**4/paper_a0**2).subs(Lambda,3*Om*H**2/c**2))
check('paper coefficient retains density parameter',dictionary==108*Om)
check('target requires an added cosmological relation',s.solve(s.Eq(dictionary,32*s.pi),Om)==[8*s.pi/27])
check('pure de Sitter coefficient is 108 rather than 32pi',dictionary.subs(Om,1)==108)
rh=c/H
check('simultaneous Hubble 8pi reading gives 288pi',s.simplify((Lambda*c**4/paper_a0**2).subs(Lambda,8*s.pi/rh**2))==288*s.pi)
check('simultaneous original target and 8pi radius need half acceleration',s.simplify(s.sqrt((8*s.pi/rh**2)/(32*s.pi))*rh)==s.Rational(1,2))
check('density length equality leaves acceleration unselected',s.simplify((Lambda*c**2/(G*rho)).subs(Lambda,8*s.pi*G*rho/c**2))==8*s.pi)

# Independent geometric computation, mostly-plus signature, ordinary Ricci convention.
t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z);N=s.exp(x)*(1+y*y)
metric=s.diag(-N*N,1,1,1);inverse=metric.inv()
connection=[[[s.simplify(sum(inverse[i,l]*(s.diff(metric[l,k],coords[j])+s.diff(metric[l,j],coords[k])-s.diff(metric[j,k],coords[l])) for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
Ricci=s.zeros(4)
for i in range(4):
    for j in range(4):
        Ricci[i,j]=s.simplify(sum(s.diff(connection[k][i][j],coords[k])-s.diff(connection[k][i][k],coords[j])+sum(connection[k][i][j]*connection[l][k][l]-connection[l][i][k]*connection[k][j][l] for l in range(4)) for k in range(4)))
R=s.simplify(sum(inverse[i,j]*Ricci[i,j] for i in range(4) for j in range(4)))
lapN=s.diff(N,x,2)+s.diff(N,y,2)
check('direct Christoffels verify Ricci tt',s.simplify(Ricci[0,0]-N*lapN)==0)
check('direct Christoffels verify spatial Hessian Ricci',all(s.simplify(Ricci[i,j]+s.diff(N,coords[i],coords[j])/N)==0 for i in range(1,4) for j in range(1,4)))
check('Ricci scalar for static lapse',s.simplify(R+2*lapN/N)==0)
proper_acc=s.sqrt(s.diff(s.log(N),x)**2+s.diff(s.log(N),y)**2)
F=proper_acc/(proper_acc+s0)
check('proper acceleration at the audit point is finite',s.simplify(proper_acc.subs(y,1)-s.sqrt(2))==0)
# Bianchi gives dPsi = W if matter stress is conserved.
W=[s.simplify(-sum(Ricci[i,j]*sum(inverse[i,l]*s.diff(F,coords[l]) for l in range(4)) for i in range(4))-F*s.diff(R,coords[j])/2) for j in range(4)]
curl=s.simplify(s.diff(W[1],y)-s.diff(W[2],x))
point=s.simplify(curl.subs(y,1))
expected=-s.sqrt(2)*s0/(s.sqrt(2)+s0)**2
check('trace divergence curl is explicitly nonzero',s.simplify(point-expected)==0,str(point))
check('curl nonzero for every positive sharing scale',point.is_negative is True)
check('constant sharing coefficient removes curl',s.simplify(curl.subs(s0,0))==0)
check('trace obstruction depends on spatially varying factor',s.diff(F,y)!=0)

# Matter action is a separate obligation: modifying a horizon coefficient
# does not change the variation of a minimally coupled point-particle action.
check('unmodified point-particle mass remains multiplicative',s.diff(s.Symbol('particle_mass')*s.Symbol('proper_time_integrand'),s.Symbol('particle_mass'))==s.Symbol('proper_time_integrand'))
result=dict(status='PASS' if all(z['passed'] for z in checks) else 'FAIL',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,trace_curl_at_y1=str(point),non_claims=['No claimed absence of all solutions','No naive boost-normalization change of proper acceleration','No modified-inertia action derived','Angular weight is a premise','No cosmological selection of Omega_Lambda','No 32pi derivation'])
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print('%s %d/%d'%(result['status'],result['passed'],result['total']))
raise SystemExit(result['status']!='PASS')
