import unittest,numpy as np
from kernel import Solver
class Controls(unittest.TestCase):
 def test_nonlinear_reverse_and_energy(self):
  s=Solver(256,eta=.3,vin=.2,alpha=10);u=s.gaussian();p=s.phi(u);E=s.energy(u,p);v,q,info=s.order4(u,p,.01);self.assertTrue(info['converged']);back,_,d=s.order4(v,q,-.01);self.assertTrue(d['converged']);self.assertLess(np.linalg.norm(back-u),1e-8);self.assertLess(abs(s.energy(v,q)-E),1e-8);self.assertLess(abs(np.vdot(v,v).real-np.vdot(u,u).real),1e-10)
 def test_gauge(self):
  a=Solver(128,eta=.3,vin=.2,alpha=10);b=Solver(128,eta=.3,vin=.2,alpha=10,pb=lambda r:np.full_like(r,7));u=a.gaussian();v=b.gaussian();p=a.phi(u);q=b.phi(v)
  for i in range(3):u,p,_=a.order4(u,p,.01);v,q,_=b.order4(v,q,.01)
  self.assertLess(np.linalg.norm(v-u*np.exp(-1j*7*.03/.3)),1e-8)
 def test_free_gaussian_order(self):
  errors=[]
  for h in [.2,.1,.05,.025]:
   s=Solver(1024,eta=1.,alpha=10,strength=0);u=s.gaussian();p=s.phi(u)
   for i in range(round(1/h)):
    u,p,d=s.order4(u,p,h);self.assertTrue(d['converged'])
   exact=2/np.pi**.25*s.r*(1+1j)**(-1.5)*np.exp(-s.r*s.r/(2*(1+1j)))*np.sqrt(s.w);errors.append(np.linalg.norm(u-exact))
  print('free Gaussian errors',errors)
  self.assertLess(errors[1],errors[0]/8);self.assertLess(errors[-1],errors[-2]/10)
if __name__=='__main__':unittest.main()
