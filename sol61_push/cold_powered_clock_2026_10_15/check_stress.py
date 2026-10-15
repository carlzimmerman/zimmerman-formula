import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def ck(n,e):
 assert s.simplify(e)==0,(n,e)
 checks.append(n)
B=s.Matrix(s.symbols('B0:3')); Bs=s.Matrix(s.symbols('S0:3')); f=s.Matrix(s.symbols('f0:3')); q=s.Matrix(s.symbols('q0:3'))
h,F0=s.symbols('h F0'); F=F0+f.dot(B-Bs)+2*h*(B-Bs).dot(B-Bs)
FB=s.Matrix([s.diff(F,b) for b in B]); sub=dict(zip(B,Bs+q))
rho=(FB.dot(B)-F).subs(sub); rhostar=f.dot(Bs)-F0
ck('normal density correction',rho-rhostar-4*h*Bs.dot(q)-2*h*q.dot(q))
for i in range(3):ck('normal momentum correction '+str(i),(-FB[i]).subs(sub)+f[i]+4*h*q[i])
ck('isotropic spatial stress correction',F.subs(sub)-F0-f.dot(q)-2*h*q.dot(q))
# Fixed-B differentiation, before target substitution, for h independent of Lambda.
l=s.symbols('l'); bsv=s.Matrix([s.Function('bs'+str(i))(l) for i in range(3)]); fv=s.Matrix([s.Function('f'+str(i))(l) for i in range(3)]); Fv=s.Function('F0')(l)+fv.dot(B-bsv)+2*h*(B-bsv).dot(B-bsv)
fl=s.diff(Fv,l); qsub=dict(zip(B,bsv+q)); zsub=dict(zip(B,bsv))
ck('controller source correction at fixed B',fl.subs(qsub)-fl.subs(zsub)-(fv.diff(l)-4*h*bsv.diff(l)).dot(q))
# Direct spacetime divergence of canonical scalar gradient for N=1,gamma=I.
t,x,y,z=s.symbols('t x y z');co=[t,x,y,z];La=s.Function('Lambda')(t);beta=s.Matrix([s.Function('beta'+str(i))(*co) for i in range(3)])
ginv=s.zeros(4);ginv[0,0]=-1
for i in range(3):
 ginv[0,i+1]=ginv[i+1,0]=beta[i]
 for j in range(3):ginv[i+1,j+1]=(1 if i==j else 0)-beta[i]*beta[j]
grad=ginv*s.Matrix([s.diff(La,c) for c in co]);box=sum(s.diff(grad[i],co[i]) for i in range(4))
ck('homogeneous scalar dAlembertian',box+s.diff(La,t,2)-s.diff(La,t)*sum(s.diff(beta[i],co[i+1]) for i in range(3)))
R,Fc,ld=s.symbols('R Fc Lambda_dot',positive=True)
energy=s.integrate(s.Rational(1,2)*Fc**2*ld**2*4*s.pi*R**2,(R,0,R))
ck('homogeneous controller ball energy',energy-2*s.pi*Fc**2*ld**2*R**3/3)
assert s.limit(energy,R,s.oo)==s.oo
checks.append('nonzero homogeneous controller has infinite total energy')
res={'claim_id':'CPC-002','checks_passed':len(checks),'checks':checks,'scope':'Exact ADM constitutive stress correction, fixed-B controller derivative, homogeneous scalar operator, and infinite-volume energy obstruction. Not a solved coupled evolution.'}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
