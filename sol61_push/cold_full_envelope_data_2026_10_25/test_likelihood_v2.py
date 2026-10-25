import unittest,math
import numpy as np
from scipy.special import ndtr
from fit_v2 import nll
from physics import project,G
class Likelihood(unittest.TestCase):
 def test_mixture_selection_is_normalized_after_mixing(self):
  v=2.;var=np.array([[16.,400.]]);weights=np.array([.9,.1]);lo=-5.;hi=5.
  d=dict(v=np.array([v]),ev=np.array([0.]),lo=np.array([lo]),hi=np.array([hi]),logprior=np.zeros((1,2)))
  pdf=np.exp(-.5*v*v/var[0])/np.sqrt(2*np.pi*var[0]);z=ndtr(hi/np.sqrt(var[0]))-ndtr(lo/np.sqrt(var[0]));expected=-math.log(weights@pdf/(weights@z))
  self.assertAlmostEqual(nll(d,var,0.,math.log(9.)),expected,places=12)
 def test_jeans_projected_virial_independent_beta(self):
  from numpy.polynomial.legendre import leggauss
  x,w=leggauss(128);theta=(x+1)*np.pi/4;w=w*np.pi/4;a=500.;m=1e7;R=a*np.tan(theta)
  for beta in [-.5,0.,.5]:
   sig=project(R,a,lambda r:G*m*r/(r*r+a*a)**1.5,beta,nr=16384,nz=256)
   got=np.sum(w*2*np.sin(theta)*np.cos(theta)*sig);expected=np.pi*G*m/(32*a)
   self.assertLess(abs(got/expected-1),1e-4)
if __name__=='__main__':unittest.main()
