"""Autonomous full density/carrier/field evolution, no supplied fast modes.

All accepted steps pass full root and physical cap tests. Numerical energy
error is reported and capped; never corrected or assigned to radiation.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from ledger_collocated import FourthOrder
from volume_initial import fine_initial

def run(config,output):
 dest=Path(output);m=FourthOrder(eta=config.get('eta',.01),material_h_kpc=config.get('material_h_kpc',.125),wave_R_kpc=10000.)
 if not config.get('transport',True):m.k=0.;m.kd=np.zeros_like(m.kd);m.ko=np.zeros_like(m.ko)
 a,x,c,v,meta=fine_initial(m,config['case'],'nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');p=np.zeros(m.n)
 E0=Eold=m.full_energy(a,x,p,c,v);Q0=m.charge(a,v);M0=float(np.sum(abs(a)**2));W0=m.diagnostics(a,x,c,v)['wave_energy']
 sink=qs=work=bwork=cwork=flux=fwork=0.;t=0.;h=config['dt_Myr'];start=time.monotonic();trace=[];rejections=[];accept=reject=0;maxE=maxQ=maxM=maxW=maxF=maxroot=0.;nextsample=0.;status='completed';history=[]
 components={key:{'chi':np.zeros_like(c),'pi':np.zeros_like(v),'flux':0.,'sink':0.} for key in ['bulk','conversion']};max_component_match=0.
 edge=int(np.argmin(abs((m.wr[:-1]+m.wr[1:])/2-500/m.rm)));sel=m.r*m.rm<80.;rsel=m.r[sel]*m.rm
 def far_energy(c,v):return float(.5*m.wvol[edge+1:]@(v[edge+1:]**2)+m.c**2*(.5*m.ww[edge+1:]@np.diff(c)[edge+1:]**2+.25*m.ww[edge]*np.diff(c)[edge]**2))
 def sample():
  nonlocal maxE,maxQ,maxM,maxW,maxF,nextsample,max_component_match
  E=m.full_energy(a,x,p,c,v);d=m.diagnostics(a,x,c,v);mass=abs(a)**2
  maxE=max(maxE,abs(E+sink-E0));maxQ=max(maxQ,abs(m.charge(a,v)+qs-Q0));maxM=max(maxM,abs(np.sum(mass)-M0));maxW=max(maxW,abs(d['wave_energy']+sink-W0-work));maxF=max(maxF,abs(far_energy(c,v)+sink-flux-fwork));outside=m.r*m.rm>70
  trace.append({'time_Myr':t,'total_energy':E,'escaped_energy':sink,'net_material_to_wave_work':work,'bulk_current_work':bwork,'conversion_work':cwork,'far_net_flux':flux,'far_source_work':fwork,'energy_ledger_error':E+sink-E0,'wave_work_error':d['wave_energy']+sink-W0-work,'far_ledger_error':far_energy(c,v)+sink-flux-fwork,'fixed_outer_T_fraction':float(np.sum(mass[0,outside])/np.sum(mass[:,outside])),**d})
  rho=mass[0]/m.vol;_,source,bulk,conv,U,rate=m.transfer(a,x,c);psi=a/np.sqrt(m.vol);jt=m.k/m.sigma*m.w*np.imag(np.conj(psi[0,:-1])*U*psi[0,1:]);history.append(np.r_[t,rho[sel],x[sel],source[sel],np.interp(rsel,((m.r[1:]+m.r[:-1])/2*m.rm),jt)])
  energies={}
  for key,z in components.items():energies[key]=float(.5*m.wvol@(z['pi']**2)+.5*m.c**2*m.ww@np.diff(z['chi'])**2)
  match=max(float(np.max(abs(sum(z['chi'] for z in components.values())-c))),float(np.max(abs(sum(z['pi'] for z in components.values())-v))));max_component_match=max(max_component_match,match)
  dc=sum(z['chi'] for z in components.values())-c;dv=sum(z['pi'] for z in components.values())-v;weighted_match=float(.5*m.wvol@(dv*dv)+.5*m.c**2*m.ww@np.diff(dc)**2)
  trace[-1].update(component_sum_error_energy=weighted_match,bulk_wave_energy=energies['bulk'],conversion_wave_energy=energies['conversion'],interference_wave_energy=d['wave_energy']-sum(energies.values()),bulk_self_far_flux=components['bulk']['flux'],conversion_self_far_flux=components['conversion']['flux'],interference_far_flux=flux-sum(z['flux'] for z in components.values()),component_sum_max_absolute_error=match)
  nextsample=t+config.get('sample_Myr',.1)
 sample()
 while t<config['duration_Myr']-1e-10:
  if time.monotonic()-start>config.get('wall_seconds',600):status='wall_limit_partial';break
  h=min(h,config['duration_Myr']-t)
  try:r=m.full_step(a,x,p,c,v,h/m.tdyn)
  except (RuntimeError,ValueError,np.linalg.LinAlgError) as e:
   r=None;info={'exception':repr(e),'fixed_point_error':float('inf')}
  if r is not None:
   an,xn,pn,cn,vn,ds,dq,info=r;En=m.full_energy(an,xn,pn,cn,vn);defect=En+ds-Eold
   bad=(info['fixed_point_error']>1e-9 or info.get('substep_failed',False) or not np.isfinite(En) or abs(defect)>config.get('step_energy_cap',2e-8) or abs(En+sink+ds-E0)>config.get('global_energy_cap',3e-6))
  else:bad=True;defect=None
  if bad:
   reject+=1;rejections.append({'time_Myr':t,'h_Myr':h,'energy_defect':defect,**{k:val for k,val in info.items() if not k.startswith('source_')}});rejections=rejections[-30:];h*=.5
   if h<config.get('minimum_dt_Myr',1e-6):status='minimum_step_failure';break
   continue
  gamma=m.gamma.copy();factor=np.exp(-gamma*h/m.tdyn/2)
  for z in components.values():
   old=z['pi'].copy();z['pi']*=factor;z['sink']+=float(.5*m.wvol@(old*old-z['pi']**2))
  m.gamma=np.zeros_like(gamma)
  try:
   for stagedt,sourceB,sourceC in info['source_stages']:
    for key,source in [('bulk',sourceB),('conversion',sourceC)]:
     z=components[key];cc,vv,_,_=m.wave_source(z['chi'],z['pi'],source/m.g,stagedt);cm=(cc+z['chi'])/2;vm=(vv+z['pi'])/2;z['flux']+=float(-stagedt*m.c**2*m.ww[edge]*(cm[edge+1]-cm[edge])*(vm[edge+1]+vm[edge])/2);z['chi']=cc;z['pi']=vv
  finally:m.gamma=gamma
  for z in components.values():
   old=z['pi'].copy();z['pi']*=factor;z['sink']+=float(.5*m.wvol@(old*old-z['pi']**2))
  a,x,p,c,v=an,xn,pn,cn,vn;Eold=En;sink+=ds;qs+=dq;work+=info['integrated_work'];bwork+=info['integrated_bulk_work'];cwork+=info['integrated_conversion_work'];flux+=info['integrated_far_flux'];fwork+=info['integrated_far_work'];t+=h;accept+=1;maxroot=max(maxroot,info['fixed_point_error'])
  if t>=nextsample or t>=config['duration_Myr']-1e-10:sample()
  if accept%25==0:dest.with_name('progress.json').write_text(json.dumps({'time_Myr':t,'h_Myr':h,'accepted':accept,'rejected':reject,'runtime_seconds':time.monotonic()-start,'last':trace[-1]}))
  # Periodically challenge a shrunken step; guard acceptance still unchanged.
  if accept%20==0 and h<config['dt_Myr'] and abs(defect)<config.get('step_energy_cap',2e-8)/8:h=min(config['dt_Myr'],h*2)
 if trace[-1]['time_Myr']!=t:sample()
 np.savez_compressed(dest.with_name('components.npz'),bulk_chi=components['bulk']['chi'],bulk_pi=components['bulk']['pi'],conversion_chi=components['conversion']['chi'],conversion_pi=components['conversion']['pi'])
 np.savez_compressed(dest.with_name('state.npz'),a=a,alpha=x,carrier_p=p,chi=c,pi=v)
 np.savez_compressed(dest.with_name('history.npz'),history=np.array(history),r_kpc=rsel,columns=np.array(['time','rhoT','alpha','source','T_edge_current_interpolated']))
 out={'config':config,'status':status,'completed_time_Myr':t,'runtime_seconds':time.monotonic()-start,'accepted_steps':accept,'rejected_steps':reject,'initial_meta':meta,'initial_energy':E0,'max_absolute_energy_error':maxE,'max_charge_error':maxQ,'max_mass_error':maxM,'max_wave_work_error':maxW,'max_far_flux_error':maxF,'max_root_error':maxroot,'max_component_sum_error':max_component_match,'trace':trace,'rejections':rejections,'interpretation':'No supplied wave population; initial dilated/formed mixed material is not unseeded all-F conversion birth. Signed work is not automatically escaped energy. Boundary restoration and formation require a sufficiently long controlled history and perturbation tests.'}
 dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['trace','rejections']},flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--config',required=True);args=ap.parse_args();run(json.loads(Path(args.config).read_text()),args.output)
