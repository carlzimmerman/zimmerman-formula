import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class ParameterFamilyGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = subprocess.run(
            [sys.executable, "-B", "parameter_family_gate.py"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        cls.result = json.loads(p.stdout)

    def test_matching_and_normalization_are_derived(self):
        self.assertIn("C**2", self.result["order_r2_matching_condition_t"])
        self.assertIn("C/2", self.result["tensor_normalization_roots"])
        self.assertIn("C/2", self.result["vector_normalization_roots"])

    def test_both_scalar_residue_branches_are_recorded(self):
        branches = self.result["residue_free_branches"]
        self.assertGreaterEqual(len(branches), 2)
        self.assertTrue(all(row["residue"] == "0" for row in branches))

    def test_general_source_gate_selects_one_branch(self):
        rows = self.result["all_six_source_branches"]
        passing = [row for row in rows
                   if row["spatial_pole_count"] == 0
                   and row["factor_failure_count"] == 0]
        failing = [row for row in rows
                   if row["spatial_pole_count"] > 0]
        self.assertEqual(len(passing), 1)
        self.assertGreaterEqual(len(failing), 1)


if __name__ == "__main__":
    unittest.main()
