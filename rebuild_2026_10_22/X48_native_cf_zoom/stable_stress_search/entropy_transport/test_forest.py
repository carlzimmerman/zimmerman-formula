"""Quiet-domain evolution checks, not observed forest likelihood tests."""
import unittest

import numpy as np
from scipy.integrate import solve_ivp

import refinement as evolution
import material


class ForestDomainTests(unittest.TestCase):
    def setUp(self):
        self.parameters = material.MaterialParameters(rho_q=1, G=1,
                                                      a0=np.sqrt(8*np.pi), tau=.5)

    def test_unheated_expanding_perturbation_remains_exactly_cold_above_density_gate(self):
        model = evolution.FloorAuditedCollapse(24, self.parameters,
                                              initial_density=1.5,
                                              initial_velocity_gradient=2.0)
        state = model.initial_state()
        state[:24] *= 1 + .01*np.sin(np.pi*state[:24])
        state[24:48] = 2*state[:24]
        result = evolution.simulate(model, initial_state=state, t_end=.05,
                                     samples=6, wall_seconds=5)
        self.assertEqual(result['status'], 'completed')
        np.testing.assert_array_equal(result['final_profile']['K'], np.zeros(24))
        np.testing.assert_array_equal(result['final_profile']['luminosity'], np.zeros(25))
        np.testing.assert_array_equal(result['final_profile']['pressure'], np.zeros(24))
        np.testing.assert_array_equal(result['final_profile']['q'], np.zeros(24))

        # Independent reduced gravity equations contain no memory coordinate.
        enclosed_mass = model.dm*np.arange(1, 25)
        def gravity_only(t, phase):
            return np.r_[phase[24:], -self.parameters.G*enclosed_mass/phase[:24]**2]
        reference = solve_ivp(gravity_only, (0, .05), state[:48],
                              method='DOP853', rtol=1e-11, atol=1e-13)
        self.assertTrue(reference.success)
        np.testing.assert_allclose(result['final_profile']['r'], reference.y[:24, -1],
                                   rtol=2e-9, atol=2e-11)
        np.testing.assert_allclose(result['final_profile']['u'], reference.y[24:, -1],
                                   rtol=2e-9, atol=2e-11)

    def test_dilute_material_with_retained_heat_has_dust_motion_and_constant_memory(self):
        model = evolution.FloorAuditedCollapse(16, self.parameters,
                                              initial_density=.25,
                                              initial_velocity_gradient=.5)
        warm = model.initial_state()
        warm[32:] = np.geomspace(.01, 100, 16)
        cold = warm.copy(); cold[32:] = 0
        heated = evolution.simulate(model, initial_state=warm, t_end=.05,
                                      samples=6, wall_seconds=5)
        virgin = evolution.simulate(model, initial_state=cold, t_end=.05,
                                      samples=6, wall_seconds=5)
        self.assertEqual(heated['status'], 'completed')
        self.assertEqual(virgin['status'], 'completed')
        np.testing.assert_array_equal(heated['final_profile']['K'], warm[32:])
        np.testing.assert_array_equal(heated['final_profile']['luminosity'], np.zeros(17))
        np.testing.assert_allclose(heated['final_profile']['r'], virgin['final_profile']['r'],
                                   rtol=2e-10, atol=2e-12)
        np.testing.assert_allclose(heated['final_profile']['u'], virgin['final_profile']['u'],
                                   rtol=2e-10, atol=2e-12)


if __name__ == '__main__':
    unittest.main()
