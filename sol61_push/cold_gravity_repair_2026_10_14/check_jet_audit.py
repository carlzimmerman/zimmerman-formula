import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,v):
 vv=s.simplify(v);assert vv==0,(name,vv);checks.append(name)
e=s.symbols('eps',real=True)
def coeff(expr):return s.simplify(s.diff(expr,e,2).subs(e,0)/2)
for case in (1,2):
 b=s.Rational(case,5);bp=s.Rational(3-case,7);bpp=s.Rational(-case,11)
 S=s.Matrix([[s.Rational(2,9),s.Rational(-case,13),s.Rational(1,8)],[-s.Rational(case,13),s.Rational(-1,6),s.Rational(2,15)],[s.Rational(1,8),s.Rational(2,15),s.Rational(case,10)]])
 sd=s.Matrix(3,3,lambda i,j:s.Rational(i+j+case,23))
 ds=[s.Matrix(3,3,lambda i,j:s.Rational((i+j+1)*(k+1)-case,31)) for k in range(3)]
 v=s.Matrix([s.Rational(1,7),s.Rational(-case,9),s.Rational(2,11)])
 dv=s.Matrix(3,3,lambda i,j:s.Rational(i-j+case,29))
 alpha=s.Rational(case,17);da=s.Matrix([s.Rational(1,19),s.Rational(-2,21),s.Rational(case,23)])
 gam=s.eye(3)+e*S;ginv=gam.inv();N=1+e*alpha;beta=s.Matrix([0,0,b])+e*v
 db0=s.zeros(3);db0[0,2]=bp;db=db0+e*dv
 EE=e*sd-sum((beta[k]*e*ds[k] for k in range(3)),s.zeros(3))-db*gam-gam*db.T
 exact=s.sqrt(gam.det())/(8*N)*(s.trace(ginv*EE*ginv*EE)-s.trace(ginv*EE)**2)
 E0=-db0-db0.T
 E1=sd-b*ds[2]-dv-dv.T-db0*S-S*db0.T
 E2=-sum((v[k]*ds[k] for k in range(3)),s.zeros(3))-dv*S-S*dv.T
 F0=s.trace(E0*E0)
 F1=2*s.trace(E0*E1)-2*s.trace(S*E0*E0)
 F2=s.trace(E1*E1)+2*s.trace(E0*E2)-4*s.trace(S*E0*E1)+2*s.trace(S*S*E0*E0)+s.trace(S*E0*S*E0)-(s.trace(E1)-s.trace(S*E0))**2
 tr=s.trace(S);d2=tr**2/8-s.trace(S*S)/4;w1=tr/2-alpha;w2=d2-alpha*tr/2+alpha**2
 zero('nonlinear ADM kinetic jet '+str(case),coeff(exact)-(F2+w1*F1+w2*F0)/8)
 H=s.Matrix([[-b*b*bp*bp/2-b*bpp-bp*bp/2,0,0,-b*bp*bp/2-bpp/2],[0,bp*bp/2,0,0],[0,0,0,0],[-b*bp*bp/2-bpp/2,0,0,-bp*bp/2]])
 Hs=H[1:,1:];Hn=s.Matrix([H[0,i+1]-b*H[3,i+1] for i in range(3)]);Ht=H[0,0]-2*b*H[0,3]+b*b*H[3,3]
 B=H[0,0]-2*sum(beta[i]*H[0,i+1] for i in range(3))+(beta.T*Hs*beta)[0]
 source=-s.sqrt(gam.det())*(-B/N+N*s.trace(ginv*Hs))/2
 targetpot=((v.T*Hs*v)[0]+w1*(-2*(v.T*Hn)[0])+w2*Ht-s.trace(Hs*(S*S-(alpha+tr/2)*S+(d2+alpha*tr/2)*s.eye(3))))/2
 zero('nonlinear inverse source jet '+str(case),coeff(source)-targetpot)
 # Exact unitary Q=-tr(gamma^-1 E)/(2N²); Q*=0 at planar target.
 Q=-s.trace(ginv*EE)/(2*N*N)
 dk=s.trace(sd)/2-b*s.trace(ds[2])/2-s.trace(dv)
 zero('Q first variation',s.diff(Q,e).subs(e,0)+dk)
 zero('nonlinear Q density jet '+str(case),coeff(N*s.sqrt(gam.det())*Q*Q/2)-dk*dk/2)
 acc=s.Rational(3,4)*s.sqrt(gam.det())/N*(e*da).dot(ginv*(e*da))
 zero('nonlinear acceleration density jet '+str(case),coeff(acc)-s.Rational(3,4)*da.dot(da))
 # First inverse-metric strains, including lapse and shift nonlinear map.
 g=s.zeros(4);g[0,0]=-N*N+(beta.T*gam*beta)[0]
 for i in range(3):
  g[0,i+1]=g[i+1,0]=(gam*beta)[i]
  for j in range(3):g[i+1,j+1]=gam[i,j]
 theta=s.eye(4);theta[3,0]=b;gstar=g.subs(e,0)
 # Derivative inverse identity avoids expanding a large inverse; independent
 # metric construction above contains nonlinear ADM lapse/shift relation.
 dg=s.diff(g,e).subs(e,0);dB=-gstar.inv()*dg*gstar.inv();SS=s.simplify(theta*dB*theta.T)
 zero('framed lapse strain '+str(case),SS[0,0]-2*alpha)
 for i in range(3):
  zero('framed shift strain '+str((case,i)),SS[0,i+1]-v[i])
  for j in range(i,3):zero('framed spatial strain '+str((case,i,j)),SS[i+1,j+1]+S[i,j])
result={'claim':'CGR-004','checks_passed':len(checks),'verdict':'Exact local-jet nonlinear expansion checks agree for tested nonzero background jets. Spatial integrated curvature independently benchmarked only through flat spectra in other runs. Not a global theorem or independent author review.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
