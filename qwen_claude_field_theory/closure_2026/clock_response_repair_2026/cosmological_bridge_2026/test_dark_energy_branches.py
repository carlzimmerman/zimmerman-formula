import unittest
import numpy as np
from dark_energy_branches import find_roots, inventory, stress
from transfer_evolve import Background


class BranchAudit(unittest.TestCase):
    def test_existing_initial_solution_is_recovered(self):
        bg = Background(.02)
        roots = find_roots(bg.model, 801)
        q = bg.solution.y[2, 0]
        self.assertLess(min(abs(r['q']-q) for r in roots), 1e-10)
        finer = find_roots(bg.model, 1601)
        np.testing.assert_allclose([r['q'] for r in roots], [r['q'] for r in finer], atol=1e-11)

    def test_stress_obeys_action_ward_identity(self):
        bg = Background(.02)
        for t in (0., .01, .02):
            result = stress(bg.at(t)[0])
            self.assertLess(abs(result['ward_residual']), 1e-10)
            self.assertAlmostEqual(result['rho_X'], result['rho_clock']+.7)

    def test_alternative_positive_gradient_root_is_not_declared_healthy(self):
        result = inventory(801)
        alternate = [r for r in result['roots'] if r.get('clock_cs2', [0])[-1]>0]
        self.assertTrue(alternate)
        self.assertEqual(result['full_theory_status'], 'OPEN')
        for row in alternate:
            self.assertEqual(row['kinetic_health'], 'not established by positive sound speed')


if __name__ == '__main__':
    unittest.main()
