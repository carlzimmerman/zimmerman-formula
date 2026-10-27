"""Bulk acoustic reference and exact reference-well energy sensitivities."""
import json,math,sys
from pathlib import Path
from scipy.integrate import quad
from scipy.optimize import brentq
prior=json.loads(Path('sol61_push/stable_window_retention_2026_10_14/run/retention.json').read_text())
source=json.loads(Path('sol61_push/stable_window_retention_2026_10_14/run/source.json').read_text())
c=299792458.;ev=1.602176634e-19;hb=1.054571817e-34;hbe=hb/ev;hc=hbe*c;kb=1.380649e-23;mass=ev/c**2;rho=2201.;checks=[]
def ck(name,e,t):
 assert e<t,(name,e,t)
 checks.append(dict(name=name,error=float(e),tolerance=t))
def mode(a,U):
 z0=a/hc*math.sqrt(2*U)
 z=brentq(lambda z:z/math.tan(z)+math.sqrt(z0*z0-z*z),math.pi/2+1e-12,min(z0,math.pi)-1e-12,xtol=1e-14)
 beta=math.sqrt(z0*z0-z*z);norm=.5-math.sin(2*z)/(4*z)+math.sin(z)**2/(2*beta)
 return hc**2*z*z/(2*a*a),math.sin(z)**2/(2*beta*norm),-U*math.sin(z)**2/(a*norm)
rows=[];noise=[]
for src in source['rows']:
 pole=[x for x in prior['rows'] if x['candidate']==src['candidate']][-1];a=pole['radius_m'];U=pole['barrier_eV'];E,Pout,Ea=mode(a,U)
 for step in [1e-4,1e-5]:
  du=(mode(a,U*(1+step))[0]-mode(a,U*(1-step))[0])/(2*U*step)
  da=(mode(a*(1+step),U)[0]-mode(a*(1-step),U)[0])/(2*a*step)
  ck('HF_U_'+src['candidate']+'_'+str(step),abs(du/Pout-1),2e-7)
  ck('HF_a_'+src['candidate']+'_'+str(step),abs(da/Ea-1),2e-7)
 Kdensity=2*U*Pout/hbe;Kradius=2*a*Ea/hbe;Kstrain=Kradius-3*Kdensity;target=1e-6
 noise.append(dict(candidate=src['candidate'],outside_probability=Pout,energy_derivative_eV_per_m=Ea,pair_frequency_per_fractional_barrier_per_s=Kdensity,pair_frequency_per_fractional_radius_per_s=Kradius,pair_frequency_per_uniform_dilation_per_s=Kstrain,assigned_phase_decay_budget_per_s=target,one_sided_fractional_barrier_ASD_limit_per_sqrt_Hz=2*math.sqrt(target)/abs(Kdensity),one_sided_uniform_dilation_ASD_limit_per_sqrt_Hz=2*math.sqrt(target)/abs(Kstrain)))
 for cs in [3000.,6000.,10000.]:
  q0=2*mass*cs/hb;epsilon=hb*cs*q0
  for T in [1.,4.,300.]:
   b=epsilon/(kb*T);nb=1/math.expm1(b)
   rate=(U*ev)**2*q0**3*nb/(2*math.pi*rho*hb*cs**2)
   # Independent natural-unit expression, rho is mass-energy density.
   rhon=rho*c*c/ev*hc**3;v=cs/c;qn=2*v
   natural=U*U*qn**3*nb/(2*math.pi*rhon*v*v)/hbe
   ck('SI_vs_natural_'+src['candidate']+'_'+str(cs)+'_'+str(T),abs(natural/rate-1),1e-12)
   rows.append(dict(candidate=src['candidate'],assigned_sound_speed_m_s=cs,temperature_K=T,phonon_wave_number_per_m=q0,phonon_wavelength_m=2*math.pi/q0,absorbed_energy_eV=epsilon/ev,free_particle_bulk_absorption_rate_per_s=rate,rate_times_comparison_duration=rate*src['weak_no_loss_time_for_probability_001_s']))
  # Gaussian delta regularization around the nonzero energy-conservation root.
  b=epsilon/(kb*300)
  for width in [.001,.0005]:
   integrand=lambda y:y**3*math.expm1(b)/math.expm1(b*y)*math.exp(-((y*y-y)/width)**2)/(math.sqrt(math.pi)*width)
   ratio=quad(integrand,.5,1.5,points=[1-10*width,1,1+10*width],epsabs=1e-11,epsrel=1e-11)[0]
   ck('delta_integral_'+src['candidate']+'_'+str(cs)+'_'+str(width),abs(ratio-1),1e-5)
result=dict(scope='Assigned isotropic homogeneous bulk single-acoustic-phonon absorption for a free carrier at rest, plus reference-well diagonal noise sensitivities; not finite-trap ejection rate or complete wall loss',bulk_rows=rows,noise_sensitivities=noise,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(noise_sensitivities=noise,room_temperature_6000m_s=[x for x in rows if x['temperature_K']==300 and x['assigned_sound_speed_m_s']==6000],passed=len(checks)),indent=2))
