import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,pathlib,json,numpy as np
P=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'cold_resolved_pulse_2026_10_25'))
from memory_gauss_v2 import Sphere
from phase_energy import measure
from phase_support import phase_kinetic
from binding import window
s=Sphere(8,8,8,eta=.2,phase=lambda r,der=0:.14*r if der else .07*r*r);rng=np.random.default_rng(282);u=rng.normal(size=(len(s.r),8,8))+1j*rng.normal(size=(len(s.r),8,8));u/=np.linalg.norm(u);rows=[]
for a,b in [(None,None),(.75,1),(1,2)]:
 v=u if a is None else window(s,u,a,b);x=phase_kinetic(s,v);old=measure(s,v);assert abs(x-old['K_phase'])<1e-11*max(1,abs(x)) and 0<=x<=old['K_operator']+1e-11;rows.append(dict(a=a,b=b,K_phase=x,reference=old['K_phase'],K_operator=old['K_operator']))
print(json.dumps(rows,indent=2))
