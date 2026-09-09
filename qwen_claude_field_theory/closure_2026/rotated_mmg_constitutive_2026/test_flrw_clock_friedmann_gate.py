import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class FLRWClockFriedmannGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        proc = subprocess.run(
            [sys.executable, "-B", "flrw_clock_friedmann_gate.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        cls.proc = proc
        cls.data = json.loads((ROOT / "run_001" / "flrw_clock_friedmann_results.json").read_text())

    def test_script_exits_cleanly(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_continuity_is_exact(self):
        self.assertTrue(self.data["continuity_identity_exact"])
        self.assertTrue(self.data["raychaudhuri_identity_exact"])
        self.assertTrue(self.data["lapse_variation_matches_rho"])
        self.assertTrue(self.data["scale_variation_matches_pressure"])

    def test_dust_to_vacuum_interpolation(self):
        self.assertLess(self.data["early_dust_rho_a3_relative_spread"], 0.01)
        self.assertLess(self.data["late_vacuum_rho_relative_spread"], 0.01)
        self.assertGreater(self.data["w_max"], -1)
        self.assertLess(self.data["w_min"], 0)

    def test_expanding_friedmann_witness(self):
        self.assertTrue(self.data["positive_H_witness"])
        self.assertTrue(self.data["finite_positive_cosmic_time_span"])
        self.assertTrue(self.data["positive_subluminal_clock_scan"])
        self.assertGreater(self.data["c_s2_min"], 0)
        self.assertLess(self.data["c_s2_max"], 1)


if __name__ == "__main__":
    unittest.main()
