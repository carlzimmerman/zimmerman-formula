"""Isolated pressure-only Newtonian spheres for the softened portal EOS."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad
p=Path(__file__).parent
prior=json.loads((p/'nonlinear_portal_run/results.json').read_text())
G=6.67430e-11;c=299792458.;rho0=1e-21;kpc=3.0856775814913673e19
H0=prior['softened']['Astar_over_m2']*c*c/2
r0=math.sqrt(H0/(4*math.pi*G*rho0));massunit=4*math.pi*rho0*r0**3
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
def run(xc,tol):
 yc=xc/math.hypot(1,xc);start=min(1e-5,1e-4/math.sqrt(xc))
 def rhs(r,z):
  y=max(0.,min(z[0],1-1e-15));root=math.sqrt(1-y*y)
  x=y/root;P=y*y/(1+root);xcs=y*y*root
  return [-z[1]/r**2,r*r*x,z[1]*x*r,r*r*P,r*r*(9*xcs-12*P)]
 def surface(r,z):return z[0]
 surface.terminal=True;surface.direction=-1
 init=[yc-xc*start**2/6,xc*start**3/3,xc*xc*start**5/15,
       (1-1/math.hypot(1,xc))*start**3/3,0.]
 sol=solve_ivp(rhs,(start,20),init,rtol=tol,atol=tol*1e-3,events=surface,dense_output=True,max_step=.025)
 assert sol.success and len(sol.t_events[0])==1
 radius=sol.t_events[0][0];y,mu,W,Pint,C=sol.y_events[0][0]
 check('stationary virial',abs(W/(3*Pint)-1)<2e-6)
 def energy(lam):
  def integrand(r):
   yy=max(0.,min(sol.sol(r)[0],1-1e-15));xx=yy/math.sqrt(1-yy*yy)
   z=lam**3*xx
   return r*r*z*z/(math.hypot(1,z)+1)/lam**3
  return quad(integrand,start,radius,epsabs=1e-11,epsrel=1e-9,limit=300)[0]-lam*W
 h=1e-3;curv_fd=(energy(1+h)-2*energy(1)+energy(1-h))/h**2
 check('independent homologous energy curvature',abs(curv_fd-C)<3e-5*max(W,abs(C)))
 return dict(central_density_over_rho0=xc,surface_dimensionless=radius,mass_dimensionless=mu,
             radius_kpc=radius*r0/kpc,mass_solar=mu*massunit/1.98847e30,
             surface_circular_speed_kms=math.sqrt(H0*mu/radius)/1000,
             homology_energy_curvature_over_binding_energy=C/W,
             homology_unstable=C<0,virial_relative_error=abs(W/(3*Pint)-1))
rows=[run(x,2e-9) for x in [.01,.1,.3,1.,3.,10.,30.,100.]]
refined=[run(x,2e-11) for x in [1.,10.,100.]]
for fine in refined:
 coarse=next(r for r in rows if r['central_density_over_rho0']==fine['central_density_over_rho0'])
 for k in ['mass_dimensionless','surface_dimensionless','homology_energy_curvature_over_binding_energy']:
  check('ODE refinement '+k,abs(fine[k]-coarse[k])<3e-6*max(1,abs(fine[k])))
check('low-density n=1 radius limit',abs(rows[0]['surface_dimensionless']/math.pi-1)<1e-4)
out=dict(all_pass=all(q['passed'] for q in checks),checks=checks,rows=rows,refined=refined,
         H0_m2_s2=H0,scale_radius_kpc=r0/kpc,
         non_claims=['Pressure-only coherent barotropic Newtonian fluid, not full reacting field',
                    'Positive trial energy curvature is not a stability proof',
                    'Negative curvature is an instability test only in retained fluid model',
                    'No baryons, kinetic stress, quantum gradients or formation calculation'])
(p/'portal_hydrostatic_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks',len(checks));assert out['all_pass']
