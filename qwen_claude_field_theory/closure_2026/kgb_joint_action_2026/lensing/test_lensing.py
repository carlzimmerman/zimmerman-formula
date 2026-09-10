#!/usr/bin/env python3
"""Exact identities and independent elementary lensing controls."""
import argparse
import json
from pathlib import Path
import unittest
import sympy as s
import lensing


class LensingTests(unittest.TestCase):
    def test_einstein_tensor_computed_from_metric(self):
        self.assertEqual(lensing.geometry()['residuals'], [0, 0])

    def test_pressure_and_isotropic_coordinate_identities(self):
        self.assertEqual(lensing.derive()['residuals'], [0]*7)

    def test_schwarzschild_density_vanishes(self):
        a = lensing.geometry()
        r, M = a['r'], s.Symbol('M', positive=True)
        self.assertEqual(s.simplify(a['rho'].subs(a['B'], 1/(1-2*M/r)).doit()), 0)

    def test_point_mass_deflection(self):
        # Born ray r^2=b^2+z^2, Phi'=Psi'=M/r^2.
        b, M = s.symbols('b M', positive=True)
        z = s.Symbol('z', real=True)
        deflection = s.integrate(2*M*b/(b*b+z*z)**s.Rational(3,2),
                                (z, -s.oo, s.oo))
        self.assertEqual(s.simplify(deflection-4*M/b), 0)

    def test_flat_force_finite_segment_pressure_deflection(self):
        # g=w/r, P=2m*k*w/r^2 gives slope ratio 1-k on a finite ray segment.
        b, length, w, k = s.symbols('b length w k', positive=True)
        z = s.Symbol('z', real=True)
        angle = s.integrate((2-k)*w*b/(b*b+z*z), (z, -length, length))
        self.assertEqual(s.simplify(angle-2*(2-k)*w*s.atan(length/b)), 0)

    def test_local_exact_ticking_clock(self):
        a = lensing.constant_pressure_clock()
        self.assertEqual(a['residuals'], [0]*6)
        r, M, m, P = s.symbols('r M m P', positive=True)
        self.assertEqual(s.simplify(a['rho'].subs(r, 4*M)), -2*P)
        self.assertEqual(s.limit(lensing.derive()['exact_pressure_ratio_change'],
                                s.Symbol('P', real=True), 0), 0)

    def test_exact_pressure_difference_rationalization(self):
        T, H = s.symbols('T H', positive=True)
        stable = -s.sqrt(T)*(H-1)/(s.sqrt(H)*(1+s.sqrt(H)))
        direct = s.sqrt(T/H)-s.sqrt(T)
        self.assertEqual(s.simplify(stable-direct), 0)

    def test_large_pressure_density_ratio_is_small_metric_effect(self):
        row = lensing.target_controls()[0]
        self.assertGreater(s.Float(row['P_over_rho']), 100000)
        self.assertLess(abs(s.Float(row['leading_Weyl_fraction'])), s.Rational(1,10**7))

    def test_negative_density_is_small_metric_effect(self):
        row = lensing.target_controls()[1]
        self.assertLess(s.Float(row['rho_over_curvature_density']), 0)
        self.assertLess(abs(s.Float(row['exact_log_slope_ratio_pressure_change'])),
                        s.Rational(11,10**7))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file', type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LensingTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    output = lensing.results()
    output['tests'] = dict(run=result.testsRun, failures=len(result.failures),
                           errors=len(result.errors), passed=result.wasSuccessful())
    if args.result_file:
        args.result_file.write_text(json.dumps(output, indent=2)+'\n')
    else:
        print(json.dumps(output, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
