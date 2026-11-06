"""Exploratory mode Jacobians; no physical inference without refinement."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import numpy as np
from evolve_projected import System
out=[]
for m in [1,4,10,15]:
 s=System(31,128);y=s.initial(True);n=s.n;cs=np.cos(2*np.pi*np.arange(n)*m/n)
 mat=np.zeros((2,2))
 for j in range(2):
  pert=np.zeros_like(y);pert[1+j*2*n:1+j*2*n+n]=cs
  ep=1e-9 if j==0 else 1e-6
  s.P*=0;fp=s.rhs(y+ep*pert);s.P*=0;fm=s.rhs(y-ep*pert)
  delta=(fp-fm)/(2*ep)
  mat[:,j]=[2*np.mean(delta[1:1+n]*cs),2*np.mean(delta[1+2*n:]*cs)]
 out.append(dict(mode=m,matrix=mat.tolist(),eigenvalues=[str(x)for x in np.linalg.eigvals(mat)]))
print(json.dumps(out,indent=2))
