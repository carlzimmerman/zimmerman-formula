#!/usr/bin/env python3
import importlib.util
import unittest
import numpy as np


class IntegratedJet(unittest.TestCase):
    def function(self):
        self.assertIsNotNone(importlib.util.find_spec('integrated_jet'),
                             'integrable radial jet primitive is missing')
        from integrated_jet import integrate_even_jet
        return integrate_even_jet

    def test_polynomial_primitive_and_origin(self):
        primitive=self.function()
        r=np.linspace(0,1,33)
        source=3+6*r*r+15*r**4-7*r**6
        exact=3*r+2*r**3+3*r**5-r**7
        got=primitive(r,source)
        self.assertEqual(got[0],0.)
        np.testing.assert_allclose(got,exact,rtol=0,atol=2e-12)

    def test_nonpolynomial_primitive_refines(self):
        primitive=self.function();errors=[]
        for size in (33,65,129):
            r=np.linspace(0,1,size)
            got=primitive(r,(4*r*r-2)*np.exp(-r*r))
            errors.append(float(max(abs(got+2*r*np.exp(-r*r)))))
        self.assertLess(errors[1],errors[0]/8,errors)
        self.assertLess(errors[2],errors[1]/8,errors)


if __name__=='__main__':unittest.main(verbosity=2)
