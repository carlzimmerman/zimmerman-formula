#!/usr/bin/env python3
"""Replay the first failed T2 witnesses; do not change either frozen resolution."""
import ast,hashlib,json,math,os,resource,time
from pathlib import Path
import engines as E
HERE=Path(__file__).resolve().parent;started=time.time();ns=E.small();np=ns['np']
source=HERE/'small_worker.py';tree=ast.parse(source.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='kmat')
kernel={'np':np,'math':math};exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),kernel);ns['kmat']=kernel['kmat']
rows=[];checks=[]
for index in [91,92]:
    for rung in [1,2]:
        path=HERE/'main/small'/f'p{index:03d}_r{rung}.json';saved=json.loads(path.read_text())
        assert all(saved['source_hashes'][k]==v for k,v in E.hashes().items())
        assert saved['source_hashes']['small_worker.py']==hashlib.sha256(source.read_bytes()).hexdigest()
        ns['rgrid'].__defaults__=(2000*rung,)
        for foot in ['canonical','alt']:
            witness=next(v for v in saved['dwarf_evaluations'].values() if v['name']=='Andromeda IX' and v['footing']==foot and abs(v['mass']-297187.1284574018)<1e-6)
            dwarf=next(d for d in ns['rows'] if d['name']==witness['name']);obj=ns['Dwarf'](dwarf,witness['width']);a0=ns['A0SI'][foot]*ns['CONV']
            value=float(obj.sigma(witness['mass'],a0,ns['GEV']['E1'](dwarf,a0),'R'));del obj
            error=abs(value/witness['sigma']-1);ok=error<=1e-8
            rows.append(dict(index=index,rung=rung,footing=foot,mass=witness['mass'],width=witness['width'],stored_sigma=witness['sigma'],replayed_sigma=value,relative_difference=error))
            checks.append(dict(name=f'p{index}_{foot}_r{rung}_replay',passed=ok))
pairs=[]
for index in [91,92]:
 for foot in ['canonical','alt']:
    a,b=[next(r['replayed_sigma'] for r in rows if r['index']==index and r['footing']==foot and r['rung']==k) for k in [1,2]]
    change=abs(a/b-1);pairs.append(dict(index=index,footing=foot,relative_change=change,frozen_line=.01,label='UNDECIDED' if change>.01 else 'numerically within line'))
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),rows=rows,pairs=pairs,source_hashes={**E.hashes(),**{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),source,HERE/'FROZEN_CRITERIA.md']}},scope='Targeted replay only; no tolerance/grid change, no final FN6 verdict; kappa=1/2 FITTED; not theory closed')
def atomic(path,value):
    tmp=path.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
atomic(HERE/'main/dwarf_failure_replay.json',obj)
atomic(HERE/'main/dwarf_failure_replay_runtime.json',dict(seconds=time.time()-started,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],pairs=pairs),indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
