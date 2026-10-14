"""One-loop QED-level scalar messenger matching; no experimental parameter claim."""
import json,math,sys
from pathlib import Path
import sympy as s
from scipy.integrate import quad
h,M,y,alpha,Q=s.symbols('h M y alpha Q',positive=True)
checks=[]
def test(name,v):
 checks.append({'name':name,'passed':bool(v)});assert v,name
# Field-dependent threshold; y=|phi|². beta_e=e³/(48pi²) for one unit-charge complex scalar.
Leff=alpha/(48*s.pi)*s.log(1+h*y/M**2)
C=-s.diff(Leff,y).subs(y,0)
test('Wilson coefficient',s.simplify(C+alpha*h/(48*s.pi*M*M))==0)
# Independent beta-function integration in inverse-coupling convention, normalized back to A.
e=s.symbols('e',positive=True)
beta_e=e**3/(48*s.pi**2)
d_inverse=s.simplify(-2*beta_e/e**3)
threshold=s.simplify(-s.Rational(1,4)*(-d_inverse)*s.log(M/s.sqrt(M*M+h*y))*e*e)
test('RG threshold vs logarithm',s.simplify(s.diff(threshold,y).subs(y,0).subs(e**2,4*s.pi*alpha)+C)==0)
V=(M*M+h*y)**2/(32*s.pi**2)*(s.log((M*M+h*y)/Q**2)-s.Rational(3,2))
massshift=s.simplify(s.diff(V,y).subs({y:0,Q:M}))
test('complex scalar potential threshold',s.simplify(massshift+h*M*M/(16*s.pi**2))==0)
# Scalar vacuum-polarization Feynman-parameter weight independently integrates to b=1/3.
z=s.symbols('z');test('scalar beta weight',s.integrate((1-2*z)**2,(z,0,1))==s.Rational(1,3))
# Threshold logarithm identity by proper-time integral; dimensionless finite differences.
for shift in [.001,.1,1.]:
 val=quad(lambda t:math.exp(-t)*(-math.expm1(-shift*t))/t,0,math.inf,epsabs=1e-12)[0]
 test('proper time log '+str(shift),abs(val-math.log1p(shift))<1e-11)
rows=[];av=1/137.035999084;mv=1e6;hc=1.973269804e-7;c=299792458.;ev=1.602176634e-19
for mass in [1e7,1e8,1e9,1e11]:
 cv=-av/(48*math.pi*mass*mass)
 sig=4*cv*cv/(3*math.pi*mv*mv)*hc*hc # omega=1eV
 rate=8*c*sig/(mv*ev)
 rows.append({'messenger_mass_eV':mass,'portal_h':1,'C_eVminus2':cv,'abs_mass_threshold_over_m2':mass*mass/(16*math.pi**2*mv*mv),'production_s_over_messenger_mass2':(2*mv)**2/mass**2,'cooling_rate_s_inv_per_J_m3':rate})
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'C':str(C),'mass_shift_MSbar_at_Q_M':str(massshift),'rows':rows,'non_claims':['Hypothetical added electrically charged scalar; no evidence it exists','QED-level matching, not full electroweak or all-scale UV completion','Mass threshold is scheme-dependent naturalness diagnostic, not observable or exclusion']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
