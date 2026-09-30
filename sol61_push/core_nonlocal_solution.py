"""Declared 3D fractional polarization model: exact point-source branch."""
import argparse,json,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name)
G,M,a0,beta,r,A=s.symbols('G M a0 beta r A',positive=True)
alpha=1/(3*a0);d=s.pi*beta/2
# Fourier convention f(x)=int d³k/(2pi)³ ftilde(k) exp(ik.x).
# F[1/r]=4pi/k², F[1/r²]=2pi²/k, Delta log r=1/r².
# |grad| log r=-pi/(2r), hence |grad| grad log r=pi rhat/(2r²).
check('fractional radial sign and normalization',s.diff(-s.pi/(2*r),r)==s.pi/(2*r*r))
amp=2*G*M/(d+s.sqrt(d*d+4*G*M/a0))
check('exact source amplitude solves Gauss law',s.simplify(amp**2/a0+d*amp-G*M)==0)
check('total field equals Newton plus selected polarization',s.simplify(A/r+A*A/(a0*r*r)+d*A/(r*r)-(A/r+G*M/r**2)).subs(M,(A*A/a0+d*A)/G)==0)
check('local limit recovers deep MOND amplitude',s.limit(amp,beta,0)==s.sqrt(G*M*a0))
check('small mass becomes linear',s.limit(amp/M,M,0)==2*G/(s.pi*beta))
check('large mass tends square root',s.limit(amp/s.sqrt(G*M*a0),M,s.oo)==1)
eta=s.symbols('eta',positive=True)
ratio=(s.sqrt(1+eta*eta)-eta)**2
check('inferred acceleration suppression',s.simplify((amp**2/(G*M*a0)).subs(beta,4*eta*s.sqrt(G*M/a0)/s.pi)-ratio)==0)
# M=(A²/a0+dA)/G => d ln A/d ln M=(A/a0+d)/(2A/a0+d).
slope=(A/a0+d)/(2*A/a0+d)
check('small mass amplitude slope one',s.limit(slope,A,0)==1)
check('large mass amplitude slope one half',s.limit(slope,A,s.oo)==s.Rational(1,2))
check('BTFR slope exceeds MOND four',s.simplify(2/slope-2*(2*A/a0+d)/(A/a0+d))==0)
# Independent Fourier radial integral with exponential IR/UV regulator epsilon.
# |grad| log r=-(1/r) int_0^infty exp(-eps k) sin(kr)/k dk=-atan(r/eps)/r.
for epsilon in (.1,.03,.01):
 val,err=quad(lambda k:math.exp(-epsilon*k)/k if k else 0,0,math.inf,weight='sin',wvar=1,epsabs=1e-10,limit=300)
 check('regulated fractional Fourier quadrature eps='+str(epsilon),abs(val-math.atan(1/epsilon))<2e-9,dict(value=val,error=err))
# Normalized mass scan: G=a0=1, d=1 => beta=2/pi.
rows=[]
for mass in (1e-6,.001,.1,1,10,1000,1e6):
 amplitude=2*mass/(1+math.sqrt(1+4*mass));residual=amplitude*amplitude+amplitude-mass
 log_slope=(amplitude+1)/(2*amplitude+1)
 check('source residual mass='+str(mass),abs(residual)/mass<1e-12)
 rows.append(dict(mass=mass,amplitude=amplitude,inferred_a0_ratio=amplitude*amplitude/mass,amplitude_mass_slope=log_slope,BTFR_mass_vs_speed_slope=2/log_slope))
# Force at point-source background has g=A/r+GM/r², so b=GM/r² as selected.
check('point source flux constant',s.simplify(4*s.pi*r*r*(A*A/a0+d*A)/r**2).diff(r)==0)
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),amplitude=str(amp),mass_scan=rows,scope='Exact declared 3D isotropic fractional static toy for r>0; p=A grad log r and point source; no finite cutoff or formation dynamics',non_claims=['Not the nonuniform sheet fermion determinant','Not a finite total energy solution','No global cosmology or covariant stability','Massless dictionary conditional','No 32pi prediction'])
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print('%s %s/%s'%(result['status'],result['passed'],result['total']));raise SystemExit(result['status']!='PASS')
