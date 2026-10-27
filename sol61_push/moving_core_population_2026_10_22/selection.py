import json,argparse
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
def solve(tol):
 eps=1e-7
 def f(x,Y):
  t,m=Y;return [-m/x**2,x*x*max(t,0)**3]
 def end(x,Y):return Y[0]
 end.terminal=True;end.direction=-1
 sol=solve_ivp(f,(eps,10),[1-eps**2/6,eps**3/3],rtol=tol,atol=tol*1e-3,events=end,dense_output=True,method='DOP853',max_step=.03)
 assert sol.success and len(sol.t_events[0])==1
 edge=sol.t_events[0][0];m=sol.sol(edge)[1]
 ii=quad(lambda x:sol.sol(x)[1]*x*max(sol.sol(x)[0],0)**3,eps,edge,epsabs=1e-10)[0]
 ufac=edge*ii/m**2;E=-3*np.pi/64;radius=ufac/(-2*E)
 return dict(edge_dimensionless=float(edge),mass_dimensionless=float(m),U_coefficient=float(ufac),radius_at_M1_Plummer_energy=float(radius),energy=E)
r=solve(1e-10);s=solve(1e-8);checks=[dict(name='repeat',passed=max(abs(r[k]-s[k]) for k in r)<1e-7),dict(name='virial_coefficient_independent_integral',passed=abs(r['U_coefficient']-1.5)<1e-8),dict(name='different_support_same_M_E',passed=abs(r['radius_at_M1_Plummer_energy']-16/np.pi)<1e-7)]
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(dict(checks=checks,witness=r,Plummer=dict(M=1,b=1,E=-3*np.pi/64,support='infinite finite-mass tail'),polytrope=dict(M=1,E=r['energy'],support_radius=r['radius_at_M1_Plummer_energy'])),indent=2)+'\n');print(r,checks);raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
