#!/usr/bin/env python3
"""Fresh worst-witness replay for every failed T2 pair in the saved audit snapshot."""
import ast,hashlib,json,math,os,resource,sys,time
from pathlib import Path
import engines as E
HERE=Path(__file__).resolve().parent;started=time.time();ns=E.small();np=ns['np']
source=HERE/'small_worker.py';tree=ast.parse(source.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='kmat')
kernel={'np':np,'math':math};exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),kernel);ns['kmat']=kernel['kmat']
audit_path=HERE/'main/small_pair_checks.json';audit=json.loads(audit_path.read_text());rows=[];checks=[];pairs=[]
for result in audit['results']:
    if not any(name.endswith('_T2_pair') for name in result['failed']):continue
    index=result['index'];saved=[json.loads((HERE/'main/small'/f'p{index:03d}_r{rung}.json').read_text()) for rung in (1,2)]
    for record in saved:
        assert all(record['source_hashes'][k]==v for k,v in E.hashes().items())
        assert record['source_hashes']['small_worker.py']==hashlib.sha256(source.read_bytes()).hexdigest()
    for foot in ('canonical','alt'):
        if foot+'_T2_pair' not in result['failed']:continue
        coarse,fine=[record['dwarf_evaluations'] for record in saved]
        keys=sorted(k for k,v in coarse.items() if v['footing']==foot)
        assert keys and all(k in fine for k in keys)
        key=max(keys,key=lambda k:abs(coarse[k]['sigma']/fine[k]['sigma']-1))
        expected_change=abs(coarse[key]['sigma']/fine[key]['sigma']-1)
        reported=next(c['value']['max_relative'] for c in result['checks'] if c['name']==foot+'_T2_pair')
        checks.append(dict(name=f'p{index}_{foot}_worst_matches_audit',passed=abs(expected_change-reported)<=1e-12))
        values=[]
        for rung,record in enumerate(saved,1):
            witness=record['dwarf_evaluations'][key];ns['rgrid'].__defaults__=(2000*rung,)
            dwarf=next(d for d in ns['rows'] if d['name']==witness['name']);obj=ns['Dwarf'](dwarf,witness['width']);a0=ns['A0SI'][foot]*ns['CONV']
            value=float(obj.sigma(witness['mass'],a0,ns['GEV']['E1'](dwarf,a0),'R'));del obj
            error=abs(value/witness['sigma']-1);values.append(value)
            rows.append(dict(index=index,rung=rung,footing=foot,name=witness['name'],mass=witness['mass'],width=witness['width'],stored_sigma=witness['sigma'],replayed_sigma=value,relative_difference=error))
            checks.append(dict(name=f'p{index}_{foot}_r{rung}_replay',passed=error<=1e-8))
        change=abs(values[0]/values[1]-1)
        checks.append(dict(name=f'p{index}_{foot}_change_reproduced',passed=abs(change-expected_change)<=1e-8))
        pairs.append(dict(index=index,p=result['p'],L_MW=result['L_MW'],footing=foot,witness=key,relative_change=change,frozen_line=.01,
                          pass_lists_changed=set(saved[0]['result']['T2'][foot]['passed'])!=set(saved[1]['result']['T2'][foot]['passed']),
                          label='UNDECIDED' if change>.01 else 'Dispersion witness within line; inspect changed pass lists'))
obj=dict(audited_completed_pairs=audit['pairs'],failed_points=len(set(r['index'] for r in pairs)),checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),rows=rows,pairs=pairs,
    source_hashes={**E.hashes(),**{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),source,HERE/'FROZEN_CRITERIA.md',audit_path]}},
    versions=dict(python=sys.version.split()[0],numpy=np.__version__),
    scope='Fresh worst dispersion witnesses for every failed T2 footing in saved snapshot; no new resolution/tolerance or full FN6 verdict; kappa=1/2 FITTED; not theory closed')
def atomic(path,value):
    tmp=path.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
atomic(HERE/'main/all_dwarf_failure_replay.json',obj);atomic(HERE/'main/all_dwarf_failure_replay_runtime.json',dict(seconds=time.time()-started,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print(json.dumps(dict(audited_pairs=audit['pairs'],failed_points=obj['failed_points'],replayed_values=len(rows),passed=obj['passed'],total=obj['total']),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
