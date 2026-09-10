#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import unittest
import sympy as s
import conformal_extension as c


class ExtensionTests(unittest.TestCase):
    def test_independent_curvature(self):
        self.assertEqual(c.curvature_check()['residual'],0)

    def test_variation_and_boundary(self):
        self.assertEqual(c.derive()['residuals'],[0]*5)

    def test_generic_radial_and_no_slip_relations(self):
        self.assertEqual(c.general_radial_identities()['residuals'],[0]*5)

    def test_primary_coefficient_translation(self):
        self.assertEqual(c.source_translation()['residuals'],[0]*2)

    def test_new_operator_cannot_be_absorbed_into_same_metric_kgb(self):
        self.assertEqual(c.derive()['independent_same_X_witness'],[0,s.Rational(89,460)])

    def test_constant_F_recovers_original_radial_equation(self):
        a = c.general_radial_identities()
        h,r,g,P,m = s.symbols('h r g P m',real=True)
        F = s.Symbol('F',positive=True)
        restored = a['B'].subs({h:0,F:m/2})
        self.assertEqual(s.factor(restored-(1+2*r*g)/(1+r*r*P/m)),0)

    def test_affine_conformal_map_is_invertible(self):
        X,lam = s.symbols('X lam',positive=True)
        C = 1+lam*X
        self.assertEqual(s.factor(C-X*s.diff(C,X)),1)
        self.assertEqual(s.factor(s.diff(X/C,X)),1/(1+lam*X)**2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ExtensionTests))
    data = c.results()
    data['tests'] = dict(run=result.testsRun,failures=len(result.failures),
                        errors=len(result.errors),passed=result.wasSuccessful())
    text = json.dumps(data,indent=2)+'\n'
    if args.result_file:args.result_file.write_text(text)
    else:print(text)
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
