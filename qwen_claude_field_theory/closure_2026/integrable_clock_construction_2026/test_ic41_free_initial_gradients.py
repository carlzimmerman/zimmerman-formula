"""Catch frozen gradients, omitted fluid flux, and a changed legacy third jet."""
import importlib.util
import unittest


class FreeGradientTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic41_free_initial_gradients'))
        return __import__('ic41_free_initial_gradients')

    def test_default_reproduces_independent_third_jet(self):
        out=self.module().field_result(dps=40,order=3)
        actual=float(out['third_W_boundary_jets'][2])
        self.assertLess(abs(actual/(-2272082897.48038343867)-1),1e-12)
        self.assertLess(float(out['second_gate_relative_error']),1e-18)

    def test_selector_uses_all_four_independent_conditions(self):
        m=self.module();self.assertTrue(callable(getattr(m,'condition_vector',None)))
        out={'second_gate_jets':['0','0','2','3'],
             'motion_corrected_third_jets':['0','0','5','7']}
        self.assertEqual(list(m.condition_vector(out)),[2,3,5,7])

    def test_changed_gradients_preserve_initial_constraints_and_face_orientation(self):
        out=self.module().field_result(qprime='-50',Sprime='0.01',dps=40,order=3)
        self.assertLess(float(out['first_constraint_error']),1e-18)
        self.assertLess(float(out['second_momentum_residual']),1e-18)
        self.assertLess(float(out['third_momentum_residual']),1e-15)
        self.assertAlmostEqual(float(out['activation_radial_derivative']),50.811946161601782,places=10)


if __name__=='__main__':unittest.main()
