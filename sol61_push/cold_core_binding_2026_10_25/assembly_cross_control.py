import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,pathlib,json,numpy as np
P=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'cold_resolved_pulse_2026_10_25'))
from memory_gauss_v2 import Sphere
f=lambda r,der=0:.26*r if der else .13*r*r
s0=Sphere(8,8,8,eta=.2);s1=Sphere(8,8,8,eta=.2,phase=f);rng=np.random.default_rng(283);u=rng.normal(size=(len(s0.r),8,8))+1j*rng.normal(size=(len(s0.r),8,8));u/=np.linalg.norm(u);A=.5*float(np.sum(abs(u)**2*s1.p[:,None,None]**2));B=float(np.vdot(u,np.einsum('ij,jkl->ikl',s1.H-s0.H-np.diag(.5*s1.p*s1.p),u)).real);C=float(np.vdot(u,s0.radial_apply(u)).real+np.vdot(u,s0.angular(u,0,True)).real);assert abs(B)>1e-6;rows=[]
for lam in [.25,.75,1.25]:
 s=Sphere(8,8,8,eta=.2,phase=lambda r,der=0:lam*f(r,der));actual=float(np.vdot(u,s.radial_apply(u)).real+np.vdot(u,s.angular(u,0,True)).real);expected=A*lam*lam+B*lam+C;assert abs(actual-expected)<1e-11;rows.append(dict(lam=lam,actual=actual,quadratic=expected,nonzero_B=B))
print(json.dumps(rows,indent=2))
