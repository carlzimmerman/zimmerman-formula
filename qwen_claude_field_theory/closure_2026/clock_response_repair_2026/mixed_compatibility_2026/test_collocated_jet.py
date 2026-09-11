#!/usr/bin/env python3
import importlib.util
import unittest
import numpy as np


class CollocatedJet(unittest.TestCase):
    def function(self):
        self.assertIsNotNone(importlib.util.find_spec('collocated_jet'),
                             'primitive in the actual odd spline basis is missing')
        from collocated_jet import collocated_primitive
        return collocated_primitive

    def test_polynomial_primitive(self):
        primitive=self.function();r=np.linspace(0,1,65)
        actual=primitive(r,3+6*r*r+15*r**4-7*r**6)
        np.testing.assert_allclose(actual,3*r+2*r**3+3*r**5-r**7,rtol=0,atol=3e-12)

    def test_nonpolynomial_primitive_refines_and_keeps_center_jet(self):
        primitive=self.function()
        from scipy.interpolate import CubicSpline
        errors=[]
        for n in (33,65,129):
            r=np.linspace(0,1,n);source=(4*r*r-2)*np.exp(-r*r)
            actual=primitive(r,source)
            fit=CubicSpline(r[1:]**2,actual[1:]/r[1:])
            self.assertLess(abs(fit(0.)+2),3e-12)
            self.assertEqual(actual[0],0.)
            errors.append(float(max(abs(actual+2*r*np.exp(-r*r)))))
        self.assertLess(errors[1],errors[0]/8,errors)
        self.assertLess(errors[2],errors[1]/8,errors)


if __name__=='__main__':unittest.main(verbosity=2)
