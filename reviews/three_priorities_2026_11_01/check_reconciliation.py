#!/usr/bin/env python3
"""Orthogonal coordinator checks of frozen TP01 finite evidence."""
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def twice_ranks(values):
    # Integer average ranks, independent of scipy.stats.rankdata.
    return [sum(2 for x in values if x < v) + sum(x == v for x in values) + 1
            for v in values]


def permutation_tail(x, y):
    n = len(x)
    a = [v - n - 1 for v in twice_ranks(x)]
    b = [v - n - 1 for v in twice_ranks(y)]
    observed = sum(u*v for u, v in zip(a, b))
    extreme = sum(abs(sum(u*v for u, v in zip(a, p))) >= abs(observed)
                  for p in itertools.permutations(b))
    return extreme, math.factorial(n)


def deleted_residual_skill(y, features):
    # PRESS identity checks explicit leave-one-out refits by a different path.
    x = np.column_stack([np.ones(len(y))] + features)
    q, r = np.linalg.qr(x, mode='reduced')
    residual = y - q @ (q.T @ y)
    leverage = (q*q).sum(axis=1)
    sse = float(np.sum((residual/(1-leverage))**2))
    null_sse = float(np.sum(((y-y.mean())*len(y)/(len(y)-1))**2))
    return 1-sse/null_sse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    evidence = json.loads((HERE/'spin_contraction/run_002/results.json').read_text())
    rows = evidence['rows']
    assert [v['seed'] for v in rows] == list(range(1, 10))
    assert evidence['controls_pass'] is True
    checks = {'nine_distinct_aligned_seed_records': True}
    for name, key in [('fQ_spin', 'spin'), ('fQ_concentration', 'pre_c')]:
        extreme, total = permutation_tail([v['f_Q'] for v in rows],
                                           [v[key] for v in rows])
        old = evidence['statistics'][name]
        assert extreme == old['extreme'] and total == old['permutations']
        checks[name+'_integer_permutation_reconstruction'] = True
    sy = np.log10([v['disc_S'] for v in rows])
    sx = np.log10([v['pre_S'] for v in rows])
    sl = np.log10([v['spin'] for v in rows])
    skills = {}
    for name, features in [('pre_S', [sx]), ('spin', [sl]),
                           ('pre_S_spin', [sx, sl])]:
        value = deleted_residual_skill(sy, features)
        assert abs(value-evidence['predictive']['log_final_S'][name]['skill']) < 1e-10
        skills[name] = value
    checks['leave_one_out_via_PRESS_identity'] = True
    error = max(abs(np.log10(v['no_S']*v['R_live'])-np.log10(v['disc_S']))
                for v in rows)
    assert error < 1e-12
    checks['same_epoch_joint_identity'] = True
    result = {
        'assertion_tested': 'Exact integer rank permutation tails for two predeclared nine-seed associations; three PRESS/LOO identities; same-epoch paired identity',
        'checks': checks, 'all_checks_pass': all(checks.values()),
        'PRESS_skills': skills, 'joint_identity_log_error': error,
        'non_claims': ['No independent particle simulation or cosmological population inference',
                       'The nine-seed data reduction is reviewed separately; these checks audit its reported statistics']}
    Path(args.out).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
