import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,pathlib,json,numpy as np
P=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'cold_resolved_pulse_2026_10_25'))
from memory_gauss_v2 import Sphere
from phase_energy import measure as old_measure
from binding import window
from phase_support import phase_kinetic
rows=[];s=Sphere(64,16,16,R=12,alpha=4,eta=.2);r=s.r[:,None,None];u=np.pi**(-.75)*np.exp(-r*r/2)*s.sr[:,None,None]*s.sa[None,:,:];boost=u*np.exp(1j*.6*r*s.mu[None,:,None])
for a,b in [(None,None),(.75,1),(1,2),(2,4)]:
 v=boost if a is None else window(s,boost,a,b);zero=u if a is None else window(s,u,a,b);expected=.0072*float(np.vdot(v,v).real);actual=phase_kinetic(s,v);raw=phase_kinetic(s,boost,a,b);old=old_measure(s,v)['K_phase'];assert phase_kinetic(s,zero)==0;assert abs(actual-expected)<2e-6 and abs(raw-expected)<2e-6 and abs(actual-old)<1e-12;rows.append(dict(a=a,b=b,expected=expected,cut=actual,raw_weighted=raw,previous_partition=old))
print(json.dumps(rows,indent=2))
