import json
import sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,v):
    assert s.simplify(v)==0,(name,s.simplify(v))
    checks.append(name)
t,x,y,z=s.symbols('t x y z',real=True);cs=(t,x,y,z)
b=s.Function('b')(x,y,z);A=s.Function('A')(t,x,y,z)
g=s.Matrix([[-1+b*b,0,0,b],[0,1,0,0],[0,0,1,0],[b,0,0,1]])
gi=g.inv();n=(1,0,0,-b)
contract=[]
for d in range(4):
    val=sum(n[a]*sum(gi[d,e]*(s.diff(g[e,3],cs[a])+s.diff(g[e,a],z)-s.diff(g[a,3],cs[e])) for e in range(4))/2 for a in range(4))
    contract.append(s.simplify(val))
for d,target in enumerate((0,-s.diff(b,x)/2,-s.diff(b,y)/2,0)):
    zero('contracted connection '+str(d),contract[d]-target)
H=sum(n[a]*s.diff(A,cs[a],z) for a in range(4))-sum(contract[d]*s.diff(A,cs[d]) for d in range(4))
zero('dynamic Hessian projection',H-(s.diff(A,t,z)-b*s.diff(A,z,2)+(s.diff(b,x)*s.diff(A,x)+s.diff(b,y)*s.diff(A,y))/2))
# x>0 eliminates absolute value ambiguity at the equator.
xx=s.symbols('xx',positive=True)
rr=s.sqrt(xx*xx+y*y+z*z)
rad=s.Function('Arad')(t,rr)
zero('radial mixed time z at equator',s.diff(rad,t,z).subs({y:0,z:0},simultaneous=True))
zero('radial zz at equator',s.diff(rad,z,2).subs({y:0,z:0},simultaneous=True)-s.diff(s.Function('Arad')(t,xx),xx)/xx)
result={'claim':'CWS-004','checks_passed':len(checks),'conclusion':'A radial time-dependent scalar leaves the same necessary momentum ODE at each time in the stated stationary metric and A(phi)R/P action.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
