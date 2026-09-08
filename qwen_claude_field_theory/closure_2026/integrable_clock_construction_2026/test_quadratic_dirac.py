"""Independent controls for the finite IC-2 quadratic Dirac calculation."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest

import sympy as s

HERE = Path(__file__).resolve().parent
_MODEL = None


class QuadraticDiracTests(unittest.TestCase):
    def model(self):
        global _MODEL
        path = HERE / "quadratic_dirac.py"
        self.assertTrue(path.exists(), "The quadratic Dirac implementation is missing")
        if _MODEL is None:
            spec = importlib.util.spec_from_file_location("quadratic_dirac_under_test", path)
            _MODEL = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_MODEL)
        return _MODEL

    def assert_zero(self, values):
        for name, value in values.items():
            with self.subTest(identity=name):
                entries = list(value) if isinstance(value, s.MatrixBase) else [value]
                self.assertTrue(all(s.simplify(entry) == 0 for entry in entries))

    def test_gauge_restoration_uses_actual_adm_and_a_density_pullback(self):
        d = self.model().derive_gauge()
        self.assert_zero(d["residuals"])
        self.assertEqual(d["linear_Knum"][0, 0], d["zd"] + d["Ed"] - d["k"]*d["shift"])
        self.assertEqual(d["linear_Knum"][1, 1], d["zd"])
        self.assertEqual(s.factor(d["linear_R"]-4*d["k"]**2*d["z"]/d["B"]**2), 0)

    def test_actual_legendre_map_retains_the_E_cross_velocity(self):
        d = self.model().derive_nonzero()
        self.assertEqual(s.factor(d["velocity_hessian"].det()+4*d["F"]**2), 0)
        self.assertEqual(s.factor(d["momenta_from_L"]["p_E"]
            +2*d["F"]*(d["zd"]+d["h"]*(-2*d["n"]+3*d["v"]/4))), 0)
        self.assert_zero(d["residuals"])

    def test_nonzero_mode_has_a_generated_first_class_chain_and_one_pair(self):
        d = self.model().derive_nonzero()
        self.assertEqual(len(d["primary_constraints"]), 3)
        self.assertEqual(len(d["secondary_constraints"]), 3)
        self.assertEqual(d["constraint_gradient_rank"], 6)
        self.assertEqual(d["poisson_rank"], 4)
        self.assertEqual((d["first_class"], d["second_class"], d["physical_pairs"]), (2, 4, 1))
        self.assertEqual(s.factor(d["secondary_constraints"][2]+d["k"]*d["pE"]), 0)
        self.assertEqual(s.factor(d["poisson_matrix"][3, 4]-2*d["F"]*d["h"]**3*d["x"]), 0)

    def test_regular_minor_is_derived_and_positive_on_the_whole_mode_domain(self):
        d = self.model().derive_nonzero()
        expected = 6*d["F"]**2*d["h"]**4*(8*d["Tcal"]+d["x"]-54)
        self.assertEqual(s.factor(d["auxiliary_hessian"].det()-expected), 0)
        self.assertTrue(d["regular_minor_positive"])
        self.assertIn("constraint_independence_minor", d, "Generic rank needs a regular-domain minor")
        self.assertEqual(s.factor(d["constraint_independence_minor"]+d["k"]*expected), 0)

    def test_preservation_includes_the_time_dependent_measure_and_wave_number(self):
        d = self.model().derive_nonzero()
        self.assert_zero(d["preservation_residuals"])
        self.assertTrue(any(s.simplify(value) != 0 for value in d["explicit_secondary_time_derivatives"]))
        self.assertTrue(any(s.simplify(value) != 0 for value in d["frozen_coefficient_preservation_residuals"]))
        self.assert_zero(d["multiplier_evolution_residuals"])

    def test_reduced_hamiltonian_keeps_both_boundary_canonical_maps(self):
        d = self.model().derive_nonzero()
        self.assert_zero(d["reduced_residuals"])
        self.assertEqual(s.factor(d["source_boundary_generator"]+9*d["F"]*d["h"]*d["z"]**2), 0)
        self.assertEqual(s.factor(d["boundary_removed_H"]
            -d["P"]**2/(4*d["F"]*d["a"])+d["F"]*d["h"]**2*d["g"]*d["z"]**2), 0)

    def test_genuine_homogeneous_mode_is_derived_without_E_or_shift(self):
        module = self.model()
        d, local = module.derive_homogeneous(), module.derive_nonzero()
        self.assert_zero(d["residuals"])
        self.assert_zero(d["preservation_residuals"])
        self.assertEqual((len(d["coordinates"]), d["first_class"], d["second_class"], d["physical_pairs"]), (3, 0, 4, 1))
        self.assertEqual(s.factor(d["kinetic"]-(4*d["Tcal"]-27)/9), 0)
        self.assertNotEqual(s.factor(local["a"].subs(local["x"], 0)-d["kinetic"]), 0)
        self.assertIn("constraint_independence_minor", d)
        self.assertEqual(s.factor(d["constraint_independence_minor"]-d["auxiliary_hessian"].det()), 0)

    def test_report_is_json_safe_and_refuses_a_full_nonlinear_count(self):
        module = self.model()
        report = module.run()
        json.dumps(report, allow_nan=False)
        self.assertTrue(report["checks_passed"])
        self.assertTrue(report["input_hash_matches"])
        self.assertFalse(report["full_nonlinear_count_proved"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main([]), 0)
            self.assertEqual(module.main(["--require-full-nonlinear-count"]), 2)

    def test_ic4_recomputes_its_changed_constraint_brackets_and_minor(self):
        module = self.model()
        self.assertTrue(hasattr(module, "derive_ic4"), "The IC-4 action has not been independently reduced")
        d = module.derive_ic4()
        self.assert_zero(d["residuals"])
        self.assert_zero(d["preservation_residuals"])
        self.assert_zero(d["multiplier_evolution_residuals"])
        self.assertEqual((d["constraint_gradient_rank"], d["poisson_rank"], d["first_class"],
                          d["second_class"], d["physical_pairs"]), (6, 4, 2, 4, 1))
        self.assertEqual(d["poisson_matrix"][3, 4], 0)
        expected = 3*d["F"]**2*d["h"]**4*(4*d["Tcal"]-27)*(8*d["Tcal"]+d["x"])/(2*d["Tcal"])
        self.assertEqual(s.factor(d["auxiliary_hessian"].det()-expected), 0)
        self.assertIn("constraint_independence_minor", d)
        self.assertEqual(s.factor(d["constraint_independence_minor"]+d["k"]*expected), 0)

    def test_ic4_canonical_reconstruction_and_local_wave_follow_from_its_H(self):
        module = self.model()
        self.assertTrue(hasattr(module, "derive_ic4"), "The IC-4 Hamiltonian is missing")
        d = module.derive_ic4()
        self.assert_zero(d["reduced_residuals"])
        self.assert_zero(d["readout_residuals"])
        self.assertIn("shift_canonical", d["readout_residuals"], "The shift readout also needs canonical matching")
        self.assertEqual(s.diff(d["a"], d["x"]), 0)
        self.assertEqual(s.factor(d["actual_acceleration"]+3*d["h"]*d["zd"]
                                 +d["h"]**2*d["sigma"]*d["x"]*d["z"]), 0)


if __name__ == "__main__":
    unittest.main()
