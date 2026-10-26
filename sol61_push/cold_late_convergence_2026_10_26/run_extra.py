"""Seal then execute an explicitly requested post-run diagnostic or figure."""
import argparse,hashlib,json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('case',choices=['diagnostics','plot']);a=ap.parse_args();dest=P/(a.case+'_001' if a.case=='diagnostics' else 'figure_001');assert not dest.exists();contract=P/(a.case+'_contract.json');assert not contract.exists();d=json.loads((P/('temporal_contract.json' if a.case=='diagnostics' else 'analysis_contract.json')).read_text());files=set(d['execution_artifacts']);seen=set();sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def include(mf):
 if mf in seen:return
 seen.add(mf);files.add(str(mf.relative_to(ROOT)));m=json.loads(mf.read_text())
 for x in m['input_artifacts']+m['outputs']:
  f=ROOT/x['path'];assert sha(f)==x['sha256'];files.add(x['path'])
  if 'sha256_after' in x:assert x['sha256_after']==x['sha256']
  if f.name=='manifest.json':include(f)
for f in (['screen_001','temporal_001'] if a.case=='diagnostics' else ['analysis_001']):
 mf=P/f/'manifest.json';m=json.loads(mf.read_text());assert m['run']['status']=='completed' and m['run']['exit_status']==0;include(mf)
for f in ['run_extra.py',a.case+'.py','DIAGNOSTIC_ADDENDUM.md']+(['quadrature.py','test_quadrature.py'] if a.case=='diagnostics' else []):files.add(str((P/f).relative_to(ROOT)))
d['claim_id']='CCT022_'+a.case.upper();d['mathematics']['assertion_tested']=a.case+' per CCT022 contracts, no physical acceptance';d['randomness']={'used':False,'generator':'','seed':None};d['execution_artifacts']=sorted(files);contract.write_text(json.dumps(d,indent=2));runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py';cmd=['/opt/homebrew/bin/python3',runner,'--root',str(ROOT),'--contract',str(contract)]
for f in d['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(dest.relative_to(ROOT))]
for f in (['result.json'] if a.case=='diagnostics' else ['result.json','later_collapse.png']):cmd+=['--result',str((dest/f).relative_to(ROOT))]
cmd+=['--timeout','240','--max-output-bytes','1048576','--max-cpu-seconds','220','--max-threads','1','--','/usr/bin/python3',str(P/(a.case+'.py')),'--out',str(dest)];raise SystemExit(subprocess.call(cmd,cwd=ROOT))
