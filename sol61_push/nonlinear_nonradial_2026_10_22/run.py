import argparse,json
from pathlib import Path
import numpy as np
from field import Field
p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args();rows=[];checks=[];f=Field();mstar=.08408132497418408
for R in [.4,.6,.9,1.3]:
 forces={}
 for b in [.5,1,2,4]:
  r,a,fg,h=f.solve(mstar*b,R);q,aq,_,_=f.solve(mstar*b,R,quadratic=True);r['quadratic_energy']=q['energy'];r['quadratic_force_norm']=q['force_norm'];rows.append(r);forces[b]=a
  print('case',R,b,r['relative_residual'],r['max_w'],r['energy'],flush=True)
  checks.append(dict(name='residual_%g_%g'%(R,b),passed=r['relative_residual']<1e-5,value=r['relative_residual']))
  if R==.6 and b==1:
   direction=np.sin(np.arange(h.size)).reshape(h.shape);direction/=np.linalg.norm(direction);eps=1e-5
   fd=(fg((h+eps*direction).ravel())[0]-fg((h-eps*direction).ravel())[0])/(2*eps);analytic=np.dot(fg(h.ravel())[1],direction.ravel())
   checks.append(dict(name='dual_gradient',passed=abs(fd-analytic)<1e-7,value=float(abs(fd-analytic))))
 for r in rows[-4:]:r['mass_scaled_force_difference']=float(np.linalg.norm(forces[r['mass']/mstar]/(r['mass']/mstar)-forces[1])/np.linalg.norm(forces[1]))
ref=[]
for n,box in [(48,8),(48,12)]:
 for b in [1,4]:
  r,_,_,_=Field(n,box).solve(mstar*b,.6);ref.append(r)
result=dict(rows=rows,refinement=ref,checks=checks)
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
