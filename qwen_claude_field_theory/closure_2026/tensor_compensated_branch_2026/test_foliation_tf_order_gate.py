import json
import subprocess
import sys
import unittest
from pathlib import Path


class FoliationTFOrderGateTest(unittest.TestCase):
    def test_k2_factor(self):
        script = Path(__file__).with_name("foliation_tf_order_gate.py")
        proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=True)
        result = json.loads(next(
            line for line in proc.stdout.splitlines() if line.startswith("RESULT_JSON=")
        ).split("=", 1)[1])
        self.assertEqual(result["status"], "LOCAL_FOLIATION_TF_HAS_K2_FACTOR")
        self.assertTrue(all(result["checks"].values()))


if __name__ == "__main__":
    unittest.main()
