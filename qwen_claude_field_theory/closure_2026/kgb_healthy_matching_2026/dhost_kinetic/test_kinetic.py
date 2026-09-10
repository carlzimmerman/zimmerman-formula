#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest
import sympy as s

class KineticChecks(unittest.TestCase):
    def data(self):
        path=Path(__file__).with_name('kinetic.py')
        self.assertTrue(path.exists(),'kinetic derivation is not implemented')
        import kinetic
        return kinetic.derive()
    def test_raw_contractions_and_D_zero(self):
        d=self.data()
        for value in d['contraction_residuals']+d['D_zero_residuals']:self.assertEqual(s.factor(value),0)
    def test_trace_hessian_null_and_square(self):
        d=self.data()
        for value in d['kinetic_residuals']:self.assertEqual(s.factor(value),0)
        self.assertNotEqual(d['hessian'][0,0],0)
    def test_primary_momenta_and_boundary_shift(self):
        for value in self.data()['momentum_residuals']:self.assertEqual(s.factor(value),0)
    def test_source_translation_and_Ricci_boundary_sign(self):
        for value in self.data()['translation_residuals']+self.data()['ricci_residuals']:self.assertEqual(s.factor(value),0)

if __name__=='__main__':unittest.main(verbosity=2)
