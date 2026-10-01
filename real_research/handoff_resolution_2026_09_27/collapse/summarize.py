"""Reconcile completed lane jobs; produce table and evidence manifests. Does not modify research source lanes."""
import pathlib,json,hashlib,subprocess,sys,platform
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for execution in sorted((HERE/'runs').glob('*/execution.json')):
 meta=json.loads(execution.read_text());name=execution.parent.name;mut=name.endswith('_MUTATE');slug=name.removesuffix('_MUTATE')
 result=HERE/'mirror/campaign_fresh_gravity'/(slug+'_results'+('_MUTATE' if mut else '')+'.json')
 j=json.loads(result.read_text()) if result.exists() else {}
 cs=j.get('checks',{});fail=[k for k,v in cs.items() if not v.get('ok',True)];load=[k for k in fail if cs[k].get('load_bearing',True)]
 reads=json.loads((execution.parent/'reads.json').read_text()) if (execution.parent/'reads.json').exists() else []
 changed=[r['path'] for r in reads if r['before']!=r['after']]
 row={'script':slug,'mutation':mut,'rc':meta['exit_status'],'seconds':meta['runtime'],'checks':len(cs),'passed':len(cs)-len(fail),'load_bearing_failed':load,'reported_failed':[k for k in fail if k not in load],'read_inputs':len(reads),'read_inputs_changed':changed,'result_exists':bool(j)}
 original=ROOT/'campaign_fresh_gravity'/result.name
 if original.exists() and j:
  orig=json.loads(original.read_text())
  diffs=[]
  def diff(a,b,path=''):
   if isinstance(a,dict) and isinstance(b,dict):
    for k in sorted(set(a)|set(b)):
     if k not in a or k not in b:diffs.append(path+'/'+k)
     else:diff(a[k],b[k],path+'/'+k)
   elif isinstance(a,list) and isinstance(b,list):
    if len(a)!=len(b):diffs.append(path+'/length')
    else:
     for i,(v,w) in enumerate(zip(a,b)):diff(v,w,path+'/'+str(i))
   elif isinstance(a,(int,float)) and isinstance(b,(int,float)):
    if abs(a-b)>1e-9*max(1,abs(a),abs(b)):diffs.append(path)
   elif a!=b:diffs.append(path)
  # runtime is embedded in engine's scientific number dict; report, do not erase silently.
  diff(j.get('numbers',{}),orig.get('numbers',{}))
  row['source_number_differences']=diffs
 rows.append(row)
 artifacts=[execution,execution.parent/'stdout.txt',execution.parent/'stderr.txt',execution.parent/'reads.json']+([result] if j else [])
 manifest={'schema_version':1,'claim_id':slug+('_MUTATE' if mut else ''),'repository':{'commit':'48905ae11213afcb9ff1b7726530bb5dd1933fe3','dirty':True},'command':' '.join(meta['argv']),'environment':{'software':['Python '+meta['python'],'numpy/scipy/sympy from local runtime; CLASS runtime in class_provenance.json'],'hardware':meta['machine']},'mathematics':{'assertion_tested':'Reproduce named '+slug+' finite checks with original script unchanged','coefficient_domain':'floating point and symbolic identities as specified in source','conventions':'Source conventions unchanged; both acceleration footings, kappa=1/2 fitted','inputs':['source_inventory.json',str(execution.parent/'reads.json')],'bounds':{'original_source':slug+'.py','timeout_seconds':900,'sequential_jobs':True,'thread_limits':'cooperative; source may set 2'},'non_claims':['No universal proof, action or observational completion follows from exit status','Pipeline closure and all native library reads are not guaranteed by Python audit hook']},'randomness':{'used':slug in {'CFG2_A_principle','CFG3_sparc','CFG5_1_principle','CFG5_2_collapse','CFG5_3_sparc'},'generator':'numpy default_rng (PCG64), primary script; transitive source pinned separately','seed':{'CFG2_A_principle':3,'CFG3_sparc':12,'CFG5_1_principle':5,'CFG5_2_collapse':1,'CFG5_3_sparc':7}.get(slug)},'run':{'started_at':meta['started'],'runtime_seconds':meta['runtime'],'exit_status':meta['exit_status']},'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in artifacts if p.exists()],'checks':[{'name':k,'passed':v['ok'],'details':str(v.get('measured',''))} for k,v in cs.items()] or [{'name':'result produced','passed':False,'details':'No result JSON; inspect stderr'}],'result':('Deliberate mutation failed scientific checks' if mut and load else 'Finite results reproduced; inspect failed and reported checks' if j else 'Execution failed before scientific output'),'residual_risks':['Legacy manifest does not independently enforce caps; execution.json and audit read hashes provide supplemental provenance','Source-selected scope and statistics can differ from CFG4 target']}
 (execution.parent/'manifest.json').write_text(json.dumps(manifest,indent=2))
(HERE/'run_table.json').write_text(json.dumps(rows,indent=2))
lines=['| script | main checks | main rc | main scientific failures | mutation checks | mutation rc | named mutation failures |','|---|---:|---:|---|---:|---:|---|']
for slug in sorted(set(r['script'] for r in rows)):
 main=next((r for r in rows if r['script']==slug and not r['mutation']),None);mut=next((r for r in rows if r['script']==slug and r['mutation']),None)
 def fmt(r):return f"{r['passed']}/{r['checks']}" if r else 'pending'
 lines.append('| '+slug+' | '+fmt(main)+' | '+str(main['rc'] if main else '?')+' | '+(', '.join(main['load_bearing_failed']+['reported '+k for k in main['reported_failed']]) if main else '?')+' | '+fmt(mut)+' | '+str(mut['rc'] if mut else '?')+' | '+(', '.join(mut['load_bearing_failed']) if mut else '?')+' |')
(HERE/'RUN_TABLE.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
print('Changed reads',sum(len(r['read_inputs_changed']) for r in rows))
