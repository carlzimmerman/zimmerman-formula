import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class TensorCompensatedDiracTests(unittest.TestCase):
    def test_finite_and_zero_sectors(self):
        proc = subprocess.run([sys.executable, "-B", "tensor_compensated_dirac_gate.py"],
                              cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        rows = [x for x in proc.stdout.splitlines() if x.startswith("RESULT_JSON=")]
        self.assertEqual(len(rows), 1)
        result = json.loads(rows[0].split("=", 1)[1])
        self.assertEqual(result["checks"]["passed"], result["checks"]["count"])
        self.assertEqual(result["finite_k"]["physical_dof"], "0")
        self.assertEqual(result["zero_k"]["physical_dof"], "1")


if __name__ == "__main__":
    unittest.main()
