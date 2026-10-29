"""Directed outer-mass sign check, independently normalized at70digits."""
from pathlib import Path
import hashlib,json,math
from mpmath import iv
p=Path(__file__).resolve().parent;r=p.parents[1];source=p/'interval_001/results.json';prior=p/'root_sign_001/results.json';d=json.loads(source.read_text());old=json.loads(prior.read_text());iv.dps=70;checks={};rows=[]
for i,b in enumerate(d['root_brackets']):
 M,R,S=[iv.mpf(b[k]) for k in ('M','R','Sigma')];signs=[]
 for k in ('r0_lower','r0_upper'):
  rr=iv.mpf(b[k]);x=R/rr;B=iv.log((1+x*x)*(1+x)**2)-2*iv.atan2(x,iv.mpf(1));res=iv.pi*S*rr*rr*B-M;signs.append(bool(res.b<0 if k=='r0_lower' else res.a>0));assert all(math.isfinite(float(v)) for v in (res.a,res.b))
 rows.append(dict(index=i,lower_outer_mass_below_target=signs[0],upper_outer_mass_above_target=signs[1]));checks[str(i)]=all(signs)
checks['coverage']=len(rows)==124;checks['original_all_pass']=all(old['checks'].values()) and old['certified_scalar_root_brackets']==124
result=dict(checks=checks,rows=rows,interval_digits=70,scope='Scalar signs only: independent outer-mass normalization and log-product expression; not a full model interval proof',input_sha256={str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [source,prior,Path(__file__)]})
(p/'root_sign_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),'all_pass',all(checks.values()));assert all(checks.values())
