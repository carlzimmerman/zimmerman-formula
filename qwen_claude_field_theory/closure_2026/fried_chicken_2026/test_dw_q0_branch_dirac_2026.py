#!/usr/bin/env python3
"""Independent regressions for the singular Q=0 DW branch audit.

The production module is loaded dynamically so the RED phase is a clean test
failure when it does not yet exist.  Tests inspect derived matrices and
Hamilton equations; they do not accept printed PASS labels as evidence.
"""
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

import sympy as sp


HERE = Path(__file__).resolve().parent
MODULE = HERE / "dw_q0_branch_dirac_2026.py"


class Q0BranchDiracTests(unittest.TestCase):
    def load_audit(self):
        self.assertTrue(MODULE.exists(), "Q=0 audit module has not been implemented")
        spec = importlib.util.spec_from_file_location("dw_q0_branch_dirac_2026", MODULE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_undivided_hessian_has_the_derived_null_vectors(self):
        q0 = self.load_audit()
        data = q0.undivided_hessian_data()
        self.assertEqual(data["rank_Q0_lambda_nonzero"], 3)
        self.assertEqual(data["rank_Q0_lambda_zero"], 2)
        for residual in data["lambda_nonzero_null_residuals"]:
            self.assertEqual(residual, sp.zeros(4, 1))
        for residual in data["lambda_zero_null_residuals"]:
            self.assertEqual(residual, sp.zeros(4, 1))
        # Differentiating after setting Q=0 would incorrectly make this
        # component vanish and lose the embedded multiplier relation.
        self.assertNotEqual(sp.factor(data["lambda_nonzero_null_vectors"][0][1]), 0)

    def test_lambda_nonzero_chain_uses_the_actual_poisson_matrix(self):
        q0 = self.load_audit()
        data = q0.lambda_nonzero_branch_data()
        self.assertIn("legendre_energy_residual", data)
        self.assertEqual(sp.factor(data["legendre_energy_residual"]), 0)
        self.assertEqual(data["pb_matrix"] + data["pb_matrix"].T, sp.zeros(5))
        self.assertEqual(data["pb_rank"], 4)
        self.assertNotEqual(data["pb_rank_witness"], 0)
        self.assertEqual(
            sp.factor(data["clock_secondary"] - data["clock_secondary_control"]),
            0,
        )
        self.assertEqual(sp.factor(data["null_multiplier_tie_residual"]), 0)
        self.assertEqual(sp.factor(data["clock_velocity_residual"]), 0)
        self.assertEqual(sp.factor(data["transport_velocity_residual"]), 0)
        self.assertEqual(data["intrinsic_formal_first_class_count"], 1)
        self.assertEqual(data["embedded_homogeneous_chain_closes"], True)
        self.assertFalse(data["ordinary_dirac_count_valid_for_embedded_branch"])

    def test_lambda_zero_branch_keeps_transverse_euler_lagrange_equations(self):
        q0 = self.load_audit()
        data = q0.lambda_zero_branch_data()
        self.assertIn("legendre_energy_residual", data)
        self.assertEqual(sp.factor(data["legendre_energy_residual"]), 0)
        self.assertEqual(data["pb_matrix"] + data["pb_matrix"].T, sp.zeros(6))
        self.assertEqual(data["pb_rank"], 4)
        self.assertNotEqual(data["pb_rank_witness"], 0)
        self.assertEqual(len(data["clock_transport_velocity_solutions"]), 2)
        for solution in data["clock_transport_velocity_solutions"]:
            self.assertEqual(sp.factor(solution[0] ** 2 - data["N"] ** 2), 0)
            self.assertEqual(sp.factor(solution[0] * solution[1] - data["c"] * data["N"] ** 2), 0)
        self.assertEqual(data["intrinsic_formal_first_class_count"], 2)
        self.assertEqual(data["embedded_homogeneous_chain_closes"], True)
        self.assertFalse(data["ordinary_dirac_count_valid_for_embedded_branch"])

    def test_q0_fourier_block_retains_opposite_residue_scalars(self):
        q0 = self.load_audit()
        data = q0.q0_fourier_ghost_data()
        self.assertIn("quadratic_expansion_residual", data)
        self.assertEqual(sp.factor(data["quadratic_expansion_residual"]), 0)
        self.assertEqual(sp.factor(data["kinetic_matrix"].det()), -1)
        self.assertEqual(data["kinetic_inertia"], (1, 1, 0))
        self.assertEqual(
            sp.factor(
                data["finite_k_operator_det"]
                + (data["omega"] ** 2 - data["k"] ** 2) ** 2
            ),
            0,
        )
        self.assertEqual(sp.factor(data["k0_operator_det"]), -data["omega"] ** 4)
        self.assertEqual(data["unrestricted_q0_status"], "DEAD")

    def test_spatial_q_constraint_tangency_separates_k_zero(self):
        q0 = self.load_audit()
        data = q0.spatial_q_tangency_data()
        self.assertEqual(sp.factor(data["uM_k0"]), 0)
        self.assertNotEqual(sp.factor(data["uM_finite_k"]), 0)
        self.assertEqual(sp.factor(data["tangency_residual"]), 0)
        self.assertEqual(data["produces_new_constraint"], False)

    def test_executable_audit_completes_all_internal_controls(self):
        self.assertTrue(MODULE.exists(), "Q=0 audit module has not been implemented")
        completed = subprocess.run(
            [sys.executable, str(MODULE)],
            cwd=HERE,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("computational checks passed: 29/29", completed.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
