import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causal_support_gate as gate


class CausalSupportGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = gate.build_gate()

    def test_one_branch_and_contrast_are_derived(self):
        checks = self.result["checks"]
        self.assertTrue(checks["six_source_selected_branch_has_no_spatial_pole"])
        self.assertTrue(checks["alternate_branch_exhibits_spatial_pole"])

    def test_wave_speeds_are_not_inserted(self):
        waves = self.result["wave_symbols"]
        self.assertEqual(waves["light_speed_squared"], "1")
        speed = float(sp.sympify(waves["clock_speed_squared"]))
        self.assertGreater(speed, 0)
        self.assertLess(speed, 1)
        self.assertIn("rate**2", waves["clock"])

    def test_cli_records_open_scope(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "causal.json"
            p = subprocess.run([sys.executable, "-B", str(HERE / "causal_support_gate.py"),
                                "--output", str(out)],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            data = json.loads(out.read_text())
            self.assertEqual(data["status"], "OPEN")
            self.assertTrue(all(data["checks"].values()))
            self.assertTrue(data["non_claims"])


if __name__ == "__main__":
    unittest.main()
