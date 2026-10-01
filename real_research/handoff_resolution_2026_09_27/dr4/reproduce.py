#!/usr/bin/env python3
"""Bounded XR22 controls and XR31 reproduction, immutable input mirror."""
import os, sys, pathlib, shutil, hashlib, json, ast, subprocess, time, datetime, platform
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=pathlib.Path(__file__).resolve().parent
MIR=OUT/'mirror'
LANE='real_research/cross_thread_review_2026_09_26'
ENV=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def setup():
    target=MIR/LANE; target.mkdir(parents=True,exist_ok=True)
    for src,dst,excluded in [(ROOT,MIR,{'real_research'}),(ROOT/'real_research',MIR/'real_research',{'cross_thread_review_2026_09_26','handoff_resolution_2026_09_27'}),(ROOT/LANE,target,set())]:
        for p in src.iterdir():
            q=dst/p.name
            if p.name in excluded or q.exists() or q.is_symlink(): continue
            if src==ROOT/LANE and p.name.startswith(('XR22_','XR31_')):
                if p.suffix=='.py' or p.name=='XR22_force_law_results.json': shutil.copy2(p,q)
            else: q.symlink_to(p)
    return target

def compare(a,b,path='',changes=None):
    changes=[] if changes is None else changes
    if path.endswith(('wall_s','production_wall_s')): return changes
    if isinstance(a,dict) and isinstance(b,dict):
        for k in a.keys()|b.keys():
            if k not in a or k not in b: changes.append([path+'/'+k,'missing'])
            else: compare(a[k],b[k],path+'/'+k,changes)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): changes.append([path,'length'])
        else:
            for i,(x,y) in enumerate(zip(a,b)): compare(x,y,path+f'/{i}',changes)
    elif a!=b: changes.append([path,a,b])
    return changes

def main():
    target=setup(); records=[]
    for mutation in (True,False):
        start=time.time(); env=dict(ENV,MUTATE=str(int(mutation)))
        log=OUT/('xr31_mutate.log' if mutation else 'xr31_main.log')
        with log.open('w') as f: p=subprocess.run([sys.executable,str(target/'XR31_k04_f6_stability.py')],cwd=MIR,env=env,stdout=f,stderr=subprocess.STDOUT)
        name='XR31_k04_f6_stability_results'+('_MUTATE' if mutation else '')+'.json'
        got=json.loads((target/name).read_text()); old=json.loads((ROOT/LANE/name).read_text())
        records.append(dict(script='XR31',mutate=mutation,rc=p.returncode,seconds=time.time()-start,differences=compare(got,old),checks=got.get('checks'),output_sha256=sha(target/name)))
    # Execute the exact main-body prefix K0-K3; stop before K4 rather than silently alter solver sizes.
    f=target/'XR22_force_law.py'; tree=ast.parse(f.read_text()); mainnode=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    cutoff=next(i for i,n in enumerate(mainnode.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='K4' for t in n.targets))
    mainnode.body=mainnode.body[:cutoff]
    tree.body=[n for n in tree.body if not isinstance(n,ast.If) or not any(isinstance(x,ast.Name) and x.id=='__name__' for x in ast.walk(n.test))]
    ast.fix_missing_locations(tree); os.environ.update(ENV); os.environ['MUTATE']='0'; sys.path.insert(0,str(target))
    ns={'__file__':str(f),'__name__':'xr22_bounded'}; exec(compile(tree,str(f),'exec'),ns)
    start=time.time(); ns['main'](); sys.stdout=sys.__stdout__
    got=ns['OUT']; old=json.loads((ROOT/LANE/'XR22_force_law_results.json').read_text())
    diffs=compare(got['numbers'],{k:old['numbers'][k] for k in got['numbers']})
    (OUT/'xr22_k0_k3.json').write_text(json.dumps(got,indent=2))
    records.append(dict(script='XR22 exact K0-K3 prefix',seconds=time.time()-start,differences=diffs,checks=got['checks']))
    (OUT/'bounded_records.json').write_text(json.dumps(records,indent=2)); print('records',[(r['script'],len(r['differences'])) for r in records])
if __name__=='__main__': main()
