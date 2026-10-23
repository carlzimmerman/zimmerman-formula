import json,sys
from pathlib import Path
import numpy as np
p=Path(__file__).parent
# Reuse the exact same force and energy definitions; no previous evolution loop.
source=(p/'reciprocal_collapse_v2.py').read_text();body=source.split(' E0=')[0].split('for N,h in [(32,.000125),(64,.0000625)]:')[1]
rows=[]
for N,tolerance in [(32,1e-7)]:
 ns={'N':N,'np':np};exec('\n'.join(line[1:] if line.startswith(' ') else line for line in body.splitlines()),ns)
 force=ns['forces'];energy=ns['energy'];r=ns['r'];v=ns['v'];B=ns['B'];V=ns['V'];w=ns['w'];m=ns['m'];E0=energy(r,v,B,V);y=np.r_[r,B,v,V];t=0.;h=.01;accepted=0;rejected=0;samples=[];failure=None;next_sample=0.
 def step(y,h):
  rr=y[:N].copy();bb=float(y[N]);vv=y[N+1:2*N+1].copy();VV=float(y[-1]);aa,ab=force(rr,bb);vv+=h*aa/2;VV+=h*ab/2;rr+=h*vv;bb+=h*VV;aa,ab=force(rr,bb);vv+=h*aa/2;VV+=h*ab/2;return np.r_[rr,bb,vv,VV]
 while t<15 and accepted+rejected<300000:
  h=min(h,15-t)
  try:
   one=step(y,h);half=step(step(y,h/2),h/2);err=float(np.max(abs(half-one)/(1+abs(half))))/tolerance
  except ValueError:err=np.inf
  if err>1:
   rejected+=1;h*=.5 if not np.isfinite(err) else max(.2,.8*err**(-1/3))
   if h<1e-15:failure='minimum step';break
   continue
  y=half;t+=h;accepted+=1;h=min(.02,h*(2 if err==0 else min(2,max(.5,.9*err**(-1/3)))))
  if t>=next_sample or t>=15:
   rr=y[:N];bb=float(y[N]);vv=y[N+1:2*N+1];VV=float(y[-1]);samples.append(dict(t=t,B=bb,cold_half_mass_radius=float(np.interp(.5,m,rr)),cold_edge=float(rr[-1]),energy=energy(rr,vv,bb,VV),max_q=float(max(m/rr**2)),min_gap=float(min(np.diff(np.r_[0,rr])))));next_sample=t+.1
 if t<15 and failure is None:failure='step budget'
 rows.append(dict(final_state=y.tolist(),final_step=h,final_energy=energy(y[:N],y[N+1:2*N+1],float(y[N]),float(y[-1])),N=N,tolerance=tolerance,initial_energy=E0,final_time=t,accepted=accepted,rejected=rejected,failure=failure,max_energy_error=max(abs(x['energy']-E0) for x in samples),samples=samples))
checks=dict(completed=all(r['failure'] is None for r in rows),energy=all(r['max_energy_error']<1e-4 for r in rows),domain=all(s['max_q']<1 and s['min_gap']>0 for r in rows for s in r['samples']))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,scope='adaptive conservative-model collapse; local step-doubling errors controlled, energy monitored; no asymptotic equilibrium claim')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({**out,'rows':[{**r,'samples':r['samples'][-2:]} for r in rows]},indent=2));sys.exit(0 if out['all_pass'] else 1)
