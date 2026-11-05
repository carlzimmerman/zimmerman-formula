"""Validate EFE records and independently audit finite virial claims."""
import hashlib,json,math,subprocess,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')

def read(name):return json.loads((HERE/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifests=[]
    for p in sorted(HERE.rglob('manifest.json')):
        c=subprocess.run([sys.executable,str(VALIDATOR),str(p),'--root',str(ROOT)],capture_output=True,text=True)
        d=json.loads(p.read_text());assert c.returncode==0 and d['run']['status']=='completed',(p,c.stderr)
        manifests.append(dict(path=str(p.relative_to(HERE)),status=d['run']['status'],sha256=sha(p),valid=True))
    assert len(manifests)==5
    initial=read('run_001/results.json');low=read('low_001/results.json')
    assert initial['all_checks_pass'] and low['all_checks_pass']
    baseline={(r['name'],r['footing']):r for r in initial['cases']['fine'] if r['eta']==0}
    states=0;negative=0;positive_eta=0;max_variance_shift=0.;max_relative_shift=0.;min_negative=0.;nearest_negative=0.;deltas=[]
    summaries=[]
    for d in [initial,low]:
        for i,r in enumerate(d['cases']['fine']):
            states+=len(r['variance']);assert len(r['variance'])==41
            invalid=[j for j,x in enumerate(r['variance']) if x<=0]
            assert invalid==r['invalid_variance_indices'];negative+=len(invalid)
            sig=[None if x<=0 else math.sqrt(x) for x in r['variance']]
            assert sig==r['sigma']
            passed=any(s is not None and abs(s-r['observed_sigma'])<=2*r['observed_error'] for s in sig)
            assert passed==r['passed']
            for label in ['coarse','expanded']:
                other=d['cases'][label][i]
                assert (r['name'],r['footing'],r['eta'])==(other['name'],other['footing'],other['eta'])
                diff=np.abs(np.array(r['variance'])-other['variance'])
                max_variance_shift=max(max_variance_shift,float(diff.max()))
                max_relative_shift=max(max_relative_shift,float((diff/np.maximum(np.abs(r['variance']),1)).max()))
                assert np.array_equal(np.asarray(r['variance'])>0,np.asarray(other['variance'])>0)
            if r['eta']>0:
                positive_eta+=len(r['variance']);delta=np.array(r['variance'])-baseline[r['name'],r['footing']]['variance']
                assert np.all(delta<0);deltas.extend(delta.tolist())
            summaries.append({k:r[k] for k in ['name','footing','eta','sigma_U1','sigma_U2','sigma_U3','passed','invalid_variance_indices']})
    assert states==2952 and positive_eta==2624 and negative==1805
    mono=[read('monopole_001/results.json'),read('monopole_low_001/results.json')]
    assert all(d['all_checks_pass'] and d['maximum_relative_difference']<1e-4 for d in mono)
    assert max_relative_shift<1e-4
    local=read('localize_001/results.json');assert local['all_checks_pass']
    selected=['PLAN.md','CONTINUATION_PLAN.md','DERIVATION.md','DERIVATION_v2.md','ERRATA.md','MECHANISM.md','README.md','calculate.py','calculate_low.py','verify_monopole.py','verify_monopole_low.py','localize.py','verify.py']
    out=dict(manifests=manifests,all_manifest_hash_checks_valid=True,distinct_configurations=states,nonzero_external_configurations=positive_eta,
        negative_total_virial_configurations=negative,all_sampled_external_variances_below_isolated=True,
        least_negative_variance_change_from_isolation=max(deltas),maximum_three_grid_variance_change=max_variance_shift,
        maximum_three_grid_scaled_variance_change=max_relative_shift,
        maximum_force_vs_homology_relative_difference=max(d['maximum_relative_difference'] for d in mono),
        maximum_actual_energy_derivative_relative_difference=max(x['relative_error'] for d in [initial,low] for x in d['controls']),
        numerical_acceptance_is_not_physical_acceptance='Negative virials are intentionally preserved as physical failures, although numerical identity/convergence checks passed.',
        qualification='Finite constant auxiliary external fields and fixed centered Plummer profiles. Scalar trace/orientation average, not actual satellite LOS/environment or an exclusion of all density profiles and tidal fields.',
        summaries=summaries,sha256={p:sha(HERE/p) for p in selected})
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:out[k] for k in ['distinct_configurations','nonzero_external_configurations','negative_total_virial_configurations','all_sampled_external_variances_below_isolated','maximum_three_grid_variance_change','maximum_force_vs_homology_relative_difference','maximum_actual_energy_derivative_relative_difference']}))

if __name__=='__main__':main()
