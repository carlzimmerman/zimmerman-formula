import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class CovariantClockPrincipalGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        proc = subprocess.run(
            [sys.executable, "-B", "covariant_clock_principal_gate.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        cls.proc = proc
        cls.data = json.loads(
            (ROOT / "run_001" / "covariant_clock_principal_results.json").read_text()
        )

    def test_script_exits_cleanly(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_exact_kernel_jacobian(self):
        self.assertTrue(self.data["kernel_identity"])
        self.assertTrue(self.data["parallel_eigenvalue_identity"])

    def test_zero_speed_principal_symbol(self):
        self.assertTrue(self.data["omega_zero_spatial_gradient"])
        self.assertEqual(self.data["clock_speed_numerator"], "0")

    def test_controlled_y_to_zero_rank_loss(self):
        self.assertTrue(self.data["ellipticity_lost_at_y0"])
        self.assertEqual(self.data["small_y_lambda_perp_over_y"], "1")
        self.assertEqual(self.data["small_y_lambda_parallel_over_y"], "2")


if __name__ == "__main__":
    unittest.main()
