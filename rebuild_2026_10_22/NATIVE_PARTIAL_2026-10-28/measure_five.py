#!/usr/bin/env python3
"""Run the inherited estimator on the five completed seeds with unchanged estimator."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REB = HERE.parent
ROOT = REB.parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    source = REB / 'X48_native_cf_zoom/x48_analyze.py'
    a2path = REB / 'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json'
    snaps = {seed: HERE / f'completed/M1e12_s{seed}_ng64/snap_zf.npz' for seed in (1, 3, 7, 8, 9)}
    prior_path = HERE / 'measurement_003_four/results.json'
    paths = [prior_path, Path(__file__), HERE / 'FIVE_SEED_CRITERIA.md', source, a2path, *snaps.values()]
    before = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    ns = dict(__file__=str(source), __name__='x48_readonly')
    exec(compile(source.read_text(), str(source), 'exec'), ns)
    controls = {}
    for c in (4., 8.):
        n = 12000
        result = ns['measure'](ns['synthetic_nfw'](c, n, 1), 1/n,
            1/(4/3*math.pi)/(18*math.pi**2), 1e-4)
        controls[str(c)] = result
    nominal = lambda r: r.get('flag') == 'ok' and abs(r['cf']/4-1) < .15
    a2 = json.loads(a2path.read_text())['cf_by_mass']
    checks = dict(synthetic_c4=nominal(controls['4.0']),
        c8_rejected_as_c4=not nominal(controls['8.0']),
        A2_reference=all(abs(a2[k]-v) <= .01 for k,v in [('1e+12',11.63),('1e+13',8.22),('1e+14',7.31)]))
    runs = {}
    for seed, p in snaps.items():
        with np.load(p, allow_pickle=False) as z:
            meta = json.loads(str(z['meta']))
            rho = meta['Mf']/(4/3*math.pi*meta['qM']**3)*(1+meta['zf'])**3
            r = ns['measure'](z['x'], float(z['m']), rho, meta['eps'])
        r.update(seed=seed, ng=meta['ng'], N=meta['N'])
        if r.get('flag') == 'ok':
            r['L_proxy'] = 7.31*r['cf']/a2['1e+12']
        runs[str(seed)] = r
    prior = json.loads(prior_path.read_text())
    checks['prior_seeds_unchanged'] = all(runs[k] == prior['runs'][k] for k in ('1', '3', '7', '8'))
    checks['inputs_stable'] = all(sha(ROOT/p) == h for p,h in before.items())
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    result = dict(scope='Five completed seeds only; no ensemble estimate, confidence interval, convergence or observational grade',
                  checks=checks, controls=controls, A2=a2, runs=runs, input_sha256=before)
    (out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if all(checks.values()) else 1)


if __name__ == '__main__':
    main()
