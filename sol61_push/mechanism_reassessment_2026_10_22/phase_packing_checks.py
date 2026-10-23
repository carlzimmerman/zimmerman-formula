import json,sys
from pathlib import Path
import sympy as s
from phase_packing_response import model
base=Path(__file__).parent
inputs=json.load(open(base/'cold_limit_run/results.json'))['rows']
rows=[]
for r in inputs:
 out=model(r['A'],r['Psi_c'],1,tol=2e-13,gamma=.01)
 rows.append(dict(A=r['A'],mass=out['mass'],status=out['status'],integrals=out['integrals']))
fmax,V,rho=s.symbols('fmax V rho',positive=True)
mass=4*s.pi*fmax*V**3/3;twoT=4*s.pi*fmax*V**5/5
checks={'ball_bound':s.simplify(twoT.subs(V,(3*rho/(4*s.pi*fmax))**s.Rational(1,3))-s.Rational(3,5)*(3/(4*s.pi*fmax))**s.Rational(2,3)*rho**s.Rational(5,3))==0}
checks['mass']=all(r['status']=='edge' and abs(r['mass']-1)<1e-5 for r in rows)
checks['virial']=all(v['virial_relative_error']<1e-5 for r in rows for v in r['integrals'])
checks['packing']=all(v['packing_ratio']>=1-1e-10 for r in rows for v in r['integrals'])
checks['quadrature_refinement']=all(max(abs(r['integrals'][0][k]/r['integrals'][1][k]-1) for k in ['twoT','force_virial','packing_bound_twoT'])<1e-5 for r in rows)
for row in rows:
 for v in row['integrals']:
  v['minimum_required_fmax']=v['fmax']/v['packing_ratio']**1.5
checks={k:bool(v) for k,v in checks.items()}
out=dict(rows=rows,checks=checks,all_pass=all(checks.values()),scope='necessary occupation/virial bound, no primordial phase-space density assumed')
with open(sys.argv[1],'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
