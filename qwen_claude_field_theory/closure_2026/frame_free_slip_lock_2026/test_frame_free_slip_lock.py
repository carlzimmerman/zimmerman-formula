import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class FrameFreeSlipLockTests(unittest.TestCase):
    def test_symbolic_gate(self):
        proc = subprocess.run([sys.executable, "-B", "frame_free_slip_lock_gate.py"],
                              cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        row = [x for x in proc.stdout.splitlines() if x.startswith("RESULT_JSON=")]
        self.assertEqual(len(row), 1)
        result = json.loads(row[0].split("=", 1)[1])
        self.assertEqual(result["checks"]["passed"], result["checks"]["count"])


if __name__ == "__main__":
    unittest.main()
