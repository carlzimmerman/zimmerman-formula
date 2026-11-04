"""Bounded KT38 closure verifier; reads lanes, writes root summaries only.

No force solver is rerun. --write refreshes RESULTS/VERIFICATION; --check
requires exact agreement with the stored closure. All lane evidence is read-only.
"""
import argparse, hashlib, json, math, resource, signal, subprocess, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
VALIDATOR = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')
MANIFESTS = {
    'analytic/tests_001': 'completed',
    'mw/checks_001': 'completed',
    'mw/full_001': 'failed',
    'mw/full_002': 'completed',
    'mw/focused_001': 'completed',
    'cassini/run_001': 'completed',
    'cassini/focus_001': 'completed',
    'dwarfs/run_001': 'completed',
    'dwarfs/continuation_001': 'completed',
}
INITIAL = [.3, 1., 3., 5., 10.]
ADAPTIVE = [1.5, 1.75, 2., 2.25, 2.5]
FEET = ['canonical', 'alt']

def read(rel):
    return json.loads((BASE / rel).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build():
    states = []
    pins = {}
    for run, expected in MANIFESTS.items():
        path = BASE / run / 'manifest.json'
        m = json.loads(path.read_text())
        assert m['run']['status'] == expected, (run, m['run'])
        checked = subprocess.run([sys.executable, str(VALIDATOR), '--root', str(ROOT), str(path)],
                                 capture_output=True, text=True, timeout=15)
        assert checked.returncode == 0, (run, checked.stdout, checked.stderr)
        states.append(dict(run=run, status=expected, manifest_valid=True,
                           exit_status=m['run']['exit_status'], runtime_seconds=m['run']['runtime_seconds']))
        pins[str(path.relative_to(ROOT))] = sha(path)
        for item in m['outputs']:
            artifact = ROOT / item['path']
            pins[str(artifact.relative_to(ROOT))] = sha(artifact)
    assert read('mw/checks_001/results.json')['all_checks_pass']
    mw, solar, dwarf = {}, {}, {}
    profile_count = 0
    positive_infinite_h = {}
    for run, lengths in [('mw/full_002', INITIAL), ('mw/focused_001', ADAPTIVE)]:
        d = read(run + '/results.json')
        assert d['selected_indices'] == list(range(1375)) and len(d['cells']) == 1375
        assert set(d['footings']) == set(FEET)
        null_count = 0
        for foot in FEET:
            scans = d['footings'][foot]['scans']
            assert [s['ell_kpc'] for s in scans] == lengths
            for scan in scans:
                rows = scan['rows']; assert len(rows) == 1375
                passed, strict = [], []
                for index, row in enumerate(rows):
                    assert row['index'] == index and row['cell'] == d['cells'][index]
                    q = row['corrected']; flags = [q[k] for k in ['L1', 'L2a', 'L2b', 'L3']]
                    assert q['all_four'] == all(flags)
                    if q['all_four']: passed.append(index)
                    if q['all_four'] and q['Lh']: strict.append(index)
                    if q['h'] is None:
                        assert q['h_status'] == 'positive infinity: fitted log-K slope is nonnegative' and not q['Lh']
                        null_count += 1
                    profile_count += 1
                sm = scan['summary']
                assert sm['pass_indices'] == passed and sm['n_pass'] == len(passed)
                assert sm['n_strict'] == len(strict) and sm['n_tested'] == 1375
                assert not passed
                mw[foot, scan['ell_kpc']] = dict(pass_count=len(passed), strict_intersection_count=len(strict),
                    population=1375, best_D=sm['best_D'], best_D_index=sm['best_D_index'], source=run)
        positive_infinite_h[run] = null_count
    assert profile_count == 27500
    for run, lengths in [('cassini/run_001', INITIAL), ('cassini/focus_001', ADAPTIVE)]:
        d = read(run + '/results.json'); assert d['all_checks_pass']
        for foot in FEET:
            data = d['footings'][foot]
            points = data.get('physical_lengths', data)
            assert sorted(map(float, points)) == sorted(lengths)
            for ell, configs in points.items():
                for q in configs.values():
                    ratio = abs(q['Q2_signed_s_minus_2']) / 5.2e-27
                    assert math.isclose(ratio, q['x_ceiling'], rel_tol=2e-14)
                    assert q['cassini_pass'] == (ratio <= 1) and q['cassini_pass']
                q = configs['fine']
                solar[foot, float(ell)] = dict(pass_cut=q['cassini_pass'], Q2_s_minus_2=q['Q2_signed_s_minus_2'],
                    abs_Q2_over_ceiling=q['x_ceiling'], source=run, configuration='fine')
    negative_rows = []
    dwarf_configs = 0
    dwarf_checks = []
    for run, lengths in [('dwarfs/run_001', INITIAL), ('dwarfs/continuation_001', ADAPTIVE)]:
        d = read(run + '/results.json'); assert d['all_checks_pass'] and d['checks']['original_sample_exact']
        assert d['ells_kpc'] == lengths and len(d['sample']) == 24 and len(d['upsilon_grid']) == 41
        assert d['upsilon_grid'][0] == 1 and d['upsilon_grid'][-1] == 3
        sample = {r['name']: r for r in d['sample']}
        for ell in lengths:
            for foot in FEET:
                sets = []
                for resolution in ['coarse', 'fine', 'expanded']:
                    rows = d['cases'][resolution][str(ell)][foot]
                    assert len(rows) == 24 and {r['name'] for r in rows} == set(sample)
                    passed = []
                    for r in rows:
                        obj = sample[r['name']]
                        sigma = r['sigma']; assert len(sigma) == 41
                        assert r['observed_sigma'] == obj['obs'] and r['observed_error'] == obj['err']
                        good = any(abs(v-obj['obs']) <= 2*obj['err'] for v in sigma)
                        assert good == r['passed']
                        assert not r['invalid_variance_indices'] and all(v > 0 for v in r['variance'])
                        if good: passed.append(r['name'])
                        if resolution == 'fine':
                            dwarf_configs += 41
                            minimum = r['checks']['minimum_radial_total_gradient']
                            if minimum < 0:
                                negative_rows.append(dict(ell_kpc=ell, footing=foot, name=r['name'],
                                    minimum_total_gradient=minimum, virial_screen_pass=good))
                    sets.append(passed)
                assert sets[0] == sets[1] == sets[2]
                sm = d['summaries'][str(ell)][foot]
                assert sm['names_passing'] == sets[0] and sm['pass_count'] == len(sets[0])
                assert sm['plain_isolated_pass'] == 19
                dwarf[foot, ell] = dict(isolated_virial_screen_pass_count=len(sets[0]), sample_size=24,
                    upsilon_sample_count=41, plain_isolated_pass_count=19, primary_satellite_EFE_grade=None, source=run)
        dwarf_checks.append(dict(run=run, all_pass_sets_identical=True,
            maximum_sigma_grid_change_km_s=d['maximum_sigma_refinement_change'],
            maximum_relative_virial_disagreement=d['maximum_relative_virial_disagreement'],
            maximum_relative_energy_fd_disagreement=d['maximum_relative_energy_fd_disagreement']))
    assert dwarf_configs == 19680
    lengths = sorted(INITIAL + ADAPTIVE)
    rows = [dict(ell_kpc=ell, selection='initial' if ell in INITIAL else 'adaptive',
                 footings={foot: dict(mw=mw[foot, ell], cassini=solar[foot, ell], dwarfs=dwarf[foot, ell])
                           for foot in FEET}) for ell in lengths]
    results = dict(schema_version=1, route='KT38_weak_field_curvature', status='checkpoint_complete',
        verdict='No primary Milky Way pass in either footing at any of the ten sampled lengths; no joint tested candidate.',
        law=dict(x='|g|^2/a0^2', s='ell^2 H:H/a0^2', z='x+s^2', P='xQ(z)/z',
                 Q0=0, Qprime='simple_nu(sqrt(z))', fixed_exponent=2, universal_parameter='ell_kpc'),
        unchanged=['baryons', 'acceleration footings', 'observations', 'primary cuts', 'strict Lh cut'],
        initial_lengths_kpc=INITIAL, adaptive_lengths_kpc=ADAPTIVE, rows=rows,
        coverage=dict(mw_profiles=profile_count, solar_length_footing_pairs=20,
                      isolated_dwarf_configurations=dwarf_configs, dwarf_quadrature_grids=3),
        cassini_all_sampled_pass=True, mw_all_sampled_primary_fail=True,
        positive_infinite_h_encoding_counts=positive_infinite_h,
        isolated_dwarf_negative_force_rows=negative_rows,
        isolated_dwarf_checks=dwarf_checks,
        health_qualification='H=0 uniform-field improvement does not eliminate negative principal static contributions in tidal backgrounds; no dynamical-health conclusion.',
        preserved_failed_run=dict(path='mw/full_001', reason='Positive infinite h rejected by JSON serialization; canonical-only saved profiles. Replayed with explicit null+status encoding.'),
        limitations=['Ten discrete lengths are not a continuum exclusion.',
          'MW counts are conditional finite-grid results; no passing witness exists here to promote.',
          'Cassini uses the prescribed constant external field, zero external Newtonian Hessian and specified Gaussian-source limit; no full ephemeris fit.',
          'Dwarf counts are isolated spherical 41-Upsilon virial screens, not primary satellite EFE grades, continuous-Upsilon exclusions or equilibrium proofs.',
          'Negative local radial forces at some 5/10 kpc dwarf samples were disclosed without imposing a new retrospective cut.',
          'No relativistic completion or all-background dynamical health is established.'],
        next_route=dict(path='../KT39_power_curvature', status='active_by_parent_instruction',
                        construction='Explicit p interpolation z=x+s^p', outcome='not assumed'))
    documents = ['PLAN.md', 'README.md', 'verify.py', 'mw/REVIEW.md', 'mw/PROVENANCE_NOTES.md',
        'analytic/DERIVATION.md', 'analytic/SOLAR_DERIVATION_REVIEW.md', 'analytic/TIDAL_LINEAR_RESPONSE.md',
        'dwarfs/CHECKPOINT.json', 'dwarfs/CONTINUATION_CHECKPOINT.json', 'cassini/README.md']
    for rel in documents:
        path = BASE / rel; pins[str(path.relative_to(ROOT))] = sha(path)
    verification = dict(schema_version=1, all_checks_pass=True, scope='Closure aggregation and saved-profile arithmetic only; no field solve rerun.',
        command='python3 rebuild_2026_10_22/KT38_weak_field_curvature/verify.py --check',
        limits=dict(wall_alarm_seconds=120, cpu_seconds=100, randomness=False),
        manifest_count=len(states), completed_manifest_count=sum(x['status']=='completed' for x in states),
        preserved_failed_manifest_count=sum(x['status']=='failed' for x in states), manifests=states,
        source_sha256=pins, independent_mw_regrade='mw/REVIEW.md: all 27500 force profiles, flags and summaries match.',
        checks=dict(mw_raw_counts=True, cassini_ceiling_arithmetic=True, dwarf_raw_dispersion_cuts=True,
                    dwarf_pass_sets_stable_three_grids=True, original_failed_status_preserved=True))
    return results, verification

def main():
    signal.alarm(120)
    resource.setrlimit(resource.RLIMIT_CPU, (100, 100))
    ap = argparse.ArgumentParser(); group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true'); group.add_argument('--check', action='store_true')
    args = ap.parse_args()
    results, verification = build()
    payload = json.dumps(results, indent=2, allow_nan=False) + '\n'
    verification['results_sha256'] = hashlib.sha256(payload.encode()).hexdigest()
    if args.write:
        (BASE / 'RESULTS.json').write_text(payload)
        (BASE / 'VERIFICATION.json').write_text(json.dumps(verification, indent=2, allow_nan=False)+'\n')
    else:
        assert read('RESULTS.json') == results
        assert read('VERIFICATION.json') == verification
        assert sha(BASE/'RESULTS.json') == verification['results_sha256']
    print(json.dumps(dict(all_checks_pass=True, manifests=verification['manifest_count'],
        preserved_failed_runs=verification['preserved_failed_manifest_count'], lengths=len(results['rows']),
        mw_profiles=results['coverage']['mw_profiles'], dwarf_configurations=results['coverage']['isolated_dwarf_configurations'])))

if __name__ == '__main__':
    main()
