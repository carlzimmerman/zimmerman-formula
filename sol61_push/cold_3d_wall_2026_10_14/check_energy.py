import sys,json,math
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(n,v):
 vv=s.simplify(v)
 assert (vv==s.zeros(*vv.shape) if isinstance(vv,s.MatrixBase) else vv==0),(n,vv)
 checks.append(n)
def pos(n,v):
 assert s.factor(v)>0,(n,v);checks.append(n)
eps,alpha=s.symbols('eps alpha',real=True)
uvars=s.symbols('uxx uyy uzz uxy uxz uyz',real=True)
u=s.Matrix([[uvars[0],uvars[3],uvars[4]],[uvars[3],uvars[1],uvars[5]],[uvars[4],uvars[5],uvars[2]]])
p=s.Matrix(s.symbols('px py pz',real=True));J=s.zeros(3)
for i in range(3):J[i,2]=p[i]
E0=-J-J.T;Kstar=s.trace(E0)/2
dv=s.Matrix(3,3,s.symbols('dv0:9',real=True));E1=u-dv-dv.T;N=1+eps*alpha;E=E0+eps*E1
exact=(s.trace(E*E)-s.trace(E)**2)/(8*N)+N*(s.trace(E)/(2*N)-Kstar)**2/2
actual=s.diff(exact,eps,2).subs(eps,0)/2
zero('full3D nonlinear kinetic completion',actual-s.trace((E1-alpha*E0)**2)/8)
# Independent source coefficient and quadratic strain cancellation atS=0.
Ht=s.symbols('Ht',real=True);Hn=s.Matrix(s.symbols('Hn0:3',real=True));hs=s.symbols('hxx hyy hzz hxy hxz hyz',real=True);Hs=s.Matrix([[hs[0],hs[3],hs[4]],[hs[3],hs[1],hs[5]],[hs[4],hs[5],hs[2]]]);v=s.Matrix(s.symbols('v0:3',real=True))
source=(Ht-2*eps*(v.T*Hn)[0]+eps**2*(v.T*Hs*v)[0])/(2*N)-N*s.trace(Hs)/2
strain=(1-Ht)*alpha**2/2+(v.T*(4*s.eye(3)-Hs)*v)[0]/2-alpha*(v.T*Hn)[0]
zero('exact inverse source strain cancellation',s.diff(source,eps,2).subs(eps,0)/2+strain-alpha**2/2-2*(v.T*v)[0])
# Unintegratedspatialcurvaturegradient form at unitwavevectorz.
a=s.Matrix(s.symbols('sxx syy szz sxy sxz syz',real=True));S=s.Matrix([[a[0],a[3],a[4]],[a[3],a[1],a[5]],[a[4],a[5],a[2]]]);tr=s.trace(S)
rgrad=(-s.trace(S*S)/4+tr**2/4+sum(S[2,j]**2 for j in range(3))/2-S[2,2]*tr/2)/2
zero('rank1curvatureform',rgrad-(a[0]*a[1]-a[3]**2)/4)
zero('curvatureupperSOS',s.trace(S*S)/8-rgrad-((a[0]-a[1])**2+a[2]**2+4*a[3]**2+2*a[4]**2+2*a[5]**2)/8)
# PositiveSOS certificate forbackgroundnormalRiccinormsplitting.
px,py,pz=p;gx=px**2+py**2;gg=gx+pz**2
Rg=s.Matrix([[-gx/2-pz**2,0,0,0],[0,px**2/2,px*py/2,px*pz],[0,px*py/2,py**2/2,py*pz],[0,px*pz,py*pz,-gx/2+pz**2]])
frob=lambda M:sum(M[i,j]**2 for i in range(M.rows) for j in range(M.cols))
zero('RicgradientnormSOS',2*gg**2-frob(Rg)-s.Rational(5,4)*gx**2-2*gx*pz**2)
xx,yy,zz,xy,xz,yz=hs;Hsq=xx**2+yy**2+zz**2+2*(xy**2+xz**2+yz**2)
R0=s.Matrix([[0,xz/2,yz/2,-(xx+yy)/2],[xz/2,0,0,0],[yz/2,0,0,0],[-(xx+yy)/2,0,0,0]])
RB=s.Matrix([[-zz,0,0,0],[0,0,0,xz/2],[0,0,0,yz/2],[0,xz/2,yz/2,zz]])
zero('Richessian0normSOS',Hsq-frob(R0)-(s.Rational(1,2)*(xx-yy)**2+zz**2+2*xy**2+s.Rational(3,2)*(xz**2+yz**2)))
zero('RichessianBnormSOS',4*Hsq-frob(RB)-(4*xx**2+4*yy**2+2*zz**2+8*xy**2+s.Rational(15,2)*(xz**2+yz**2)))
# Normboundarithmetic: sqrt3<7/4; staticEH+Theta <=2B²d²+13g²s².
pos('sqrt3 rationalupper',s.Rational(7,4)-s.sqrt(3))
A=(9+s.sqrt(3))/4;C=s.Rational(11,4)+5*s.sqrt(3)/4
pos('mixedcoeffbound',s.Rational(43,16)-A);pos('masscoeffbound',s.Rational(79,16)-C)
B,g0,ss,dd=s.symbols('B g S d',nonnegative=True)
e1=B*dd+2*g0*ss
inter=s.expand(e1**2/8+s.Rational(43,16)*g0*ss*e1+s.Rational(79,16)*g0**2*ss**2)
upper=s.Rational(55,32)*B**2*dd**2+s.Rational(397,32)*g0**2*ss**2
zero('staticYoungSOS',upper-inter-s.Rational(51,32)*(B*dd-g0*ss)**2)
pos('integergradientbound',2-s.Rational(55,32));pos('integermassbound',13-s.Rational(397,32))
# Inversesource potentialnormbound <(3/2)eta*S².
pos('sourcepotentialnormbound',s.Rational(3,2)-(s.Rational(5,8)+3*s.sqrt(3)/8))
# b radialCinf profile: exactelementaryconstants and exponentialupperbound.
X=s.Rational(4,3);order=6;exp_upper=sum(X**n/s.factorial(n) for n in range(order+1))+(X**(order+1)/s.factorial(order+1))/(1-X/(order+2))
pos('e4over3less4seriescertificate',4-exp_upper)
zero('radialHessian514bound',s.Integer(514)**2-s.Integer(512)**2-2*s.Integer(32)**2-4)
V=s.Rational(1,10);radius=s.Integer(100)
g2=256*V*V/radius**2;j=514*V/radius**2;eta=10*((1+V)*j+g2)
massloss=13*g2+s.Rational(3,2)*eta
pos('concretesphericalmassmargin',s.Rational(1,4)-massloss)
zero('sphericalgradientmargin',s.Rational(1,8)-s.Rational(5,2)*V**2-s.Rational(1,10))
# Nonlinearstaticjetsecondvariations with nonzeroThetaStar andgeneral3Dstrain derivatives.
for case in (1,2):
 S0=s.Matrix([[s.Rational(2,9),s.Rational(-case,13),s.Rational(1,8)],[-s.Rational(case,13),s.Rational(-1,6),s.Rational(2,15)],[s.Rational(1,8),s.Rational(2,15),s.Rational(case,10)]])
 dS=[s.Matrix(3,3,lambda i,j:s.Rational((i+j+1)*(k+1)-case,31)) for k in range(3)]
 bv=s.Rational(case,10);pv=s.Matrix([s.Rational(1,13),s.Rational(-2,17),s.Rational(case,19)]);JJ=s.zeros(3)
 for i in range(3):JJ[i,2]=pv[i]
 A0=-JJ-JJ.T;A1=-bv*dS[2]-JJ*S0-S0*JJ.T;ks=s.trace(A0)/2
 gamma=s.eye(3)+eps*S0;inv=gamma.inv();AA=inv*(A0+eps*A1)
 L=s.sqrt(gamma.det())*((s.trace(AA*AA)-s.trace(AA)**2)/8+(s.trace(AA)/2-ks)**2/2)
 actual=s.simplify(s.diff(L,eps,2).subs(eps,0)/2)
 ts=s.trace(S0);d2=ts**2/8-s.trace(S0*S0)/4
 first=(s.trace(A1*A1)-4*s.trace(S0*A0*A1)+2*s.trace(S0*S0*A0*A0)+s.trace(S0*A0*S0*A0)+ts*(s.trace(A0*A1)-s.trace(S0*A0*A0))+d2*s.trace(A0*A0))/8
 second=-ks*(s.trace(S0*S0*A0)-s.trace(S0*A1)+ts*(s.trace(A1)-s.trace(S0*A0))/2+d2*s.trace(A0))/2+ks**2*d2/2
 zero('nonlinearfull3DstaticThetajet '+str(case),actual-first-second)
 # Frobeniusbound at jet: gradientnormtotal andbackgroundgradientnorm.
 dnorm=s.sqrt(sum(frob(a) for a in dS));snorm=s.sqrt(frob(S0));gnorm=s.sqrt(pv.dot(pv))
 pos('staticnormboundjet '+str(case),2*bv*bv*dnorm**2+13*gnorm**2*snorm**2-actual)
result={'claim':'C3W-001E','checks_passed':len(checks),'jointkinetic':'exactpositivecompleted square forarbitrary3Dgradientb includingbz','staticgradientcoercivity':'1/8-(5/2)B²','staticmasscoercivity':'1/(2D)-13g²-(3/2)eta','explicitprofile':{'V_max':'1/10','R_min_sqrtD':100,'D_g2_bound':str(g2),'D_eta_bound':str(eta),'D_mass_loss_bound':str(massloss),'gradient_margin':'1/10','safe_mass_margin':'1/(4D)'},'sourceRiccinorm':'eta<=2[(1+B)HessbF+g²] strongerthanusedfactor10','scope':'Symbolicidentities+finitejetchecks supportingseparateallR3analyticproof; no nonlinearwellposedness,physicalcarrier,interfaceorengineproof'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
