import unittest
import background_audit as a


class BackgroundTests(unittest.TestCase):
    def test_einstein_momentum_is_computed_from_curvature(self):
        g=a.geometry()
        self.assertTrue(g['checks']['all_geometry_momentum_components_zero'])
        self.assertTrue(g['checks']['hamiltonian_component'])
        self.assertGreater(g['nonzero_christoffels'],0)

    def test_comoving_matter_has_no_momentum(self):
        self.assertTrue(a.geometry()['checks']['comoving_perfect_fluid_momentum_zero'])

    def test_gamma0_and_cubic_metric_variations(self):
        checks=a.derive()['checks']
        for k in ['gamma0_metric_flux','cubic_metric_flux','total_flux']:
            self.assertTrue(checks[k])

    def test_generalized_shift_current_matches_flux(self):
        checks=a.derive()['checks']
        self.assertTrue(checks['flux_equals_gradient_times_shift_current'])
        self.assertTrue(checks['scalar_Euler_is_charge_conservation'])

    def test_energy_and_independent_integration_by_parts(self):
        checks=a.derive()['checks']
        for k in ['cubic_energy_sign_and_Y_term','energy_current_identity',
                  'independent_cubic_integration_by_parts','isotropic_zero_gradient_energy']:
            self.assertTrue(checks[k])

    def test_comoving_gradient_kinematics(self):
        self.assertTrue(a.derive()['checks']['projected_gradient_redshifts'])


if __name__=='__main__':unittest.main()
