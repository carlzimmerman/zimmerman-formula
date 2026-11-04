"""Validate immutable finite-run records and inventory the energy package."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
OWN=Path(__file__).resolve().parent
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 pending=[str(p.relative_to(ROOT)) for p in OWN.glob('run_*') if p.is_dir() and not (p/'manifest.json').exists()]
 if pending:raise RuntimeError('Unfinished/unrecorded run directories: '+repr(pending))
 records=[]
 for path in sorted(OWN.glob('run_*/manifest.json')):
  m=json.loads(path.read_text());proc=subprocess.run([sys.executable,str(VALIDATOR),str(path),'--root',str(ROOT)],capture_output=True,text=True);rp=path.with_name('result.json');result=json.loads(rp.read_text()) if rp.exists() else {};rss=result.get('peak_rss_bytes',result.get('max_rss_bytes'))
  records.append(dict(manifest=str(path.relative_to(ROOT)),manifest_sha256=digest(path),status=m['run']['status'],validation_passed=proc.returncode==0,validation_output=(proc.stdout+proc.stderr).strip(),runtime_seconds=m['run']['runtime_seconds'],resource_limits=m['run']['resource_limits'],result_peak_rss_bytes_as_recorded=rss,result_observation_runtime_seconds=result.get('runtime_seconds'),command=m['command'],inputs=len(m['input_artifacts']),results=[v for v in m['outputs'] if v['kind']=='result'],mathematical_checks=result.get('checks',{})))
 sources={str(p.relative_to(ROOT)):digest(p) for p in sorted(OWN.glob('*.py'))};contracts={str(p.relative_to(ROOT)):digest(p) for p in sorted(OWN.glob('contract*.json'))};out=dict(schema_version=1,scope='CC11 energy finite matched-update package; source hashes and per-run manifests control provenance.',base_shared_revision='dca7a564b31be47fe51049509ade99042a3a2afb',active_runs=[],source_sha256=sources,contract_sha256=contracts,records=records,all_records_validate=all(r['validation_passed'] for r in records),interpretation='Completed execution is not a physics claim; failed/resource-limited experimental routes remain recorded. See STATUS.md and DERIVATION.md.',errata=['Early fresh contract templates retained obsolete inherited dN inventory [5e-5,2.5e-5]; explicit stepmax, argv and saved accepted histories define actual coarse1e-4/fine5e-5. Old contracts/manifests are preserved.','A failed early record may lack final result RSS; no missing measurement is invented. Promoted completed controls retain measured macOS peak RSS in their result JSON.'])
 (OWN/'PROVENANCE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(records=len(records),all_records_validate=out['all_records_validate'],active_runs=[])));assert out['all_records_validate']
if __name__=='__main__':main()
