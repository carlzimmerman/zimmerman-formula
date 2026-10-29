"""Independent bounded HG2 statistic check; no physical model fitting or source writes.

Run from the repository root with the output JSON path as the sole argument.
The stored measured delta recovers the stored blue-lens reference exactly by
log10(g_ref)=log10(g_obs)-delta, so this tests the published finite statistic.
"""
import json
import math
from pathlib import Path
import statistics
import sys

INPUT = Path('rebuild_2026_10_22/HG2_kids_lowg_hot_gas/hg2_kids_lowg_hot_gas.json')
data = json.loads(INPUT.read_text())
rows = [row for row in data['groups'] if row['delta'] is not None]

def contrast(values):
    bins = {}
    for row, value in zip(rows, values):
        key = math.floor(math.log10(row['sigma']) / 0.1)
        bins.setdefault(key, {'BRIGHT': [], 'FAINT': []})[row['flag']].append(value)
    terms = []
    nb = nf = 0
    for key, arms in sorted(bins.items()):
        if arms['BRIGHT'] and arms['FAINT']:
            weight = min(len(arms['BRIGHT']), len(arms['FAINT']))
            difference = statistics.median(arms['BRIGHT']) - statistics.median(arms['FAINT'])
            terms.append({'sigma_bin': key/10, 'weight': weight, 'difference': difference})
            nb += len(arms['BRIGHT']); nf += len(arms['FAINT'])
    return sum(t['weight']*t['difference'] for t in terms)/sum(t['weight'] for t in terms), nb, nf, terms

lgbar = [math.log10(row['gbar']) for row in rows]
lgref = [math.log10(row['gobs']) - row['delta'] for row in rows]
measured = contrast([row['delta'] for row in rows])
assert abs(measured[0] - data['D']) < 1e-12
assert measured[1:3] == (data['n_bright'], data['n_faint'])

# Strictly increasing power-law F_q(g)=A*g^q. The normalization A cancels
# from D. Choose it to ensure F_q>=g on this entire finite sample, showing
# that even this extra sample constraint does not force the sign of D.
family = []
for q in (0.01, 0.1, 0.25, 0.5, 1.0):
    logA = max((1-q)*x for x in lgbar)
    logF = [logA + q*x for x in lgbar]
    D, nb, nf, terms = contrast([f-r for f, r in zip(logF, lgref)])
    family.append({'q': q, 'log10_A_SI': logA, 'D': D, 'strictly_increasing': q > 0,
                   'min_F_over_gbar': min(10**(f-x) for f,x in zip(logF,lgbar)),
                   'n_bright': nb, 'n_faint': nf, 'terms': terms})

# Exact family in the parent's observation: F=ref*(g/gstar)^(-epsilon).
# D=-epsilon*D(log gbar) by affine equivariance of each median. This says
# nothing about F's monotonicity or physical viability.
contrast_lgbar = contrast(lgbar)[0]
epsilon = 0.2
constructed = contrast([-epsilon*(x+12) for x in lgbar])[0]
assert abs(constructed + epsilon*contrast_lgbar) < 1e-12
result = {
    'assertion_tested': 'Whether negative HG2 D is impossible for every positive strictly increasing g_pred=F(gbar).',
    'n_supported': len(rows), 'D_measured_reproduced': measured[0],
    'shared_bright': measured[1], 'shared_faint': measured[2],
    'power_law_examples': family, 'contrast_log_gbar': contrast_lgbar,
    'reference_tilt_example': {'epsilon': epsilon, 'D': constructed},
    'counterexample_found': any(r['D'] < 0 and r['strictly_increasing'] and r['min_F_over_gbar'] >= 1-1e-12 for r in family),
    'non_claims': ['No physical validity, fit quality, field equation, or global asymptotic condition is established.',
                   'No existing model grade, frozen criterion, or source result is changed.',
                   'The constructed normalization is selected only for the finite sample and is not a proposed theory.']
}
assert result['counterexample_found']
Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ('D_measured_reproduced','contrast_log_gbar','counterexample_found')}))
print(json.dumps([{'q':r['q'],'D':r['D'],'min_F_over_gbar':r['min_F_over_gbar']} for r in family]))
