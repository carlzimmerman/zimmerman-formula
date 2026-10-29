import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,sys,time
import numpy as np
from mpmath import iv
sys.set_int_max_str_digits(100000);iv.dps=50;p=Path(__file__).resolve().parent;r=p.parents[1];ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);out.mkdir(parents=True,exist_ok=True);t0=time.monotonic()
paths=[Path(__file__),p/'COMPARATOR_001_CRITERIA.md',p/'comparator_contract.json',p.parent/'F2_outer_lensing/f2_outer_lensing.py',p/'projection_anchor_001/x53_on_shpS9_L3.75_corrected_own/x62_x53copy_1.executed.py',p/'projection_anchor_001/projection_primitive_enclosures.npz',p/'catalogue_001/results.json',p/'native_matrix_001/native_matrices.npz',p/'exact_dual_001/certificate.json',p.parent/'CSM1_consistent_core_switch/calibration/run_003_audited/results.json',p/'domain_propagation_review.json'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in paths};read=lambda i:json.loads(paths[i].read_text());proj=dict(np.load(paths[5]));cat=read(6);nat=dict(np.load(paths[7]));cert=read(8);foot=read(9)['levels']['3.75']['lens']['result']['canonical'];prof=foot['profiles'];grid=nat['LMG'];nodes=np.flatnonzero(np.any(nat['weights']>0,axis=0));rg=proj['radius'];weights=[[F(v) for v in row] for row in cat['ideal_weights']];checks={};ck=lambda k,v:checks.update({k:bool(v)});J=lambda v:iv.mpf(float(v));Q=lambda v:iv.mpf(v.numerator)/iv.mpf(v.denominator);conversion=True

def cast(v):
 global conversion
 lo=float(np.nextafter(float(v.a),-np.inf));hi=float(np.nextafter(float(v.b),np.inf));assert np.isfinite([lo,hi]).all();conversion &= bool(J(lo)<=v.a and J(hi)>=v.b);return lo,hi

f2=paths[3].read_text();x53=paths[4].read_text();ck('source_scope_guards',all(v in f2 for v in ['logMcold=lmc','cfg["fhot"] * 10 ** (-cfg["dMs"])','Miso = Mb * AQ.nu_simple(Gpc * Mb / RGRID_PC ** 2 / a0)','return Miso, "linear"']) and 'dMs=0.0, dcold=0.0, fhot=0.5, ye="zero"' in x53);ck('positive_inventory',len(nodes)==127 and all(sum(row)==1 and all(v>=0 for v in row) for row in weights));low=np.empty((127,len(rg)));high=np.empty_like(low);aggregate=[[iv.mpf(0) for _ in rg] for _ in range(4)];source_stack=np.zeros((4,15));wrong_tail=np.zeros((4,15));A=proj['binary_coefficients'];a0=J(9.3603e-11)*J(3.0857e16)/J(1e6);offset=2*iv.log(J(.70)/J(.679))/iv.log(10)
for j,node in enumerate(nodes):
 lm=J(grid[node]);ms=iv.exp(lm*iv.log(10));mc=iv.exp((lm+J(-.69)*(lm-offset)+J(6.63))*iv.log(10));current=[]
 for k,rad in enumerate(rg):
  rr=J(rad);mb=ms+mc+ms/2*(iv.mpf(1) if rad>=1e5 else (rr/J(1e5))**3);y=J(4.30091e-3)*mb/rr**2/a0;v=mb*(iv.mpf('.5')+iv.sqrt(iv.mpf('.25')+1/y));lo,hi=cast(v);low[j,k],high[j,k]=lo,hi;current.append(iv.mpf([lo,hi]))
 for b in range(4):
  w=weights[b][node]
  if not w:continue
  wi=Q(w)
  for k,v in enumerate(current):aggregate[b][k]+=wi*v
 # Diagnostic only: inherited binary64 source mass and saved float operator.
 lmf=grid[node];Ms=10**lmf;Mc=10**(lmf+(-.69*(lmf-2*np.log10(.70/.679))+6.63));Mb=Ms+Mc+.5*Ms*np.minimum(1.,(rg/1e5)**3);mf=Mb*(.5+np.sqrt(.25+1/(4.30091e-3*Mb/rg**2/(9.3603e-11*3.0857e16/1e6))))
 for b in range(4):
  if nat['weights'][b,node]==0:continue
  source_stack[b]+=nat['weights'][b,node]*np.einsum('ij,j->i',A[1,b],mf,optimize=False);wrong_tail[b]+=nat['weights'][b,node]*np.einsum('ij,j->i',A[0,b],mf,optimize=False)
agglo=np.empty((4,len(rg)));agghi=np.empty_like(agglo)
for b in range(4):
 for k,v in enumerate(aggregate[b]):agglo[b,k],agghi[b,k]=cast(v)
coefflo=proj['lower'][1];coeffhi=proj['upper'][1];native=np.empty((60,2))
for b in range(4):
 for row in range(15):
  v=sum((iv.mpf([float(coefflo[b,row,k]),float(coeffhi[b,row,k])])*iv.mpf([float(agglo[b,k]),float(agghi[b,k])]) for k in range(len(rg))),iv.mpf(0));native[15*b+row]=cast(v)
source=np.array(prof['L']);scale=float(np.max(abs(source)));relative=float(np.max(abs(source_stack-source))/scale);ck('source_reproduction',relative<1e-9);ck('mass_mutation',np.max(abs(source_stack*1.01-source))/scale>1e-9);ck('weight_mutation',np.max(abs(source_stack*1.01-source))/scale>1e-9);tailchange=float(np.max(abs(source_stack-wrong_tail)));ck('tail_mutation',not np.array_equal(A[0],A[1]) and tailchange>0);ck('finite_arrays',all(np.isfinite(a).all() for a in [low,high,agglo,agghi,native,source_stack,wrong_tail]) and np.all(low>0) and np.all(low<=high));ck('outward_casts',conversion)
L=[[F(v) for v in row] for row in cert['L']];D=list(map(F,cert['D']));bvec=list(map(F,cert['law_b']));T=[[F(float(v)) for v in row] for row in nat['T']];Y=list(map(lambda v:F(float(v)),np.array(prof['data']).ravel()));res=[]
for i in range(60):
 base=Y[i]-sum((T[i][j]*bvec[j] for j in range(4)),F(0));res.append((base-F(float(native[i,1])),base-F(float(native[i,0]))))
z=[]
for i,(lo,hi) in enumerate(res):
 for j in range(i):
  a,b=L[i][j]*z[j][0],L[i][j]*z[j][1];lo-=max(a,b);hi-=min(a,b)
 z.append((lo,hi))
upper=sum((max(abs(lo),abs(hi))**2/D[i] for i,(lo,hi) in enumerate(z)),F(0));hybrid=F(read(10)['exact_review_dual_lower']);ck('law_candidate_feasible',len(bvec)==4 and all(v>=0 for v in bvec));ck('positive_LDL',all(v>0 for v in D) and all(L[i][i]==1 for i in range(60)));ck('input_hashes',all(sha(r/f)==h for f,h in hashes.items()));delta=np.maximum(abs(native[:,0]-source.ravel()),abs(native[:,1]-source.ravel()));np.savez_compressed(out/'analytic_comparator.npz',mass_lower=low,mass_upper=high,node_indices=nodes,radius_pc=rg,aggregate_lower=agglo,aggregate_upper=agghi,native_bounds=native,source_reproduction=source_stack,wrong_tail=wrong_tail)
result=dict(checks=checks,mass_coordinates=low.size,native_coordinates=60,max_native_difference_from_recorded=float(delta.max()),source_stack_relative_error=relative,tail_mutation_native_change=tailchange,exact_residual_boxes=[[str(v) for v in pair] for pair in res],exact_triangular_boxes=[[str(v) for v in pair] for pair in z],exact_candidate_score_upper=str(upper),candidate_score_upper=float(upper),old_numerical_candidate_upper=float(F(cert['law_candidate_upper'])),reviewed_hybrid_lower=float(hybrid),exact_hybrid_lower=str(hybrid),common_scope_margin=hybrid>upper+9,runtime_seconds=time.monotonic()-t0,input_sha256=hashes,original_floating_evaluator_certified=False,global_L_exclusion=False,scope='Original-input analytic masses on registered fixed numerical projection/catalogue primitives and actual covariance; exact feasible comparator upper. Original floating solver/libm/continuum quadrature not certified.');(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'upper',float(upper),'hybrid',float(hybrid),'margin',hybrid>upper+9);assert all(checks.values())
