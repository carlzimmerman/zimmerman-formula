"""Exact audit of L293's declared hydrostatic surrogate, not of a full halo.

All numerical atmospheres here prescribe a point-source logarithmic potential
and P=rho*C(r). Neither assumption is established for the L290 action.
"""
from pathlib import Path
import json
import math
import sys
import numpy as np
import sympy as s
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
checks={}
def exact(name, expression):
    value=s.simplify(expression)
    assert value==0,(name,value)
    checks[name]=True

r,R,h,eta,c2,rhob=s.symbols('r R h eta c2 rhob',positive=True)
C=c2/(1+h*r);v2=eta*c2
lr=s.log((1+h*r)/(1+h*R))+eta*s.log(R/r)+eta*h*(R-r)
rh=rhob*s.exp(lr)
exact('boundary_normalization',lr.subs(r,R))
exact('hydrostatic_equation',(s.diff(rh*C,r)+rh*v2/r)/rh)
correct_slope=-v2/C-r*s.diff(C,r)/C
wrong_slope=-v2/C+r*s.diff(C,r)/C
exact('density_log_slope',r*s.diff(lr,r)-correct_slope)
exact('slope_error',wrong_slope-correct_slope+2*h*r/(1+h*r))
wrong_lr=-eta*(s.log(R/r)+h*(R-r))
wrong_residual=s.factor(C*s.diff(wrong_lr,r)+s.diff(C,r)+v2/r)
exact('wrong_density_residual',wrong_residual-(2*v2/r+s.diff(C,r)))

gamma,K,CR=s.symbols('gamma K CR',positive=True)
rho_inverse=K*r**(-gamma)
C_inverse=v2/gamma+(CR-v2/gamma)*(r/R)**gamma
exact('inverse_powerlaw_pressure',s.diff(rho_inverse*C_inverse,r)+rho_inverse*v2/r)
exact('inverse_boundary',C_inverse.subs(r,R)-CR)
exact('amplitude_preserves_slope',s.diff(s.log(rho_inverse),r)+gamma/r)

G=6.67430e-11;ms=1.98847e30;kpc=3.0856775814913673e19
c=299792458.;a0=1.2e-10;Mb=2e14*ms;AD=4e5
rM=math.sqrt(G*Mb/a0)/kpc;vf2=math.sqrt(G*Mb*a0);q=vf2/c**2;coef=AD/rM
def log_density(rad,boundary=5000.):
    return math.log1p(coef*rad)-math.log1p(coef*boundary)+q*math.log(boundary/rad)+q*coef*(boundary-rad)
def slope(rad):
    return -q*(1+coef*rad)+coef*rad/(1+coef*rad)
grid=np.geomspace(30.,5000.,8000);band=(grid>=75)&(grid<=420)
source_slopes=-q*(1+coef*grid)-coef*grid/(1+coef*grid)
correct_slopes=np.array([slope(x) for x in grid])
sol=solve_ivp(lambda x,z:[-q*(1+coef*math.exp(x))+coef*math.exp(x)/(1+coef*math.exp(x))],
              (math.log(5000.),math.log(30.)),[0.],method='DOP853',rtol=1e-12,atol=1e-12,
              dense_output=True,max_step=.05)
assert sol.success
probe=np.geomspace(30,5000,101)
ivp_error=max(abs(sol.sol(math.log(x))[0]-log_density(x)) for x in probe)
assert ivp_error<2e-9,ivp_error
rho_cos=.26*1.36e11*ms/(1000*kpc)**3
mass_integral,quad_error=quad(lambda x:x*x*math.exp(log_density(x)),30.,1400.,epsabs=0,epsrel=2e-11)
annulus_mass=4*math.pi*kpc**3*rho_cos*mass_integral/Mb
assert annulus_mass>1e20

# Existing project demonstration, reproduced without observational data:
# an actual core can have a nonzero fitted slope over a finite band.
rr=np.exp(np.linspace(math.log(20),math.log(2000),300));mask=(rr>=40)&(rr<=750)
rho_core=(1+(rr/200.)**2)**(-3.5/2)
core_fit=float(np.polyfit(np.log(rr[mask]),np.log(rho_core[mask]),1)[0])
assert abs(core_fit+1.573)<.003

# A single fitted band mean does not identify a profile or fix AD uniquely
# across observational footings. This is a diagnostic, not a fit to data.
def mean_slope(ad):
    zz=ad*grid[band]/rM
    return float(np.mean(-q*(1+zz)+zz/(1+zz)))
ad_mean_target=brentq(lambda ad:mean_slope(ad)+1.53,1e4,1e6)

result={
 'exact_checks':checks,
 'hydrostatic_solution':'rho(r)/rho(R) = (1+h*r)/(1+h*R) * (R/r)^eta * exp(eta*h*(R-r))',
 'correct_slope':s.sstr(correct_slope),
 'wrong_density_ODE_residual_divided_by_rho':s.sstr(wrong_residual),
 'inverse_pressure':'C(r)=v^2/gamma+(C_R-v^2/gamma)*(r/R)^gamma',
 'source_parameters':{'Mb_solar':2e14,'AD':AD,'outer_kpc':5000,'inner_mass_kpc':30,'mass_radius_kpc':1400},
 'source_formula_band_mean':float(source_slopes[band].mean()),
 'correct_formula_band_mean':float(correct_slopes[band].mean()),
 'correct_slope_at_75_200_420_kpc':{str(x):slope(x) for x in [75,200,420]},
 'density_1400_over_outer':math.exp(log_density(1400)),
 'annular_mass_30_1400_over_baryons':annulus_mass,
 'quadrature_relative_error_estimate':quad_error/mass_integral,
 'independent_log_density_IVP_max_error':ivp_error,
 'rM_kpc':rM,'gN_over_a0_at_75_420':[(rM/x)**2 for x in [75,420]],
 'core200_fit_slope_40_750':core_fit,
 'AD_for_mean_slope_minus_1p53_in_same_surrogate':ad_mean_target,
 'non_claims':['No self-gravitating halo: the enormous mass invalidates the prescribed baryon-only potential.',
               'P=rho*C(r) is a declared surrogate, not the EOS of L290.',
               'Band mean or cored-profile mimicry is not an observational fit.',
               'Deep-MOND point-source force is outside its asymptotic regime across the selected inner band.',
               'No theory viability or universal exclusion.']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['exact_checks','non_claims']},indent=2))
print('Exact hydrostatic audit and independent IVP check passed:',len(checks))
