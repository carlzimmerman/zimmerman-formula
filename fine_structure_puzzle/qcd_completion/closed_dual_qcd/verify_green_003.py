"""CDQ-002 exact symbolic Green-kernel controls and finite numerics."""
import json
from pathlib import Path
import sympy as sp
import mpmath as mp

x=sp.symbols('x',positive=True)
r,h=sp.symbols('r h',positive=True)
F=(sp.pi-x)*sp.cot(x)-sp.Rational(1,2)
radial=sp.simplify(sp.diff(F,x,2)+2*sp.cot(x)*sp.diff(F,x)-2)
assert radial==0
anti=sp.limit(F,x,sp.pi,dir='-')
antid=sp.limit(sp.diff(F,x),x,sp.pi,dir='-')
assert anti==-sp.Rational(3,2) and antid==0
series=sp.series(h*((sp.pi-r*h)*sp.cot(r*h)-sp.Rational(1,2))/(4*sp.pi**2),h,0,5)
expected=1/(4*sp.pi*r)-3*h/(8*sp.pi**2)-r*h*h/(12*sp.pi)+r*r*h**3/(12*sp.pi**2)-r**3*h**4/(180*sp.pi)
assert sp.simplify(series.removeO()-expected)==0

neutral=[]
for k in range(1,7):
    charges=[1]*k+[-1]*k
    selfpart=sum(q*q for q in charges)
    pairpart=sum(charges[i]*charges[j] for i in range(len(charges)) for j in range(i+1,len(charges)))
    assert selfpart+2*pairpart==sum(charges)**2==0
    neutral.append({'events':2*k,'self':selfpart,'twice_pairs':2*pairpart,'sum':selfpart+2*pairpart})

records=[]
for dps in [60,85]:
    mp.mp.dps=dps
    mean=mp.quad(lambda t:(mp.pi-t)*mp.sin(t)*mp.cos(t)-mp.sin(t)**2/2,[0,mp.pi/2,mp.pi])
    assert abs(mean)<mp.mpf('1e-55')
    rs=[]
    for radius in map(mp.mpf,['4','8','16','32','64']):
        sep=mp.mpf('0.7')
        kernel=((mp.pi-sep/radius)*mp.cot(sep/radius)-mp.mpf('0.5'))/(4*mp.pi**2*radius)
        leading=(kernel-1/(4*mp.pi*sep))*radius
        rs.append({'R':str(radius),'R_delta_G':mp.nstr(leading,dps)})
    records.append({'dps':dps,'mean_integral':mp.nstr(mean,25),'fixed_separation_values':rs})

out={'claim_id':'CDQ-002','symbolic':{'radial_equation_residual':str(radial),'antipode_value':str(anti),'antipode_derivative':str(antid),'series':str(series)},'neutral_configurations':neutral,'numerics':records,'non_claims':['Finite-configuration expansion is not uniform at r~R','Does not establish the full interacting plasma or curved hard matching']}
dest=Path('fine_structure_puzzle/qcd_completion/closed_dual_qcd/runs/green-003/result.json')
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'result':str(dest),'symbolic_controls':4,'neutral_cases':6,'precisions':[60,85]}))
