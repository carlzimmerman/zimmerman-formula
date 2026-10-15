import sys,json
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,v):
 value=s.simplify(v);assert value==0,(name,value);checks.append(name)
t,x,y,z=s.symbols('t x y z',real=True);coords=(t,x,y,z);b=s.Function('b')(x,y,z)
g=s.Matrix([[-1+b*b,0,0,b],[0,1,0,0],[0,0,1,0],[b,0,0,1]]);gi=g.inv()
Ga=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[j])+s.diff(g[d,j],coords[c])-s.diff(g[j,c],coords[d])) for d in range(4))/2) for c in range(4)] for j in range(4)] for a in range(4)]
U=s.Matrix([1,0,0,-b]);Uc=s.Matrix([-1,0,0,0]);P=gi+U*U.T
Theta=sum(s.diff(U[m],coords[m])+sum(Ga[m][m][n]*U[n] for n in range(4)) for m in range(4))
Q=-sum(P[m,n]*Ga[0][m][n] for m in range(4) for n in range(4))
zero('target determinant',g.det()+1);zero('target Theta',Theta+s.diff(b,z));zero('target Q',Q-s.diff(b,z))
for m in range(4):zero('target acceleration '+str(m),sum(U[n]*(s.diff(Uc[m],coords[n])-sum(Ga[k][n][m]*Uc[k] for k in range(4))) for n in range(4)))
eps,al,dt,ts=s.symbols('eps alpha deltaTheta ThetaStar',real=True)
N=1+eps*al;TT=ts+eps*dt
zero('Q-Theta first variation on zero-expansion target',s.diff(-TT/N,eps).subs({eps:0,ts:0})+dt)
zero('Q and Theta squared differences agree throughquadratic atThetaStar0',s.diff((TT-ts)**2-(-TT/N+ts)**2,eps,2).subs({eps:0,ts:0}))
ks=s.symbols('kxx kyy kzz kxy kxz kyz',real=True);K=s.Matrix([[ks[0],ks[3],ks[4]],[ks[3],ks[1],ks[5]],[ks[4],ks[5],ks[2]]]);tr=s.trace(K)
full=(s.trace(K*K)-tr*tr+(tr-ts)**2)/2
zero('exact negative-trace cancellation',full-(s.trace(K*K)-2*tr*ts+ts**2)/2)
velH=s.hessian(full,ks)
zero('six positive orthonormal Kij velocity Hessian',sum((velH-s.diag(1,1,1,2,2,2))[i,j]**2 for i in range(6) for j in range(6)))
zero('regulator target value',((TT-ts)**2).subs(eps,0));zero('regulator target first variation',s.diff((TT-ts)**2,eps).subs(eps,0))
result={'claim':'CGR-005','checks_passed':len(checks),'normalized_action_replacement':'+Mp²(Theta-ThetaStar)²/2, Theta=divU,ThetaStar=-b_z; +3Mp² a_mu a^mu/4; strainKc4,L100,mu2,hD=Mp²','background':'unchanged for arbitrary smooth staticb','evidence_transfer':'Q and normalizedTheta quadratic actions agree for prior homogeneous exterior and planar b(x) wall runs sinceThetaStar0','unreduced_kinetic':'exact spatial velocity Hessian positive for positive lapse and spatial metric; lapse/shift reduction and potential still require separate analysis','warning':'No full3D reduced wall stability, physical finite medium, causality or engine result.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
