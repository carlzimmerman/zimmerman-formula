import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
REB=HERE.parent
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
source=REB/'X48_native_cf_zoom/x48_analyze.py'
a2path=REB/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json'
priorpath=REB/'NATIVE_PARTIAL_2026-10-28/measurement_002_three/results.json'
snapshots={(ng,s):REB/f'X48_native_cf_zoom/runs/M1e12_s{s}_ng{ng}/snap_zf.npz' for ng in (48,64) for s in (3,7,8)}
files=[Path(__file__),HERE/'NATIVE_DIAGNOSTIC_CRITERIA.md',source,a2path,priorpath,*snapshots.values()]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p.relative_to(ROOT)):sha(p) for p in files}
src=source.read_text();old='edges = np.geomspace(rconv, rvir, 25)';assert src.count(old)==1
a2=json.loads(a2path.read_text());prior=json.loads(priorpath.read_text());results={};checks={}
for edges in (21,25,29):
    ns=dict(__file__=str(source),__name__='x48_diagnostic_readonly')
    code=src.replace(old,f'edges = np.geomspace(rconv, rvir, {edges})')
    exec(compile(code,str(source),'exec'),ns)
    n=12000
    control=ns['measure'](ns['synthetic_nfw'](4.,n,1),1/n,1/(4/3*math.pi)/(18*math.pi**2),1e-4)
    good=control.get('flag')=='ok' and abs(control['cf']/4-1)<.15
    rows={}
    for (ng,s),p in snapshots.items():
        with np.load(p,allow_pickle=False) as z:
            m=json.loads(str(z['meta']));rho=m['Mf']/(4/3*math.pi*m['qM']**3)*(1+m['zf'])**3
            r=ns['measure'](z['x'],float(z['m']),rho,m['eps'])
        rows[f'{ng}|{s}']=r
    paired={}
    for s in (3,7,8):
        lo,hi=rows[f'48|{s}'],rows[f'64|{s}']
        if lo.get('flag')==hi.get('flag')=='ok':
            paired[str(s)]=dict(cf48=lo['cf'],cf64=hi['cf'],ratio64_over48=hi['cf']/lo['cf'],
                paired_L_diagnostic=7.31*hi['cf']/lo['cf'],
                prescribed_L_proxy=7.31*hi['cf']/a2['cf_by_mass']['1e+12'])
    results[str(edges)]=dict(synthetic_control=control,synthetic_control_valid=good,runs=rows,paired=paired)
primary=results['25']
checks['primary_benchmark']=primary['synthetic_control_valid']
checks['ng48_reproduces_cached']=all(abs(primary['runs'][f'48|{s}']['cf']-a2['runs'][f'M1e12_s{s}_ng48']['cf'])<1e-10 for s in (3,7,8))
checks['ng64_reproduces_published']=all(abs(primary['runs'][f'64|{s}']['cf']-prior['runs'][str(s)]['cf'])<1e-10 for s in (3,7,8))
checks['inputs_stable']=all(sha(ROOT/p)==h for p,h in before.items())
result=dict(scope='Finite diagnostic only; primary estimator and NL1 prescription unchanged',checks=checks,variants=results,input_sha256=before)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(checks=checks,paired=primary['paired'],variants={k:{s:v['paired'].get(s,{}).get('prescribed_L_proxy') for s in ('3','7','8')} for k,v in results.items()}),indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
