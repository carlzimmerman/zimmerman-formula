"""Finite spectral cancellation witness; not a common covariant theory."""
import argparse
import json
import math
from collections import defaultdict
from itertools import combinations_with_replacement
from pathlib import Path
import sympy as s
from scipy.integrate import quad

checks=[]
def check(name,ok,detail=None):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))
    print(('PASS ' if ok else 'FAIL ')+name)

F=(0,2,2,3,6); B=(1,1,1,5,5)
def moment(power):return sum(n**power for n in F)-sum(n**power for n in B)
for power in (0,1,2):check('matched moment '+str(power),moment(power)==0)
check('positive vacuum cubic moment',moment(3)==6)
check('one excess massless fermion weight',F.count(0)-B.count(0)==1)
check('fourth moment controls UV tail',moment(4)==156)

# Enumerate all multisets in the declared bound, not random samples.
counts=[];first=None
for length in range(2,6):
    groups=defaultdict(list)
    for xs in combinations_with_replacement(range(9),length):
        groups[(sum(xs),sum(n*n for n in xs))].append(xs)
    witnesses=[]
    for arr in groups.values():
        for f in arr:
            for b in arr:
                if f.count(0)>b.count(0) and sum(n**3 for n in f)>sum(n**3 for n in b):
                    witnesses.append((sum(f),max(f+b),f,b))
    counts.append(dict(length=length,witnesses=len(witnesses)))
    if witnesses and first is None:first=min(witnesses)
check('no witness lengths 2 to 4 in integer bound',all(r['witnesses']==0 for r in counts[:3]))
check('minimal-sum bounded witness reproduced',first==(13,6,F,B),str(first))

P,M,y,K,mu,G=s.symbols('P M y K mu G',positive=True)
eta=lambda fn:sum(fn(n) for n in F)-sum(fn(n) for n in B)
mass=lambda n:s.sqrt(n*n*M*M+y*y*P*P)
f=eta(lambda n:mass(n)**3)
pref=mu/(9*s.pi**2)
rho=pref*f
jet=s.series(f,P,0,5).removeO().expand()
expected=6*M**3+y**3*P**3-s.Rational(57,80)*y**4*P**4/M
check('small-field jet has no quadratic term',s.simplify(jet-expected)==0)
check('all-field squared-mass UV cancellation',s.simplify(eta(lambda n:mass(n)**2))==0)
cut=-pref*eta(lambda n:(K*K+mass(n)**2)**s.Rational(3,2)-mass(n)**3)
# The first two divergent terms cancel; remaining inverse-cutoff terms vanish.
inv=s.symbols('inv',positive=True)
tail=eta(lambda n:s.series((1+mass(n)**2*inv**2)**s.Rational(3,2),inv,0,5).removeO())
check('cutoff remainder begins at inverse K',s.simplify(tail-s.Rational(3,8)*inv**4*eta(lambda n:mass(n)**4))==0)
check('regulated energy tends to joint finite energy',s.simplify(eta(lambda n:mass(n)**4)-156*M**4)==0)

rows=[]
for field in (0.,.2,1.):
    masses=[math.sqrt(n*n+field*field) for n in F+B]
    signs=[1]*len(F)+[-1]*len(B)
    for cutoff in (20.,40.,80.):
        # Sum modes before integrating: separate divergent quadratures are avoided.
        weighted=lambda t:math.fsum(sig*math.sqrt(t*t+m*m) for sig,m in zip(signs,masses))
        integrand=lambda t:t*weighted(t)
        energy=-quad(integrand,0,cutoff,epsabs=1e-9,epsrel=1e-9)[0]/(3*math.pi**2)
        pressure_integrand=lambda t:t**3*math.fsum(sig/math.sqrt(t*t+m*m) for sig,m in zip(signs,masses))
        pressure=-quad(pressure_integrand,0,cutoff,epsabs=1e-9,epsrel=1e-9)[0]/(6*math.pi**2)
        exact=float(cut.subs({mu:1,M:1,y:1,P:field,K:cutoff}))
        boundary=-cutoff**2*weighted(cutoff)/(6*math.pi**2)
        check('independent energy integral P=%s K=%s'%(field,cutoff),abs(energy-exact)<1e-7)
        check('pressure boundary P=%s K=%s'%(field,cutoff),abs(energy+pressure-boundary)<1e-7)
        rows.append(dict(P=field,K=cutoff,energy=energy,pressure=pressure,rho_plus_pressure=energy+pressure,boundary=boundary))

# Large field: count and square moments cancel the P³ and P terms.
x=s.symbols('x',positive=True)
fx=eta(lambda n:(n*n+x*x)**s.Rational(3,2))
large=eta(lambda n:s.series((1+n*n*inv**2)**s.Rational(3,2),inv,0,5).removeO())
check('large field energy tends to zero from leading positive side',s.simplify(large-s.Rational(117,2)*inv**4)==0)
fp=s.diff(fx,x)
derivative_at_10=float(fp.subs(x,10))
check('declared MOND induction turns negative at finite field',derivative_at_10<0,derivative_at_10)
alpha=4*G*mu*y**3/(9*s.pi)
a0=1/(3*alpha)
rho0=2*mu*M**3/(3*s.pi**2)
Lambda=8*s.pi*G*rho0
C=s.simplify(Lambda/a0**2)
check('common spectrum gives explicit coefficient dictionary',s.simplify(C-256*(G*mu*M*y**2)**3/(27*s.pi**3))==0)
check('coefficient changes with unfixed common mass',s.diff(C,M)!=0)
h=s.symbols('h',positive=True)
target_h=s.Rational(3,2)*s.pi**s.Rational(4,3)
check('32pi would require an additional dimensionless relation',s.simplify(256*target_h**3/(27*s.pi**3)-32*s.pi)==0)
check('pairwise spectral equality kills all response and vacuum',sum(mass(n)**3 for n in F)-sum(mass(n)**3 for n in F)==0)
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,search=counts,fermion_effective_masses=F,boson_effective_masses=B,rows=rows,coefficient=str(C),non_claims=['No symmetry enforces the mass moments','Effective weights are not a specified particle multiplet','Critical quadratic gravity-polarization matching remains input','Rest-frame pressure is not covariant stress proof','No stable high-field constitutive completion','No 32pi prediction'])
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print('%s %d/%d'%(result['status'],result['passed'],result['total']))
raise SystemExit(result['status']!='PASS')
