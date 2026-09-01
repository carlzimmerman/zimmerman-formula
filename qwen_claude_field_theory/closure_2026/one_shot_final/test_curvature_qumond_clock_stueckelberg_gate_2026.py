#!/usr/bin/env python3
"""Regression tests for the restored-clock curvature-QUMOND audit."""

from __future__ import annotations

import unittest

import sympy as sp

from curvature_qumond_clock_stueckelberg_gate_2026 import (
    derive_clock_stueckelberg_gate,
)


class ClockStueckelbergGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = derive_clock_stueckelberg_gate()

    def test_restored_clock_is_boundary_only_on_flat_branch(self) -> None:
        gauge = self.result["gauge"]
        action = self.result["quadratic_action"]

        self.assertTrue(all(item == 0 for item in gauge["invariant_residuals"]))
        self.assertEqual(gauge["lagrangian_variation"], 0)
        self.assertEqual(action["total_derivative_residual"], 0)
        self.assertEqual(action["clock_euler_lagrange"], 0)
        self.assertEqual(
            sp.simplify(
                action["direct_clock_primary"]
                - action["p_pi"]
                + 2
                * action["k"] ** 2
                * (action["ell"] - 2 * action["zeta"])
            ),
            0,
        )

    def test_dirac_chain_leaves_nonclock_gauge_invariant_scalar(self) -> None:
        canonical = self.result["canonical"]
        mode = self.result["mode"]

        self.assertEqual(canonical["velocity_rank"], 3)
        self.assertEqual(canonical["velocity_nullity"], 4)
        self.assertEqual(canonical["constraint_pb_rank"], 2)
        self.assertEqual(canonical["first_class_count"], 5)
        self.assertEqual(canonical["second_class_count"], 2)
        self.assertEqual(canonical["physical_scalar_dof"], 1)
        self.assertEqual(canonical["clock_primary_preservation"], 0)
        self.assertTrue(all(item == 0 for item in canonical["closure_residuals"]))
        self.assertEqual(
            sp.simplify(
                mode["reduced_lagrangian"]
                - 6 * mode["zeta_dot"] ** 2
                + 2 * mode["k"] ** 2 * mode["zeta"] ** 2
            ),
            0,
        )
        self.assertEqual(
            sp.simplify(
                mode["canonical_lagrangian"]
                - mode["v_dot"] ** 2 / 2
                + mode["k"] ** 2 * mode["v"] ** 2 / 6
            ),
            0,
        )
        self.assertEqual(mode["sound_speed_squared"], sp.Rational(1, 3))
        self.assertEqual(mode["clock_projection"], 0)

    def test_lambda_and_cosmological_constant_are_independent_gates(self) -> None:
        background = self.result["background"]

        self.assertEqual(background["luminal_lambda_solutions"], [0])
        self.assertEqual(background["tensor_speed_Lambda_derivative"], 0)
        self.assertEqual(background["flat_vacuum_Lambda_solutions"], [0])
        self.assertEqual(background["vacuum_flrw_compatibility_Lambda_solutions"], [0])
        self.assertEqual(background["coasting_barotropic_w_at_zero_Lambda"], [sp.Rational(-1, 3)])
        self.assertNotEqual(background["matter_coasting_condition"], 0)


if __name__ == "__main__":
    unittest.main()
