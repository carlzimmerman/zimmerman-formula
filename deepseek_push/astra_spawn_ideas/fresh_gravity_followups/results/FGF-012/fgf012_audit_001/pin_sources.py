from pathlib import Path
import hashlib,json,re,datetime
root=Path.cwd(); out=root/'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-012/fgf012_audit_001'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
task=root/'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-012.md'
expected=dict(re.findall(r'- `([^`]+)` SHA256 `([0-9a-f]{64})`',task.read_text()))
man=json.loads((root/'campaign_fresh_gravity_astra/stage_04/cluster_observables/run_002/manifest.json').read_text())
for x in man['input_artifacts']:expected[x['path']]=x['sha256_after']
rows=[dict(path=p,expected=h,actual=sha(root/p)) for p,h in expected.items()]
for x in rows:x['pass']=x['actual']==x['expected']
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'all_pass':all(x['pass'] for x in rows)}
(out/'source_hash_check.json').write_text(json.dumps(result,indent=2)+'\n')
print('Source hashes:',len(rows),'all pass:',result['all_pass'])
assert result['all_pass']
