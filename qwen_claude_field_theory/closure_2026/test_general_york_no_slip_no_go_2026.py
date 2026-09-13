import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class GeneralYorkNoSlipNoGoTest(unittest.TestCase):
    def test_symbolic_gate_passes(self):
        run = subprocess.run([sys.executable, "general_york_no_slip_no_go_2026.py"],
                             cwd=HERE, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("THEOREM (scoped)", run.stdout)
        self.assertIn("PASS", run.stdout)


if __name__ == "__main__":
    unittest.main()
