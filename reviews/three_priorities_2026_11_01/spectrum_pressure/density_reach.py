import json,sys,resource
from pathlib import Path
import mpmath as mp
from pressure_scan import cw
mp.mp.dps=60
data=json.loads(Path(sys.argv[2]).read_text());roots=data['direct_derivative_roots']
x0=mp.mpf(roots['X_min']);xp=mp.mpf(roots['X_pressure']);h=lam=mp.mpf('.6');g=mp.sqrt(mp.mpf(29)/200)*lam
def d(x,n=1):return mp.diff(lambda s:cw(x*mp.exp(s),h,lam,g),0,n)
B=d(x0,2)/9;sp=mp.log(xp/x0);rows=[]
for j in range(1,34):
    s=sp*j/33;x=x0*mp.exp(s);us=d(x);uss=d(x,2);wss=2*us+uss
    rho=(us*mp.exp(2*s)/(3*B))**(mp.mpf(3)/5)
    rows.append({'s':float(s),'X_over_min':float(x/x0),'rho_over_rhostar':float(rho),
                 'U_s':float(us),'Wss':float(wss),'dlnrho_ds':float(3*wss/(5*us)),
                 'compressibility_numerator':float(uss-3*us)})
checks={'33_positive_source_states':all(r['U_s']>0 for r in rows),
        '33_radially_stable_states':all(r['Wss']>0 for r in rows),
        '33_monotone_density_states':all(a['rho_over_rhostar']<b['rho_over_rhostar'] for a,b in zip(rows,rows[1:])),
        'density_below_old_scale':rows[-1]['rho_over_rhostar']<1,
        'positive_compressibility_interior':all(r['compressibility_numerator']>0 for r in rows[:-1])}
out={'claim_id':'TP01_DENSITY_REACH','checks':checks,'Bcurv':str(B),'s_pressure':str(sp),
     'rho_over_rhostar_at_pressure_boundary':str((d(xp)*mp.exp(2*sp)/(3*B))**(mp.mpf(3)/5)),
     'monotonicity_identity':'dlnrho/ds=3(2Us+Uss)/(5Us)>0 on the positive-source radial stable branch',
     'cases':rows,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
     'non_claims':['Comparison rho_* is defined from vacuum curvature, not a proven asymptotic log coefficient',
                   'The unknown waterbag phase level k cancels; no measured density predicted','No full higher-loop/portal/halo completion']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2));assert all(checks.values()),checks
