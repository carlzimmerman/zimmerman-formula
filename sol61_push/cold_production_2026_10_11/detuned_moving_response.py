"""Continuum moving-source Born response to a fixed Gaussian daughter shell."""
import json,math
from pathlib import Path
from scipy.special import sici
from scipy.integrate import quad
from scipy.optimize import brentq
p=Path(__file__).parent
par=json.loads((p/'detuned_carrier_run/results.json').read_text())['parameters']
u=par['u'];eps=par['epsilon'];R=par['M_eV']/par['m_eV']
D=4*u*u/(eps*(math.sqrt(R*R+4*u*u)+R))
a=R*eps/(2*u*u);b=eps*eps/(2*u*u)
gamma=0.5772156649015328606
checks=[]
def check(n,v,tol):checks.append(dict(name=n,value=float(v),passed=bool(abs(v)<tol)))
def response(t,F=1.):
 si,ci=sici(D*t)
 I0=2*t*si+2*(math.cos(D*t)-1)/D
 I1=2*(gamma+math.log(D*t)-ci)
 return 2*F*F*(a*I0+b*I1)
def direct(t):
 # In y=delta*t, integrate by periods to avoid oscillatory quadrature aliasing.
 end=D*t;step=2*math.pi
 pieces=math.ceil(end/step)
 return 2*sum(quad(lambda y:(a+b*y/t)*t*(1 if y==0 else 4*math.sin(y/2)**2/y**2),j*step,min(end,(j+1)*step),epsabs=1e-11)[0] for j in range(pieces))
check('angular density integrates to one',a*D+b*D*D/2-1,1e-12)
for t in [.00001,.001,.1,1.]:check('analytic versus angular integral t='+str(t),response(t)-direct(t),1e-10)
check('initial quadratic response',response(1e-6)/(2e-12)-1,1e-7)
rows=[]
for t in [1.,10.,30.,50.,100.,200.,1000.]:
 # delta*t <=1 is the unresolved coherent low-momentum region.
 qcoh=math.sqrt(2*R*eps/t+eps*eps/t**2)/u
 rows.append(dict(x=t,Born_source_charge=response(t),asymptotic_source_charge=2*math.pi*a*t,q_coherent=qcoh,N_min_dq_below_qcoh_and_qNyquist_above_two=math.ceil(4/qcoh)))
tenth=brentq(lambda t:response(t)-.1,.001,100)
one=brentq(lambda t:response(t)-1,.001,1000)
out=dict(parameters=par,model='Stationary monochromatic isotropic classical Gaussian daughter shell, F=1; zero initial moving source, linear forced source, no backreaction',D=D,angular_density_coefficients=[a,b],rows=rows,x_at_Born_fraction_point_one=tenth,x_at_Born_fraction_one=one,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Not an evolution of the actual produced state','Born response fails when conversion appreciably changes daughters','No instability eigenvalue or nonlinear final fraction','Moving-source occupation is coherent driven response, not automatically irreversible particle production','Finite radial width, quartic shift, source remnant and expansion omitted'])
(p/'detuned_moving_response_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
