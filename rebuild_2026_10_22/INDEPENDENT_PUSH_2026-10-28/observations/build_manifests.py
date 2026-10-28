#!/usr/bin/env python3
"""Create v2 computation manifests from the recorded before/after hashes."""
from pathlib import Path
import json, hashlib, platform
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for suffix in ('','_MUTATE'):
    output=HERE/f'observations_results{suffix}.json'
    log=HERE/f'observations{suffix}.out'
    r=json.loads(output.read_text());run=r['run'];before=run['input_hashes'];after=run['input_hashes_after']
    assert before==after
    assert all(sha(ROOT/k)==h for k,h in after.items()),'stale input, rerun diagnostics'
    passed=all(r['checks'].values())
    command=['python3','-B',str((HERE/'recover_observations.py').relative_to(ROOT))]
    if suffix:command.append('--mutate')
    manifest=dict(schema_version=2,claim_id='OBSERVATIONS-2026-10-28'+suffix,
        repository=dict(commit=run['commit'],dirty=True),command=command,
        environment=dict(software=[dict(name='Python',version=run['python']),dict(name='numpy',version=run['numpy']),dict(name='scipy',version=run['scipy'])],
                         hardware=platform.system()+' '+platform.machine(),
                         launch_environment='PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1; nice -n15 requested but sandbox rejected priority change'),
        mathematics=dict(assertion_tested='Four-source hydrostatic beta-model GC projection diagnostic with aperture sensitivity; IC1613 entire-speed angle bound; 26-row CLoGS overlap and NGC4261 stored FAINT counterexample',
            coefficient_domain='IEEE754 float64 numerical integration; integer IDs and categorical associations',
            conventions='mu=.62; kT keV; forces SI; GC projected offsets log10(sigmaGC/sigmaX); whole-speed angle calculation optimistic when pressure support is fixed',
            inputs=list(before),bounds=dict(n_sluggs=4,n_clogs=26,n_group_scale_CLoGS=14,radial_grid_points=6000,projection_points=8001,one_thread=True),
            non_claims=['No unchanged GT1 or HO2 regrade','No new D, sample count, physical inclination likelihood or Z grade','No claim of exact isothermal HSE beyond source apertures','No universal theorem or gravity preference']),
        randomness=dict(used=False,generator='',seed=None),
        run=dict(started_at=run['started_at'],runtime_seconds=run['runtime_seconds'],exit_status=0 if passed else 1,status='completed' if passed else 'failed',
                 resource_limits=dict(memory_bytes=None,cpu_seconds=None,max_cores=None,max_threads=1),peak_RSS_GB=run['peak_RSS_GB'],
                 resource_observation='RSS checked below1GB; no OS memory/CPU cap; runtime seconds; priority request rejected'),
        outputs=[dict(path=str(output.relative_to(ROOT)),sha256=sha(output),kind='result'),dict(path=str(log.relative_to(ROOT)),sha256=sha(log),kind='log')],
        checks=[dict(name=k,passed=v) for k,v in r['checks'].items()],
        result='implementation and finite diagnostic verified in stated range' if passed else 'expected analytic-oracle mutation caught; no physical counterexample implied',
        residual_risks=['Published formal errors omit model systematics','GC anisotropy/density assumptions inherited and explicit','Global Xray aperture temperature is not a radial profile','Group gas at619kpc remains unknown','Source-table extraction audited separately in source_manifest.json'],
        input_artifacts=[dict(path=k,sha256=v,sha256_after=after[k]) for k,v in before.items()],
        declared_results=[str(output.relative_to(ROOT))])
    target=HERE/f'computation_manifest{suffix}.json'
    target.write_text(json.dumps(manifest,indent=2)+'\n')
    print(target.name,sha(target))
