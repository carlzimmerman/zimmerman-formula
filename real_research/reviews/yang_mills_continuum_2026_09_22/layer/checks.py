"""Exact finite checks of YM-C3's model estimate and two counterexamples.

The analytic proofs are in PROOF.md. This code does not implement a
Yang-Mills vacuum, a continuum limit, or a weak-coupling mass-gap proof.
"""
import argparse
from itertools import product
import json
from pathlib import Path
import sympy as s


def tree_check(d, side):
    vertices = sorted(product(range(side), repeat=d), key=lambda z: (sum(z), z))
    index = {z: i for i, z in enumerate(vertices)}
    m, r = len(vertices), 3
    rotations = [s.eye(3), s.Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
                 s.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])]
    assert rotations[1] * rotations[2] != rotations[2] * rotations[1]
    edges = []
    transport = {}
    for z in vertices:
        for k in range(d):
            if z[k] + 1 < side:
                w = tuple(z[i] + (i == k) for i in range(d))
                rot = rotations[(index[z] + k) % len(rotations)]
                assert rot.T * rot == s.eye(r) and rot.det() == 1
                edges.append((z, w, rot))
                transport[z, w] = rot
    root = vertices[0]
    T = {root: s.eye(r)}
    for z in vertices[1:]:
        k = next(k for k in range(d) if z[k])
        parent = tuple(z[i] - (i == k) for i in range(d))
        T[z] = T[parent] * transport[parent, z]
    gradient = s.zeros(r * len(edges), r * m)
    for j, (z, w, rot) in enumerate(edges):
        gradient[r*j:r*(j+1), r*index[z]:r*(index[z]+1)] = s.eye(r)
        gradient[r*j:r*(j+1), r*index[w]:r*(index[w]+1)] = -rot
    average = s.zeros(r, r*m)  # Omit the harmless normalization sqrt(m).
    null_basis = s.zeros(r*m, r*(m-1))
    for z in vertices:
        average[:, r*index[z]:r*(index[z]+1)] = T[z]
    for j, z in enumerate(vertices[1:]):
        null_basis[:r, r*j:r*(j+1)] = -s.eye(r)
        null_basis[r*index[z]:r*(index[z]+1), r*j:r*(j+1)] = T[z].T
    assert average * null_basis == s.zeros(r, r*(m-1))
    assert average * average.T == m * s.eye(r)
    C = s.Rational(d*(side-1)*m, 2)
    matrix = null_basis.T * (C*gradient.T*gradient-s.eye(r*m)) * null_basis
    lower, diag = matrix.LDLdecomposition()
    assert lower * diag * lower.T == matrix
    assert all(diag[i, i] > 0 for i in range(diag.rows))
    return {'dimension': d, 'block_side': side, 'internal_components': r,
            'C': str(C), 'exact_positive_LDL_pivots': diag.rows,
            'background': 'specified noncommuting integer SO(3) transports'}


def flux_check(d, side):
    sites = list(product(range(side), repeat=d))

    def shift(z, i, step=1):
        return tuple((z[k]+step*(k == i)) % side for k in range(d))

    central = {(z, i): (-1)**sum(z[:i]) for z in sites for i in range(d)}
    velocity = {(z, i): 0 for z in sites for i in range(d)}
    zero = (0,)*d
    velocity[zero, 0] = 1
    velocity[shift(zero, 0), 1] = 1
    velocity[shift(zero, 1), 0] = -1
    velocity[zero, 1] = -1
    curl_square = 0
    plaquettes = 0
    for z in sites:
        assert sum(velocity[z, i]-velocity[shift(z, i, -1), i]
                   for i in range(d)) == 0
        for i in range(d):
            for j in range(i+1, d):
                sign = (central[z, i]*central[shift(z, i), j]
                        *central[shift(z, j), i]*central[z, j])
                assert sign == -1
                curl = (velocity[z, i]+velocity[shift(z, i), j]
                        -velocity[shift(z, j), i]-velocity[z, j])
                curl_square += curl**2
                plaquettes += 1
    for block in product(range(side//2), repeat=d):
        block_sites = [tuple(2*block[i]+offset[i] for i in range(d))
                       for offset in product(range(2), repeat=d)]
        assert all(sum(velocity[z, i] for z in block_sites) == 0
                   for i in range(d))
    assert curl_square == 20+8*(d-2)
    return {'dimension': d, 'torus_side': side, 'plaquettes': plaquettes,
            'all_plaquette_holonomies': '-I', 'divergence': 0,
            'all_component_block_averages': 0, 'curl_squared': curl_square,
            'magnetic_second_derivative_in_units_b_over_x':
            str(-s.Rational(curl_square, 4))}


def schur_check():
    values = []
    for H in (s.Matrix([[2, 1], [1, 2]]),
              s.Matrix([[4, s.sqrt(2), 0], [s.sqrt(2), 4, s.sqrt(2)],
                        [0, s.sqrt(2), 4]])):
        D, B = H[1:, 1:], H[1:, :1]
        C = D.inv()*B
        S = (H[:1, :1]-B.T*C)[0]
        G = 1+(C.T*C)[0]
        values.append(s.simplify(S/G))
    assert values == [s.Rational(6, 5), s.Rational(84, 29)]
    assert values[1] != 2*values[0]
    t, c = s.symbols('t c', real=True)
    assert s.diff(1+s.cos(t*c/2), t, 2).subs(t, 0) == -c**2/4
    return {'first_level': str(values[0]), 'second_level': str(values[1]),
            'twice_first_level': str(2*values[0]), 'harmonic_spacing': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = {'status': 'PASS', 'arithmetic': 'exact integer, rational, algebraic SymPy',
              'tree_comparisons': [tree_check(d, L) for d, L in
                                   ((1, 4), (2, 2), (2, 3), (3, 2))],
              'wilson_background_checks': [flux_check(d, M) for d, M in
                                           ((2, 4), (2, 6), (3, 4), (3, 6))],
              'quantum_schur_counterexample': schur_check(),
              'non_claims': ['No interacting Yang-Mills ground state computed',
                            'No volume-uniform nonlinear multiscale estimate proved',
                            'Finite checks do not prove the universal geometric lemma']}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
