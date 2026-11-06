import sys
sys.path.insert(0,'ac2q_postfold_2026_11_06/coupled')
from evolve_constrained import System,rk4
import numpy as np
for dt in [.0001,.000025]:
 s=System(31,128);y=s.initial();t=0
 try:
  for i in range(round(.15/dt)):
   y=rk4(s,y,dt);t+=dt
   if i%100==99:
    r=s.diagnostic(y,t)
    if r['spectral_tail']>1e-3:raise RuntimeError('tail')
  print(dt,t,r,flush=True)
 except Exception as e: print(dt,t,str(e),flush=True)
