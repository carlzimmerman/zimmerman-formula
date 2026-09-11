#!/usr/bin/env python3
import unittest
import numpy as np
from evolve import derivatives


class RegularDerivativeTests(unittest.TestCase):
    def test_even_and_odd_polynomial_center_jets(self):
        r=np.linspace(0,1,65);dx=r[1]
        for odd,y,d1,d2 in ((False,1+2*r*r+3*r**4,4*r+12*r**3,4+36*r*r),
                             (True,2*r+3*r**3,2+9*r*r,18*r)):
            a,b=derivatives(y,dx,odd)
            np.testing.assert_allclose(a[:3],d1[:3],atol=1e-11)
            np.testing.assert_allclose(b[:3],d2[:3],atol=1e-10)

    def test_smooth_derivatives_converge_at_fourth_order(self):
        errors=[]
        for n in (33,65):
            r=np.linspace(0,1,n);y=np.exp(-r*r)
            a,b=derivatives(y,r[1]);cut=slice(0,-3)
            errors.append(max(np.max(abs(a[cut]+2*r[cut]*y[cut])),
                              np.max(abs(b[cut]-(4*r[cut]**2-2)*y[cut]))))
        self.assertLess(errors[1],errors[0]/12)

if __name__=='__main__':unittest.main(verbosity=2)
