"""Bounded final sprint: neutral finite-temperature surface response."""
import argparse
import json
from pathlib import Path
import sympy as s
parser=s.ArgumentParser() if False else argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
m,T,d,v,P,y,H,beta,M2,nu,t=s.symbols('m T d v P y H beta M2 nu t',positive=True)
checks={}
def check(name,expr):
    checks[name]=s.simplify(expr)==0
    assert checks[name],name
check('thermal_log_identity',(1+s.exp(-m/T))*s.exp(m/(2*T))-(2*s.cosh(m/(2*T))).rewrite(s.exp))
slope=d*T*m*s.log(2*s.cosh(m/(2*T)))/(s.pi*v**2)
series=s.series(slope,m,0,6).removeO()
expected=d*T*s.log(2)*m/(s.pi*v**2)+d*m**3/(8*s.pi*v**2*T)-d*m**5/(192*s.pi*v**2*T**3)
check('infrared_slope_series',series-expected)
potential_series=s.integrate(series,(m,0,m))
check('no_cubic_at_positive_temperature',potential_series.coeff(m,3))
check('zero_temperature_slope',s.limit(slope,T,0,dir='+')-d*m**2/(2*s.pi*v**2))
a0=2*H/beta
flux=2*T*P*s.log(2*s.cosh(y*P/(2*T)))/(y*a0)
check('infrared_stiffness',s.limit(flux/P,P,0)-2*T*s.log(2)/(y*a0))
check('large_mass_cubic_flux',s.limit(flux/(P**2/a0),P,s.oo)-1)
delta_GH=beta*s.log(2)/(2*s.pi*y)
check('conditional_horizon_temperature', (2*T*s.log(2)/(y*a0)).subs(T,H/(2*s.pi))-delta_GH)
C0=nu*d*y**3/(6*s.pi*v**2)
a0_micro=2*M2/(3*C0)
check('fixed_mode_count_continuous_ratio', (3*H**2/a0_micro**2).subs(y,t*y)-t**6*(3*H**2/a0_micro**2))
result={'passed':len(checks),'checks':checks,
        'conditional_GH_target_stiffness_for_y_1':float((s.sqrt(128*s.pi/3)*s.log(2)/(2*s.pi))),
        'scope':'Free neutral planar bands at actual T>0; horizon temperature substitution conditional; no interacting or covariant vacuum completion'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':len(checks)}))
