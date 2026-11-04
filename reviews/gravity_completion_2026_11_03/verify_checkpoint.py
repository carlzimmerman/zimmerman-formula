"""Fresh archival validation only; never reruns or rewrites scientific jobs."""
import ast
import collections
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'VERIFICATION.json'
VALIDATOR=Path.home()/'.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py'


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()


def main():
    files=sorted(p for p in HERE.rglob('*') if p.is_file() and p!=OUT)
    hashes={p:sha(p) for p in files}
    byhash=collections.defaultdict(list)
    for p,h in hashes.items():byhash[h].append(str(p.relative_to(ROOT)))
    parsed_python=[];parsed_json=[]
    for p in files:
        if p.suffix=='.py':
            ast.parse(p.read_text(),filename=str(p));parsed_python.append(str(p.relative_to(HERE)))
        elif p.suffix=='.json':
            json.loads(p.read_text());parsed_json.append(str(p.relative_to(HERE)))
    records=[]
    for p in files:
        if p.name!='manifest.json':continue
        m=json.loads(p.read_text())
        proc=subprocess.run([sys.executable,str(VALIDATOR),str(p),'--root',str(ROOT)],capture_output=True,text=True,cwd=ROOT)
        differences=[]
        for item in m.get('input_artifacts',[]):
            q=Path(item['path']);q=q if q.is_absolute() else ROOT/q
            current=sha(q) if q.is_file() else None
            if current!=item['sha256']:
                differences.append(dict(path=item['path'],expected_sha256=item['sha256'],current_sha256=current,
                                        exact_preserved_sources=byhash.get(item['sha256'],[])))
        records.append(dict(path=str(p.relative_to(HERE)),sha256=hashes[p],claim_id=m.get('claim_id'),
                            recorded_status=m.get('run',{}).get('status'),validator_exit=proc.returncode,
                            validator_output=(proc.stdout+proc.stderr).strip(),historical_source_differences=differences))
    old_report=ROOT/'reviews/gravity_vacuum_production_2026_11_01/HANDOFF_VERIFICATION.json'
    old_pins=json.loads(old_report.read_text())['artifact_inventory']
    old_changes=[]
    for pin in old_pins:
        p=ROOT/pin['path']
        current=sha(p) if p.is_file() else None
        if current!=pin['sha256']:old_changes.append(dict(path=pin['path'],expected=pin['sha256'],current=current))
    status=collections.Counter(r['recorded_status'] for r in records)
    invalid=[r for r in records if r['validator_exit']]
    recovered=all(d['exact_preserved_sources'] for r in invalid for d in r['historical_source_differences'])
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    report=dict(checkpoint='TP06 gravity and production',verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                base_checkpoint='a5617b4742892d38b77382fd67540fba365b2993',assessment_head=head,
                scope='Fresh JSON/Python syntax, run status and input/output hash validation. Numerical runs are preserved; interpretation requires the linked derivations/reviews.',
                python_sources_parsed=len(parsed_python),json_files_parsed=len(parsed_json),
                run_status_counts=dict(status),manifest_records=records,
                manifest_validator_successes=len(records)-len(invalid),manifest_validator_differences=len(invalid),
                all_historical_source_differences_exactly_archived=recovered,
                original_TP01_to_TP05_artifacts_rechecked=len(old_pins),original_artifact_differences=old_changes,
                interpretation_guards={
                    'scalar_vacuum_is_not_complete_loop_SUGRA_spectrum':True,
                    'protected_81eV_is_prescription_not_verified_pole':True,
                    'leading_fixed_current_partial_lifetime_not_total_bound':True,
                    'radial_threshold_scan_not_global_exclusion':True,
                    'heated_equilibrium_static_failure_not_nonequilibrium_no_go':True,
                    'charged_stability_not_conserved_total_pair_number':True,
                    'unequal_coupling_maximum_holds_at_fixed_F_not_fixed_f':True,
                    'DE_residual_tuned_not_predicted':True,
                    'kappa_fitted_not_derived':True},
                supersession_notes=[
                    'Canonical initial45digit parameter printout is not a reproducible tiny-CC packet; run_highprecision and root independent reconstruction are preferred.',
                    'Protected physical81eV pole inference is not established; protected_review/REVIEW.md supplies exact Ward ambiguity and fixed-current partial-width bound.',
                    'Production DERIVATION_CURRENT.md and run_refresh are preferred to earlier scope/kinetic drafts; reviews preserve the corrected birth/H inequalities.',
                    'Hierarchy mass maximum is fixed-F_eff; HIERARCHY_CLARIFICATION.md resolves compact prose.',
                    'Root canonical_independent scope label contains a harmless99-field wording error; intended nonclaim is a full transverse spectrum proof. Model has98 real scalar coordinates before gauge removal.',
                    'Failed numerical/serialization/quadrature histories remain failed; exact historical sources are mapped when applicable.'],
                validator_sha256=sha(VALIDATOR),
                artifact_inventory=[dict(path=str(p.relative_to(HERE)),sha256=hashes[p],bytes=p.stat().st_size) for p in files])
    OUT.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('python_sources_parsed','json_files_parsed','run_status_counts','manifest_validator_successes','manifest_validator_differences','original_TP01_to_TP05_artifacts_rechecked')},indent=2))
    print('Earlier artifact differences:',len(old_changes))
    print('Historical changed sources exactly archived:',recovered)
    for r in invalid:print(r['path'],r['recorded_status'],r['validator_output'])
    assert all(r['validator_exit']==0 for r in records if r['recorded_status']=='completed'), 'Completed record has stale/invalid provenance'
    assert recovered, 'A changed historical source has not been recovered'


if __name__=='__main__':main()
