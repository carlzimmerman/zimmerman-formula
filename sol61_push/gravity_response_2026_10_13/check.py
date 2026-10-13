#!/usr/bin/env python3
"""Forced linear Jeans mode: exact response versus independent ODE integration."""
import math,json,sys
from pathlib import Path
from scipy.integrate import solve_ivp
checks=[];rows=[]
def check(name,a,b,atol=1e-9,rtol=2e-9):
 checks.append(dict(name=name,actual=float(a),expected=float(b),passed=bool(abs(a-b)<=atol+rtol*abs(b))))
# Dimensionless time s=sqrt(J)*t; R=delta_rho_c/delta_rho_b.
# R''+epsilon R=1 with initially zero contrast and velocity.
for eps in [0.,1e-8,1e-4,.01,1.,100.,-.01,-1.]:
 for s in [.01,.1,1.,3.]:
  if eps>0:exact=2*math.sin(math.sqrt(eps)*s/2)**2/eps
  elif eps==0:exact=s*s/2
  else:exact=2*math.sinh(math.sqrt(-eps)*s/2)**2/(-eps)
  sol=solve_ivp(lambda t,y:[y[1],1-eps*y[0]],[0,s],[0.,0.],rtol=1e-11,atol=1e-13,method='DOP853')
  assert sol.success
  check(f'forced mode eps={eps} s={s}',sol.y[0,-1],exact)
  if eps>=0:assert exact<=s*s/2+1e-12
  # K/J=1+eps>=0 includes stable and Jeans-unstable regimes tested.
  assert exact<=2*math.sinh(s/2)**2+1e-12
  rows.append(dict(epsilon=eps,time_in_Jeans_units=s,response=exact,
                   stable_finite_time_bound=s*s/2,nonnegative_pressure_bound=2*math.sinh(s/2)**2))
G=6.67430e-11
physical=[]
for rho in [1.,1e3,1e9]:
 J=4*math.pi*G*rho
 physical.append(dict(density_kg_m3=rho,Jeans_time_s=1/math.sqrt(J),
                      max_stable_induced_gain_at_1s=J/2,
                      first_time_to_static_gain_100_s=math.pi*math.sqrt(99)/(2*math.sqrt(J))))
result=dict(all_passed=all(c['passed'] for c in checks),check_count=len(checks),checks=checks,
            mode_grid=rows,physical_scales=physical,
            density_needed_for_induced_gain_99_at_1s=99/(2*math.pi*G),
            density_needed_for_extra_a_point02_eta_point1_L1=.02/(2*G*.1*1),
            scope='Linear one-mode response in a conditional condensate/Newtonian periodic completion. No full carrier solution, nonlinear collapse, active pump, or modified metric.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','mode_grid']},indent=2))
sys.exit(0 if result['all_passed'] else 1)
