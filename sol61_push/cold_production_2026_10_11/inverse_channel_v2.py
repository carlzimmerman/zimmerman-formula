"""Kinematic screen of moving-source inverse production, not a collision rate."""
import json, math
from pathlib import Path
import numpy as np
p=Path(__file__).parent
source=json.loads((p/'envelope_run_v2/results.json').read_text())
u=source['parameters']['u']; checks=[]; rows=[]
def geometry(p2,q2):
    prod=np.sqrt((1+p2)*(1+q2))
    prod_minus_one=(p2+q2+p2*q2)/(prod+1)
    ct=(prod_minus_one-2*u*u)/np.sqrt(p2*q2)
    K2=p2+q2+2*prod_minus_one-4*u*u
    return ct,K2
for ratio in [.8,1.,1.2]:
    p2=ratio*u*u;ct,K2=geometry(p2,p2)
    expected=1-2/ratio
    checks.append(dict(name='equal momenta ratio '+str(ratio),passed=abs(ct-expected)<1e-12 and abs(K2-4*(p2-u*u))<1e-18))
for row in source['rows']:
    p2=(np.array(row['initial_mode_p_over_m'])/row['a_at_x200'])**2
    F=np.array(row['final_pair_fractions']);weights=F/F.sum()
    ct,K2=geometry(p2[:,None],p2[None,:])
    allowed=(ct>=-1)&(ct<=1)&(K2>=0)
    pair_weights=weights[:,None]*weights[None,:]
    eligible=float(np.sum(pair_weights*allowed))
    high=float(np.sum(weights[p2>u*u]))
    rows.append(dict(K=row['K'],vmax=row['vmax'],independent_magnitude_pair_eligibility=eligible,daughter_number_fraction_above_rest_source_resonance=high,max_kinematically_allowed_source_p_over_m=float(np.sqrt(K2[allowed].max()))))
    checks.append(dict(name='probability bounds K'+str(row['K']),passed=0<=eligible<=1 and 0<=high<=1))
checks=[dict(c,passed=bool(c["passed"])) for c in checks]
out=dict(rows=rows,checks=checks,all_pass=all(x['passed'] for x in checks),non_claims=['Eligibility is not angular probability, production fraction or rate','Product magnitude weights do not model quantum correlations','No collision evolution'])
(p/'inverse_channel_run_v2'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
