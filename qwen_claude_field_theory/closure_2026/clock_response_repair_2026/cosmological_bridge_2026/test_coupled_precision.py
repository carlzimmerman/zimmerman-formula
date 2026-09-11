import unittest
import mpmath as mp
from coupled_precision import hermite, run


class CoupledPrecisionTests(unittest.TestCase):
    def test_hermite_cubic_and_derivatives(self):
        with mp.workdps(35):
            f = lambda t: hermite(mp.matrix([0]), mp.matrix([1]),
                mp.matrix([0]), mp.matrix([3]), mp.mpf(1), t)[0]
            for t in (mp.mpf('.2'), mp.mpf('.7')):
                self.assertLess(abs(f(t)-t**3), mp.mpf('1e-30'))
                self.assertLess(abs(mp.diff(f, t, 2)-6*t), mp.mpf('1e-30'))

    def test_original_euler_residual_refines(self):
        result = run(steps=('.002', '.001', '.0005'))
        errors = [r['max_scaled_euler'] for r in result['rows']]
        self.assertTrue(all(b < a/2 for a, b in zip(errors, errors[1:])), errors)
        self.assertLess(errors[-1], 1e-6)
        for row in result['rows']:
            self.assertLess(row['max_background_constraint'], 1e-8)


if __name__ == '__main__':
    unittest.main()
