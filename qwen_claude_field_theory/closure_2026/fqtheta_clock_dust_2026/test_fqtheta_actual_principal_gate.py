import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fqtheta_actual_principal_gate as gate


class FQThetaActualPrincipalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = gate.build_gate()

    def test_action_jet_is_derived(self):
        jet = gate.derive_action_jet()
        M2 = jet["symbols"]["M2"]
        self.assertEqual(sp.simplify(jet["Uzz"] - 4 * M2), 0)
        self.assertEqual(sp.simplify(jet["Unz"] + 4 * M2), 0)
        self.assertEqual(sp.simplify(jet["Unn"]), 0)
        self.assertEqual(sp.simplify(jet["Unp"]), 0)
        self.assertEqual(sp.simplify(jet["Upp"] - 2 * M2 * jet["Gpp"].subs(
            {sp.Symbol("yy", positive=True): jet["symbols"]["y0"]})), 0)

    def test_affine_dirac_chain_is_nontrivial_and_not_hardcoded(self):
        d = self.data["dirac"]
        self.assertEqual(d["velocity_hessian_determinant"], "0")
        self.assertNotEqual(d["poisson_determinant"], "0")
        local = d["local_k_nonzero"]
        self.assertEqual(local["constraint_jacobian_rank"], local["constraint_count"])
        self.assertEqual(local["poisson_rank"], local["constraint_count"])
        self.assertEqual(local["configuration_dof"], "1")
        self.assertTrue(d["poisson_determinant_independent_of_y0"])

    def test_nonzero_braiding_is_required_for_expanding_dust(self):
        d = self.data["dust_braiding_dichotomy"]
        self.assertTrue(d["f_zero_expanding_requires_A_zero"])
        self.assertTrue(d["f_zero_has_no_dust_term"])
        self.assertIn("C=-A a^3", d["interpretation"])

    def test_k_zero_is_separate_and_rank_jumps(self):
        d = self.data["dirac"]
        self.assertGreater(d["k_zero"]["first_class_count"], 0)
        self.assertEqual(d["k_zero"]["configuration_dof"], "0")
        self.assertNotEqual(d["local_k_nonzero"]["configuration_dof"],
                            d["k_zero"]["configuration_dof"])
        self.assertIn("k**2", d["reduced"]["symplectic_coefficient"])

    def test_exponential_zero_field_limit_is_computed(self):
        c = self.data["constitutive_limits"]
        self.assertEqual(c["Gpp_limit_y0_to_0"], "0")
        self.assertEqual(c["lambda_parallel_limit_y0_to_0"], "0")
        jet = gate.derive_action_jet()
        M2, y0 = jet["symbols"]["M2"], jet["symbols"]["y0"]
        Q0 = sp.Symbol("Q0", nonzero=True, real=True)
        freq = sp.sympify(self.data["dirac"]["reduced"]["frequency_square"],
                          locals={"Q0": Q0, "y0": y0})
        expected = sp.simplify(Q0**2 * jet["Gpp"].subs(
            {sp.Symbol("yy", positive=True): y0}) / 2)
        self.assertEqual(sp.simplify(freq - expected), 0)

    def test_cli_records_open(self):
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, "-B", str(HERE / "fqtheta_actual_principal_gate.py"),
                                "--output", str(Path(d) / "result.json")],
                               text=True, capture_output=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            obj = json.loads((Path(d) / "result.json").read_text())
            self.assertEqual(obj["status"], "OPEN")
            self.assertTrue(obj["non_claims"])


if __name__ == "__main__":
    unittest.main()
