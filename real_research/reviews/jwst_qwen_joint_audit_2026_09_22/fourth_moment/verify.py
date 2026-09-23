"""Fresh-sample challenge to the frozen pair's full-spectrum degeneracy."""
import json
import runpy
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
simulate = runpy.run_path(str(ROOT/'real_research/reviews/bhstar_scattering_clock_2026_09_21/transport.py'))['simulate']


def estimate(x):
    return {'mean': float(x.mean()), 'se': float(x.std(ddof=1)/np.sqrt(len(x)))}


def summarize(x):
    a = 2*x['angular']
    b = 3*a*a
    m2, m4 = a.mean(), b.mean()
    influence = (b-m4)/m2**2-2*m4*(a-m2)/m2**3
    kurtosis = {'mean': float(m4/m2**2), 'se': float(influence.std(ddof=1)/np.sqrt(len(a)))}
    return {'width': estimate(a), 'fourth': estimate(b), 'kurtosis': kurtosis,
            'direct_fourth': estimate(x['v']**4),
            'paired_calibration': estimate(x['v']**4-b)}


def compare(a, b):
    out = {}
    for k in ('fourth','kurtosis','direct_fourth'):
        d = b[k]['mean']-a[k]['mean']
        se = float(np.hypot(a[k]['se'], b[k]['se']))
        out[k] = {'difference': d, 'se': se, 'z': d/se,
                  'relative_difference': d/a[k]['mean']}
    return out


def main():
    data = {'A': [], 'B': [], 'A_null': []}
    batches = []
    for i in range(3):
        seed = 9224000+10*i
        cases = {'A': simulate(200000,2.,0.,0.,'central',seed),
                 'B': simulate(200000,1/3,10.,0.4689264972650708,'central',seed+1),
                 'A_null': simulate(200000,2.,0.,0.,'central',seed+2)}
        batches.append({'seeds': [seed,seed+1,seed+2],
                        'comparison': compare(summarize(cases['A']),summarize(cases['B']))})
        for name, x in cases.items():
            data[name].append({k:x[k] for k in ('v','angular')})
    stats = {name:summarize({k:np.concatenate([x[k] for x in xs]) for k in ('v','angular')}) for name,xs in data.items()}
    effect, null = compare(stats['A'],stats['B']),compare(stats['A'],stats['A_null'])
    result = {'claim':'Finite fourth-moment and kurtosis comparison, not observational detectability or novelty',
              'parameters_frozen':True,'n_per_cloud':600000,'stats':stats,'batches':batches,
              'effect':effect,'identical_cloud_null':null,
              'checks':{'fourth_differs_over_5se':abs(effect['fourth']['z'])>5,
                        'kurtosis_differs_over_5se':abs(effect['kurtosis']['z'])>5,
                        'direct_fourth_differs_over_5se':abs(effect['direct_fourth']['z'])>5,
                        'null_within_4se':all(abs(x['z'])<4 for x in null.values()),
                        'paired_calibrations_within_6se':all(abs(x['paired_calibration']['mean'])<6*x['paired_calibration']['se'] for x in stats.values())}}
    (Path(__file__).parent/'certified/result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'effect':effect,'null':null,'checks':result['checks']},indent=2))


if __name__=='__main__':
    main()
