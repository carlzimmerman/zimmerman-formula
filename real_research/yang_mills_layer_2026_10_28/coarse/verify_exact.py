"""Exact algebra check for the one specified four-state counterexample.

This checks no Yang--Mills estimate, parameter range, or limiting theorem.
It uses rational arithmetic through SymPy; the analytic proof is in PROOF.md.
"""

import json
import sympy as s

A = s.Matrix([[2, -1, -1], [-1, 1, 0], [-1, 0, 1]])
B = s.Matrix([[0, -1, 1]])
D = s.Matrix([[4]])
C = D.inv() * B
S = A - B.T * C
G = s.eye(3) + C.T * C
K = s.Matrix([[2, -1, -1], [-1, s.Rational(13, 18), s.Rational(5, 18)],
              [-1, s.Rational(5, 18), s.Rational(13, 18)]])
V = s.Matrix.hstack(s.Matrix([1, 1, 1]), s.Matrix([-2, 1, 1]),
                   s.Matrix([0, 1, -1]))
assert V.det() != 0
assert S * V == V * s.diag(0, 3, s.Rational(1, 2))
assert G * V == V * s.diag(1, 1, s.Rational(9, 8))
assert K * V == V * s.diag(0, 3, s.Rational(4, 9))
assert G * K == S
assert S[1, 2] == s.Rational(1, 4)
assert K[1, 2] == s.Rational(5, 18)
assert K * s.ones(3, 1) == s.zeros(3, 1)
u = s.Matrix([0, 1, -1])
absu = s.Matrix([0, 1, 1])
assert (absu.T * K * absu)[0] > (u.T * K * u)[0]

# Recover blocks directly from the original four-state Dirichlet energy.
T = s.Matrix([[1, 0, 0, 1], [1, 0, 0, -1],
              [0, 1, 0, 0], [0, 0, 1, 0]])
mass = s.diag(s.Rational(1, 6), s.Rational(1, 6),
              s.Rational(1, 3), s.Rational(1, 3))
L = s.zeros(4)
for i, j, c in [(0, 2, 1), (1, 3, 1), (0, 1, s.Rational(1, 2))]:
    v = s.zeros(4, 1)
    v[i], v[j] = 1, -1
    L += c * v * v.T
assert T.T * mass * T == s.eye(4) / 3
assert T.T * L * T == A.row_join(B.T).col_join(B.row_join(D))
generator = mass.inv() * L / 3
assert generator * s.ones(4, 1) == s.zeros(4, 1)
assert all(generator[i, j] <= 0 for i in range(4) for j in range(4) if i != j)

print(json.dumps({
    "arithmetic": "exact rational",
    "tested_object": "single four-state conditional-expectation Schur reduction",
    "result": "all identities passed",
    "S_BC": str(S[1, 2]), "K_BC": str(K[1, 2]),
    "normalized_eigenvalues": ["0", "4/9", "3"],
    "supports": "non-Markov closure counterexample only",
}, indent=2))
