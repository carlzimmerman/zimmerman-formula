"""Nonlinear pinned exterior constraints, from the IC30 varied action."""
import importlib.util
import unittest
import sympy as s


class PinnedTailTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic31_pinned_tail'))
        import ic31_pinned_tail
        return ic31_pinned_tail

    def test_lapse_operator_from_unpinned_variation(self):
        for name,value in self.module().identities().items():
            self.assertEqual(s.simplify(value),0,name)

    def test_shear_free_control_and_fixed_action_tail(self):
        m=self.module(); models=m.models()
        control=m.solve(models[0],amplitude=0,nodes=121)
        self.assertTrue(control['success'])
        self.assertLess(control['max_lapse_displacement'],1e-10)
        result=m.solve(models[0],amplitude=1,nodes=121)
        self.assertTrue(result['success'])
        self.assertLess(result['max_lapse_residual'],1e-7)
        self.assertLess(result['max_z_residual'],1e-10)
        self.assertLess(result['max_w_residual'],1e-8)
        self.assertGreater(result['min_D'],0)
        self.assertGreater(result['min_pin_margin'],0)
        self.assertGreater(result['max_lapse_displacement'],1e-6)
        self.assertLess(result['constraint_jacobian_largest_eigenvalue'],0)
        self.assertLess(result['max_shift_residual'],1e-7)


if __name__=='__main__':
    unittest.main()
