import json
import os
import subprocess
import sys
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))


class L232RobustnessAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = subprocess.run([sys.executable, "L232_robustness_audit.py"], cwd=HERE,
                           check=False, capture_output=True, text=True)
        cls.stdout, cls.returncode = p.stdout, p.returncode
        with open(os.path.join(HERE, "L232_robustness_results.json"), encoding="utf-8") as fh:
            cls.result = json.load(fh)

    def test_executable_and_finite_scores(self):
        self.assertEqual(self.returncode, 0, self.stdout)
        self.assertGreater(self.result["ngal"], 0)
        for scores in self.result["equal_galaxy"].values():
            self.assertEqual(set(map(int, scores["scores_dex"])), {1, 2, 3, 4})
            self.assertTrue(all(float(v) >= 0 for v in scores["scores_dex"].values()))
            self.assertIn(scores["winner"], [1, 2, 3, 4])

    def test_bootstrap_is_well_formed(self):
        for boot in self.result["bootstrap"].values():
            self.assertEqual(sum(boot["wins"].values()), boot["draws"])
            self.assertAlmostEqual(sum(boot["winner_fraction"].values()), 1.0)
            self.assertGreaterEqual(boot["margin_p05_dex"], 0.0)


if __name__ == "__main__":
    unittest.main()
