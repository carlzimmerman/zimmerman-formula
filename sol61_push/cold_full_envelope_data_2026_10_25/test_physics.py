import unittest
import numpy as np
from physics import project, shell_potential, g_cold, window_logpdf
G=.00430091
class Physics(unittest.TestCase):
 def test_plummer_project(self):
  a=500.;m=1e7;R=np.array([0.,100.,500.,1500.])
  got=project(R,a,lambda r:G*m*r/(r*r+a*a)**1.5,nr=8192,nz=256)
  exact=3*np.pi*G*m/(64*a)/np.sqrt(1+(R/a)**2)
  self.assertLess(np.max(abs(got/exact-1)),8e-5)
 def test_shell_theorem_and_potential(self):
  r=np.geomspace(.001,1e7,65536);m=1e8;b=900.
  dm=np.diff(np.r_[0,m*r**3/(r*r+b*b)**1.5])
  q=np.array([0.,50.,500.,5000.,1e8])
  got=shell_potential(q,r,dm)
  exact=-G*m/np.sqrt(q*q+b*b)
  self.assertLess(np.max(abs(got/exact-1)),.001)
  np.testing.assert_allclose(g_cold(np.array([10.,20.]),np.array([100.]),np.array([1e8])),0)
 def test_window_pdf(self):
  from scipy.integrate import quad
  val=quad(lambda v:float(np.exp(window_logpdf(np.array([v]),2.,np.array([100.]),-30.,50.))[0]),-30,50)[0]
  self.assertAlmostEqual(val,1.,places=8)
if __name__=='__main__':unittest.main()
