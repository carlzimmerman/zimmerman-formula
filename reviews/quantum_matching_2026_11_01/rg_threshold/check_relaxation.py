import json,sys,resource
from pathlib import Path
import numpy as np
import mpmath as mp
from relaxation import normal_data,normal_data_reference,matrices,d
mp.mp.dps=50
rows=[];matrix_controls=[]
for es in ['.01','.03','.05','.1']:
    e=mp.mpf(es);x=mp.mpf('7.3671437212785083116194')*mp.sqrt(e/31)/e
    for ratio in ['1','1.2','1.5']:
        r=normal_data_reference(x*mp.mpf(ratio),e,cp_controls=True);r.update(e=float(e),X_over_TP01min=float(ratio));rows.append(r)
    c=[float(e),float(e),float(mp.sqrt(mp.mpf(29)/200)*e),1.];X=float(x)
    a=(2*c[0]/(30*c[0]**2+c[1]**2))**.5;b=c[0]*X/c[1]
    for label,dz in [('a',np.r_[0j,1j*d,np.zeros(24)]),('b',np.r_[0j,np.zeros(24),d])]:
        step=1e-5*max(1,a if label=='a' else b)
        plus=matrices(X,a+(step if label=='a' else 0),b+(step if label=='b' else 0),c)
        minus=matrices(X,a-(step if label=='a' else 0),b-(step if label=='b' else 0),c)
        exact=matrices(X,a,b,c,dz)
        errs=[float(np.max(abs((p-m)/(2*step)-v)))/max(1,float(np.max(abs(v)))) for p,m,v in zip(plus,minus,exact)]
        matrix_controls.append({'e':float(e),'direction':label,'max_scaled_error':max(errs)})
checks={'12_states':len(rows)==12,'analytic_matrix_derivatives':max(r['max_scaled_error'] for r in matrix_controls)<1e-7,
        'CP_odd_tadpoles_zero':max(abs(v) for r in rows for v in r['CP_odd_tadpoles'])<1e-14,
        'normal_relative_shifts_below_1percent':max(abs(r[k]) for r in rows for k in ['a_relative_shift','b_relative_shift'])<.01,
        'angular_metric_stays_positive':all(r['F0']+r['deltaF_angular']>0 for r in rows),
        'vacuum_relaxation_negative':all(r['deltaU_vac']<0 for r in rows)}
out={'claim_id':'TP02_FINITE_RELAXATION','checks':checks,'states':rows,'matrix_controls':matrix_controls,
     'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
     'non_claims':['Gaugedfixed-scheme finite matching subset, not complete two-loop potential',
                   'Angular geometric correction omits direct finite derivative graphs',
                   'Native occupied source must include CWb−omega²60b and E² term, not only vacuumshift/metric']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
