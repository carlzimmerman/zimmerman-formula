import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,pathlib,resource,sys,numpy as np,scipy
from scipy.interpolate import CubicSpline
from lean import Sphere,OLD
from inventory import shells
from phase_energy import measure
from budget import initial
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];p=argparse.ArgumentParser();p.add_argument('--through',type=int,required=True);p.add_argument('--output',required=True);a=p.parse_args();files=[P/'runs'/('draco_joint_s%02d.json'%i) for i in range(1,a.through+1)];src=ROOT/'sol61_push/cold_envelope_formation_2026_10_24/runs/draco_escape_long_fields.npz';pins=[P/'analyze.py',P/'inventory.py',P/'phase_energy.py',P/'lean.py',OLD/'sphere_v3.py',OLD/'budget.py',OLD/'flux.py',src]+files+[f.with_suffix('.npz') for f in files]
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}
before=hashes();meta=json.loads(files[0].read_text());pars=meta['parameters'];units=meta['physical'];eta=units['eta_code'];old=np.load(src);r,v,lm=[old[k] for k in ['r','initial','lm']];j=next(j for j,x in enumerate(lm) if tuple(x)==(0,0));valid=(r<21.8)&(abs(v[:,j])>1e-20);rv=r[valid];sp=CubicSpline(rv,eta*np.unwrap(np.angle(v[valid,j])))
def phase(x,der=0):
 if der:return np.where(x<=rv[-1],sp(x,1),sp(rv[-1],1))
 return np.where(x<=rv[-1],sp(x),sp(rv[-1])+sp(rv[-1],1)*(x-rv[-1]))
s=Sphere(pars['ne'],pars['nt'],pars['nf'],eta=eta,phase=phase);u0=initial(s,old);p0=s.poisson(u0);b0=shells(s,u0,p0);q0=measure(s,u0);m0rad=np.sum(abs(u0)**2,axis=(1,2));previous=b0;previous_t=0;rows=[];del u0,p0
for f in files:
 d=json.loads(f.read_text());raw=np.load(f.with_suffix('.npz'));u=raw['u'];pot=raw['phi'];b=shells(s,u,pot);q=measure(s,u);assert abs(b['K_global_SEM']-q['K_operator'])<1e-10
 # Duplicated checkpoint instants have zero duration; retain the newest identical state.
 hh={round(h['t'],12):h for h in d['history']};hist=[hh[k] for k in sorted(hh)];tt=np.array([h['t'] for h in hist]);local=[h for h in hist if h['t']>=previous_t-1e-12];lt=np.array([h['t'] for h in local]);ints={k:np.trapz([h['flux'][k] for h in hist],tt,axis=0) for k in ['mass','energy','Jz']};lints={k:np.trapz([h['flux'][k] for h in local],lt,axis=0) for k in ints}
 def budget(start,flux):
  result={}
  for k,z in [('mass','M'),('energy','E_canonical'),('Jz','Jz')]:
   residual=np.array(b[z])-start[z]+flux[k];result[k]=dict(net_outward=flux[k].tolist(),residual=residual.tolist(),residual_over_transport=(abs(residual)/np.maximum(abs(flux[k]),1e-30)).tolist())
  return result
 change=np.cumsum(np.sum(abs(u)**2,axis=(1,2))-m0rad)[:-1];finite=float(np.max(abs(change+d['finite_mass_transport'])));assert finite<1e-10
 row=dict(tag=f.stem,T=float(tt[-1]),M_Rstar_Msun=b['M'][0]*units['Munit_Msun'],status=d['status'],last=d['history'][-1],inventory=b,field_support=q,finite_mass_residual=finite,cumulative=budget(b0,ints),last_segment=dict(start=previous_t,end=float(tt[-1]),budgets=budget(previous,lints)));rows.append(row);previous=b;previous_t=tt[-1];print(f.stem,tt[-1],row['M_Rstar_Msun'],'Jerr',row['last']['Jz_relative_error'],'Ebudget',row['cumulative']['energy']['residual_over_transport'],flush=True)
 del u,pot,raw
out=dict(initial_inventory=b0,initial_support=q0,physical=units,rows=rows,inputs_before=before,inputs_after=hashes(),software=dict(Python=sys.version,numpy=np.__version__,scipy=scipy.__version__),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
assert before==out['inputs_after'] and out['peak_RSS_bytes']<1_000_000_000;(P/a.output).write_text(json.dumps(out,indent=2)+'\n')
