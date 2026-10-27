import sympy as s
import json,sys
from pathlib import Path
checks=[]
def ck(name,expr):
 assert s.simplify(expr)==0,name
 checks.append(name)
a,K,C,d,u=s.symbols('a K C d u',positive=True)
W=a*a/K*(C-u/a-s.log(1-u/a))
ck('constant_shift_changes_only_vacuum',W.subs(C,C+d)-W-d*a*a/K)
ck('response_independent_of_C',s.diff(W,C,u))
g=K*s.diff(W,u)
ck('simple_kernel',g-u-g*g/(g+a))
kappa=s.symbols('kappa',positive=True)
ck('vacuum_matching_C',((4*s.pi/kappa**2)*a*a/(4*s.pi))-a*a/kappa**2)
r,b,c,H,Q,S,j=s.symbols('r b c H Q S j',real=True,nonzero=True)
ck('ratio_evolution',((-3*H*c+Q)*b-c*(-3*H*b))/b**2-Q/b)
ck('conversion_cancels_total_mass',(-j-S)+(j+S))
# The unchanged identity would predict -j instead of -j-S.
ck('polarization_defect',(-j)-(-j-S)-S)
A,B,x=s.symbols('A B x',real=True)
ck('mass_sheet_cancels_in_ESD',(A+x)-(B+x)-(A-B))
# Truncated flat-circular-speed potential normalized at infinity.
# Phi(r)=-V^2[1+ln(Re/r)]; escape condition includes exterior point-mass tail.
V,Re=s.symbols('V Re',positive=True)
phi=-V**2*(1+s.log(Re/r))
ck('flat_potential_force',s.diff(phi,r)-V**2/r)
ck('edge_matches_point_potential',phi.subs(r,Re)+V**2)
res={'exact_checks':checks,'count':len(checks),'scope':'Conditional algebra, not a solved conversion action, distribution function, or observational likelihood'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
