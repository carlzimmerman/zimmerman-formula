"""Necessary principal kinetic checks from the unchanged quadratic action."""
import unittest
import numpy as np

from dark_energy_branches import clock_speed
from radiation_probe import ProbeBackground
from branch_kinetic import kinetic, kinetic_blocks


class BranchKineticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bg = ProbeBackground(5.)

    def values(self, H, q):
        return self.bg.evaluate([1., H, q, 0., .001, .01], extended=True)[0]

    def test_schur_complement_matches_stationary_full_quadratic_form(self):
        v = self.values(.6967532055475008, .9477017173736229)
        reduced, velocity, mixed, auxiliary = kinetic_blocks(v, 3000.)
        for direction in (np.array([1., -2., .5, 3.]),
                          np.array([-.3, .2, 4., -1.])):
            stationary = -np.linalg.solve(auxiliary, mixed.T @ direction)
            full_direction = np.r_[direction, stationary]
            full = np.block([[velocity, mixed], [mixed.T, auxiliary]])
            self.assertAlmostEqual(direction @ reduced @ direction,
                                   full_direction @ full @ full_direction,
                                   delta=1e-9*(1+abs(direction @ reduced @ direction)))

    def test_kinetic_matrix_is_real_symmetric_without_rank_assumption(self):
        v = self.values(.6967532055475008, .9477017173736229)
        result = kinetic(v, 3000.)
        np.testing.assert_allclose(result['matrix'], result['matrix'].T,
                                   rtol=0., atol=result['null_tolerance'])
        np.testing.assert_allclose(result['eigenvalues'],
                                   np.linalg.eigvalsh(result['matrix']))
        self.assertTrue(np.isrealobj(result['matrix']))

    def test_negative_gradient_speed_does_not_imply_negative_kinetic_eigenvalue(self):
        v = self.values(.5191118192004086, .9078321505772312)
        self.assertLess(clock_speed(v, 30000.)[0], 0.)
        result = kinetic(v, 3000.)
        self.assertGreaterEqual(min(result['eigenvalues']), -result['null_tolerance'])


if __name__ == '__main__':
    unittest.main()
