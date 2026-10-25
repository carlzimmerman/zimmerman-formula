import argparse,json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import logsumexp
CHI=11.220184543019636
F=CHI/(1+CHI)
G=6.67430e-11;HB=1.054571817e-34;KB=1.380649e-23;MS=1.98847e30;KP=3.085677581491367e19

def occupation(r,s,tau):
    if tau==0:return 1.
    return np.tanh(r/tau)/(1+2*np.exp(-(r+s)/tau)/(1+np.exp(-2*r/tau)))

def susceptibility(tau):
    if tau==0:return 1.
    return 1-2*tau/3*np.log(4/(1+3*np.exp(-2/tau)))

def integral(fun,E,tau):
    points=sorted(set([0.,1.]+[float(a) for a in [E,tau,10*tau] if 0<a<1]))
    return sum(quad(fun,a,b,epsabs=2e-14,epsrel=2e-11)[0] for a,b in zip(points[:-1],points[1:]))

def remainder(E,tau):
    if tau==0:return E*(1-E/(1+np.sqrt(1+E*E))) # 1-sqrt(1+E²)+E
    # chi_T minus P/E, scaled by chi. Avoid subtracting two entire integrals.
    return integral(lambda s:occupation(s,s,tau)-s/np.hypot(s,E)*occupation(np.hypot(s,E),s,tau),E,tau)

def source(x,tau):
    E=x/F
    return F*x*(1-susceptibility(tau)+remainder(E,tau))

def tests():
    errors=[]
    for s in [.001,.1,.8]:
        for E in [.01,.3]:
            for tau in [.01,.1,1.]:
                def free(e):
                    r=np.hypot(s,e);levels=np.array([s-r,s+r,2*s,2*s])
                    return -tau*logsumexp(-levels/tau)
                step=1e-6
                numerical=-(free(E+step)-free(E-step))/(2*step)
                exact=E/np.hypot(s,E)*occupation(np.hypot(s,E),s,tau)
                errors.append(abs(numerical-exact))
    chierror=max(abs(integral(lambda s:occupation(s,s,t),.01,t)-susceptibility(t)) for t in [.0001,.01,.1,1.])
    cold=max(abs(remainder(e,0)-(1-np.sqrt(1+e*e)+e)) for e in [1e-4,.01,1,10])
    assert max(errors)<1e-8 and chierror<1e-12 and cold<1e-13
    return dict(free_energy_derivative_max_absolute_error=max(errors),thermal_susceptibility_integral_error=chierror,cold_formula_error=cold)

def main(output):
    r=dict(checks=tests(),thermal_slopes=[],thermal_tolerances=[],mass_speed=[],profiles=[])
    for tau in [0,.001,.01,.1,1.]:
        vals=[]
        for E in [1e-4,2e-4,.001,.01,.1]:
            vals.append(dict(E=E,retuned_remainder=E*remainder(E,tau),fixed_source=source(E*F,tau)))
        r['thermal_slopes'].append(dict(tau=tau,chiT_over_chi=susceptibility(tau),values=vals,
            low_E_retuned_power=float(np.log(vals[1]['retuned_remainder']/vals[0]['retuned_remainder'])/np.log(2)),
            low_E_fixed_power=float(np.log(vals[1]['fixed_source']/vals[0]['fixed_source'])/np.log(2))))
    t=10**.05
    for x in [1e-4,.001,.01,.1,1.]:
        y=source(x,0)
        tau=brentq(lambda u:source(x/t,u)-y,0,100,xtol=1e-14)
        r['thermal_tolerances'].append(dict(x=x,max_tau_for_005dex_downward_shift=float(tau)))
        fm=(t*t*x*x/(1+t*x)-x*x/(1+x))/(t*x)
        for A in [1.,10.]:
            r['mass_speed'].append(dict(x=x,allowed_medium_fraction_total=float(fm),required_mode_to_dyn_ratio=A,
                epsilon_ceiling=float(18*x*x*fm/(A*A*F**3))))
    for M,b in [(3e5,.3),(1e8,1.),(6e10,3.),(1e14,300.)]:
        rho=3*5.364*M*MS/(4*np.pi*(b*KP)**3);sigma=np.sqrt(G*(1+5.364)*M*MS/(6*b*KP))
        omega=np.sqrt(12*np.pi*G*rho/(.1*F))
        r['profiles'].append(dict(Mb=M,b_kpc=b,rho=rho,sigma_kms=sigma/1000,degeneracy_proxy=rho/sigma**3,
            short_range_rate_proxy=rho*sigma,
            optimistic_T_kelvin=[dict(x=a['x'],T=a['max_tau_for_005dex_downward_shift']*HB*omega/(2*KB)) for a in r['thermal_tolerances']]))
    disk=r['profiles'][2]
    for p in r['profiles']:
        p['degeneracy_relative_to_disk']=p['degeneracy_proxy']/disk['degeneracy_proxy']
        p['short_range_rate_relative_to_disk']=p['short_range_rate_proxy']/disk['short_range_rate_proxy']
    r['screen_counts']=dict(common_degeneracy_threshold_can_select_disk_excluding_smallest_dwarf=False)
    assert r['profiles'][0]['degeneracy_relative_to_disk']>1
    with open(output,'w') as f:json.dump(r,f,indent=2,allow_nan=False)
    print(json.dumps(r))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
