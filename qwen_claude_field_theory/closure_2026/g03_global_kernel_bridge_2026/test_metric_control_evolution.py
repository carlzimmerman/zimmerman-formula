"""Next-jet tests: distinguish a correct audit from a surviving wall gate."""
import unittest
import numpy as np
import sympy as s

from metric_control_evolution import derive_next, evolve_control, recursion_identities
from metric_collar_control import CENTERS, WIDTH


class NextJetTests(unittest.TestCase):
    def test_canonical_recursion_retains_pressure_and_anisotropic_momenta(self):
        d = recursion_identities()
        self.assertEqual(d['pressure_force_residuals'], ['0','0'])
        self.assertEqual(d['trace_kinematic_residual'], '0')
        self.assertEqual(d['conformal_operator_residuals'], ['0']*12)
        self.assertNotEqual(d['radial_minus_transverse_velocity'], '0')

    def test_observable_is_spacetime_scalar_not_only_foliation_projection(self):
        d = recursion_identities()
        self.assertEqual(d['Ricci_scalar_residual'], '0')
        self.assertEqual(d['Ricci_normal_residual'], '0')

    def test_momentum_constraint_propagates_using_KG_not_prescribed_stress(self):
        d = recursion_identities()
        self.assertEqual(d['canonical_KG_momentum_Ward_residual'], '0')
        self.assertEqual(d['gravitational_spatial_Noether_residual'], '0')

    def test_derivative_normalization_and_curved_density_cancellation(self):
        d = derive_next()
        self.assertEqual(d['density_third'], '0')
        self.assertEqual(d['trace_second_coefficient'], '-24')
        self.assertEqual(d['trace_third_coefficient'], '288')
        self.assertEqual(d['forcing_ratio'], '-12')

    def test_sixth_jet_product_rule_includes_normal_metric_jet(self):
        d = derive_next()
        self.assertEqual(d['sixth_identity_residual'], '0')
        self.assertNotEqual(d['normal_metric_omission_residual'], '0')

    def test_reintegrated_source_is_not_silently_reoptimized(self):
        r = evolve_control(.5, 0., .02)
        self.assertEqual(len(r['forcing_probes']), 10)
        for x, lapse, actual in r['forcing_probes']:
            offsets = (x-CENTERS)/WIDTH
            expected = sum(weight*np.exp(1-1/(1-offset**2))
                           for offset,weight in zip(offsets,r['input_weights']) if abs(offset)<1)
            self.assertAlmostEqual(actual/(-288*lapse**3), expected, places=12)
        self.assertLess(r['second_control_relative'], 1e-5)
        self.assertLess(r['refinement_relative'], 1e-5)
        self.assertLess(r['ODE_residual'], 1e-5)
        self.assertLess(r['boundary_residual'], 1e-9)
        self.assertGreater(r['next_control_resolution'], 100)
        self.assertEqual(r['fixed_profile_next_collar_gate'], 'FAIL')

    def test_singular_scaling_is_rejected_not_called_zero_response(self):
        with self.assertRaises(ValueError):
            evolve_control(1., 0., .01)

    def test_unresolved_cannot_satisfy_strict_requirement(self):
        from metric_control_evolution import exit_status
        result = dict(audit_checks_pass=True,cases=[dict(fixed_profile_next_collar_gate='UNRESOLVED')])
        self.assertEqual(exit_status(result,True),2)
        self.assertEqual(exit_status(result,False),0)
        result['audit_checks_pass']=False
        self.assertEqual(exit_status(result,False),1)


if __name__ == '__main__':
    unittest.main()
