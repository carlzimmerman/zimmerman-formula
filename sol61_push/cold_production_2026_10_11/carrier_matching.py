"""Exact rational checks of threshold matching and rotating cold solutions."""
import json,itertools
from fractions import Fraction as F
from pathlib import Path
p=Path(__file__).parent;checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
for i,(m,Delta,g,A) in enumerate(itertools.product([F(1),F(2,3)],[F(1,100),F(1,3)],[F(1,10),F(2,7)],[F(0),F(1,5),F(3)])):
    M2=4*m*m+Delta;chi=-g*A*A/Delta;lam=g*g/Delta
    phi_res=2*g*chi*A+2*lam*A**3
    chi_res=(M2-4*m*m)*chi+g*A*A
    U=Delta*chi*chi+2*g*chi*A*A+lam*A**4
    kinetic=m*m*A*A+4*m*m*chi*chi
    potential=m*m*A*A+4*m*m*chi*chi+U
    E=kinetic+potential;Q=2*m*A*A+8*m*chi*chi
    check('exact circular equations '+str(i),phi_res==0 and chi_res==0)
    check('exact charge saturation and pressure '+str(i),E==m*Q and kinetic==potential)
    check('threshold cancellation '+str(i),lam+g*g/(4*m*m-M2)==0)
rows=[]
for x in [F(0),F(1,100),F(1,10),F(1,2),F(9,10),F(11,10),F(2)]:
    ratio=1+1/(x-1)
    check('amplitude reduction '+str(x),ratio==-x/(1-x))
    rows.append(dict(relative_s_excess=str(x),effective_quartic_over_minimum=str(ratio)))
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Tree level only','No finite-density scattering or halo simulation','No production claim for added repulsive quartic'])
(p/'carrier_matching_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Checks:',len(checks),out['all_pass']);print(json.dumps(rows,indent=2));assert out['all_pass']
