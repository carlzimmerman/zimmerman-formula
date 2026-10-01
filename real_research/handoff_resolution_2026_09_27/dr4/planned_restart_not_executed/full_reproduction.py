#!/usr/bin/env python3
import reproduce as R
import sys, json, subprocess, time, datetime, platform, resource
from pathlib import Path
T=R.setup()
inputs=[R.ROOT/R.LANE/f for f in ('XR22_common.py','XR22_force_law.py','XR22_prereg_statistic.py')]
inputs+=list((R.ROOT/'real_research/derivation_chain_2026').glob('FP*_results.json'))
inputs+=[R.ROOT/'prep_2026/gaia_dr4_prep'/f for f in ('wide_binary_pipeline.py','PREREGISTRATION_DR4.md','AMENDMENT12_HASH.txt')]
inputs+=list((R.ROOT/'qwen_claude_field_theory/closure_2026').glob('g03*_table*.json'))
# Snapshot working-tree hashes, not only HEAD.
hashes={str(p.relative_to(R.ROOT)):R.sha(p) for p in inputs}
meta={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R.ROOT,text=True).strip(),'python':sys.version,'hardware':platform.platform(),'input_hashes':hashes,'caps':{'numerical_threads':1,'XR22_NPROC':1,'hard_memory_limit':None,'hard_CPU_limit':None},'runs':[]}
(R.OUT/'full_records.json').write_text(json.dumps(meta,indent=2))
for slug in ('XR22_force_law','XR22_prereg_statistic'):
    for mutation in (True,False):
        name=slug+('_MUTATE' if mutation else '')
        argv=[sys.executable,str(T/(slug+'.py'))]; env=dict(R.ENV,MUTATE=str(int(mutation)),XR22_NPROC='1')
        start=time.time(); print('START',name,flush=True)
        with (R.OUT/(name+'_console.log')).open('w') as f: p=subprocess.run(argv,cwd=R.MIR,env=env,stdout=f,stderr=subprocess.STDOUT)
        result=T/(slug+'_results'+('_MUTATE' if mutation else '')+'.json')
        row={'name':name,'argv':argv,'mutate':mutation,'seconds':time.time()-start,'returncode':p.returncode,'output_exists':result.exists()}
        if result.exists():
            data=json.loads(result.read_text()); old=json.loads((R.ROOT/R.LANE/result.name).read_text())
            row.update(output_sha256=R.sha(result),committed_sha256=R.sha(R.ROOT/R.LANE/result.name),differences=R.compare(data,old),checks=data['checks'],verdict=data['verdict'])
        meta['runs'].append(row); meta['input_hashes_after']={str(p.relative_to(R.ROOT)):R.sha(p) for p in inputs}
        (R.OUT/'full_records.json').write_text(json.dumps(meta,indent=2)); print('END',name,row['seconds'],row['returncode'],len(row.get('differences',[])),flush=True)
        if p.returncode != (1 if mutation else 0): print('UNEXPECTED EXIT stopping',flush=True); break
