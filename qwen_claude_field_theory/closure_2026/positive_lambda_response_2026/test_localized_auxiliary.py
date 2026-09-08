"""Catch localization signs, omitted lapse/metric derivatives, and false DOF counts."""
import contextlib
import importlib.util
import io
import json
import unittest
from unittest.mock import patch

import sympy as s


class LocalizedAuxiliaryTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("localized_auxiliary"))
        import localized_auxiliary
        return localized_auxiliary

    def test_eliminating_actual_auxiliaries_recovers_both_negative_kernels(self):
        d = self.module().derive_localization_mode()
        m, c, ell, source_u, source_v = (d[key] for key in
            ["m", "c", "eigenvalue", "source_u", "source_v"])
        self.assertEqual(s.factor(d["on_shell_action"]
            + m*source_u**2/(16*ell) + c*source_v**2/ell**2), 0)
        self.assertEqual(d["solution"][d["W"]], 2*c*source_v/ell**2)
        self.assertTrue(all(value == 0 for value in d["auxiliary_equation_residuals"]))

    def test_curved_direct_variations_check_all_four_scalar_equations(self):
        d = self.module().derive_curved_variation()
        self.assertNotEqual(d["ricci_scalar"], 0)
        self.assertEqual(len(d["scalar_el_residuals"]), 4)
        self.assertTrue(all(value == 0 for value in d["scalar_el_residuals"]))
        self.assertEqual(d["integration_by_parts_residual"], 0)

    def test_lapse_variation_includes_the_laplacian_of_the_auxiliary_coupling(self):
        d = self.module().derive_curved_variation()
        x = d["coordinates"][0]
        fixture = {d["zeta"]: 0, d["n"]: 0, d["U"]: x*x,
                   d["V"]: 0, d["W"]: 0}
        actual = s.simplify(d["scalar_el"]["log_lapse"].subs(fixture).doit())
        self.assertEqual(actual, d["m"])

    def test_all_six_metric_components_follow_actual_christoffel_variation(self):
        d = self.module().derive_curved_variation()
        self.assertEqual(len(d["metric_variation_residuals"]), 6)
        self.assertTrue(all(value == 0 for value in d["metric_variation_residuals"]))
        self.assertNotEqual(d["metric_el"][0, 1], 0)

    def test_metric_variation_retains_the_nonminimal_curvature_derivatives(self):
        d = self.module().derive_curved_variation()
        x = d["coordinates"][0]
        fixture = {d["zeta"]: 0, d["n"]: 0, d["U"]: x*x,
                   d["V"]: 0, d["W"]: 0}
        actual = d["metric_el"].subs(fixture).doit().subs(x, 1).applyfunc(s.simplify)
        expected = d["m"]*s.diag(s.Rational(1, 8), -s.Rational(3, 8), -s.Rational(3, 8))
        self.assertEqual(actual, expected)

    def test_auxiliary_constraints_come_from_momenta_and_hamiltonian_brackets(self):
        d = self.module().derive_auxiliary_constraints()
        self.assertEqual(d["velocity_momenta"], [0, 0, 0])
        self.assertEqual(d["poisson_rank"], 6)
        self.assertEqual(d["first_class"], 0)
        self.assertEqual(d["auxiliary_pairs"], 0)
        self.assertEqual(s.factor(d["poisson_matrix"].det()
            - d["m"]**2*d["eigenvalue"]**6/64), 0)

    def test_arbitrary_time_dependent_sources_fix_all_primary_multipliers(self):
        d = self.module().derive_auxiliary_constraints()
        self.assertEqual(len(d["multipliers"]), 3)
        self.assertTrue(all(value == 0 for value in d["preservation_residuals"]))
        self.assertTrue(all(value == 0 for value in d["solution_drift_residuals"]))

    def test_zero_mode_is_not_assigned_the_nonzero_mode_inverse_or_count(self):
        d = self.module().derive_auxiliary_constraints()
        self.assertEqual(d["zero_mode"]["poisson_rank"], 2)
        self.assertIsNone(d["zero_mode"]["auxiliary_pairs_claimed"])
        self.assertNotEqual(d["zero_mode"]["secondary_constraints"][0], 0)

    def test_json_and_cli_report_auxiliary_closure_without_full_theory_closure(self):
        module = self.module()
        result = json.loads(json.dumps(module.run(), allow_nan=False))
        self.assertTrue(result["checks_passed"])
        self.assertTrue(result["nonzero_mode_auxiliary_closure"])
        self.assertEqual(result["auxiliary_pairs"], 0)
        self.assertIsNone(result["full_nonlinear_gravity_count_claimed"])
        self.assertFalse(result["compact_projector_metric_variation_completed"])
        self.assertFalse(result["generic_R3_finite_action_neighborhood_proved"])
        with contextlib.redirect_stdout(io.StringIO()) as stream:
            status = module.main(["--require-auxiliary-closure"])
        self.assertEqual(status, 0)
        self.assertTrue(json.loads(stream.getvalue())["checks_passed"])

    def test_failed_algebra_returns_one_before_the_optional_gate_exit(self):
        module = self.module()
        failed_result = {"checks_passed": False, "nonzero_mode_auxiliary_closure": False}
        for arguments in ([], ["--require-auxiliary-closure"]):
            with self.subTest(arguments=arguments):
                with patch.object(module, "run", return_value=failed_result):
                    with contextlib.redirect_stdout(io.StringIO()):
                        status = module.main(arguments)
                self.assertEqual(status, 1)


if __name__ == "__main__":
    unittest.main()
