import unittest

import numpy as np

from rmmg_constitutive_action import (
    clock_health_scan,
    dirac_scalar_sector,
    exponential_kernel,
    weak_field_variation,
)


class RMMGConstitutiveGateTests(unittest.TestCase):
    def test_kernel_is_exact(self):
        k = exponential_kernel()
        self.assertTrue(k["mu_identity"])
        self.assertGreater(k["lambda_perp_at_1"], 0.0)

    def test_independent_potentials(self):
        v = weak_field_variation()
        self.assertTrue(v["slip_equation_is_laplacian"])
        self.assertTrue(v["aqual_target_matches"])

    def test_actual_dirac_rank_and_zero_mode(self):
        nz = dirac_scalar_sector(1.0, 2.0, 1.0)
        z = dirac_scalar_sector(0.0, 2.0, 1.0)
        # The dimension and rank come from the constructed matrix; the test
        # does not insert a preselected rank into the calculation.
        self.assertEqual(nz["rank"], len(nz["matrix"]))
        self.assertEqual(nz["remaining_scalar_phase_dimension"], nz["phase_space_dimension"] - nz["rank"])
        self.assertEqual(z["rank"], int(np.linalg.matrix_rank(np.asarray(z["matrix"]))))
        self.assertLess(z["rank"], nz["rank"])
        self.assertEqual(nz["preservation_status"], "uniquely_fixed")
        self.assertEqual(z["preservation_status"], "rank_deficient")

    def test_clock_is_separately_healthy_on_witness_scan(self):
        c = clock_health_scan()
        self.assertTrue(c["positive_K_X_on_scan"])
        self.assertTrue(c["positive_Sigma_on_scan"])
        self.assertTrue(c["positive_cs2_on_scan"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
