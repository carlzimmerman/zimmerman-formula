import unittest

import numpy as np

from normalized_acceleration_action_gate import (
    kernel_identities,
    lapse_euler_identity,
    lapse_dirac_matrix,
    spatial_stress_anisotropy,
    unitary_gauge_reduction,
)


class NormalizedAccelerationActionGateTests(unittest.TestCase):
    def test_kernel_and_lapse_flux(self):
        k = kernel_identities()
        v = lapse_euler_identity()
        self.assertTrue(k["exact_exponential"])
        reduction = unitary_gauge_reduction()
        self.assertTrue(reduction["prefactor_is_sqrt_h"])
        self.assertTrue(reduction["normalized_acceleration_is_DN"])
        self.assertTrue(v["new_exact_divergence"])
        self.assertTrue(v["old_unit_slope_nonzero"])

    def test_metric_stress_is_derived_not_assumed(self):
        s = spatial_stress_anisotropy()
        self.assertFalse(s["anisotropy_identically_zero"])
        self.assertNotEqual(s["anisotropy_at_y1"], 0.0)

    def test_lapse_dirac_rank_and_zero_mode(self):
        nz = lapse_dirac_matrix(1.0, 1.0)
        z = lapse_dirac_matrix(0.0, 0.0)
        self.assertEqual(nz["rank"], int(np.linalg.matrix_rank(np.asarray(nz["matrix"]))))
        self.assertEqual(z["rank"], int(np.linalg.matrix_rank(np.asarray(z["matrix"]))))
        self.assertLess(z["rank"], nz["rank"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
