import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


class PpnTunedAetherDiracTests(unittest.TestCase):
    def test_c14_zero_is_constrained_in_finite_k_branch(self):
        proc = subprocess.run(
            [sys.executable, "ppn_tuned_aether_dirac_gate.py"],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        rows = [x for x in proc.stdout.splitlines() if x.startswith("RESULT_JSON=")]
        self.assertEqual(len(rows), 1)
        result = json.loads(rows[0].split("=", 1)[1])
        self.assertEqual(result["checks"]["passed"], result["checks"]["count"])
        self.assertEqual(result["finite_k"]["physical_dof"], "0")
        self.assertEqual(result["finite_k"]["witness_rank"], 10)


if __name__ == "__main__":
    unittest.main()
