import json
import subprocess
import sys
import unittest
from pathlib import Path

import sector_rank_gate


class SectorRankGateTests(unittest.TestCase):
    def test_sector_ranks_are_computed_and_distinct(self):
        result = sector_rank_gate.build_gate()
        ranks = result["sector_ranks"]
        self.assertIsInstance(ranks["k0_static"], int)
        self.assertTrue(result["checks"]["homogeneous_dynamic_sector_is_distinct"])
        self.assertTrue(result["checks"]["k0_static_is_degenerate"])
        self.assertTrue(result["checks"]["kneq_static_is_not_degenerate"])

    def test_factorization_is_derived(self):
        result = sector_rank_gate.build_gate()
        self.assertTrue(result["checks"]["determinant_factorization_derived"])
        self.assertTrue(result["checks"]["clock_characteristic_rank_drops"])

    def test_cli_records_open_scope(self):
        root = Path(__file__).resolve().parent
        output = root / "run_002" / "sector_rank_test_results.json"
        proc = subprocess.run(
            [sys.executable, "-B", "sector_rank_gate.py", "--output", str(output)],
            cwd=root, text=True, capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(output.read_text())
        self.assertTrue(payload["status"].endswith("FULL_THEORY_OPEN"))
        output.unlink()


if __name__ == "__main__":
    unittest.main()
