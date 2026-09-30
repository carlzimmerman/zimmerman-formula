"""Exploratory stable exact vacuum-annulus integration; not a source BVP."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
H=1.;beta=10.;lam=2.;Bl=lam-1.;S=3*lam-1.;u=1.5*S*H**2
r0=1e-6;r1=1e-5;GM=1e-16;a0=2*H/beta

def parts(r,y):
 lnN,sig,dW,dth,p=y;W=-H+dW;th=3*H+dth;E=np.exp(sig);t=1/E
 a=p+1.5*beta*p*p/th;n=E*a;ct=Bl+2*beta*p**3/th**3
 rest=H*S*dth+.5*Bl*dth*dth-2*dth*dW-3*dW*dW-p*p-2*beta*p**3/th
 C=rest-np.expm1(-2*sig)/r**2-2*t*a/r
 Cw=-2*dth-6*dW
 Cth=H*S+Bl*dth-2*dW+3*beta*t*p*p/(th*th*r)+2*beta*p**3/th**2
 tk=(3*beta*p*p/th**2-2*r*W*E)/ct;t0=-4*W*E*p/ct
 W0=-(dth+3*dW)/r-2*E*W*p
 denom=-6*beta*t*p/(th*r)-3*beta*p*p/th+2*r*E*W*(dth+3*dW)+Cth*tk
 constant=-6*beta*t*p*p/(th*r*r)+2*a*(p-1.5*beta*p*p/th)/r+2*rest/r+Cw*W0+Cth*t0
 pp=-constant/denom
 dy=np.array([n,r*E*pp+2*E*p-n,W0-r*E*W*pp,tk*pp+t0,pp])
 return dy,C,denom

def rhs_r(r,y):return parts(r,y)[0]

def initial_state(factor):
 p=np.sqrt(a0*GM)/r0;dt=factor*beta*p**3/(9*Bl);th=3*H+dt
 rest=H*S*dt+.5*Bl*dt*dt-p*p-2*beta*p**3/th
 aa=p+1.5*beta*p*p/th;dd=r0*r0*(aa*aa+rest)
 sig=-np.log1p(-r0*aa+dd/(np.sqrt(1+dd)+1))
 return np.array([0,sig,0,dt,p])

def integrate(endpoint,factor=0,cutoff=None,tight=False):
 events=None
 if cutoff is not None:
  def stop(z,y):return parts(np.exp(z),y)[2]+cutoff
  stop.terminal=True;stop.direction=1;events=stop
 sol=solve_ivp(lambda z,y:np.exp(z)*rhs_r(np.exp(z),y),(np.log(r0),np.log(endpoint)),initial_state(factor),
  method='DOP853',rtol=1e-10 if tight else 1e-9,
  atol=[1e-17,1e-17,1e-14,1e-14,1e-13] if tight else [1e-16,1e-16,1e-13,1e-13,1e-12],
  max_step=.015 if tight else .03,events=events,dense_output=True)
 assert sol.success,sol.message
 return sol

def diagnostics(rr,states):
 rows=[]
 for r,y in zip(rr,states.T):
  dy,C,D=parts(r,y);lnN,sig,dW,dt,p=y;W=-H+dW;th=3*H+dt;E=np.exp(sig);t=1/E
  w=r*W;wp=W+r*dy[2];a=p+1.5*beta*p*p/th
  orbit=dy[0]-E*E*w*(dy[1]*w+wp)/(1-E*E*w*w)
  pred=GM/r**2+np.sqrt(a0*GM)/r
  kin=H*S*dt+.5*Bl*dt*dt-2*dt*dW-3*dW*dW
  curv=-np.expm1(-2*sig)/r**2
  lapse=kin+curv+2*t*t*dy[1]/r-2*t*(dy[4]+2*p/r)-p*p-2*beta*p**3/th
  scale=1+abs(kin)+abs(curv)+abs(2*t*t*dy[1]/r)+abs(2*t*(dy[4]+2*p/r))+p*p+2*beta*p**3/th
  ct=Bl+2*beta*p**3/th**3
  momentum=ct*dy[3]-2*dy[2]-3*beta*p*p*dy[4]/th**2-2*(dt+3*dW)/r
  mscale=1+abs(ct*dy[3])+abs(2*dy[2])+abs(3*beta*p*p*dy[4]/th**2)
  rows.append({'r':float(r),'P':float(p),'Theta':float(th),'sigma':float(sig),'dW':float(dW),
   'constraint':float(C),'lapse_normalized_residual':float(lapse/scale),'shift_normalized_residual':float(momentum/mscale),
   'flux_ratio':float(r*r*1.5*beta*p*p/th/GM),'orbit':float(orbit),'predicted_reduced':float(pred),
   'background_subtracted_force_relative_error':float((orbit+H*H*r)/pred-1),
   'D':float(D),'compatibility_numerator':float(-D*dy[4]),'Pprime':float(dy[4]),
   'static_F_over_N_squared':float(1-E*E*w*w)})
 return rows

parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
rr=np.geomspace(r0,r1,64)
local=integrate(r1);tight=integrate(r1,tight=True)
rows=diagnostics(rr,local.sol(np.log(rr)))
ref=diagnostics(rr,tight.sol(np.log(rr)))
summary={
 'max_abs_lapse_normalized_residual':max(abs(v['lapse_normalized_residual']) for v in rows),
 'max_abs_shift_normalized_residual':max(abs(v['shift_normalized_residual']) for v in rows),
 'max_flux_fractional_drift':max(abs(v['flux_ratio']-1) for v in rows),
 'max_background_subtracted_force_relative_error':max(abs(v['background_subtracted_force_relative_error']) for v in rows),
 'max_relative_P_tolerance_difference':max(abs(v['P']/w['P']-1) for v,w in zip(rows,ref))}
assert summary['max_abs_lapse_normalized_residual']<1e-10
assert summary['max_abs_shift_normalized_residual']<1e-10
assert summary['max_flux_fractional_drift']<2e-6
assert summary['max_background_subtracted_force_relative_error']<2e-6
assert summary['max_relative_P_tolerance_difference']<1e-7
outer=[]
for cutoff in [1e-4,1e-5,1e-6]:
 sol=integrate(.01,cutoff=cutoff,tight=True)
 row=diagnostics([np.exp(sol.t[-1])],sol.y[:,-1:])[0]
 row.update({'cutoff':cutoff,'initial_trace_factor':0,'event_reached':sol.status==1})
 assert row['event_reached'] and abs(row['compatibility_numerator'])>1e-4
 outer.append(row)
shoot=[]
for factor in [.5,1,2]:
 sol=integrate(.01,factor=factor,cutoff=1e-5)
 row=diagnostics([np.exp(sol.t[-1])],sol.y[:,-1:])[0]
 row.update({'initial_trace_factor':factor,'event_reached':sol.status==1})
 assert not row['event_reached'] and row['P']>0 and row['Theta']>0
 shoot.append(row)
out={'parameters':{'H':H,'beta':beta,'lambda':lam,'U_over_M2':u,'GM_initial_flux':GM,'r0':r0,'r1':r1},
 'local_checks':summary,'local_rows':rows,'outer_cutoff_checks':outer,'trace_sweep':shoot,
 'scope':'Finite exact necessary radial vacuum IVPs; no source interior, matter mass calibration, global de Sitter match, full angular/foliation check, perturbation health or 32pi selection.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'local_checks':summary,'outer':[{k:v[k] for k in ['r','D','compatibility_numerator','Pprime']} for v in outer],
 'trace_sweep':[{k:v[k] for k in ['r','initial_trace_factor','P','Theta','event_reached']} for v in shoot]},indent=2))
