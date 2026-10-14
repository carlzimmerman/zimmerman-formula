"""Elastic photon scattering from the same contact operator; target initially at rest."""
import json,sys,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
C,m,w,t=s.symbols('C m w t',positive=True)
z=m*m+2*m*w; A=(z-m*m)**2/z
# Incoming photon average (2), outgoing photon sum (2), no scalar spin.
ds=C*C*t*t/(4*s.pi*(z-m*m)**2)
sigma=s.simplify(s.integrate(ds,(t,-A,0)))
recoil=s.simplify(s.integrate(-t/(2*m)*ds,(t,-A,0))/sigma)
checks=[]
def test(name,x):
 checks.append({'name':name,'passed':bool(x)});assert x,name
test('total cross section',s.simplify(sigma-C*C*(z-m*m)**4/(12*s.pi*z**3))==0)
test('mean recoil',s.simplify(recoil-3*A/(8*m))==0)
test('soft cross section',s.simplify(s.limit(sigma/w**4,w,0)-4*C*C/(3*s.pi*m*m))==0)
# Independent physical-polarization evaluation in the target-rest frame.
g=s.diag(1,-1,-1,-1)
def dot(a,b):return (a.T*g*b)[0]
x=s.symbols('x',real=True);v=s.sqrt(1-x*x);wp=m*w/(m+w*(1-x))
k=s.Matrix([w,0,0,w]);kp=s.Matrix([wp,wp*v,0,wp*x])
ins=[s.Matrix([0,1,0,0]),s.Matrix([0,0,1,0])]
outs=[s.Matrix([0,x,0,-v]),s.Matrix([0,0,1,0])]
polsum=s.simplify(sum((4*C*(dot(k,kp)*dot(e,f)-dot(k,f)*dot(kp,e)))**2 for e in ins for f in outs)/2)
tvalue=-2*w*wp*(1-x)
test('polarization average equals 4 C2 t2',s.simplify(polsum-4*C*C*tvalue*tvalue)==0)
# Integrate lab angle using dt/dcos(theta), separately from symbolic t integral.
rows=[]
for ratio in [1e-6,.001,.1,1.]:
 # m=C=1 for normalized quadrature; scaled integrand avoids tiny absolute-error false pass.
 def f(x):
  wp=ratio/(1+ratio*(1-x));tt=-2*ratio*wp*(1-x)
  jac=2*ratio*ratio/(1+ratio*(1-x))**2
  return tt*tt*jac/(16*math.pi*ratio*ratio)/ratio**4
 val=quad(f,-1,1,epsabs=1e-12,epsrel=1e-12)[0]*ratio**4
 expected=4*ratio**4/(3*math.pi*(1+2*ratio)**3)
 test('lab angular integration '+str(ratio),abs(val/expected-1)<1e-10)
 rows.append({'omega_over_m':ratio,'sigma_over_C2m2':val,'recoil_over_m':1.5*ratio*ratio/(1+2*ratio),'nphoton_over_nopposite_for_equal_event_rates':(2/math.pi)/val})
# Event-rate ratio uses n_gamma sigma c versus n_opposite a, a/c=2 C²m²/pi.
bench=[];mv=1e6;hc=1.973269804e-7
for omega in [1.,1e3,1e5]:
 sv=4*omega**4/(3*math.pi*mv**2*(1+2*omega/mv)**3)
 bench.append({'omega_eV':omega,'sigma_m2_per_C_eVminus2_squared':sv*hc*hc,'mean_recoil_eV':1.5*omega*omega/(mv+2*omega),'photon_to_opposite_density_equal_event_rate':(2*mv*mv/math.pi)/sv})
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'sigma':str(sigma),'mean_recoil':str(recoil),'dimensionless_cases':rows,'benchmark_m_eV':mv,'benchmark':bench,'non_claims':['Single initially resting carrier; no net cooling calculation for moving distribution','No full loop form factor or empirical Wilson coefficient','Event-rate comparison assumes uncorrelated opposite species']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(bench,indent=2))
