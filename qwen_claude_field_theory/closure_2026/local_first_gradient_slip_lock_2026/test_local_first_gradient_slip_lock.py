#!/usr/bin/env python3
"""Reproducibility test for the local first-gradient slip-lock gate."""

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "local_first_gradient_slip_lock.py"


class LocalSlipLockGateTest(unittest.TestCase):
    def test_gate_exits_and_reports_all_checks(self):
        proc = subprocess.run(
            [sys.executable, "-B", str(SCRIPT)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        rows = [line for line in proc.stdout.splitlines() if line.startswith("RESULT_JSON=")]
        self.assertEqual(len(rows), 1)
        result = json.loads(rows[0].split("=", 1)[1])
        self.assertEqual(result["status"], "LOCAL_FIRST_GRADIENT_SLIP_LOCK")
        self.assertEqual(result["checks"]["passed"], result["checks"]["count"])
        self.assertEqual(result["C_on_equal_flux"], "mu")


if __name__ == "__main__":
    unittest.main()
