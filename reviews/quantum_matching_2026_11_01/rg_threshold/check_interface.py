import json,sys,resource,time
from pathlib import Path
import mpmath as mp
from improved import evaluate,profile,threshold,C1,flow
mp.mp.dps=50
e=mp.mpf('.03');x=mp.mpf('7.367143721278508')*mp.sqrt(e/31)/e
rows=[];start=time.monotonic()
for scheme in ['fixed','rg1','rg2','rg2log']:
    for eta in map(mp.mpf,('.5','1','2')):
        o=evaluate(x,e,eta,scheme,32);r={'scheme':scheme,'eta':float(eta)}
        r.update({k:str(o[k]) for k in ['U','F','Q','Qm','U2log','field_transport_error']})
        if 'critical_ratio_drift' in o:r['critical_ratio_drift']=str(o['critical_ratio_drift'])
        rows.append(r)
o32=evaluate(x,e,1,'rg2',32);o64=evaluate(x,e,1,'rg2',64)
step_error=abs(o32['U']-o64['U']);ferror=abs(o32['F']/o64['F']-1)
at=x*mp.mpf('1.2');p=profile(at,e,1,'rg2',32)
dh=mp.mpf('.002');vs=[evaluate(at*mp.exp(i*dh),e,1,'rg2',32)['U'] for i in (-2,-1,0,1,2)]
us=(vs[0]-8*vs[1]+8*vs[3]-vs[4])/(12*dh);uss=(-vs[0]+16*vs[1]-30*vs[2]+16*vs[3]-vs[4])/(12*dh**2)
errors=[abs(us-p['U_s']),abs(uss-p['U_ss'])]
spreads={}
for scheme in ['rg1','rg2','rg2log']:
    us=[mp.mpf(r['U']) for r in rows if r['scheme']==scheme]
    spreads[scheme]=max(us)-min(us)
checks={'RK4_U_step_error_below_1e-24':step_error<mp.mpf('1e-24'),
        'RK4_F_relative_step_error_below_1e-20':ferror<mp.mpf('1e-20'),
        'characteristic_T_dictionary':max(abs(mp.mpf(r['field_transport_error'])) for r in rows)<mp.mpf('1e-20'),
        'independent_derivatives_abs_below_1e-15':max(errors)<mp.mpf('1e-15'),
        'CS2log_reduces_scale_spread':spreads['rg2log']<spreads['rg2'],
        'actual_gcrit_drift_not_reset':any(abs(mp.mpf(r.get('critical_ratio_drift','0')))>mp.mpf('1e-10') for r in rows)}
out={'claim_id':'TP02_INTERFACE','checks':checks,'rows':rows,'RK4_U_step_error':str(step_error),'RK4_F_relative_step_error':str(ferror),
     'independent_derivative_errors':[str(v) for v in errors],'scale_spreads':{k:str(v) for k,v in spreads.items()},
     'profile':{k:str(p[k]) for k in ['U','F','U_s','U_ss','a','a_prime']},
     'runtime_seconds_observed':time.monotonic()-start,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
     'non_claims':['Scale-spread reduction is not a bound on unknown finite two-loop matching','F contains RG angular wavefunction only; no finite threshold metric']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
