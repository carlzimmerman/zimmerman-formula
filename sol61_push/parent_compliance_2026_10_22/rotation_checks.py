import argparse,json
from pathlib import Path
import sympy as s
import numpy as np

pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--mutate',action='store_true');args=pa.parse_args()
q,I0,b,J,mu,q0,e,v,w,M=s.symbols('q I0 b J mu q0 e v w M',positive=True)
I=I0+b/q
V=mu**2*(q-q0)**2/2+e**2/(2*q)
L=I*v*v/2+M*w*w/2-V
R=s.simplify((L-J*v).subs(v,J/I))
E=J*J/(2*I)+V
checks=[]
def ck(name,ok,value):
    checks.append(dict(name=name,passed=bool(ok),value=str(value)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(value))
ck('fixed_J_routh',s.simplify(R-(M*w*w/2-E))==0,R)
ck('positive_kinetic_hessian',s.simplify(s.hessian(L,(v,w)).det()-M*I)==0,M*I)
drive=s.factor(s.diff(E,q).subs(q,q0))
ck('stiffening_condition',s.simplify(drive-(J*J*b/(2*(I0*q0+b)**2)-e*e/(2*q0*q0)))==0,drive)
rows=[]
for j in [0,1,3]:
    En=E.subs({I0:1,b:1,J:j,mu:1,q0:1,e:s.Rational(1,10)})
    deriv=s.factor(s.diff(En,q));poly=s.Poly(s.together(deriv).as_numer_denom()[0],q)
    roots=s.polys.polytools.intervals(poly,eps=s.Rational(1,10**12))
    positives=[(a,bb,mult) for (a,bb),mult in roots if a>0]
    ck('positive_root_count_J'+str(j),len(positives)==1 and positives[0][2]==1,positives)
    root=float((positives[0][0]+positives[0][1])/2)
    curvature=float(s.diff(En,q,2).subs(q,root))
    row=dict(J=j,chi=root,stiffness=1/root,curvature=curvature,
             inertia=1+1/root,angular_velocity=j/(1+1/root),
             inertia_change_from_chi0=(1+1/root)/2-1,
             energy_at_equilibrium=float(En.subs(q,root)),
             energy_at_chi0=float(En.subs(q,1)))
    rows.append(row)
    ck('stable_J'+str(j),curvature>0 and row['energy_at_equilibrium']<=row['energy_at_chi0']+1e-12,row)
order=rows[0]['chi']>1 and rows[2]['chi']<rows[1]['chi']<1
ck('rotational_stiffening',not order if args.mutate else order,[(r['J'],r['chi']) for r in rows])
res=dict(status='checks_passed' if all(c['passed'] for c in checks) else 'checks_failed',checks=checks,rows=rows,
         non_claims=['Dimensionless toy only','New coupling b is not derived','No covariant or observational validation',
                     'No dissipation: a minimum is not an attractor'])
path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(res,indent=2)+'\n')
print(f"CHECKS {sum(c['passed'] for c in checks)}/{len(checks)}")
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
