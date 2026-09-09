"""The angular equation must be varied before radial isotropic gauge fixing."""
import importlib.util
import unittest


class UnpinnedAngularTests(unittest.TestCase):
    def result(self):
        self.assertIsNotNone(importlib.util.find_spec('ic45_unpinned_angular'))
        import ic45_unpinned_angular as module
        return module.derive()

    def test_unpinned_action_and_curvature_match_existing_definitions(self):
        d=self.result()
        self.assertEqual(d['curvature_identity'], 0)
        self.assertEqual(d['action_boundary_identity'], 0)
        self.assertEqual(d['trace_identity'], 0)

    def test_angular_evolution_is_not_discarded_by_isotropic_gauge(self):
        d=self.result()
        self.assertNotEqual(d['shear_equation'], 0)
        self.assertEqual(d['shear_jump_identity'], 0)

    def test_six_condition_construction_satisfies_independent_angular_transmission(self):
        d=self.result()
        self.assertEqual(d['ic44_angular_residual'], 0)


if __name__=='__main__':unittest.main()
