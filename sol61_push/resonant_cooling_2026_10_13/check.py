#!/usr/bin/env python3
"""Conditional nondegenerate radiative recycling; narrow and off-shell kernels."""
import json,math,sys,warnings
from pathlib import Path
from scipy.integrate import quad,IntegrationWarning
from scipy.special import gamma,kve
warnings.simplefilter('error',IntegrationWarning)
checks=[]
Z=gamma(4)**2*gamma(1.5)/gamma(9.5)
def association(theta):
 # Thermal integrals after E=delta+T*z; all photon energy is E-delta.
 a7=quad(lambda z:math.sqrt(1+theta*z)*z**7*math.exp(-z),0,150,epsabs=1e-8,epsrel=1e-10)[0]
 a8=quad(lambda z:math.sqrt(1+theta*z)*z**8*math.exp(-z),0,150,epsabs=1e-8,epsrel=1e-10)[0]
 return dict(theta=theta,association_over_decay_cooling=19/(2240*Z)*theta**9*a8,
             mean_association_photon_pair_energy_over_gap=theta*a8/a7)
def check(name,a,b,rtol=1e-6,atol=0.):
 checks.append(dict(name=name,actual=float(a),expected=float(b),passed=bool(abs(a-b)<=atol+rtol*abs(b))))
# x=relative kinetic energy / gap; theta=T/gap.
# Leading energy-dependent widths: r0 sqrt(x), rg x^(17/2).
def integral(theta,r0,rg,power,tol):
 center=1/theta;half=(r0+rg)/(2*theta)
 upper=max(100.,center+100*half)
 points={0.,upper,center}
 for s in [1,4,16,64,256]:
  for sign in [-1,1]:
   z=center+sign*s*half
   if 0<z<upper:points.add(z)
 points=sorted(points)
 def f(z):
  x=theta*z; width=r0*math.sqrt(x)+rg*x**8.5
  return z**power*math.exp(-z)/((x-1)**2+width**2/4)
 value=sum(quad(f,a,b,epsabs=tol,epsrel=tol,limit=200)[0] for a,b in zip(points,points[1:]))
 return theta**(power+1)*value
rows=[]
for r0 in [1e-3,1e-5]:
 for theta in [.5,.2,.1,.05,.02,.002]:
  rg=r0*1e-8
  I9=integral(theta,r0,rg,9,1e-9);I10=integral(theta,r0,rg,10,1e-9)
  check(f'quadrature refine rate theta={theta} r0={r0}',I9,integral(theta,r0,rg,9,1e-7),rtol=1e-6)
  check(f'quadrature refine cooling theta={theta} r0={r0}',I10,integral(theta,r0,rg,10,1e-7),rtol=1e-6)
  nwa=2*math.pi/(r0+rg)*math.exp(-1/theta)
  rows.append(dict(theta=theta,r0=r0,rg=rg,rate_integral=I9,cooling_integral=I10,
   full_over_narrow_rate=I9/nwa,full_over_narrow_cooling=I10/nwa,
   mean_photon_pair_energy_over_gap=(16/19)*I10/I9,
   offshell_low_T_cooling_ratio=I10/(gamma(11)*theta**11)))
# Both allowed tree attachments of the photon portal contribute off shell.
# At x=E/gap<1, compare their coherent sum to decay-side amplitude alone.
# The cooling-weighted daughter kinetic fraction z has Beta(3/2,9).
attachments=[]
normalization=gamma(1.5)*gamma(9)/gamma(10.5)
for x in [1e-5,.001,.01,.1]:
 ratio=quad(lambda z:z**.5*(1-z)**8*(1+(x-1)/(x*z-1))**2,0,1,epsabs=1e-12)[0]/normalization
 attachments.append(dict(E_over_gap=x,full_over_decay_attachment_cooling=float(ratio)))
check('two-attachment low-energy limit',attachments[0]['full_over_decay_attachment_cooling'],4,rtol=1e-5)
# Independent exact MB Bessel ratio vs NR detailed-balance expression.
thermal=[]
for m in [1e3,1e4,1e6]:
 delta=5.;M=2*m+delta
 for theta in [.2,.5,1.]:
  T=theta*delta
  exact=2*math.pi**2*M*M/(m**4*T)*kve(1,M/T)/kve(2,m/T)**2*math.exp(-delta/T)
  nr=(2*math.pi/T)**1.5*M**1.5/m**3*math.exp(-delta/T)
  check(f'exact MB versus NR m={m} theta={theta}',exact,nr,rtol=.02)
  thermal.append(dict(m=m,T=T,exact_over_NR=float(exact/nr)))
# Near-threshold limit also approximates M as 2m in the scattering integral.
# Physical examples at degeneracy eta=n*(2pi/(mT))^(3/2)=1e-4 and T=gap.
hbar=6.582119569e-16;hc=1.973269804e-7;eV=1.602176634e-19;c=299792458.;G=6.67430e-11
assoc=[association(t) for t in [1.,.5,.2,.1,.05,.02,.002]]
physical=[]
for m in [1e3,12500.,1e6]:
 delta=5.;M=2*m+delta;T=delta;L=10*M;eta=1e-4
 n=eta*(m*T/(2*math.pi))**1.5
 rho=n/hc**3*m*eV/c**2
 rgamma=Z*delta**8.5/(96*math.pi**5*M*math.sqrt(m)*L**6)/hbar
 nK=eta*2**1.5*math.exp(-delta/T) # leading M=2m thermal prefactor
 # Best possible recycling rate at fixed radiative width: lambda <= Gamma_gamma.
 tmin=(57/32)*(T/delta)/(nK*rgamma)
 physical.append(dict(m_eV=m,eta=eta,T_eV=T,density_kg_m3=rho,
  gamma_radiative_s_inv=rgamma,minimum_NWA_cooling_time_s=tmin,
  minimum_two_pole_NWA_cooling_time_s=tmin/(1+assoc[0]['association_over_decay_cooling']),
  gravitational_time_s=1/math.sqrt(4*math.pi*G*rho),
  cooling_to_gravity_time_ratio=tmin*math.sqrt(4*math.pi*G*rho),
  two_pole_cooling_to_gravity_time_ratio=tmin/(1+assoc[0]['association_over_decay_cooling'])*math.sqrt(4*math.pi*G*rho)))
# Bottleneck checks across branching ratios, including radiatively dominated decay.
bottlenecks=[]
for r in [1e-8,1.,1e8]:
 lam=r/(1+r)
 check(f'bottleneck lambda <= gamma_rad r={r}',max(0,lam-1),0,atol=1e-15)
 check(f'bottleneck lambda <= gamma0 r={r}',max(0,lam-r),0,atol=1e-15)
 bottlenecks.append(dict(gamma0_over_gamma_rad=r,effective_rate_over_gamma_rad=lam))
r=dict(all_passed=all(x['passed'] for x in checks),checks=checks,kernel_cases=rows,thermal_checks=thermal,
 radiative_association=assoc,
 low_energy_two_attachment_check=attachments,
 physical_NWA_bounds=physical,bottlenecks=bottlenecks,
 scope='Dilute Maxwell-Boltzmann; tabulated energy kernel retains decay-side attachment only. Full off-shell tree has two attachments; their subthreshold interference is checked separately. No complete thermal tree rate, coherent/Bose-enhanced kinetics, UV completion, thermalization/escape proof or apparatus.')
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
sys.exit(0 if r['all_passed'] else 1)
