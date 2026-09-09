import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fqtheta_gate as gate


class FQThetaTests(unittest.TestCase):
    def test_homogeneous_action_and_hessian_are_varied(self):
        r = gate.homogeneous_variation()
        self.assertEqual(sp.simplify(r["L_reconstructed"] - r["L"]), 0)
        self.assertEqual(sp.simplify(r["mixed_entry"] - 3*r["a"]**2*r["Fq"]/r["N"]), 0)
        expected = 3*r["a"]**4/r["N"]**2 * (2*r["M2"]*r["Kqq"] - 3*r["Fq"]**2 - 6*r["M2"]*r["adot"]/(r["N"]*r["a"])*r["Fqq"])
        self.assertEqual(sp.simplify(r["detW"] - expected), 0)

    def test_degeneracy_is_solved_not_inserted(self):
        r = gate.homogeneous_variation()
        self.assertEqual(sp.simplify(r["detW_affine_locus"]), 0)
        self.assertEqual(sp.simplify(r["generic_degeneracy"].rhs - (3*r["adot"]*r["Fqq"]/(r["N"]*r["a"])+3*r["Fq"]**2/(2*r["M2"]))), 0)

    def test_static_exponential_and_no_slip_are_independent_variations(self):
        r = gate.static_variation()
        self.assertEqual(sp.simplify(r["mu_identity"]), 0)
        self.assertEqual(sp.simplify(r["psi_eom"]-r["psi_eom_expected"]), 0)
        mu_px = 1-sp.exp(-sp.diff(r["Phi"], r["x"])/r["a0"])
        self.assertEqual(sp.simplify(r["phi_flux_on_slip"] - 4*r["M2"]*mu_px*sp.diff(r["Phi"], r["x"])), 0)
        self.assertEqual(sp.simplify(r["Ftheta_static"]), 0)

    def test_stress_and_charge_are_derived(self):
        r = gate.flrw_stress()
        self.assertEqual(sp.simplify(r["rho"] - (r["K"]-r["Q"]*r["Kq"]+3*r["H"]*r["Q"]*r["Fq"])), 0)
        self.assertEqual(sp.simplify(r["pressure"] - (-r["K"]-r["Fq"]*r["Qdot"])), 0)
        self.assertIn("d_dt", str(r["charge_eom"]))

    def test_witness_exhibits_positive_density_pressureless_but_negative_bare_sound_speed(self):
        r = gate.witness()
        self.assertTrue(r["degenerate"])
        self.assertTrue(r["rho_bare"] > 0)
        self.assertEqual(r["pressure_bare"], 0)
        self.assertTrue(r["bare_sound_speed_sq"] < 0)
        self.assertTrue(r["Fq_at_dust"] != 0)
        self.assertEqual(sp.diff(r["F"], sp.Symbol("Q"), 2), 0)

    def test_affine_charge_elimination_has_no_dust_term(self):
        r = gate.affine_cosmology()
        self.assertEqual(r["identity"], 0)
        self.assertEqual(r["dust_coefficient"], 0)

    def test_cli_records_open_not_certified(self):
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, "-B", str(HERE/"fqtheta_gate.py"), "--output-dir", d],
                               text=True, capture_output=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            data = json.loads((Path(d)/"results.json").read_text())
            self.assertEqual(data["theory_status"], "OPEN")
            self.assertTrue(all(row["passed"] for row in data["checks"]))
            self.assertTrue(data["non_claims"])


if __name__ == "__main__":
    unittest.main()
