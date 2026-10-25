"""Conditional same-seed short pulse; no claim of higher-accuracy formation history."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,pathlib,resource,subprocess,sys,time,numpy as np,scipy
from scipy.interpolate import CubicSpline
from lean import OLD,Sphere as CN
from gauss import Sphere as Gauss
from inventory import shells
from flux import flux
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];p=argparse.ArgumentParser();p.add_argument('--method',choices=['cn','gauss'],required=True);p.add_argument('--dt',type=float,required=True);p.add_argument('--T',type=float,default=.2);p.add_argument('--tag',required=True);a=p.parse_args();start=time.time();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();seed=OLD/'runs/draco_v2_256';data=ROOT/'sol61_push/cold_envelope_formation_2026_10_24/runs/draco_escape_long_fields.npz';pins=[P/'pulse_compare.py',P/'lean.py',P/'gauss.py',P/'inventory.py',P/'GAUSS_CONTRACT.md',OLD/'sphere_v3.py',OLD/'flux.py',OLD/'budget.py',pathlib.Path(str(seed)+'.json'),pathlib.Path(str(seed)+'.npz'),data]
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}
before=hashes();d=json.loads(pathlib.Path(str(seed)+'.json').read_text());raw=np.load(str(seed)+'.npz');assert d['status']=='finished requested finite interval';units=d['physical'];eta=units['eta_code'];source=np.load(data);r,v,lm=[source[k] for k in ['r','initial','lm']];j=next(j for j,x in enumerate(lm) if tuple(x)==(0,0));valid=(r<21.8)&(abs(v[:,j])>1e-20);rv=r[valid];sp=CubicSpline(rv,eta*np.unwrap(np.angle(v[valid,j])))
def phase(x,der=0):
 if der:return np.where(x<=rv[-1],sp(x,1),sp(rv[-1],1))
 return np.where(x<=rv[-1],sp(x),sp(rv[-1])+sp(rv[-1],1)*(x-rv[-1]))
s=(CN if a.method=='cn' else Gauss)(256,24,32,eta=eta,phase=phase)
for k,q in dict(r=s.r,w=s.w,mu=s.mu,aw=s.aw,S=s.phase).items():assert np.array_equal(raw[k],q)
u=raw['u'];pot=s.poisson(u);assert np.max(abs(pot-raw['phi']))<1e-12;initial=s.moments(u,pot);b0=shells(s,u,pot);history=[];scale=initial['K']+abs(initial['W']);m0rad=np.sum(abs(u)**2,axis=(1,2));status='finished requested finite interval'
def diag(t):
 h=s.moments(u,pot);h.update(t=t,seed_absolute_T=d['history'][-1]['t'],E_relative_error=(h['E']-initial['E'])/scale,Jz_relative_error=(h['Jz']-initial['Jz'])/max(abs(initial['Jz']),eta*initial['M']),flux=flux(s,u,pot));history.append(h);return h
h=diag(0)
for it in range(round(a.T/a.dt)):
 u,pot=s.step(u,pot,a.dt);h=diag((it+1)*a.dt)
 if abs(h['M']/initial['M']-1)>1e-10 or max(abs(h['E_relative_error']),abs(h['Jz_relative_error']),h['angular_edge_fraction'],h['azimuth_edge_fraction'])>.05:status='stopped numerical gate';break
 if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>750_000_000:status='stopped memory headroom';break
b1=shells(s,u,pot);tt=[h['t'] for h in history];budget={}
for key,q in [('mass','M'),('energy','E_canonical'),('Jz','Jz')]:
 val=np.trapz([h['flux'][key] for h in history],tt,axis=0);res=np.array(b1[q])-b0[q]+val;budget[key]=dict(net_outward=val.tolist(),residual=res.tolist(),residual_over_transport=(abs(res)/np.maximum(abs(val),1e-30)).tolist())
finite=float(np.max(abs(np.cumsum(np.sum(abs(u)**2,axis=(1,2))-m0rad)[:-1]+s.transport_mass)));assert finite<1e-10
out=dict(parameters=vars(a),physical=units,scope='conditional short pulse from accepted CCT015 T8 saved wave, local reference reset; not a re-evolved or corrected formation history',started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),interpreter=sys.executable,argv=sys.argv,software=dict(Python=sys.version,numpy=np.__version__,scipy=scipy.__version__),inputs_before=before,inputs_after=hashes(),initial_moments=initial,initial_inventory=b0,final_inventory=b1,history=history,budgets=budget,finite_mass_residual=finite,status=status,seconds=time.time()-start)
assert before==out['inputs_after'];dest=P/'pulse_runs';dest.mkdir(exist_ok=True);assert not (dest/(a.tag+'.json')).exists();np.savez_compressed(dest/(a.tag+'.npz'),u=u,phi=pot);out['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;(dest/(a.tag+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(a.tag,status,history[-1]['E_relative_error'],out['peak_RSS_bytes'],flush=True)
