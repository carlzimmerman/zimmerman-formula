"""Regression tests for filed G1's three-start gate; no science inputs mutated."""
import importlib.util
import math
from pathlib import Path
import unittest
import subprocess
import sys

class FitChecks(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).with_name('ac1_fit_checks.py')
        self.assertTrue(path.exists(), 'Three-start gate must be an independently testable function')
        spec = importlib.util.spec_from_file_location('fit_checks', path)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def test_disagreeing_start_cannot_be_discarded(self):
        self.assertFalse(self.mod.start_agreement([430, 432, 700])['pass'])

    def test_one_or_two_starts_are_not_agreement(self):
        for speeds in ([430], [430, 430], []):
            self.assertFalse(self.mod.start_agreement(speeds)['pass'])

    def test_nonfinite_and_nonpositive_starts_fail(self):
        for value in (float('nan'), float('inf'), 0, -1):
            self.assertFalse(self.mod.start_agreement([430, 430, value])['pass'])

    def test_filed_boundary_and_close_solution(self):
        self.assertTrue(self.mod.start_agreement([370, 400, 430])['pass'])
        self.assertFalse(self.mod.start_agreement([369, 400, 430])['pass'])
        self.assertTrue(self.mod.start_agreement([429, 430, 431])['pass'])

    def test_error_floor_does_not_claim_sn_matching(self):
        result = self.mod.velocity_error(430, 10, .089)
        self.assertAlmostEqual(result['error'], 38.27)
        self.assertEqual(result['method'], 'fixed archived mock RMS floor; not S/N-matched')
        self.assertEqual(self.mod.velocity_error(430, 80, .089)['error'], 80)
        for speed,error in ((430,float('nan')),(430,-1),(0,1)):
            self.assertRaises(ValueError,self.mod.velocity_error,speed,error,.089)

    def test_scorer_refuses_historical_output_directory(self):
        here = Path(__file__).resolve().parent
        result = subprocess.run([sys.executable, '-B', str(here/'ac1_score.py'), '--output-dir', str(here)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Refusing to overwrite historical AC1 outputs', result.stderr)

if __name__ == '__main__':
    unittest.main()
