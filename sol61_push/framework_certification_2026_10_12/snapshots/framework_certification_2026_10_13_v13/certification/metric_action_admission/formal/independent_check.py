import sympy as s
import json
from pathlib import Path
E,P,Q,m,v=s.symbols('e Phi Psi m v', real=True)
n=s.sqrt((1-2*E*Q)/(1+2*E*P))
L=-m*s.sqrt(1+2*E*P-(1-2*E*Q)*v**2)
r=s.symbols('s',real=True)
checks={
 'actual_index_derivative':s.diff(n,E).subs(E,0)+P+Q,
 'null_index_square':n**2-(1-2*E*Q)/(1+2*E*P),
 'actual_fermat_derivative':s.diff(n*s.sqrt(1+v**2),E).subs(E,0)+(P+Q)*s.sqrt(1+v**2),
 'actual_worldline_derivative':s.diff(L,E).subs(E,0)+m*(P+Q*v**2)/s.sqrt(1-v**2),
 'rest_worldline_derivative':s.diff(L,E).subs({E:0,v:0})+m*P,
 'slip_optical_coefficient':s.diff(n,E).subs({E:0,Q:r*P})+(1+r)*P,
 'moving_Psi_counterexample':s.diff(L,E).subs({E:0,P:0,Q:1,m:1,v:s.Rational(1,2)})+s.sqrt(3)/6,
 'optical_slip_difference':s.diff(n,E).subs({E:0,P:1,Q:1})-s.diff(n,E).subs({E:0,P:1,Q:0})+1,
}
rows=[{'name':k,'residual':str(s.simplify(x)),'pass':s.simplify(x)==0} for k,x in checks.items()]
result={'scope':'Independent exact local action algebra, not gravity solution or full ray trajectory','checks':rows,'all_pass':all(x['pass'] for x in rows),'sympy_version':s.__version__}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert result['all_pass']
