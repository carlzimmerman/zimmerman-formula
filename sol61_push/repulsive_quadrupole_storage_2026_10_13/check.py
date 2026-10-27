"""Maxwell-compatible local quadrupole and scalar B^2 trapping audit."""
import json,math,sys
from pathlib import Path
import sympy as s
from scipy.integrate import quad
prior=json.loads(Path('sol61_push/muon_portal_magnetic_storage_2026_10_13/run/results.json').read_text())
kappa=abs(prior['U_10T_eV'])/100
hc=1.973269804e-7;hbar=6.582119569e-16;c=299792458.;m=1e6;grav=9.80665
checks=[]
def ck(name,ok):
 checks.append({'name':name,'passed':bool(ok)});assert ok,name
x,y,z,b,q,h,M=s.symbols('x y z b q h M',positive=True)
B=s.Matrix([b*x,b*y,-2*b*z])
ck('div B zero',s.diff(B[0],x)+s.diff(B[1],y)+s.diff(B[2],z)==0)
ck('curl B zero',s.Matrix([s.diff(B[2],y)-s.diff(B[1],z),s.diff(B[0],z)-s.diff(B[2],x),s.diff(B[1],x)-s.diff(B[0],y)])==s.zeros(3,1))
psi=s.exp(-q*(x*x+y*y+2*z*z)/2)
# kappa*b^2=h^2*q^2/(2M); h denotes hbar*c and M mass-energy.
Hpsi=-h*h/(2*M)*sum(s.diff(psi,v,2) for v in [x,y,z])+h*h*q*q/(2*M)*(x*x+y*y+4*z*z)*psi
ck('anisotropic oscillator ground eigenfunction',s.simplify(Hpsi/psi-2*h*h*q/M)==0)
a=s.symbols('a',positive=True);f=s.symbols('f',real=True)
ck('gravity square completion',s.expand(4*a*z*z+f*z-(4*a*(z+f/(8*a))**2-f*f/(16*a)))==0)
rows=[]
for gradient,radius in [(100.,.01),(1000.,.01),(.001,10000.)]:
 w=hc*gradient*math.sqrt(2*kappa/m)
 ell=math.sqrt(hc*hc/(m*w));E0=2*w
 wall=kappa*gradient**2*radius**2 # equatorial value on a hypothetical spherical boundary
 omega=w/hbar
 sag=grav/(4*omega**2)
 # Independently from force balance in energy-per-length units.
 sag_force=m*grav/(8*c*c*kappa*gradient**2)
 ck('gravity force-frequency agreement '+str(gradient),math.isclose(sag,sag_force,rel_tol=2e-9))
 # Numerical Gaussian ground probability within the equatorial x,y disk.
 disk=quad(lambda t:2*t*math.exp(-t*t),0,radius/ell,epsabs=1e-14)[0]
 ck('radial Gaussian integral '+str(gradient),math.isclose(disk,-math.expm1(-(radius/ell)**2),rel_tol=1e-10,abs_tol=1e-14))
 rows.append({'gradient_T_per_m':gradient,'radius_m':radius,'equatorial_B_T':gradient*radius,
 'axial_B_on_sphere_T':2*gradient*radius,'hbar_omega_xy_eV':w,'ground_energy_eV':E0,
 'oscillator_length_xy_m':ell,'equatorial_boundary_energy_eV':wall,'ground_over_boundary':E0/wall,
 'ground_probability_in_xy_disk':disk,'Earth_gravity_sag_m':sag,
 'sag_inside_radius':sag<radius,'vacuum_source_K_over_boundary':1e-9/wall})
# Necessary force balance somewhere inside sphere, not sufficient retention:
# |dU/dz| <= 8 kappa b^2 a.
radius=.01
b_grav=math.sqrt(m*grav/(8*c*c*kappa*radius))
b_quant=2*hc*math.sqrt(2/(m*kappa))/radius**2
Bedge=10.
a_quant=2*hc*math.sqrt(2/(m*kappa))/Bedge
result={'all_pass':all(v['passed'] for v in checks),'checks':checks,
 'kappa_eV_per_T2':kappa,'rows':rows,
 'gradient_ground_equals_boundary_at_1cm_T_per_m':b_quant,
 'gradient_gravity_sag_equals_radius_at_1cm_T_per_m':b_grav,
 'equatorial_B_at_gravity_sag_equality_T':b_grav*radius,
 'radius_ground_equals_boundary_at_equatorial_10T_m':a_quant,
 'B_barrier_equals_vacuum_K_T':math.sqrt(1e-9/kappa),
 'non_claims':['Local quadrupole is not a global finite-coil barrier specification',
 'Infinite harmonic eigenstates do not establish finite-trap resonances or lifetimes',
 'Sag assumes ordinary gravitational and inertial mass equality',
 'Extreme gradients are extrapolated scales, not validated apparatus designs']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
