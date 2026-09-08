"""Regression tests for derived equations, not a full-theory certificate."""
import importlib.util
import unittest

import sympy as s


class ConstitutiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if importlib.util.find_spec("constitutive_gate") is None:
            raise AssertionError("The variational computation has not been implemented")
        import constitutive_gate
        cls.g = constitutive_gate

    def test_einstein_term_is_derived_before_varying_both_potentials(self):
        d = self.g.derive_static()
        self.assertEqual(s.simplify(d["eh_ibp_residual"]), 0)
        for residual in d["el_residuals"]:
            self.assertEqual(s.simplify(residual), 0)
        self.assertEqual(s.simplify(d["slip"]), 0)

    def test_gr_control_and_measured_newton_constant(self):
        d = self.g.derive_static()
        self.assertEqual(s.simplify(d["G_ratio"].subs(d["alpha"], 0)), 1)
        self.assertEqual(s.simplify(d["boost"].subs(d["A"], 0)), 1)
        self.assertEqual(s.limit(d["boost"], d["jtot"], s.oo), 1)

    def test_bare_gradient_changes_deep_field_prediction(self):
        d = self.g.derive_static()
        corner = {d["A"]: s.Rational(9, 5), d["alpha"]: s.Rational(1, 100000)}
        b1 = d["boost"].subs(corner).subs(d["jtot"], 1)
        self.assertEqual(b1, s.Rational(199999, 19999))
        self.assertEqual(d["boost"].subs(corner).subs(d["jtot"], 0), 0)

    def test_exact_exponential_primitive_and_nonconvex_branch(self):
        d = self.g.exponential_carrier()
        self.assertEqual(d["primitive_residual"], 0)
        self.assertEqual(d["flux_residual"], 0)
        self.assertGreater(float(d["stiffness"].subs({d["y"]: s.Rational(1, 2), d["B"]: 1})), 0)
        self.assertLess(float(d["stiffness"].subs({d["y"]: 2, d["B"]: 1})), 0)

    def test_constrained_completion_is_not_original_high_field_law(self):
        d = self.g.constrained_completion()
        self.assertEqual(d["join_value_residual"], 0)
        self.assertEqual(d["join_slope_residual"], 0)
        self.assertEqual(d["fenchel_residual"], 0)
        self.assertAlmostEqual(float(d["mu_sat"].subs(d["y"], 2)), 0.8160602794142788)
        self.assertAlmostEqual(float(d["mu_exact"].subs(d["y"], 2)), 0.8646647167633873)

    def test_constraint_matrix_detects_directional_and_zero_mode_degeneracy(self):
        rows = self.g.static_constraint_examples()
        by_name = {row["name"]: row for row in rows}
        self.assertGreater(by_name["plateau_parallel"]["pb_rank"], by_name["plateau_transverse"]["pb_rank"])
        self.assertGreater(by_name["regular_zero_mode"]["pb_rank"], by_name["plateau_zero_mode"]["pb_rank"])
        for row in rows:
            self.assertTrue(row["antisymmetric"])
            self.assertEqual(row["preservation_remainder"], 0)
            self.assertEqual(row["computed_static_only_dof"], 0)

    def test_total_potential_kernel_does_not_share_carrier_obstruction(self):
        d = self.g.total_potential_kernel()
        self.assertEqual(d["constitutive_residual"], 0)
        self.assertEqual(d["longitudinal_residual"], 0)
        self.assertEqual(d["deep_mond_coefficient"], 1)
        self.assertEqual(d["newtonian_limit"], 1)
        self.assertEqual(d["zero_eigenvalues"], [0, 0])

    def test_metric_variant_preserves_trace_degeneracy_but_hits_zero_field_endpoint(self):
        d = self.g.metric_route_screen()
        self.assertEqual(d["trace_velocity_hessian"], 0)
        self.assertEqual(d["homogeneous_f"], 0)
        self.assertEqual(d["homogeneous_f_s"], 1)


if __name__ == "__main__":
    unittest.main()
