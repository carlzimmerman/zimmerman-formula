"""Tests of an explicit Hamiltonian completion, not a full-theory certificate."""
import contextlib
import importlib.util
import io
from pathlib import Path
import unittest

import sympy as s

MODEL = None


class NonlinearSquareTests(unittest.TestCase):
    def model(self):
        global MODEL
        path = Path(__file__).with_name("nonlinear_square_completion.py")
        self.assertTrue(path.exists(), "Missing nonlinear construction calculation")
        if MODEL is None:
            spec = importlib.util.spec_from_file_location("tested_nonlinear_square", path)
            MODEL = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(MODEL)
        return MODEL

    def test_square_direction_is_solved_from_the_ic4_gradient_matrix(self):
        d = self.model().derive()
        self.assertEqual(s.factor(d["b"]+d["T"]/9+s.Rational(3, 8)), 0)
        self.assertEqual(d["gradient_match"], s.zeros(2))
        self.assertEqual(d["square_hessian"].det(), 0)
        self.assertEqual(d["square_hessian"].rank(), 1)

    def test_quadratic_transfer_uses_rational_remainder_and_coefficient_match(self):
        d = self.model().derive()
        self.assertEqual(d["rational_remainder"], 0)
        self.assertEqual(d["witness_gradient_difference"], 0)
        self.assertEqual(d["curvature_coefficient_match"], 0)

    def test_stationary_full_first_jets_are_unchanged(self):
        self.assertTrue(all(v == 0 for v in self.model().derive()["static_first_jets"]))

    def test_homogeneous_hamiltonian_is_exactly_unchanged(self):
        self.assertEqual(self.model().derive()["homogeneous_difference"], 0)

    def test_algebraic_auxiliary_has_no_spatial_derivative_in_plateau(self):
        d = self.model().derive()
        self.assertEqual(d["passive_gradient_derivative"], 0)
        self.assertEqual(d["coordinate_jacobian"].det(), 1)

    def test_mass_matrix_is_differentiated_at_fixed_canonical_momenta(self):
        d = self.model().derive()
        expected = s.Matrix([[24, -27], [-27, 2*d["T"]+s.Rational(135, 8)]])
        self.assertEqual((d["mass_matrix"]-expected).applyfunc(s.factor), s.zeros(2))
        self.assertEqual(s.factor(d["mass_matrix"].det()-12*(4*d["T"]-27)), 0)

    def test_plateau_metric_legendre_transform_is_nondegenerate_near_witness(self):
        self.assertEqual(self.model().derive()["legendre_residuals"], [0, 0, 0])

    def test_covariant_phase_action_maps_termwise_to_the_same_hamiltonian(self):
        result = self.model().derive()
        self.assertIn("covariant_bridge", result, "Missing covariant action bridge")
        self.assertTrue(all(v == 0 for v in result["covariant_bridge"].values()))

    def test_covariant_auxiliary_momenta_are_varied_and_eliminated(self):
        result = self.model().derive()
        self.assertIn("covariant_elimination", result, "Missing momentum variation")
        self.assertTrue(all(v == 0 for v in result["covariant_elimination"].values()))

    def test_full_auxiliary_second_variation_contains_cross_terms(self):
        result = self.model().derive()
        self.assertIn("second_variation_residual", result, "Missing functional Hessian derivation")
        self.assertEqual(result["second_variation_residual"], 0)

    def test_momentum_constraint_of_the_numeric_tt_seed_is_derived(self):
        result = self.model().derive()
        self.assertIn("TT_momentum_constraint", result)
        self.assertEqual(result["TT_momentum_constraint"], s.zeros(3, 1))

    def test_switch_has_distinct_static_and_expanding_plateaus(self):
        model = self.model()
        for r in (-2., 0., .49, 1.51, 3.):
            self.assertEqual(model.activation(r), 0.)
        for r in (.9, 1., 1.1):
            self.assertEqual(model.activation(r), 1.)
        for r in (.75, .8, 1.15, 1.2):
            self.assertGreater(model.activation(r), 0.)
            self.assertLess(model.activation(r), 1.)

    def test_clock_expansion_switch_is_even_in_canonical_momentum(self):
        model = self.model()
        for r in (.6, .8, .9, 1., 1.1, 1.2, 1.4):
            self.assertEqual(model.activation(r), model.activation(-r))

    def test_inhomogeneous_auxiliary_solution_is_recomputed_and_refined(self):
        d = self.model().numerical()
        self.assertTrue(d["all_converged"])
        self.assertLess(d["maximum_residual"], 1e-8)
        self.assertGreater(d["minimum_hessian_eigenvalue"], 0.)
        self.assertLess(d["maximum_departure_of_r_from_one"], .25)
        self.assertLess(d["refinement_difference_32_64"], d["refinement_difference_16_32"])
        self.assertGreater(d["inhomogeneous_auxiliary_amplitude"], 1e-8)

    def test_grid_solver_varies_the_supplied_hamiltonian_not_a_fixed_fixture(self):
        model = self.model()
        self.assertTrue(hasattr(model, "solve_auxiliary_density"), "Missing reusable actual-density solve")
        d = model.derive()
        perturbed = d["Hnongrad"]+s.Rational(1, 10000)*d["m"]*d["vol"]*d["h0"]**2*d["xi"]
        result = model.solve_auxiliary_density(d, perturbed)
        self.assertTrue(result["all_converged"])
        self.assertNotEqual(result["records"][0]["initial_residual"], model.numerical()["records"][0]["initial_residual"])

    def test_full_theory_request_is_not_satisfied_by_auxiliary_coercivity(self):
        model = self.model()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(model.main(["--symbolic-only"]), 0)
            self.assertEqual(model.main(["--symbolic-only", "--require-full-closure"]), 2)


if __name__ == "__main__":
    unittest.main()
