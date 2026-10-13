"""Conditional ideal Bose chemical-equilibrium endpoint, not a dynamical simulation."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import zeta,gamma
p=Path(__file__).parent
old=json.loads((p/'nr_quantum_bound_run/results.json').read_text())
a=old['parameters'];coeff=old['NR_coefficients']
m=a['m_eV'];M=a['M_eV'];gap=M-2*m
nq=2*a['rho_source_eV4']/M;excess=gap*nq/2
checks=[]
def ck(n,b):checks.append(dict(name=n,passed=bool(b)))
def moment(power,alpha):
    def integrand(x):
        arg=x*x+alpha
        if arg>700:return 0.
        if arg==0:return 1. if power==2 else 0.
        return x**power/math.expm1(arg)
    return quad(integrand,0,30,epsabs=1e-11,epsrel=1e-11,limit=200)[0]
def gas(mass,T,alpha):
    pref=(2*mass*T)**1.5/(2*math.pi**2)
    return pref*moment(2,alpha),pref*T*moment(4,alpha)
def state(T):
    na,ka=gas(m,T,0);nb,kb=gas(M,T,gap/T)
    kinetic=ka+kb;D=kinetic+gap*nb;P=2*kinetic/3
    entropy=(D+P)/T
    return dict(T_eV=T,daughter_thermal_density=na,source_thermal_density=nb,thermal_charge_density=na+2*nb,excess_density=D,pressure=P,entropy_density=entropy)
T=brentq(lambda T:state(T)['excess_density']-excess,1e-8,10,xtol=1e-13)
initial=state(T);sinit=initial['entropy_density']
ck('initial energy conservation',abs(initial['excess_density']/excess-1)<1e-10)
for power in [2,4]:
    ref=.5*gamma((power+1)/2)*zeta((power+1)/2)
    ck('Bose integral zeta control '+str(power),abs(moment(power,0)/ref-1)<1e-10)
# Independent fugacity series check where alpha>0.
alpha=gap/T
j=np.arange(1,20001,dtype=float)
for power in [2,4]:
    order=(power+1)/2
    ref=.5*gamma(order)*np.sum(np.exp(-j*alpha)/j**order)
    ck('source fugacity series '+str(power),abs(moment(power,alpha)/ref-1)<1e-10)
rows=[]
for scale in [1,2,10,100,1e3,1e6]:
    targetS=sinit/scale**3
    t=brentq(lambda x:state(x)['entropy_density']/targetS-1,T/(scale*scale)*.05,T,xtol=1e-25,rtol=1e-12) if scale>1 else T
    r=state(t);charge=nq/scale**3
    frac=1-r['thermal_charge_density']/charge
    r.update(scale_factor_ratio=scale,charge_density=charge,daughter_condensate_charge_fraction=frac,source_charge_fraction=2*r['source_thermal_density']/charge,pressure_over_total_energy=r['pressure']/(m*charge+r['excess_density']))
    ck('positive condensate '+str(scale),0<frac<1)
    ck('adiabatic entropy '+str(scale),abs(r['entropy_density']/targetS-1)<1e-9)
    rows.append(r)
keff=coeff['positive_quartic_residual'];c=coeff['cubic'];k=coeff['quartic']
cond=rows[0]['daughter_condensate_charge_fraction']*nq
mu=2*keff*cond
# Static source slaved to condensate, only an interaction-size estimate.
induced_nb=(c*cond/gap)**2
est=dict(mean_field_mu_eV=mu,mu_over_temperature=mu/T,mu_over_gap=mu/gap,condensate_interaction_energy_over_initial_excess=keff*cond**2/excess,induced_coherent_source_charge_fraction=2*induced_nb/nq)
ck('perturbative mean field scale',mu/T<1e-5 and mu/gap<1e-4)
out=dict(parameters=a,initial_charge_density_eV3=nq,initial_excess_density_eV4=excess,rows=rows,interaction_size_estimates=est,checks=checks,all_pass=all(x['passed'] for x in checks),non_claims=['Chemical and kinetic equilibrium assumed, no thermalization time derived','Ideal continuum gas approximation to interacting regulated NR model','Adiabatic homogeneous expansion assumes continued equilibrium','No halo formation, abundance origin, transfer function or observational verdict'])
(p/'bose_endpoint_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
