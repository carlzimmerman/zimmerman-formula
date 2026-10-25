"""Conditional late pulse from the last clean saved complex Draco wave."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,pathlib,resource,subprocess,sys,time,numpy as np,scipy
from refinement_v3 import load,P,ROOT
from fast_flux import flux
from inventory_memory import shells
p=argparse.ArgumentParser();p.add_argument('--tag',required=True);p.add_argument('--dt',type=float,default=.04);p.add_argument('--T',type=float,default=20.);p.add_argument('--wall',type=float,default=220);p.add_argument('--resume');a=p.parse_args();dest=P/'refined_runs';dest.mkdir(exist_ok=True);outpath=dest/(a.tag+'.json');assert not outpath.exists();start=time.time();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
pins=[P/x for x in ['refined_pulse.py','refinement_v3.py','memory_gauss_v2.py','memory_gauss.py','gauss.py','lean.py','inventory_memory.py','fast_flux.py','REFINED_PULSE_CONTRACT.md','MEMORY_POISSON_CONTRACT.md','refinement_preflight_fallback.json','runs/draco_joint_s05.json','runs/draco_joint_s05.npz']]
from lean import OLD
pins += [OLD/x for x in ['sphere_v3.py','flux.py','budget.py']]
if a.resume:pins += [dest/(a.resume+x) for x in ['.json','.npz']]
def hashes():return {str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in pins}
before=hashes();assert json.loads((P/'refinement_preflight_fallback.json').read_text())['headroom_pass'];s,u,pot,units,seed=load(nt=48,nf=80);t=seed['seed_absolute_T'];initial=s.moments(u,pot);b0=shells(s,u,pot);mrad0=np.sum(abs(u)**2,axis=(1,2));history=[];scale=initial['K']+abs(initial['W'])
if a.resume:
 d=json.loads((dest/(a.resume+'.json')).read_text());raw=np.load(dest/(a.resume+'.npz'));assert d['status'] in ['wall checkpoint','finished requested interval'];assert d['inputs_before']==d['inputs_after']
 for f,v in d['inputs_after'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==v
 for k,v in dict(r=s.r,w=s.w,mu=s.mu,aw=s.aw,S=s.phase).items():assert np.array_equal(raw[k],v)
 assert d['physical']==units and d['seed_refinement']==seed
 assert max(abs(d['history'][-1]['E_relative_error']),abs(d['history'][-1]['Jz_relative_error']),d['history'][-1]['angular_edge_fraction'],d['history'][-1]['azimuth_edge_fraction'])<.01
 u=raw['u'];pot=s.poisson(u);t=d['history'][-1]['t'];history=d['history'];initial=d['initial_moments'];b0=d['initial_inventory'];scale=initial['K']+abs(initial['W']);s.transport_mass[:]=d['finite_mass_transport'];s.transport_Jz[:]=d['finite_radial_matter_Jz_transport'];del raw
status='finished requested interval'
def diag():
 h=s.moments(u,pot);h.update(t=t,elapsed_Myr=t*units['tunit_Myr'],E_relative_error=(h['E']-initial['E'])/scale,Jz_relative_error=(h['Jz']-initial['Jz'])/max(abs(initial['Jz']),s.eta*initial['M']),flux=flux(s,u,pot));history.append(h);print(a.tag,t,h['M_inner']*units['Munit_Msun'],h['E_relative_error'],h['Jz_relative_error'],h['angular_edge_fraction'],flush=True);return h
h=diag()
while t<a.T-1e-12:
 dt=min(a.dt,a.T-t);u,pot=s.step(u,pot,dt);t+=dt;h=diag()
 if abs(h['M']/initial['M']-1)>1e-10 or max(abs(h['E_relative_error']),abs(h['Jz_relative_error']),h['angular_edge_fraction'],h['azimuth_edge_fraction'])>.01 or h['boundary_fraction']>1e-4:status='physical acceptance stop';break
 if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=750_000_000:status='memory headroom stop';break
 if time.time()-start>a.wall:status='wall checkpoint';break
b1=shells(s,u,pot);hh={round(h['t'],12):h for h in history};hist=[hh[k] for k in sorted(hh)];tt=[h['t'] for h in hist];budgets={}
for key,q in [('mass','M'),('energy','E_canonical'),('Jz','Jz')]:
 v=np.trapz([h['flux'][key] for h in hist],tt,axis=0);res=np.array(b1[q])-b0[q]+v;budgets[key]=dict(net_outward=v.tolist(),residual=res.tolist(),residual_over_transport=(abs(res)/np.maximum(abs(v),1e-30)).tolist())
finite=float(np.max(abs(np.cumsum(np.sum(abs(u)**2,axis=(1,2))-mrad0)[:-1]+s.transport_mass)));assert finite<1e-10
out=dict(parameters=vars(a),scope='conditional angular-refined late pulse; no corrected formation, remnant, stars or four-dwarf closure',seed_refinement=seed,physical=units,initial_moments=initial,initial_inventory=b0,final_inventory=b1,history=history,budgets=budgets,finite_mass_transport=s.transport_mass.tolist(),finite_radial_matter_Jz_transport=s.transport_Jz.tolist(),finite_mass_residual=finite,inputs_before=before,inputs_after=hashes(),revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=sys.argv,interpreter=sys.executable,software=dict(Python=sys.version,numpy=np.__version__,scipy=scipy.__version__),status=status,seconds=time.time()-start)
assert before==out['inputs_after'];np.savez_compressed(dest/(a.tag+'.npz'),u=u,phi=pot,r=s.r,w=s.w,mu=s.mu,aw=s.aw,S=s.phase);out['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;outpath.write_text(json.dumps(out,indent=2)+'\n');print(status,out['peak_RSS_bytes'],flush=True)
