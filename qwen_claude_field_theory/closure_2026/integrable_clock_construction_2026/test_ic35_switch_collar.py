"""A finite-multiplier mixed-activation collar must solve the varied constraints."""
import importlib.util
import unittest


class SwitchCollarTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic35_switch_collar'))
        import ic35_switch_collar
        return ic35_switch_collar

    def test_principal_matrix_is_computed_from_action(self):
        for name,value in self.module().identities().items():
            self.assertEqual(value,0,name)

    def test_collar_crosses_switch_with_finite_auxiliary(self):
        row=self.module().experiment(width=.01,nodes=401)
        self.assertTrue(row['success'],row)
        self.assertGreater(row['activation_square_range'][1],.75)
        self.assertLess(row['activation_square_range'][0],.5)
        self.assertLess(row['max_ode_residual'],1e-5)
        self.assertLess(row['max_auxiliary_residual'],1e-8)

    def test_profile_is_selected_by_first_preservation(self):
        m=self.module()
        self.assertTrue(hasattr(m,'integrable_collar'))
        row=m.integrable_collar(width=.002,nodes=401)
        self.assertTrue(row['success'],row)
        self.assertLess(row['max_relative_ode_residual'],1e-5)
        self.assertLess(row['max_first_preservation_residual'],1e-7)
        self.assertLess(row['activation_square_range'][0],.5)
        self.assertGreater(row['activation_square_range'][1],.5)


if __name__=='__main__':
    unittest.main()
