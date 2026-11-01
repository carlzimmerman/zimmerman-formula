"""Independent benchmarks for the bounded spherical equilibrium experiment."""
import unittest

import numpy as np

from equilibria import density_from_enthalpy, solve_equilibrium, match_mass, dust_shell_radius
from material import dimensionless_enthalpy


class EquilibriumTests(unittest.TestCase):
    def test_enthalpy_inverse_across_both_active_branches(self):
        for density in (1.001, 1.1, 1.5, 1.9, 2.0, 5.0, 30.0):
            with self.subTest(density=density):
                self.assertAlmostEqual(density_from_enthalpy(float(dimensionless_enthalpy(density))), density, places=9)

    def test_dense_interior_matches_exact_sinc_profile(self):
        equilibrium = solve_equilibrium(20.0)
        x = np.array([0.1, 0.5, 1.0, 2.0])
        exact = 20 * np.sinc(x / (np.sqrt(2) * np.pi))
        actual = equilibrium.density(x)
        np.testing.assert_allclose(actual, exact, rtol=2e-7, atol=1e-8)
        self.assertGreater(equilibrium.radius, 2.0)

    def test_free_surface_and_monotone_mass(self):
        equilibrium = solve_equilibrium(5.0)
        x = np.linspace(0, equilibrium.radius, 200)
        self.assertAlmostEqual(float(equilibrium.density(equilibrium.radius)), 1.0, places=7)
        self.assertTrue(np.all(np.diff(equilibrium.mass_inside(x)) >= 0))
        self.assertGreater(equilibrium.core_radius, 0)
        self.assertLess(equilibrium.half_mass_radius, equilibrium.radius)

    def test_smooth_baryon_loading_preserves_cold_mass_and_finite_center(self):
        initial = solve_equilibrium(10.0)
        final = match_mass(initial.mass, 0.1 * initial.mass, 0.2 * initial.radius,
                           central_hint=initial.central_density)
        self.assertLess(abs(final.mass / initial.mass - 1), 2e-7)
        self.assertGreater(final.central_density, initial.central_density)
        self.assertTrue(np.isfinite(final.central_density))
        self.assertGreater(final.core_radius, 0)

    def test_pressure_branch_resists_more_than_circular_dust_reference(self):
        initial = solve_equilibrium(10.0)
        baryon_mass = 0.1 * initial.mass
        baryon_scale = 0.2 * initial.radius
        final = match_mass(initial.mass, baryon_mass, baryon_scale,
                           central_hint=initial.central_density)
        for fraction in (0.01, 0.05, 0.1, 0.5):
            initial_radius = initial.radius_at_mass_fraction(fraction)
            final_radius = final.radius_at_mass_fraction(fraction)
            reference = dust_shell_radius(initial_radius, fraction * initial.mass,
                                          baryon_mass, baryon_scale)
            self.assertLess(reference, final_radius)
            self.assertLess(final_radius, initial_radius)
            self.assertAlmostEqual(float(final.mass_inside(final_radius))/final.mass,
                                   fraction, places=8)

    def test_invalid_equilibrium_and_baryon_parameters(self):
        for density in (1.0, 0.0, np.nan):
            with self.subTest(density=density), self.assertRaises(ValueError):
                solve_equilibrium(density)
        for mass, scale in ((-1, 1), (1, 0), (1, np.nan)):
            with self.subTest(mass=mass, scale=scale), self.assertRaises(ValueError):
                solve_equilibrium(5, baryon_mass=mass, baryon_scale=scale)


if __name__ == "__main__":
    unittest.main()
