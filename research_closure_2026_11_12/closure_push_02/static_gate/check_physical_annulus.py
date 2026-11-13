#!/usr/bin/env python3
"""Physical-parameter finite annulus, never a global matching or halo fit."""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,simpson

def gate(u):
 with np.errstate(all='ignore'):
  s=np.exp(-u**3);return s,-3*u*u*s,(9*u**4-6*u)*s

def ref(x):
 s=np.sqrt(1+4*x*x)
 return np.arcsinh(2*x)-(1+s)/(2*x)-np.arcsinh(120.),(1+s)/(2*x*x),2/(1+s),2/(x*s)

def run(mu,uR,tol=2e-6,previous=None):
 G=6.674e-11;MSUN=1.989e30;MPC=3.0857e22;a0=9.3603e-11
 rM=math.sqrt(G*MSUN*1e11/a0)/MPC;ell=22e-6/rM;m=mu*rM
 d=ref(np.array([60.]))[3][0]/uR
 r=np.geomspace(1.,60.,300);initial=np.vstack(ref(r)) if previous is None else previous.sol(r)
 targetF,targetP,targetZ=ref(r)[0][-1],ref(r)[2][-1],ref(r)[3][0]
 def fun(x,q):
  f,y,p,Z=q;S,Sp,Spp=gate(np.clip(Z/d,-2,15))
  DD=ell*ell/2-m*m*f*f*Spp/(2*d*d)
  return np.vstack((y,Z-m*m*f*S-2*y/x,Z-2*p/x,(p/(1-p)-y+m*m*f*y*Sp/d)/DD))
 def bc(qa,qb):return np.array([qa[1]-qa[2]-1.,qa[3]-targetZ,qb[0]-targetF,qb[2]-targetP])
 with np.errstate(all='ignore'):
  sol=solve_bvp(fun,bc,r,initial,tol=tol,max_nodes=15000)
 x=np.geomspace(1,60,10001);q=sol.sol(x);qprime=sol.sol(x,1);f,y,p,Z=q
 S,Sp,Spp=gate(Z/d);DD=ell*ell/2-m*m*f*f*Spp/(2*d*d)
 with np.errstate(all='ignore'):
  constit=y+ell*ell*qprime[3]/2-m*m*f*y*Sp/d-m*m*f*f*Spp*qprime[3]/(2*d*d)-p/(1-p)
  pois=qprime[1]+2*y/x-Z+m*m*f*S
  gauss=x*x*(y-p);dust=simpson(-m*m*x*x*f*S,x=x)
 original=np.vstack(ref(x));force_diff=float(np.max(np.abs(y/original[1]-1)))
 accepted=bool(sol.status==0 and np.all(np.isfinite(q)) and np.min(Z)>0 and np.min(p)>0 and np.max(p)<1 and np.min(DD)>0 and np.max(np.abs(constit))<1e-4 and np.max(np.abs(pois))<1e-4)
 row={'mu_Mpc_inverse':mu,'rM_Mpc':rM,'m':m,'ell':ell,'uR_reference':uR,'d':d,'tol':tol,'status':int(sol.status),'message':sol.message,'nodes':len(sol.x),'solver_max_rms':float(np.max(sol.rms_residuals)),'accepted_finite_annulus':accepted,'u_actual_min':float(np.min(Z/d)),'pmin':float(np.min(p)),'pmax':float(np.max(p)),'Dmin':float(np.min(DD)),'max_constitutive_residual_original':float(np.max(np.abs(constit))),'max_Poisson_residual_original':float(np.max(np.abs(pois))),'boundary_residual':float(np.max(np.abs(bc(sol.y[:,0],sol.y[:,-1])))),'force_max_fractional_departure_from_reference':force_diff,'annular_dust_mass_in_baryon_units':float(dust),'Gauss_flux_change':float(gauss[-1]-gauss[0]),'Gauss_flux_integral_absolute_error':float(abs(gauss[-1]-gauss[0]-dust))}
 return sol,row

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();rows=[]
 last=None
 for mu in [198.25,25120.]:
  sol,row=run(mu,4.);rows.append(row)
  if row['accepted_finite_annulus']:last=sol
 # Independent mesh/tolerance refinement of high-mu solve if accepted.
 if rows[-1]['accepted_finite_annulus']:
  sol,row=run(25120.,4.,tol=5e-7,previous=last);rows.append(row)
  xx=np.geomspace(1,60,10001);refine=float(np.max(np.abs(sol.sol(xx)-last.sol(xx))))
 else:refine=None
 result={'assertion':'Finite annular BVP with physical mu,Lstar,Mb; artificial boundary matching; positive Pi; not a global cosmological state','Mb_Msun':1e11,'domain_x':[1,60],'rows':rows,'high_mu_refinement_max_abs_state_difference':refine}
 nonfinite=[]
 def clean(v,path='root'):
  if isinstance(v,dict):return {k:clean(z,path+'.'+k) for k,z in v.items()}
  if isinstance(v,list):return [clean(z,path+'['+str(k)+']') for k,z in enumerate(v)]
  if isinstance(v,float) and not math.isfinite(v):nonfinite.append({'path':path,'value':str(v)});return None
  return v
 result=clean(result);result['nonfinite_values_in_rejected_attempts']=nonfinite
 Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 print(json.dumps(result,indent=2,allow_nan=False))
