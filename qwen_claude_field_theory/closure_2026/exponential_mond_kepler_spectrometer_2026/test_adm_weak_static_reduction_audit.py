#!/usr/bin/env python3
"""Tests for the explicit ADM-to-weak-static branch reduction."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

import sympy as sp


HERE = Path(__file__).resolve().parent
PATH = HERE / "adm_weak_static_reduction_audit.py"
SPEC = importlib.util.spec_from_file_location("adm_reduction", PATH)
ADM = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ADM)


class ADMReductionTests(unittest.TestCase):
    def test_spatial_ricci_scalar_is_generated_from_metric(self) -> None:
        direct = ADM.derive_spatial_ricci_direct()
        self.assertEqual(direct["residual"], 0)
        self.assertGreater(direct["nonzero_christoffel_components"], 0)

    def test_eh_density_reduces_after_integration_by_parts(self) -> None:
        d = ADM.derive_reduction()
        self.assertEqual(d["eh_residual"], 0)
        self.assertEqual(
            sp.simplify(
                d["eh_post_ibp"]
                - (-2 * d["grad_phi_dot_grad_psi"] + d["grad_psi_squared"])
            ),
            0,
        )

    def test_exact_exponential_is_retained_at_leading_post_newtonian_order(self) -> None:
        d = ADM.derive_reduction()
        self.assertEqual(d["y_residual"], 0)
        self.assertEqual(d["mond_residual"], 0)
        self.assertTrue(d["mond_leading"].has(sp.exp(-d["u"] / d["a0"])))

    def test_wrong_ell0_scaling_loses_the_finite_mond_argument(self) -> None:
        bad = ADM.derive_reduction(ell0_epsilon_power=0)
        self.assertNotEqual(bad["y_residual"], 0)

    def test_point_particle_and_planck_G_relation_give_poisson_normalization(self) -> None:
        d = ADM.derive_reduction()
        self.assertEqual(d["particle_residual"], 0)
        self.assertEqual(d["dust_source_residual"], 0)
        self.assertEqual(d["high_y_poisson_residual"], 0)

    def test_wrong_planck_scaling_breaks_dust_normalization(self) -> None:
        bad = ADM.derive_reduction(planck_epsilon_power=-1)
        self.assertNotEqual(bad["dust_source_residual"], 0)

    def test_lambda_fixed_a0_scaling_removes_only_field_dependent_leading_term(self) -> None:
        good = ADM.derive_reduction(cosmological_epsilon_power=2)
        bad = ADM.derive_reduction(cosmological_epsilon_power=1)
        self.assertEqual(good["cosmological_field_residual"], 0)
        self.assertNotEqual(bad["cosmological_field_residual"], 0)

    def test_static_auxiliary_branch_is_explicit(self) -> None:
        d = ADM.derive_reduction()
        self.assertEqual(d["auxiliary_trace_residual"], 0)
        self.assertEqual(d["lambda_euler_nonzero_k_residual"], 0)
        self.assertEqual(d["lambda_euler_k0"], 0)
        self.assertEqual(d["K_ij_branch"], 0)
        self.assertEqual(d["D2lambda_branch"], 0)
        self.assertEqual(d["barK_ij_branch"], 0)
        self.assertEqual(
            sp.diff(d["auxiliary_fourier_density"], d["lambda_dot_k"], 2),
            d["auxiliary_velocity_hessian"],
        )
        self.assertEqual(d["auxiliary_velocity_hessian"], 0)

    def test_cartesian_density_reduces_to_radial_measure(self) -> None:
        d = ADM.derive_reduction()
        self.assertEqual(d["spherical_reduction_residual"], 0)
        self.assertEqual(d["radial_u_residual"], 0)

    def test_spatial_sign_mutation_fails_target_reduction(self) -> None:
        good = ADM.derive_reduction(spatial_exponent_sign=-1)
        bad = ADM.derive_reduction(spatial_exponent_sign=1)
        self.assertEqual(good["eh_residual"], 0)
        self.assertNotEqual(bad["eh_residual"], 0)

    def test_doubled_gravitational_prefactor_is_detected(self) -> None:
        bad = ADM.derive_reduction(action_prefactor=sp.Integer(1))
        self.assertNotEqual(bad["eh_residual"], 0)

    def test_recorded_ledger_matches_live_reduction(self) -> None:
        import json

        recorded = json.loads((HERE / "adm_reduction_results.json").read_text())
        self.assertEqual(recorded, ADM.build_results())


if __name__ == "__main__":
    unittest.main(verbosity=2)
