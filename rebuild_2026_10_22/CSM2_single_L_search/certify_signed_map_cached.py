import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import argparse,hashlib,json,sys
import numpy as np
from mpmath import iv
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(HERE));from projection_operator import operator
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
files=[Path(__file__),HERE/'SIGNED_DOT_CRITERIA.md',HERE/'projection_operator.py',HERE/'mass_enclosure_001/outward_mass_vectors.npz',HERE/'mass_enclosure_001/results.json',HERE/'native_matrix_001/native_matrices.npz',HERE/'interval_001/results.json',HERE/'interval_001/score_boxes.npz',HERE.parent/'CSM1_consistent_core_switch/calibration/run_003_audited/results.json'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={str(p.relative_to(ROOT)):sha(p) for p in files};iv.dps=50
mass=np.load(files[3]);mass_lower=mass['lower'];mass_upper=mass['upper'];assert all(json.loads(files[4].read_text())['checks'].values());nat=np.load(files[5]);info=json.loads(files[6].read_text());prof=json.loads(files[8].read_text())['levels']['3.75']['lens']['result']['canonical']['profiles'];weights=nat['weights'];Q=nat['P']@nat['W'];R=nat['R'];rg=mass['radius_pc'];nodes=mass['node_indices'];base=np.array(prof['H']).ravel();y=np.array(prof['data']).ravel();LD=np.longdouble;finfo=np.finfo(LD)
assert finfo.nmant>=52 and finfo.tiny<LD(2)**-1000;u=iv.mpf(2)**-50;eta=iv.mpf(2)**-1000;checks={};dot_count=0;conversion=True

def cast(q):
 global conversion
 l=float(np.nextafter(float(q.a),-np.inf));h=float(np.nextafter(float(q.b),np.inf));conversion &= bool(iv.mpf(l)<=q.a and iv.mpf(h)>=q.b);assert np.isfinite([l,h]).all();return l,h

def dot(a,x):
 global dot_count
 a=np.asarray(a,LD);x=np.asarray(x,LD);products=a*x;assert np.isfinite(products).all();nz=abs(products[products!=0]);assert len(nz)==0 or np.min(nz)>finfo.tiny
 s=np.einsum('i->',products,optimize=False,dtype=LD);v=np.einsum('i->',abs(products),optimize=False,dtype=LD);n=len(a);assert np.isfinite([s,v]).all()
 sl=np.nextafter(float(s),-np.inf);sh=np.nextafter(float(s),np.inf);vh=np.nextafter(float(v),np.inf);assert LD(sl)<=s<=LD(sh) and LD(vh)>=v
 g=2*n*u/(1-2*n*u);norm=(iv.mpf(float(vh))+2*n*eta)/(1-g);err=g*norm+2*n*eta;dot_count+=1
 return iv.mpf([float(sl),float(sh)])+iv.mpf([-1,1])*err

def check(k,v):checks[k]=bool(v)
q=dot(np.array([1.,-1.,2.]),np.array([3.,3.,.5]));check('exact_dot_control',q.a<=1 and q.b>=1);check('mutation_detected',not(q.a<=1.01 and q.b>=1.01))
# IEEE subtraction + outward one-ulp guard. The saved operands are finite.
dl=np.nextafter(mass_lower[::2]-mass_upper[::2],-np.inf);du=np.nextafter(mass_upper[1::2]-mass_lower[::2],np.inf);assert dl.shape==(62,3601) and np.isfinite(dl).all() and np.isfinite(du).all();check('delta_order',np.all(dl<=du))
# Verify the subtraction bounds against directed interval arithmetic at every coordinate.
for j in range(62):
 for k in range(3601):
  lo=iv.mpf(float(mass_lower[2*j,k]))-iv.mpf(float(mass_upper[2*j,k]));hi=iv.mpf(float(mass_upper[2*j+1,k]))-iv.mpf(float(mass_lower[2*j,k]));assert iv.mpf(float(dl[j,k]))<=lo.a and iv.mpf(float(du[j,k]))>=hi.b
A=np.array([operator(R[b]*1e6,rg,np.linspace(0,12,2401),'const') for b in range(4)]);assert A.shape==(4,15,3601) and np.isfinite(A).all();pbound=np.empty((62,4,15,2));dstack=[iv.mpf(0) for _ in range(60)];visited=0
for j,node in enumerate(nodes):
 for b in range(4):
  for k in range(15):
   c=A[b,k];lower=np.where(c>=0,dl[j],du[j]);upper=np.where(c>=0,du[j],dl[j]);l=dot(c,lower);h=dot(c,upper);q=iv.mpf([l.a,h.b]);pbound[j,b,k]=cast(q);dstack[15*b+k]+=iv.mpf(float(weights[b,node]))*q;visited+=2
rbox=[]
for i in range(60):
 total=iv.mpf(0)
 for j in range(60):total+=iv.mpf(float(Q[i,j]))*(iv.mpf(float(y[j]))-iv.mpf(float(base[j]))-dstack[j])
 rbox.append(total)
score=iv.mpf(0)
for q in rbox:
 if q.a>0:score+=q.a**2
 elif q.b<0:score+=q.b**2
lower_score=cast(score)[0];resbounds=np.array([cast(q) for q in rbox]);sample=np.load(files[7])['source_profiles'];sample_ok=True
for model in sample:
 for i in range(60):
  v=iv.mpf(0)
  for j in range(60):v+=iv.mpf(float(Q[i,j]))*(iv.mpf(float(y[j]))-iv.mpf(float(model.ravel()[j])))
  sample_ok &= bool(rbox[i].a<=v.a and rbox[i].b>=v.b)
check('coverage',visited==62*4*15*2);check('outward_casts',conversion);check('source_samples_contained',sample_ok);check('finite_outputs',np.isfinite(pbound).all() and np.isfinite(resbounds).all() and np.isfinite(lower_score));check('inputs_stable',all(sha(ROOT/f)==h for f,h in hashes.items()))
np.savez_compressed(out/'signed_map_evidence.npz',A=A,Q=Q,weights=weights,node_indices=nodes,delta_lower=dl,delta_upper=du,projected_bounds=pbound,residual_bounds=resbounds,base=base,data=y)
result=dict(checks=checks,lower_score_fixed_map=lower_score,score_interval=str(score),dot_calls=dot_count,projection_bound_visits=visited,longdouble=dict(nmant=finfo.nmant,eps=str(finfo.eps),tiny=str(finfo.tiny)),input_sha256=hashes,full_model_interval_certified=False,scope='Anchored fixed binary64 coefficient map only, conditional on continuum mass-box coverage; not an original-likelihood certificate',remaining_obligations=['Column/branch/continuum mass-box coverage','Projection coefficient-construction bounds','Nuisance/whitening coefficient relation to original covariance and constrained score'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,lower_score_fixed_map=lower_score,dot_calls=dot_count),indent=2));raise SystemExit(0 if all(checks.values()) else 1)
