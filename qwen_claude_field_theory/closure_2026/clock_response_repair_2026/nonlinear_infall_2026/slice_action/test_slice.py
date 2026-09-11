#!/usr/bin/env python3
"""Test-first checks for the exact initial-slice reduction; no numerical BVP."""
import importlib.util
from pathlib import Path
import unittest

import sympy as s

_audit = None


class InitialSliceTests(unittest.TestCase):
    def audit(self):
        global _audit
        path = Path(__file__).with_name("derive.py")
        self.assertTrue(path.is_file(), "The exact action-to-slice reduction is not implemented")
        if _audit is None:
            spec = importlib.util.spec_from_file_location("slice_derivation", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _audit = mod.build_audit()
        return _audit

    def test_full_action_euler_equations_reduce_to_claimed_slice(self):
        audit = self.audit()
        required = {
            "tau_covariant_variation", "slice_hamiltonian", "slice_momentum",
            "slice_metric_trace", "slice_chi_current", "slice_tau_preservation",
            "radial_metric_tracefree", "angular_acceleration", "lapse_elimination",
            "geodesic_areal_acceleration", "background_subtracted_areal_acceleration",
        }
        self.assertTrue(required.issubset(audit["checks"]))
        self.assertTrue(all(audit["checks"].values()))

    def test_generated_clock_gradient_changes_lapse_principal_coefficient(self):
        audit = self.audit()
        q, W, d = (audit["symbols"][name] for name in ("q", "W", "d"))
        actual = audit["expressions"]["lapse_principal"]
        self.assertEqual(s.cancel(actual-(W-2*q**2*d)), 0)
        self.assertNotEqual(s.cancel(actual-W), 0)
        self.assertEqual(s.cancel(audit["expressions"]["Qdot_laplacian_coefficient"]), 0)

    def test_baryon_free_and_uncoupled_controls(self):
        audit = self.audit()
        for name in ("background_tau", "background_flow_H", "background_flow_q",
                     "background_lapse_source", "gamma_zero_lapse", "gamma_zero_current",
                     "mass_constraint", "regular_origin", "vacuum_exterior"):
            self.assertTrue(audit["checks"][name], name)

    def test_matter_starts_to_move_and_conserves_rest_mass(self):
        audit = self.audit()
        for name in ("dust_rest_sources", "dust_generated_gradient", "dust_slice_continuity"):
            self.assertTrue(audit["checks"][name], name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
