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
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def local(x,Q):
 esc=esc0/math.sqrt(1+x*x);rhoSI=rho0/(1+x*x)**2.5;n=rhoSI*c*c/ev*hc**3/m
 amplitude=n/(w0*math.sqrt(2)*esc**1.5*betaf(1.5,4.5))
 if esc<=.5:return dict(x=x,escape_energy=esc,charge_rate_per_Gyr=0.,spontaneous_escape_geometry=0.)
 z,w=leggauss(Q);qmax=math.sqrt(2*esc-1);qsplit=math.sqrt(2*esc)-1
 total=escape=0.;maxorb=-math.inf
 for lo,hi in [(0.,qsplit),(qsplit,qmax)]:
  qs=lo+(hi-lo)*(z+1)/2;wq=w*(hi-lo)/2
  ec=1+qs*qs;half=np.minimum(qs,esc-ec/2)
  e1=ec[:,None]/2+half[:,None]*z;e2=ec[:,None]-e1
  shape=np.maximum(1-e1/esc,0)**3.5*np.maximum(1-e2/esc,0)**3.5
  inner=half*(shape@w);weight=wq*2*qs*inner
  total+=float(sum(weight));escape+=float(np.dot(weight,1-half/qs))
  maxorb=max(maxorb,float(max(qs*qs/2-esc)))
 check('new sources bound by resonance energy gap',maxorb<=-.5+1e-12)
 rate=2*K0*amplitude*amplitude*total/(n*hbev)*year*1e9
 return dict(x=x,escape_energy=esc,charge_rate_per_Gyr=rate,spontaneous_escape_geometry=escape/total,maximum_sampled_source_orbital_energy_over_vstar2=maxorb)
def integrated(R,Q):
 z,w=leggauss(R);total=esc=inside=0.
 for lo,hi in [(0.,1.),(1.,xmax)]:
  xx=lo+(hi-lo)*(z+1)/2;ww=w*(hi-lo)/2
  for x,weight in zip(xx,ww):
   row=local(float(x),Q);massweight=3*x*x/(1+x*x)**2.5
   term=weight*massweight*row['charge_rate_per_Gyr'];total+=term;esc+=term*row['spontaneous_escape_geometry']
   if hi==1.:inside+=term
 return dict(radial_order=R,energy_order=Q,initial_global_source_charge_rate_per_Gyr=total,birth_weighted_spontaneous_escape_geometry=esc/total,birth_fraction_inside_scale_radius=inside/total)
check('Plummer central density relation',abs(3*mass/(4*math.pi*scale**3)/rho0-1)<1e-14)
check('finite total mass normalization',abs(quad(lambda x:3*x*x/(1+x*x)**2.5,0,math.inf)[0]-1)<1e-12)
for x in [0.,1.,2.]:
 esc=esc0/math.sqrt(1+x*x)
 I=quad(lambda e:math.sqrt(2*e)*(1-e/esc)**3.5,0,esc,epsabs=1e-12)[0]
 J=quad(lambda e:e*math.sqrt(2*e)*(1-e/esc)**3.5,0,esc,epsabs=1e-12)[0]
 check('occupation normalization',abs(I/(math.sqrt(2)*esc**1.5*betaf(1.5,4.5))-1)<1e-10)
 check('isotropic Jeans dispersion',abs(J/I-esc/4)<1e-10)
runs=[integrated(24,24),integrated(48,48),integrated(96,96)]
check('radial and energy refinement',abs(runs[-1]['initial_global_source_charge_rate_per_Gyr']/runs[-2]['initial_global_source_charge_rate_per_Gyr']-1)<1e-6)
check('escape geometry refinement',abs(runs[-1]['birth_weighted_spontaneous_escape_geometry']-runs[-2]['birth_weighted_spontaneous_escape_geometry'])<1e-7)
locals=[local(x,96) for x in [0.,.5,1.,2.,4.,xmax+.1]]
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,runs=runs,local_rows=locals,halo=dict(scale_radius_kpc=scale/kpc,total_mass_solar=mass/1.98847e30,central_escape_speed_kms=math.sqrt(12)*sigma0/1000,activation_radius_kpc=xmax*scale/kpc,activation_radius_over_scale=xmax),non_claims=['Chosen Plummer initial equilibrium, not a derived halo profile','Initial production rates only; no depletion or potential response','Escape probability is unweighted isotropic decay geometry, not actual Bose-stimulated evaporation','No baryons, vacuum coupling or acceleration law'])
(p/'bound_halo_reactions_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks:',len(checks));assert out['all_pass']
