#!/usr/bin/env python3
"""Verify KT36 records and derive compact results from raw, pinned outputs."""
import hashlib,json,subprocess,sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')

def read(rel):return json.loads((HERE/rel).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    records=[]
    for p in sorted(HERE.rglob('manifest.json')):
        r=subprocess.run([sys.executable,str(VALIDATOR),str(p),'--root',str(ROOT)],capture_output=True,text=True)
        d=json.loads(p.read_text())
        records.append(dict(path=str(p.relative_to(HERE)),status=d['run']['status'],valid=r.returncode==0,
                            output=r.stdout.strip(),error=r.stderr.strip(),sha256=sha(p)))
    assert records and all(r['valid'] for r in records)
    grid=read('mw/universal_grid_001/results.json');ref=read('mw/universal_refine_001/results.json')
    results=dict(universal_length_kpc=3.,universal_grid={},universal_witnesses={},constitutive_models=[])
    count=0
    for foot,f in grid['footings'].items():
        results['universal_grid'][foot]=[]
        for s in f['scans']:
            assert len(s['rows'])==1375 and s['summary']['numerical_tail_gate_passed']
            n=sum(r['corrected']['all_four'] for r in s['rows']);assert n==s['summary']['n_pass']
            count+=len(s['rows'])
            results['universal_grid'][foot].append(dict(length_kpc=s['universal_width_kpc'],passes=n,strict=s['summary']['n_strict']))
        assert f and ref['footings'][foot]['all_refinements_pass']
        rows=ref['footings'][foot]['cases'];assert len(rows)==6
        chosen=next(x for x in rows if x['refine']==5)
        results['universal_witnesses'][foot]=dict(cell=ref['footings'][foot]['cell'],
                                                 scores=chosen['row']['corrected'],
                                                 max_negative_mass_fraction=max(x['negative_mass_fraction'] for x in rows))
    assert count==8250
    for name in ['constitutive_grid_001','constitutive_continuation_001','constitutive_edges_001']:
        d=read('mw/'+name+'/results.json')
        for c in d['cases']:
            if not c['numerical_gates_pass']:
                assert (c['footing'],c['epsilon'],c['response']['name'])==('canonical',.2,'cutoff_t1.52_p6')
                replacement=read('mw/constitutive_low_recheck_001/results.json')['cases'][0]
                assert (replacement['footing'],replacement['epsilon'],replacement['response'])==(c['footing'],c['epsilon'],c['response'])
                c=replacement
            assert c['n_tested']==1375 and c['numerical_gates_pass'] and c['n_pass']==0
            assert len(c['all_vc'])==1375 and sum(x['corrected']['all_four'] for x in c['full_scores'])==0
            results['constitutive_models'].append({k:c[k] for k in ['footing','epsilon','response','n_tested','n_L1_pass','n_pass','max_vc','best','dual_full_max_vc_error','min_rejected_L1_margin']})
    assert len(results['constitutive_models'])==14
    er=read('mw/edge_refine_001/results.json');assert er['all_selected_refinements_fail']
    results['closest_constitutive_refined']=next(x for x in er['cases'] if x['refine']==4)['row']['corrected']
    assert read('mw/constitutive_checks_002/results.json')['passed']
    results['universal_grid_state_count']=count
    results['constitutive_state_count']=sum(c['n_tested'] for c in results['constitutive_models'])
    results['additional_constitutive_resolution_evaluations']=1375
    results['interpretation']='Two-primary-check witness for one universal physical length; strict vertical-scale failure and severe isolated-dwarf deficit. No broadly viable theory or unrestricted family exclusion.'
    (HERE/'RESULTS.json').write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
    selected=['README.md','PLAN.md','RESULTS.json','mw_witnesses.png','mw_witnesses.pdf',
              'mw/universal_grid_001/results.json','mw/universal_refine_001/results.json',
              'mw/edge_refine_001/results.json','dwarfs/run_001/results.json',
              'dwarfs/review/run_001/results.json','alternative/UNIVERSAL_REVIEW.md',
              'alternative/TOTAL_PHANTOM_BOUND.md','universal_length/FRACTIONAL_REVIEW.md']
    out=dict(manifest_count=len(records),statuses=dict(Counter(r['status'] for r in records)),records=records,
             all_manifest_hash_checks_valid=True,
             retained_semantic_defects=['Original fractional contract p6 convention, corrected independent replay','First MW literal-controls contract count6 instead of10, corrected controls002'],
             superseded_failed_accuracy_run='response/refine_001',
             coverage=dict(universal_grid=count,distinct_constitutive_states=results['constitutive_state_count'],additional_constitutive_resolution_evaluations=1375,selected_universal_refinements=12,selected_constitutive_refinements=4),
             visual_review='mw_witnesses.png inspected; vertical profiles sorted by observed radii before rendering',
             sha256={f:sha(HERE/f) for f in selected},
             current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
             qualification='Execution/hash validation is separate from mathematical review and numerical acceptance; retained failed/superseded records are not promoted to successful evidence.')
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['manifest_count','statuses','all_manifest_hash_checks_valid','coverage']}))

if __name__=='__main__':main()
