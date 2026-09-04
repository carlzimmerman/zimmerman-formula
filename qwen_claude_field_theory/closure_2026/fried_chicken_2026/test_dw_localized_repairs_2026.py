#!/usr/bin/env python3
"""Independent regressions for the localized DW action audits.

These tests intentionally use a direct reduced Euler--Lagrange projection for
the curvature sign and an independently derived coefficient for the retarded
quadratic branch.  They do not accept a printed PASS flag as evidence.
"""
from pathlib import Path
import subprocess
import sys
import unittest

import sympy as sp

import dw_localized_noether_identity_2026 as ward


HERE = Path(__file__).resolve().parent


class LocalizedDWRepairTests(unittest.TestCase):
    def run_dirac_probe(self, body):
        completed = subprocess.run(
            [sys.executable, "-c", "import sympy as sp; import dw_localized_dirac_count_2026 as d; " + body],
            cwd=HERE,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        return completed.stdout.strip().splitlines()

    def test_curvature_metric_projection_matches_direct_variation(self):
        """The analytic E_00 must match varying the reduced action in N."""
        fpoly = lambda Z: ward.c1 * Z + ward.c2 * Z**2 + ward.c3 * Z**3
        lagrangian, metric_eom, _, _, misc = ward.build_all(fpoly)
        direct = ward.euler_lagrange(lagrangian, ward.N, [ward.t, ward.x])
        projected = misc["sqrtg"] * metric_eom[0, 0] * (2 / ward.N**3)
        self.assertEqual(ward.simplify0(direct - projected), 0)

    def test_retarded_branch_energy_sign_is_derived_from_action(self):
        """For W0=-a0^2/kappa and f'(0)=1/2 the branch energy is positive."""
        # Independent oracle from the homogeneous quadratic action.  With the
        # mostly-plus metric, Z=-4*vX**2/a0**2 and the local kinetic density is
        # -W0*f1*Z + vX*vxi.  Equal retarded Green functions give vxi=-a*vX,
        # where a is the X-X Hessian coefficient.  Derive both coefficients
        # here rather than accepting the audit helper's reported sign.
        kappa, a0, f1 = sp.symbols("kappa a0 f1", positive=True)
        vX, vxi = sp.symbols("vX vxi")
        W0 = -a0**2 / kappa
        Z_homogeneous = -4 * vX**2 / a0**2
        local_kinetic = -W0 * f1 * Z_homogeneous + vX * vxi
        a_from_action = sp.factor(sp.diff(local_kinetic, vX, 2))
        retarded_kinetic = sp.expand(local_kinetic.subs(vxi, -a_from_action * vX))
        retarded_energy = sp.factor(retarded_kinetic.coeff(vX, 2))
        expected_a = sp.factor(a_from_action.subs(f1, sp.Rational(1, 2)))
        expected_energy = sp.factor(retarded_energy.subs(f1, sp.Rational(1, 2)))

        probe = (
            "data=d.localization_quadratic_data(); "
            "print(sp.simplify(data['a_at_f1_half'])); "
            "print(sp.simplify(data['retarded_energy_at_f1_half']))"
        )
        values = self.run_dirac_probe(probe)
        self.assertEqual(values, [str(expected_a), str(expected_energy)])
        self.assertEqual(expected_a, -4 / kappa)
        self.assertEqual(expected_energy, 2 / kappa)
        self.assertNotEqual(expected_energy, -2 / kappa)  # old wrong sign

    def test_hessian_minors_split_generic_and_singular_strata(self):
        values = self.run_dirac_probe(
            "a=d.homogeneous_hessian_data(); "
            "print(sp.factor(a['generic_minor'])); "
            "print(a['rank_Q0_lambda_nonzero']); "
            "print(a['rank_Q0_lambda_zero']); "
            "print(sp.factor(a['Q0_lambda_minor'])); "
            "print(sp.factor(a['Q0_lambda0_minor']))"
        )
        self.assertEqual(values, ["Q**2/N**4", "3", "2", "2*lambda/N**3", "-1/N**2"])

    def test_constraint_matrix_is_computed_and_loses_rank_at_Q_zero(self):
        values = self.run_dirac_probe(
            "a=d.generic_constraint_data(); "
            "print(sp.factor(a['det_pb'])); "
            "print(sp.factor(a['det_pb_on_shell'])); "
            "print(a['rank_generic']); "
            "print(a['formal_off_shell_rank_Q0']); "
            "print(a['generic_chart_valid_at_Q0'])"
        )
        self.assertEqual(values, ["16*Q**2*pnu**4", "16*Q**6", "4", "2", "False"])

    def test_finite_k_and_zero_mode_poles_are_not_conflated(self):
        values = self.run_dirac_probe(
            "a=d.localization_quadratic_data(); "
            "print(sp.factor(a['finite_k_operator_det'])); "
            "print(sp.factor(a['k0_operator_det'])); "
            "print(a['residue_signature']); "
            "print(d.STATUS_UNRESTRICTED_LOCAL); "
            "print(d.STATUS_RETARDED_HISTORY); "
            "print(d.STATUS_Q0_DIRAC)"
        )
        self.assertEqual(
            values,
            ["-(k - omega)**2*(k + omega)**2", "-omega**4", "opposite", "DEAD", "OPEN_NONCANONICAL", "OPEN"],
        )

    def test_clock_transport_symbol_has_only_zero_frequency_roots(self):
        values = self.run_dirac_probe(
            "a=d.clock_transport_symbol_data(); print(sp.factor(a['det_operator']))"
        )
        self.assertEqual(values, ["-4*omega**4"])

    def test_dirac_audit_script_completes_its_internal_controls(self):
        completed = subprocess.run(
            [sys.executable, "dw_localized_dirac_count_2026.py"],
            cwd=HERE,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("computational checks passed: 20/20", completed.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
