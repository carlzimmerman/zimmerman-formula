#!/usr/bin/env python3
"""TP02 final provenance and interpretation-guard checks; no simulation reruns."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    records=[]
    for path in sorted(HERE.rglob('manifest.json')):
        result=subprocess.run([sys.executable,str(VALIDATOR),str(path),'--root',str(ROOT)],capture_output=True,text=True)
        data=json.loads(path.read_text())
        record={'path':str(path.relative_to(HERE)),'sha256':digest(path),
                'status':data['run']['status'],'current_hash_validation_exit':result.returncode,
                'validator_output':(result.stdout+result.stderr).strip()}
        assert result.returncode==0,record
        assert record['status']=='completed',record
        result_path=path.parent/'result.json'
        if result_path.exists():
            checks=json.loads(result_path.read_text()).get('checks',{})
            assert all(v for v in checks.values() if isinstance(v,bool)),str(result_path)
        records.append(record)
        print(record['path'],record['status'],'validated')
    assert len(records)==15,len(records)

    # Keep the comparator and the derived state separate in synthesis.
    comparator=[]
    for run in ['run_pressure_01','run_pressure_03','run_pressure_05','run_pressure_1']:
        data=json.loads((HERE/'rg_threshold'/run/'result.json').read_text())
        assert len(data['schemes'])==7
        for row in data['schemes']:
            assert row['witness_at_1p2']['negative_compressibility']
            assert row['boundary_U_s']>0 and row['boundary_Wss']>0
            comparator.append({'e':data['e'],'scheme':row['scheme'],'eta':row['eta']})
    relaxed=json.loads((HERE/'rg_threshold/run_relaxed_pressure/result.json').read_text())
    assert len(relaxed['cases'])==4
    assert all(c['witness_at_1p2']['negative_compressibility'] for c in relaxed['cases'])
    native=json.loads((HERE/'matter_coupling/run_occupied/result.json').read_text())
    assert len(native['cases'])==3
    for case in native['cases']:
        assert case['boundary']['w_ex']>.6
        samples=case['samples']
        at12=next(v for v in samples if v['X0_over_min']==1.2)
        at13=next(v for v in samples if v['X0_over_min']==1.3)
        assert at12['cs2_IR']>0 and at13['cs2_IR']<0

    # TP01's recorded sources and reviewed correction bytes remain unchanged.
    previous=ROOT/'reviews/three_priorities_2026_11_01'
    snapshot=json.loads((previous/'INPUT_SNAPSHOT.json').read_text())
    preserved=[]
    for item in snapshot['inputs']:
        assert digest(ROOT/item['snapshot'])==item['sha256']
        if not item['path'].startswith('covariant_push_'):
            assert digest(ROOT/item['path'])==item['sha256']
            preserved.append(item['path'])
    edits=json.loads((previous/'law_dictionary/EDIT_RECORD.json').read_text())['files']
    for item in edits:
        assert digest(ROOT/item['path'])==item['after_sha256']
        preserved.append(item['path'])
    old_verification=json.loads((previous/'VERIFICATION.json').read_text())
    for item in old_verification['review_pins']:
        assert digest(previous/item['path'])==item['sha256']

    review_paths=[
        'SOURCE_CHECKS.md','COORDINATOR_RG_AUDIT.md','PHASE_RESPONSE_AUDIT.md',
        'HEAVY_MATCHING_AUDIT.md','rg_derivation/IMPLEMENTATION_REVIEW.md',
        'rg_derivation/IMPLEMENTATION_REVIEW_INPUTS.json',
        'rg_derivation/OCCUPIED_REVIEW.md','rg_derivation/OCCUPIED_REVIEW_INPUTS.json',
        'matter_coupling/RG_MATCHING_REVIEW.md']
    review_pins=[{'path':p,'sha256':digest(HERE/p)} for p in review_paths]
    broken=[];link_count=0
    for path in HERE.rglob('*.md'):
        prose=re.sub(r'```[\s\S]*?```','',path.read_text())
        prose='\n'.join(line for line in prose.splitlines()
                         if not line.startswith(('    ','\t')))
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',prose):
            if target.startswith(('http:','https:','#','mailto:')):
                continue
            local=(path.parent/target.split('#')[0]).resolve()
            link_count+=1
            if not local.exists() and local!=HERE/'VERIFICATION.json':
                broken.append({'from':str(path.relative_to(HERE)),'target':target})
    assert not broken,broken
    structures=json.loads((HERE/'run_structures/result.json').read_text())
    assert structures['all_checks_pass']
    out={'checkpoint':'TP02','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'base_head':'40d43dbb8a9f1517e214302380f7659df7626e6a',
         'assessment_head':subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip(),
         'scope':'Fresh current-input manifest checks, source preservation, exact comparator/native interpretation guards, links and pinned mathematical reviews; not a complete physical validation.',
         'completed_v2_records':len(records),'records':records,
         'old_waterbag_scheme_witnesses':len(comparator),'finite_heavy_comparator_cases':4,
         'native_occupied_stencils':3,'coordinator_exact_structure_checks':len(structures['checks']),
         'native_1p2_positive_1p3_negative_guard':True,
         'TP01_recorded_source_and_review_bytes_unchanged':preserved,
         'review_pins':review_pins,'checked_local_links':link_count,
         'artifact_checker_adjustment':'Initial link regex included indented mathematical code; the checker now skips code blocks. No scientific artifact changed.',
         'no_production_or_external_job_started':True,
         'no_Git_mutation_by_TP02':True,
         'unresolved':['Direct finite two-loop vacuum graphs','Direct finite occupied component kinetic/current matching','Gauge/light/IR state and lifetime','Gravity and selected abundance'],
         'outcome':'Pressure obstruction persists in all computed weak partial matchings; actual state couplings derived; complete physical matching remains open.'}
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print('TP02 verified:',len(records),'completed records;',link_count,'local links;',len(comparator),'comparator witnesses; native-state guard passed.')


if __name__=='__main__':
    main()
