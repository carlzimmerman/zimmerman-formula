import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,pathlib,json,numpy as np
P=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[0]/'cold_resolved_pulse_2026_10_25'))
from memory_gauss_v2 import Sphere
from binding import measure,negative_weight_bounds,window
rng=np.random.default_rng(281);rows=[]
for i in range(1000):
 e=np.r_[-2.,rng.uniform(-2,3,7)];p=rng.dirichlet(np.ones(len(e)));mu=float(p@e);var=float(p@((e-mu)**2));lo,hi=negative_weight_bounds(mu,var,-2.);actual=float(p[e<0].sum());assert lo-1e-13<=actual<=hi+1e-13
rows.append(dict(check='exact finite spectral measures',cases=1000))
for ne in [64,128]:
 s=Sphere(ne,16,16,R=12,alpha=4,eta=.2);r=s.r[:,None,None];u=np.pi**(-.75)*np.exp(-r*r/2)*s.sr[:,None,None]*s.sa[None,:,:];plain=measure(s,u);boost=measure(s,u*np.exp(1j*.6*r*s.mu[None,:,None]));M=plain['M'];K=.03;W=-1/np.sqrt(2*np.pi)
 assert abs(M-1)<1e-9 and abs(plain['K']-K)<2e-6 and abs(plain['W_self']-W)<.001
 assert abs(boost['Pz']-.12)<2e-6 and abs(boost['K']-(K+.0072))<3e-6 and abs(boost['K_bulk_rest_diagnostic']-K)<3e-6
 for a,b in [(.75,1),(1,2),(2,4)]:
  v=window(s,u,a,b);assert np.max(abs(v[s.r>=b]))==0;cut=measure(s,v);assert 0<cut['M']<=M+1e-14;assert abs(cut['Pz'])<1e-12
 rows.append(dict(ne=ne,plain=plain,boost=boost,analytic_K=K,analytic_W=W))
print(json.dumps(rows,indent=2))
