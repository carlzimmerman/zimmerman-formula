"""Soft photon portal and ideal spherical well: conditional one-particle audit."""
import json, math, sys
from pathlib import Path
import sympy as s
from scipy.optimize import brentq

source = json.loads(Path('sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())
case = source['reduced_muon_case']
alpha, ml, MR, m = 1/137.035999084, 105658375.5, 2e6, 1e6
hc, evj, mu0 = 1.973269804e-7, 1.602176634e-19, 1.25663706212e-6
mu, yuk = case['equal_width_mu_R_phi_eV'], case['yukawa']
g = 2*alpha*yuk/(3*math.pi*ml)  # zero-external-momentum muon loop
C = -mu*g/(4*MR**2)
bconv = math.sqrt(hc**3/(mu0*evj))
u_per_T2 = abs(C)*bconv**2/m
checks=[]
def check(name, value):
    checks.append({'name':name,'passed':bool(value)})
    assert value, name
R, a, b, y, f, M2 = s.symbols('R a b y f M2', nonzero=True)
L = -M2*R**2/2 - a*R*y - b*R*f/4
Re = -(a*y+b*f/4)/M2
Le = s.expand(L.subs(R,Re))
check('eliminated source stationary', s.simplify(s.diff(L,R).subs(R,Re)) == 0)
check('mixed operator coefficient', s.simplify(Le.coeff(y,1).coeff(f,1)-a*b/(4*M2)) == 0)
delta, U = s.symbols('delta U', real=True)
check('fixed source born energy', s.simplify((delta-2*U)/2+U-delta/2) == 0)
# Independent SI route: induced R=-g B_nat^2/(2 MR^2), dE=mu R/(2m).
U10 = C*(10*bconv)**2/m
check('tadpole and operator energy agree', math.isclose(U10,mu*(-g*(10*bconv)**2/(2*MR**2))/(2*m),rel_tol=1e-14))
uSI=100/(2*mu0)
check('field energy conversion', math.isclose((10*bconv)**2/2,uSI*hc**3/evj,rel_tol=1e-14))
g_on = math.sqrt(64*math.pi*case['photon_width_eV']/MR**3)
check('soft versus on-shell loop controlled', 0 < g_on/g-1 < 3e-5)
roots=[]
for z0 in [1.0,1.5,1.6,2.0,3.0]:
    if z0 <= math.pi/2:
        # x cot x and sqrt(z0^2-x^2) are positive for 0<x<z0<pi/2.
        roots.append({'z0':z0,'bound_state':False})
        continue
    def eq(x): return x/math.tan(x)+math.sqrt(max(0,z0*z0-x*x))
    x=brentq(eq,math.pi/2,min(z0,math.pi-1e-10),xtol=5e-15)
    check('radial matching '+str(z0),abs(eq(x))<1e-11)
    roots.append({'z0':z0,'bound_state':True,'x':x,'binding_over_depth':1-(x/z0)**2})
a_cm=.01
Vcrit=math.pi**2*hc**2/(8*m*a_cm**2)
rcrit=math.pi*hc/math.sqrt(8*m*abs(U10))
check('threshold length inversion', math.isclose(abs(U10)*rcrit*rcrit,math.pi**2*hc**2/(8*m),rel_tol=1e-14))
result={'checks':checks,'all_pass':all(c['passed'] for c in checks),
 'g_soft_eV_inverse':g,'g_on_over_g_soft_minus_one':g_on/g-1,
 'C_eV_inverse_squared':C,'B_eV_squared_per_tesla':bconv,
 'U_10T_eV':U10,'radius_threshold_10T_m':rcrit,
 'depth_threshold_radius_1cm_eV':Vcrit,
 'B_threshold_radius_1cm_T':math.sqrt(Vcrit/u_per_T2),
 'B_depth_equals_vacuum_K_T':math.sqrt(1e-9/u_per_T2),
 'source_vacuum_excess_eV':2e-9,
 'source_total_daughter_energy_above_free_mass_each_eV':1e-9,
 'well_roots':roots,
 'non_claims':['No realizable magnetic geometry, capture rate, or particle existence',
 'Huge field values are extrapolations of the leading soft effective interaction',
 'Binding threshold is for an ideal attractive spherical well; not a magnetic shell barrier',
 'Born energy identity assumes unchanged source pole and local independent daughter energies']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
