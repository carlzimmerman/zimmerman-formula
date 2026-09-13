import json
import subprocess
import sys
import unittest
from pathlib import Path


class RegulatorTradeoffGateTest(unittest.TestCase):
    def test_regulator_tradeoff(self):
        script = Path(__file__).with_name("regulator_tradeoff_gate.py")
        proc = subprocess.run(
            [sys.executable, str(script)], capture_output=True, text=True, check=True
        )
        result = json.loads(next(
            line for line in proc.stdout.splitlines() if line.startswith("RESULT_JSON=")
        ).split("=", 1)[1])
        self.assertEqual(result["status"], "LOCAL_REGULATOR_TRADEOFF_CONFIRMED")
        self.assertTrue(all(result["checks"].values()))


if __name__ == "__main__":
    unittest.main()
