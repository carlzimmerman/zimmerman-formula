import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,pathlib,json,numpy as np
Q=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(Q.parent/'cold_resolved_pulse_2026_10_25'))
from memory_gauss_v2 import Sphere
from radial_phase import radial_phase
s=Sphere(64,16,16,R=12,alpha=4,eta=.2);u=np.pi**(-.75)*np.exp(-s.r[:,None,None]**2/2)*s.sr[:,None,None]*s.sa[None,:,:];z=s.r[:,None,None]*s.mu[None,:,None];zero=radial_phase(s,u);boost=radial_phase(s,u*np.exp(1j*.6*z));assert zero==0 and abs(boost-.0024)<2e-8
s1=Sphere(64,16,16,R=12,alpha=4,eta=.2,phase=lambda r,der=0:.2*r if der else .1*r*r);carrier=radial_phase(s1,u);assert abs(carrier-.03)<1e-10;print(json.dumps(dict(real=zero,plane_z=boost,expected_plane=.0024,carrier=carrier,expected_carrier=.03),indent=2))
