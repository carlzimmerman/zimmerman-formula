"""CE-FM-004 independent exact-rational audit of CFG750 instantaneous capture."""
import json,sys
from pathlib import Path
import sympy as s

dm=(s.Integer(200)-s.Rational(1,10))/4000
seed=s.Rational(1,10000);mn=1+seed
lo,hi=s.Rational(1,1000),s.Rational(1,100)
checks=[]
def check(name,condition,detail):
    checks.append(dict(name=name,passed=bool(condition),detail=detail))
    if not condition:raise AssertionError(name)

captures=[n for n in range(4001) if lo<=seed+n*dm<=hi]
check('CONSISTENT interval unrepresentable',len(captures)==0,{'dm':str(dm),'captures':captures})
check('first capture exceeds RUNAWAY threshold',seed+dm>s.Rational(1,20),str(seed+dm))
def field(rs):
    total=s.Integer(0)
    for i,r in enumerate(rs):
        mo=(i+1)*dm
        next_inverse=rs[i+1]**(-3) if i+1<len(rs) else 0
        total+=mo**3*(r**(-3)-next_inverse)/9
    return total

rows=[]
for tail in ([s.Integer(1)],[s.Rational(1,2),s.Integer(1)]):
    r0=s.Rational(9,100);rs=[r0]+tail;v0=s.Integer(5)
    before=dm*v0**2/2-dm*mn*sum(1/r for r in rs)+field(rs)
    after=-dm*(mn+dm)*sum(1/r for r in tail)+field(tail)
    swallowed=dm*v0**2/2-dm*mn/r0
    defect=s.simplify(after+swallowed-before)
    field_change=field(tail)-field(rs)
    expected=field_change-dm**2*sum(1/r for r in tail)
    check(f'analytical ledger defect {len(tail)} retained',defect==expected,str(defect))
    check(f'negative energy defect {len(tail)} retained',defect<0,float(defect))
    rows.append(dict(retained_radii=list(map(str,tail)),initial_energy=float(before),field_change=float(field_change),
                     Newton_binding_change=float(-dm**2*sum(1/r for r in tail)),ledger_defect=float(defect),
                     relative_to_initial=abs(float(defect/before))))
result=dict(checks=checks,dm=str(dm),first_capture_mass=str(seed+dm),consistent_capture_counts=captures,
            instantaneous_capture=rows,
            scope='Exact rational instantaneous update and attainable mass lattice; no formation, GR capture or empirical claim.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
