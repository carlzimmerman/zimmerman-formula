import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class RMMGLapseConstraintVariationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.run(
            [sys.executable, "-B", "rmmg_lapse_constraint_variation_gate.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        cls.data = json.loads(
            (ROOT / "run_001" / "rmmg_lapse_constraint_variation_results.json").read_text()
        )

    def test_script_exits_cleanly(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_affine_constraint_and_euler_equation_differ(self):
        self.assertTrue(self.data["checks"]["advertised_constraint_vanishes_on_affine"])
        self.assertTrue(self.data["checks"]["euler_residual_derived"])
        self.assertTrue(self.data["checks"]["unit_slope_constraint_still_zero"])
        self.assertTrue(self.data["checks"]["unit_slope_residual_nonzero"])


if __name__ == "__main__":
    unittest.main()
