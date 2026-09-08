"""Control fixtures for a changed primary, not an assigned DOF count."""
import unittest
import sympy as s
import braiding_gate as gate


class BraidingTests(unittest.TestCase):
    def data(self):
        self.assertTrue(callable(getattr(gate, "derive", None)), "Missing changed-primary canonical calculation")
        return gate.derive()

    def test_legendre_map_derives_the_mixed_primary(self):
        d = self.data()
        self.assertTrue(all(s.simplify(x) == 0 for x in d["residuals"]))
        c = d["canonical"]
        self.assertEqual(s.simplify(c["primary"][0]-(c["pn"]-c["eta"]*c["pz"])), 0)

    def test_mond_constraints_leave_one_initial_data_pair(self):
        c = self.data()["canonical"]
        self.assertEqual((c["rank"], c["first_class"], c["dof"]), (4, 0, 1))
        self.assertEqual(len(c["constraints"]), 4)
        self.assertEqual(c["z_tilde_velocity"], 0)

    def test_unmodified_control_continues_preservation_weakly(self):
        c = self.data()["unmodified"]
        self.assertEqual((c["rank"], c["first_class"], c["dof"]), (2, 2, 0))
        self.assertTrue(all(x == 0 for x in c["preservation_residuals"]))

    def test_eta_zero_does_not_remove_added_scalar_pair(self):
        c = self.data()["eta_zero"]
        self.assertEqual((c["rank"], c["dof"]), (4, 1))
        self.assertEqual(c["Hred"], 0)

    def test_ordinary_matter_changes_homogeneous_constraint(self):
        c = self.data()["homogeneous"]
        # Fixed physical matter; wrong reuse of transformed matter misses this.
        fixture = {c["N"]: 1, c["a"]: 1, c["m"]: 1, c["ps"]: 2, c["eta"]: 1}
        self.assertEqual(c["lapse_bracket_on_constraint"].subs(fixture), 16)
        self.assertEqual((c["generic_rank"], c["generic_dof"]), (2, 2))
        self.assertEqual((c["gr_rank"], c["gr_dof"]), (0, 1))

    def test_no_slip_and_invertibility_exceptions_are_distinct(self):
        c = self.data()["canonical"]
        self.assertEqual(s.simplify(c["gamma_static"]-(1+2*c["eta"])), 0)
        self.assertEqual(s.solve(c["gamma_static"]-1, c["eta"]), [0])

    def test_homogeneous_exception_is_preserved_not_divided_away(self):
        c = self.data()["homogeneous"]
        self.assertEqual(c["exception_minus_third"]["secondary_implies_A"], 0)
        self.assertEqual(c["exception_minus_third"]["pa_drift_on_final_surface"],
                         3*c["ps"]**2/(2*c["a"]**4))
        self.assertEqual(c["vacuum_secondary_differential"], [0]*6)

    def test_measured_G_normalizes_static_law(self):
        c = self.data()["canonical"]
        self.assertEqual(s.simplify(c["mu_measured"]-(1-c["alpha"]/(1+c["eta"])**2)), 0)
        self.assertEqual(c["mu_measured"].subs(c["eta"], 0), 1-c["alpha"])

    def test_combined_report_does_not_certify_failed_candidates(self):
        d = gate.run()
        self.assertIn("transformed_affine_screen", d)
        self.assertIn("anisotropic_primary_screen", d)
        self.assertTrue(d["algebra_checks_passed"])
        self.assertFalse(d["two_tensor_gate"])


if __name__ == "__main__":
    unittest.main()
