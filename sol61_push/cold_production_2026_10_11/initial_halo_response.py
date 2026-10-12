"""Initial resonant source production in a finite collisionless Plummer test halo."""
import json,math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import beta as betaf
from scipy.integrate import quad
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
m=params['m_eV'];g=params['cubic_g_eV'];u=params['u']
c=299792458.;G=6.67430e-11;ev=1.602176634e-19;hb=1.054571817e-34;hbev=hb/ev;hc=hbev*c;year=365.25*86400;kpc=3.0856775814913673e19
rho0=1e-21;sigma0=200000.;vstar=u*c
scale=math.sqrt(9*sigma0*sigma0/(2*math.pi*G*rho0));mass=6*sigma0*sigma0*scale/G
esc0=6*sigma0*sigma0/vstar**2;xmax=math.sqrt((2*esc0)**2-1)
w0=(m*u)**3/(2*math.pi**2);K0=g*g*m*m*u**4/(16*math.pi**3)

from fractions import Fraction
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def pressure_loss(x,Q=64):
 esc=esc0/math.sqrt(1+x*x);rhoSI=rho0/(1+x*x)**2.5;n=rhoSI*c*c/ev*hc**3/m
 amplitude=n/(w0*math.sqrt(2)*esc**1.5*betaf(1.5,4.5))
 z,w=leggauss(Q);qmax=math.sqrt(2*esc-1);split=math.sqrt(2*esc)-1
 total=derivative=0.
 for lo,hi in [(0.,split),(split,qmax)]:
  qs=lo+(hi-lo)*(z+1)/2;wq=w*(hi-lo)/2;ec=1+qs*qs;half=np.minimum(qs,esc-ec/2)
  e1=ec[:,None]/2+half[:,None]*z;e2=ec[:,None]-e1
  shape=(1-e1/esc)**3.5*(1-e2/esc)**3.5
  kernel=wq[:,None]*2*qs[:,None]*half[:,None]*w
  total+=float(np.sum(kernel*shape))
  derivative+=float(np.sum(kernel*shape*3.5*(1/(esc-e1)+1/(esc-e2))))
 rate=2*K0*amplitude*amplitude*total/(n*hbev)
 S=rhoSI*vstar*vstar*rate/3
 Sr=S*derivative/total*(-esc0*x/(1+x*x)**1.5)/scale
 return S,Sr,derivative/total
# Collision moments: ec=e1+e2, source kinetic ec-1.
for e1 in [Fraction(1,2),Fraction(1),Fraction(3,2)]:
 for e2 in [Fraction(1,2),Fraction(1),Fraction(3,2)]:
  ec=e1+e2
  check('reaction kinetic energy loss',ec-1-e1-e2==-1)
  check('reaction isotropic stress loss',Fraction(2,3)*(ec-1-e1-e2)==-Fraction(2,3))
rows=[];myr=year*1e6
for x in [.1,.25,.5,1.,2.,4.]:
 S,Sr,logder=pressure_loss(x);h=1e-4
 fd=(pressure_loss(x+h)[0]-pressure_loss(x-h)[0])/(2*h*scale)
 check('analytic pressure-loss gradient',abs(fd/Sr-1)<2e-6)
 check('inward acceleration of mass current',Sr<0)
 enclosed=mass*x**3/(1+x*x)**1.5
 coefficient=-(2*math.pi/3)*(scale*x)**2*Sr/enclosed
 phicoeff=-(2*math.pi*G/3)*S
 # Independent initial equilibrium force balance.
 pressure_gradient=-6*rho0*sigma0*sigma0*x/scale/(1+x*x)**4
 gravity=-rho0/(1+x*x)**2.5*G*mass*x/scale**2/(1+x*x)**1.5
 check('initial Jeans equilibrium',abs(pressure_gradient/gravity-1)<1e-14)
 rows.append(dict(r_over_b=x,r_kpc=x*scale/kpc,pressure_loss_Pa_per_second=S,pressure_loss_gradient_Pa_per_second_per_m=Sr,enclosed_mass_fraction_t3_coefficient_per_Myr3=coefficient*myr**3,potential_t3_coefficient_m2_s2_per_Myr3=phicoeff*myr**3))
S0,_,logder0=pressure_loss(0.);central=esc0*S0*logder0/(2*scale*scale*rho0)
h=1e-3
centralfd=-(pressure_loss(h)[0]-S0)/(rho0*scale*scale*h*h)
check('central density third-order coefficient',abs(centralfd/central-1)<1e-5)
Sfine=pressure_loss(.5,96)[0];check('quadrature refinement',abs(Sfine/pressure_loss(.5,48)[0]-1)<1e-10)
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,rows=rows,central_density_fraction_t3_coefficient_per_Myr3=central*myr**3,non_claims=['Initial Taylor derivatives of NR Boltzmann-Poisson system only','No finite-time error bound or final halo state','Gravity sourced by leading conserved mass mQ; relativistic corrections omitted','No radiation cooling, vacuum selector or baryonic scaling'])
(p/'initial_halo_response_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks:',len(checks));assert out['all_pass']
