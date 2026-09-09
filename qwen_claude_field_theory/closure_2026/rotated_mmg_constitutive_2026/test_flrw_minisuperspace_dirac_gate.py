import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class FLRWMinisuperspaceDiracGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        proc = subprocess.run(
            [sys.executable, "-B", "flrw_minisuperspace_dirac_gate.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        cls.proc = proc
        cls.data = json.loads((ROOT / "run_001" / "flrw_minisuperspace_dirac_results.json").read_text())

    def test_script_exits_cleanly(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)

    def test_primary_secondary_pair_and_count(self):
        self.assertTrue(self.data["C_independent_of_lapse"])
        self.assertEqual(self.data["constraint_bracket_rank_on_surface"], 0)
        self.assertEqual(self.data["homogeneous_physical_dof_count"], 1)

    def test_clock_hessian_is_healthy(self):
        self.assertTrue(self.data["clock_hessian_identity"])
        self.assertTrue(self.data["positive_clock_hessian_coefficient_scan"])


if __name__ == "__main__":
    unittest.main()
