"""Rerun against restored exact cached inputs into a NEW named run folder."""
from pathlib import Path
import sys,json,hashlib,subprocess
root=Path(__file__).resolve().parents[4];f=Path(__file__).resolve().parent;rel=f.relative_to(root)
reg=json.loads((f/'sources.json').read_text());c=json.loads((f/'contract.json').read_text())
for item in reg['files']:
 p=root/item['path'];assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],f"restore exact input {p}"
exe=Path(reg['python_executable']['path']);assert hashlib.sha256(exe.read_bytes()).hexdigest()==reg['python_executable']['sha256'],'restore exact child Python binary'
name=sys.argv[1] if len(sys.argv)>1 else 'rerun';assert name.replace('_','').isalnum()
dest=rel/'runs'/name
runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py'
a=['python3',runner,'--root',str(root),'--contract',str(rel/'contract.json')]
for p in c['execution_artifacts']:a+=['--input',p]
a+=['--output',str(dest),'--result',str(dest/'results.json'),'--result',str(dest/'transfers.npz'),'--timeout','60','--max-output-bytes','200000','--max-cpu-seconds','45','--max-threads','1','--',str(exe),str(rel/'transfer_checks.py'),'--out',str(dest)]+sys.argv[2:]
raise SystemExit(subprocess.call(a,cwd=root))
