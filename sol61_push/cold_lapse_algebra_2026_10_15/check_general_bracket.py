import sys,json
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
z=s.symbols('z',real=True);h=s.symbols('h',positive=True)
q=[s.Function(v)(z) for v in ['a','b','c']];p=[s.Function(v)(z) for v in ['pa','pb','pc']];a,b,c=q;pa,pb,pc=p;n=s.Function('n')(z)
root=s.sqrt(a*b*c)
R=-s.diff(a,z,2)/(a*c)-s.diff(b,z,2)/(b*c)+s.diff(a,z)**2/(2*a*a*c)+s.diff(b,z)**2/(2*b*b*c)-s.diff(a,z)*s.diff(b,z)/(2*a*b*c)+s.diff(a,z)*s.diff(c,z)/(2*a*c*c)+s.diff(b,z)*s.diff(c,z)/(2*b*c*c)
P=pa*s.diff(a,z)+pb*s.diff(b,z)-pc*s.diff(c,z)-2*c*s.diff(pc,z)
Hg=(2*sum((q[i]*p[i])**2 for i in range(3))-sum(q[i]*p[i] for i in range(3))**2)/root-root*R/2
H=Hg+P*P/(8*h*root)+h*root*sum((1/v-1)**2 for v in q)/2
def Euler(v,order):return s.expand(sum((-1)**j*s.diff(s.diff(n*H,s.diff(v,z,j)),z,j) for j in range(order+1)))
Eq=[Euler(v,2) for v in q];Ep=[Euler(v,1) for v in p]
A=[s.diff(e,n) for e in Eq];B=[s.diff(e,s.diff(n,z)) for e in Eq];CC=[s.diff(e,s.diff(n,z,2)) for e in Eq]
D=[s.diff(e,n) for e in Ep];E=[s.diff(e,s.diff(n,z)) for e in Ep]
assert s.simplify(sum(CC[i]*E[i] for i in range(3)))==0
bracket=sum(A[i]*E[i]-D[i]*B[i] for i in range(3))+s.diff(sum(CC[i]*D[i] for i in range(3)),z)
shift=P/(4*h*root);W=-P*(3-1/c)/(2*c)
residual=s.factor(s.together(bracket-(-W+shift*H)))
assert residual==0,str(residual)
res={'claim_id':'CLA-004','checks_passed':2,'scope':'All smooth positive diagonal spatial metrics and diagonal momenta depending on z in constant h>0 rest-source patch; exact full functional bracket, not flat substitution.','strong_bracket_coefficient':'B=-W+s*C, W=-Pz*(3-1/gamma_zz)/(2 gamma_zz), s=Pz/(4h sqrtgamma)','weak_lapse_equation':'div(N² W)=0, sign convention accounted for; C term vanishes on full constraint surface','non_claim':'Not all non-diagonal/transverse modes, no completed secondary algorithm or healthy DOF count.'}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
