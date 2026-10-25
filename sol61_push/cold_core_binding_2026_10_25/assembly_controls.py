import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,pathlib,json,numpy as np
P=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'cold_resolved_pulse_2026_10_25'))
from memory_gauss_v2 import Sphere
phase=lambda r,der=0: .2*r if der else .1*r*r
s0=Sphere(64,16,16,R=12,alpha=4,eta=.2);s1=Sphere(64,16,16,R=12,alpha=4,eta=.2,phase=phase);u=np.pi**(-.75)*np.exp(-s0.r[:,None,None]**2/2)*s0.sr[:,None,None]*s0.sa[None,:,:];A=.5*float(np.sum(abs(u)**2*s1.p[:,None,None]**2));K0=float(np.vdot(u,s0.radial_apply(u)).real+np.vdot(u,s0.angular(u,0,True)).real);B=float(np.vdot(u,s1.radial_apply(u)-s0.radial_apply(u)).real)-A;assert abs(A-.03)<1e-10 and abs(B)<1e-10;rows=[]
for lam in [0,.25,.75,1,1.25]:
 s=Sphere(64,16,16,R=12,alpha=4,eta=.2,phase=lambda r,der=0:lam*phase(r,der));K=float(np.vdot(u,s.radial_apply(u)).real+np.vdot(u,s.angular(u,0,True)).real);expected=A*lam*lam+B*lam+K0;assert abs(K-expected)<1e-12;rows.append(dict(lam=lam,K=K,quadratic=expected,analytic=.03+.03*lam*lam))
print(json.dumps(rows,indent=2))
