"""Guarded implicit representative continuation and radial stiffness screen.
Radial IVP eigenvalues are not temporal stability/health eigenvalues.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from ode import equations
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True,type=Path);aa=ap.parse_args();base=Path(__file__).resolve().parent;out=aa.output_dir.resolve();out.relative_to(base);out.mkdir(parents=True,exist_ok=True)
eta=.5;A=1.;m=1e-12;L=math.sqrt(m*A);r0=10*L/A;xf=math.log(.03);y0=np.array([0.,math.log1p(L),eta,L]);x0=math.log(r0)
def raw(x,y):return np.array(equations(math.exp(x),y,eta,A)[0])
jacs=[]
for multiplier in [1.,.1]:
 J=np.zeros((4,4));steps=multiplier*np.array([1e-8,1e-8,1e-6,1e-9])
 for j in range(4):
  delta=np.zeros(4);delta[j]=steps[j];J[:,j]=(raw(x0,y0+delta)-raw(x0,y0-delta))/(2*steps[j])
 ev=np.linalg.eigvals(J);jacs.append({'steps':steps.tolist(),'matrix':J.tolist(),'eigenvalues':[[float(x.real),float(x.imag)] for x in ev]})
count=[0];last=[x0,y0.copy()]
class Guard(Exception):pass
def rhs(x,y):
 count[0]+=1;last[:]=[x,y.copy()]
 if count[0]>12000:raise Guard('12000RHS evaluation cap')
 return raw(x,y)
def horizon(x,y):return equations(math.exp(x),y,eta,A)[1]['F']/math.exp(2*y[0])-.01
horizon.terminal=True;horizon.direction=-1
def wzero(x,y):return y[2]-.001
wzero.terminal=True;wzero.direction=-1
res={'jacobian_controls':jacs,'initial':{'eta':eta,'A_over_H':A,'m':m,'r0':r0,'y':y0.tolist()},'non_claims':['No matchedsource or outerboundary','Radial Jacobian not temporalhealth','No coefficientselector']}
try:
 sol=solve_ivp(rhs,(x0,xf),y0,method='Radau',rtol=1e-9,atol=1e-12,max_step=.1,events=[horizon,wzero],dense_output=True)
 pts=[]
 for x in np.linspace(sol.t[0],sol.t[-1],65):
  rr=math.exp(float(x));dy,z=equations(rr,sol.sol(x),eta,A);pts.append({'r':rr,**z})
 res.update(success=bool(sol.success),message=sol.message,nfev=count[0],steps=len(sol.t),events=[x.tolist() for x in sol.t_events],samples=pts,end=pts[-1],target_reached=bool(abs(sol.t[-1]-xf)<1e-10))
except (Guard,OverflowError,ValueError,ZeroDivisionError) as e:
 rr=math.exp(last[0]);dy,z=equations(rr,last[1],eta,A);res.update(success=False,message=str(e),nfev=count[0],last_trial_radius=rr,last_trial=z)
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k not in ['jacobian_controls','samples','non_claims']}));raise SystemExit(0 if res['success'] else 1)
