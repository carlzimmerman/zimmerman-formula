"""Retrospective completion audit. Does not reconstruct missing pre-run hashes."""
import json,hashlib,sys
from pathlib import Path
from sy1 import tasks,tdir
HERE=Path(__file__).resolve().parent
R={'scope':'Completion and stored-control-output audit; hashes observed after run, not proof of all original input provenance.','modes':{},'artifacts':{},'checks':{}}
for mode in ['planted','real','scrambled','mutate']:
 complete=0
 for task in tasks(mode):
  d=Path(tdir(str(HERE/'runs'),mode,task));pr=json.loads((d/'progress.json').read_text());done=json.loads((d/'DONE').read_text())
  assert pr['iters']==done['iters']==done['target']==1500
  assert pr['bf1_sha']==done['bf1_sha']=='1d9795d658b95a46'
  for f in [d/'progress.json',d/'DONE',d/'front.csv']:
   R['artifacts'][str(f.relative_to(HERE))]=hashlib.sha256(f.read_bytes()).hexdigest()
  complete+=1
 R['modes'][mode]={'expected':len(tasks(mode)),'complete':complete,'iters':1500}
P=json.loads((HERE/'sy1_planted_read.json').read_text());S=json.loads((HERE/'sy1_scrambled_read.json').read_text());M=json.loads((HERE/'sy1_mutate_read.json').read_text())
R['planted']={a:P[a]['all_recovered'] for a in 'TZ'};R['scrambled_stage1']={a:S[a]['stage1'] for a in 'TZ'}
R['mutation']={a:{k:M[a][k] for k in ['stage1','real_fronts_stage1','ok']} for a in 'TZ'}
R['checks']={'all_166_completed':sum(v['complete'] for v in R['modes'].values())==166,'planted_recovered':all(R['planted'].values()),'mutation_rejects_own_and_real':all(M[a]['ok'] and M[a]['stage1']==M[a]['real_fronts_stage1']==0 for a in 'TZ')}
for name in ['FROZEN_CRITERIA.md','AMENDMENT_A1.md','AMENDMENT_A2.md','sy1.py','sy1_export.py','sy1_data.py','sy1_leaves.py','sy1_read.py','sy1_planted_read.json','sy1_scrambled_read.json','sy1_mutate_read.json']:
 R['artifacts'][name]=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
Path(sys.argv[1]).write_text(json.dumps(R,indent=2));print(json.dumps({k:v for k,v in R.items() if k!='artifacts'},indent=2));assert all(R['checks'].values())
