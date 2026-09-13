import json
import subprocess
import sys
import unittest
from pathlib import Path


class IROperatorTradeoffGateTest(unittest.TestCase):
    def test_operator_fork(self):
        script = Path(__file__).with_name("ir_operator_tradeoff_gate.py")
        proc = subprocess.run(
            [sys.executable, str(script)], capture_output=True, text=True, check=True
        )
        result = json.loads(next(
            line for line in proc.stdout.splitlines() if line.startswith("RESULT_JSON=")
        ).split("=", 1)[1])
        self.assertEqual(result["status"], "SCREENED_ELLIPTIC_OR_PROPAGATING_HYPERBOLIC_FORK")
        self.assertTrue(all(result["checks"].values()))


if __name__ == "__main__":
    unittest.main()
