"""Independent canonical fixtures; catches lost constraints/signs/singular limits."""
import unittest
import sympy as s
import expansion_switch as gate


class ExpansionSwitchTests(unittest.TestCase):
    def data(self):
        self.assertTrue(callable(getattr(gate, "derive", None)),
                        "Missing action-derived expansion-switch calculation")
        return gate.derive()

    def test_raw_adm_variation_and_preservation(self):
        d = self.data()
        self.assertTrue(all(s.simplify(x) == 0 for x in d["residuals"]))

    def test_nonzero_field_canonical_pair_not_removed(self):
        d = self.data()["nonzero"]
        self.assertEqual((len(d["primary"]), len(d["secondary"])), (2, 2))
        self.assertEqual((d["rank"], d["first_class"], d["dof"]), (4, 0, 1))
        self.assertEqual(s.simplify(d["matrix"]+d["matrix"].T), s.zeros(4))

    def test_small_nonzero_acceleration_ghost_fixture(self):
        d = self.data()["nonzero"]
        subs = {d["m"]: 1, d["b"]: -s.Rational(1, 12), d["alpha"]: s.Rational(1, 2), d["k"]: 1}
        self.assertEqual(d["kinetic"].subs(subs), -2)
        self.assertEqual(d["speed2"].subs(subs), -1)

    def test_larger_acceleration_changes_sign_not_pair_count(self):
        d = self.data()["nonzero"]
        subs = {d["m"]: 1, d["b"]: -1, d["alpha"]: s.Rational(1, 2)}
        self.assertEqual(d["kinetic"].subs(subs), 9)
        self.assertEqual(d["speed2"].subs(subs), s.Rational(2, 9))
        self.assertEqual(d["matrix"].subs(subs).rank(), 4)

    def test_critical_b_is_not_a_new_constraint(self):
        d = self.data()["critical"]
        self.assertEqual((d["rank"], d["dof"]), (4, 1))
        self.assertEqual(d["z_velocity"], 0)
        self.assertNotEqual(d["p_velocity"], 0)

    def test_zero_field_rebuilds_legendre_transform(self):
        d = self.data()
        self.assertEqual((d["trace_zero"]["rank"], d["trace_zero"]["dof"]), (6, 0))
        self.assertEqual((d["vacuum"]["rank"], d["vacuum"]["first_class"], d["vacuum"]["dof"]), (4, 1, 0))
        self.assertEqual(len(d["vacuum"]["primary"]), 3)

    def test_switch_leaves_static_first_variation_unchanged(self):
        d = self.data()["switch"]
        self.assertEqual(d["B0"], 0)
        self.assertEqual(d["Bprime0"], 0)
        self.assertEqual(s.simplify(d["Bsecond0"]+2/d["K0"]**2), 0)
        self.assertEqual(s.simplify(d["alpha_flrw"]-d["K0"]**2/(9*d["H"]**2+d["K0"]**2)), 0)

    def test_linear_switch_value_zero_does_not_mean_variation_zero(self):
        d = self.data()["static_invariance"]
        self.assertEqual(d["allowed_constants"], {d["c0"]: 0, d["c1"]: 0})
        self.assertNotEqual(d["linear_shift_equation"], 0)

    def test_flrw_uv_recovery_not_a_full_stability_certificate(self):
        d = self.data()["flrw"]
        self.assertEqual(s.simplify(d["UV_kinetic"]-d["D"]), 0)
        self.assertEqual(s.simplify(d["UV_speed2"]-d["Z"]/d["D"]), 0)
        self.assertTrue(d["positive_pole_kappa2"].is_positive)

    def test_homogeneous_sector_is_not_static_k_limit(self):
        d = self.data()["homogeneous"]
        self.assertEqual((d["poisson_rank"], d["first_class"], d["homogeneous_dof"]), (2, 2, 1))
        self.assertNotEqual(d["stiff_H"], 0)

    def test_zero_expansion_and_uv_limits_do_not_commute(self):
        d = self.data()["flrw"]
        self.assertIn("H_zero_then_UV_kinetic", d)
        self.assertNotEqual(s.simplify(d["H_zero_then_UV_kinetic"]-d["UV_kinetic"]), 0)
        self.assertTrue(d["H_zero_then_UV_kinetic"].is_negative)

    def test_architectures_remain_separate_in_saved_evidence(self):
        result = gate.run() if hasattr(gate, "run") else {}
        self.assertIn("independent_cuscuton_screen", result)
        self.assertEqual(result["independent_cuscuton_screen"]["two_tensor_gate"], "FAIL")
        self.assertFalse(result["acceptance"])

    def test_general_F_s_K_trace_degenerate_repair_has_no_lapse_gradient_change(self):
        self.assertTrue(callable(getattr(gate, "general_local_deformation", None)),
                        "Missing general F(s,K) variational restriction")
        d = gate.general_local_deformation()
        self.assertEqual(d["trace_hessian"], 0)
        self.assertNotEqual(d["shift_equation"], 0)
        self.assertEqual(d["allowed_lapse_gradient_change"], 0)
        self.assertEqual(d["integration_residual"], 0)


if __name__ == "__main__":
    unittest.main()
