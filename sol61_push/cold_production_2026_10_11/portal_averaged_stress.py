"""Frozen-distribution portal response using a produced spatial intensity sample."""
import json,math
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.integrate import solve_ivp,quad
from scipy.optimize import minimize_scalar
p=Path(__file__).parent
sample=json.loads((p/'portal_intensity_run/results.json').read_text())['rows'][0]
z=np.array(sample['normalized_intensity_samples'])
cosmo=json.loads((p/'portal_cosmology_run/results.json').read_text())
portal=json.loads((p/'nonlinear_portal_run/results.json').read_text())
G=6.67430e-11;c=299792458.;Mpc=3.0856775814913673e22
bg=cosmo['background'];rm0=bg['rhom0_kg_m3'];rr0=bg['rhor0_kg_m3'];rL=bg['rhoLambda_kg_m3'];rho0=1e-21
Hsound=portal['softened']['Astar_over_m2']*c*c/2
li=math.log(bg['initial_a']);checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
def response(x):return float(x*np.mean(z*z/(1+(x*z)**2)**1.5))
def pressure(x):
 v=x*z;r=np.hypot(1,v)
 return float(np.mean(v*v/(r*(r+1))))
check('normalized empirical intensity',abs(np.mean(z)-1)<1e-14)
check('strictly positive represented intensities',np.min(z)>0)
rows=[]
for x in [.001,.01,.1,1.,10.,100.,1000.]:
 value=response(x);coherent=x/(1+x*x)**1.5;h=x*1e-4
 derivative=(pressure(x+h)-pressure(x-h))/(2*h)
 check('pressure derivative at frozen distribution',abs(derivative/value-1)<1e-5)
 rows.append(dict(mean_density_over_crossover=x,response_over_Hsound=value,
                  response_over_coherent=value/coherent,pressure_over_Astar_S0=pressure(x)))
check('dilute bunching enhancement',abs(response(1e-6)/1e-6/np.mean(z*z)-1)<1e-8)
# Compare a two-component equal-variance Gaussian intensity model at crossover.
gamma2=quad(lambda q:4*q*math.exp(-2*q)*q*q/(1+q*q)**1.5,0,math.inf,epsabs=1e-11)[0]

def solve_grid(N):
 grid=np.linspace(math.log(rm0/rho0)-.01,math.log(rm0/rho0)-3*li+.01,N)
 interp=PchipInterpolator(grid,np.log([response(math.exp(v)) for v in grid]))
 def rhs(k):
  def fun(l,y):
   a=math.exp(l);rm=rm0/a**3;rr=rr0/a**4;H2=8*math.pi*G*(rm+rr+rL)/3
   slope=-(3*rm+4*rr)/(2*(rm+rr+rL))
   cs2=Hsound*math.exp(float(interp(math.log(rm/rho0))))
   return [y[1],-(2+slope)*y[1]+(4*math.pi*G*rm/H2-cs2*(k/Mpc)**2/(a*a*H2))*y[0]]
  return fun
 out=[]
 for k in [.1,.3,1.,3.,10.]:
  s=solve_ivp(rhs(k),(li,0),[1.,1.],rtol=2e-10,atol=2e-12,max_step=.01)
  assert s.success
  out.append(dict(k_per_Mpc=k,final_amplitude_over_pressureless=float(s.y[0,-1]/cosmo['pressureless_growth'])))
 return out
coarse=solve_grid(301);fine=solve_grid(601)
for a,b in zip(coarse,fine):check('response interpolation refinement',abs(a['final_amplitude_over_pressureless']-b['final_amplitude_over_pressureless'])<1e-5)
peak=minimize_scalar(lambda lx:-response(math.exp(lx)),bounds=(-5,5),method='bounded')
out=dict(all_pass=all(q['passed'] for q in checks),checks=checks,
 intensity_statistics=dict(count=len(z),mean=float(np.mean(z)),second_moment=float(np.mean(z*z)),
                          minimum=float(np.min(z)),maximum=float(np.max(z))),
 response_rows=rows,equal_two_gaussian_crossover_response_over_Hsound=gamma2,
 peak_mean_density_over_crossover=math.exp(peak.x),peak_partial_response_speed_kms=math.sqrt(-peak.fun*Hsound)/1000,
 growth_rows=fine,
 non_claims=['Frozen intensity-distribution partial derivative, not derived dynamical sound speed',
 'Single classical seed and finite grid; no ensemble or continuum distribution',
 'No evolution of correlations, kinetic stress, reactions or local density shape through dilution',
 'Growth comparison retains the earlier one-fluid closure limitations'])
(p/'portal_averaged_stress_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
