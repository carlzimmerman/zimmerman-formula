import unittest
import numpy as np
import stability
import refinement
import convective_transport as convective


class StabilityPreparationTests(unittest.TestCase):
    def test_memory_preparation_conserves_energy_but_records_entropy_change(self):
        params=convective.baseline.material.MaterialParameters(rho_q=1,G=1,
            a0=np.sqrt(8*np.pi),tau=.5)
        model=refinement.FloorAuditedCollapse(32,params,initial_density=3)
        state=model.initial_state(); state[64:]=.3
        prepared,audit=stability.entropy_perturbation(model,state)
        self.assertGreater(np.max(prepared[64:]-state[64:]),0)
        self.assertLess(np.min(prepared[64:]-state[64:]),0)
        self.assertLess(abs(audit['delta_energy']['total']),1e-14)
        np.testing.assert_array_equal(prepared[:64],state[:64])
        self.assertTrue(np.all(prepared[64:]>=0))
        self.assertNotEqual(audit['entropy_preparation_change'],0)


if __name__=='__main__':
    unittest.main()
