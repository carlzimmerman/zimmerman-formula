import sys,json
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(n,v):
 assert s.simplify(v)==0,(n,s.simplify(v));checks.append(n)
q=s.symbols('q',positive=True);Z,Y,zd,yd=s.symbols('Z Y zd yd',real=True)
f=q+2+2/(q+1)
base=zd**2+2*yd**2/(q+4)-f*Z**2-2*Y**2
add=(2*zd**2+yd**2-q*(2*Z**2+Y**2)/2)/2
lag=base+add
K=s.hessian(lag,(zd,yd));G=-s.hessian(lag,(Z,Y))
fz=s.factor(G[0,0]/K[0,0]);fy=s.factor(G[1,1]/K[1,1])
zero('elastic clock frequency',fz-(3*q/4+1+1/(q+1)));zero('elastic material frequency',fy-(q/2+2))
zero('uniform clock kinetic',K[0,0]-4);zero('uniform Ykinetic lowergap',K[1,1]-1-4/(q+4))
kv=4/(q+8)+s.Rational(1,2);gv=2+q/4;fv=s.factor(gv/kv);ft=3*q/4+2
zero('vector frequency',fv-(q/2+32/(q+16)))
# Exact derivative ranges: clock(-1/4,3/4),vector(3/8,1/2),Y1/2,tensor3/4.
zero('clock derivative',s.diff(fz,q)-(s.Rational(3,4)-1/(q+1)**2))
zero('vector derivative',s.diff(fv,q)-(s.Rational(1,2)-32/(q+16)**2))
# Eachf>c2*q and |f'|<=c2 =>vg²<c2: clock3/4,vector1/2,Y1/2,tensor3/4.
for name,ff,cs in [('clock',fz,s.Rational(3,4)),('Y',fy,s.Rational(1,2)),('vector',fv,s.Rational(1,2)),('tensor',ft,s.Rational(3,4))]:
 assert s.factor(ff-cs*q)>0;checks.append(name+' positive gradientgap')
 for qq in (s.Rational(1,1000000),s.Rational(1,2),1,10,10000):
  vv=s.factor((q*s.diff(ff,q)**2/ff).subs(q,qq));assert 0<=vv<cs;checks.append(name+' rational speed '+str(qq))
# Exact unitary spatial projection from full inverse ADM metric.
N=s.symbols('N',positive=True);v=s.Matrix(s.symbols('v0:3'));a,b,c=s.symbols('a b c',positive=True);gam=s.diag(a,b,c)
g=s.zeros(4);g[0,0]=-N*N+(v.T*gam*v)[0]
for i in range(3):
 g[0,i+1]=g[i+1,0]=(gam*v)[i]
 for j in range(3):g[i+1,j+1]=gam[i,j]
U=s.Matrix([1/N,*[-vi/N for vi in v]]);P=g.inv()+U*U.T
zero('unitary projected spatial inverse identity',sum((P[1:,1:]-gam.inv())[i,j]**2 for i in range(3) for j in range(3)))
result={'claim':'CGR-009','checks_passed':len(checks),'selected_extra_operator':'Mp²/8 sumIJ[(U.grad Cij)²-(1/2)P.gradCij.gradCij],Cij=projectedSpatialMaterialStrain','Kscalar':str(K),'Gscalar':str(G),'clock_frequency2':str(fz),'Y_frequency2':str(fy),'vector_frequency2':str(fv),'tensor_frequency2':str(ft),'uniform_group_speed_squared_bounds':{'clock':'3/4','Y':'1/2','vector':'1/2','tensor':'3/4'},'scope':'allqpositive homogeneous exterior; no full3Dwall or causal/observational/engine guarantee'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
