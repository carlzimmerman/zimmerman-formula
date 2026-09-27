#!/usr/bin/env python3
"""Validate this checkpoint's accepted evidence, not physical closure."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

root=Path(__file__).resolve().parents[2]
base=Path(__file__).resolve().parent
validator=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py')
manifest_paths=['vacuum/run_001/manifest.json','occupied/run_001/manifest.json','static/run1/manifest.json','transport/run_001/manifest.json']
records=[]
for rel in manifest_paths:
    p=base/rel
    r=subprocess.run(['python3',str(validator),str(p),'--root',str(root)],capture_output=True,text=True,timeout=30)
    assert r.returncode==0,(rel,r.stdout,r.stderr)
    records.append({'path':str(p.relative_to(root)),'exit_code':r.returncode,'validation':r.stdout.strip()})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lean=[]
for folder,src,rec,log in [('vacuum','ReciprocalVacuum20260926.lean','lean_attempt1.json','lean_attempt1.log'),('occupied','OccupiedBridge20260926.lean','lean_record.json','lean_attempt1.log')]:
    data=json.loads((base/folder/rec).read_text())
    assert data['exit_code']==0
    assert sha(base/folder/src)==data['source_sha256']
    assert sha(base/folder/log)==data['log_sha256']
    source=(base/folder/src).read_text(); output=(base/folder/log).read_text()
    assert not re.search(r'\b(sorry|admit|axiom)\b',source)
    assert 'sorryAx' not in output and 'error:' not in output
    axioms=re.findall(r'depends on axioms: \[([^\]]*)\]',output)
    for group in axioms:
        assert set(x.strip() for x in group.split(',')) <= {'propext','Classical.choice','Quot.sound'}
    count=len(re.findall(r'^theorem\s+',source,re.M))
    assert len(axioms)==count
    lean.append({'source':str((base/folder/src).relative_to(root)),'statements':count,'sha256':sha(base/folder/src),'axioms':'standard only','compiler_record':str((base/folder/rec).relative_to(root))})
missing=[]; checked=0
for p in base.rglob('*.md'):
    # Frozen source copies retain links relative to their original locations.
    if 'snapshots' in p.parts: continue
    prose=re.sub(r'\\\[.*?\\\]', '', p.read_text(), flags=re.S)
    for target in re.findall(r'\]\(([^)]+)\)',prose):
        if '://' in target or target.startswith('#'): continue
        target=target.split('#')[0]
        checked+=1
        resolved=(p.parent/target).resolve()
        if resolved==base/'verification.json': continue  # Produced below.
        if not resolved.exists(): missing.append([str(p.relative_to(root)),target])
assert not missing,missing
out={'manifests':records,'lean':lean,'lean_statement_count':sum(x['statements'] for x in lean),'local_links_checked':checked,'missing_links':missing,'scope':'Source/hash/manifest and accepted Lean-output verification only; mathematical audits remain separate.'}
(base/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'manifests':len(records),'lean_statements':out['lean_statement_count'],'local_links_checked':checked,'status':'passed'}))
