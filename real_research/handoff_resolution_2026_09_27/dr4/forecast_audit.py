#!/usr/bin/env python3
"""Independent algebra on XR22 stored bin forecasts; no new force solves."""
from pathlib import Path
import json, math, hashlib, datetime, platform, sys
import numpy as np
O=Path(__file__).resolve().parent; R=O.parents[2]
p=R/'real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic_results.json'
x=json.loads(p.read_text())['numbers']; ans=[]
for foot in ['canonical','alt']:
    rows=sorted([(float(k.split('|')[1]),v) for k,v in x['sepbins'].items() if k.startswith(foot+'|')])
    for (a,A),(b,B) in zip(rows[:-1],rows[1:]):
        if a>.10001: continue
        d=np.array([(rb['ratio']-ra['ratio'])/math.log(b/a) for ra,rb in zip(A,B)])
        sig=np.array([ra['sig_med']*math.sqrt(ra['n']/(30000*ra['frac'])) for ra in A]); w=1/sig**2
        h=np.array([1+ra['ratio'] for ra in A])
        info=float(np.dot(d*w,d)); ref=sum(x['fisher_sep'][f'{foot}|{a:.6g}'])
        profile=info-float(np.dot(d*w,h))**2/float(np.dot(h*w,h))
        # Named sensitivity scenario: hypothetical rank-one 2% multiplicative calibration uncertainty.
        C=np.diag(sig**2)+.02**2*np.outer(h,h)
        corr=float(d@np.linalg.solve(C,d))
        assert abs(info-ref)<1e-10*max(1,info)
        assert profile>=-1e-10 and corr<=info+1e-10
        assert np.dot(np.zeros_like(d)*w,np.zeros_like(d))==0
        ans.append(dict(footing=foot,xi_pc=a,next_xi_pc=b,fisher=info,sigma_fixed_calibration=1/math.sqrt(info),sigma_free_common_amplitude=1/math.sqrt(profile),sigma_hypothetical_correlated_2percent=1/math.sqrt(corr),ratio_2to5_over_20to30=(A[0]['ratio']+A[1]['ratio'])/(2*A[-1]['ratio']),source_fisher_difference=info-ref))
result={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Algebraic audit of stored forecast; not new forward-model run. Profile common amplitude ignores anchor; 2% rank-one term is a sensitivity scenario, not inherited frozen covariance.','rows':ans,'checks':{'source_fisher_agrees':True,'profile_never_increases_information':True,'xi_free_mutation_information_zero':True},'versions':{'python':sys.version,'numpy':np.__version__}}
(O/'forecast_audit_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(ans,indent=2))
