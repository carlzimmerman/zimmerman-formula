#!/usr/bin/env python3
"""Necessary principal kinetic check from the unchanged quadratic action.

Lapse and shift are eliminated at stationary quadratic order.  Dust density
and its residual constraints are not reduced, so this is not a DOF count or a
complete no-ghost theorem.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path

import numpy as np
import sympy as sy

from branch_continuation import BranchBackground
from dark_energy_branches import inventory
from derive import construct
from transfer_evolve import Background


@lru_cache(maxsize=1)
def _block_evaluators():
    derived = construct()
    symbols = derived['s']
    action = derived['action'].subs({symbols['e']: 0, symbols['ed']: 0})
    velocities = [symbols[name] for name in ('zd', 'sigmad', 'radd', 'thetad')]
    auxiliaries = [symbols[name] for name in ('n', 'b')]
    velocity = sy.hessian(action, velocities)
    mixed = sy.Matrix([[sy.diff(action, x, y) for y in auxiliaries]
                       for x in velocities])
    auxiliary = sy.hessian(action, auxiliaries)
    parameters = sorted(velocity.free_symbols | mixed.free_symbols |
                        auxiliary.free_symbols, key=str)
    functions = [sy.lambdify(parameters, block, 'numpy', cse=True)
                 for block in (velocity, mixed, auxiliary)]
    return [str(x) for x in parameters], functions


def _value(v, name, k):
    if name == 'k':
        return k
    try:
        return v[name]
    except KeyError as error:
        raise KeyError('missing quadratic-action background value: '+name) from error


def kinetic_blocks(v, k):
    """Return reduced, velocity, mixed, and auxiliary Hessian blocks."""
    names, functions = _block_evaluators()
    arguments = [_value(v, name, k) for name in names]
    velocity, mixed, auxiliary = [np.asarray(fn(*arguments), dtype=float)
                                  for fn in functions]
    stationary_response = np.linalg.solve(auxiliary, mixed.T)
    reduced = velocity-mixed@stationary_response
    reduced = (reduced+reduced.T)/2
    return reduced, velocity, mixed, auxiliary


def kinetic(v, k):
    """Return the principal reduced matrix and spectrum without a rank claim."""
    matrix, _, _, _ = kinetic_blocks(v, k)
    eigenvalues = np.linalg.eigvalsh(matrix)
    tolerance = (100*matrix.shape[0]*np.finfo(float).eps*
                 max(1., float(np.linalg.norm(matrix, ord=np.inf))))
    return dict(matrix=matrix, eigenvalues=eigenvalues,
                null_tolerance=tolerance)


def _serial(result):
    return dict(matrix=result['matrix'].tolist(),
                eigenvalues=result['eigenvalues'].tolist(),
                null_tolerance=result['null_tolerance'])


def default_roots(k):
    roots = inventory()['roots']
    background = Background(.02)
    rows = []
    for root in roots:
        row = dict(H=root['H'], q=root['q'])
        try:
            v = background.evaluate([1., root['H'], root['q'], 0., .001, .01],
                                    extended=True)[0]
            row.update(kinetic=_serial(kinetic(v, k)))
        except (ValueError, KeyError, np.linalg.LinAlgError) as error:
            row['skipped'] = str(error)
        rows.append(row)
    return rows


def continuation(path, k):
    if path is None:
        return None
    if not path.exists():
        return dict(file=str(path), skipped='continuation file not found', branches=[])
    raw = json.loads(path.read_text())
    branches = raw if isinstance(raw, list) else raw.get('branches', raw.get('results', []))
    output = []
    for branch in branches:
        direction = branch.get('direction')
        saved = dict(direction=direction, samples=[])
        try:
            background = BranchBackground(direction)
        except (TypeError, ValueError) as error:
            saved['skipped'] = str(error)
            output.append(saved)
            continue
        for sample in branch.get('samples', []):
            row = {name: sample.get(name) for name in ('loga', 'a', 'H', 'q', 'tau')}
            try:
                a = float(sample['a'])
                state = [a, sample['H'], sample['q'], sample['tau'],
                         .001*a**-3, .01*a**-4]
                v = background.evaluate(state, extended=True)[0]
                row.update(kinetic=_serial(kinetic(v, k)))
            except (KeyError, TypeError, ValueError, np.linalg.LinAlgError) as error:
                row['skipped'] = str(error)
            saved['samples'].append(row)
        output.append(saved)
    return dict(file=str(path), branches=output)


def run(k=3000., continuation_file=None):
    return dict(k=float(k), roots=default_roots(k),
                continuation=continuation(continuation_file, k),
                velocity_order=['zd', 'sigmad', 'radd', 'thetad'],
                auxiliary_order=['n', 'b'],
                scope=('Necessary principal kinetic check after lapse/shift elimination; '
                       'dust density/residual constraints unreduced; no assumed rank, DOF count, '
                       'complete no-ghost theorem, or global branch claim.'),
                full_theory_status='OPEN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file', type=Path)
    parser.add_argument('--continuation-file', type=Path)
    parser.add_argument('--k', type=float, default=3000.)
    args = parser.parse_args()
    result = run(args.k, args.continuation_file)
    if args.result_file:
        args.result_file.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
