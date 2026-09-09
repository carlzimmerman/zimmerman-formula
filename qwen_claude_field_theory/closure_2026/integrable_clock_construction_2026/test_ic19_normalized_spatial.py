"""IC19: protect the normalization, variational operator, and mode separation."""
import importlib.util
import pathlib
import unittest
import mpmath as mp


class NormalizedSpatialTests(unittest.TestCase):
    def model(self):
        path=pathlib.Path(__file__).with_name('ic19_normalized_spatial.py')
        self.assertTrue(path.exists(), 'The normalized action computation is missing')
        spec=importlib.util.spec_from_file_location('ic19',path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        mp.mp.dps=60
        return module

    def test_normalization_is_imposed_in_the_action_not_a_display(self):
        m=self.model()
        c=m.constants()
        self.assertLess(abs(32*mp.pi*c['a02']/c['Lambda']-1),mp.mpf('1e-50'))
        self.assertGreater(abs(m.legacy.constants()['a02']-c['a02']),1)

    def test_exact_spatial_variation_and_tensor_repair(self):
        m=self.model()
        checks=m.identities()
        self.assertGreater(len(checks),5)
        self.assertTrue(all(v==0 for v in checks.values()),checks)

    def test_expanding_plateau_has_a_uniform_activation_margin(self):
        m=self.model()
        result=m.plateau_domain()
        self.assertGreater(result['analytic_r_squared_lower_bound'],mp.mpf('.75'))
        # At S=100.075 the nonvacuum correction is below 60-digit precision;
        # the direct Friedmann evaluation can lie one rounding unit below the bound.
        self.assertTrue(all(row['r_squared']>=result['analytic_r_squared_lower_bound']-mp.mpf('1e-50') for row in result['samples']))
        self.assertTrue(all(row['FX']>0 and row['Q']>row['FX'] for row in result['samples']))

    def test_spatial_lapse_operator_matches_direct_variation(self):
        m=self.model()
        row=m.curved_point('.1','.8')
        self.assertLess(abs(row['secondary_residual']),mp.mpf('1e-45'))
        self.assertLess(abs(row['direct_lapse_hessian_residual']),mp.mpf('1e-45'))
        self.assertGreater(row['Rbar'],0)

    def test_zero_and_nonzero_modes_are_not_the_same_rank_input(self):
        m=self.model()
        rows=[m.curved_point('.1',r) for r in ('.75','.8','.84')]
        self.assertTrue(all(row['B']>0 for row in rows))
        for row in rows:
            self.assertNotEqual(row['mode_operator'][0],row['mode_operator'][1])

    def test_domain_and_strict_status(self):
        m=self.model()
        with self.assertRaises(ValueError):m.curved_point('.075','.8')
        with self.assertRaises(ValueError):m.curved_point('.1','.1')
        self.assertEqual(m.completion_status({'checks':{'a':False}},False),1)
        self.assertEqual(m.completion_status({'checks':{'a':True}},True),2)

    def test_switch_has_no_hidden_lapse_derivative_at_fixed_canonical_momentum(self):
        m=self.model()
        self.assertTrue(hasattr(m,'switch_argument'),'Lapse-independent switch missing')
        self.assertLess(abs(mp.diff(lambda S:m.switch_argument(S,mp.mpf('-2.1')),mp.mpf('.1'))),mp.mpf('1e-50'))

    def test_scalar_kinetic_is_not_inferred_from_lapse_rank(self):
        m=self.model()
        self.assertTrue(hasattr(m,'scalar_kinetic'),'Reduced scalar kinetic calculation missing')
        row=m.scalar_kinetic('.1','.8',1)
        self.assertLess(abs(row['schur_identity_residual']),mp.mpf('1e-45'))

    def test_preservation_on_the_curved_background_is_computed(self):
        m=self.model()
        row=m.curved_point('.1','.82')
        self.assertIn('direct_preservation_residual',row)
        self.assertGreater(row['H_physical'],0)
        self.assertLess(abs(row['direct_preservation_residual']),mp.mpf('1e-45'))

    def test_curvature_repair_must_check_the_cross_term(self):
        m=self.model()
        self.assertTrue(hasattr(m,'curvature_completion'),'Curvature compatibility calculation missing')
        result=m.curvature_completion()
        self.assertEqual(result['uncompleted_control'], -4)
        self.assertEqual(result['completed_hessian_residual'],0)


if __name__=='__main__':unittest.main()
