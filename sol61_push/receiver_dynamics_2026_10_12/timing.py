from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import solve_ivp

H0=4.
q90=.9
s90=(q90+(1-H0)*math.log(H0/(H0-q90)))/(4*H0)
rows=[]
for eps in [.03,.01,.003]:
    def f(t,z):
        q,x,p=z; y=1-q
        return [p*p*y,eps*p,-eps*x-p*y/(2*H0)]
    def event(t,z): return z[0]-q90
    event.terminal=True; event.direction=1
    sol=solve_ivp(f,(0,.1/eps**2),[0,1,0],method='Radau',rtol=1e-9,atol=1e-11,events=event,dense_output=True)
    assert sol.success and len(sol.t_events[0])==1
    t90=float(sol.t_events[0][0]); q,x,p=sol.sol(np.linspace(0,t90,501))
    err=float(np.max(np.abs(q/H0+x*x+p*p-1)))
    assert err<=1e-7 and q.min()>=-1e-9 and q.max()<=q90+1e-8
    approx=s90/eps**2
    rows.append({'epsilon':eps,'t90_over_tau':t90,'leading':approx,
                 'relative_difference':t90/approx-1,'energy_error':err})
assert abs(rows[-1]['relative_difference'])<=.02

sec_year=365.25*86400
tau=1e8*sec_year
a0=9.36e-11
c=299792458.
physical=[]
for factor in [1.,5.78881]:
    omega=factor*a0/c
    eps=omega*tau
    leading_gyr=s90/eps**2*tau/sec_year/1e9
    # Rigorous onset lower bound from |pi(t)| <= omega sqrt(2H0) t.
    lower=((3*math.log(10)*tau)/(omega*omega))**(1/3)/sec_year/1e9
    physical.append({'frequency_factor_a0_over_c':factor,'epsilon':eps,
                     'leading_t90_Gyr':leading_gyr,'onset_lower_bound_Gyr':lower})
result={'capacity_ratio_H0_over_DA':H0,'slow_time_s90':s90,'runs':rows,
        'conditional_physical_illustrations':physical,
        'scope':'Normalized reduced receiver; neither Gamma nor omega is derived. Slow-manifold physical numbers are leading approximations.'}
Path(__file__).with_name('timing_run').joinpath('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
