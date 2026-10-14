"""Energy drift of a single moving scalar in prescribed isotropic monoenergetic light."""
import json,sys,math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
import sympy as s
checks=[]
def test(name,v):
 checks.append({'name':name,'passed':bool(v)});assert v,name
# Analytic soft recoil and zero-recoil drag coefficients using separate limits.
b,u,x,w=s.symbols('b u x w',real=True)
D=(1-b*u)/s.sqrt(1-b*b)
boost=(1-b*u+b*(u-b)*x)/(1-b*b)
weight=s.Rational(3,16)*(1-b*u)*D**4*(1-x)**2
zero_recoil=s.series(weight*(1-boost),b,0,3).removeO().expand()
drag=s.integrate(s.integrate(zero_recoil,(u,-1,1)),(x,-1,1))
test('soft drag coefficient',s.simplify(drag+4*b*b)==0)
recoil0=s.Rational(3,16)*(1-x)**2*w*(1-x)
heat=s.integrate(s.integrate(recoil0,(u,-1,1)),(x,-1,1))
test('soft recoil coefficient',s.simplify(heat-s.Rational(3,2)*w)==0)
# Output is dot K/(n_gamma*c*sigma0*omega), m=C=1; sigma0=4 omega^4/(3pi).
def kernel(beta,omega,N):
 q,wt=leggauss(N);mu=q[:,None];ang=q[None,:];weights=wt[:,None]*wt[None,:]
 gam=1/math.sqrt(1-beta*beta); dop=gam*(1-beta*mu)
 den=1+omega*dop*(1-ang)
 boost=gam*gam*(1-beta*mu+beta*(mu-beta)*ang)
 change=(den-boost)/den
 value=3/16*(1-beta*mu)*dop**4*(1-ang)**2/den**4*change
 return float(np.sum(weights*value))
rows=[]
for omega in [1e-6,1e-4,.001,.01]:
 rest=kernel(0,omega,48)
 test('stationary exact '+str(omega),abs(rest/(1.5*omega/(1+2*omega)**4)-1)<1e-9)
 root=brentq(lambda b:kernel(b,omega,48),0,.4,xtol=1e-14)
 root2=brentq(lambda b:kernel(b,omega,80),0,.4,xtol=1e-14)
 test('root quadrature '+str(omega),abs(root-root2)<1e-10)
 kval=root*root/((math.sqrt(1-root*root))*(1+math.sqrt(1-root*root)))
 low=kernel(root/2,omega,80);high=kernel(root*2,omega,80)
 test('heating below and cooling above '+str(omega),low>0 and high<0)
 rows.append({'omega_over_m':omega,'zero_drift_beta':root,'zero_drift_K_over_omega':kval/omega,'leading_K_over_omega':3/16,'heating_below':low,'cooling_above':high,'root_refinement_error':abs(root-root2)})
test('soft limit root',abs(rows[0]['zero_drift_K_over_omega']/(3/16)-1)<1e-5)
# Illustrative SI relaxation rate in leading soft approximation.
mv=1e6;omega=1.;coupling=1e-19;hc=1.973269804e-7;c=299792458.;ev=1.602176634e-19
sig0=4*coupling**2*omega**4/(3*math.pi*mv*mv)*hc*hc
rate_per_u=8*c*sig0/(mv*ev)
bench={'m_eV':mv,'omega_eV':omega,'C_eVminus2':coupling,'sigma0_m2':sig0,'leading_K_zero_eV':3*omega/16,'relaxation_s_inv_per_J_m3':rate_per_u,'u_J_m3_for_one_second_relaxation':1/rate_per_u,'nphoton_over_nopposite_for_relaxation_equal_annihilation':3/16*(mv/omega)**5}
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'rows':rows,'benchmark':bench,'non_claims':['Single-particle drift, not full distribution stationary state or condensate cooling','Prescribed isotropic monoenergetic unpolarized bath, no stimulated scattering','Unknown coupling; benchmark energy density not a physically controlled operating point']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
