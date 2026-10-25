import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,numpy as np
from sphere_v3 import Sphere
rows=[]
for nf in [32,64]:
 s=Sphere(32,24,nf,eta=.2);r=s.r[:,None,None];mu=s.mu[None,:,None];ph=s.phi[None,None,:];A=r**16*np.exp(-r*r/2)*(1-mu*mu)**8*(np.exp(16j*ph)+.7*np.exp(1j*np.pi/4)*np.exp(-16j*ph));u=A*s.sr[:,None,None]*s.sa[None,:,:];u/=np.linalg.norm(u);pot=s.poisson(u);Jop=s.transform(s.transform(u)*s.eta*s.m[None,None,:],True);torque=2*np.real(np.vdot(Jop,-1j/s.eta*pot*u));h=s.moments(u,pot);rows.append(dict(nf=nf,torque=float(torque),angular_edge=h['angular_edge_fraction'],azimuth_edge=h['azimuth_edge_fraction']))
assert abs(rows[0]['torque'])>.01 and abs(rows[1]['torque'])<1e-10
print(json.dumps(rows,indent=2))
