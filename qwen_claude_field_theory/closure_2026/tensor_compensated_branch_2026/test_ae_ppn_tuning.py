import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class AEPpnTuningTests(unittest.TestCase):
    def test_derived_ppn_locus_and_warning(self):
        proc = subprocess.run(
            [sys.executable, "ae_ppn_tuning_gate.py"],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        rows = [x for x in proc.stdout.splitlines() if x.startswith("RESULT_JSON=")]
        self.assertEqual(len(rows), 1)
        result = json.loads(rows[0].split("=", 1)[1])
        self.assertEqual(result["checks"]["passed"], result["checks"]["count"])
        self.assertEqual(result["alpha1"], "0")
        self.assertEqual(result["alpha2"], "0")
        self.assertEqual(result["cT_squared"], "1")
        self.assertEqual(result["spin0_speed_denominator"], "0")


if __name__ == "__main__":
    unittest.main()
