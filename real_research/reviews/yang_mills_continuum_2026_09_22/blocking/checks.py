"""Exact finite checks of the Schur metric and bare-projector obstructions.

These check algebra/normalization. Universal statements use the adjacent proofs;
no Yang-Mills Hamiltonian or continuum limit is represented by these matrices.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
import argparse
import json
import sympy as s


def principal_minors(matrix):
    return [matrix.extract(ids, ids).det()
            for size in range(1, matrix.rows + 1)
            for ids in combinations(range(matrix.rows), size)]


parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
count = 0
for c0, c1, d, scale in product((0, 1, -1, 2), (0, 1, -1, 2),
                               (s.Rational(1, 2), 1, 3),
                               (s.Rational(1, 3), 1, 4)):
    d, scale = s.Rational(d), s.Rational(scale)
    C = s.Matrix([[c0, c1]])
    S = s.diag(0, scale)
    D = s.Matrix([[d]])
    A = S + C.T * D * C
    B = D * C
    H = A.row_join(B.T).col_join(B.row_join(D))
    G = s.eye(2) + C.T * C
    omega = s.Matrix([1, 0, -c0])
    assert H * omega == s.zeros(3, 1)
    assert H.rank() == 2
    gamma = s.trace(G.inv() * S)
    assert gamma > 0
    mass = 1 / (1 / gamma + 1 / d)
    assert mass.is_Rational
    complement = s.eye(3) - omega * omega.T / (omega.T * omega)[0]
    assert all(v >= 0 for v in principal_minors(H - mass * complement))
    count += 1

# Explicit disproof of the corresponding assertion with the metric omitted.
H = s.Matrix([[0, 0, 0], [0, 2, 1], [0, 1, 1]])
assert s.factor(H[1:, 1:].charpoly().as_expr()) == s.Symbol('lambda')**2 - 3*s.Symbol('lambda') + 1
assert (3 - s.sqrt(5)) / 2 < s.Rational(1, 2)

cell = s.Matrix([[1, -2], [-2, 4]])  # exactly 3 h
bare_rows = []
for cells in range(1, 7):
    H3 = s.zeros(2**cells)
    for index in range(cells):
        H3 += s.kronecker_product(s.eye(2**index), cell,
                                 s.eye(2**(cells-index-1)))
    ground = s.Matrix([1])
    for _ in range(cells):
        ground = s.kronecker_product(ground, s.Matrix([2, 1]))
    bare = s.zeros(2**cells, 1)
    bare[0] = 1
    witness = ground - 2**cells * bare
    assert H3 * ground == s.zeros(2**cells, 1)
    assert witness[0] == 0
    assert (witness.T * witness)[0] == 5**cells - 4**cells
    assert (witness.T * H3 * witness)[0] == cells * 4**cells
    bare_rows.append({'cells': cells, 'discarded_energy_upper':
                     str(s.Rational(cells * 4**cells, 3*(5**cells-4**cells)))})

# Exact rational scale sums; infinite-series bound derived analytically.
scale_count = 0
for L, sigma, q, depth in product((2, 3, 4), (F(1, 2), F(1), F(2)),
                                  (F(0), F(1, 3), F(2)), (1, 2, 8, 32)):
    finite = sum((sigma + q*r) / F(L)**r for r in range(1, depth+1))
    bound = sigma / (L-1) + q*L / (L-1)**2
    assert finite <= bound
    scale_count += 1

result = {'arithmetic': 'exact SymPy rational/algebraic and Fraction arithmetic',
          'schur_metric_cases': count, 'naive_metric_claim': 'refuted exactly at M=1',
          'bare_projector_cases': bare_rows, 'scale_budget_cases': scale_count,
          'status': 'PASS',
          'non_claims': ['No Yang-Mills projector construction or eliminated-mode estimate',
                         'No continuum limit or new mass-gap proof',
                         'Finite cases support algebra; written proof supplies universal comparison']}
args.output.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
