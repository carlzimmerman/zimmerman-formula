"""Checks of the constraint-reduced global vacuum evolution, not full closure."""
import importlib.util
import unittest
import numpy as np


class GlobalEvolutionTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('metric_global_evolution'),
                             'The same-action global evolution implementation is missing')
        import metric_global_evolution
        return metric_global_evolution

    def test_canonical_reduction_and_momentum_integral_are_derived(self):
        r=self.module().derive_reduction()
        self.assertTrue(all(x=='0' for x in r['identity_residuals'].values()))
        self.assertNotEqual(r['global_trace_kinetic_coefficient'],'0')

    def test_spatial_gauge_reconstruction_satisfies_varied_equations(self):
        r=self.module().gauge_covariance()
        self.assertEqual(r['on_shell_gauge_EL_residuals'],['0','0','0'])

    def test_fixed_wall_lapse_does_not_impose_zero_boundary_energy(self):
        r=self.module().boundary_charge()
        self.assertEqual(r['lapse_homogeneity_residual'],'0')
        self.assertEqual(r['boundary_charge_identity_residual'],'0')
        self.assertNotEqual(r['charge_normal_metric_derivative'],'0')

    def test_vacuum_force_is_spatially_constant_on_full_curved_background(self):
        r=self.module().global_response(.5,0.,.02)
        self.assertLess(r['force_constancy_absolute'],1e-7)
        self.assertLess(r['ODE_residual'],1e-5)
        self.assertLess(r['boundary_residual'],1e-9)
        self.assertLess(r['mean_residual'],1e-9)
        self.assertLess(r['refinement_relative'],1e-6)

    def test_generator_preserves_reduced_symplectic_form(self):
        r=self.module().global_response(.5,0.,.02)
        M=np.array(r['generator']); O=np.array(r['symplectic_matrix'])
        self.assertLess(np.linalg.norm(M.T@O+O@M)/(1+np.linalg.norm(O@M)),1e-7)

    def test_matrix_exponential_solves_actual_computed_generator(self):
        r=self.module().global_response(.5,0.,.02)
        self.assertLess(r['evolution_refinement_relative'],1e-7)
        self.assertLess(r['quadratic_invariant_drift'],1e-7)

    def test_growth_gate_is_computed_and_distinguishes_a_stable_control(self):
        m=self.module()
        stable=np.array([[0.,1.],[-1.,0.]])
        growing=np.array([[0.,1.],[1.,0.]])
        self.assertEqual(m.growth_gate(stable,stable)['status'],'UNRESOLVED')
        self.assertEqual(m.growth_gate(growing,growing)['status'],'FAIL')
        r=m.global_response(.5,0.,.02)
        self.assertEqual(r['growth_gate']['status'],'FAIL')
        self.assertLess(r['quartic_identity_residual'],1e-10)
        self.assertGreater(r['growth_gate']['resolution_ratio'],100)

    def test_unresolved_is_not_a_strict_stability_pass(self):
        m=self.module()
        r=dict(audit_pass=True,cases=[dict(growth_gate=dict(status='UNRESOLVED'))])
        self.assertEqual(m.exit_status(r,True),2)

    def test_high_field_characteristic_identity_avoids_float_cancellation(self):
        r=self.module().global_response(10.5,float(32*np.pi),.002)
        self.assertLess(r['quartic_identity_residual'],1e-10)

    def test_excluded_zero_field_and_singular_chart_are_not_certified(self):
        for y in [0.,1.]:
            with self.assertRaises(ValueError):
                self.module().global_response(y,0.,.01)


if __name__=='__main__':
    unittest.main()
