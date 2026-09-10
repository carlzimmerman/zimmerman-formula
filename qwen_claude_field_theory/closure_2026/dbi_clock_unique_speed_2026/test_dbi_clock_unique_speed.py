import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class DBIClockUniqueSpeedTests(unittest.TestCase):
    def test_kernel_checked_theorem(self):
        proc = subprocess.run(
            [sys.executable, "run_lean.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        result = json.loads((ROOT / "run_001" / "lean_result.json").read_text())
        self.assertEqual(result["exit_status"], 0)
        self.assertTrue(result["theorem_present"])


if __name__ == "__main__":
    unittest.main()
