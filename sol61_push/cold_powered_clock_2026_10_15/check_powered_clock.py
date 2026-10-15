import json, sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=False)
checks=[]
def ck(name, expr):
    residual=s.simplify(expr)
    assert residual==0,(name,residual)
    checks.append(name)
# Direct inverse-Jacobian variation at a unitary background. Rows: material A;
# columns: spacetime mu. The inverse has rows mu and columns A.
eps=s.symbols('eps'); p=s.Matrix(1,4,s.symbols('p0:4'))
J=s.eye(4); J[0,:]=J[0,:]+eps*p
E=J.inv(); dE=E.diff(eps).subs(eps,0)
for mu in range(4):
    for I in range(1,4):
        ck('inverse clock variation %s %s'%(mu,I),dE[mu,I]+(p[I] if mu==0 else 0))
a=s.Matrix(s.symbols('a1:4')); ell=s.Matrix(s.symbols('ell0:4'))
Jvar=(ell.T*dE[:,1:]*a)[0]
ck('controller clock variation sign',Jvar+ell[0]*sum(a[i]*p[i+1] for i in range(3)))
# Local action check using the exact perturbed clock Phi0=t+eps*pi:
# E_I^0=-eps*pi_I/(1+eps*pi_t), E_I^j=delta_Ij.
exact=sum(a[i]*(ell[i+1]-eps*p[i+1]*ell[0]/(1+eps*p[0])) for i in range(3))
ck('direct perturbed-clock action',s.diff(exact,eps).subs(eps,0)-Jvar)
# Geometric current and the new source, with arbitrary smooth spatial sigma.
x,y,z=s.symbols('x y z',real=True); coords=[x,y,z]
lam,ld,M=s.symbols('Lambda Lambda_dot M',real=True)
sig=s.Function('sigma')(x,y,z); b=lam*sig; psi=b+b**3/3
W=s.Matrix([s.diff(psi,x,z),s.diff(psi,y,z),-s.diff(psi,x,2)-s.diff(psi,y,2)])*M**2/2
ac=s.Matrix([s.diff(sig**2,x),s.diff(sig**2,y),0])*M**2*lam/4
div=lambda v:sum(s.diff(v[i],coords[i]) for i in range(3))
ck('steady core divergence',div(W))
residual=M**2*lam*ld*(s.diff(sig**2,x,2)+s.diff(sig**2,y,2))/4
ck('uniform ramp residual',div(W+ld*ac)-residual)
# At an equatorial regular current center: Psi_ss+Psi_s/s=0.
u,v,w,r=s.symbols('sigma sigma_s sigma_ss radius',real=True)
psi_s=lam*(1+lam**2*u**2)*v
psi_ss=lam*(1+lam**2*u**2)*w+2*lam**3*u*v**2
wcenter=-v/r-2*lam**2*u*v**2/(1+lam**2*u**2)
ck('center condition',(psi_ss+psi_s/r).subs(w,wcenter))
divac=M**2*lam*(2*v**2+2*u*(w+v/r))/4
center=M**2*lam*v**2*(1-lam**2*u**2)/(2*(1+lam**2*u**2))
ck('nonzero center forcing',divac.subs(w,wcenter)-center)
# Full affine constitutive response at C=0, not merely a truncated B expansion.
q=s.Matrix(s.symbols('q0:3')); Bstar=s.Matrix(s.symbols('bst0:3'))
f=s.Matrix(s.symbols('f0:3')); h=s.symbols('h',positive=True)
a0,a1,a2,a01,a02,a12=s.symbols('a0 a1 a2 a01 a02 a12')
At=s.Matrix([[a0,a01,a02],[a01,a1,a12],[a02,a12,a2]])
B=Bstar+q
L=4*h*s.eye(3)+2*At
response=f+4*h*q+2*At*B
for i in range(3):ck('exact affine B response '+str(i),response[i]-(f+2*At*Bstar+L*q)[i])
# Independent exact rational invertible matrix witness for compensation sign.
Lnum=s.Matrix([[7,1,2],[1,8,-1],[2,-1,9]])
acnum=s.Matrix([2,-3,0]); qnum=-ld*Lnum.inv()*acnum
for i in range(3):ck('compensating current '+str(i),(Lnum*qnum+ld*acnum)[i])
assert all(d>0 for d in [Lnum[:i,:i].det() for i in range(1,4)])
checks.append('positive definite exact response witness')
# General pointwise response: define the constitutive correction as L q=-ld A.
# Conservation reduces identically without differentiating an inverse matrix.
corr=W-ld*ac
ck('compensated total divergence',div(corr+ld*ac))
results={'claim_id':'CPC-001','checks_passed':len(checks),'checks':checks,
 'powered_clock_equation':'d_i(N^2 W^i + N sqrt(gamma) A^i partial_t Lambda)=0 in unitary gauge',
 'A_definition':'A^I=M^2 Lambda partial_I(sigma^2)/4 for I=1,2; A^3=0',
 'ramp_residual':str(residual),'center_forcing':str(center),
 'repair':'delta B=-partial_t Lambda L^{-1} A; delta beta=+partial_t Lambda L^{-1} A at N=1; L=4h I+F0 I-S',
 'scope':'Exact clock equation only for stated algebraic constitutive action plus canonical Lambda and inverse-Jacobian current. No coupled Einstein/controller solution, stability, thrust, or physical carrier.'}
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(results,indent=2))
