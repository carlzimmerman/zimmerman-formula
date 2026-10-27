import argparse,json
from pathlib import Path
import sympy as s
from scipy.optimize import brentq

p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
e,q,q0,mu=s.symbols('e q q0 mu',positive=True)
V=e**2/(2*q)+mu**2*(q-q0)**2/2
H=s.hessian(V,(e,q))
checks=[]
def ck(name,ok,value):
    checks.append(dict(name=name,passed=bool(ok),value=str(value)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(value))
ck('joint_hessian_determinant',s.simplify(H.det()-mu**2/q)==0,s.factor(H.det()))
ck('equilibrium_softens',s.simplify(s.diff(V,q)-(mu**2*(q-q0)-e**2/(2*q**2)))==0,s.diff(V,q))
dqde=s.factor(-s.diff(V,q,e)/s.diff(V,q,2))
ck('implicit_response',s.simplify(dqde-e*q/(e**2+mu**2*q**3))==0,dqde)
rows=[]
for ev in [0,.1,1,10,100]:
    qv=brentq(lambda q:q-1-ev**2/(2*q*q),1,1000)
    av=1/qv
    rows.append(dict(mismatch=ev,susceptibility=qv,stiffness=av))
ck('passive_stiffness_order',all(r['stiffness']>=1 for r in rows) if args.mutate else all(r['stiffness']<=1 for r in rows),rows)
result=dict(status='checks_passed' if all(c['passed'] for c in checks) else 'checks_failed',checks=checks,rows=rows,
            non_claims=['No phase selector','No covariant parent','No exclusion of externally driven or metastable states'])
path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=2)+'\n')
print(f"CHECKS {sum(c['passed'] for c in checks)}/{len(checks)}")
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
