#!/usr/bin/env python3
"""Exercise complete coverage and corrupt-result rejection using temporary fixtures."""
import copy,hashlib,itertools,json,platform,tempfile
from pathlib import Path
import numpy as np
import scipy
import engine as E
import grade as G
checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
def cases():
    for tid,foot,hi,rung in itertools.product(range(12),E.FOOTS,['free','fixed'],[1,2]):
        for mode,step in [('reference',.01),('double',.01),('plus',.01),('minus',.01),('plus',.005),('minus',.005)]:
            yield dict(template=tid,foot=foot,hi=hi,rung=rung,mode=mode,step=step,replicate=0,scenario='flat',snr=30)
    for tid,rep,snr,foot,hi,rung,scenario in itertools.product(range(12),range(3),[30,60,120,240],E.FOOTS,['free','fixed'],[1,2],['flat','rise']):
        for mode in (['main','mutate'] if scenario=='flat' else ['main']):
            yield dict(template=tid,foot=foot,hi=hi,rung=rung,mode=mode,step=.01,replicate=rep,scenario=scenario,snr=snr)
with tempfile.TemporaryDirectory(prefix='grader_fixture_',dir=E.HERE) as d:
    directory=Path(d);tag=directory.name;paths=[]
    for c in cases():
        t=E.TEMPLATES[c['template']];mode=c['mode']
        delta=(-.2 if mode in ['mutate','double'] else (-.3*c['step'] if mode=='plus' else (.3*c['step'] if mode=='minus' else (.60*(t['z']-1) if c['scenario']=='rise' else 0.))))
        pars=[0.]* (12 if c['hi']=='free' else 11);pars[10]=t['logM']+delta
        fit=dict(parameters=pars,chi2=1.,status=1)
        s=dict(template=t,rung=c['rung'],footing=c['foot'],replicate=c['replicate'],scenario=c['scenario'],snr=c['snr'],hi_case=c['hi'],mode=mode,step=c['step'],delta=pars[10]-t['logM'],resolved=True,fits=[fit,copy.deepcopy(fit)],boundary_names=[])
        obj=dict(identity=dict(sources=E.hashes(),worker=G.sha(E.HERE/'worker.py'),arguments=c,versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__)),scientific=s)
        p=directory/mode/(G.key(c)+'.json');p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(obj));paths.append(p)
    full=G.grade(tag)
    check('all4032_cases_covered',full['found_cases']==4032 and full['missing_cases']==0 and not full['invalid_cases'])
    check('sixteen_cells_eighteen_forecasts_each',len(full['rows'])==16 and all(len(r.get('scan',[]))==18 for r in full['rows']))
    check('both_footings_calibrated_fixture',all(v=='WINDOW' for v in full['footings'].values()))
    p=next(p for p in paths if p.parent.name=='main');saved=p.read_text();obj=json.loads(saved)
    obj['scientific']['resolved']=False;p.write_text(json.dumps(obj))
    bad=G.grade(tag);check('inconsistent_resolution_rejected',len(bad['invalid_cases'])==1)
    check('invalid_case_withholds_affected_power',any(not r['complete'] and 'scan' not in r for r in bad['rows']))
    obj=json.loads(saved);obj['identity']['worker']='stale';p.write_text(json.dumps(obj))
    check('stale_worker_rejected',len(G.grade(tag)['invalid_cases'])==1)
    p.unlink();missing=G.grade(tag)
    check('missing_case_not_imputed',missing['missing_cases']==1 and any(not r['complete'] and 'scan' not in r for r in missing['rows']))
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={p.name:G.sha(p) for p in [Path(__file__),Path(G.__file__)]},scope='Temporary synthetic4032-case fixtures only; no production fit or power claim')
E.atomic(E.HERE/'grader_checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
