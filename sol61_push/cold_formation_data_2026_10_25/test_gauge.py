import unittest,numpy as np
from radial_v4 import Radial,phi_shell
class Gauge(unittest.TestCase):
 def test_constant_gauge_and_invariants(self):
  a=Radial(128,eta=.2,vin=.3);b=Radial(128,eta=.2,vin=.3,pb=lambda r:np.full_like(r,7.));u=a.gaussian();v=b.gaussian();pa=phi_shell(a.r,abs(u)**2);pb=pa.copy();E=a.energy(u,pa);tag=abs(u)**2*(a.r<1);tagb=tag.copy();M=tag.sum();dt=.003
  for i in range(20):
   u,pa,tag,ia=a.step(u,pa,dt,tag);v,pb,tagb,ib=b.step(v,pb,dt,tagb);self.assertTrue(ia['converged'] and ib['converged'])
  self.assertLess(np.linalg.norm(v-u*np.exp(-1j*7*20*dt/.2)),1e-10);self.assertLess(np.max(abs(tag-tagb)),1e-10);self.assertLess(abs(tag.sum()-M),1e-10);self.assertLess(abs(a.energy(u,pa)-E),1e-9);self.assertLess(abs(b.energy(v,pb)-a.energy(u,pa)-7*np.vdot(u,u).real),1e-9)
if __name__=='__main__':unittest.main()
