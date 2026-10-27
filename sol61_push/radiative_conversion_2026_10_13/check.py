#!/usr/bin/env python3
"""Conditional radiative spectrum and full homogeneous two-field dynamics."""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import beta, betainc, gamma
from numpy.polynomial.legendre import leggauss
checks=[]
def check(name,actual,expected,atol=1e-9,rtol=1e-7):
 checks.append(dict(name=name,actual=float(actual),expected=float(expected),passed=bool(abs(actual-expected)<=atol+rtol*abs(expected))))
# Homogeneous carrier, no source elimination, no photon feedback or gravity.
rows=[]
for c,k in [(0.2,0.1),(0.3,0.2),(0.5,0.35)]:
 for seed in [0.,0.001,0.01]:
  delta=1.; y0=np.array([seed+0j,1.+0j]);Q0=seed**2+2
  def rhs(t,y):
   p,b=y
   return -1j*np.array([2*c*b*p.conjugate()+2*k*abs(p)**2*p,delta*b+c*p*p])
  times=np.linspace(0,100,4001)
  sol=solve_ivp(rhs,[0,100],y0,method='DOP853',t_eval=times,rtol=2e-11,atol=2e-13)
  assert sol.success
  p,b=sol.y;n=abs(p)**2;nb=abs(b)**2;S=2*(b.conjugate()*p*p).real
  Q=n+2*nb;D=delta*nb+c*S+k*n*n
  check(f'charge c={c} seed={seed}',np.max(abs(Q-Q0)),0,atol=2e-8)
  check(f'energy c={c} seed={seed}',np.max(abs(D-D[0])),0,atol=2e-8)
  check(f'neutral bilinear c={c} seed={seed}',np.max(abs(S-(D[0]-delta*(Q0-n)/2-k*n*n)/c)),0,atol=2e-7)
  if seed==0:check(f'classical zero seed c={c}',max(n),0,atol=1e-25)
  rows.append(dict(c=c,k=k,seed=seed,charge=Q0,initial_energy=float(D[0]),max_daughter_charge_fraction=float(max(n)/Q0),final_daughter_charge_fraction=float(n[-1]/Q0),source_min=float(min(nb)),max_abs_neutral_bilinear=float(max(abs(S))),linear_pump_growth_squared=4*c*c-0.25))
# Dirichlet photon-energy distribution from leading NR four-body phase space.
Z=gamma(4)**2*gamma(1.5)/gamma(9.5)
C=Z/(12*math.pi**4)
# Independent tensor Gauss-Legendre quadrature with exact daughter recoil
# within the NR kinetic-energy approximation; x=E1/delta, y=(1-x)*v.
def integrate(N,r,relativistic=False):
 z,w=leggauss(N);u=(z+1)/2;wu=w/2
 x=u[:,None,None];v=u[None,:,None];mu=z[None,None,:]
 y=(1-x)*v
 a=1-x-y; bvec=x*x+y*y+2*x*y*mu
 kinetic=a-r*bvec/4
 if relativistic:
  kinetic=(4*a+r*(a*a-bvec))/(4+4*r*a+r*r*(a*a-bvec))
 f=x**3*y**3*np.sqrt(np.maximum(kinetic,0))*(1-x)*(1-mu)**2
 weights=wu[:,None,None]*wu[None,:,None]*w[None,None,:]
 # divide angular integral 8/3, already in the rate prefactor
 return float(np.sum(f*weights)*3/8)
quadrature=[]
for r in [0.,1e-5,4e-4,.01]:
 a=integrate(64,r);b=integrate(128,r)
 check(f'phase space refinement delta/m={r}',b,a,atol=0,rtol=1e-4)
 if r==0:check('analytic simplex normalization',b,Z,atol=0,rtol=1e-5)
 assert 0<b<=Z*(1+1e-5)
 quadrature.append(dict(delta_over_m=r,integral_64=a,integral_128=b,ratio_to_leading=b/Z))
 if r>0:
  ra=integrate(64,r,True);rb=integrate(128,r,True)
  check(f'exact relativistic phase refinement delta/m={r}',rb,ra,atol=0,rtol=1e-4)
  quadrature[-1].update(relativistic_64=ra,relativistic_128=rb,relativistic_ratio_to_leading=rb/Z)
# Photon polarization sum independent of phase-space quadrature.
for mu in [-1.,-.3,0.,.8,1.]:
 s=math.sqrt(max(0,1-mu*mu));n1=np.array([0.,0.,1.]);n2=np.array([s,0.,mu])
 e1=[np.array([1.,0.,0.]),np.array([0.,1.,0.])]
 e2=[np.array([mu,0.,-s]),np.array([0.,1.,0.])]
 tsum=sum(((1-mu)*(-a@b)-(-n1@b)*(-n2@a))**2 for a in e1 for b in e2)
 check(f'polarization sum mu={mu}',tsum,2*(1-mu)**2)
# Visible window defined here as 400-700 nm; no visual-safety classification.
hc=1239.8419843320026;lo=hc/700;hi=hc/400
spectra=[]
for gap in [3.,5.,8.,399.960008]:
 a=min(1,lo/gap);b=min(1,hi/gap)
 spectra.append(dict(gap_eV=gap,photon_mode_eV=.4*gap,mean_photon_eV=8*gap/19,
  visible_photon_fraction=float(betainc(4,5.5,b)-betainc(4,5.5,a)),
  visible_radiated_energy_fraction=float(betainc(5,5.5,b)-betainc(5,5.5,a)),
  pair_total_mean_photon_energy_eV=16*gap/19,
  daughter_rms_speed_over_c_for_m_1MeV=math.sqrt(3*gap/(19*1e6))))
result=dict(all_passed=all(v['passed'] for v in checks),checks=checks,carrier_cases=rows,phase_space=quadrature,dirichlet_normalization=Z,branching_ratio_coefficient=C,spectra=spectra,
 scope='Conditional dimension-seven portal, tree level, weak coupling and leading delta/m spectrum; homogeneous mean-field carrier simulations have no photon or gravity feedback. No predicted absolute coupling, empirical identification or device.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));sys.exit(0 if result['all_passed'] else 1)
