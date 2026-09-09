import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class ActionAngleInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.run(
            [sys.executable, "-B", "action_angle_invariant.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        cls.data = json.loads(
            (ROOT / "run_001" / "action_angle_invariant_results.json").read_text()
        )

    def test_script_exits_cleanly(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_symbolic_cancellations_are_exact(self):
        self.assertTrue(self.data["checks"]["single_orbit_cancellation"])
        self.assertTrue(self.data["checks"]["two_orbit_cancellation"])

    def test_quadrature_invariant_is_finite(self):
        self.assertTrue(self.data["checks"]["quadrature_rows_finite"])
        self.assertEqual(len(self.data["rows"]), 4)


if __name__ == "__main__":
    unittest.main()
