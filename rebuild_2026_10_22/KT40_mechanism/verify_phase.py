"""Validate retained KT40 provenance and reconstruct the mechanism verdict."""
import hashlib,json,math,subprocess,sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def read(path):return json.loads((HERE/path).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    records=[]
    for path in sorted(HERE.rglob('manifest.json')):
        r=subprocess.run([sys.executable,str(VALIDATOR),str(path),'--root',str(ROOT)],capture_output=True,text=True)
        records.append(dict(path=str(path.relative_to(HERE)),status=json.loads(path.read_text())['run']['status'],
                            valid=r.returncode==0,sha256=sha(path),message=r.stdout.strip(),error=r.stderr.strip()))
    assert len(records)==18 and all(r['valid'] for r in records)
    assert Counter(r['status'] for r in records)==dict(completed=14,failed=4)
    for path in ['mw/run_001/results.json','mw/hydro_002/results.json','mw/force_001/results.json',
                 'scaling/run_002/results.json','scaling/crossovers_001/results.json',
                 'efe/run_001/results.json','efe/low_001/results.json',
                 'efe/monopole_001/results.json','efe/monopole_low_001/results.json','efe/localize_001/results.json']:
        assert read(path)['all_checks_pass']
    force=read('mw/force_001/results.json');assert force['complete'] and len(force['cases'])==8
    examples={};profile_count=0
    for c in force['cases']:
        for point in c['points']:
            v=point['force_parts'];assert math.isclose(v['total'],v['Newton']+v['A']+v['B'],rel_tol=1e-9)
            if point['R_kpc']==12:
                assert v['total']<0 and all(p['potential_difference_gz']<0 for p in point['potential_differences'])
                if c['refine']==6:examples[c['footing']]=point
        profile_count+=sum(len(p['z_kpc']) for p in c['profiles'])
    assert profile_count==2384
    hydro=read('mw/hydro_002/results.json');gas={}
    for foot in ['canonical','alt']:
        c=next(c for c in hydro['cases'] if c['footing']==foot and c['refine']==5)
        positive=[j for j in c['jets'] if j['hydrostatic_barotropic_two_gas']['positive_compressibility_hydrostatic_closure']]
        negative=[j for j in c['jets'] if not j['hydrostatic_barotropic_two_gas']['positive_compressibility_hydrostatic_closure']]
        assert len(positive)==14 and len(negative)==1
        assert all(not j['hydrostatic_barotropic_two_gas']['high_k_growth_under_positive_compressibility'] for j in positive)
        assert (negative[0]['R_kpc'],negative[0]['Z_kpc'])==(12.,.3)
        gas[foot]=dict(restoring_points=14,negative_compressibility_points=1,
                       vertical_high_k_growth_at_restoring_points=0,
                       all_direction_audit='dynamics/hydro_audit_001/results.json')
    allrows=[]
    for path in ['efe/run_001/results.json','efe/low_001/results.json']:
        d=read(path);allrows+=d['cases']['fine']
        assert len(d['sample'])==4 and len(d['upsilon_grid'])==41
    assert len(allrows)==72
    iso={(r['name'],r['footing']):r['variance'] for r in allrows if r['eta']==0}
    external_count=negative_count=0
    for r in allrows:
        assert len(r['variance'])==41 and all(math.isfinite(v) for v in r['variance'])
        if r['eta']>0:
            assert all(v<b for v,b in zip(r['variance'],iso[r['name'],r['footing']]))
            external_count+=41;negative_count+=sum(v<0 for v in r['variance'])
        if r['name']=='Draco' and r['eta']==.01:assert all(v<0 for v in r['variance'])
    assert external_count==2624 and negative_count==1805
    local=read('efe/localize_001/results.json')['profiles']
    draco=next(r for r in local if r['name']=='Draco')
    terms=draco['total_variance_terms'];assert math.isclose(terms['Newton']+terms['A']+terms['B'],terms['total'],rel_tol=1e-12)
    scaling=read('scaling/run_002/results.json')
    for foot,r in scaling['solar'].items():
        assert r['asymptotic_relative_error']<2.4e-8
        assert abs(r['Q2_asymptotic_si']/r['Q2_stored_si']-1)<2.4e-8
    result=dict(power=1.125,ell_kpc=3.,
                verdict='Equations and mechanism identified. Primary MW/Cassini fits remain real, but the fixed law has numerical outward-force witnesses and negative prescribed-profile EFE virials; no viable complete physical mechanism established.',
                screening=dict(chi='(ell/L)^(9/4) (g/a0)^(1/4)',transition_length='ell (g/a0)^(1/9)',plummer_chi_mass_size='M^(1/4) a^(-11/4)'),
                solar=scaling['solar'],mw_outward_force_ref6=examples,mw_gas_completion=gas,
                efe=dict(distinct_configurations=2952,nonzero_field_configurations=external_count,
                         decreased_virial_configurations=external_count,negative_virial_configurations=negative_count,
                         draco_example=draco,scope='Fixed centered Plummer profiles and imposed uniform auxiliary fields; no actual satellite orbital environment or tides.'),
                general_obstruction=dict(statement='Local curvature energy with finite high-curvature limit approached from above somewhere implies positive Hessian susceptibility on some positive-density rank-one jet.',
                    consequence='Unbounded frozen pressureless high-k growth on some backgrounds; not a universal matter or relativistic no-go.',proof='dynamics/GENERAL_OBSTRUCTION.md'),
                unresolved=['Fundamental origin of parameters and microscopic response','New completion controlling curvature stress','Actual Galaxy-satellite field/tide embedding','General collisionless/MHD/relativistic dynamics'])
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    selected=['README.md','PLAN.md','RESULTS.json','mechanism_failures.png','mechanism_failures.pdf','FINAL_AUDIT.md',
              'scaling/README.md','scaling/DERIVATION.md','scaling/PROVENANCE_NOTES.md',
              'efe/README.md','efe/MECHANISM.md','dynamics/GENERAL_OBSTRUCTION.md',
              'dynamics/DERIVATION.md','dynamics/MW_FORCE_REVIEW.md','dynamics/EFE_REVIEW.md',
              'mw/HYDRO_PROVENANCE.md']
    out=dict(manifest_count=len(records),statuses=dict(Counter(r['status'] for r in records)),all_manifest_hash_checks_valid=True,
             records=records,counts=dict(efe_total=2952,efe_nonzero=2624,efe_negative_virial=1805,mw_force_models=8,mw_profile_samples=profile_count),
             superseded_completed_semantic_record='scaling/run_001: dimensional Q2 conversion defect; use run_002.',
             preserved_failed_records=['mw/hydro_001','scaling/refinement_001','dynamics/run_001','dynamics/run_002'],
             distinction='Hash-valid completed execution is separate from accepted mathematics, numerical accuracy, and physical viability.',
             visual_review='mechanism_failures.png inspected after restricting the nonnegative external-field axis; sign conventions and scope labeled.',
             sha256={name:sha(HERE/name) for name in selected})
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['manifest_count','statuses','all_manifest_hash_checks_valid','counts']}))


if __name__=='__main__':main()
