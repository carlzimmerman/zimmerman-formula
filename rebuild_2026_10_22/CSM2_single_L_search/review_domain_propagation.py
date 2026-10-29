"""Exhaustive exact-rational domain majorant checks and unchanged dual review."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,resource,signal,sys,time
import numpy as np
import mpmath as mp
resource.setrlimit(resource.RLIMIT_CPU,(120,120));signal.alarm(150);sys.set_int_max_str_digits(100000)
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'domain_propagation_001';paths=[Path(__file__),run/'results.json',run/'domain_extension.npz',p/'nonlinear_001/original_input_mass_vectors.npz',p/'mass_enclosure_001/outward_mass_vectors.npz',p/'signed_dot_002_cached/signed_map_evidence.npz',p/'projection_anchor_001/projection_primitive_enclosures.npz',p/'source_forward_001/forward_error_evidence.npz',p/'source_forward_review.json',p/'catalogue_001/results.json',p/'projection_dual_inflation.json',p/'exact_dual_001/certificate.json',p/'native_matrix_001/native_matrices.npz'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in paths};load=lambda i:dict(np.load(paths[i]));read=lambda i:json.loads(paths[i].read_text());d=read(1);ext=load(2);new=load(3);old=load(4);signed=load(5);proj=load(6);fw=load(7);src=read(8);cat=read(9);prior=read(10);c=read(11);nat=load(12);eps=F(float(d['epsilon']));lam=F(float(d['lambda_envelope']));needed_eps=F(0);needed_lam=F(1);halo_count=0;law_count=0;checks={};t0=time.monotonic()
for j in range(62):
 for k in range(3601):
  den=F(float(old['upper'][2*j+1,k]));lo=F(float(new['lower'][2*j,k]))-F(float(old['upper'][2*j,k]));hi=F(float(new['upper'][2*j+1,k]))-F(float(old['lower'][2*j,k]));need=max(F(0),F(float(signed['delta_lower'][j,k]))-lo,hi-F(float(signed['delta_upper'][j,k])))/den;needed_eps=max(needed_eps,need);needed_lam=max(needed_lam,F(float(new['upper'][2*j+1,k]))/den);assert F(float(ext['halo_delta_lower'][j,k]))<=lo and F(float(ext['halo_delta_upper'][j,k]))>=hi;halo_count+=1
lookup={int(node):j for j,node in enumerate(proj['node_indices'])}
for j,node in enumerate(ext['law_nodes']):
 for k in range(3601):
  saved=F(float(proj['node_mass'][lookup[int(node)],k]));lo=F(float(ext['law_lower'][j,k]));hi=F(float(ext['law_upper'][j,k]));needed_eps=max(needed_eps,abs(lo-saved)/saved,abs(hi-saved)/saved);needed_lam=max(needed_lam,hi/saved);law_count+=1
# Enclose the saved outward arrays too. This may strengthen a main budget that
# directly bounded the higher-precision analytic interval before float export.
eps=max(eps,needed_eps);lam=max(lam,needed_lam);checks['all223262_halo_coordinates']=halo_count==223262;checks['all234065_law_coordinates']=law_count==234065;checks['exact_positive_majorants']=eps>=needed_eps and lam>=needed_lam and eps>=0 and lam>=1;mp.mp.dps=70;law_tests=0;M=lambda v:mp.mpf(float(v));G=M(4.30091e-3);a0=M(9.3603e-11)*M(3.0857e16)/M(1e6)
for j,node in enumerate(ext['law_nodes']):
 lm=M(nat['LMG'][node]);ms=mp.power(10,lm);mc=mp.power(10,lm+M(-.69)*(lm-2*mp.log10(M(.70)/M(.679)))+M(6.63))
 for k in [0,900,1800,2700,3600]:
  rad=M(ext['radius_pc'][k]);mb=ms+mc+ms/2*min(1,(rad/M(1e5))**3);law=mb/2+mp.sqrt(mb**2/4+mb*a0*rad**2/G);assert M(ext['law_lower'][j,k])<=law<=M(ext['law_upper'][j,k]);law_tests+=1
checks['325_independent_law_tests']=law_tests==325;checks['finite_arrays']=all(np.isfinite(ext[k]).all() for k in ext);aa=list(map(F,c['a']));extras=[];boxes=[]
for i in range(60):
 b,k=divmod(i,15);U=sum((F(float(fw['path_U'][tail,b,k])) for tail in range(2)),F(0));ee=F(prior['exact_inflation'][i])+eps*U+lam*(F(src['exact_review_error_bounds'][i])+F(cat['exact_stack_error'][i]));extras.append(ee);lo,hi=map(F,c['native_residual_boxes'][i]);boxes.append((lo-ee,hi+ee))
nl=sum((min(a*lo,a*hi) for a,(lo,hi) in zip(aa,boxes)),F(0));nh=sum((max(a*lo,a*hi) for a,(lo,hi) in zip(aa,boxes)),F(0));bound=max(nl,-nh,F(0))**2/F(c['denominator']);checks['conservative_vs_main']=all(v>=F(old) for v,old in zip(extras,d['exact_extra']));checks['margin']=bound>F(c['law_candidate_upper'])+9;checks['original_controls']=all(d['checks'].values());checks['input_hashes']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,exact_review_epsilon=str(eps),exact_review_lambda=str(lam),main_epsilon_covers_exported_arrays=F(float(d['epsilon']))>=needed_eps,main_lambda_covers_exported_arrays=F(float(d['lambda_envelope']))>=needed_lam,exact_review_extra=list(map(str,extras)),exact_review_dual_lower=str(bound),review_dual_lower=float(bound),law_tests=law_tests,halo_coordinates=halo_count,law_coordinates=law_count,runtime_seconds=time.monotonic()-t0,input_sha256=hashes,full_model_interval_certified=False,scope='Exact exhaustive bound on exported analytic-domain arrays, independent law review and unchanged rational dual; floating solver/libm continuum unresolved');(p/'domain_propagation_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'eps',float(eps),'lambda',float(lam),'lower',float(bound));assert all(checks.values())
