"""Reconstruct complete exact dual/LDL certificate without approximate Q."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
import numpy as np
sys.set_int_max_str_digits(100000)
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'exact_dual_001';files=[Path(__file__),run/'certificate.json',run/'results.json',p/'native_matrix_001/native_matrices.npz',p/'signed_dot_002_cached/signed_map_evidence.npz'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};c=json.loads(files[1].read_text());d=json.loads(files[2].read_text());nat=np.load(files[3]);ev=np.load(files[4]);C=[[F(float(x)) for x in row] for row in nat['C']];T=[[F(float(x)) for x in row] for row in nat['T']];L=[[F(x) for x in row] for row in c['L']];D=list(map(F,c['D']));aa=list(map(F,c['a']));checks={};n=60
checks['LDL_all3600entries']=all(sum((L[i][k]*D[k]*L[j][k] for k in range(n)),F(0))==C[i][j] for i in range(n) for j in range(n));checks['SPD_pivots']=all(x>0 for x in D);checks['lower_triangular']=all(L[i][i]==1 and all(L[i][j]==0 for j in range(i+1,n)) for i in range(n));checks['orthogonal']=all(sum((T[i][b]*aa[i] for i in range(n)),F(0))==0 for b in range(4));ca=[sum((C[i][j]*aa[j] for j in range(n)),F(0)) for i in range(n)];den=sum((aa[i]*ca[i] for i in range(n)),F(0));checks['denominator']=den==F(c['denominator']) and den>0
# Reconstruct native residual intervals directly in a different accumulation order.
pb=ev['projected_bounds'];w=ev['weights'];nodes=ev['node_indices'];base=ev['base'];y=ev['data'];boxes=[]
for i in range(n):
 b,k=divmod(i,15);lower=F(float(y[i]))-F(float(base[i]));upper=lower
 for j,node in reversed(list(enumerate(nodes))):
  ww=F(float(w[b,node]));lower-=ww*F(float(pb[j,b,k,1]));upper-=ww*F(float(pb[j,b,k,0]))
 boxes.append((lower,upper))
checks['native_boxes']=all(boxes[i]==tuple(map(F,c['native_residual_boxes'][i])) for i in range(n));nl=sum((min(aa[i]*boxes[i][0],aa[i]*boxes[i][1]) for i in range(n)),F(0));nh=sum((max(aa[i]*boxes[i][0],aa[i]*boxes[i][1]) for i in range(n)),F(0));checks['numerator_box']=[nl,nh]==list(map(F,c['numerator_box']));dist=max(nl,-nh,F(0));bound=dist**2/den;checks['bound']=bound==F(c['dual_lower']);checks['point_Cauchy_Schwarz']=F(c['point_dual'])<=F(c['baseline_candidate_score']);checks['law_b_nonnegative']=all(F(x)>=0 for x in c['law_b']);checks['margin_exact']=bound>F(c['law_candidate_upper'])+9;checks['original_controls']=all(d['checks'].values());checks['inputs_stable']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,input_sha256=hashes,exact_margin=str(bound-F(c['law_candidate_upper'])-9),review='Self/adversarial full rational certificate reconstruction, independent native-box accumulation order; no independent-agent claim',scope='Original C,T nuisance bound conditional on published anchored fixed-projection boxes; physical continuum coverage still open')
(p/'exact_dual_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),'allpass',all(checks.values()));assert all(checks.values())
