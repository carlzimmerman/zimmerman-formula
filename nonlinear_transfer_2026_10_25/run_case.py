import argparse,json,time
from pathlib import Path
import numpy as np
from live import Live
from initial import initial

def run(config,output):
 m=Live(coupling=config.get('coupling',True));case=config['case'];dt=config['dt_Myr']/m.tdyn;duration=config['duration_Myr'];dest=Path(output)
 if config.get('equilibrium'):
  old=np.load(config['equilibrium']);a=old['a'].copy();x=old['alpha'].copy();chi=old['chi'].copy();pi=old['pi'].copy();meta={'source_equilibrium':config['equilibrium']}
  if case=='dilated':
   rr=m.edges*m.rm;shift=m.edges*(1+.2*np.exp(-(rr/200)**4));masses=[]
   for species in a:masses.append(np.diff(np.interp(m.edges,shift,np.r_[0,np.cumsum(abs(species)**2)])))
   a=np.sqrt(np.maximum(masses,0)).astype(complex);x=np.arctan2(abs(a[0]),abs(a[1]));x,_,_=m.minimize_alpha(a,chi,x,maxit=300)
  if case.startswith('boundary_'):
   delta=(1 if case.endswith('plus') else -1)*.5/m.rm;theta=np.arctan2(abs(a[0]),abs(a[1]));theta2=np.interp(m.r-delta,m.r,theta,left=theta[0],right=theta[-1]);mass=sum(abs(a)**2);a=np.array([np.sqrt(mass)*np.sin(theta2),np.sqrt(mass)*np.cos(theta2)],complex);x,_,_=m.minimize_alpha(a,chi,np.interp(m.r-delta,m.r,x,left=x[0],right=x[-1]),maxit=300)
 else:a,x,chi,pi,meta=initial(m,case)
 E0=m.energy(a,x,chi,pi);M0=sum(np.sum(abs(a)**2,axis=0));C0=float(m.wvol@pi+m.g*sum(abs(a[0])**2));sink=0.;qs=0.;trace=[];maxE=0.;maxC=0.;maxM=0.;maxres=0.;start=time.monotonic();status='completed';initial_diag=m.diagnostics(a,x,chi,pi);steps=int(round(duration/config['dt_Myr']));every=max(1,int(round(.1/config['dt_Myr'])))
 for j in range(steps):
  a,x,chi,pi,ds,dq,res=m.step(a,x,chi,pi,dt);sink+=ds;qs+=dq;maxres=max(maxres,res)
  if j%every==0 or j==steps-1:
   d=m.diagnostics(a,x,chi,pi);E=m.energy(a,x,chi,pi);maxE=max(maxE,abs(E+sink-E0));maxC=max(maxC,abs(m.wvol@pi+m.g*sum(abs(a[0])**2)+qs-C0));maxM=max(maxM,abs(d['mass']-M0));trace.append({'time_Myr':(j+1)*config['dt_Myr'],'total_energy':E,'escaped_energy':sink,**d})
   if d['cap_slack']<=0 or not np.isfinite(E):status='physical_cap_or_nonfinite_failure';break
   if maxres>1e-5:status='carrier_solve_failure';break
   if time.monotonic()-start>config.get('wall_seconds',240):status='wall_limit_partial';break
 elapsed=(j+1)*config['dt_Myr'];out={'config':config,'status':status,'completed_time_Myr':elapsed,'runtime_seconds':time.monotonic()-start,'initial_meta':meta,'initial':initial_diag,'initial_energy':E0,'final':m.diagnostics(a,x,chi,pi),'escaped_energy':sink,'max_absolute_energy_ledger_error':maxE,'max_shift_charge_ledger_error':maxC,'max_mass_error':maxM,'max_carrier_projected_residual':maxres,'trace':trace,'non_claims':['Carrier inertia omitted: zero-inertia freely minimized carrier limit','No energy drift assigned to radiation; compare drift with actual wave and escape','One radial initial condition is not a galaxy population','The exact complex gradient differs from inherited angle discretization','Sponge output is not certified far-field escape without domain/resolution check']};np.savez_compressed(dest.with_name('state.npz'),a=a,alpha=x,chi=chi,pi=pi);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='trace'},flush=True)

def main(config):
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();run(config,arg.output)
