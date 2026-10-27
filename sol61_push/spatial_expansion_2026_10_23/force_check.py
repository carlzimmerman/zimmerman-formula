import argparse,json
from pathlib import Path
import numpy as np
from model import Model
p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args();m=Model(8,.001);xc=m.x0.copy();xb=xc.copy();P,c,res=m.fields(xc);z=np.zeros_like(xc);Z=np.zeros_like(P);v=np.zeros_like(c);state=m.evaluate(xc,xb,P,c,1,z,z,Z,v);j=13;axis=1;expected=-m.mc*state[0][j,axis];rows=[]
for eps in [1e-4,1e-5,1e-6,1e-7,1e-8]:
 xp=xc.copy();xm=xc.copy();xp[j,axis]+=eps;xm[j,axis]-=eps;fd=(m.evaluate(xp,xb,P,c,1,z,z,Z,v)[4]-m.evaluate(xm,xb,P,c,1,z,z,Z,v)[4])/(2*eps);rows.append(dict(eps=eps,derivative=fd,expected=expected,error=abs(fd-expected)/abs(expected)))
checks=[dict(name='two_smallest_force_steps',passed=bool(max(x['error'] for x in rows[-2:])<1e-5),value=float(max(x['error'] for x in rows[-2:])))]
Path(args.output).write_text(json.dumps(dict(checks=checks,rows=rows),indent=2,default=lambda x:x.item())+'\n')
