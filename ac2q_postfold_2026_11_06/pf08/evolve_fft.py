import argparse,json,time
from pathlib import Path
import numpy as np
from fft_constraints import FFTPadded as Padded,FFTSystem as System
from evolve_projected import rk4
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,required=True);ap.add_argument('--dt',type=float,default=.00125);ap.add_argument('--end',type=float,required=True);ap.add_argument('--evaluation',type=int);ap.add_argument('--restart');a=ap.parse_args()
t0=time.time();m=a.evaluation or 2*a.n+1;s=Padded(a.n,evaluation=m)
if a.restart:
 old=json.loads(Path(a.restart).read_text());assert old['n']==a.n and old['evaluation']==m and old['dt']==a.dt
 y=np.array(old['final_state']);s.fine.P=np.array(old['final_P']);t=old['time'];assert old['status']=='checkpoint'
else:y=s.initial();t=0
out=dict(n=a.n,dt=a.dt,evaluation=m,start=t,end=a.end,restart=a.restart);records=[]
def diagnose(y,t):
 z=s.lift(y,m);l,b,pl,r=s.fine.unpack(z);bx=s.fine.dx(b);pb=r+2*s.fine.M**2*np.exp(4*b)/pl*(2*s.fine.dxx(b)+3*bx**2)
 raw=float(np.max(abs(s.fine.dx(pl)-bx*pb))/(s.k*np.max(abs(pl))))
 zp=s.fine.project(z);f=s.fine.constrain(zp);rr=zp[1+2*m:];spectra={}
 for key,x in dict(q=f['q'],N=f['N'],b=f['b'],r=rr,pb=f['pb']).items():
  coeff=np.fft.fft(x-x.mean());tail=abs(s.fine.modes)>=a.n/3
  spectra[key]=float(np.sum(abs(coeff[tail])**2)/(np.sum(abs(coeff)**2)+1e-100))
 row=s.diagnostic(y,t);row.update(raw_momentum_normalized=raw,spectra=spectra)
 return row
try:
 records.append(diagnose(y,t))
 while t<a.end-1e-12:
  dt=min(a.dt,a.end-t);y=rk4(s,y,dt);t+=dt
  row=diagnose(y,t);records.append(row)
  if row['raw_momentum_normalized']>1e-7:raise RuntimeError('raw momentum tolerance')
  if max(row['spectra'].values())>1e-3:raise RuntimeError('multifield underresolution')
  if time.time()-t0>105:
   out['reason']='wall budget checkpoint before requested end';break
 out['status']='checkpoint'
except (ValueError,RuntimeError,np.linalg.LinAlgError)as e:out['status']='stopped';out['reason']=str(e)
out.update(target_reached=bool(t>=a.end-1e-12),linear_iterations=s.fine.linear_iterations,time=t,seconds=time.time()-t0,records=records,final_state=y.tolist(),final_P=s.fine.P.tolist())
Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['records','final_state','final_P']},indent=2));raise SystemExit(0 if out['status']=='checkpoint'else 1)
