from pathlib import Path
import json,hashlib,subprocess,sys,math,re
H=Path(__file__).resolve().parent
for p in sorted((H/'runs').glob('*/provenance.json')):
 r=json.loads(p.read_text())
 if r['status']=='running':continue
 out=p.parent; result=out/'results.json'; j=json.loads(result.read_text()) if result.exists() else {}
 paths=[x for x in out.iterdir() if x.is_file() and x.name!='manifest.json']
 stdout=(out/'stdout.txt').read_text(); times=re.findall(r'\[(\d+) s\]',stdout)
 m={'schema_version':1,'claim_id':'HR01-T/'+r['job'],'repository':{'commit':r['base_head'],'dirty':True},'command':r['argv'],'environment':{'software':['Python '+r['python'],'NumPy1.26.2','SciPy1.11.4','SymPy1.14.0','CLASS3.3.4.0 when reached; initially copied during bound main before G9 import'],'hardware':r['platform']},'mathematics':{'assertion_tested':'Exact unmodified XR36 source finite controls and observational proxies','coefficient_domain':'float64 and symbolic expressions where declared','conventions':'both source a0 footings; kappa fitted; source masks and baseline conventions unchanged','inputs':['mirror_sources.json',r['argv'][1]],'bounds':{'range':'full original script; no reduced range','timeout_seconds':r['wall_cap_seconds'],'threads':'source numerical-library environment sets 2; cooperative'},'non_claims':['Not a proof of full covariant action, derived kappa or joint data pass','Environment failures are not mathematical counterexamples']},'randomness':{'used':'web_lensing' in r['job'],'generator':'numpy default_rng PCG64','seed':19},'run':{'started_at':r['started_utc'],'runtime_seconds':r['elapsed_seconds'],'exit_status':r['exit_code']},'outputs':[{'path':str(x.relative_to(H)),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in paths],'checks':list(j.get('checks',{}).values()),'result':r['status']+'; '+str(j.get('verdict','no scientific JSON: see stderr')),'residual_risks':['v1 schema does not require input hashes; separate mirror source digest records retained','Bound main wrapper includes intentional queue-parent pause; final source elapsed seconds: '+str(times[-1] if times else 'not available'),'Copied runtime package provenance retained separately'],'source_hash_before':r['source_sha256'],'source_hash_after':hashlib.sha256(Path(r['argv'][1]).read_bytes()).hexdigest()}
 (out/'manifest.json').write_text(json.dumps(m,indent=2))
chosen={'action_main':'XR36_gate_action_verified','action_mutate':'XR36_gate_action_MUTATE_verified','bound_main':'XR36_bound_regions','bound_mutate':'XR36_bound_regions_MUTATE','web_main':'XR36_web_lensing_verified','web_mutate':'XR36_web_lensing_MUTATE','frame_main':'frame_tide_audit_scalar','frame_mutate':'frame_tide_audit_MUTATE_scalar','cmass_main':'cmass_source_gate_spectral','cmass_mutate':'cmass_source_gate_MUTATE_spectral','tide_main':'density_tide_pair_verified','tide_mutate':'density_tide_pair_MUTATE_verified'}
status={'base_head':'48905ae11213afcb9ff1b7726530bb5dd1933fe3','theory_status':'incomplete','runs':{},'mutation_comparisons':{}}
for k,d in chosen.items():
 p=H/'runs'/d; r=p/'results.json';m=p/'manifest.json'
 if r.exists():
  j=json.loads(r.read_text());status['runs'][k]={'path':str(p.relative_to(H)),'verdict':j['verdict'],'checks_passed':sum(v['ok'] for v in j['checks'].values()),'checks_total':len(j['checks']),'failed_checks':[key for key,v in j['checks'].items() if not v['ok']],'manifest_present':m.exists()}
 else:status['runs'][k]={'path':str(p.relative_to(H)),'status':'pending or failed before scientific output'}
for lane in ['action','bound','web','frame','cmass','tide']:
 paths=[H/'runs'/chosen[lane+x]/'results.json' for x in ['_main','_mutate']]
 if all(p.exists() for p in paths):
  a,b=[json.loads(p.read_text())['checks'] for p in paths]
  status['mutation_comparisons'][lane]={'pass_to_fail':[k for k in a.keys()&b.keys() if a[k]['ok'] and not b[k]['ok']],'baseline_already_failed':[k for k in a.keys()&b.keys() if not a[k]['ok'] and not b[k]['ok']]}
js=json.loads((H/'mirror_sources.json').read_text());changed=[];original=[]
for f,v in js['input_hashes'].items():
 p=H/'mirror'/f
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=v:changed.append(f)
 p=H.parents[2]/f
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=v:original.append(f)
status['input_freshness']={'files':len(js['input_hashes']),'mirror_changes':changed,'original_changes':original}
(H/'RUN_STATUS.json').write_text(json.dumps(status,indent=2));print(json.dumps(status,indent=2))
