"""Exact-dyadic review:24 projection dots and final stored-box score.
Predeclared cases: node rows0,31,61; bins0,3; projection rows0,14;
both coefficient-sign-selected lower and upper endpoint vectors. No sampling
is represented as exhaustive; main arithmetic bound covers all7440dot visits.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,math
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'signed_dot_002_cached';files=[Path(__file__),run/'results.json',run/'signed_map_evidence.npz'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};d=json.loads(files[1].read_text());z=np.load(files[2]);checks={};count=0
for node in (0,31,61):
 for b in (0,3):
  for row in (0,14):
   c=z['A'][b,row]
   for endpoint in (0,1):
    x=np.where(c>=0,z['delta_lower'][node] if endpoint==0 else z['delta_upper'][node],z['delta_upper'][node] if endpoint==0 else z['delta_lower'][node]);exact=sum((F(float(a))*F(float(v)) for a,v in zip(c,x)),F(0));lo,hi=z['projected_bounds'][node,b,row];key=f'{node}|{b}|{row}|{endpoint}';checks[key]=F(float(lo))<=exact<=F(float(hi));count+=1
score=F(0)
for lo,hi in z['residual_bounds']:
 dist=F(float(lo)) if lo>0 else -F(float(hi)) if hi<0 else F(0);score+=dist*dist
floorfloat=math.nextafter(float(score),-math.inf);checks['exact_box_score_floor']=F(floorfloat)<=score;checks['large_margin_for_stored_box']=score>F('163.34346325076024');checks['agreement_diagnostic']=abs(float(score)-d['lower_score_fixed_map'])<1e-8;checks['finite_evidence']=all(np.isfinite(z[k]).all() for k in z.files);checks['coverage']=count==24;checks['original_controls']=all(d['checks'].values());checks['inputs_stable']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,projection_dot_cases=count,exact_stored_box_score_floor=floorfloat,score_numerator=str(score.numerator),score_denominator=str(score.denominator),input_sha256=hashes,scope='Exact dyadic selected-dot and stored-residual-box arithmetic review; fixed anchored map only',full_model_interval_certified=False)
(p/'signed_dot_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),'allpass',all(checks.values()),'exact stored-box floor',floorfloat);assert all(checks.values())
