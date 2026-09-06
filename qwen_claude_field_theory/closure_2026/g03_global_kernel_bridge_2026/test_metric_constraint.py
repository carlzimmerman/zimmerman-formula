"""Tests for a metric-only constrained MOND Hamiltonian, not a closure badge."""
import importlib.util
import unittest

AVAILABLE = importlib.util.find_spec('metric_constraint') is not None


class ImplementationTest(unittest.TestCase):
    def test_metric_constraint_calculation_exists(self):
        self.assertTrue(AVAILABLE,'Constraint-first calculation missing')


@unittest.skipUnless(AVAILABLE,'not implemented')
class MetricConstraintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import metric_constraint
        cls.r=metric_constraint.derive()

    def test_same_Hamiltonian_static_and_homogeneous_gates(self):
        self.assertTrue(all(self.r['checks'].values()))
        self.assertEqual(self.r['static_slip_residual'],'0')
        self.assertGreater(self.r['homogeneous_expanding_H_squared'],0)

    def test_primary_secondary_and_higher_preservation(self):
        for row in self.r['dirac'].values():
            self.assertTrue(row['preservation_closed'])
            self.assertEqual(row['scalar_mode_count'],0)
        self.assertGreater(len(self.r['dirac']['generic']['generations']),2)

    def test_generic_symbolic_rank_not_only_a_numeric_witness(self):
        row=self.r['dirac']['generic_symbolic']
        self.assertTrue(row['preservation_closed'])
        self.assertIn('alpha',' '.join(row['constraints']))

    def test_homogeneous_canonical_clock_count_separate_from_local_mode(self):
        row=self.r['homogeneous_dirac']
        self.assertTrue(row['preservation_closed'])
        self.assertEqual(row['physical_pairs_including_dust_clock'],1)
        self.assertEqual(row['second_class'],0)
        self.assertNotEqual(row['expanding_momentum_squared'],0)

    def test_tensor_principal_kinetic_and_dispersion_are_computed(self):
        self.assertTrue(self.r['checks']['tensor_principal_positive_kinetic'])
        self.assertTrue(self.r['checks']['tensor_principal_luminal'])

    def test_static_zero_field_has_a_coercive_energy_not_a_fake_inverse(self):
        self.assertTrue(self.r['checks']['static_energy_generates_mu'])
        self.assertTrue(self.r['checks']['static_energy_quadratic_lower_bound'])
        self.assertTrue(self.r['checks']['longitudinal_eigenvalue_exceeds_transverse'])
        self.assertIn('y**3',self.r['static_energy_zero_field_series'])

    def test_zero_field_rank_not_inherited(self):
        self.assertNotEqual(self.r['dirac']['generic']['bracket_rank'],
                            self.r['dirac']['zero_field']['bracket_rank'])
        self.assertFalse(self.r['nonlinear_DOF_certified'])

    def test_causal_probe_is_conserved_and_not_a_gauge_potential(self):
        self.assertTrue(self.r['checks']['probe_conserved'])
        self.assertNotEqual(self.r['principal_tidal_probe'],0)
        self.assertEqual(self.r['GR_tidal_difference'],'0')


if __name__=='__main__':
    unittest.main()
