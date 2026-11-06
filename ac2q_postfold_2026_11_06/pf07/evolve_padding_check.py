import argparse,json,time
import numpy as np
from dealias import Padded
from evolve_projected import rk4,validation
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=31);ap.add_argument('--dt',type=float,default=.0025);ap.add_argument('--tmax',type=float,default=.5);ap.add_argument('--padding',type=int,default=3);a=ap.parse_args()
t0=time.time();out={'validation':validation(),'n':a.n,'dt':a.dt,'tmax':a.tmax,'padding':a.padding}
s=Padded(a.n,factor=a.padding);y=s.initial();t=0;records=[]
try:
 if not out['validation']['pass_checks']:raise RuntimeError('validation')
 records.append(s.diagnostic(y,0))
 while t<a.tmax-1e-12:
  dt=min(a.dt,a.tmax-t);y=rk4(s,y,dt);t+=dt
  r=s.diagnostic(y,t)
  # Tail relative to represented spectrum, not the padded evaluation grid.
  f=s.fine.constrain(s.fine.project(s.lift(y,s.fine.n)));q=f['q'];qs=np.fft.fft(q-q.mean())
  tail=abs(s.fine.modes)>=a.n/3
  r['spectral_tail']=float(np.sum(abs(qs[tail])**2)/(np.sum(abs(qs)**2)+1e-100))
  records.append(r)
  if r['spectral_tail']>1e-3:raise RuntimeError('underresolution')
 out['status']='completed pre-break'
except (ValueError,RuntimeError,np.linalg.LinAlgError) as e:out['status']='stopped';out['reason']=str(e)
out.update(time=t,seconds=time.time()-t0,records=records,final_state=y.tolist(),final_P=s.fine.P.tolist())
open(a.output,'w').write(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['records','final_state','final_P']},indent=2))
raise SystemExit(0 if out['status']=='completed pre-break'else 1)
