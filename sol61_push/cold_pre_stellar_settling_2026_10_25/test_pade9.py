import unittest,numpy as np
from scipy.linalg import expm
from kernel_pade9 import Solver
class Controls(unittest.TestCase):
 def test_scalar_unitarity_and_dense_oracle(self):
  s=Solver(8,eta=.3,alpha=3,strength=0);n=len(s.r);H=np.diag(s.diag.astype(complex))
  for d,h in enumerate(s.upper,1):H+=np.diag(h,d)+np.diag(h.conj(),-d)
  rng=np.random.default_rng(5);u=rng.normal(size=n)+1j*rng.normal(size=n);u/=np.linalg.norm(u);scale=np.max(abs(np.linalg.eigvalsh(H)));h=.3/scale
  v=s.rational(u,np.zeros(n),h);exact=expm(-1j*H*h/.3)@u;self.assertLess(np.linalg.norm(v-exact),1e-9);self.assertLess(abs(np.vdot(v,v).real-1),1e-10)
 def test_nonlinear_energy_reverse_and_gauge(self):
  a=Solver(128,eta=.3,vin=.2,alpha=8);b=Solver(128,eta=.3,vin=.2,alpha=8,pb=lambda r:np.full_like(r,7));u=a.gaussian();p=a.phi(u);E=a.energy(u,p);v,q,d=a.order4(u,p,.02);self.assertTrue(d['converged']);w,_,f=a.order4(v,q,-.02);self.assertTrue(f['converged']);self.assertLess(np.linalg.norm(w-u),1e-8);self.assertLess(abs(a.energy(v,q)-E),1e-8);vb,_,db=b.order4(u,b.phi(u),.02);self.assertTrue(db['converged']);self.assertLess(np.linalg.norm(vb-v*np.exp(-1j*7*.02/.3)),1e-8)
 def test_free_gaussian(self):
  s=Solver(512,eta=1.,alpha=8,strength=0);u=s.gaussian();p=s.phi(u)
  for i in range(4):u,p,d=s.order4(u,p,.25);self.assertTrue(d['converged'])
  exact=2/np.pi**.25*s.r*(1+1j)**(-1.5)*np.exp(-s.r*s.r/(2*(1+1j)))*np.sqrt(s.w);self.assertLess(np.linalg.norm(u-exact),1e-5)
 def test_nonlinear_order(self):
  states=[]
  for h in [.04,.02,.01,.00125]:
   s=Solver(32,eta=.3,vin=.2,alpha=3);u=s.gaussian();p=s.phi(u)
   for i in range(round(.16/h)):u,p,d=s.order4(u,p,h);self.assertTrue(d['converged'])
   states.append(u)
  e=[np.linalg.norm(u-states[-1]) for u in states[:-1]];print('nonlinear errors',e);self.assertLess(e[1],e[0]/8);self.assertLess(e[2],e[1]/8)
if __name__=='__main__':unittest.main()
