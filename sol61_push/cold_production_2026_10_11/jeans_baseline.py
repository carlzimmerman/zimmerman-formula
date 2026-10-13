"""Collisionless Maxwellian Vlasov-Poisson baseline for the stipulated bath."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erfcx
p=Path(__file__).parent
G=6.67430e-11;rho=1e-21;sigma=200000.;kpc=3.0856775814913673e19;year=365.25*86400
omega=math.sqrt(4*math.pi*G*rho);lamJ=2*math.pi*sigma/omega
prior=json.loads((p/'resonant_kinetics_run/results.json').read_text())
mode_time=next(z['mode_relaxation_Gyr'] for z in prior['rows'] if z['rho_kg_m3']==rho and z['sigma_1d_kms']==200)
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def volterra(a,N,T=12.):
 t=np.linspace(0,T,N+1);dt=T/N;free=np.exp(-.5*(a*t)**2);kernel=t*free;d=np.zeros(N+1);d[0]=1
 for j in range(1,N+1):d[j]=free[j]+dt*(np.dot(kernel[1:j+1][::-1],d[:j])-.5*kernel[j]*d[0])
 return t,d
rows=[]
for wavelength in [10.,50.,100.,1000.]:
 a=lamJ/(wavelength*kpc);gamma=None
 if a<1:
  gamma=brentq(lambda gam:1-math.sqrt(math.pi)*gam/(math.sqrt(2)*a)*erfcx(gam/(math.sqrt(2)*a))-a*a,0,1,xtol=1e-14)
  integral=quad(lambda t:t*math.exp(-.5*a*a*t*t-gamma*t),0,math.inf,epsabs=1e-11)[0]
  check('dispersion matches Laplace kernel',abs(integral-1)<1e-10)
 else:check('no positive growth root',1/(a*a)<1)
 t1,d1=volterra(a,2048);t2,d2=volterra(a,4096)
 rel=float(max(abs(d1-d2[::2])/(1+abs(d2[::2]))))
 check('Volterra grid refinement',rel<1e-4)
 growth=float(np.polyfit(t2[t2>=8],np.log(d2[t2>=8]),1)[0])
 if gamma is not None:check('time growth matches dispersion',abs(growth-gamma)<.003)
 efold=1/(omega*gamma)/year/1e6 if gamma is not None else None
 rows.append(dict(wavelength_kpc=wavelength,k_over_kJ=a,unstable=gamma is not None,growth_over_omegaJ=gamma,efolding_Myr=efold,kinetic_mode_time_over_gravity_efold=mode_time*1000/efold if efold else None,volterra_tolerance_difference=rel,late_time_growth_over_omegaJ=growth,density_amplification_at_12_Jeans_times=float(d2[-1])))
# At marginal a=1, d(t)=1 solves the Volterra equation exactly.
t,d=volterra(1.,4096);check('marginal benchmark',max(abs(d-1))<1e-4)
scales=json.loads((p/'repulsive_scales_run/results.json').read_text());mass=1e-12*1.602176634e-19/299792458.**2
quantum=(1.054571817e-34*(2*math.pi/(10*kpc))/(mass*sigma))**2
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,rows=rows,Jeans_wavelength_kpc=lamJ/kpc,Jeans_time_Myr=1/omega/year/1e6,source_mode_time_Gyr=mode_time,contact_pressure_over_kinetic_pressure=scales['coherent_contact_speed_m_s']**2/sigma**2,quantum_gradient_parameter_at_10kpc=quantum,non_claims=['Homogeneous mean-subtracted collisionless Jeans problem, not a finite equilibrium halo','No collision-induced shift of stability threshold','No nonlinear collapse, baryons, cosmic expansion or halo profile'])
(p/'jeans_baseline_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
