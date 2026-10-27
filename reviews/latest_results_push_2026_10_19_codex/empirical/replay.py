#!/usr/bin/env python3
"""Replay the bounded packet in a fresh scratch directory, preserving all evidence."""
import json,pathlib,shutil,subprocess,sys,tempfile
source=pathlib.Path(__file__).resolve().parent
if '--help' in sys.argv:
 print('Usage: python3 replay.py [new-empty-parent-directory]\nCreates a fresh child directory and executes the three declared bounded runs.');raise SystemExit(0)
parent=sys.argv[1] if len(sys.argv)>1 else '/private/tmp'
root=pathlib.Path(tempfile.mkdtemp(prefix='zimmerman_empirical_replay_',dir=parent))
contracts=['contract.json','robustness_contract.json','verify_contract.json']
# Inputs produced by an earlier step are not copied; those steps regenerate them.
files=set(contracts)
for c in contracts:
 for f in json.loads((source/c).read_text())['execution_artifacts']:
  if not f.startswith('run/'):files.add(f)
for f in files:
 dest=root/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/f,dest)
runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py'
validator=str(pathlib.Path(runner).with_name('validate_manifest.py'))
for c,script,out in zip(contracts,['discriminate.py','robustness.py','verify.py'],['run','robustness_run','verify_run']):
 args=[sys.executable,runner,'--root',str(root),'--contract',str(root/c),'--output',out,'--result',out+'/result.json','--timeout','45','--max-output-bytes','131072','--max-cpu-seconds','40','--max-threads','1']
 for f in json.loads((root/c).read_text())['execution_artifacts']:args.extend(['--input',f])
 args+=['--',sys.executable,script];subprocess.run(args,check=True)
 subprocess.run([sys.executable,validator,str(root/out/'manifest.json'),'--root',str(root)],check=True)
print('Replayed evidence:',root)
