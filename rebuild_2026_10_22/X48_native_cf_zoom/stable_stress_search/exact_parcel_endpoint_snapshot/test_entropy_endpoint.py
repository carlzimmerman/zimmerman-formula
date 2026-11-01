"""Independent EOS, fixed-mass and energy checks for constructed endpoints."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

import equilibria
import material

import entropy_endpoint as endpoint


class EntropyEndpointTests(unittest.TestCase):
    def setUp(self):
        self.params = material.MaterialParameters(rho_q=1, G=1, a0=np.sqrt(8 * np.pi), tau=0.5)

    def test_loading_preserves_exact_parcel_values_and_hashes_source_bytes(self):
        payload = dict(total_mass=1.0, n_shells=3, t_reached=8.0,
                       initial=dict(total=-0.5), final_profile=dict(K=[0.3, 0.1, 0.2]))
        raw = (json.dumps(payload) + "\n").encode()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "collapse.json"
            path.write_bytes(raw)
            profile = endpoint.load_collapse(path)
        np.testing.assert_array_equal(profile.sorted_K, [0.1, 0.2, 0.3])
        self.assertEqual(profile.input_sha256, hashlib.sha256(raw).hexdigest())
        self.assertEqual(profile.source_time, 8.0)
        self.assertEqual(profile.initial_energy, -0.5)
        mass = np.linspace(0, 1, 10001)
        self.assertAlmostEqual(float(np.trapz(profile.coefficient(mass), mass)), 0.2, places=9)

    def test_continuous_entropy_integral_accounts_for_concave_interpolation(self):
        profile = endpoint.EntropyProfile([1.0, 8.0], 2.0)
        summary = endpoint.entropy_integrals(profile, self.params, alpha=8.0)
        self.assertAlmostEqual(summary["source_discrete_sigma_mass_integral"], 3.0)
        self.assertAlmostEqual(summary["sorted_continuous_sigma_mass_integral"], 87 / 28)
        self.assertAlmostEqual(summary["endpoint_continuous_sigma_mass_integral"], 87 / 14)
        self.assertGreaterEqual(summary["interpolation_relative_entropy_increase"], 0)

    def test_pressure_inverse_is_checked_against_the_independent_material_law(self):
        densities = np.r_[1.0, 1 + np.geomspace(1e-6, 0.99, 50), 2.0, 3.0, 20.0]
        K = np.geomspace(0.01, 2.0, len(densities))
        pressure = material.pressure(densities, K, self.params)
        recovered = endpoint.density_from_pressure(pressure, K, self.params)
        np.testing.assert_allclose(recovered, densities, rtol=2e-9, atol=3e-10)

    def test_constant_entropy_matches_independent_enthalpy_integration(self):
        # The existing solver uses dimensionless enthalpy, not P(r), as state.
        K = 0.3
        reference = equilibria.solve_equilibrium(5.0, rtol=2e-10, max_step=0.02)
        length = np.sqrt(K / (4 * np.pi))
        mass = 4 * np.pi * length**3 * reference.mass
        profile = endpoint.EntropyProfile(np.full(8, K), mass)
        result = endpoint.solve_equilibrium(profile, self.params, rtol=2e-8)
        self.assertAlmostEqual(result["central_density"], 5.0, places=4)
        self.assertAlmostEqual(result["radius"], reference.radius * length, places=5)
        self.assertLess(result["relative_mass_error"], 1e-6)
        self.assertGreater(result["core_radius"], 0)

    def test_energy_integral_agrees_with_independent_profile_quadrature(self):
        profile = endpoint.EntropyProfile(np.linspace(0.02, 0.5, 8), 1.0)
        result = endpoint.solve_equilibrium(profile, self.params, output_points=2049)
        f = result["profile"]
        r, m, rho, K = (np.array(f[k]) for k in ["r", "m", "rho", "K"])
        potential = np.divide(m, r, out=np.zeros_like(m), where=r > 0)
        energy = np.trapz(material.specific_energy(rho, K, self.params) - potential, m)
        self.assertAlmostEqual(float(energy), result["total_energy"], delta=2e-5)
        self.assertTrue(np.all(np.diff(K) >= -1e-13))
        self.assertGreaterEqual(result["minimum_active_gamma1"], 2 - 1e-10)
        self.assertGreaterEqual(result["minimum_buoyancy_squared"], -1e-10)

    def test_energy_obstruction_is_reported_without_forcing_an_endpoint(self):
        profile = endpoint.EntropyProfile(np.full(8, 0.2), 1.0)
        base = endpoint.solve_equilibrium(profile, self.params)
        result = endpoint.construct_endpoint(profile, self.params,
                                             target_energy=base["total_energy"] - 0.1)
        self.assertEqual(result["status"], "energetic_obstruction")
        self.assertIsNone(result["endpoint"])

    def test_common_entropy_increase_can_match_an_admissible_energy(self):
        profile = endpoint.EntropyProfile(np.full(8, 0.2), 1.0)
        base = endpoint.solve_equilibrium(profile, self.params)
        target = base["total_energy"] + 0.1
        result = endpoint.construct_endpoint(profile, self.params, target_energy=target)
        self.assertEqual(result["status"], "constructed_endpoint")
        self.assertGreater(result["alpha"], 1)
        self.assertLess(result["relative_energy_error"], 2e-6)
        self.assertLess(result["endpoint"]["relative_mass_error"], 1e-6)
        self.assertTrue(np.all(np.array(result["endpoint"]["parcel_K"]) >= profile.sorted_K))

    def test_zero_or_negative_entropy_is_rejected_without_a_hidden_floor(self):
        for K in [[0.1, 0], [0.1, -0.1], [np.nan, 0.2]]:
            with self.assertRaises(ValueError):
                endpoint.EntropyProfile(K, 1.0)

    def test_exact_parcel_mode_never_reduces_any_sorted_parcel_coefficient(self):
        profile = endpoint.EntropyProfile([8.0, 1.0], 2.0)
        masses = np.array([0, 0.25, 0.999999, 1, 1.000001, 2])
        np.testing.assert_array_equal(profile.parcel_coefficient(masses, alpha=1.4),
                                      1.4 * np.array([1, 1, 1, 8, 8, 8]))
        for i in range(2):
            points = i + np.linspace(1e-9, 1 - 1e-9, 51)
            self.assertTrue(np.all(profile.parcel_coefficient(points, alpha=1.4) >= profile.sorted_K[i]))

    def test_exact_parcel_constant_K_matches_independent_enthalpy_solution(self):
        K = 0.3
        reference = equilibria.solve_equilibrium(5.0, rtol=2e-10, max_step=0.02)
        length = np.sqrt(K / (4 * np.pi))
        mass = 4 * np.pi * length**3 * reference.mass
        profile = endpoint.EntropyProfile(np.full(8, K), mass)
        result = endpoint.solve_equilibrium(profile, self.params, rtol=2e-8, mode="exact_parcels")
        self.assertEqual(result["integration_method"], "RK45")
        self.assertAlmostEqual(result["central_density"], 5, places=4)
        self.assertAlmostEqual(result["radius"], length * reference.radius, places=5)
        self.assertTrue(result["mass_residual_accepted"])

    def test_exact_parcel_contacts_preserve_pressure_and_stabilizing_density_order(self):
        profile = endpoint.EntropyProfile([0.05, 0.1, 0.2, 0.3], 1.0)
        result = endpoint.solve_equilibrium(profile, self.params, alpha=1.2,
                                            rtol=2e-8, mode="exact_parcels")
        self.assertEqual(len(result["contacts"]), 3)
        for contact in result["contacts"]:
            self.assertGreaterEqual(contact["K_outer"], contact["K_inner"])
            self.assertLessEqual(contact["rho_outer"], contact["rho_inner"])
            for side in ["inner", "outer"]:
                pressure = float(material.pressure(contact["rho_" + side], contact["K_" + side], self.params))
                self.assertAlmostEqual(pressure, contact["pressure"], delta=2e-8)
        np.testing.assert_array_equal(result["parcel_K"], 1.2 * profile.sorted_K)

    def test_exact_endpoint_checks_energy_mass_and_every_parcel_entropy(self):
        profile = endpoint.EntropyProfile([0.1, 0.2, 0.3, 0.4], 1.0)
        base = endpoint.solve_equilibrium(profile, self.params, mode="exact_parcels", rtol=2e-8)
        run = endpoint.construct_endpoint(profile, self.params, target_energy=base["total_energy"] + 0.1,
                                           mode="exact_parcels", rtol=2e-8)
        self.assertEqual(run["status"], "constructed_endpoint")
        self.assertTrue(run["energy_residual_accepted"])
        self.assertTrue(run["endpoint"]["mass_residual_accepted"])
        self.assertGreaterEqual(run["entropy_integrals"]["minimum_parcel_K_ratio"], 1)
        source_entropy = float(np.mean(np.cbrt(profile.sorted_K / self.params.k_star)))
        self.assertAlmostEqual(run["entropy_integrals"]["sorted_sigma_mass_integral"], source_entropy)
        self.assertAlmostEqual(run["entropy_integrals"]["endpoint_sigma_mass_integral"],
                               source_entropy * run["alpha"]**(1 / 3))

    def test_plummer_loading_preserves_mass_and_the_same_entropy_function(self):
        profile = endpoint.EntropyProfile([0.05, 0.1, 0.2, 0.3], 1.0)
        base = endpoint.solve_equilibrium(profile, self.params, alpha=1.2)
        comparison = endpoint.compare_plummer_loading(profile, self.params, base, rtol=2e-7)
        loaded = comparison["loaded_equilibrium"]
        self.assertLess(loaded["relative_mass_error"], 2e-6)
        self.assertGreater(loaded["central_density"], base["central_density"])
        self.assertLess(loaded["half_mass_radius"], base["half_mass_radius"])
        np.testing.assert_allclose(
            loaded["profile"]["K"],
            1.2 * np.interp(loaded["profile"]["m"], [0.125, 0.375, 0.625, 0.875], [0.05, 0.1, 0.2, 0.3]),
            rtol=1e-14,
        )
        self.assertGreaterEqual(loaded["minimum_buoyancy_squared"], -1e-10)
        for row in comparison["comparisons"]:
            independent = equilibria.dust_shell_radius(row["initial_radius"], row["mass_fraction"],
                                                       0.3, 0.1 * base["radius"])
            self.assertAlmostEqual(row["circular_reference_radius"], independent, places=10)


if __name__ == "__main__":
    unittest.main()
