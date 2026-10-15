import sys,json
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(n,v):
 vv=s.simplify(v);assert vv==0,(n,vv);checks.append(n)
lam,g,W,E,D,B=s.symbols('Lambda g W E D B',real=True);eps=1+g*W*lam
L=eps*E**2/2-B**2/2;disp=s.diff(L,E);energy=s.factor(disp*E-L)
zero('MaxwellpositiveLegendre',energy-eps*E**2/2-B**2/2)
HD=energy.subs(E,D/eps);zero('fixedDenergyform',HD-D**2/(2*eps)-B**2/2)
zero('controlleropticalforce',s.diff(L,lam)-g*W*E**2/2)
zero('reciprocalfixedDwork',s.diff(HD,lam)+g*W*(D/eps)**2/2)
# Capacity saturating exteriorfieldell=Delta*a/r;integralgrad²=4pi aDelta².
r,a,delta=s.symbols('r a Delta',positive=True);ell=delta*a/r
capacity=s.integrate(4*s.pi*r*r*s.diff(ell,r)**2,(r,a,s.oo))
zero('harmoniccapacityequality',capacity-4*s.pi*a*delta**2)
# CauchySchwarz gives allotheradmissiblefields>=thisvalue,provedseparately.
Mp,Fc,Cm,bb=s.symbols('Mp Fc Cmix b',positive=True)
coef=Fc**2*(1-bb**2)-Mp**2*(1+Cm**2)
choice=2*Mp**2*(1+Cm**2)/(1-bb**2)
zero('strongcontrollerquadraticmargin',coef.subs(Fc**2,choice)-Mp**2*(1+Cm**2))
energycap=s.factor(coef*capacity/2)
zero('strongcontrollertotalenergycapacity',energycap.subs(Fc**2,choice)-2*s.pi*Mp**2*(1+Cm**2)*a*delta**2)
c=s.Integer(299792458);G=s.Rational('6.67430e-11');example=c**4*s.Rational(1)*s.Rational('0.01')**2/(4*G)
result={'claim':'C3W-005','checks_passed':len(checks),'postulated_operator':'+gp W(Phi)Lambda E_mu E^mu/2','positive_EM_condition':'epsilon=1+gp W Lambda>0','controller_source':'gp W E²/2','power_transfer':'EM losesgp W dotLambda E²/2,controllergainsit forfixedclock/window;fullstressincludesmedium','activation_energy_lower_for_explicit_strongchoice':'E2>=c^4 aDelta²/(4G),fromcoupledquadraticcapacitybound;notuniversaloractualfuelcost','illustrative_model_E_J':float(example),'illustrative_a_m':1,'illustrative_Delta':0.01,'scope':'Postulatedinterfaceandconditionalpositivequadraticenergymodel,nofiniteenergylaunchsolutionoractualcoldfuel'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
