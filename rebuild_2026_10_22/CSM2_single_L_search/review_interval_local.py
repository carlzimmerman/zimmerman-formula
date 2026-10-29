"""Independent score-box arithmetic and pinned baseline-column reconciliation."""
from pathlib import Path
import json,hashlib
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'interval_001';d=json.loads((run/'results.json').read_text());z=np.load(run/'score_boxes.npz');checks={}
lo=np.asarray(z['residual_lower'],np.longdouble);hi=np.asarray(z['residual_upper'],np.longdouble);dist=np.where(lo>0,lo,np.where(hi<0,-hi,0));lower=max(0,float(np.sum(dist*dist))-.0001);checks['independent_box_bound']=bool(np.isfinite(lower) and abs(lower-d['lower_score'])<1e-8)
checks['root_domain']=all(b['r0_lower']>b['R']*1e-7 and b['r0_upper']<b['R']*1e3 for b in d['root_brackets']);checks['no_saturation']=not any(b['saturated'] for b in d['root_brackets']);checks['all_nodes']=len(d['nodes'])==127 and sum(n['halo'] for n in d['nodes'])==62
cols=json.loads((r/'rebuild_2026_10_22/CSM1_consistent_core_switch/calibration/run_003_audited/results.json').read_text())['levels']['3.75']['lens']['core_columns'];cols=[c for c in cols if c['footing']=='canonical']
errors=[]
for n in d['nodes']:
 c=min(cols,key=lambda c:abs(c['mass']/n['M']-1));errors.append(max(abs(c['mass']/n['M']-1),abs(c['column']/n['column']-1),abs(c['floor']/n['floor']-1)));assert c['expected']==n['halo']
checks['pinned_columns']=bool(np.isfinite(errors).all() and max(errors)<1e-12);checks['no_event_margin']=all(not(3.75-1e-10<=n['threshold']<=3.751+1e-10) for n in d['nodes']);checks['source_samples']=all(s['free_score']>=lower for s in d['source_scores']);checks['conditional_label']=d['conditional_numeric_exclusion'] and not d['certified_exclusion']
files=[Path(__file__),run/'results.json',run/'score_boxes.npz'];result=dict(checks=checks,independent_lower_score=lower,max_pinned_column_relative_error=max(errors),input_sha256={str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},review='Self/adversarial reconstruction; no independent-agent or exact-interval certification',limitations=['Root comparisons, peak location and padding remain binary64 conditional','Source-law mass profiles are inherited from audited source rather than independently rederived','Branch and weight mutation controls are perturbation sensitivity checks, not a second end-to-end mutated source run','Proof note is hashed after arithmetic; dynamically traced scientific inputs were hashed on first read and checked stable'])
(p/'interval_review.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values())
