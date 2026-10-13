"""Declared single-fluid linear growth screen through the portal density crossover."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.optimize import minimize_scalar
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
portal=json.loads((p/'nonlinear_portal_run/results.json').read_text())
G=6.67430e-11;c=299792458.;Mpc=3.0856775814913673e22
rho0=1e-21;rho_source=rho0*portal['source_to_halo_density_ratio']
rhom0=rho_source/(1+params['z'])**3;rhoL=6e-27;rhor0=8e-31
H0sound=portal['softened']['Astar_over_m2']*c*c/2
ai=.001;li=math.log(ai)
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
def background(lna):
 a=math.exp(lna);rm=rhom0/a**3;rr=rhor0/a**4
 H2=8*math.pi*G*(rm+rr+rhoL)/3
 dlogH=-(3*rm+4*rr)/(2*(rm+rr+rhoL))
 x=rm/rho0;cs2=H0sound*x/(1+x*x)**1.5
 return a,rm,H2,dlogH,cs2

def growth(k,pressure,tol):
 kSI=k/Mpc
 def rhs(lna,z):
  a,rm,H2,dlogH,cs2=background(lna)
  acoustic=cs2*kSI*kSI/(a*a*H2) if pressure else 0.
  return [z[1],-(2+dlogH)*z[1]+(4*math.pi*G*rm/H2-acoustic)*z[0]]
 sol=solve_ivp(rhs,(li,0),[1.,1.],rtol=tol,atol=tol*1e-2,dense_output=True,max_step=.01)
 assert sol.success
 return sol
control=growth(0.,False,2e-10)
rows=[]
for k in [.1,.3,1.,3.,10.]:
 s=growth(k,True,2e-9);fine=growth(k,True,2e-11)
 ratio=float(fine.y[0,-1]/control.y[0,-1])
 check('ODE refinement',abs((s.y[0,-1]-fine.y[0,-1])/control.y[0,-1])<1e-6)
 rows.append(dict(k_per_Mpc=k,wavelength_Mpc=2*math.pi/k,
                  final_amplitude_over_pressureless=ratio,
                  squared_amplitude_ratio=ratio*ratio,
                  final_growth=float(fine.y[0,-1])))
zero=growth(0.,True,2e-10)
check('zero-wavenumber pressure decouples',abs(zero.y[0,-1]/control.y[0,-1]-1)<1e-12)
def kj(lna):
 a,rm,H2,dlogH,cs2=background(lna)
 return a*math.sqrt(4*math.pi*G*rm/cs2)*Mpc
minimum=minimize_scalar(kj,bounds=(li,0),method='bounded',options={'xatol':1e-12})
# Sound travel in comoving length: integral c_s/(a H) d ln a.
fun=lambda l:math.sqrt(background(l)[4]/background(l)[2])/background(l)[0]/Mpc
sound=quad(fun,li,0,epsabs=1e-9,epsrel=1e-10)[0]
soundearly=quad(fun,math.log(1e-6),li,epsabs=1e-9,epsrel=1e-10)[0]
across=(rhom0/rho0)**(1/3);apeak=(math.sqrt(2)*rhom0/rho0)**(1/3)
check('sound-speed peak location',abs(background(math.log(apeak))[4]/(H0sound*2/(3*math.sqrt(3)))-1)<1e-12)
# Independent EdS normalization check of the linear ODE without pressure.
eds=solve_ivp(lambda l,z:[z[1],-.5*z[1]+1.5*z[0]],(li,0),[1,1],rtol=1e-10,atol=1e-12)
check('Einstein-de Sitter growing solution',abs(eds.y[0,-1]*ai-1)<1e-8)
out=dict(all_pass=all(t['passed'] for t in checks),checks=checks,
 background=dict(rhom0_kg_m3=rhom0,rhoLambda_kg_m3=rhoL,rhor0_kg_m3=rhor0,
                 initial_a=ai,initial_D=1.,initial_dD_dloga=1.,
                 maximum_omitted_interaction_energy_over_rest=H0sound/c**2),
 crossover_redshift=1/across-1,sound_peak_redshift=1/apeak-1,
 peak_sound_speed_kms=math.sqrt(H0sound*2/(3*math.sqrt(3)))/1000,
 minimum_comoving_Jeans_k_per_Mpc=minimum.fun,Jeans_minimum_redshift=math.exp(-minimum.x)-1,
 comoving_sound_distance_from_ai_Mpc=sound,earlier_sound_distance_from_1e6_Mpc=soundearly,
 pressureless_growth=float(control.y[0,-1]),rows=rows,
 non_claims=['Single coherent barotropic matter fluid on declared radiation/matter/Lambda background',
 'Not a Boltzmann transfer function, CMB calculation or observational exclusion',
 'No baryon perturbations, radiation perturbations, reactions, incoherent stress or nonlinear collapse',
 'Initial growing perturbation is imposed, not derived from production'])
(p/'portal_cosmology_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
