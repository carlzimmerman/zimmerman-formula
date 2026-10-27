"""CE-FM-060: exact static stiffness residual, not solution or mode error."""
import json,sys,math
from pathlib import Path
import sympy as s
import numpy as np
x,l=s.symbols('x ell',positive=True);U=2/(1+s.sqrt(1+4*x*x))
lap=s.diff(U,x,2)+2*s.diff(U,x)/x-2*U/x**2
R=l*l*(1+8*x*x)/(1+4*x*x)**s.Rational(3,2)
checks=[]
def exact(n,e):
    assert s.simplify(e)==0,(n,e)
    checks.append(n)
exact('canonical residual operator',-l*l*x*x*lap/2-R)
exact('small radius residual',s.limit(R,x,0)-l*l)
exact('large radius coefficient',s.limit(x*R,x,s.oo)-l*l)
exact('ratio derivative',s.diff(R,x)-4*l*l*x*(1-8*x*x)/(1+4*x*x)**s.Rational(5,2))
peak=1/s.sqrt(8)
exact('global residual maximum',R.subs(x,peak)-4*s.sqrt(6)*l*l/9)
# All positive: squared comparisons are equivalent and exact.
for xx,thr,sign in [(10,s.Rational(9,100),1),(99,s.Rational(1,100),1),(100,s.Rational(1,100),-1)]:
    diff=s.simplify((R.subs({x:xx,l:1}))**2-thr**2)
    assert sign*diff>0;checks.append('exact residual comparison x='+str(xx))
b=Path('argon_push/AG4_law_from_action');a=json.loads((b/'ag4_derive_results.json').read_text())
xx=np.logspace(-3,1.7,200)
for row in a['G4_rows']:
    ell=row['Ldim'];mask=xx>=10*ell**2
    vals=ell**2*(1+8*xx**2)/(1+4*xx**2)**1.5
    got=float(vals[mask].max())
    assert math.isclose(got,row['max_ratio_ge10rs'],rel_tol=1e-8);checks.append('stored sampled maximum '+str(ell))
assert a['gates']['G4'] is False and a['gate_pass'] is False;checks.append('failed gate remains failed')
rows=[{'x':v,'ratio_for_ell1':float(R.subs({x:v,l:1}))} for v in [1,3,10,99,100]]
res={'claim_id':'CE-FM-060','checks_passed':len(checks),'checks':checks,'exact_ratio':'ell^2*(1+8*x^2)/(1+4*x^2)^(3/2)','global_max_coefficient':float(4*s.sqrt(6)/9),'ell1_controls':rows,'stored_G4_rows':a['G4_rows'],'scope':'Static force-equation residual evaluated on gamma=0 profile; no finite-gamma boundary solution, field-error bound or dynamic mode result.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
