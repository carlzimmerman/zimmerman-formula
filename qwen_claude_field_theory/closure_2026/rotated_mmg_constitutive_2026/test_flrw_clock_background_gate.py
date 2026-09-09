import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class FLRWClockBackgroundGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        proc = subprocess.run(
            [sys.executable, "-B", "flrw_clock_background_gate.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        cls.proc = proc
        cls.data = json.loads((ROOT / "run_001" / "flrw_clock_background_results.json").read_text())

    def test_script_exits_cleanly(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_expanding_background_forces_zero_Kx(self):
        self.assertTrue(self.data["H_nonzero_requires_K_chi_zero"])
        self.assertTrue(self.data["DBI_nonzero_current_coefficient"])

    def test_potential_repair_is_not_a_constant_Lambda(self):
        self.assertFalse(self.data["potential_repair_is_fixed_constant"])
        self.assertIn("H", self.data["required_potential_slope"])


if __name__ == "__main__":
    unittest.main()
