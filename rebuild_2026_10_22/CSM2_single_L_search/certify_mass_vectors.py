import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import argparse,hashlib,json,math,time
import numpy as np
from mpmath import iv
import mpmath
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
paths=[Path(__file__),HERE/'MASS_ENCLOSURE_CRITERIA.md',HERE/'interval_001/results.json',HERE/'root_sign_001/results.json',HERE/'native_matrix_001/native_matrices.npz',HERE/'interval_local.py'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={str(p.relative_to(ROOT)):sha(p) for p in paths};d=json.loads(paths[2].read_text());root=json.loads(paths[3].read_text());assert root['certified_scalar_root_brackets']==124 and all(root['checks'].values())
# Source radius/log-mass construction is pinned by interval_local.py and native grid.
rg=np.logspace(1.,10.,3601);lmgrid=np.load(paths[4])['LMG'];nodes=[n for n in d['nodes'] if n['halo']];assert len(nodes)==62
iv.dps=50
B=lambda x:iv.log(1+x*x)+2*iv.log(1+x)-2*iv.atan2(x,iv.mpf(1))
Bn=lambda x:np.log1p(x*x)+2*np.log1p(x)-2*np.arctan(x)
low=np.empty((124,3601));high=np.empty_like(low);rows=[];failures=[];converted=True;root_ok=True;mutation=False;t0=time.monotonic();coef=[]
for ni,node in enumerate(nodes):
 lm=lmgrid[node['i']];Ms=float(10**lm);Mc=float(10**(lm+(-.69*(lm-2*np.log10(.70/.679))+6.63)));coef.append(dict(node=node['i'],Ms=Ms,Mc=Mc))
 # Fixed binary64 coefficients; the continuous radius expression is evaluated outward.
 ms,mc=iv.mpf(Ms),iv.mpf(Mc);hot=ms/2;rh=iv.mpf(100000)
 bary=[]
 for r in rg:
  q=iv.mpf(float(r))/rh;v=q**3
  bary.append(ms+mc+hot*(iv.mpf(1) if r>=100000 else v))
 for endpoint in (0,1):
  j=2*ni+endpoint;b=d['root_brackets'][j];assert b['M']==node['M'];M,R,S=[iv.mpf(b[k]) for k in ('M','R','Sigma')];rl,rh0=[iv.mpf(b[k]) for k in ('r0_lower','r0_upper')]
  root_ok &= bool((iv.pi*S*rl**2*B(R/rl)-M).b<0 and (iv.pi*S*rh0**2*B(R/rh0)-M).a>0)
  factorlo=iv.pi*S*rl**2;factorhi=iv.pi*S*rh0**2
  rr=np.minimum(rg,b['R']);mb=Ms+Mc+.5*Ms*np.minimum(1.,(rg/100000)**3);cl=mb+np.pi*b['Sigma']*b['r0_lower']**2*Bn(rr/b['r0_upper']);cu=mb+np.pi*b['Sigma']*b['r0_upper']**2*Bn(rr/b['r0_lower']);pad=1e-8*np.maximum(abs(cl),abs(cu))+1e-6;cl-=pad;cu+=pad
  misses=0
  for k,r in enumerate(rr):
   tt=iv.mpf(float(r));l=bary[k]+factorlo*B(tt/rh0);u=bary[k]+factorhi*B(tt/rl)
   a0=float(np.nextafter(float(l.a),-np.inf));a1=float(np.nextafter(float(u.b),np.inf));low[j,k]=a0;high[j,k]=a1
   converted &= bool(iv.mpf(a0)<=l.a and iv.mpf(a1)>=u.b)
   if not(iv.mpf(float(cl[k]))<=l.a and iv.mpf(float(cu[k]))>=u.b):
    misses+=1
    if len(failures)<20:failures.append(dict(bracket=j,radius_index=k))
   if j==0 and not(iv.mpf(float(cl[k]*1.01))<=l.a and iv.mpf(float(cu[k]*1.01))>=u.b):mutation=True
  rows.append(dict(bracket=j,node=node['i'],endpoint=endpoint,padding_misses=misses))
 if ni%10==0:print(json.dumps(dict(nodes_complete=ni+1,seconds=time.monotonic()-t0)),flush=True)
checks=dict(coverage=low.shape==(124,3601) and len(rows)==124,roots_revalidated=bool(root_ok),finite=bool(np.isfinite(low).all() and np.isfinite(high).all()),ordered_nonnegative=bool(np.all(low>=0) and np.all(low<=high)),outward_conversion=bool(converted),registered_padding_contains_all=all(x['padding_misses']==0 for x in rows),mutation_detected=bool(mutation),B_zero=bool(B(iv.mpf(0))==0),inputs_stable=all(sha(ROOT/p)==h for p,h in hashes.items()))
np.savez_compressed(out/'outward_mass_vectors.npz',lower=low,upper=high,radius_pc=rg,node_indices=np.array([n['i'] for n in nodes]),stellar_mass=np.array([x['Ms'] for x in coef]),cold_mass=np.array([x['Mc'] for x in coef]))
result=dict(checks=checks,rows=rows,failures_first20=failures,input_sha256=hashes,coefficients=coef,backend=dict(mpmath=mpmath.__version__,interval_decimal_digits=50),mass_coordinates=124*3601,runtime_seconds=time.monotonic()-t0,fixed_coefficient_mass_vectors_certified=bool(checks['outward_conversion'] and checks['roots_revalidated'] and checks['finite'] and checks['coverage']),full_model_interval_certified=False,scope='Directed endpoint mass vectors for fixed saved coefficients only; no certified continuous-L score',remaining_obligations=['Column/branch/continuum coefficient enclosures','Projection/stacking/whitening coefficient bounds','Signed-dot/final score rounding bounds'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,mass_coordinates=result['mass_coordinates'],runtime_seconds=result['runtime_seconds']),indent=2));raise SystemExit(0 if all(checks.values()) else 1)
