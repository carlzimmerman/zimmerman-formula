"""Separate local timestep check; never merge changed dt into an earlier history."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,pathlib,resource,subprocess,sys,time,numpy as np,scipy
from refinement_v3 import load,P,ROOT
from fast_flux import flux
from inventory_memory import shells
p=argparse.ArgumentParser();p.add_argument('--seed',required=True);p.add_argument('--dt',type=float,required=True);p.add_argument('--T',type=float,default=.2);p.add_argument('--tag',required=True);a=p.parse_args();start=time.time();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();sf=P/'refined_runs'/(a.seed+'.json');d=json.loads(sf.read_text());assert d['status'] in ['wall checkpoint','finished requested interval'];assert d['inputs_before']==d['inputs_after'];last=d['history'][-1];assert max(abs(last['E_relative_error']),abs(last['Jz_relative_error']),last['angular_edge_fraction'],last['azimuth_edge_fraction'])<.01
pins=[ROOT/q for q in d['inputs_after']]+[sf,sf.with_suffix('.npz'),P/'late_compare.py'];pins=sorted(set(pins))
def hashes():return {str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in pins}
before=hashes()
for q,v in d['inputs_after'].items():assert before[q]==v
ne,nt,nf=d['seed_refinement']['new_grid'];s,u,pot,units,seed=load(nt=nt,nf=nf);raw=np.load(sf.with_suffix('.npz'));u=raw['u'];pot=s.poisson(u);assert np.max(abs(pot-raw['phi']))<1e-12;del raw
initial=s.moments(u,pot);b0=shells(s,u,pot);mrad0=np.sum(abs(u)**2,axis=(1,2));scale=initial['K']+abs(initial['W']);history=[];t=0.;status='finished requested interval'
def diag():
 h=s.moments(u,pot);h.update(t=t,absolute_T=last['t']+t,E_relative_error=(h['E']-initial['E'])/scale,Jz_relative_error=(h['Jz']-initial['Jz'])/max(abs(initial['Jz']),s.eta*initial['M']),flux=flux(s,u,pot));history.append(h);return h
h=diag()
while t<a.T-1e-12:
 dt=min(a.dt,a.T-t);u,pot=s.step(u,pot,dt);t+=dt;h=diag()
 if abs(h['M']/initial['M']-1)>1e-10 or max(abs(h['E_relative_error']),abs(h['Jz_relative_error']),h['angular_edge_fraction'],h['azimuth_edge_fraction'])>.01 or h['boundary_fraction']>1e-4:status='physical acceptance stop';break
 if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=750_000_000:status='memory headroom stop';break
b1=shells(s,u,pot);budgets={}
for key,q in [('mass','M'),('energy','E_canonical'),('Jz','Jz')]:
 v=np.trapz([h['flux'][key] for h in history],[h['t'] for h in history],axis=0);res=np.array(b1[q])-b0[q]+v;budgets[key]=dict(net_outward=v.tolist(),residual=res.tolist(),residual_over_transport=(abs(res)/np.maximum(abs(v),1e-30)).tolist())
finite=float(np.max(abs(np.cumsum(np.sum(abs(u)**2,axis=(1,2))-mrad0)[:-1]+s.transport_mass)));assert finite<1e-10
out=dict(parameters=vars(a),scope='separate conditional short latepulse, reset local reference; timestep comparison only',physical=units,seed_absolute_T=last['t'],initial_moments=initial,initial_inventory=b0,final_inventory=b1,history=history,budgets=budgets,finite_mass_residual=finite,inputs_before=before,inputs_after=hashes(),revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=sys.argv,interpreter=sys.executable,software=dict(Python=sys.version,numpy=np.__version__,scipy=scipy.__version__),status=status,seconds=time.time()-start)
assert before==out['inputs_after'];dest=P/'late_runs';dest.mkdir(exist_ok=True);assert not (dest/(a.tag+'.json')).exists();np.savez_compressed(dest/(a.tag+'.npz'),u=u,phi=pot);out['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;(dest/(a.tag+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(a.tag,status,h['E_relative_error'],out['peak_RSS_bytes'],flush=True)
