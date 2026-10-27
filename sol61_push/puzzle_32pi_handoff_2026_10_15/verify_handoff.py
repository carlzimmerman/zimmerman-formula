from pathlib import Path
import subprocess,json,hashlib,sys
root=Path(__file__).resolve().parents[2]
out=Path(__file__).resolve().parent
project=root/'fable_independent_2026/lean_2026'
validator=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py')
routes=['medium_cone','nonselection','curvature_tracking','tracking_force','nonlinear_tracking','backreaction','environment','handoff']
records=[]
for name in routes:
    folder=root/f'sol61_push/puzzle_32pi_{name}_2026_10_15'
    files=list(folder.glob('*.lean'))
    assert len(files)==1
    lean=files[0];digest=hashlib.sha256(lean.read_bytes()).hexdigest()
    old=folder/'lean_verification.json'
    if old.exists():
        assert json.loads(old.read_text())['source_sha256']==digest, 'Stale source '+str(lean)
    run=subprocess.run(['/opt/homebrew/bin/lake','env','lean',str(lean)],cwd=project,text=True,capture_output=True,timeout=120)
    log=run.stdout+run.stderr
    (out/f'{name}_lean_recheck.out').write_text(log)
    assert run.returncode==0 and 'sorryAx' not in log and 'error:' not in log,log
    count=log.count('depends on axioms:');assert count>0
    manifest=folder/'run/manifest.json'
    checked=False
    if manifest.exists():
        val=subprocess.run([sys.executable,str(validator),str(manifest),'--root',str(root)],capture_output=True,text=True,timeout=30)
        assert val.returncode==0,val.stdout+val.stderr
        checked=True
    records.append({'route':name,'lean_source':str(lean.relative_to(root)),'source_sha256':digest,'lean_exit_code':0,'axiom_reports':count,'manifest_validated':checked})
    print(name,count,'passed',flush=True)
result={'assessment_base':'283acbcffe1c6c4a5e8f9860f66e43c4e3808ab3','records':records,'total_lean_theorems':sum(x['axiom_reports'] for x in records),'validated_manifests':sum(x['manifest_validated'] for x in records),'limits':'Algebraic formalizations only; prose physical argument self-reviewed, not independently refereed'}
(out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('ALL',result['total_lean_theorems'],'Lean theorems passed;',result['validated_manifests'],'manifests validated',flush=True)
