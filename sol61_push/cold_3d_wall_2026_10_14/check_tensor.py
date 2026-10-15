import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(n,v):
 assert s.simplify(v)==0,(n,v);checks.append(n)
q=s.symbols('q',positive=True);h,hd=s.symbols('h hd',real=True);kap=s.Integer(4);cs=s.Rational(1,2);mu=s.Integer(2)
L=(1+kap)*hd**2/4-(1+kap*cs)*q*h*h/4-mu*h*h/2
K=s.diff(L,hd,2);G=-s.diff(L,h,2);freq=s.factor(G/K)
zero('TTfrequency',freq-3*q/5-s.Rational(4,5))
speed2=s.factor(q*s.diff(freq,q)**2/freq)
zero('TTgroupdeficit',s.Rational(3,5)-speed2-s.Rational(12,5)/(3*q+4))
assert 1-s.sqrt(s.Rational(3,5))>s.Rational(3,10**15);checks.append('uniformvacuumfailsprimaryspeedinterval')
result={'claim':'C3W-006','checks_passed':len(checks),'tensor_frequency2':str(freq),'max_tensor_group_speed_c':float(s.sqrt(s.Rational(3,5))),'physical_scope':'SpecifieduniforminfinitemediumcannotrepresentobservedordinaryvacuumunderstandardtensorGWinterpretation; finiteengineeredphasepossibleonlyafternewmatchinganalysis.','primary_reference':'https://arxiv.org/pdf/1710.05834','bound_used':'historicalGW170817 -3e-15<=(vGW-c)/c<=7e-16; no latestboundclaim'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
