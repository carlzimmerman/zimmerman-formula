"""Catch omitted time-normal flux, shift-gradient jumps and phase equations."""
import importlib.util
import unittest
import sympy as s


class MovingInterfaceTests(unittest.TestCase):
    def model(self):
        self.assertIsNotNone(importlib.util.find_spec('ic44_moving_interface'),
                             'The action-derived moving-interface implementation is absent')
        import ic44_moving_interface as module
        return module

    def test_time_normal_flux_detects_discontinuous_trace_momentum(self):
        d=self.model().derive();v,beta,dq,dh=d['speed'],d['beta'],d['dq'],d['dh']
        subs={v:1,beta:0,dq:1,dh:0}
        self.assertEqual(s.simplify(d['normal_Q_jump'].subs(subs)), -2)
        self.assertEqual(s.simplify(d['normal_beta_jump'].subs(subs)), -s.Rational(2,3))

    def test_bulk_equation_rejects_noncharacteristic_auxiliary_gradient_jump(self):
        d=self.model().derive()
        self.assertEqual(s.simplify(d['q_equation_jump'].subs(
            {d['speed']:1,d['beta']:0,d['amplitude']:1,d['db']:0})), 2)
        self.assertNotEqual(d['transmission_determinant'], 0)
        self.assertEqual(d['transmission_residual'], s.zeros(2,1))

    def test_characteristic_exception_and_shape_condition_are_retained(self):
        d=self.model().derive()
        for k in ('q_equation_jump','shear_equation_jump'):
            self.assertEqual(s.simplify(d[k].subs({d['speed']:-d['beta'],d['db']:0})), 0)
        self.assertEqual(d['shape_jump'], 0)
        self.assertEqual(d['auxiliary_factorization_error'], 0)

    def test_inactive_clock_equation_is_varied_before_restricting(self):
        d=self.model().derive()
        self.assertEqual(d['inactive_clock_direct_identity'], 0)
        self.assertNotEqual(d['inactive_clock_equation'], 0)


if __name__=='__main__':unittest.main()
