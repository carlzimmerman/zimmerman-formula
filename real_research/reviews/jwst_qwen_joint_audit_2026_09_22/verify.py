"""Independent analysis of Qwen's matched-pair suggestion, reusing pinned transport.

No new transport implementation is claimed. Fit h on training paths only;
freeze it, then evaluate full moments on independent validation paths.
"""
import json
import runpy
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
simulate = runpy.run_path(str(ROOT / 'real_research/reviews/bhstar_scattering_clock_2026_09_21/transport.py'))['simulate']


def stats(x):
    return {'mean': float(x.mean()), 'se': float(x.std(ddof=1)/np.sqrt(len(x))), 'n': len(x)}


def moments(x):
    # E[v^2 | spatial path] = 2 sum_i T_i(1-mu_i).
    # D is spatial-path measurable, so this also applies to the joint moment.
    return {'width': stats(2*x['angular']), 'joint': stats(2*x['angular']*x['delay']),
            'delay': stats(x['delay']), 'scatter_count': stats(x['n']),
            'doppler_calibration': stats(x['v']**2-2*x['angular'])}


def comparison(a, b):
    out = {}
    for k in ('width', 'joint', 'delay'):
        delta = b[k]['mean']-a[k]['mean']
        se = float(np.hypot(a[k]['se'], b[k]['se']))
        out[k] = {'delta': delta, 'se': se, 'z': delta/se,
                  'relative_delta': delta/a[k]['mean'],
                  'relative_abs_plus_1p96se': (abs(delta)+1.96*se)/a[k]['mean']}
    return out


def main():
    train_n = 1000000
    ref = simulate(train_n, 2., 0., 0., 'central', 9223100)
    cold = simulate(train_n, 1/3, 10., 0., 'central', 9223101)
    hot = simulate(train_n, 1/3, 10., 1., 'central', 9223101)
    assert np.array_equal(cold['delay'], hot['delay'])
    assert np.array_equal(cold['n'], hot['n'])
    slope = 2*(hot['angular']-cold['angular'])
    h = float((2*ref['angular'].mean()-2*cold['angular'].mean())/slope.mean())
    assert np.isfinite(h) and h >= 0
    train = {'n': train_n, 'seeds': [9223100, 9223101], 'q': 10., 'tau0': 1/3,
             'frozen_h': h, 'reference': moments(ref), 'cold': moments(cold),
             'width_slope': stats(slope)}
    del ref, cold, hot, slope
    validation, pools = [], {'reference': [], 'matched': [], 'cold': []}
    for i in range(3):
        seed = 9223200+10*i
        cases = {
            'reference': simulate(200000, 2., 0., 0., 'central', seed),
            'matched': simulate(200000, 1/3, 10., h, 'central', seed+1),
            'cold': simulate(200000, 1/3, 10., 0., 'central', seed+2)}
        measured = {k: moments(x) for k,x in cases.items()}
        validation.append({'seeds': [seed, seed+1, seed+2], 'moments': measured,
                           'comparison': comparison(measured['reference'], measured['matched'])})
        for k, x in cases.items():
            pools[k].append({key: x[key] for key in ('angular','delay','n','v')})
    pooled = {k: moments({key: np.concatenate([x[key] for x in xs])
                        for key in ('angular','delay','n','v')}) for k,xs in pools.items()}
    comp = comparison(pooled['reference'], pooled['matched'])
    neg = comparison(pooled['reference'], pooled['cold'])
    result = {'status': 'finite Monte Carlo evidence; no novelty or observational claim',
              'training': train, 'validation': validation, 'pooled': pooled,
              'comparison': comp, 'cold_negative_comparison': neg,
              'checks': {'width_equivalent_at_1pct_approx_95pct': comp['width']['relative_abs_plus_1p96se'] < .01,
                         'delay_equivalent_at_1pct_approx_95pct': comp['delay']['relative_abs_plus_1p96se'] < .01,
                         'joint_differs_over_5se': abs(comp['joint']['z']) > 5,
                         'cold_width_fails_1pct': abs(neg['width']['relative_delta']) > .01,
                         'doppler_calibrations_within_6se': all(abs(m['doppler_calibration']['mean']) < 6*m['doppler_calibration']['se'] for m in pooled.values())}}
    out = Path(__file__).parent/'certified/result.json'
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'h': h, 'checks': result['checks'], 'comparison': comp}, indent=2))


if __name__ == '__main__':
    main()
