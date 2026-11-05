#!/usr/bin/env python3
"""Resume the frozen run; read and validate controls only after full completion."""
import json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.chdir(HERE)
os.environ['PATH']=str(Path(sys.executable).parent)+os.pathsep+os.environ.get('PATH','')
from sy1 import tasks,tdir
status={'started':time.strftime('%Y-%m-%d %H:%M:%S'),'state':'search_running','python':sys.version.split()[0]}
def save():
 (HERE/'controls_completion.json').write_text(json.dumps(status,indent=2))
save()
r=subprocess.run(['/bin/bash','run_sy1.sh'])
if r.returncode:
 status.update(state='search_interrupted',exit=r.returncode);save();sys.exit(r.returncode)
missing=[]
for mode in ('planted','real','scrambled','mutate'):
 for t in tasks(mode):
  d=Path(tdir(str(HERE/'runs'),mode,t));p=d/'progress.json'
  if not (d/'DONE').is_file() or not p.is_file() or json.loads(p.read_text()).get('iters')!=1500:missing.append(str(d.relative_to(HERE)))
if missing:
 status.update(state='incomplete_searches',missing=missing);save();sys.exit(1)
status['state']='reading_controls';save()
for mode in ('planted','scrambled','mutate'):
 r=subprocess.run([sys.executable,'sy1_read.py',mode])
 if r.returncode:status.update(state='reader_failed',mode=mode,exit=r.returncode);save();sys.exit(r.returncode)
p=json.loads((HERE/'sy1_planted_read.json').read_text())
s=json.loads((HERE/'sy1_scrambled_read.json').read_text())
m=json.loads((HERE/'sy1_mutate_read.json').read_text())
status.update(state='controls_complete',finished=time.strftime('%Y-%m-%d %H:%M:%S'),planted={a:p[a]['all_recovered'] for a in 'TZ'},scrambled_stage1={a:s[a]['stage1'] for a in 'TZ'},mutation={a:m[a]['ok'] for a in 'TZ'})
status['controls_pass']=all(status['planted'].values()) and all(status['mutation'].values())
save();print(json.dumps(status,indent=2),flush=True)
sys.exit(0 if status['controls_pass'] else 1)
