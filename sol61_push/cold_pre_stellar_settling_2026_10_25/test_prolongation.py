import unittest,numpy as np
from kernel_gated import Solver
from prolongation_v2 import transfer
from radial_v4 import phi_shell
class Controls(unittest.TestCase):
 def test_cubic_reference_field_reproduction(self):
  a=Solver(8,eta=.2,vin=.3,alpha=3);b=Solver(16,eta=.2,vin=.3,alpha=3)
  def f(s):
   x=np.arcsinh(s.r*np.sinh(s.alpha)/s.R)/s.alpha
   return x*(1-x)*(1+(.2+.7j)*x)
  u=f(a)*np.sqrt(a.w);v=transfer(a.r,a.w,u,b,a.ne,a.alpha);self.assertLess(np.max(abs(v/np.sqrt(b.w)-f(b))),1e-12)
 def test_fluctuation_binding_identity(self):
  s=Solver(64,eta=.2,alpha=3);r=s.r;m1=np.exp(-r*r)*s.w*r*r;m2=np.exp(-r*r/2)*s.w*r*r;m1/=m1.sum();m2/=m2.sum();mean=.3*m1+.7*m2
  W=lambda m:.5*np.sum(m*phi_shell(r,m))
  fluct=.3*W(m1-mean)+.7*W(m2-mean)
  self.assertLess(fluct,0);self.assertLess(abs(.3*W(m1)+.7*W(m2)-W(mean)-fluct),1e-14)
if __name__=='__main__':unittest.main()
