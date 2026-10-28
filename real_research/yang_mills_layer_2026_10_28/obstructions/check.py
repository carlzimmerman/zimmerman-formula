#!/usr/bin/env python3
"""Exact finite checks for PROOF.md; all acceptance arithmetic is rational."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def conv(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] = out.get(i + j, F(0)) + x * y
    return out


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def mv(a, x):
    return [dot(row, x) for row in a]


def mm(a, b):
    return [[dot(row, col) for col in zip(*b)] for row in a]


def trans(a):
    return [list(row) for row in zip(*a)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def distance(a, b):
    ancestors = {}
    d = 0
    while a:
        ancestors[a] = d
        a //= 2
        d += 1
    d = 0
    while b not in ancestors:
        b //= 2
        d += 1
    return d + ancestors[b]


def rotor_checks():
    base = {-1: F(1, 2), 0: F(1), 1: F(1, 2)}
    cube = conv(conv(base, base), base)
    kernel = {i: 16 * a / 41 for i, a in cube.items()}
    kernel[0] += F(1, 41)
    expected = {0: F(1), -1: F(30, 41), 1: F(30, 41),
                -2: F(12, 41), 2: F(12, 41),
                -3: F(2, 41), 3: F(2, 41)}
    assert kernel == expected
    t = kernel[1]
    ratio = 2 * t * t
    assert ratio == F(1800, 1681) and ratio > 1
    cases = []
    for depth in range(6):
        leaves = list(range(2 ** depth, 2 ** (depth + 1)))
        # Independent combinatorial calculation over every ordered leaf pair.
        variance = sum((F(1, 2) * t ** distance(a, b)
                        for a in leaves for b in leaves), F(0))
        bracket = 1 + F(1, 2) * sum((ratio ** d for d in range(1, depth + 1)), F(0))
        formula = F(len(leaves), 2) * bracket
        assert variance == formula
        for leaf in leaves:
            counts = {d: sum(distance(leaf, b) == 2 * d for b in leaves)
                      for d in range(1, depth + 1)}
            assert counts == {d: 2 ** (d - 1) for d in range(1, depth + 1)}
        energy = F(len(leaves), 2)
        assert energy / variance == 1 / bracket
        cases.append({"depth": depth, "vertices": 2 ** (depth + 1) - 1,
                      "leaves": len(leaves), "ordered_pairs": len(leaves) ** 2,
                      "variance": str(variance), "energy": str(energy),
                      "rayleigh": str(energy / variance)})
    return {"fourier": {str(i): str(v) for i, v in sorted(kernel.items())},
            "branching_correlation_factor": str(ratio), "cases": cases}


def gaussian_checks():
    cases = []
    for n in range(1, 21):
        lap = [[F(2 if i == j else -1 if abs(i - j) == 1 else 0)
                for j in range(n)] for i in range(n)]
        solution = [F(i * (n + 1 - i), 2) for i in range(1, n + 1)]
        assert mv(lap, solution) == [F(1)] * n
        variance = sum(solution, F(0))
        assert variance == F(n * (n + 1) * (n + 2), 12)
        assert F(n) / variance == F(12, (n + 1) * (n + 2))
        # T is sqrt(2) times the orthogonal c/r coordinate change, in
        # interleaved (c_1,r_1,...,c_n,r_n) order. Everything stays rational.
        tmat = [[F(0)] * (2 * n) for _ in range(2 * n)]
        prec = [[F(0)] * (2 * n) for _ in range(2 * n)]
        for i in range(n):
            tmat[2*i][2*i] = tmat[2*i][2*i+1] = F(1)
            tmat[2*i+1][2*i] = F(1)
            tmat[2*i+1][2*i+1] = F(-1)
            prec[2*i][2*i] = F(1)
            for j in range(n):
                prec[2*i+1][2*j+1] = lap[i][j]
        assert mm(tmat, trans(tmat)) == [[2*x for x in row] for row in eye(2*n)]
        omega = [[x / 2 for x in row] for row in mm(mm(trans(tmat), prec), tmat)]
        squared = mm(omega, omega)
        for i in range(n):
            block = [row[2*i:2*i+2] for row in omega[2*i:2*i+2]]
            assert block == [[F(3, 2), F(-1, 2)], [F(-1, 2), F(3, 2)]]
            assert mv(block, [F(1), F(1)]) == [F(1), F(1)]
            assert mv(block, [F(1), F(-1)]) == [F(2), F(-2)]
        for i in range(2*n):
            for j in range(2*n):
                if abs(i//2 - j//2) > 1:
                    assert omega[i][j] == 0
                if abs(i//2 - j//2) > 2:
                    assert squared[i][j] == 0
                assert abs(omega[i][j]) <= 2
                assert abs(squared[i][j]) <= 4
        cases.append({"cells": n, "variance_of_sum_r": str(variance),
                      "energy": n, "rayleigh": str(F(n) / variance),
                      "conditional_pair_eigenvalues": ["1", "2"],
                      "potential_matrix_range_cells": 2})
    return cases


def schur_checks():
    mu = [F(1, 6), F(1, 6), F(1, 3), F(1, 3)]
    # Fine form matrix in point coordinates, built directly from conductances.
    lap = [[F(0)] * 4 for _ in range(4)]
    for i, j, c in [(0, 2, F(1, 3)), (1, 3, F(1, 3)), (0, 1, F(1, 6))]:
        lap[i][i] += c
        lap[j][j] += c
        lap[i][j] -= c
        lap[j][i] -= c
    fine = [[lap[i][j] / mu[i] for j in range(4)] for i in range(4)]
    assert mv(fine, [F(1)]*4) == [F(0)]*4
    assert all(fine[i][j] <= 0 for i in range(4) for j in range(4) if i != j)
    lift = [[F(1), F(1, 4), F(-1, 4)],
            [F(1), F(-1, 4), F(1, 4)],
            [F(0), F(1), F(0)],
            [F(0), F(0), F(1)]]
    # S and G are recomputed from J* fine J and J* J, with coarse mass 1/3.
    sl = mm(mm(trans(lift), lap), lift)
    s = [[3*x for x in row] for row in sl]
    weighted_lift = [[mu[i] * x for x in row] for i, row in enumerate(lift)]
    g = [[3*x for x in row] for row in mm(trans(lift), weighted_lift)]
    expected_s = [[F(2),F(-1),F(-1)], [F(-1),F(3,4),F(1,4)],
                  [F(-1),F(1,4),F(3,4)]]
    assert s == expected_s
    v, w, one = [F(0),F(1),F(-1)], [F(-2),F(1),F(1)], [F(1)]*3
    assert mv(s, v) == [x/2 for x in v]
    assert mv(g, v) == [F(9,8)*x for x in v]
    assert mv(s, w) == [3*x for x in w]
    assert mv(g, w) == w
    assert mv(s, one) == [F(0)]*3 and mv(g, one) == one
    assert mm(g, s) == mm(s, g)
    # Rational spectral projectors evaluate G^-1/2 S G^-1/2 exactly.
    k = [[3*w[i]*w[j]/dot(w,w) + F(4,9)*v[i]*v[j]/dot(v,v)
          for j in range(3)] for i in range(3)]
    assert k == [[F(2),F(-1),F(-1)], [F(-1),F(13,18),F(5,18)],
                 [F(-1),F(5,18),F(13,18)]]
    assert mm(g, k) == s
    abs_v = [abs(x) for x in v]
    s_before, s_after = dot(v,mv(s,v))/3, dot(abs_v,mv(s,abs_v))/3
    k_before, k_after = dot(v,mv(k,v))/3, dot(abs_v,mv(k,abs_v))/3
    assert (s_before,s_after,k_before,k_after) == (F(1,3),F(2,3),F(8,27),F(2,3))
    assert s_after > s_before and k_after > k_before
    q = [F(1),F(-1),F(0),F(0)]
    d = dot(q,mv(lap,q))/sum((mu[i]*q[i]*q[i] for i in range(4)),F(0))
    assert d == 4
    return {"fine_generator": [[str(x) for x in row] for row in fine],
            "S": [[str(x) for x in row] for row in s],
            "G": [[str(x) for x in row] for row in g],
            "K": [[str(x) for x in row] for row in k], "D": str(d),
            "absolute_value_energies": {"S_before":str(s_before),"S_after":str(s_after),
                                        "K_before":str(k_before),"K_after":str(k_after)}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = {"status": "all finite exact checks passed",
              "rotor": rotor_checks(), "gaussian": gaussian_checks(),
              "schur": schur_checks(),
              "scope": "Finite exact arithmetic supports the written analytic proofs; no Yang--Mills gap or all-volume theorem is inferred from finite checking."}
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "rotor_depths": [0,5],
                      "gaussian_sizes": [1,20], "schur_states": 4,
                      "output": args.output}, indent=2))


if __name__ == "__main__":
    main()
