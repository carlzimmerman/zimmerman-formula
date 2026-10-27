import unittest
import numpy as np
from medium import source,normal_modes,nonlinear

class CollectiveTests(unittest.TestCase):
    def test_critical_and_gapped_slopes(self):
        for floor,exponent in [(0.,2.),(.1,3.)]:
            a=source(1e-5,10.,floor);b=source(2e-5,10.,floor)
            self.assertAlmostEqual(np.log2(b/a),exponent,delta=.001)

    def test_vacuum_plasma(self):
        w,v=normal_modes(2.,np.array([]),np.array([]),3.)
        self.assertAlmostEqual(w[-1],np.sqrt(13),places=10)
        self.assertAlmostEqual(v[-1],2/np.sqrt(13),places=10)

    def test_passive_causality(self):
        w,v=normal_modes(.7,np.array([1.,3.]),np.array([2.,4.]),.5)
        self.assertTrue(np.all(np.isfinite(w)))
        self.assertLessEqual(np.max(np.abs(v)),1+1e-12)

    def test_nonlinear_energy(self):
        r=nonlinear(.1,10.,16,3.,1e-9)
        self.assertLess(r['energy_error'],1e-7)
        self.assertLess(r['norm_error'],1e-8)
        self.assertLess(r['max_speed'],1.)
        self.assertLess(r['momentum_error'],1e-12)

if __name__=='__main__':unittest.main()
