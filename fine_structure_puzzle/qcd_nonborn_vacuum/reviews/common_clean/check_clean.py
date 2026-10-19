#!/usr/bin/env python3
"""Independent exact coefficient and field-strength matrix check.

Only standard-library rational arithmetic. The source transcription and
Euclidean definitions are in this reviewer's pre-author SOURCECRITICAL.md.
The author code/result files are never imported or opened by this program.
This program was written after author inspection, so code blindness is NOT
claimed; the critical mathematics was pinned before that inspection.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path


class P:
    """Four-variable sparse polynomial with exact rational coefficients."""
    def __init__(self, terms=None):
        self.t = {e: F(c) for e, c in (terms or {}).items() if c}

    def __add__(self, other):
        ans = dict(self.t)
        for e, c in other.t.items():
            ans[e] = ans.get(e, F(0)) + c
        return P(ans)

    def __neg__(self):
        return P({e: -c for e, c in self.t.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        ans = {}
        for e, c in self.t.items():
            for f, d in other.t.items():
                g = tuple(x + y for x, y in zip(e, f))
                ans[g] = ans.get(g, F(0)) + c * d
        return P(ans)

    def __eq__(self, other):
        return self.t == other.t


ZERO = P()
ONE = P({(0, 0, 0, 0): 1})
k = [P({tuple(int(i == j) for j in range(4)): 1}) for i in range(4)]
k2 = sum((x * x for x in k), ZERO)


def outer(f):
    return [[a * b for b in f] for a in f]


def matrix_sum(items):
    return [[sum((m[a][b] for m in items), ZERO) for b in range(4)]
            for a in range(4)]


def field_pair(a, b):
    # F_ab = k_a A_b - k_b A_a, directly from the field definition.
    return [k[a] if j == b else -k[b] if j == a else ZERO
            for j in range(4)]


def trace(m):
    return sum((m[a][a] for a in range(4)), ZERO)


def average_quadratic_on_unit_s3(p):
    total = F(0)
    for e, c in p.t.items():
        assert sum(e) == 2
        if 2 in e:
            total += c / 4
        else:
            # A mixed moment vanishes by reflection of either coordinate.
            assert sorted(e) == [0, 0, 1, 1]
    return total


def linear_sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def linear_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def strings(v):
    return [str(x) for x in v]


def main(output):
    # E and B constructed separately from all six F_ab components.
    electric = matrix_sum([outer(field_pair(0, i)) for i in range(1, 4)])
    magnetic = matrix_sum([outer(field_pair(i, j))
                           for i in range(1, 4) for j in range(i + 1, 4)])
    total = matrix_sum([electric, magnetic])
    for a in range(4):
        for b in range(4):
            assert total[a][b] == (k2 if a == b else ZERO) - k[a] * k[b]
    for matrix in [electric, magnetic, total]:
        for a in range(4):
            assert sum((matrix[a][b] * k[b] for b in range(4)), ZERO) == ZERO
    e_mean = average_quadratic_on_unit_s3(trace(electric))
    b_mean = average_quadratic_on_unit_s3(trace(magnetic))
    assert e_mean == b_mean == F(3, 2)

    # The decomposition into dispersive (a+b)E and subtraction -b(E+B)
    # is checked as a polynomial matrix identity for each a,b coefficient.
    dispersive_mean = e_mean
    subtraction_mean = -average_quadratic_on_unit_s3(trace(total))
    assert dispersive_mean + subtraction_mean == -b_mean

    # Direct fresh transcription from BKSM (7a),(8a); Q[kappa_s].
    electric_log = linear_sub((F(9), F(0)), (F(3), F(0)))
    electric_constant = scale(F(1, 8),
                              linear_sub((F(71), F(0)), (F(39), F(0))))
    magnetic_log = scale(F(3),
                         linear_sub((F(3), F(1)), (F(1), F(-1))))
    magnetic_constant = scale(F(1, 4),
                              linear_sub((F(37, 2), F(6)),
                                         (F(13, 2), F(-6))))
    minus_log = linear_sub(electric_log, magnetic_log)
    minus_constant = linear_sub(electric_constant, magnetic_constant)
    plus_log = linear_add(electric_log, magnetic_log)
    plus_constant = linear_add(electric_constant, magnetic_constant)
    # Independently read Eq. (10) is the checksum, not a generated input.
    assert minus_log == (F(0), F(-6))
    assert minus_constant == (F(1), F(-3))
    assert plus_log == (F(12), F(6))
    assert plus_constant == (F(7), F(3))

    # Ball volume/(2pi)^4 = K^4/(32pi^2); action prefactor=2pi.
    # Rational coefficient recorded after multiplying the result by pi.
    csoft_pi = 2 * e_mean / 32
    assert csoft_pi == F(3, 32)
    # Multiply C/u=1/(96pi^2 F^2) and extra 1/pi from source formulas.
    soft_log_pi4 = scale(csoft_pi / 96, minus_log)
    assert soft_log_pi4 == (F(0), F(-3, 512))
    scalar_log_pi4 = scale(F(1, 2), soft_log_pi4)
    assert scalar_log_pi4 == (F(0), F(-3, 1024))

    # Exact radial polynomial division for photon mass t=lambda^2,
    # y=k^2: y^2/(y+t)=y-t+t^2/(y+t).
    y, t = k[0], k[1]
    assert y * y == (y + t) * (y - t) + t * t
    # Coefficient of lambda^4 log(lambda^2) is -1/(16pi^2)
    # before 3pi*(alpha-beta), so mixed source log has this coefficient.
    mass_regulator_mixed_pi4 = scale(-F(3, 16 * 96), minus_log)
    assert mass_regulator_mixed_pi4 == (F(0), F(3, 256))

    # Exhaustive finite rational-charge check is a diagnostic only.
    count = 0
    for a in range(-3, 4):
        for b in range(-3, 4):
            q = (F(a, 3), F(b, 3), F(-1, 3))
            swapped = (q[1], q[0], q[2])
            assert sum(q) == sum(swapped)
            assert sum(x*x for x in q) == sum(x*x for x in swapped)
            assert q[0] - q[1] == -(swapped[0] - swapped[1])
            count += 1

    result = {
        "status": "exact bounded assertions passed",
        "tensor_checks": {"dimension": 4, "homogeneous_degree": 2,
                          "transversality_components_checked": 12,
                          "total_kernel_components_checked": 16,
                          "electric_s3_mean": str(e_mean),
                          "magnetic_s3_mean": str(b_mean),
                          "dispersive_mean": str(dispersive_mean),
                          "subtraction_mean": str(subtraction_mean)},
        "source_differences_units_gA2_over_96pi3F2m": {
            "electric_log": strings(electric_log),
            "electric_constant": strings(electric_constant),
            "magnetic_log": strings(magnetic_log),
            "magnetic_constant": strings(magnetic_constant),
            "minus_log": strings(minus_log), "minus_constant": strings(minus_constant),
            "plus_log": strings(plus_log), "plus_constant": strings(plus_constant)},
        "soft_ball_coefficient_times_pi": str(csoft_pi),
        "soft_ball_log_units_gA2_over_pi4F2m": strings(soft_log_pi4),
        "scalar_mass_log_units_gA2_over_pi4F2m": strings(scalar_log_pi4),
        "photon_mass_mixed_log_units_gA2_over_pi4F2m": strings(mass_regulator_mixed_pi4),
        "rational_charge_cases": count,
        "randomness_used": False,
        "non_claims": ["No path-integral computation", "No all-momentum mass response",
                       "No chiral remainder bound", "No empirical LEC input",
                       "No arbitrary-degree tensor identity beyond declared polynomials"]}
    Path(output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"passed": True, "tensor_mean": str(e_mean),
                      "soft_ball_log": strings(soft_log_pi4),
                      "charge_cases": count}))


if __name__ == "__main__":
    main(sys.argv[1])
