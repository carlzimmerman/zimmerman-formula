import unittest,numpy as np
from radial import Radial,phi_shell
from stars import Background,draw,Cold,Cohort
class Stars(unittest.TestCase):
 def test_df_energy_and_angular_distribution(self):
  s=Radial(256,eta=.2);u=s.gaussian();bg=Background(.01,[.2],.05);sample=draw(s.r,abs(u)**2,bg,.2,8192,314)
  self.assertLess(sample['cdf_max_decrease'],1e-6)
  self.assertLess(abs(np.mean(sample['direction_mu']**2)-.25),.015)
  self.assertLess(sample['moment_control_relative_error'],.01)
 def test_static_orbits_refine(self):
  field=Radial(256,eta=.2);dm=abs(field.gaussian())**2;bg=Background(.01,[.2],.05);cold=Cold(field.r,dm);errors=[]
  for dt in [.002,.001]:
   c=Cohort(field.r,dm,bg,.2,256,314,0.)
   for i in range(round(.2/dt)):c.advance(cold,cold,dt)
   errors.append(c.max_frozen_drift)
   self.assertLess(c.max_frozen_drift,.002)
   self.assertLess(np.max(abs(c.x-c.xc)),1e-12)
   self.assertLess(np.max(abs(c.work)),1e-12)
  self.assertLess(errors[1],errors[0]*.5)
if __name__=='__main__':unittest.main()
