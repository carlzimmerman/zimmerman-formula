import json
import subprocess
import sys
import unittest
from pathlib import Path


class IndependentDecouplingConsistencyTest(unittest.TestCase):
    def test_mismatch_is_reproduced(self):
        script = Path(__file__).with_name("independent_decoupling_consistency.py")
        proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=True)
        result = json.loads(next(
            line for line in proc.stdout.splitlines() if line.startswith("RESULT_JSON=")
        ).split("=", 1)[1])
        self.assertEqual(result["status"], "DECoupling_GHOST_BAND_MISMATCH")
        self.assertTrue(all(result["checks"].values()))


if __name__ == "__main__":
    unittest.main()
