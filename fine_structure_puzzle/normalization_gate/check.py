#!/usr/bin/env python3
"""Exact finite/symbolic checks for CLAIM.md; no measured alpha enters."""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    a, b, c, z, m2 = s.symbols('a b c z m2', positive=True)
    K = s.Matrix([[a, b], [b, c]])
    q = s.Matrix([1, 0])
    inverse = (z*K+s.diag(0, m2)).inv()
    residue = s.factor(z*(q.T*inverse*q)[0])
    expected = (c*z+m2)/((a*c-b*b)*z+a*m2)
    assert s.simplify(residue-expected) == 0
    massive = s.limit(residue, z, 0, dir='+')
    massless_first = s.simplify(residue.subs(m2, 0))
    assert s.simplify(massive-1/a) == 0
    assert s.simplify(massless_first-c/(a*c-b*b)) == 0
    # A genuine mixed benchmark: positive K, both diagonal entries fixed.
    benchmark = {a: s.Integer(2), b: s.Integer(1), c: s.Integer(3)}
    assert massive.subs(benchmark) == s.Rational(1, 2)
    assert massless_first.subs(benchmark) == s.Rational(3, 5)

    # Universal coordinate-covariance identity for a symbolic shear.
    t = s.symbols('t', real=True)
    S = s.Matrix([[1, t], [0, 1]])
    Kp, qp = S.T*K*S, S.T*q
    assert s.simplify((qp.T*Kp.inv()*qp)[0]-(q.T*K.inv()*q)[0]) == 0

    # Exact rank-one Higgs kernels, not random floating-point fixtures.
    hull = []
    K0 = s.Matrix([[2, 1], [1, 3]])
    qs = [s.Matrix([1, 0]), s.Matrix([0, 1]), s.Matrix([1, 1])]
    for h0 in range(-2, 3):
        for h1 in range(-2, 3):
            if h0 == 0 and h1 == 0:
                continue
            h = s.Matrix([h0, h1])
            n = s.Matrix([h1, -h0])
            M = h*h.T
            pole = (z*K0+M).inv().applyfunc(lambda x: s.limit(z*x, z, 0, dir='+'))
            target = n*n.T/(n.T*K0*n)[0]
            assert pole == target
            for qi in qs:
                assert s.simplify((qi.T*pole*qi)[0]-(qi.T*n)[0]**2/(n.T*K0*n)[0]) == 0
            hull.append([h0, h1])
    assert len(hull) == 24

    # Rational rotations keep the exact eigenvalues fixed; q,h remain fixed.
    orientations = []
    u = s.symbols('u', real=True)
    cosine, sine = (1-u*u)/(1+u*u), 2*u/(1+u*u)
    R = s.Matrix([[cosine, -sine], [sine, cosine]])
    Kr = s.simplify(R*s.diag(1, 2)*R.T)
    assert s.simplify(Kr.det()-2) == 0
    assert s.simplify(s.trace(Kr)-3) == 0
    projected = s.factor(1/Kr[0, 0])
    for ui in [s.Integer(0), s.Rational(1, 2), s.Integer(1)]:
        Ki = Kr.subs(u, ui)
        assert Ki[0, 0] > 0 and Ki.det() > 0
        orientations.append({'rotation_parameter': str(ui), 'K': str(Ki),
                             'four_pi_alpha': str(projected.subs(u, ui))})
    assert [x['four_pi_alpha'] for x in orientations] == ['1', '25/41', '1/2']
    result = {
        'claim_id': 'FSP-N', 'base_checkpoint': 'FSP-000',
        'assertion_tested': 'Symbolic 2x2 inverse-pole limits and shear covariance; 24 Higgs kernels x 3 charges; fixed-spectrum rational-rotation counterfamily.',
        'non_claims': ['No prediction of measured alpha', 'No UV completion established', 'No finite loop or experimental precision claim'],
        'symbolic_residue': str(residue), 'massive_then_zero_momentum': str(massive),
        'massless_first': str(massless_first), 'higgs_vectors_tested': hull,
        'charge_vectors_per_higgs': 3, 'orientations': orientations,
        'checks_passed': True,
    }
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['claim_id', 'checks_passed', 'massive_then_zero_momentum', 'massless_first']}))


if __name__ == '__main__':
    main()
