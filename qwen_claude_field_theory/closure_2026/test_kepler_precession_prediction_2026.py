import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class KeplerPrecessionPredictionTest(unittest.TestCase):
    def test_derivation_and_table_run(self):
        run = subprocess.run([sys.executable, "kepler_precession_prediction_2026.py"],
                             cwd=HERE, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("PREDICTION TABLE", run.stdout)
        self.assertIn("PASS", run.stdout)


if __name__ == "__main__":
    unittest.main()
