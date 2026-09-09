"""Independent benchmarks for analytic time jets and interface flatness."""
import importlib.util
from types import SimpleNamespace
import unittest
import numpy as np


class InterfaceTests(unittest.TestCase):
    def module(self,name):
        self.assertIsNotNone(importlib.util.find_spec(name),name+' is missing')
        return __import__(name)

    def test_fixed_quintic_third_jet_on_nonunit_interval(self):
        m=self.module('ic37_analytic_second_jet')
        # Exact polynomial (S-2)^5 on [2,4], specified by endpoint jets.
        table=SimpleNamespace(x=np.array([2.,4.]),jets=np.array([[0.,0.,0.],[32.,80.,160.]]))
        S=np.array([2.,2.3,3.,3.8,4.])
        np.testing.assert_allclose(m.third_jet(table,S),60*(S-2)**2,rtol=1e-12,atol=1e-12)

    def test_gradient_generated_second_matter_stress(self):
        m=self.module('ic37_analytic_second_jet')
        # S=Q=0, j=2, v=4, gdot=3; second gradient energy = j*gdot^2/v=4.5.
        hdd,pwdd=m.matter_constraints_second(7.,2.,0.,0.,0.,3.,0.,0.,.2,4.)
        self.assertAlmostEqual(float(hdd),4.5)
        self.assertAlmostEqual(float(pwdd),-1.8)

    def test_moving_boundary_and_flat_switch_identities(self):
        m=self.module('ic37_interface_flatness')
        for name,value in m.identities().items():self.assertEqual(value,0,name)

    def test_interface_matching_does_not_hide_quadratic_defect(self):
        m=self.module('ic37_interface_flatness')
        r=np.linspace(2.,2.01,65)
        C=np.tile([0.,0.,1.],(len(r),1));W=np.tile([1.,0.,0.],(len(r),1))
        out=m.edge_compatibility(r,C,W,np.zeros_like(r),(r-2)**2,8)
        self.assertLess(abs(out['edge_jets'][0]),1e-12)
        self.assertLess(abs(out['edge_jets'][1]),1e-10)
        self.assertAlmostEqual(out['edge_jets'][2],2.,places=6)

    def test_analytic_time_jets_agree_with_independent_finite_kicks(self):
        m=self.module('ic37_analytic_second_jet')
        self.assertTrue(callable(getattr(m,'audit',None)))
        out=m.audit()
        self.assertLess(out['flow_disagreement'],1e-9)
        self.assertLess(out['relative_acceleration_disagreement'],1e-5)
        self.assertLess(out['relative_constraint_source_disagreement'],1e-5)

    def test_flatness_alone_is_not_a_finite_multiplier_certificate(self):
        m=self.module('ic37_interface_flatness')
        self.assertTrue(callable(getattr(m,'flat_counterexample',None)))
        out=m.flat_counterexample()
        self.assertEqual(out['all_power_flat_limit'],0)
        import sympy as s
        self.assertEqual(out['response_limit'],s.oo)


if __name__=='__main__':unittest.main()
