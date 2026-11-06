import argparse,json,time
from pathlib import Path
import numpy as np
from reduced_system_v2 import ReducedSystem,rk4
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,required=True);ap.add_argument('--dt',type=float,required=True);ap.add_argument('--end',type=float,required=True);ap.add_argument('--restart');a=ap.parse_args()
t0=time.time();s=ReducedSystem(a.n);m=s.m;t=0
if a.restart:
 old=json.loads(Path(a.restart).read_text());assert old['n']==a.n and old['evaluation']==m and old['status']=='checkpoint'
 z=np.array(old['final_state']);t=old['time']
 if old.get('representation')=='reduced':y=z
 else:
  n=a.n;assert len(z)==3*n+1;y=np.concatenate([z[:1+n],[z[1+n:1+2*n].mean()],z[1+2*n:]])
 s.fine.P=np.array(old['final_P']);s.fine.gvar=np.array(old['final_gvar'])
 if 'final_pl' in old:s.cached_pl=np.array(old['final_pl'])
else:y=s.initial()
out=dict(n=a.n,evaluation=m,dt=a.dt,start=t,end=a.end,restart=a.restart,representation='reduced');records=[]
def check():
 row=s.diagnostic(y,t);records.append(row)
 if row['momentum_abs']>1e-8:raise RuntimeError('momentum residual')
 if row['represented_rate_error']>1e-6:raise RuntimeError('canonical momentum rate')
 if max(row['spectra'].values())>1e-3:raise RuntimeError('multifield underresolution')
try:
 check()
 while t<a.end-1e-12:
  dt=min(a.dt,a.end-t);y=rk4(s,y,dt);t+=dt;check()
  if time.time()-t0>105:out['reason']='wall budget checkpoint before requested end';break
 out['status']='checkpoint'
except (ValueError,RuntimeError,np.linalg.LinAlgError)as e:out['status']='stopped';out['reason']=str(e)
out.update(target_reached=bool(t>=a.end-1e-12),time=t,seconds=time.time()-t0,records=records,final_state=y.tolist(),final_P=s.fine.P.tolist(),final_gvar=s.fine.gvar.tolist(),final_pl=s.cached_pl.tolist())
Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if not k.startswith('final_')and k!='records'},indent=2));raise SystemExit(0 if out['status']=='checkpoint'else 1)
