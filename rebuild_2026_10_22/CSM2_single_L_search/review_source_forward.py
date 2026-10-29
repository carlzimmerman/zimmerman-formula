"""Exact-rational error-budget recomposition from saved upper path majorants.
Use max(main bound, independently recomposed bound) per coordinate, then
reconstruct the unchanged covariance dual exactly. No physical parameter fit.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys
import numpy as np
sys.set_int_max_str_digits(100000)
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'source_forward_001';files=[Path(__file__),run/'results.json',run/'forward_error_evidence.npz',p/'projection_anchor_001/projection_primitive_enclosures.npz',p/'native_matrix_001/native_matrices.npz',p/'projection_dual_inflation.json',p/'exact_dual_001/certificate.json'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};d=json.loads(files[1].read_text());z=np.load(files[2]);proj=np.load(files[3]);nat=np.load(files[4]);prior=json.loads(files[5].read_text());c=json.loads(files[6].read_text());N=d['N'];u=F(1,2**50);eta=F(1,2**1022);gamma=N*u/(1-N*u);glo,ghi=[F(v.strip()) for v in d['gamma'].strip('[]').split(',')];checks={};checks['gamma_interval']=glo<=gamma<=ghi;checks['syntactic_count']=N==2*len(proj['weight'])+128;nodes=proj['node_indices'];flags=proj['node_halo'];weights=nat['weights'];W=[[F(0) for _ in range(4)] for _ in range(2)]
for j,node in enumerate(nodes):
 for b in range(4):W[0 if flags[j] else 1][b]+=F(float(weights[b,node]))
U=z['path_U'];V=z['path_V'];E=z['native_errors'];chosen=[];relative_gap=0.
for i in range(60):
 b,k=divmod(i,15);ee=sum((gamma*F(float(U[t,b,k]))+eta*W[t][b]*F(float(V[t,b,k]))/(1-N*u) for t in range(2)),F(0));raw=F(float(E[b,k]));chosen.append(max(raw,ee));relative_gap=max(relative_gap,float(abs(raw-ee)/max(raw,ee,F(1,2**1000))))
checks['positive_derived_errors']=all(v>=0 for v in chosen);checks['recorded_budget_diagnostic']=relative_gap<1e-12;aa=list(map(F,c['a']));boxes=[]
for i in range(60):
 lo,hi=map(F,c['native_residual_boxes'][i]);extra=F(prior['exact_inflation'][i])+chosen[i];boxes.append((lo-extra,hi+extra))
nl=sum((min(aa[i]*boxes[i][0],aa[i]*boxes[i][1]) for i in range(60)),F(0));nh=sum((max(aa[i]*boxes[i][0],aa[i]*boxes[i][1]) for i in range(60)),F(0));dist=max(nl,-nh,F(0));bound=dist**2/F(c['denominator']);law=F(c['law_candidate_upper']);checks['lower_consistency']=abs(float(bound)-d['dual_lower_after_error'])<1e-8;checks['exact_margin']=bound>law+9;checks['original_controls']=all(d['checks'].values());checks['inputs_stable']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,exact_review_error_bounds=list(map(str,chosen)),max_relative_budget_difference=relative_gap,exact_review_dual_lower=str(bound),review_dual_lower=float(bound),input_sha256=hashes,scope='Exact error-budget/dual arithmetic under reviewed source-operation model; not independent binary authentication or mass/continuum certificate')
(p/'source_forward_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),'allpass',all(checks.values()),'lower',float(bound),'budgetgap',relative_gap);assert all(checks.values())
