import json,math,sys
from pathlib import Path
import sympy as s
from scipy.integrate import quad
mu,V,y,b=s.symbols('mu V y b',positive=True)
# Matching the GP profile slopes fixes the interface density.
assert s.expand((1-y*y)**2/2-(b*y*y+y**4/2)-(.5-(1+b)*y*y))==0
# Exact inside and outside GP equations in units xi=(2m mu_int)^-1/2.
x,z=s.symbols('x z',real=True)
f=s.tanh((z-x)/s.sqrt(2));h=s.sqrt(2*b)/s.sinh(s.sqrt(b)*(x+z))
assert s.simplify(-s.diff(f,x,2)-f+f**3)==0
assert s.simplify(s.trigsimp(-s.diff(h,x,2)+b*h+h**3))==0
m=1e6;delta=5.;X=2/7;eps=1e-4;lam=1e-6;kap=lam/(4*m*m);n=X*delta/(4*kap)
mu_int=2*kap*(1-eps)*n;E=delta*.7143737072979501/2
hc=1.973269804e-7;c=299792458.;G=6.67430e-11;xi=hc/math.sqrt(2*m*mu_int)
rows=[]
for depth in [1.,1.5,2.]:
 beta=depth/mu_int-1;y0=math.sqrt(mu_int/(2*depth))
 x0=math.sqrt(2)*math.atanh(y0);x1=math.asinh(math.sqrt(2*beta)/y0)/math.sqrt(beta)
 inside=math.tanh(x0/math.sqrt(2));outside=math.sqrt(2*beta)/math.sinh(math.sqrt(beta)*x1)
 di=-(1-inside*inside)/math.sqrt(2)
 do=-math.sqrt(2)*beta*math.cosh(math.sqrt(beta)*x1)/math.sinh(math.sqrt(beta)*x1)**2
 assert abs(inside-outside)<1e-12 and abs(di-do)<1e-12
 assert depth>mu_int and E+mu_int-depth>0
 # A gravitational potential depth comparison GMm/R, not a shell construction.
 radius=.005;mass=depth/m*c*c*radius/G
 rows.append(dict(depth_eV=depth,chemical_potential_eV=mu_int-depth,escaping_particle_kinetic_eV=E+mu_int-depth,
  interface_density_fraction=y0*y0,profile_value_mismatch=abs(inside-outside),profile_slope_mismatch=abs(di-do),
  outside_decay_length_m=xi/math.sqrt(beta),equivalent_GM_over_R_mass_at_5mm_kg=mass))
# Verify the positive-effective-coefficient obstruction over a bounded parameter family.
checks=[]
for d in [.1,1,10]:
 for k in [.1,1,10]:
  g=math.sqrt(.7*k*d)
  for chem in [-10,-1,0]:
   eff=k-g*g/(d-2*chem);assert eff>0
   checks.append(dict(delta=d,kappa=k,mu=chem,effective=eff))
out=dict(rows=rows,positive_coefficient_checks=checks,exact_profile_identities=3,
 bulk_interaction_chemical_potential_eV=mu_int,quasiparticle_energy_eV=E,
 necessary_trap_depth_window_eV=[mu_int,mu_int+E],healing_length_m=xi,
 scope='No-binding argument for the untrapped repulsive carrier; explicitly added external one-body square well in a leading single-field interface model. No microscopic trap operator or interface scattering derived.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
