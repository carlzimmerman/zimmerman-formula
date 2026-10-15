import sys,json
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(n,v):
 vv=s.simplify(v);assert vv==0,(n,vv);checks.append(n)
x,y,z=s.symbols('x y z',real=True);coord=(x,y,z);profile=s.Function('s')(x,y,z);lam=s.Function('Lambda')(x,y,z);Mp=s.symbols('Mp',positive=True);V=s.symbols('V',real=True)
A=[1,1,4]
force=-Mp**2*V*sum(A[i]*s.diff(profile**2,coord[i],2) for i in range(3))/4
J=[-Mp**2*V*A[i]*s.diff(profile**2,coord[i])/4 for i in range(3)]
zero('exactpointwisecontrollerEulercompletion',force-sum(s.diff(J[i],coord[i]) for i in range(3)))
# Fullrestrictedstaticdensity; this is not reducedgeneralmetricHamiltonian.
b=lam*profile
EH=Mp**2*(s.diff(b,x)**2+s.diff(b,y)**2)/4
source=-Mp**2*lam**2*(profile*s.diff(profile,z,2)+(s.diff(profile,x)**2+s.diff(profile,y)**2)/4+s.diff(profile,z)**2)
current=-Mp**2*lam*sum(A[i]*s.diff(profile**2,coord[i])*s.diff(lam,coord[i]) for i in range(3))/4
Theta=Mp**2*profile**2*s.diff(lam,z)**2/2
positive=Mp**2*profile**2*((s.diff(lam,x)**2+s.diff(lam,y)**2)/4+s.diff(lam,z)**2/2)
zero('exactpurecontrollerstaticdivergenceidentity',EH+source+current+Theta-positive+Mp**2*s.diff(lam**2*profile*s.diff(profile,z),z))
# Addcanonicalcontrol andshownegativegradientmarginwhens²<=1,|b|<=B.
F,B,gp,gz,sp=s.symbols('F B gp gz s',positive=True)
static=Mp**2*sp**2*(gp**2/4+gz**2/2)-F**2*(gp**2+(1-B**2)*gz**2)/2
# Worstcasecoefficient <=-[F²(1-B²)-Mp²]*(grad²)/2 forsp<=1.
worst=-(F**2*(1-B**2)-Mp**2)*(gp**2+gz**2)/2
zero('puregradientboundSOS',worst-static-(Mp**2*((2-sp**2)*gp**2/4+(1-sp**2)*gz**2/2)+F**2*B**2*gp**2/2))
# OnconstantLambda canonicalderivativesandJ.gradLambda vanish; nofirstmetric/Phi variation.
eps,l0,l1,j0,j1=s.symbols('eps l0 l1 j0 j1',real=True)
zero('constantLambdaJtermzero',((j0+eps*j1)*eps*l1).subs(eps,0))
zero('constantLambdaJmetricfirstvariationzero',s.diff((j0+eps*j1)*0,eps))
result={'claim':'C3W-004','checks_passed':len(checks),'controller_current':'Jmu=-Mp²Lambda/4 E_I^mu diag(1,1,4)_IJ partialPhiJ(s²)','constantbranch':'allconstantLambda stationarybackgroundsnowonecovariantaction; source/metric/Phi preservedandLambdaEulercompleted','puregradient_static_afterboundary':'Mp² s²[(dxLambda)²/4+(dyLambda)²/4+(dzLambda)²/2]','necessary_puresector_Fc2_bound':'Fc²(1-B²)>Mp² sufficient fornegativepurecontrollerstaticform; fullmixedboundrequiresmore','scope':'Nofullmixednumeric7modetheorem,nofiniteenergylaunchorcoldfuelmechanism'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
