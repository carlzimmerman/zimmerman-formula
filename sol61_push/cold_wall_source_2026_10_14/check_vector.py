import json
import sys
from pathlib import Path
import sympy as s

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,value):
    if isinstance(value,s.MatrixBase):
        assert value.applyfunc(s.simplify)==s.zeros(*value.shape),(name,value)
    else:
        assert s.simplify(value)==0,(name,value)
    checks.append(name)
k=s.Matrix(s.symbols('kx ky kz',real=True));k2=(k.T*k)[0]
beta=s.Matrix(s.symbols('bx by bz',real=True))
P=s.eye(3)-k*k.T/k2
zero('transverse projector idempotent',P*P-P)
zero('transverse projector annihilates k',P*k)
j=(k2*s.eye(3)-k*k.T)*beta/2
zero('constraint current is transverse',(k.T*j)[0])
zero('constraint equals projected shift',j-k2*P*beta/2)
q0,q1,q2=s.symbols('q0 q1 q2')
zero('general scalar longitudinal current has no transverse projection',P*(q0*k))
zero('scalar time and higher spatial derivatives remain longitudinal',P*((q0+q1*k2+q2*k2*k2)*k))
# Minimal P(X) in a local inertial frame: T_0i=P_X dot(phi) partial_i(phi).
# Overall sign of energy flux relative to this covariant contraction is kept.
px,clock,amp=s.symbols('PX clock amplitude',real=True)
zero('P(X) linear momentum is longitudinal',P*(px*clock*s.I*amp*k))
x,y,z=s.symbols('x y z');coords=(x,y,z)
b=x*x*z+y*y
bs=s.Matrix([0,0,b])
div=sum(s.diff(bs[i],coords[i]) for i in range(3))
jreal=s.Matrix([s.diff(div,coords[i])-sum(s.diff(bs[i],cc,2) for cc in coords) for i in range(3)])/2
zero('directed source x',jreal[0]-s.diff(b,x,z)/2)
zero('directed source y',jreal[1]-s.diff(b,y,z)/2)
zero('directed source z',jreal[2]+(s.diff(b,x,2)+s.diff(b,y,2))/2)
zero('real source divergence',sum(s.diff(jreal[i],coords[i]) for i in range(3)))
h,mp=s.symbols('h Mp',positive=True)
velocity=-mp**2*j/h
zero('fluid can match momentum alone',-h*velocity-mp**2*j)
result={'claim':'CWS-003','checks_passed':len(checks),'Fourier_constraint':'G_ni=1/2(k^2 delta_ij-k_i k_j) beta_j','interpretation':'Nonzero transverse shift needs transverse source in standard Einstein vector constraint; linear scalar momentum is longitudinal. Fluid momentum matching alone does not match density or pressure.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
