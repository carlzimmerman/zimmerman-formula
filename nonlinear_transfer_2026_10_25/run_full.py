import argparse,json,time
from pathlib import Path
import numpy as np
from full import Full
from initial import initial

def run(config,output):
 m=Full(wave_h_kpc=config.get('wave_h_kpc',2.),coupling=config.get('coupling',True));dt=config['dt_Myr']/m.tdyn;case=config['case'];dest=Path(output)
 if config.get('equilibrium'):
  old=np.load(config['equilibrium']);a=old['a'].copy();x=old['alpha'].copy();chi=np.zeros(len(m.wr));pi=chi.copy();meta={'equilibrium':config['equilibrium']}
  if case=='dilated':
   rr=m.edges*m.rm;shift=m.edges*(1+.2*np.exp(-(rr/200)**4));a=np.sqrt(np.maximum([np.diff(np.interp(m.edges,shift,np.r_[0,np.cumsum(abs(v)**2)])) for v in a],0)).astype(complex);x,_,_=m.minimize_alpha(a,chi,np.arctan2(abs(a[0]),abs(a[1])),maxit=300)
  if case.startswith('boundary_'):
   delta=(1 if case.endswith('plus') else -1)*.5/m.rm;th=np.arctan2(abs(a[0]),abs(a[1]));tn=np.interp(m.r-delta,m.r,th,left=th[0],right=th[-1]);mass=np.sum(abs(a)**2,axis=0);a=np.array([np.sqrt(mass)*np.sin(tn),np.sqrt(mass)*np.cos(tn)],complex);x,_,_=m.minimize_alpha(a,chi,np.interp(m.r-delta,m.r,x,left=x[0],right=x[-1]),maxit=300)
 else:a,x,chi,pi,meta=initial(m,case)
 p=np.zeros(m.n);E0=m.full_energy(a,x,p,chi,pi);C0=float(m.wvol@pi+m.g*sum(abs(a[0])**2));M0=float(np.sum(abs(a)**2));sink=0.;qs=0.;maxE=0.;maxQ=0.;maxM=0.;trace=[];initial_diag=m.diagnostics(a,x,chi,pi);start=time.monotonic();status='completed';maxit=0;maxroot=0.;maxfp=0.;steps=int(round(config['duration_Myr']/config['dt_Myr']));every=max(1,int(round(.1/config['dt_Myr'])))
 for j in range(steps):
  a,x,p,chi,pi,ds,dq,info=m.full_step(a,x,p,chi,pi,dt);sink+=ds;qs+=dq;maxit=max(maxit,info['iterations']);maxroot=max(maxroot,info['carrier_root_residual']);maxfp=max(maxfp,info['fixed_point_error'])
  if j%every==0 or j==steps-1 or info['fixed_point_error']>1e-8 or info['carrier_root_residual']>1e-7:
   d=m.diagnostics(a,x,chi,pi);E=m.full_energy(a,x,p,chi,pi);ck=float(.5*sum(p*p/m.Z(a)));maxE=max(maxE,abs(E+sink-E0));maxQ=max(maxQ,abs(m.wvol@pi+m.g*sum(abs(a[0])**2)+qs-C0));maxM=max(maxM,abs(d['mass']-M0));trace.append({'time_Myr':(j+1)*config['dt_Myr'],'total_energy':E,'escaped_energy':sink,'carrier_kinetic':ck,**d})
   if d['cap_slack']<=0 or not np.isfinite(E):status='physical_cap_or_nonfinite_failure';break
   if info['fixed_point_error']>1e-8 or info['carrier_root_residual']>1e-7:status='nonlinear_solve_failure';break
   if time.monotonic()-start>config.get('wall_seconds',240):status='wall_limit_partial';break
 out={'config':config,'status':status,'completed_time_Myr':(j+1)*config['dt_Myr'],'runtime_seconds':time.monotonic()-start,'initial_meta':meta,'initial':initial_diag,'initial_energy':E0,'final':m.diagnostics(a,x,chi,pi),'escaped_energy':sink,'max_absolute_energy_ledger_error':maxE,'max_shift_charge_ledger_error':maxQ,'max_mass_error':maxM,'max_carrier_root_residual':maxroot,'max_fixed_point_residual':maxfp,'maximum_midpoint_iterations':maxit,'trace':trace,'non_claims':['Finite-carrier implicit midpoint; stiff carrier oscillations require accuracy checks','No numerical drift is counted as radiation','Inherited material grid and chosen canonical completion require spatial checks','Normal-F EOS remains prior K30; no universal population result','Sponge escape requires domain and resolution checks']};np.savez_compressed(dest.with_name('state.npz'),a=a,alpha=x,carrier_p=p,chi=chi,pi=pi);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='trace'},flush=True)

def main(config):
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();run(config,arg.output)
