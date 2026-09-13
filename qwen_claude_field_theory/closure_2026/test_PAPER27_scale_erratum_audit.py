import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class Paper27ScaleErratumAuditTest(unittest.TestCase):
    def test_derivation_and_source_audit(self):
        run = subprocess.run([sys.executable, "PAPER27_scale_erratum_audit.py"],
                             cwd=HERE, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("a0=s/n", run.stdout)
        self.assertIn("ambiguous_c", run.stdout)


if __name__ == "__main__":
    unittest.main()
