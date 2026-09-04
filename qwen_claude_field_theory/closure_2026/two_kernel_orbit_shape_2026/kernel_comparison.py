#!/usr/bin/env python3
"""Scope audit of f21: paired galaxy scores with a0 profiled in BOTH laws.

These are descriptive unweighted log-residual MSEs, NOT chi-square tests,
likelihood ratios, Gaussian significances, or full AQUAL disk predictions.
Distance, inclination and stellar M/L remain fixed to hunt_lib's defaults.
"""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

from orbit_shape import acceleration


def compare_profiles(gbar, gobs, gid, loga_grid, replicates=999, seed=20260904):
    b, o = np.asarray(gbar, float), np.asarray(gobs, float)
    ids = np.asarray(gid)
    grid = np.asarray(loga_grid, float)
    if b.ndim != 1 or b.shape != o.shape or ids.shape != b.shape:
        raise ValueError('one equally sized vector per data field required')
    if np.any(b <= 0) or np.any(o <= 0) or not np.all(np.isfinite(b+o)):
        raise ValueError('positive finite accelerations required')
    if len(grid) < 3 or np.any(np.diff(grid) <= 0):
        raise ValueError('increasing profile grid required')
    names, ids = np.unique(ids, return_inverse=True)
    counts = np.bincount(ids)
    losses = {}
    fits = {}
    for kernel in ('mu_exp', 'nu_rar'):
        columns = []
        for la in grid:
            residual = np.log10(o/acceleration(b, 10**la, kernel))
            columns.append(np.bincount(ids, weights=residual**2)/counts)
        loss = np.array(columns).T
        losses[kernel] = loss
        mean = loss.mean(axis=0)
        i = int(np.argmin(mean))
        point = np.average(loss, axis=0, weights=counts)
        j = int(np.argmin(point))
        fits[kernel] = {'a0': float(10**grid[i]), 'mse_dex2': float(mean[i]),
                        'rms_dex': float(np.sqrt(mean[i])),
                        'optimum_at_boundary': i in (0, len(grid)-1),
                        'point_weighted_a0': float(10**grid[j]),
                        'point_weighted_rms_dex': float(np.sqrt(point[j]))}
    rng = np.random.default_rng(seed)
    # One common draw resamples whole galaxies, including ALL their radii;
    # each law is refitted on precisely the same draw. No independent bins.
    weights = rng.multinomial(len(names), np.full(len(names), 1/len(names)),
                              size=replicates)/len(names)
    boot = {k: weights @ v for k, v in losses.items()}
    delta = np.min(boot['mu_exp'], axis=1)-np.min(boot['nu_rar'], axis=1)
    return {'galaxies': len(names), 'points': len(b), 'fit': fits,
            'delta_mse_mu_minus_rar': fits['mu_exp']['mse_dex2']-fits['nu_rar']['mse_dex2'],
            'paired_delta_mse_percentiles': np.percentile(delta, [2.5, 50, 97.5]).tolist(),
            'bootstrap_fraction_delta_positive': float(np.mean(delta > 0)),
            'bootstrap_boundary_fraction': {k: float(np.mean(
                (np.argmin(v, axis=1) == 0) | (np.argmin(v, axis=1) == len(grid)-1)))
                for k, v in boot.items()},
            'profile_log10a0_bounds': [float(grid[0]), float(grid[-1])],
            'profile_grid_points': len(grid), 'replicates': replicates, 'seed': seed,
            'interpretation': 'Descriptive paired resampling; not a significance or theory rejection'}


def main():
    root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(root/'hunt_2026'))
    from hunt_lib import load_sparc, A0
    galaxies = load_sparc()
    gb = np.concatenate([g['gbar'] for g in galaxies])
    go = np.concatenate([g['gobs'] for g in galaxies])
    gid = np.concatenate([np.full(len(g['gbar']), i) for i, g in enumerate(galaxies)])
    valid = (gb > 0) & (go > 0) & np.isfinite(gb+go)
    gb, go, gid = gb[valid], go[valid], gid[valid]
    result = compare_profiles(gb, go, gid, np.linspace(-10.6, -9.4, 501))
    refined = compare_profiles(gb, go, gid, np.linspace(-10.6, -9.4, 1001), 99)
    result['refinement_1001_grid_change_in_full_sample_mse'] = {
        k: refined['fit'][k]['mse_dex2']-result['fit'][k]['mse_dex2'] for k in result['fit']}
    result['fixed_a0_equal_galaxy_rms'] = {}
    result['catalog_ceiling_audit'] = {}
    counts = np.bincount(gid)
    for footing, a in A0.items():
        result['fixed_a0_equal_galaxy_rms'][footing] = {
            k: float(np.sqrt(np.mean(np.bincount(gid, weights=
                np.log10(go/acceleration(gb, a, k))**2)/counts))) for k in result['fit']}
        above = go-gb > .66*a
        result['catalog_ceiling_audit'][footing] = {
            'a0': a, 'points_above_0.66a0': int(above.sum()),
            'galaxies_with_at_least_one_estimate_above': int(len(np.unique(gid[above]))),
            'maximum_catalog_gph_over_a0': float(np.max(go-gb)/a),
            'interpretation': 'Raw inferred accelerations, with observational/systematic errors; not true-force counterexamples'}
    files = [root/'hunt_2026/hunt_lib.py', root/'hunt_2026/f21_two_kernels_and_the_phantom_maximum.py',
             root/'real_research/data/SPARC_Lelli2016c.mrt']
    files += [root/'real_research/data/sparc_data'/f"{g['name']}_rotmod.dat" for g in galaxies]
    hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    result['input_hashes'] = hashes
    result['input_set_sha256'] = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    result['model_scope'] = ('Two algebraic kernels applied to disk catalog accelerations; '
        'fixed catalog distance/inclination and M/L=0.5 disk, 0.7 bulge. '
        'Neither replaces a non-spherical AQUAL/QUMOND forward solve.')
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
