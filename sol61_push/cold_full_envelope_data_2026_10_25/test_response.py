import unittest
import numpy as np
from response import integrate_case
class Response(unittest.TestCase):
 def test_stationary_null(self):
  d=integrate_case(1e8,900.,5e5,[200.],200.,0.,6.,n=32)
  self.assertLess(abs(d['late_r50_ratio']-1),1e-7)
  self.assertLess(abs(d['late_variance_ratio']-1),1e-7)
  self.assertLess(d['work_ledger_max_relative'],1e-5)
 def test_external_work_and_refine(self):
  a=integrate_case(1e8,900.,5e5,[200.],200.,.1,6.,n=32)
  b=integrate_case(1e8,900.,5e5,[200.],200.,.1,6.,n=32,tight=True)
  self.assertLess(a['work_ledger_max_relative'],1e-5)
  self.assertLess(abs(a['late_variance_ratio']/b['late_variance_ratio']-1),1e-5)
if __name__=='__main__':unittest.main()
