"""Analytic mass-integral controls, independent of galaxy outcomes."""
import unittest
import numpy as np
from quadrature import cell_mass

class Controls(unittest.TestCase):
 def test_cubic_legendre_norm(self):
  z=np.array([-1.,-1/np.sqrt(5),1/np.sqrt(5),1.]);v=(5*z**3-3*z)/2
  self.assertAlmostEqual(cell_mass(1,0.,2.,v,8).sum(),2/7,places=14)
 def test_complex_polynomial_orthogonality(self):
  z=np.array([-1.,-1/np.sqrt(5),1/np.sqrt(5),1.]);c=np.array([.2+.3j,-.7+.1j,.8-.4j,.3+.9j]);v=np.polynomial.legendre.legval(z,c);expected=sum(2/(2*k+1)*abs(a)**2 for k,a in enumerate(c))
  self.assertAlmostEqual(cell_mass(1,0.,2.,v,8).sum(),expected,places=13)
 def test_mapped_constant(self):
  v=np.full(3*8+1,2+3j);self.assertLess(abs(cell_mass(8,10.,40.,v,16).sum()/(13*40)-1),1e-13)

if __name__=='__main__':unittest.main()
