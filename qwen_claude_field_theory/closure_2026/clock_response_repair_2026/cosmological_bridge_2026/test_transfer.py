import importlib.util
import unittest
import numpy as np


class FiniteWavelengthTransfer(unittest.TestCase):
    def implementation(self):
        self.assertIsNotNone(importlib.util.find_spec('transfer_evolve'),
                             'missing same-action finite-wavelength evolution')
        import transfer_evolve
        return transfer_evolve

    def test_all_initial_modes_satisfy_uneliminated_equations(self):
        run=self.implementation().evolve(ks=(.3,3.),tend=.02)
        self.assertLess(run['max_background_constraint'],1e-9)
        for mode in run['modes']:
            for check in mode['diagnostics']:
                self.assertLess(check['max_scaled_euler'],3e-6)
                self.assertLess(check['max_scaled_momentum'],1e-6)
                self.assertLess(check['max_scaled_slip'],1e-6)

    def test_zero_mode_cannot_enter_divided_equations(self):
        with self.assertRaisesRegex(ValueError,'positive'):
            self.implementation().evolve(ks=(0.,),tend=.02)

    def test_refining_integrator_preserves_transfer_matrix(self):
        module=self.implementation()
        loose=module.evolve(ks=(3.,),tend=.02,rtol=2e-8)
        tight=module.evolve(ks=(3.,),tend=.02,rtol=2e-10)
        np.testing.assert_allclose(loose['modes'][0]['transfer_end'],
                                   tight['modes'][0]['transfer_end'],
                                   rtol=3e-6,atol=1e-7)


if __name__=='__main__':unittest.main()
