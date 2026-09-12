import unittest
import numpy as np
from plane_slice import construct, Slice


class PlaneSliceTests(unittest.TestCase):
    def test_exact_contractions(self):
        self.assertTrue(all(construct()['checks'].values()))

    def test_sourced_homogeneous_constraint_and_lapse_control(self):
        sl=Slice();s=sl.source
        row=sl.point(0.,[0.,s['H'],1/s['clock_rate'],0.])
        self.assertLess(max(abs(x) for x in row['residuals']),1e-11)
        self.assertAlmostEqual(row['kx'],s['H'],places=11)
        self.assertLess(abs(row['bp']),1e-11)
        self.assertLess(abs(row['Npp']),1e-10)

    def test_finite_gradient_not_a_homogeneous_relabeling(self):
        sl=Slice(b0=.009);s=sl.source
        row=sl.point(0.,[.009,s['H'],1/s['clock_rate'],0.])
        self.assertGreater(abs(row['ktp']),1e-5)
        self.assertGreater(row['Y'],0.)
        self.assertLess(max(abs(x) for x in row['residuals']),1e-10)

    def test_overdensity_generates_gradient_curvature(self):
        sl=Slice(amplitude=.0001);s=sl.source
        row=sl.point(0.,[0.,s['H'],1/s['clock_rate'],0.])
        self.assertGreater(abs(row['bp']),1e-6)
        self.assertGreater(abs(row['Npp']),1e-6)
        self.assertLess(max(abs(x) for x in row['residuals']),1e-10)

    def test_reflection_invariance(self):
        sl=Slice(amplitude=.0001);s=sl.source
        left=sl.point(-.2,[-.003,s['H'],1/s['clock_rate'],-.001])
        right=sl.point(.2,[.003,s['H'],1/s['clock_rate'],.001])
        for i in (0,1):
            self.assertAlmostEqual(left['principal'][i]['quarter_finite_gamma'],
                                   right['principal'][i]['quarter_finite_gamma'],places=13)


if __name__=='__main__':unittest.main()
