"""Wall compatibility: catch omitted normal metric evolution and KG jet terms."""
import importlib.util
import unittest

AVAILABLE=importlib.util.find_spec('metric_wall_jets') is not None


class ImplementationTest(unittest.TestCase):
    def test_wall_jet_calculation_exists(self):
        self.assertTrue(AVAILABLE,'Higher boundary compatibility calculation missing')


@unittest.skipUnless(AVAILABLE,'not implemented')
class WallJetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import metric_wall_jets as model
        cls.r=model.audit()

    def test_canonical_kinetic_reduction(self):
        self.assertEqual(self.r['symbolic']['kinetic_reduction_residual'],'0')
        self.assertEqual(self.r['symbolic']['normal_fourth_identity_residual'],'0')

    def test_KG_time_jet_is_computed_not_assigned(self):
        self.assertEqual(self.r['symbolic']['KG_fifth_identity_residual'],'0')
        self.assertEqual(self.r['symbolic']['wall_third_jet'],'0')
        self.assertEqual(self.r['symbolic']['wall_fourth_jet'],'0')

    def test_full_constraints_reduce_the_fifth_jet(self):
        self.assertEqual(self.r['symbolic']['on_shell_reduction_residual'],'0')

    def test_response_is_resolved_before_boundary_verdict(self):
        for row in self.r['responses']:
            self.assertLess(row['boundary_residual'],1e-9)
            self.assertLess(row['ODE_residual'],1e-6)
            self.assertLess(row['refinement_difference'],1e-6)


if __name__=='__main__':
    unittest.main()
