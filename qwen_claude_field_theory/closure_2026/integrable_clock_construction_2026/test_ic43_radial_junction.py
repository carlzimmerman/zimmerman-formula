import importlib.util
import unittest


class RadialJunctionTests(unittest.TestCase):
    def test_auxiliary_normal_derivative_jump_has_zero_metric_and_variational_flux(self):
        self.assertIsNotNone(importlib.util.find_spec('ic43_radial_junction'))
        out=__import__('ic43_radial_junction').derive()
        self.assertTrue(all(v==0 for v in out['auxiliary_flux_jump']))
        self.assertEqual(out['physical_lapse_jump'],0)
        self.assertEqual(out['physical_spatial_jump'],0)
        self.assertEqual(out['physical_gradient_identity'],0)


if __name__=='__main__':unittest.main()
