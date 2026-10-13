"""Linear expanding Vlasov-Hermite response for the stipulated local portal mean field."""
import math,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.interpolate import PchipInterpolator
p=Path(__file__).parent
z=np.array(json.loads((p/'portal_intensity_run/results.json').read_text())['rows'][0]['normalized_intensity_samples'])
cosmo=json.loads((p/'portal_cosmology_run/results.json').read_text())
fluid=json.loads((p/'portal_averaged_stress_run/results.json').read_text())
portal=json.loads((p/'nonlinear_portal_run/results.json').read_text())
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
G=6.67430e-11;c=299792458.;Mpc=3.0856775814913673e22
bg=cosmo['background'];rm0=bg['rhom0_kg_m3'];rr0=bg['rhor0_kg_m3'];rL=bg['rhoLambda_kg_m3'];ai=bg['initial_a'];li=math.log(ai)
Hsound=portal['softened']['Astar_over_m2']*c*c/2
sigma0=params['u']*c/(math.sqrt(3)*(1+params['z']))
grid=np.linspace(math.log(rm0/1e-21)-.01,math.log(rm0/1e-21)-3*li+.01,601)
response=lambda x:float(x*np.mean(z*z/(1+(x*z)**2)**1.5))
interp=PchipInterpolator(grid,np.log([response(math.exp(x)) for x in grid]))
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
def background(l):
 a=math.exp(l);rm=rm0/a**3;rr=rr0/a**4;H=math.sqrt(8*math.pi*G*(rm+rr+rL)/3)
 C=Hsound*math.exp(float(interp(math.log(rm/1e-21))))
 return a,rm,H,C

def evolve(k,N,velscale=1.,force=True,initial_velocity=True,tol=2e-10):
 kSI=k/Mpc
 def coefficients(l):
  a,rm,H,C=background(l);sig=velscale*sigma0/a
  b=kSI*sig/(a*H)
  F=kSI/(a*H*sig)*(C-4*math.pi*G*rm*a*a/kSI**2) if force else 0.
  return b,F
 def rhs(l,h):
  b,F=coefficients(l);dh=np.zeros_like(h)
  for n in range(N+1):
   if n>0:dh[n]+=b*math.sqrt(n)*h[n-1]
   if n<N:dh[n]-=b*math.sqrt(n+1)*h[n+1]
  dh[1]+=F*h[0]
  return dh
 h=np.zeros(N+1);h[0]=1.
 if initial_velocity:h[1]=-1/coefficients(li)[0]
 sol=solve_ivp(rhs,(li,0),h,rtol=tol,atol=tol*1e-2,max_step=.01)
 assert sol.success
 return float(sol.y[0,-1])
rows=[]
for k in [.1,.3,1.,3.,10.]:
 a=evolve(k,4);b=evolve(k,8);ref=evolve(k,8,tol=2e-12)
 cold=evolve(k,8,velscale=.1)
 f=next(v['final_amplitude_over_pressureless'] for v in fluid['growth_rows'] if v['k_per_Mpc']==k)
 check('Hermite refinement',abs(a-b)/cosmo['pressureless_growth']<1e-7)
 check('ODE refinement',abs(b-ref)/cosmo['pressureless_growth']<1e-7)
 check('cold limit approaches fluid control',abs(cold/cosmo['pressureless_growth']-f)<2e-6)
 rows.append(dict(k_per_Mpc=k,kinetic_amplitude_over_pressureless=ref/cosmo['pressureless_growth'],
                  fluid_amplitude_over_pressureless=f,ten_times_colder_amplitude_over_pressureless=cold/cosmo['pressureless_growth']))
free_distance=quad(lambda l:sigma0/(background(l)[0]**2*background(l)[2])/Mpc,li,0,epsabs=1e-12)[0]
# A larger but still NR dispersion resolves a measurable free-streaming control.
free=evolve(10,12,velscale=100,force=False,initial_velocity=False)
expected=math.exp(-.5*(10*100*free_distance)**2)
check('force-free Gaussian phase mixing',abs(free-expected)<1e-8)
out=dict(all_pass=all(v['passed'] for v in checks),checks=checks,rows=rows,
 sigma_today_m_s=sigma0,comoving_free_streaming_dispersion_Mpc=free_distance,
 non_claims=['Stipulated frozen-distribution mean-field coefficient; not derived nonlinear quantum kinetic closure',
 'Single Maxwellian component with redshifting dispersion; reactions and actual two-species distributions omitted',
 'No observed transfer spectrum or final halo law'])
(p/'portal_vlasov_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
