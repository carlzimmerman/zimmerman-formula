import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class LinearSectorStabilityTests(unittest.TestCase):
    def test_principal_sector_gate(self):
        proc = subprocess.run(
            [sys.executable, "-B", "linear_sector_stability_gate.py"],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        rows = [x for x in proc.stdout.splitlines() if x.startswith("RESULT_JSON=")]
        self.assertEqual(len(rows), 1)
        result = json.loads(rows[0].split("=", 1)[1])
        self.assertEqual(result["checks"]["passed"], result["checks"]["count"])
        self.assertEqual(result["tensor"]["cT_squared"], "1")
        self.assertEqual(result["vector"]["physical_dof"], "0")
        self.assertEqual(result["scalar"]["finite_k_physical_dof"], "0")


if __name__ == "__main__":
    unittest.main()
