"""Frozen catalogue numerical map: exact ideal weights and conservative error."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,sys,time
import numpy as np
from mpmath import iv
sys.set_int_max_str_digits(100000);iv.dps=50
a=argparse.ArgumentParser();a.add_argument('--output',required=True);out=Path(a.parse_args().output);out.mkdir(parents=True,exist_ok=True)
p=Path(__file__).resolve().parent;r=p.parents[1];data=r/'real_research/data/lensing_rar';t0=time.monotonic()
files=[Path(__file__),p/'CATALOGUE_ERROR_CRITERIA.md',p/'catalogue_error_contract.json',p/'native_matrix.py',p/'native_matrix_001/native_matrices.npz',p/'projection_anchor_001/projection_primitive_enclosures.npz',p/'mass_enclosure_001/outward_mass_vectors.npz',p/'source_forward_001/forward_error_evidence.npz',p/'source_forward_review.json',p/'projection_dual_inflation.json',p/'exact_dual_001/certificate.json',data/'lr_lenses.npz',data/'cfg110_perlens.npz',p/'source_audit_numpy_1_26_4/compiled_base.c',p.parent/'F2_outer_lensing/f2_outer_lensing.py']
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};checks={};ck=lambda k,v:checks.update({k:bool(v)})
load=lambda f:{k:v for k,v in np.load(f).items()}
nat=load(files[4]);proj=load(files[5]);mass=load(files[6]);fw=load(files[7]);ln=load(files[11]);pl=load(files[12]);grid=nat['LMG'];weights=nat['weights'];lm=ln['logM'];z=ln['z'];w=pl['WW'].sum(axis=1);bins=np.digitize(lm,[8.5,10.3,10.6,10.8,11.0001])-1

def ch(z,om):
 zz=np.linspace(0,1,4001);e=np.sqrt(om*(1+zz)**3+1-om);return np.interp(z,zz,np.r_[0,np.cumsum(.5*(1/e[1:]+1/e[:-1])*np.diff(zz))])
q=ch(z,.3085)/ch(z,.3);h=.679;lookup={int(n):j for j,n in enumerate(mass['node_indices'])};profiles=[]
for j,node in enumerate(proj['node_indices']):profiles.append(mass['upper'][2*lookup[int(node)]+1] if proj['node_halo'][j] else proj['node_mass'][j])
profiles=np.asarray(profiles);ck('mass_premise',np.isfinite(profiles).all() and np.all(profiles>=0));u=F(1,2**50);eta=F(1,2**1022);records=[];ideal_all=[];bounds=[];tables=[];stress=[];mutation=False
# Interval coefficient magnitudes and pointwise maximum profiles bound every
# active ideal table ordinate, with no cancellation assumption.
for b in range(4):
 sel=bins==b;ww=w[sel];x=lm[sel]+2*np.log10(.70/h)+2*np.log10(q[sel]);ids=np.clip(np.searchsorted(grid,x,side='right')-1,0,len(grid)-2);alpha=np.clip((x-grid[ids])/(grid[ids+1]-grid[ids]),0,1);actual=np.zeros(len(grid));np.add.at(actual,ids,ww*(1-alpha)/ww.sum());np.add.at(actual,ids+1,ww*alpha/ww.sum());ck(f'weights_reproduce_{b}',np.array_equal(actual,weights[b]));ck(f'positive_normal_{b}',np.isfinite(ww).all() and np.all(ww>np.finfo(float).tiny) and np.isfinite(x).all())
 exact=[F(0) for _ in grid];W=sum(map(lambda v:F(float(v)),ww),F(0));sterbenz=True
 for xx,j,v in zip(x,ids,ww):
  xx=F(float(xx));g0=F(float(grid[j]));g1=F(float(grid[j+1]));a=max(F(0),min(F(1),(xx-g0)/(g1-g0)));vv=F(float(v));exact[j]+=vv*(1-a);exact[j+1]+=vv*a
  sterbenz &= F(float(grid[j+1]-grid[j]))==g1-g0
  if g0<xx<g1:sterbenz &= F(float(float(xx)-grid[j]))==xx-g0
 exact=[e/W for e in exact];ideal_all.append(list(map(str,exact)));disc=sum((abs(v-F(float(a))) for v,a in zip(exact,actual)),F(0));ck(f'ideal_probability_{b}',sum(exact)==1 and all(e>=0 for e in exact));ck(f'support_{b}',all((v>0)==(a>0) for v,a in zip(exact,actual)));ck(f'Sterbenz_{b}',sterbenz)
 active=weights[b,proj['node_indices']]>0;vmax=profiles[active].max(axis=0);minw=min(F(float(v)) for v in weights[b] if v>0);B=[]
 for row in range(15):
  upper=iv.mpf(0)
  for tail in range(2):
   coeff=np.maximum(abs(proj['lower'][tail,b,row]),abs(proj['upper'][tail,b,row]));v=sum((iv.mpf(float(c))*iv.mpf(float(m)) for c,m in zip(coeff,vmax)),iv.mpf(0));upper=max(upper,v.b)
  # Sum of group bounds dominates each individual error times its positive weight.
  ee=sum(map(F,[json.loads(files[8].read_text())['exact_review_error_bounds'][b*15+row]]),F(0))/minw
  bf=F(float(np.nextafter(float(upper.b),np.inf)))+ee;B.append(bf)
 n=len(ww);N=2*n+32;gamma=N*u/(1-N*u);step=min(F(float(grid[j+1]))-F(float(grid[j])) for j in range(len(grid)-1));errs=[]
 for bf in B:
  rounding=3*bf*gamma/(1-gamma)+eta*(2*N+32)*(1+bf)*(1+W+1/W)**2*(1+1/step)/(1-gamma);errs.append(rounding+bf*disc)
 bounds.extend(errs);tables.append(list(map(str,B)));ck(f'no_overflow_{b}',max(B)*max(W,F(1))/step<F(2)**1000 and W>F(2)**-900 and step>F(2)**-900)
 for label,tab in [('constant',np.ones(len(grid))),('alternating',np.where(np.arange(len(grid))%2,1.,-1.)),('smooth',np.sin(grid))]:
  got=np.interp(x,grid,tab)@ww/ww.sum();ideal=sum((e*F(float(t)) for e,t in zip(exact,tab)),F(0));old=sum((F(float(e))*F(float(t)) for e,t in zip(actual,tab)),F(0));error=abs(F(float(got))-old);testbound=3*gamma/(1-gamma)+disc+eta*(2*N+32)*2*(1+W+1/W)**2*(1+1/step)/(1-gamma);stress.append(error<=testbound)
  if label=='constant':mutation |= abs(F(float(got*1.01))-old)>testbound
 records.append(dict(bin=b,n=n,N=N,exact_weight_L1_error=str(disc),sum_w=str(W),min_positive_weight=str(minw),max_table_bound=float(max(B)),max_stack_error=float(max(errs)),gamma=str(gamma)))
 print('bin',b,'n',n,'max table',float(max(B)),'error',float(max(errs)),flush=True)
ck('stress_cases',len(stress)==12 and all(stress));ck('mutation_detected',mutation);ck('finite_outputs',np.isfinite([float(v) for v in bounds]).all());c=json.loads(files[10].read_text());prior=json.loads(files[9].read_text());src=json.loads(files[8].read_text());aa=list(map(F,c['a']));boxes=[]
for i in range(60):
 lo,hi=map(F,c['native_residual_boxes'][i]);extra=F(prior['exact_inflation'][i])+F(src['exact_review_error_bounds'][i])+bounds[i];boxes.append((lo-extra,hi+extra))
nl=sum((min(aa[i]*v[0],aa[i]*v[1]) for i,v in enumerate(boxes)),F(0));nh=sum((max(aa[i]*v[0],aa[i]*v[1]) for i,v in enumerate(boxes)),F(0));lower=max(nl,-nh,F(0))**2/F(c['denominator']);ck('inputs_stable',all(sha(r/f)==v for f,v in hashes.items()))
result=dict(checks=checks,records=records,ideal_weights=ideal_all,table_bounds=tables,exact_stack_error=list(map(str,bounds)),conditional_dual_lower=float(lower),exact_dual_lower=str(lower),law_upper=float(F(c['law_candidate_upper'])),conditional_margin=lower>F(c['law_candidate_upper'])+9,stress_cases=len(stress),runtime_seconds=time.monotonic()-t0,input_sha256=hashes,full_model_interval_certified=False,scope='Reviewed floating implementation and fixed catalogue inputs; covered table/mass domain remains conditional, not real-L exclusion')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'lower',float(lower));assert all(checks.values())
