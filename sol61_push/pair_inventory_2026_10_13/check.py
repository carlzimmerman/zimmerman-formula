"""Dilute, mixed neutral gas; prescribed beams; no dense-condensate claim."""
import json,math,sys
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
C,z,b,m,ng=s.symbols('C z b m ng',positive=True)
checks=[]
def test(name,x):
    checks.append({'name':name,'passed':bool(x)})
    assert x,name
# Crossed polarization sum has 4x production's incoming average.
Msum=8*C**2*z**2
sigma_ann=Msum/(32*s.pi*z*b) # 1/2 identical outgoing photons
av=s.simplify(sigma_ann*2*b)
test('annihilation sigma v',s.simplify(av-C**2*z/(2*s.pi))==0)
a=s.simplify(av.subs(z,4*m*m))
sigma_prod=C*C*z*b/(8*s.pi)
R=2*ng**2*sigma_prod
n2=s.simplify(R/a)
test('coupling cancels at equilibrium',s.simplify(n2-ng**2*z*b/(8*m*m))==0)
test('detailed balance ratio',s.simplify(sigma_prod/sigma_ann-b*b/2)==0)
# Dimensionless x=n/sqrt(R/a), tau=sqrt(R*a)t, dx/dtau=1-x²-l*x.
rows=[]
for loss in [0.,.1,1.,10.]:
    d=math.sqrt(loss*loss+4); xp=2/(d+loss); xm=-(d+loss)/2
    t=np.linspace(0,10,101)
    analytic=xp*(-np.expm1(-d*t))/(1-(xp/xm)*np.exp(-d*t))
    sol=solve_ivp(lambda t,y:[1-y[0]**2-loss*y[0]],(0,10),[0.],t_eval=t,rtol=1e-10,atol=1e-12)
    error=float(np.max(abs(sol.y[0]-analytic)))
    test('ODE analytic loss '+str(loss),sol.success and error<2e-9)
    test('equilibrium cap loss '+str(loss),xp<=1)
    rows.append({'loss_dimensionless':loss,'equilibrium_fraction':xp,'max_error':error})
# A nonrelativistic illustrative density, not the old dense condensate.
c=299792458.; ev=1.602176634e-19; hc=1.973269804e-7; mass=1e6
rho=1e-9; n=rho/(2*mass*ev/c**2)
table=[]
for K in [1e-6,.001,1.,5.]:
    E=mass+K; beta=math.sqrt(K*(2*mass+K))/E
    nphot=n*mass/E*math.sqrt(2/beta)
    intensity=nphot*E*ev*c
    wave=2*math.pi*hc/math.sqrt(K*(2*mass+K))
    table.append({'K_eV':K,'rho_total_kg_m3':rho,'density_each_m3':n,'intensity_per_beam_W_m2':intensity,'matter_to_beam_energy_density_ratio':math.sqrt(beta/2),'occupation_diagnostic_n_lambda3':n*wave**3})
    test('energy ratio '+str(K),math.isclose(rho*c*c/(2*intensity/c),math.sqrt(beta/2),rel_tol=1e-12))
# Conditional filling time, positive C values selected only for scaling.
base=table[2]; E=mass+1; beta=math.sqrt(2*mass+1)/E
coeffs=[]
for coupling in [1e-25,1e-22,1e-19]:
    aSI=2*coupling**2*mass**2/math.pi*hc**2*c
    tau=1/(aSI*n)
    coeffs.append({'C_eVminus2':coupling,'annihilation_a_m3_s':aSI,'time_to_90pct_equilibrium_s':math.atanh(.9)*tau,'C_s':coupling*4*E*E})
test('time scales C inverse square',math.isclose(coeffs[0]['time_to_90pct_equilibrium_s']/coeffs[1]['time_to_90pct_equilibrium_s'],1e6,rel_tol=1e-12))
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'annihilation_sigma_v':str(av),'equilibrium_n_squared':str(n2),'ode_cases':rows,'density_diagnostics':table,'conditional_filling_times':coeffs,'non_claims':['No actual C measurement or matching','Ideal cold nondegenerate well-mixed gas only; micro-eV row violates dilute occupation','No beam source, trap, dense Bose kinetics or gravity mechanism']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
