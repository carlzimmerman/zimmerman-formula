import unittest

import numpy as np

from algebraic_compensator_gate import dirac_algebraic_block, envelope_identity, stress_flux_no_go


class AlgebraicCompensatorGateTests(unittest.TestCase):
    def test_envelope_theorem_is_symbolic(self):
        self.assertTrue(envelope_identity()["envelope_identity_exact"])

    def test_regular_algebraic_compensator_cannot_remove_flux_stress(self):
        r = stress_flux_no_go()
        self.assertTrue(r["incompatibility_at_y1"])

    def test_dirac_rank_drop_is_measured(self):
        regular = dirac_algebraic_block(1.0)
        singular = dirac_algebraic_block(0.0)
        self.assertEqual(regular["rank"], int(np.linalg.matrix_rank(np.asarray(regular["matrix"]))))
        self.assertEqual(singular["rank"], int(np.linalg.matrix_rank(np.asarray(singular["matrix"]))))
        self.assertLess(singular["rank"], regular["rank"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
