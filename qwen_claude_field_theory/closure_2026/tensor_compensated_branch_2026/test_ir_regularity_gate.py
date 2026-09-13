import json
import subprocess
import sys
import unittest
from pathlib import Path


class IRRegularityGateTest(unittest.TestCase):
    def test_gate_derives_singularity(self):
        script = Path(__file__).with_name("ir_regularity_gate.py")
        proc = subprocess.run(
            [sys.executable, str(script)], capture_output=True, text=True, check=True
        )
        line = next(x for x in proc.stdout.splitlines() if x.startswith("RESULT_JSON="))
        result = json.loads(line.split("=", 1)[1])
        self.assertEqual(result["status"], "IR_SINGULAR_FOR_GENERIC_ANISOTROPIC_SOURCE")
        self.assertTrue(all(result["checks"].values()))


if __name__ == "__main__":
    unittest.main()
