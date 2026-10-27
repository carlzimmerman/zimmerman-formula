"""Linear front forcing and a passive-outlet energy bound.

Uses only the actual FD-02 branch forces and metric. No release is assigned to
the front. This tests the tangent linear mode under prescribed slow infall,
not the nonlinear two-port radiation field.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline,PchipInterpolator

def calculate(run,dt_Myr):
 a=np.array(run['rows']);L=a[:,0];time=np.array(run['time_grid_Myr'])/run['tdyn_Myr'];td=run['tdyn_Myr'];logG=PchipInterpolator(L,np.log(a[:,7]));G=np.exp(logG(L));speed=np.sqrt(np.maximum(2*(a[0,2]-a[:,2])/G,0));acc=(-a[:,3]-.5*G*logG(L,1)*speed**2)/G;PR=CubicSpline(L,a[:,13]);force=-(a[:,13]*acc+(PR(L,1)-.5*a[:,14])*speed**2)
 # Continuous interpolant explicitly defines the finite linear model tested.
 Kf=PchipInterpolator(time,a[:,5]);Cf=PchipInterpolator(time,a[:,12]);Ff=PchipInterpolator(time,force)
 steps=int(np.ceil(time[-1]*td/dt_Myr));tt=np.linspace(0,time[-1],steps+1);dt=tt[1]-tt[0];mid=(tt[1:]+tt[:-1])/2;K=Kf(mid);C=Cf(mid);F=Ff(mid);Ke=Kf(tt);Ce=Cf(tt);Fe=Ff(tt)
 z=0.;p=0.;work=0.;paramwork=0.;maxE=0.;maxz=0.;E0=0.
 # A backward-error-friendly ledger: parameter half-steps plus exact affine
 # midpoint work. It verifies both the force and variable inertia terms.
 for i in range(steps):
  paramwork+=.5*p*p*(1/C[i]-1/Ce[i])+.5*(K[i]-Ke[i])*z*z
  v=dt*dt*K[i]/(4*C[i]);zn=((1-v)*z+dt*p/C[i]+dt*dt*F[i]/(2*C[i]))/(1+v);pn=p+dt*(F[i]-K[i]*(z+zn)/2)
  work+=F[i]*(zn-z);z,p=zn,pn
  paramwork+=.5*p*p*(1/Ce[i+1]-1/C[i])+.5*(Ke[i+1]-K[i])*z*z
  E=.5*p*p/Ce[i+1]+.5*Ke[i+1]*z*z;maxE=max(maxE,E);maxz=max(maxz,abs(z))
 finalE=.5*p*p/Ce[-1]+.5*Ke[-1]*z*z
 # Rigorous bound for the sampled piecewise-constant parameter model:
 # B_new = a B_old + b, a=max(1,sqrt(C_old/C_new),sqrt(K_new/K_old)),
 # b=sqrt(K_new/2)*abs((F/K)_new-(F/K)_old).
 # Then D+E_relative <= B² for ANY passive outlet at this single port.
 origin=Fe/Ke;B=np.sqrt(Ke[0]/2)*abs(origin[0])
 for i in range(1,len(tt)):
  mult=max(1.,np.sqrt(Ce[i-1]/Ce[i]),np.sqrt(Ke[i]/Ke[i-1]));B=mult*B+np.sqrt(Ke[i]/2)*abs(origin[i]-origin[i-1])
 return {'source_branch_grid':run['grid_size'],'time_step_Myr':float(dt*td),'steps':steps,'maximum_linear_front_energy_Eunit':float(maxE),'final_linear_front_energy_Eunit':float(finalE),'maximum_front_departure_kpc':float(maxz*9.452259710729319),'force_work_Eunit':float(work),'parameter_work_Eunit':float(paramwork),'absolute_energy_ledger_error':float(abs(finalE-E0-work-paramwork)),'passive_outlet_bound_Eunit':float(B*B),'passive_bound_over_branch_release':float(B*B/run['release_after_start']),'note':'Bound applies to this linear mode and a passive outlet connected only to it. Baseline slow scalar source, changing source shape and nonlinear infall-front feedback are not represented as independent active pumps.'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();source=json.loads(Path('front_dynamics_2026_10_25/run_branch_checked/results.json').read_text());out={'runs':[],'non_claims':['No universal bound on the full nonlinear two-port scalar/material system','Prescribed infall with the computed mechanical metric, not integrated material feedback','Positive boundary curvature is conditional on this restricted branch','Passive bound is exact for the piecewise-constant coefficient sequence; convergence to the chosen interpolant is checked numerically']}
 for r in source['runs']:
  for dt in [.2,.1,.05]:
   ans=calculate(r,dt);assert ans['absolute_energy_ledger_error']<1e-14;out['runs'].append(ans);Path(arg.output).write_text(json.dumps(out,indent=2)+'\n');print(ans,flush=True)
