import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class EllipticDoubleMultiplierDiracTests(unittest.TestCase):
    def test_finite_and_zero_mode_audit(self):
        proc = subprocess.run([sys.executable, "-B", "dirac_double_multiplier_gate.py"],
                              cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        row = [x for x in proc.stdout.splitlines() if x.startswith("RESULT_JSON=")]
        self.assertEqual(len(row), 1)
        result = json.loads(row[0].split("=", 1)[1])
        self.assertEqual(result["checks"]["passed"], result["checks"]["count"])
        self.assertEqual(result["finite_k"]["physical_dof"], "1")
        self.assertEqual(result["zero_k"]["physical_dof"], "1")


if __name__ == "__main__":
    unittest.main()
