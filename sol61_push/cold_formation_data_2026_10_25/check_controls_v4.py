"""Orthogonal checks on v4 field, DF and orbit code."""
import unittest,numpy as np
from radial_v4 import Radial,phi_shell
from stars_v2 import Background,Cold,Cohort,draw
class Controls(unittest.TestCase):
 def test_gaussian(self):
  s=Radial(512,eta=.2,vin=.1);u=s.gaussian();m=abs(u)**2
  self.assertLess(abs(m.sum()-1),1e-8);self.assertLess(abs(.5*np.sum(m*phi_shell(s.r,m))+1/np.sqrt(2*np.pi)),.002);self.assertLess(abs(s.kinetic(u)-(.75*.2**2+.5*np.sum(m*s.p*s.p))),1e-5)
 def test_conservation_tag(self):
  s=Radial(128,eta=.3);u=s.gaussian();phi=phi_shell(s.r,abs(u)**2);E=s.energy(u,phi);tag=abs(u)**2*(s.r<1);T=tag.sum()
  for i in range(12):
   u,phi,tag,d=s.step(u,phi,.003,tag);self.assertTrue(d['converged']);self.assertLess(abs(tag.sum()-T),1e-10);self.assertGreaterEqual(tag.min(),-1e-12);self.assertLess(np.max(tag-abs(u)**2),1e-10)
  self.assertLess(abs(s.energy(u,phi)-E),1e-9);self.assertLess(abs(np.sum(abs(u)**2)-1),1e-6)
 def test_DF_and_static_orbits(self):
  s=Radial(256,eta=.2);dm=abs(s.gaussian())**2;bg=Background(.01,[.2],.05);cold=Cold(s.r,dm);d=draw(s.r,dm,bg,.2,4096,314);self.assertLess(d['moment_control_relative_error'],.01);self.assertLess(d['cdf_max_decrease'],1e-6);self.assertLess(abs(np.mean(d['direction_mu']**2)-.25),.02)
  errs=[]
  for dt in [.004,.002]:
   c=Cohort(s.r,dm,bg,.2,256,314,0.)
   for i in range(round(.2/dt)):c.advance(cold,cold,dt)
   errs.append(c.max_ledger);self.assertFalse(c.substep_cap_exceeded);self.assertLess(c.max_frozen_drift,.002);self.assertLess(np.max(abs(c.x-c.xc)),1e-12)
  self.assertLess(errs[1],errs[0]*.6)
if __name__=='__main__':unittest.main()
