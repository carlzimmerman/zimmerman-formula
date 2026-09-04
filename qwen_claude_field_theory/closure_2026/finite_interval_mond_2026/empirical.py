#!/usr/bin/env python3
"""Frozen, one-triple-per-galaxy tests; empirical failure is a result, not a bug.

No kernel parameters are fitted. See CONTRACT.md for selection and non-claims.
The input log-error covariance is conditional: SPARC does not supply the full
inter-ring/baryonic covariance needed for a theory-level rejection test.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SEED, REPLICATES = 2026090401, 1999
KERNELS = ('mu_exp', 'nu_rar', 'simple', 'deep', 'newton')
KMS2_KPC = 1e6 / 3.0857e19


def select_triple(b, minimum_span=.5):
    """Select by baryonic input alone, never by observed g or a model residual."""
    b = np.asarray(b, float)
    if b.ndim != 1 or len(b) < 3 or np.any(~np.isfinite(b)) or np.any(b <= 0):
        raise ValueError('at least three finite positive baryonic accelerations')
    x = np.log10(b)
    lo, hi = int(np.argmin(x)), int(np.argmax(x))
    span = x[hi]-x[lo]
    if span < minimum_span:
        return None
    candidates = [i for i in range(len(b)) if i not in (lo, hi)]
    mid = min(candidates, key=lambda i: (abs(x[i]-(x[lo]+x[hi])/2), i))
    t = (x[mid]-x[lo])/span
    return (lo, mid, hi) if .25 <= t <= .75 else None


def contrasts(b, g, covariance):
    """Return (log endpoint ratio, log chord defect) and their joint covariance."""
    b, g, cov = np.asarray(b, float), np.asarray(g, float), np.asarray(covariance, float)
    if b.shape != (3,) or g.shape != (3,) or cov.shape != (3, 3):
        raise ValueError('three accelerations and a 3x3 log10-g covariance required')
    if np.any(~np.isfinite(b+g)) or np.any(b <= 0) or np.any(g <= 0) or np.any(np.diff(b) <= 0):
        raise ValueError('positive finite g and strictly increasing positive b required')
    if not np.all(np.isfinite(cov)) or not np.allclose(cov, cov.T, rtol=1e-12, atol=1e-15):
        raise ValueError('finite symmetric covariance required')
    if np.linalg.eigvalsh(cov).min() < -1e-12*max(np.max(np.abs(cov)), 1e-30):
        raise ValueError('positive semidefinite covariance required')
    t = np.log(b[1]/b[0])/np.log(b[2]/b[0])
    C = np.array([[-1., 0., 1.], [t-1., 1., -t]])
    return C @ np.log10(g), C @ cov @ C.T


def bootstrap_means(values, replicates=REPLICATES, seed=SEED):
    values = np.asarray(values, float)
    if values.ndim != 2 or len(values)<2 or not np.all(np.isfinite(values)) or replicates < 1:
        raise ValueError('at least two finite galaxy rows and positive replication count required')
    rng = np.random.default_rng(seed)
    weights = rng.multinomial(len(values), np.full(len(values), 1/len(values)), size=replicates)
    return (weights @ values)/len(values)


def load_catalog():
    sys.path.insert(0, str(ROOT/'hunt_2026'))
    from hunt_lib import read_master
    master = read_master()
    files = sorted((ROOT/'real_research/data/sparc_data').glob('*_rotmod.dat'))
    if not master or not files:
        raise ValueError('SPARC source data missing')
    catalog = []
    for path in files:
        name = path.stem.removesuffix('_rotmod')
        if name not in master:
            raise ValueError(f'rotmod galaxy absent from master table: {name}')
        data = np.loadtxt(path, ndmin=2)
        if data.shape[1] != 8:
            raise ValueError(f'expected eight rotmod columns: {path}')
        catalog.append({'name': name, 'data': data, 'master': master[name]})
    return catalog, [ROOT/'real_research/data/SPARC_Lelli2016c.mrt', ROOT/'hunt_2026/hunt_lib.py']+files


def make_rows(catalog, disk_ml=.5, radius_min=1., qmax=2, incmin=30., gas_min=0., a0=9.36e-11):
    from response_math import acceleration
    rows, excluded = [], {}
    def reject(name, reason):
        excluded[name] = reason
    for galaxy in catalog:
        name, d, m = galaxy['name'], galaxy['data'], galaxy['master']
        if m['Q'] > qmax or m['inc'] < incmin or m['Rdisk'] <= 0:
            reject(name, 'catalog_quality_inclination_or_scale_length')
            continue
        r, v, ev, vg, vd, vb = d[:, :6].T
        with np.errstate(divide='ignore', invalid='ignore'):
            gas = vg*np.abs(vg)/r*KMS2_KPC
            b = gas+(disk_ml*vd**2+1.4*disk_ml*vb**2)/r*KMS2_KPC
        mask = (np.all(np.isfinite(d[:, :6]), axis=1) & (r>0) & (v>0) & (ev>=0)
                & (r>=radius_min*m['Rdisk']) & np.isfinite(b) & (b>0))
        valid = np.flatnonzero(mask)
        if len(valid) < 6:
            reject(name, 'fewer_than_six_eligible_radii')
            continue
        picked = select_triple(b[valid])
        if picked is None:
            reject(name, 'insufficient_baryonic_span_or_middle_point')
            continue
        idx = valid[np.array(picked)]
        if gas_min > 0 and np.any(gas[idx]/b[idx] < gas_min):
            reject(name, 'gas_fraction_cut')
            continue
        bt, gt = b[idx], v[idx]**2/r[idx]*KMS2_KPC
        sigma_log = 2*ev[idx]/v[idx]/np.log(10.)
        observed, cov = contrasts(bt, gt, np.diag(sigma_log**2))
        predicted = {k: contrasts(bt, acceleration(bt, a0, k), np.zeros((3, 3)))[0].tolist()
                     for k in KERNELS}
        span = float(np.log10(bt[2]/bt[0]))
        rows.append({'name': name, 'indices_zero_based': idx.tolist(), 'r_kpc': r[idx].tolist(),
                     'b_m_s2': bt.tolist(), 'g_m_s2': gt.tolist(), 'v_kms': v[idx].tolist(),
                     'ev_kms': ev[idx].tolist(), 'sigma_log10g': sigma_log.tolist(),
                     'gas_fraction': (gas[idx]/bt).tolist(), 'span_dex': span,
                     'observed_D_J_dex': observed.tolist(), 'covariance_D_J_dex2': cov.tolist(),
                     'predicted_D_J_dex': predicted,
                     'replication_half': int(hashlib.sha256(name.encode()).hexdigest()[:2], 16)%2})
    return rows, excluded


def summarize(rows):
    if not rows:
        return {'status': 'insufficient_data', 'galaxies': 0}
    if len(rows) == 1:
        return {'status': 'single_galaxy_no_population_inference', 'galaxies': 1,
                'observed_mean_D_J': rows[0]['observed_D_J_dex'],
                'note': 'One galaxy cannot supply a population resampling uncertainty.'}
    obs = np.array([r['observed_D_J_dex'] for r in rows])
    cov = np.array([r['covariance_D_J_dex2'] for r in rows])
    span = np.array([r['span_dex'] for r in rows])
    boot_obs = bootstrap_means(obs)
    sigma = np.sqrt(np.maximum(cov[:, [0, 1], [0, 1]], 0))
    result = {'status': 'computed_descriptive_not_certified', 'galaxies': len(rows),
              'observed_mean_D_J': obs.mean(axis=0).tolist(),
              'observed_mean_percentiles_2p5_50_97p5': np.percentile(boot_obs, [2.5, 50, 97.5], axis=0).tolist(),
              'observed_median_secant_slope': float(np.median(obs[:, 0]/span)),
              'fraction_observed_secants_in_half_to_one': float(np.mean((obs[:, 0]>=span/2)&(obs[:, 0]<=span))),
              'fraction_observed_J_negative': float(np.mean(obs[:, 1]<0)),
              'catalog_error_only_two_sigma_violations': {
                  'secant_below_half': int(np.sum(obs[:, 0]+2*sigma[:, 0]<span/2)),
                  'secant_above_one': int(np.sum(obs[:, 0]-2*sigma[:, 0]>span)),
                  'J_above_zero': int(np.sum(obs[:, 1]-2*sigma[:, 1]>0))},
              'kernel': {}}
    losses = {}
    for kernel in KERNELS:
        pred = np.array([r['predicted_D_J_dex'][kernel] for r in rows])
        residual = obs-pred
        boot_resid = bootstrap_means(residual)
        losses[kernel] = residual**2
        result['kernel'][kernel] = {
            'predicted_mean_D_J': pred.mean(axis=0).tolist(),
            'mean_residual_D_J': residual.mean(axis=0).tolist(),
            'mean_residual_percentiles': np.percentile(boot_resid, [2.5, 50, 97.5], axis=0).tolist(),
            'rms_D_J': np.sqrt(np.mean(residual**2, axis=0)).tolist()}
    result['paired_mse_mu_exp_minus_rival'] = {}
    for k in KERNELS[1:]:
        delta = losses['mu_exp']-losses[k]
        boot = bootstrap_means(delta)
        result['paired_mse_mu_exp_minus_rival'][k] = {
            'mean_D_J': delta.mean(axis=0).tolist(),
            'percentiles_D_J': np.percentile(boot, [2.5, 50, 97.5], axis=0).tolist(),
            'fraction_bootstrap_positive_D_J': np.mean(boot>0, axis=0).tolist()}
    # These are conditional expected sensitivities, not observed significances.
    pred_e = np.array([r['predicted_D_J_dex']['mu_exp'] for r in rows])
    pred_r = np.array([r['predicted_D_J_dex']['nu_rar'] for r in rows])
    error_mean = np.sqrt(np.sum(sigma**2, axis=0))/len(rows)
    result['conditional_velocity_noise_only'] = {
        'mean_standard_error_D_J': error_mean.tolist(),
        'predicted_mean_exp_minus_rar_D_J': (pred_e-pred_r).mean(axis=0).tolist(),
        'note': 'No baryonic/inter-ring systematic covariance; not a total uncertainty.'}
    return result


def controls(rows):
    """Finite synthetic experiments; no physics certificate from a green flag."""
    from response_math import acceleration
    rng = np.random.default_rng(SEED+1)
    errors, rescale, covshift, permutation_residuals = [], [], [], []
    fake_samples, fake_sigma = [], []
    for row in rows:
        b, g = np.array(row['b_m_s2']), np.array(row['g_m_s2'])
        sg = np.array(row['sigma_log10g'])
        true = acceleration(b, 9.36e-11, 'mu_exp')
        pred, cov = contrasts(b, true, np.diag(sg**2))
        obs, _ = contrasts(b, g, np.diag(sg**2))
        expected = row['predicted_D_J_dex']['mu_exp']
        errors.append(np.max(np.abs(pred-expected)))
        vv, cc = contrasts(b, true/(1.37*1.11**2), np.diag(sg**2)+.07*np.ones((3, 3)))
        rescale.append(np.max(np.abs(vv-pred)))
        covshift.append(np.max(np.abs(cc-cov)))
        # Null is generated in log space; actual velocity-noise likelihood differs.
        draws = np.log10(true)[None, :]+rng.normal(size=(999, 3))*sg
        t = np.log(b[1]/b[0])/np.log(b[2]/b[0])
        C = np.array([[-1., 0., 1.], [t-1., 1., -t]])
        fake_samples.append(draws @ C.T-pred)
        fake_sigma.append(np.diag(cov))
        shuffled = rng.permutation(g)
        permutation_residuals.append(contrasts(b, shuffled, np.diag(sg**2))[0]-pred)
    if not rows:
        return {'status': 'insufficient_data'}
    mean_samples = np.mean(np.array(fake_samples), axis=0)
    expected_var = np.sum(fake_sigma, axis=0)/len(rows)**2
    ratio = np.var(mean_samples, axis=0, ddof=1)/expected_var
    # A constructive wrong-response mutant breaks both target shape properties.
    bm = np.array([1., 10., 100.])
    wrong, _ = contrasts(bm, [100., 10., 1.], np.eye(3))
    concave, _ = contrasts(bm, [1., 50., 100.], np.eye(3))
    checks = {'synthetic_exact_recovery': bool(max(errors)<1e-12),
              'coherent_distance_inclination_cancellation': bool(max(rescale)<1e-12),
              'common_mode_covariance_cancellation': bool(max(covshift)<1e-12),
              'conditional_noise_variance_recovery': bool(np.all((ratio>.8)&(ratio<1.2))),
              'reversed_force_mutant_violates_compression': bool(wrong[0]<1),
              'concave_mutant_violates_J_sign': bool(concave[1]>0)}
    return {'checks': checks, 'all_implementation_controls_pass': all(checks.values()),
            'conditional_noise_empirical_to_analytic_variance_ratio_D_J': ratio.tolist(),
            'conditional_noise_mean_residual_D_J': np.mean(mean_samples, axis=0).tolist(),
            'permuted_observed_force_rms_D_J': np.sqrt(np.mean(np.array(permutation_residuals)**2, axis=0)).tolist(),
            'note': 'Surrogate/negative controls, not empirical confirmations of the law.'}


def run():
    catalog, files = load_catalog()
    configs = {
        'primary': {}, 'low_stellar_ml': {'disk_ml': .3}, 'high_stellar_ml': {'disk_ml': .8},
        'high_quality': {'qmax': 1, 'incmin': 45.}, 'inner_half_scale': {'radius_min': .5},
        'outer_two_scales': {'radius_min': 2.}, 'gas_dominated': {'gas_min': .8},
        'alternative_a0': {'a0': 1.13e-10}}
    result = {'contract': 'CONTRACT.md', 'seed': SEED, 'replicates': REPLICATES,
              'catalog_galaxies': len(catalog), 'scenarios': {}}
    for name, config in configs.items():
        rows, excluded = make_rows(catalog, **config)
        result['scenarios'][name] = {'config': config, 'summary': summarize(rows), 'rows': rows,
                                     'exclusions': excluded}
        if name == 'primary':
            if not rows:
                raise ValueError('empty primary sample is not a completed test')
            result['controls'] = controls(rows)
            result['label_split_replication_not_blind'] = {
                str(half): summarize([r for r in rows if r['replication_half']==half]) for half in (0, 1)}
    result['input_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    result['non_claims'] = ['No global novelty or empirical discovery certificate.',
                           'No full relativistic or non-spherical AQUAL theory test.',
                           'No blind external dataset; SPARC already explored extensively.',
                           'No full error likelihood; stellar/baryonic and inter-ring systematics remain.',
                           'Common normalization cancellation does not remove radial warps or M/L gradients.']
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    serialized = json.dumps(result, indent=2, allow_nan=False)+'\n'
    if args.output:
        args.output.write_text(serialized)
        for name, scenario in result['scenarios'].items():
            s = scenario['summary']
            concise = {k: s[k] for k in ('status', 'galaxies', 'observed_mean_D_J',
                       'observed_mean_percentiles_2p5_50_97p5') if k in s}
            if 'kernel' in s:
                concise['kernel_rms_D_J'] = {k: v['rms_D_J'] for k, v in s['kernel'].items()}
            print(name, json.dumps(concise))
        print('Controls:', json.dumps(result['controls']))
    else:
        print(serialized, end='')
    return 0 if result['controls']['all_implementation_controls_pass'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
