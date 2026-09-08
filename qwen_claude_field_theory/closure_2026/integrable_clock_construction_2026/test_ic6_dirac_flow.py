#!/usr/bin/env python3
"""Regression controls for the full-metric IC6 homogeneous Dirac flow."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np

PATH = Path(__file__).with_name("ic6_dirac_flow.py")


class DiracFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = None
        if PATH.exists():
            spec = importlib.util.spec_from_file_location("ic6_dirac_flow_tested", PATH)
            cls.module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.module)

    def model(self):
        self.assertIsNotNone(self.module, "The IC6 canonical flow implementation is missing")
        return self.module

    def test_isotropic_witness_has_independent_exact_velocity_and_mass(self):
        # Catches missing volume/momentum dependence and altered action constants.
        m = self.model()
        f = np.exp(-0.5)
        y = np.array([1., 1., 1., 0., 0., 0., -f, -f, -f, 0., 0., 0., .25, 2./3.])
        d = m.evaluate(y)
        np.testing.assert_allclose(d["secondary"], 0., atol=3e-13)
        np.testing.assert_allclose(d["velocity"][:6], [2., 2., 2., 0., 0., 0.], atol=3e-13)
        np.testing.assert_allclose(d["velocity"][6:12], [-f, -f, -f, 0., 0., 0.], atol=3e-13)
        np.testing.assert_allclose(d["multipliers"], 0., atol=3e-13)
        T = -27./16.+54./(5.*np.log(9./5.))
        np.testing.assert_allclose(d["K"], -f*np.array([[24., -27.], [-27., 2.*T+135./8.]]), atol=4e-12)
        # At g=I, an off-diagonal canonical momentum p_12=2*pi^12
        # contributes A=p_12^2/2, hence H_pp=2*exp(1/2) at F=0.
        H = m.jets(y)
        np.testing.assert_allclose(np.diag(H.h)[9:12], 2.*np.exp(.5), atol=3e-13)

    def test_covariant_value_and_all_canonical_derivatives_agree(self):
        # Catches incorrect off-diagonal canonical factors and frozen metric.
        m = self.model()
        result = m.derivative_audit(m.initial_state(constrained=False))
        self.assertLess(result["covariant_value_error"], 2e-13)
        self.assertLess(result["complex_step_gradient_error"], 2e-11)
        self.assertLess(result["finite_difference_hessian_error"], 2e-7)
        self.assertGreater(result["wrong_offdiagonal_factor_error"], 1e-4)

    def test_full_poisson_matrix_computes_nonzero_omega_and_rank(self):
        # Catches assigned ranks, deleted Omega, and the wrong primary sign.
        m = self.model()
        y = m.initial_state()
        d = m.evaluate(y)
        O = d["poisson_matrix"]
        np.testing.assert_allclose(O+O.T, 0., atol=2e-12)
        np.testing.assert_allclose(O[:2, 2:], -d["K"], atol=2e-12)
        np.testing.assert_allclose(O[2:, 2:], d["Omega"], atol=2e-12)
        self.assertEqual(np.linalg.matrix_rank(O, tol=1e-9), 4)
        self.assertEqual(d["constraint_rank"], np.linalg.matrix_rank(O, tol=1e-9))
        self.assertGreater(np.max(np.abs(d["Omega"])), 1e-3)
        self.assertGreater(np.linalg.norm(d["drift"]), 1e-3)
        self.assertLess(np.max(np.abs(d["tangency"])), 2e-12)
        self.assertLess(np.max(np.abs(d["secondary"])), 1e-11)
        self.assertEqual(d["homogeneous_configuration_count"], 6)

    def test_frozen_metric_and_zero_multiplier_controls_fail_preservation(self):
        # Removing either actual preservation term must visibly fail.
        m = self.model()
        d = m.evaluate(m.initial_state())
        self.assertGreater(np.max(np.abs(d["frozen_metric_tangency"])), 1e-3)
        self.assertGreater(np.max(np.abs(d["zero_multiplier_tangency"])), 1e-3)

    def test_integrated_unprojected_flow_preserves_constraints_with_refinement(self):
        # Catches a static re-solve disguised as evolution and wrong multiplier sign.
        m = self.model()
        coarse = m.integrate(16, end_time=.08)
        fine = m.integrate(32, end_time=.08)
        self.assertGreater(fine["state_displacement"], .1)
        self.assertGreater(fine["auxiliary_displacement"], 1e-5)
        # RK4 internal predictor stages are only second-order approximations.
        # Fourth-order accuracy applies to completed time steps.
        self.assertLess(fine["max_accepted_secondary_residual"], 1e-7)
        self.assertLess(fine["max_accepted_secondary_residual"], coarse["max_accepted_secondary_residual"]/8.)
        self.assertLess(fine["max_accepted_energy_error"], 1e-7)
        self.assertLess(fine["max_accepted_primary_residual"], 1e-10)
        self.assertEqual(fine["computed_ranks"], [4])
        self.assertGreater(fine["minimum_metric_eigenvalue"], .9)
        self.assertGreater(fine["minimum_JT"], .9)
        self.assertLess(fine["maximum_activation_distance"], .25)
        self.assertEqual(fine["auxiliary_newton_solves_after_initialization"], 0)

    def test_exact_invariant_brackets_and_actual_block_inverse(self):
        # Catches a normalized-momentum convention error or a fake matrix inverse.
        m = self.model()
        audit = m.invariant_audit(m.initial_state())
        self.assertEqual(audit["exact_polynomial_residuals"], ["0", "0", "0"])
        self.assertLess(audit["invariant_drift_error"], 1e-11)
        self.assertLess(audit["invariant_Omega_error"], 1e-11)
        self.assertLess(audit["left_inverse_residual"], 2e-12)
        self.assertLess(audit["right_inverse_residual"], 2e-12)

    def test_source_pin_rejection_and_branch_exclusion(self):
        # Catches ignoring changed authoritative input or leaving the defined branch.
        m = self.model()
        self.assertTrue(m.verify_sources())
        bad = dict(m.INPUTS)
        bad["IC5_ACTION.md"] = "0"*64
        with self.assertRaises(RuntimeError):
            m.verify_sources(bad)
        y = m.initial_state()
        y[-1] = 1.01
        with self.assertRaises(ValueError):
            m.evaluate(y)


if __name__ == "__main__":
    unittest.main()
