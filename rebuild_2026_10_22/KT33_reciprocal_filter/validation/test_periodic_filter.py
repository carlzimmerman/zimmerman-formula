"""Independent behavioral tests for the continuum-map periodic realization."""
import math
import unittest

import numpy as np

from periodic_filter import PeriodicFilter


class PeriodicChecks(unittest.TestCase):
    def setUp(self):
        self.model = PeriodicFilter(32, sigma=0.7, external=(1.0, 0.0, 0.0))
        self.x, self.y, self.z = self.model.coordinates

    def test_newtonian_control_preserves_unsmoothed_source(self):
        rho = np.sin(self.x) + 0.2 * np.cos(2 * self.y)
        expected = -np.sin(self.x) - 0.05 * np.cos(2 * self.y)
        np.testing.assert_allclose(self.model.potential(rho, newtonian=True), expected,
                                   atol=2e-14, rtol=0)

    def test_identity_filter_equals_plain_qumond(self):
        model = PeriodicFilter(24, sigma=0, external=(1, 0.3, 0))
        x, y, z = model.coordinates
        rho = 1 + 0.2 * np.sin(x) + 0.1 * np.cos(y + z)
        np.testing.assert_allclose(model.potential(rho), model.potential(rho, outer=False),
                                   atol=2e-14, rtol=0)

    def test_response_matches_independent_two_mode_integral(self):
        m = self.model
        rho = 1 - 0.2 / math.exp(-0.7**2 / 2) * np.sin(self.x)
        f, h = np.cos(self.x), np.cos(2 * self.x)
        step = 1e-4
        def paired(a, b, outer):
            derivative = (m.potential(rho + step*b, outer=outer)
                          - m.potential(rho - step*b, outer=outer)) / (2*step)
            return float(np.mean(a*derivative))
        old = [paired(f,h,False), paired(h,f,False)]
        corrected = [paired(f,h,True), paired(h,f,True)]
        np.testing.assert_allclose(old, [0.0017058629236758362, 0.0035575464090079347],
                                   atol=2e-11, rtol=0)
        np.testing.assert_allclose(corrected, [0.0013351866519796187]*2,
                                   atol=2e-11, rtol=0)
        self.assertGreater(abs(old[0]-old[1]), 1e-3)

    def test_force_cancels_for_asymmetric_source(self):
        m = PeriodicFilter(32, sigma=0.7, external=(3,0,0))
        x, y, z = m.coordinates
        rho = 2 + np.cos(x) + 0.4*np.cos(2*x) + 0.1*np.cos(y+z)
        def force(outer):
            return np.array([np.mean(rho*g) for g in m.gradient(m.potential(rho, outer=outer))])
        self.assertLess(float(np.linalg.norm(force(True))), 1e-12)
        self.assertGreater(float(np.linalg.norm(force(False))), 1e-4)


if __name__ == '__main__':
    unittest.main()
