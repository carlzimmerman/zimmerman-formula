import unittest

from alc_gate import flrw_gate, limit_gate, static_gate, tensor_gate, ward_gate


class AccelerationLockedClockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.static = static_gate()
        cls.flrw = flrw_gate()
        cls.tensor = tensor_gate()
        cls.limits = limit_gate()
        cls.ward = ward_gate()

    def test_static_law_and_slip_are_varied_independently(self):
        self.assertEqual(self.static["mu_identity"], 0)
        self.assertEqual(self.static["no_slip_residual"], 0)
        self.assertEqual(self.static["slip_AQUAL_residual"], 0)

    def test_clock_dust_and_expanding_branch(self):
        self.assertTrue(self.flrw["H_nonzero_allowed"])
        self.assertEqual(self.flrw["clock_charge"], "a^3 sigma = constant")
        self.assertEqual(self.flrw["continuity_residual_after_charge"], 0)

    def test_tensor_gate_is_luminal(self):
        self.assertEqual(str(self.tensor["c_T_squared"]), "c**2")

    def test_zero_and_high_field_limits_are_not_hidden(self):
        self.assertEqual(self.limits["mu_limit_y0"], 0)
        self.assertEqual(self.limits["mu_limit_yinf"], 1)
        self.assertEqual(self.limits["correction_limit_yinf"], -2)

    def test_matter_ward_identity_is_metric(self):
        self.assertIn("nabla_mu T_m", self.ward["ward_identity"])


if __name__ == "__main__":
    unittest.main()
