import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class PhantomNoSlipWardTrilemmaTest(unittest.TestCase):
    def test_symbolic_trilemma(self):
        run = subprocess.run([sys.executable, "phantom_noslip_ward_trilemma_2026.py"],
                             cwd=HERE, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("TRILEMMA", run.stdout)
        self.assertIn("PASS", run.stdout)


if __name__ == "__main__":
    unittest.main()
