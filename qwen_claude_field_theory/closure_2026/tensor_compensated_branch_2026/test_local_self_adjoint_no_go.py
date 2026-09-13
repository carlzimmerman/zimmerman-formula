import json
import subprocess
import sys
import unittest
from pathlib import Path


class LocalSelfAdjointNoGoTest(unittest.TestCase):
    def test_conditional_no_go(self):
        script = Path(__file__).with_name("local_self_adjoint_no_go.py")
        proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=True)
        result = json.loads(next(
            line for line in proc.stdout.splitlines() if line.startswith("RESULT_JSON=")
        ).split("=", 1)[1])
        self.assertEqual(result["status"], "CONDITIONAL_LOCAL_MULTIPLIER_NO_GO")
        self.assertTrue(all(result["checks"].values()))


if __name__ == "__main__":
    unittest.main()
