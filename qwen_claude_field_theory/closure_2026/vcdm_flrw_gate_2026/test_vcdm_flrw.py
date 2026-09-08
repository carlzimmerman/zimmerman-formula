"""Controls for a variational FLRW gate, not a gravity certification suite."""
import importlib.util
import unittest

import sympy as s


class FLRWTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("vcdm_flrw"), "FLRW derivation is not implemented")
        import vcdm_flrw
        return vcdm_flrw

    def test_raw_adm_and_integrated_trace_actions_agree(self):
        d = self.module().derive_nonzero_mode()
        self.assertEqual(d["boundary_residual"], 0)
        self.assertEqual(d["background_tadpole_residual"], 0)

    def test_unmodified_high_momentum_control(self):
        d = self.module().derive_nonzero_mode()
        canonical = {d["alpha"]: 0, d["D"]: 1, d["Z"]: 1}
        self.assertEqual(s.limit(d["kinetic"].subs(canonical), d["k"], s.oo), 1)
        self.assertEqual(s.limit(d["omega2"].subs(canonical)/d["physical_k2"], d["k"], s.oo), 1)

    def test_unmodified_radiation_sound_speed_is_not_assigned_light_speed(self):
        d = self.module().derive_nonzero_mode()
        radiation = {d["alpha"]: 0, d["D"]: 6, d["Z"]: 2}
        self.assertEqual(s.limit(d["kinetic"].subs(radiation), d["k"], s.oo), 6)
        self.assertEqual(s.limit(d["omega2"].subs(radiation)/d["physical_k2"], d["k"], s.oo), s.Rational(1, 3))

    def test_eliminated_auxiliaries_satisfy_the_original_variations(self):
        d = self.module().derive_nonzero_mode()
        self.assertEqual(d["constraint_residuals"], [0, 0, 0])

    def test_homogeneous_expanding_control_is_not_discarded(self):
        d = self.module().derive_homogeneous()
        self.assertEqual(d["stiff_solution_residuals"], [0, 0, 0, 0])
        self.assertNotEqual(d["stiff_H"], 0)
        self.assertTrue(d["bracket_antisymmetric"])
        self.assertEqual(d["preservation_residuals"], [0, 0, 0])

    def test_matter_density_mode_is_not_deleted_by_auxiliary_elimination(self):
        d = self.module().derive_nonzero_mode()
        self.assertEqual(s.simplify(d["mond_density"]+3*d["q"]*d["Z"]*d["ud"]), 0)

    def test_canonical_algorithm_preserves_all_secondary_constraints(self):
        mod = self.module()
        d = mod.scalar_dirac(mod.derive_nonzero_mode())
        self.assertEqual(d["preservation_residuals"], [0, 0, 0])
        matrix = s.Matrix(d["poisson_matrix"])
        self.assertEqual(matrix, -matrix.T)
        self.assertNotEqual(d["poisson_determinant"], 0)

    def test_zero_background_matter_limit_is_reclassified_not_divided_by_q(self):
        mod = self.module()
        d = mod.scalar_dirac(mod.derive_nonzero_mode())
        self.assertIn("vacuum_canonical_control", d)
        vac = d["vacuum_canonical_control"]
        self.assertLess(vac["independent_secondary_count"], len(d["secondary"]))
        self.assertGreater(vac["matter_velocity_hessian"], 0)

    def test_V_second_derivative_two_thirds_can_expand_with_matter(self):
        d = self.module().derive_homogeneous()
        self.assertIn("de_sitter_stiff_residuals", d)
        self.assertEqual(d["de_sitter_stiff_residuals"], [0, 0, 0, 0])

    def test_radiation_evolution_checks_expansion_and_tolerance(self):
        mod = self.module()
        self.assertTrue(hasattr(mod, "radiation_evolution"), "Evolving radiation control is not implemented")
        r = mod.radiation_evolution(mod.derive_nonzero_mode())
        self.assertEqual(r["background_residuals"], [0, 0, 0])
        self.assertLess(r["mond_relative_tolerance_change"], 1e-6)
        self.assertGreater(r["mond_growth"], 1e6)
        self.assertLess(r["control_max_abs_u"], 2)


if __name__ == "__main__":
    unittest.main()
