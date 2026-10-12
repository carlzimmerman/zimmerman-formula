"""Finite, externally controlled quadratic preparation; no vacuum creation claim."""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
p=Path(__file__).parent
checks=[]
def check(name,b): checks.append(dict(name=name,passed=bool(b)))
u=.001
mass_ratio=math.sqrt(1+u*u) # M/(2m)
def state(theta=math.pi/4, duration=math.pi/2, ratio=2.):
    x0=math.sqrt(2)*math.cos(theta); y0=math.sqrt(2)*math.sin(theta)
    x=x0*math.cos(duration); y=y0*math.cos(ratio*duration)
    vx=-x0*math.sin(duration); vy=-ratio*y0*math.sin(ratio*duration)
    energy=.5*(x*x+y*y+vx*vx+vy*vy)
    charge=2*(y*vx-x*vy)
    work= .5*(ratio*ratio-1)*(y0*y0-y*y)
    efficiency=charge/(2*energy)
    return dict(energy=energy,charge=charge,net_switch_work=work,
                efficiency=efficiency,eta=1-efficiency/mass_ratio)
rows=[]
for theta in [math.pi/4-.02,math.pi/4,math.pi/4+.02]:
    for duration in [math.pi/2-.01,math.pi/2,math.pi/2+.01]:
        for ratio in [1.99,2.,2.01]:
            s=state(theta,duration,ratio)
            check('switch energy identity',abs(s['energy']-1-s['net_switch_work'])<3e-15)
            def rhs(t,z):
                x,y,vx,vy,q=z
                return [vx,vy,-x,-ratio*ratio*y,2*(ratio*ratio-1)*x*y]
            z0=[math.sqrt(2)*math.cos(theta),math.sqrt(2)*math.sin(theta),0,0,0]
            sol=solve_ivp(rhs,[0,duration],z0,rtol=2e-12,atol=2e-13)
            z=sol.y[:,-1]
            check('charge torque integral',sol.success and abs(z[4]-s['charge'])<2e-11)
            check('charge efficiency bound',abs(s['efficiency'])<=1+1e-14)
            rows.append(dict(theta=theta,duration=duration,frequency_ratio=ratio,**s))
ideal=state()
check('ideal maximal charge',abs(ideal['efficiency']-1)<1e-14)
check('ideal zero net drive work',abs(ideal['net_switch_work'])<1e-14)
# At exact pulse duration/ratio, r=sin(2 theta), an analytic finite identity.
for theta in np.linspace(-math.pi,math.pi,41):
    check('phase efficiency identity',abs(state(float(theta))['efficiency']-math.sin(2*theta))<2e-14)
limits=[]
for eta_target in [1e-6,1e-5]:
    phase=.5*math.acos((1-eta_target)*mass_ratio)
    timing=brentq(lambda d: state(duration=math.pi/2+d)['eta']-eta_target,0,.05,xtol=1e-15)
    ratio=brentq(lambda d: state(ratio=2+d)['eta']-eta_target,0,.05,xtol=1e-15)
    limits.append(dict(eta_target=eta_target,phase_offset_radians=phase,
                      positive_duration_offset_Mt=timing,positive_frequency_ratio_offset=ratio))
out=dict(ideal=ideal,one_parameter_tolerances=limits,checks=checks,
         all_pass=all(c['passed'] for c in checks),sampled_rows=rows,
         non_claims=['Prescribed instantaneous switches, not autonomous cosmology',
                     'Initial displaced condensate and phase supplied',
                     'No quantum vacuum creation or daughter evolution during pulse',
                     'One-parameter tolerances are not simultaneous-error bounds'])
(p/'source_preparation_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['checks','sampled_rows']},indent=2))
print('Checks:',len(checks));assert out['all_pass']
