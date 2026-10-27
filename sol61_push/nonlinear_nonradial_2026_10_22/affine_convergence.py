import json,argparse
from pathlib import Path
import numpy as np
from isolated import Isolated
p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args();mstar=.08408132497418408
# Gaussian affine flow: T=M/2 sum(adot_i²), C=L²/[2M(a²+b²)].
def run(b=1,spin=.02,n=24,dt=.1,end=25):
 f=Isolated(n,6);M=b*mstar;a=np.array([1.08,.72,.9]);v=np.zeros(3);r=f.evaluate(M,a)
 I=M*sum(a[:2]**2);L=np.sqrt(2*spin*abs(r['gravity'])*I)
 def force(r,a):
  I=M*sum(a[:2]**2);d=np.array(r['axis_log_derivatives'])/a;d[:2]-=L*L*M*a[:2]/I**2
  return -d/M
 def E(r,a,v):return r['energy']+.5*M*sum(v*v)+L*L/(2*M*sum(a[:2]**2))
 E0=E(r,a,v);rows=[];acc=force(r,a);reason='time_limit'
 for step in range(round(end/dt)+1):
  rows.append(dict(t=step*dt,axes=a.tolist(),v=v.tolist(),energy_error=float((E(r,a,v)-E0)/abs(E0)),max_w=r['max_w'],relative_residual=r['relative_residual']))
  if min(a)<1.5*f.dx:reason='resolution_limit';break
  if max(a)>f.box/4:reason='box_tail_limit';break
  if step==round(end/dt):break
  v+=dt*acc/2;a+=dt*v;r=f.evaluate(M,a);acc=force(r,a);v+=dt*acc/2
 return dict(b=b,spin=spin,n=n,dt=dt,L=float(L),E0=float(E0),stop_reason=reason,rows=rows,max_energy_error=max(abs(z['energy_error']) for z in rows))
results=[]
for n,dt in [(40,.05),(48,.1)]:
 results.append(run(b=4,n=n,dt=dt,end=12))
 Path(args.output).write_text(json.dumps(dict(cases=results),indent=2)+'\n')
