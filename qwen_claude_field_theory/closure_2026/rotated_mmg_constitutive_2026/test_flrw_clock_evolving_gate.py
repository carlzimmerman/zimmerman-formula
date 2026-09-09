import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class FLRWClockEvolvingGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        proc = subprocess.run(
            [sys.executable, "-B", "flrw_clock_evolving_gate.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        cls.proc = proc
        cls.data = json.loads((ROOT / "run_001" / "flrw_clock_evolving_results.json").read_text())

    def test_script_exits_cleanly(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_unique_evolving_clock_branch(self):
        self.assertEqual(self.data["unique_root_scan"], 32)
        self.assertTrue(self.data["charge_shape_strictly_increasing_on_0_1"])
        self.assertLess(self.data["relative_current_spread"], 1e-10)

    def test_clock_is_healthy_and_subluminal(self):
        self.assertTrue(self.data["positive_K_chi_scan"])
        self.assertTrue(self.data["positive_Sigma_scan"])
        self.assertTrue(self.data["positive_clock_c_s2_scan"])
        self.assertTrue(self.data["subluminal_clock_c_s2_scan"])


if __name__ == "__main__":
    unittest.main()
