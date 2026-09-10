#!/usr/bin/env python3
import argparse
import importlib.util
import json
from pathlib import Path
import unittest
import mpmath as mp
import precision_check as p


def root_comparison():
    path = Path(__file__).resolve().parents[1]/'joint_static.py'
    spec = importlib.util.spec_from_file_location('joint_precision_float_comparison',path)
    root = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(root)
    state = root.initial(1e-6,2e-6,.1,.3,.25)
    actual = root.inspect(.5,state,(1e-6,2e-6))
    reference = p.check(60)
    with mp.workdps(60):
        error = {key:abs(mp.mpf(actual[key])/reference[key]-1) for key in ('PX','PXX')}
        for i in range(2):
            for key in ('GX','GXX','kinetic','cross','radial','angular'):
                error[f'halo{i+1}_{key}'] = abs(mp.mpf(actual['halos'][i][key])/reference['halos'][i][key]-1)
    return error


class PrecisionTests(unittest.TestCase):
    def test_signed_value_and_first_derivative_matching(self):
        a = p.check(60)
        self.assertLess(a['H_relative_mismatch'],mp.mpf('1e-50'))
        self.assertLess(a['Hprime_relative_mismatch'],mp.mpf('1e-50'))
        self.assertLess(a['halos'][0]['H'],0)
        self.assertNotEqual(a['constraint_denominator'],0)

    def test_original_stress_and_current(self):
        for row in p.check(60)['halos']:
            self.assertLess(row['relative_stress_error'],mp.mpf('1e-50'))
            self.assertLess(row['relative_current_error'],mp.mpf('1e-50'))
            self.assertGreater(row['rho'],0)

    def test_both_action_derivatives_match(self):
        a = p.check(60)
        self.assertLess(a['GX_relative_mismatch'],mp.mpf('1e-50'))
        self.assertLess(a['GXX_relative_mismatch'],mp.mpf('1e-50'))

    def test_bounded_static_hamiltonian_and_strict_cone(self):
        for row in p.check(60)['halos']:
            self.assertTrue(row['bounded_static_hamiltonian'])
            self.assertTrue(row['strict_cone'])
            self.assertGreater(row['radial_discriminant'],0)
            self.assertGreater(row['light_margin'],0)

    def test_sixty_digits_against_eighty(self):
        low,high = p.check(60),p.check(80)
        with mp.workdps(80):
            for key in ('PX','PXX'):
                self.assertLess(abs(low[key]/high[key]-1),mp.mpf('1e-45'))
            for a,b in zip(low['halos'],high['halos']):
                for key in ('GX','GXX','kinetic','radial','angular','cross'):
                    self.assertLess(abs(a[key]/b[key]-1),mp.mpf('1e-45'))

    def test_root_complex_step_output_matches_independent_derivative(self):
        for error in root_comparison().values():
            self.assertLess(error,mp.mpf('1e-10'))

    def test_third_mass_next_derivative_mismatch(self):
        a = p.third_mass_check(60)
        self.assertLess(a['H_relative_mismatch'],mp.mpf('1e-45'))
        self.assertLess(a['Hprime_relative_mismatch'],mp.mpf('1e-45'))
        self.assertGreater(abs(a['required_PXX_fractional_change']),mp.mpf('.1'))
        self.assertGreater(a['Hsecond_relative_mismatch'],mp.mpf('.01'))
        self.assertTrue(a['third_halo']['strict_cone'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(PrecisionTests))
    data = p.serial(dict(check60=p.check(60),check80=p.check(80),
        root_float_relative_errors=root_comparison(),third_mass=p.third_mass_check(60),
        tests=dict(run=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful())))
    encoded = json.dumps(data,indent=2)+'\n'
    if args.result_file:
        args.result_file.write_text(encoded)
    else:
        print(encoded)
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':
    raise SystemExit(main())
