"""Read-only numerical provenance verification and local artifact inventory."""
import sys
sys.dont_write_bytecode=True
import ast,json,hashlib,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def main():
    runs=[]
    for path in sorted(HERE.glob('run_*/manifest.json')):
        result=subprocess.run([sys.executable,str(VALIDATOR),str(path),'--root',str(ROOT)],capture_output=True,text=True,timeout=30)
        manifest=json.loads(path.read_text())
        runs.append(dict(path=str(path.relative_to(ROOT)),status=manifest['run']['status'],validator_exit=result.returncode,validator_stdout=result.stdout.strip(),validator_stderr=result.stderr.strip()))
    sources=[]
    for path in sorted(HERE.glob('*.py')):
        ast.parse(path.read_text(),filename=str(path));sources.append(str(path.relative_to(ROOT)))
    report=dict(base_checkpoint='a5617b4742892d38b77382fd67540fba365b2993',all_manifests_validate=all(r['validator_exit']==0 for r in runs),completed=sum(r['status']=='completed' for r in runs),preserved_failed=sum(r['status']=='failed' for r in runs),runs=runs,python_sources_parsed=sources,science_not_rerun=True)
    (HERE/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    inventory=[]
    for path in sorted(HERE.rglob('*')):
        if path.is_file() and path.name!='ARTIFACTS.json':
            inventory.append(dict(path=str(path.relative_to(ROOT)),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (HERE/'ARTIFACTS.json').write_text(json.dumps(dict(base_checkpoint=report['base_checkpoint'],artifacts=inventory),indent=2)+'\n')
    print(json.dumps(dict(all_manifests_validate=report['all_manifests_validate'],completed=report['completed'],preserved_failed=report['preserved_failed'],python_sources_parsed=len(sources),artifacts_hashed=len(inventory)),indent=2))
    assert report['all_manifests_validate']


if __name__=='__main__':main()
