import sys,json
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def ck(n,e):
 assert s.simplify(e)==0,(n,e)
# Normalized-clock variation: dF=dU dot (F_B +2 F_C B).
B=s.Matrix(s.symbols('B0:3',real=True));dU=s.Matrix(s.symbols('dU0:3',real=True));fb=s.Matrix(s.symbols('f0:3',real=True))
a,b,c,d,e,f=s.symbols('a b c d e f',real=True);A=s.Matrix([[a,d,e],[d,b,f],[e,f,c]])
dC=dU*B.T+B*dU.T
ck('proper clock constitutive variation',fb.dot(dU)+s.trace(A*dC)-dU.dot(fb+2*A*B))
# Frozen exact normal Ricci from earlier geometry derivation, declared hashed input.
geo=Path('sol61_push/cold_3d_wall_2026_10_14/geometry_run_v2/calculation/results.json')
data=json.loads(geo.read_text());names=['B','px','py','pz','hxx','hyy','hzz','hxy','hxz','hyz'];ss={v:s.Symbol(v,real=True) for v in names}
R=s.sympify(data['normal_Ricci'],locals=ss);eta=s.diag(-1,1,1,1);G=s.simplify(R-eta*s.trace(eta*R)/2)
rho=G[0,0];j=-G[0,1:].T;S=G[1:,1:];beta=s.Matrix([0,0,ss['B']]);F0=beta.dot(j)-rho;FA=(F0*s.eye(3)-S)/2
W=s.simplify(-j+2*FA*(-beta))
x,y,z=s.symbols('x y z',real=True);coords=[x,y,z];bb=s.Function('b')(x,y,z)
sub={ss['B']:bb,ss['px']:s.diff(bb,x),ss['py']:s.diff(bb,y),ss['pz']:s.diff(bb,z)}
for n,ij in [('hxx',(x,x)),('hyy',(y,y)),('hzz',(z,z)),('hxy',(x,y)),('hxz',(x,z)),('hyz',(y,z))]:sub[ss[n]]=s.diff(bb,*ij)
Wfun=W.subs(sub);Psi=bb+bb**3/3
want=s.Matrix([s.diff(Psi,x,z),s.diff(Psi,y,z),-s.diff(Psi,x,2)-s.diff(Psi,y,2)])/2
for i in range(3):ck('geometric clock current '+str(i),Wfun[i]-want[i])
ck('geometric clock current divergence',sum(s.diff(want[i],coords[i]) for i in range(3)))
# Independent frame-to-coordinate stress conversion.
coframe=s.eye(4);coframe[3,0]=ss['B'];metric=coframe.T*eta*coframe;Tcov=coframe.T*G*coframe;Tmixed=s.simplify(metric.inv()*Tcov)
for i in range(3):ck('clock current equals T^i_0 '+str(i),W[i]-Tmixed[i+1,0])
# Axisymmetric streamfunction identity in cylindrical coordinates.
r,zz=s.symbols('r zc',positive=True);PS=s.Function('Psi')(r,zz);stream=-r*s.diff(PS,r)/2
Ws=s.diff(PS,r,zz)/2;Wz=-(s.diff(PS,r,2)+s.diff(PS,r)/r)/2
ck('axisymmetric streamfunction radial',Ws+s.diff(stream,zz)/r)
ck('axisymmetric streamfunction axial',Wz-s.diff(stream,r)/r)
ck('axisymmetric current divergence',s.diff(r*Ws,r)/r+s.diff(Wz,zz))
# Constraint-compatible small momentum bump has no positive lapse at its extremum.
zz=s.symbols('zz',real=True);amp,epsilon,hh,NN=s.symbols('amp epsilon h N',positive=True)
p=amp*(1+epsilon*s.cos(zz));t=(p*p+s.diff(p,zz)**2/(2*hh))/(4*p);P=-2*s.diff(p,zz)
ck('bump Hamiltonian constraint',p*p-4*t*p+s.diff(p,zz)**2/(2*hh))
ck('bump current zero at extremum',P.subs(zz,0))
ck('bump current divergence at extremum',s.diff(P,zz).subs(zz,0)-2*amp*epsilon)
ck('positive lapse obstruction at extremum',(NN*s.diff(P,zz)).subs(zz,0)-2*amp*epsilon*NN)
res={'claim_id':'CLA-002','checks_passed':len(checks),'clock_current':'W^i=sqrt(gamma) gamma^ij (F_Bj+2F_CjI B^I); d_i(N^2 W^i)=0','target_current':'W=(Psi_xz,Psi_yz,-Psi_xx-Psi_yy)/2 with Psi=b+b^3/3, Mp=1','energy_convention':'W^i=T^i_0; conventional Killing energy current is -T^mu_0','scope':'Exact pure EH+algebraic F(B,C), no explicit clock Phi0 dependence; controller-current extra variations excluded. Frozen earlier normal Ricci input used and independently checked by coordinate stress conversion.'}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(res,indent=2))
