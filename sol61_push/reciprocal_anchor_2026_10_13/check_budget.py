import json,sys
from pathlib import Path
import sympy as s
eps,b,Ne,N,r,Q,M,delta=s.symbols('epsilon b N_edge N r Q M delta',positive=True)
checks=[]
def check(name,c,detail):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name)
rho=(1+eps)*(Ne/N-1)/b
check('zero pressure surface',s.simplify(rho.subs(N,Ne))==0,rho)
check('hydrostatic first integral at free boundary',s.simplify(N*(1+eps+b*rho)-(1+eps)*Ne)==0,rho)
check('density decreases with outward increasing lapse',s.diff(rho,N)<0,s.diff(rho,N))
# Inner/outer average inequality: Qi/Vi >= Qo/Vo implies Qi >= Q Vi/(Vi+Vo).
Vi,Vo,Qi,Qo=s.symbols('Vi Vo Qi Qo',positive=True)
check('enclosed-average reduction',s.simplify(Qi/Vi-Qo/Vo-(Qi*(Vi+Vo)-(Qi+Qo)*Vi)/(Vi*Vo))==0,'Density monotonicity supplies nonnegative left side')
n=s.symbols('n',positive=True)
source=n+eps*n+b*n*n/2
check('source exceeds rescaled reference density',s.simplify(source-(1+eps)*n)==b*n*n/2,source)
bound=r*(Q/(delta*M))**s.Rational(1,3)
check('radius bound saturates stipulated source budget',s.simplify(Q*(r/bound)**3-delta*M)==0,bound)
rows=[]
ratio=s.Rational(1341,250)
for dv in [s.Rational(1,100),s.Rational(1,10),s.Rational(1,2)]:
    value=(ratio/dv)**s.Rational(1,3)
    rows.append(dict(input_Q_over_Mb=str(ratio),stipulated_delta=str(dv),minimum_Ranchor_over_r=float(value)))
out=dict(checks=checks,controls=rows,scope='Necessary hydrostatic source budget for connected compact ordinary EOS anchor, not sufficiency, a measured tolerance, or full global solution.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
