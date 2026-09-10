import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class MatterWardTests(unittest.TestCase):
    def test_minimal_matter_ward_identity(self):
        proc = subprocess.run(
            [sys.executable, "matter_ward_gate.py"],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        rows = [x for x in proc.stdout.splitlines() if x.startswith("RESULT_JSON=")]
        self.assertEqual(len(rows), 1)
        result = json.loads(rows[0].split("=", 1)[1])
        self.assertEqual(result["checks"]["passed"], result["checks"]["count"])
        self.assertEqual(result["ward_residuals"], ["0", "0"])


if __name__ == "__main__":
    unittest.main()
