import unittest
from decimal import Decimal
from exterior import homogeneous, evaluate, constrained_modes


class ExteriorTests(unittest.TestCase):
    def test_regular_controls_do_not_hardcode_obstruction(self):
        jets = dict(PX=1., PXX=1., W=1., WY=0.)
        stable = homogeneous(jets, .5, 0., 0., 1., 0.)
        self.assertGreater(stable['speed_squared'], 0.)
        self.assertFalse(stable['negative_discriminant'])
        jets['WY'] = .1
        unstable = homogeneous(jets, .5, 0., 0., 20., 0.)
        self.assertLess(unstable['speed_squared'], 0.)
        self.assertTrue(unstable['negative_discriminant'])

    def test_singular_clock_is_not_a_pass(self):
        with self.assertRaises(ValueError):
            homogeneous(dict(PX=1., PXX=1., W=1., WY=.5), 1., 0., 0., 1., 0.)

    def test_actual_first_physical_exterior_and_decimal_sign(self):
        row, _ = evaluate(0)
        p = row['principal']
        self.assertGreater(abs(row['physical_Q']-row['reference_qbar']), .001)
        self.assertGreater(p['F'], 0.)
        self.assertGreater(p['K'], 0.)
        self.assertLess(p['G'], -.003)
        self.assertLess(Decimal(row['decimal_control']['G']), 0)
        self.assertLess(max(abs(x) for x in row['background_constraint_residuals']), 1e-12)
        self.assertAlmostEqual(p['imaginary_speed'], .039420487174980146, places=12)

    def test_earlier_time_is_not_falsely_declared_unstable(self):
        row, _ = evaluate(184)
        self.assertGreater(row['principal']['speed_squared'], 0.)
        self.assertFalse(row['principal']['negative_discriminant'])

    def test_constrained_transfer_limit_matches_independent_contraction(self):
        row, values = evaluate(0, extended=True)
        modes = constrained_modes(values, row['principal']['imaginary_speed'])
        errors = [r['distance_to_independent_imaginary_speed'] for r in modes]
        self.assertTrue(all(a > b for a, b in zip(errors, errors[1:])))
        self.assertLess(errors[-1], 2e-7)
        self.assertLess(max(r['normalized_eigen_residual'] for r in modes), 1e-10)


if __name__ == '__main__':
    unittest.main()
