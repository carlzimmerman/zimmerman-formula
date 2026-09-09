"""Action-derived joint completion: static jets, constraints and live evolution."""
import importlib.util
import pathlib
import unittest
import mpmath as mp


class JointCompletionTests(unittest.TestCase):
    def model(self):
        path=pathlib.Path(__file__).with_name('ic20_joint_completion.py')
        self.assertTrue(path.exists(),'Joint-completion action computation missing')
        spec=importlib.util.spec_from_file_location('ic20',path)
        m=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        mp.mp.dps=60
        return m

    def test_exact_joint_and_static_identities(self):
        m=self.model()
        checks=m.identities()
        self.assertGreater(len(checks),6)
        self.assertTrue(all(v==0 for v in checks.values()),checks)

    def test_coefficients_are_solved_from_actual_variations(self):
        m=self.model()
        p=m.design()
        b=m.state(p['S0'],p['q0'],p['z0'],0,p)
        self.assertLess(max(abs(v) for v in b['constraints']),mp.mpf('1e-45'))
        self.assertGreater(b['H_physical'],0)
        self.assertTrue(0<b['scalar_UV_speed_squared']<1)
        self.assertLess(abs(b['tensor_speed_squared']-1),mp.mpf('1e-45'))

    def test_auxiliary_rank_is_computed_in_uniform_and_spatial_modes(self):
        m=self.model()
        p=m.design()
        b=m.state(p['S0'],p['q0'],p['z0'],0,p)
        for k2 in (0,1,10000):
            block=m.constraint_block(b,k2)
            self.assertEqual(block['rank'],4)
            self.assertGreater(block['determinant'],0)

    def test_curvature_coefficient_is_not_a_propagating_field_by_assumption(self):
        m=self.model()
        p=m.design()
        b=m.state(p['S0'],p['q0'],p['z0'],0,p)
        self.assertLess(b['raw_zz'],0)
        self.assertGreater(b['scalar_UV_momentum'],0)
        self.assertLess(abs(b['compatibility_residual']),mp.mpf('1e-45'))

    def test_scalar_dispersion_uses_the_full_reduced_matrix(self):
        m=self.model()
        p=m.design()
        b=m.state(p['S0'],p['q0'],p['z0'],0,p)
        d=m.dispersion(b,'1e12')
        self.assertGreater(d['momentum_coefficient'],0)
        self.assertGreater(d['frequency_squared'],0)
        self.assertLess(abs(d['speed_squared']-b['scalar_UV_speed_squared']),mp.mpf('1e-6'))
        lower=m.dispersion(b,'1e10')
        self.assertLess(abs(d['speed_squared']-b['scalar_UV_speed_squared']),
                        abs(lower['speed_squared']-b['scalar_UV_speed_squared'])/90)

    def test_mutating_the_designed_first_derivative_changes_the_cone(self):
        m=self.model()
        p=m.design()
        b=m.state(p['S0'],p['q0'],p['z0'],0,p)
        altered=dict(p);altered['a1']+=1
        bad=m.state(p['S0'],p['q0'],p['z0'],0,altered)
        self.assertGreater(abs(bad['scalar_UV_speed_squared']-b['scalar_UV_speed_squared']),mp.mpf('.001'))

    def test_strict_report_refuses_full_closure(self):
        m=self.model()
        self.assertEqual(m.completion_status({'checks':{'a':False}},False),1)
        self.assertEqual(m.completion_status({'checks':{'a':True}},True),2)

    def test_background_constraints_are_preserved_along_actual_evolution(self):
        m=self.model()
        self.assertTrue(hasattr(m,'continuation'),'Background continuation missing')
        result=m.continuation(steps=4,step='-.00001')
        self.assertGreater(len(result['states']),1)
        self.assertLess(result['maximum_constraint_residual'],mp.mpf('1e-40'))
        self.assertLess(result['maximum_preservation_residual'],mp.mpf('1e-40'))
        self.assertGreater(result['efolds_from_charge'],0)

    def test_time_dependent_curvature_mixing_is_not_frozen_away(self):
        m=self.model()
        p=m.design();b=m.state(p['S0'],p['q0'],p['z0'],0,p)
        self.assertIn('frozen_scalar_UV_speed_squared',b)
        self.assertGreater(abs(b['scalar_UV_speed_squared']-b['frozen_scalar_UV_speed_squared']),mp.mpf('.01'))

    def test_spatial_secondary_bracket_includes_curvature_variation(self):
        m=self.model();p=m.design();b=m.state(p['S0'],p['q0'],p['z0'],0,p)
        r=b['raw'];k2=mp.mpf(7)
        fQ=3*r['S']-3*b['q']*r['Sq']+4*k2*r['SR']
        gQ=3*r['z']-3*b['q']*r['qz']+4*k2*r['zR']
        direct=(fQ*r['qz']-r['Sq']*gQ)/2
        calculated=m.constraint_block(b,k2)['poisson_matrix'][2][3]
        self.assertLess(abs(calculated-direct),mp.mpf('1e-45'))

    def test_matter_background_is_varied_not_borrowed_from_old_cosmology(self):
        m=self.model()
        self.assertTrue(hasattr(m,'matter_continuation'))
        r=m.matter_continuation(steps=4,step='.00001')
        self.assertEqual(len(r['states']),5)
        self.assertLess(r['maximum_constraint_residual'],mp.mpf('1e-40'))
        self.assertLess(r['maximum_charge_residual'],mp.mpf('1e-40'))
        self.assertGreater(r['states'][-1]['Q'],0)

    def test_all_wavelength_identity_retains_time_derivative_of_lapse_mixing(self):
        m=self.model();p=m.design();b=m.state(p['S0'],p['q0'],p['z0'],0,p)
        self.assertTrue(hasattr(m,'all_wavelength_witness'))
        r=m.all_wavelength_witness(b)
        self.assertTrue(0<r['IR_ratio']<1)
        self.assertLess(r['maximum_direct_residual'],mp.mpf('1e-40'))


if __name__=='__main__':unittest.main()
