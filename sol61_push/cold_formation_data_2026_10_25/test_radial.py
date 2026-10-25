import unittest,numpy as np
from radial import Radial,phi_shell
class Controls(unittest.TestCase):
 def test_gaussian_and_positive_form(self):
  s=Radial(128,eta=.2);u=s.gaussian();m=np.sum(abs(u)**2)
  self.assertLess(abs(m-1),1e-7)
  self.assertLess(abs(s.kinetic(u)/(.75*.2**2)-1),2e-5)
  w=.5*np.sum(abs(u)**2*phi_shell(s.r,abs(u)**2))
  self.assertLess(abs(w/(-1/np.sqrt(2*np.pi))-1),.004)
  rng=np.random.default_rng(1);z=rng.normal(size=len(u))+1j*rng.normal(size=len(u));self.assertGreater(s.kinetic(z),0)
 def test_nonzero_carrier_kinetic(self):
  s=Radial(256,eta=.2,vin=.3);u=s.gaussian()
  expected=.75*.2**2+.5*np.sum(abs(u)**2*s.p**2)
  self.assertLess(abs(s.kinetic(u)/expected-1),1e-5)
 def test_conservation_and_tag(self):
  s=Radial(128,eta=.3);u=s.gaussian();phi=phi_shell(s.r,abs(u)**2);E=s.energy(u,phi);q=abs(u)**2*(s.r<1)
  for i in range(8):u,phi,q,info=s.step(u,phi,.003,q)
  self.assertLess(abs(np.sum(abs(u)**2)-1),1e-7)
  self.assertLess(abs(s.energy(u,phi)-E),1e-9)
  self.assertLess(abs(q.sum()-np.sum(abs(s.gaussian())**2*(s.r<1))),1e-10)
  self.assertGreaterEqual(q.min(),-1e-14);self.assertLess(np.max(q-abs(u)**2),1e-12)
if __name__=='__main__':unittest.main()
