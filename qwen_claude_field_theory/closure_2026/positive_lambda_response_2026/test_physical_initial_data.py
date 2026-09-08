"""Physical canonical matter is not an independently assigned external stress."""

import importlib
import importlib.util
import json
import unittest
import contextlib
import io

import sympy as s


class PhysicalInitialDataTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("physical_initial_data"),
                             "The physical initial-data derivation is not implemented")
        return importlib.import_module("physical_initial_data")

    def test_actual_stress_and_full_linear_ward_identity(self):
        d = self.module().derive_stress_ward()
        for name, residual in d["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)
        self.assertTrue(any(s.simplify(value) != 0 for value in d["connection_correction"]))
        self.assertTrue(any(s.simplify(value) != 0 for value in d["background_divergence_delta_T"]))

    def test_constraints_and_full_cauchy_fields(self):
        d = self.module().derive_constraints()
        for name, residual in d["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)
        self.assertEqual(d["kinetic"], 9)
        self.assertEqual(d["speed_squared"], s.Rational(1, 9))
        self.assertEqual(s.simplify(d["matter_momentum"]-9*d["a"]**3*d["ud"]), 0)

    def test_laplacian_data_commute_and_have_positive_energy_flux(self):
        d = self.module().derive_support()
        self.assertEqual(s.simplify(d["laplacian_commutator"]), 0)
        self.assertEqual(s.simplify(d["energy_balance_residual"]), 0)
        self.assertEqual(s.simplify(d["outgoing_flux_square_residual"]), 0)
        self.assertEqual(s.simplify(d["incoming_flux_square_residual"]), 0)
        self.assertEqual(s.simplify(d["harmonic_moment_integrand_residual"]), 0)
        self.assertEqual(s.simplify(d["kernel_inverse_cancellation"]), 0)

    def test_compact_first_jet_fixture_has_an_initial_not_new_tidal_tail(self):
        d = self.module().derive_fixture()
        for name, residual in d["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)
        self.assertNotEqual(d["initial_exterior_Weyl_xx"], 0)
        self.assertFalse(d["initial_tidal_data_compact"])
        self.assertFalse(d["zero_past_realization"])
        self.assertEqual(d["initial_scalar_field"], 0)

    def test_positive_lambda_background_is_independently_checked(self):
        d = self.module().derive_background()
        self.assertTrue(all(s.simplify(value) == 0 for value in d["residuals"].values()))
        self.assertEqual(d["Lambda"], 3*d["Hd"]**2)

    def test_free_zero_initial_data_and_stricter_no_tail_class_are_not_external_probe(self):
        d = self.module().run()
        json.dumps(d)
        self.assertTrue(d["checks_passed"])
        self.assertFalse(d["external_signed_probe_identified_with_canonical_delta_T"])
        self.assertFalse(d["zero_past_unforced_nontrivial_matter_claimed"])
        self.assertEqual(d["compact_laplacian_data_result"], "NO_EXTERIOR_TAIL")
        self.assertEqual(d["compact_first_jet_fixture_result"], "INITIAL_TIDAL_TAIL_ALREADY_PRESENT")
        self.assertFalse(d["nonlinear_constraint_completion_claimed"])

    def test_unforced_cauchy_moment_has_a_strict_precone_curvature_bound(self):
        module = self.module()
        self.assertTrue(hasattr(module, "derive_cauchy_response"),
                        "The unforced physical Cauchy response has not been derived")
        d = module.derive_cauchy_response()
        for name, residual in d["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)
        self.assertEqual(d["normalized_damping_bound"], 9)
        self.assertEqual(d["normalized_mass_bound"], 18)
        self.assertEqual(d["green_derivative_lower_bound"], s.Rational(211, 400))
        self.assertTrue(d["inner_ball_abs_Weyl_lower_bound"].is_positive)
        self.assertTrue(d["outside_light_cone_margin_bound"].is_positive)
        self.assertFalse(d["initial_Weyl_is_independent_Cauchy_datum"])

    def test_annular_data_are_identical_to_background_in_the_inner_ball(self):
        module = self.module()
        self.assertTrue(hasattr(module, "derive_annular_fixture"))
        d = module.derive_annular_fixture()
        for name, residual in d["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)
        for field in d["initial_inner_ball_fields"].values():
            entries = list(field) if isinstance(field, s.MatrixBase) else [field]
            self.assertTrue(all(s.simplify(entry) == 0 for entry in entries))
        self.assertNotEqual(d["initial_inner_ball_Weyl_xy"], 0)
        self.assertTrue(d["torus_mean_zero_by_parity"])

    def test_healthy_linear_cauchy_failure_is_not_a_zero_past_actuator_claim(self):
        module = self.module()
        result = module.run()
        self.assertIn("healthy_linear_cauchy_gate", result)
        self.assertEqual(result["healthy_linear_cauchy_gate"], "FAIL")
        self.assertFalse(result["zero_past_unforced_nontrivial_matter_claimed"])
        self.assertFalse(result["nonlinear_constraint_completion_claimed"])
        self.assertTrue(hasattr(module, "main"))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main([]), 0)
            self.assertEqual(module.main(["--require-cauchy-locality"]), 2)


if __name__ == "__main__":
    unittest.main()
