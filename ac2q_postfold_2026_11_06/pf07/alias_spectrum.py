import argparse,json
import numpy as np
from dealias import Padded
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=[]
for n in [15,31]:
 for factor in [1,3]:
  s=Padded(n,factor=factor);y=s.initial();s.diagnostic(y,0)
  J=np.zeros((2*n,2*n))
  for j in range(2*n):
   col=np.zeros_like(y);ep=1e-9 if j<n else 1e-6;idx=1+j if j<n else 1+n+j
   col[idx]=ep;fp=s.rhs(y+col);fm=s.rhs(y-col);v=(fp-fm)/(2*ep)
   J[:,j]=np.concatenate([v[1:1+n],v[1+2*n:]])
  ev=np.linalg.eigvals(J);out.append(dict(n=n,padding=factor,max_real=float(ev.real.max()),max_abs_imag=float(abs(ev.imag).max()),largest=[str(x)for x in sorted(ev,key=lambda z:z.real)[-6:]]))
print(json.dumps(out,indent=2));open(a.output,'w').write(json.dumps(out,indent=2)+'\n')
