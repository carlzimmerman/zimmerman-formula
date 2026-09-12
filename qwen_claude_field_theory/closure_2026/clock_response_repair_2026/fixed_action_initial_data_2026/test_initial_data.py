import unittest
import numpy as np
from initial_data import FrozenBackground, roots, sample, continue_initial
from dark_energy_branches import find_roots


class InitialDataChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bg = FrozenBackground()

    def test_frozen_coefficient_join(self):
        model = self.bg.model
        old = model.backward.background(0.)
        new = model.background(0.)
        np.testing.assert_allclose(old['raw'],new['raw'],rtol=1e-13,atol=1e-15)
        for tau in (-1.,-.25):
            np.testing.assert_array_equal(model.background(tau)['raw'],
                                          model.backward.background(tau)['raw'])

    def test_baseline_and_double_grid_agree(self):
        old = find_roots(self.bg.model,1601)
        new = roots(self.bg.model,0.,.001,.01,1601)
        fine = roots(self.bg.model,0.,.001,.01,3201)
        np.testing.assert_allclose([r['q'] for r in old],[r['q'] for r in new],rtol=0,atol=1e-12)
        np.testing.assert_allclose([r['q'] for r in fine],[r['q'] for r in new],rtol=0,atol=1e-12)

    def test_new_initial_data_original_constraints_and_ward(self):
        found = roots(self.bg.model,1.,.001,.01)
        self.assertTrue(found)
        for r in found:
            p = sample(self.bg,r,0.,[r['H'],r['q'],r['tau'],0.])
            self.assertLess(p['scaled_friedmann_residual'],1e-10)
            self.assertLess(p['scaled_clock_residual'],1e-10)
            self.assertLess(abs(p['stress']['ward_residual']),1e-10)
            self.assertEqual(len(p['kinetic']['eigenvalues']),4)
            for mode in p['high_k']:
                self.assertEqual(len(mode['scaled_eigenvalue_real']),6)
                self.assertTrue(np.isfinite(mode['scaled_eigenvalue_real']).all())

    def test_new_charge_conservation(self):
        found = roots(self.bg.model,1.,.001,.01)
        initial = max(found,key=lambda r:r['q'])
        result = continue_initial(self.bg,initial,efolds=.05)
        self.assertEqual(len(result['samples']),3)
        self.assertLess(result['max_charge_drift'],1e-9)
        for p in result['samples']:
            self.assertAlmostEqual(p['a']**3*p['baryon'],.001,places=14)
            self.assertAlmostEqual(p['a']**4*p['radiation'],.01,places=14)


if __name__ == '__main__':
    unittest.main()
