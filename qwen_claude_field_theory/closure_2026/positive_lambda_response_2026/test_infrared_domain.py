"""Exact nonlinear infrared-domain controls, not an on-shell exclusion test."""
import contextlib
import importlib.util
import io
import json
import unittest

import sympy as s


class InfraredDomainTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("infrared_domain"),
                             "The nonlinear infrared domain screen is not implemented")
        import infrared_domain
        return infrared_domain

    def test_actual_metric_curvature_and_compact_support_ibp_identity(self):
        d = self.module().derive()
        self.assertEqual(d["ricci_residual"], 0)
        self.assertEqual(d["density_ibp_residual"], 0)
        self.assertEqual(d["phi_curvature_residual"], 0)
        self.assertEqual(d["phi_density_ibp_residual"], 0)

    def test_charge_of_the_explicit_conformal_family_is_exactly_quadratic(self):
        d = self.module().derive()
        self.assertEqual(s.simplify(d["profile_charge"]
                                   -32*s.pi*d["epsilon"]**2*d["A"]), 0)
        self.assertTrue(d["profile_charge"].is_positive)
        self.assertEqual(d["background_metric_residual"], s.zeros(3))

    def test_curved_laplacian_flux_fixes_the_exterior_monopole_sign(self):
        d = self.module().derive()
        self.assertEqual(d["curved_flux_residual"], 0)
        self.assertEqual(d["enclosed_charge_derivative_residual"], 0)
        self.assertEqual(d["exterior_flux_residual"], 0)
        self.assertEqual(s.simplify(d["exterior_potential"]-d["Q"]/(4*s.pi*d["r"])), 0)

    def test_exact_shell_norm_and_action_difference(self):
        d = self.module().derive()
        self.assertEqual(s.simplify(d["shell_norm"]
            -d["Q"]**2*(d["L2"]-d["L1"])/(4*s.pi)), 0)
        self.assertEqual(s.simplify(d["shell_action"]
            +d["b"]*d["tau_T"]*d["Q"]**2*(d["L2"]-d["L1"])/(96*s.pi)), 0)
        self.assertEqual(d["action_limit"], -s.oo)

    def test_the_divergence_is_invisible_through_cubic_amplitude_order(self):
        d = self.module().derive()
        self.assertEqual(d["zero_amplitude_jets"], [0]*4)
        self.assertEqual(d["first_nonzero_amplitude_order"], 4)
        self.assertEqual(s.simplify(d["profile_action_slope"].subs(
            {d["epsilon"]: s.Rational(1, 2), d["A"]: 1,
             d["b"]: 1, d["tau_T"]: 1})+2*s.pi/3), 0)

    def test_zero_monopole_dipole_control_has_finite_exterior_norm(self):
        d = self.module().derive()
        self.assertEqual(d["dipole_laplace_residual"], 0)
        self.assertEqual(d["dipole_flux"], 0)
        self.assertEqual(s.simplify(d["dipole_tail_norm"]
                                   -d["dipole_strength"]**2/(12*s.pi*d["R"])), 0)
        self.assertEqual(s.simplify(d["monopole_gradient_tail"]
                                   -d["Q"]**2/(4*s.pi*d["R"])), 0)

    def test_vanishing_coefficient_and_unperturbed_background_are_separate_controls(self):
        d = self.module().derive()
        self.assertEqual(d["profile_action_slope"].subs(d["b"], 0), 0)
        self.assertEqual(d["profile_action_slope"].subs(d["tau_T"], 0), 0)
        self.assertEqual(d["profile_charge"].subs(d["epsilon"], 0), 0)

    def test_json_and_cli_report_only_the_unprojected_offshell_domain_failure(self):
        mod = self.module()
        data = json.loads(json.dumps(mod.run()))
        self.assertTrue(data["checks_passed"])
        self.assertEqual(data["unprojected_R3_domain_gate"], "FAIL")
        self.assertFalse(data["all_onshell_perturbations_excluded"])
        self.assertFalse(data["compact_projected_theories_excluded"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(mod.main([]), 0)
            self.assertEqual(mod.main(["--require-finite-domain"]), 2)


if __name__ == "__main__":
    unittest.main()
