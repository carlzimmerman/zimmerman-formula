import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class ClockGradientRepairGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        proc = subprocess.run(
            [sys.executable, "-B", "clock_gradient_repair_gate.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        cls.proc = proc
        cls.data = json.loads((ROOT / "run_001" / "clock_gradient_repair_results.json").read_text())

    def test_script_exits_cleanly(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_explicit_clock_is_healthy_on_scan(self):
        self.assertTrue(self.data["positive_K_X_scan"])
        self.assertTrue(self.data["positive_Sigma_scan"])
        self.assertTrue(self.data["positive_clock_c_s2_scan"])
        self.assertTrue(self.data["subluminal_clock_c_s2_scan"])

    def test_repaired_symbol_is_positive_and_subluminal(self):
        self.assertTrue(self.data["combined_positive_frequency_coefficient"])
        self.assertTrue(self.data["combined_subluminal_scan"])
        self.assertGreater(self.data["combined_min_c_s2"], 0)

    def test_counted_scalar_is_not_hidden(self):
        self.assertTrue(self.data["explicit_propagating_clock"])
        self.assertEqual(self.data["acceleration_sector_at_y0"], "0")


if __name__ == "__main__":
    unittest.main()
