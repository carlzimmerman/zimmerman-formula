import unittest

from alc_aether_regularization import build_scan, symbolic_branch


class ALCAetherRegularizationTests(unittest.TestCase):
    def test_ppn_tuning_is_derived_symbolically(self):
        branch = symbolic_branch()
        e, r = branch["symbols"]
        self.assertEqual(str(branch["c13"]), "epsilon*(r + 1)")
        self.assertEqual(str(branch["c123"]), "epsilon*(r + 1)**2/3")
        # The tuned branch has alpha_1=0 by construction; alpha_2's second
        # factor vanishes identically without inserting a numerical target.
        c1, c2, c3, c4 = (branch[name] for name in ("c1", "c2", "c3", "c4"))
        alpha1_num = sp_together(c3**2 + c1*c4)
        alpha2_factor = sp_together(2*c1 + 3*c2 + c3 + c4)
        self.assertEqual(alpha1_num, 0)
        self.assertEqual(alpha2_factor, 0)
        self.assertEqual(branch["alpha1"], 0)
        self.assertEqual(branch["alpha2"], 0)

    def test_regular_passes_are_not_two_tensor_only(self):
        result = build_scan()
        self.assertGreater(result["counts"]["regular_necessary_gate_passes"], 0)
        self.assertEqual(
            result["counts"]["regular_passes_with_extra_scalar"],
            result["counts"]["regular_necessary_gate_passes"],
        )
        for point in result["points"]:
            if point["passes_necessary_ppn_gw_speed_gate"]:
                self.assertNotEqual(point["scalar_kinetic_factor"], 0.0)
                self.assertNotEqual(point["scalar_gradient_factor"], 0.0)

    def test_degenerate_branch_is_reported_separately(self):
        result = build_scan()
        self.assertGreater(result["counts"]["degenerate_or_singular_points"], 0)
        self.assertIn("separate full Dirac", result["interpretation"]["degenerate_branch"])


def sp_together(expr):
    # Keep the test dependency local and explicit; this helper avoids relying
    # on printed forms for exact symbolic cancellation.
    import sympy as sp
    return sp.simplify(expr)


if __name__ == "__main__":
    unittest.main()
