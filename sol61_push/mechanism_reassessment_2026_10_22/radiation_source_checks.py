"""Vacuum reduced scalar radiation from a mass-conserving spherical source."""
import sympy as s
from scipy.integrate import quad
import math,json,sys
from pathlib import Path
K,w,k,kap,gamma,M,eps,R=s.symbols('K omega k kappa gamma M epsilon R',positive=True)
rhot=s.symbols('rho_tilde',real=True)
A=-K*rhot/(4*s.pi*gamma*(k*k+kap*kap))
Pflux=4*s.pi*w*k*gamma*(k*k+kap*kap)*A*A/2
Pformula=K*K*w*k*rhot*rhot/(8*s.pi*gamma*(k*k+kap*kap))
checks={'far_field_flux_power':s.simplify(Pflux-Pformula)==0}
x=s.symbols('x',real=True)
checks['mass_conserving_form_factor_limit']=s.limit((-x*x*s.exp(-x*x/2))/(x*x),x,0)==-1
rho=lambda r:math.exp(-r*r/2)/(2*math.pi)**1.5*(r*r-3)
mass=quad(lambda r:4*math.pi*r*r*rho(r),0,math.inf,epsabs=1e-12)[0]
I=quad(lambda r:4*math.pi*r**4*rho(r),0,math.inf,epsabs=1e-12)[0]
checks['breathing_mass_zero']=abs(mass)<1e-12
checks['breathing_second_moment']=abs(I-6)<1e-11
rows=[]
for kval in [.1,1.,3.]:
 value=quad(lambda r:4*math.pi*r*r*rho(r)*(math.sin(kval*r)/(kval*r) if r else 1.),0,math.inf,epsabs=1e-12)[0]
 expected=-kval*kval*math.exp(-kval*kval/2)
 rows.append({'kR':kval,'quadrature':value,'exact':expected})
checks['source_transform']=max(abs(v['quadrature']-v['exact']) for v in rows)<1e-11
Iamp=s.symbols('delta_I',real=True)
low=s.simplify(Pformula.subs(rhot,-k*k*Iamp/6).subs(kap,k))
checks['low_frequency_power']=s.simplify(low-K*K*w*k**3*Iamp**2/(576*s.pi*gamma))==0
result={'checks':checks,'all_pass':all(checks.values()),'power_formula':str(Pformula),'low_k_power':str(low),'gaussian_transform_rows':rows,'mass_residual':mass,'second_moment':I,'scope':'homogeneous unpolarized reduced model; prescribed weak source; no galaxy matching or self-consistent cooling'}
p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n')
for name,ok in checks.items():print(name,'PASS' if ok else 'FAIL')
print('COMPLETE',sum(checks.values()),'/',len(checks))
sys.exit(0 if all(checks.values()) else 1)
