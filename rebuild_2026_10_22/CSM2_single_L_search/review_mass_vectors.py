"""Independent80-digit root refinement and normalized-mass checks at4radii/bracket.
Criteria frozen in this source before execution:124brackets, radius indices
0,1200,2400,3600, relative root width<=1e-30, all496normalized interval profiles
contained in saved outward boxes. Failure/inconclusive refinements are retained.
This reviews endpoint mass vectors, not a continuous-L score.
"""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import hashlib,json,math
import numpy as np
from mpmath import iv,mp
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'mass_enclosure_001';files=[Path(__file__),run/'results.json',run/'outward_mass_vectors.npz',p/'interval_001/results.json'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};d=json.loads(files[1].read_text());old=json.loads(files[3].read_text());z=np.load(files[2]);iv.dps=80;mp.dps=80
B=lambda x:iv.log((1+x*x)*(1+x)**2)-2*iv.atan2(x,iv.mpf(1));checks={};records=[];cases=0
for j,b in enumerate(old['root_brackets']):
 M,R,S=[iv.mpf(b[k]) for k in ('M','R','Sigma')];lo,hi=[mp.mpf(b[k]) for k in ('r0_lower','r0_upper')];decided=True
 while hi-lo>mp.mpf('1e-30')*lo:
  mid=(lo+hi)/2;v=iv.mpf(mid);f=iv.pi*S*v*v*B(R/v)-M
  if f.b<0:lo=mid
  elif f.a>0:hi=mid
  else:decided=False;break
 rr=iv.mpf([lo,hi]);ms=iv.mpf(float(z['stellar_mass'][j//2]));mc=iv.mpf(float(z['cold_mass'][j//2]));ok=decided
 for k in (0,1200,2400,3600):
  rv=float(z['radius_pc'][k]);t=iv.mpf(rv);mb=ms+mc+ms/2*(iv.mpf(1) if rv>=100000 else (t/100000)**3)
  mh=M if rv>=b['R'] else M*B(t/rr)/B(R/rr);mass=mb+mh;ok &= bool(iv.mpf(float(z['lower'][j,k]))<=mass.a and iv.mpf(float(z['upper'][j,k]))>=mass.b);assert all(math.isfinite(float(v)) for v in (mass.a,mass.b));cases+=1
 checks[str(j)]=bool(ok);records.append(dict(bracket=j,refinement_decided=decided,checks_pass=bool(ok)))
checks['coverage']=cases==496 and len(records)==124;checks['original_controls']=all(d['checks'].values());checks['inputs_stable']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,records=records,cases=cases,input_sha256=hashes,review='Self/adversarial interval review using refined root and normalized compact mass; selected radii review only, original directed coverage is all446524coordinates',full_model_interval_certified=False)
(p/'mass_enclosure_review.json').write_text(json.dumps(result,indent=2)+'\n');print('reviewchecks',len(checks),'cases',cases,'all_pass',all(checks.values()));assert all(checks.values())
