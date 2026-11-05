#!/usr/bin/env python3
"""Grade the entire frozen AZ45 grid; missing/unresolved fits cannot yield power."""
import argparse,hashlib,itertools,json,math,platform
from pathlib import Path
import numpy as np
import scipy
import engine as E
import calibration as C
import population as P

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def key(c):return f"t{c['template']:02d}_r{c['rung']}_{c['foot']}_n{c['replicate']}_{c['scenario']}_s{c['snr']}_{c['hi']}_{c['mode']}_{c['step']}"
def grade(tag):
    versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__)
    sources=E.hashes();worker=sha(E.HERE/'worker.py');seen={};missing=set();errors={};loaded={}
    def read(c):
        name=str(Path(tag)/c['mode']/(key(c)+'.json'));path=E.HERE/name
        if name in loaded:return loaded[name]
        if not path.exists():missing.add(name);return None
        seen[name]=sha(path)
        try:
            obj=json.loads(path.read_text());v=obj['scientific']
            expected=dict(sources=sources,worker=worker,arguments=c,versions=versions)
            if obj['identity']!=expected:raise ValueError('stale or mismatched identity')
            for field,ck in [('rung','rung'),('footing','foot'),('replicate','replicate'),('scenario','scenario'),('snr','snr'),('hi_case','hi'),('mode','mode'),('step','step')]:
                if v[field]!=c[ck]:raise ValueError('scientific metadata mismatch: '+field)
            if v['template']!=E.TEMPLATES[c['template']]:raise ValueError('template mismatch')
            fits=v['fits']
            if len(fits)!=2:raise ValueError('two starts required')
            finite=[f for f in fits if math.isfinite(f['chi2']) and all(math.isfinite(x) for x in f['parameters'])]
            if not finite:raise ValueError('no finite fit')
            best=min(finite,key=lambda f:f['chi2']);delta=best['parameters'][10]-v['template']['logM']
            resolved=len(finite)==2 and all(f['status']>0 for f in finite) and abs(fits[0]['parameters'][10]-fits[1]['parameters'][10])<=.05
            if v['resolved']!=resolved or not math.isclose(delta,v['delta'],rel_tol=0,abs_tol=1e-12):raise ValueError('inconsistent fit summary')
            loaded[name]=v;return v
        except (KeyError,ValueError,TypeError,IndexError) as ex:
            errors[name]=str(ex);return None
    controls=json.loads((E.HERE/'controls.json').read_text())
    globals_ok=(controls['source_hashes']==sources and controls['versions']==versions and
                len(controls['checks'])==56 and all(c['passed'] for c in controls['checks']) and
                len(controls['forward_pairs'])==24 and all(c['passed'] for c in controls['forward_pairs']))
    evidence={}
    for filename in ['population_checks.json','calibration_checks.json']:
        obj=json.loads((E.HERE/filename).read_text());valid=all(c['passed'] for c in obj['checks'])
        valid=valid and all(sha(E.HERE/p)==h for p,h in obj['source_hashes'].items())
        globals_ok=globals_ok and valid;evidence[filename]=dict(sha256=sha(E.HERE/filename),valid=valid)
    rows=[]
    for fi,(foot,hi,snr) in enumerate(itertools.product(E.FOOTS,['free','fixed'],[30,60,120,240])):
        noisy=np.empty((2,3,3,4,3));levers=np.empty((2,12,6));complete=True;resolved=True;boundary=[];unresolved=[]
        for tid,rung in itertools.product(range(12),[1,2]):
            base=dict(template=tid,foot=foot,hi=hi,rung=rung,replicate=0,scenario='flat',snr=30)
            for li,(mode,step) in enumerate([('reference',.01),('double',.01),('plus',.01),('minus',.01),('plus',.005),('minus',.005)]):
                c=dict(base,mode=mode,step=step);v=read(c)
                if v is None:complete=False;continue
                levers[rung-1,tid,li]=v['delta'];resolved=resolved and v['resolved']
                if not v['resolved']:unresolved.append(key(c))
                if v['boundary_names']:boundary.append(dict(case=key(c),parameters=v['boundary_names']))
            for rep,scenario_index in itertools.product(range(3),range(3)):
                scenario='rise' if scenario_index==1 else 'flat';mode='mutate' if scenario_index==2 else 'main'
                c=dict(base,mode=mode,step=.01,replicate=rep,scenario=scenario,snr=snr);v=read(c)
                if v is None:complete=False;continue
                noisy[rung-1,scenario_index,tid//4,tid%4,rep]=v['delta'];resolved=resolved and v['resolved']
                if not v['resolved']:unresolved.append(key(c))
                if v['boundary_names']:boundary.append(dict(case=key(c),parameters=v['boundary_names']))
        row=dict(footing=foot,hi=hi,snr=snr,complete=complete,label='NO VERDICT',boundary_hits=boundary,unresolved=unresolved)
        if complete:
            cal=C.calibrate(noisy,levers,resolved);row['calibration']=cal
            if cal['passed'] and globals_ok:
                scan=[]
                for total in [36,72,144,288,576,1152]:
                    scan.extend(P.rates(noisy[1,0],noisy[1,1],total,snr,list(E.FOOTS).index(foot),['free','fixed'].index(hi)))
                for r in scan:r['label']='NO VERDICT' if not r['converged'] else ('WINDOW' if r['rungs'][1]['power_gate'] else 'FAIL')
                row['scan']=scan
                row['label']='WINDOW' if any(r['label']=='WINDOW' for r in scan) else ('NO VERDICT' if any(r['label']=='NO VERDICT' for r in scan) else 'FAIL')
            else:row['reason']='calibration/control/resolution failure; no power claim'
        else:row['reason']='missing or invalid cases; no imputation'
        rows.append(row)
    expected_unique=4032
    if len(set(seen)|missing)!=expected_unique:raise RuntimeError('Grader does not cover the frozen4032-case grid')
    footings={f:('WINDOW' if any(r['label']=='WINDOW' for r in rows if r['footing']==f) else
                  ('FAIL' if all(r['label']=='FAIL' for r in rows if r['footing']==f) else 'NO VERDICT')) for f in E.FOOTS}
    return dict(status='IN PROGRESS' if missing else ('UNDECIDED: invalid evidence' if errors else 'complete grid graded'),
                footings=footings,expected_cases=expected_unique,found_cases=len(seen),missing_cases=len(missing),invalid_cases=errors,
                global_controls_passed=bool(globals_ok),statistical_evidence=evidence,rows=rows,input_hashes=seen,
                code_hashes={p.name:sha(p) for p in [Path(__file__),Path(C.__file__),Path(P.__file__)]},
                source_hashes=sources,versions=versions,
                scope='Conditional synthetic mass-residual forecast, not a sealed a0(z) prediction; kappa=1/2 FITTED; not theory closed')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--tag',default='grid');a=ap.parse_args();out=grade(a.tag)
    E.atomic(E.HERE/a.tag/'population_report.json',out)
    print(json.dumps({k:out[k] for k in ['status','footings','expected_cases','found_cases','missing_cases','global_controls_passed']},indent=2))
    raise SystemExit(1 if out['invalid_cases'] else (75 if out['missing_cases'] else 0))
