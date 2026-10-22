#!/usr/bin/env python3
"""Read-only administrative verification; no PDE or mathematical test."""
from pathlib import Path
import hashlib,json,re,sys
here=Path(__file__).resolve().parent
root=next(p for p in here.parents if (p/'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json').is_file())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]
result=json.loads((here/'result.json').read_text())
contract=json.loads((root/'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json').read_text())
for key in contract['required_fields']:
    if key not in result: errors.append('missing required field: '+key)
for group in ['input_sha256','artifacts_sha256']:
    for path,want in result[group].items():
        p=root/path
        if not p.is_file() or digest(p)!=want: errors.append(group+': '+path)
inputs=json.loads((here/'input_sha256.json').read_text())
if inputs!=result['input_sha256']: errors.append('input maps differ')
task=root/'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-051.md'
if digest(task)!=result['task_sha256']: errors.append('task hash mismatch')
pins=re.findall(r'`([^`]+)` SHA256 `([0-9a-f]{64})`',task.read_text())
if len(pins)!=10: errors.append('ancestry count is not ten')
for path,want in pins:
    if result['input_sha256'].get(path)!=want: errors.append('ancestry pin absent/differs: '+path)
freeze=json.loads((here/'FREEZE.json').read_text())
for path,want in freeze['sha256'].items():
    p=root/path
    if not p.is_file() or digest(p)!=want: errors.append('freeze: '+path)
print(json.dumps({'ok':not errors,'errors':errors,'ancestry_pins':len(pins),
                  'input_count':len(inputs),'frozen_artifacts':len(freeze['sha256']),
                  'mathematical_computations':0,'writes_performed':0},indent=2))
sys.exit(bool(errors))
