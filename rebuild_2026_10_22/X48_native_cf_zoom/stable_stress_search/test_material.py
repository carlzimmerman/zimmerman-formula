"""Independent constitutive identities and domain checks; run with unittest."""

import unittest

import numpy as np

import material


class MaterialTests(unittest.TestCase):
    def setUp(self):
        self.params = material.MaterialParameters(rho_q=2.0, a0=4.0, G=0.5, tau=0.25)

    def test_gate_and_density_weight_have_the_declared_branches(self):
        # Catches an incorrect transition or an omitted dormant energy offset.
        d = np.array([0.1, 1.0, 1.5, 2.0, 3.0])
        np.testing.assert_allclose(material.activation(d), [0, 0, 0.5, 1, 1])
        np.testing.assert_allclose(material.activation_derivative(d), [0, 0, 1.5, 0, 0])
        np.testing.assert_allclose(
            material.density_weight(2 * d, self.params), [3, 3, 3.1875, 4, 6]
        )

    def test_stress_scale_uses_rho_q_rather_than_latent_density(self):
        # The inputs give P0=4/pi and Kstar=1/pi independently of W's offset.
        self.assertAlmostEqual(self.params.p0, 4 / np.pi)
        self.assertAlmostEqual(self.params.k_star, 1 / np.pi)

    def test_pressure_is_the_energy_derivative_at_fixed_memory(self):
        # Catches a force-law pressure substituted for the thermodynamic one.
        rho = np.array([0.4, 1.8, 2.3, 3.0, 3.7, 4.2, 10.0])
        k = np.array([0.0, 0.2, 0.5, 1.0, 2.0, 0.3, 0.8])
        step = 1e-5 * rho
        de_drho = (
            material.specific_energy(rho + step, k, self.params)
            - material.specific_energy(rho - step, k, self.params)
        ) / (2 * step)
        np.testing.assert_allclose(
            material.pressure(rho, k, self.params), rho**2 * de_drho,
            rtol=2e-8, atol=2e-9,
        )

    def test_sound_speed_is_the_pressure_derivative_at_fixed_memory(self):
        # Catches omission of the activation-gradient stiffness in the ramp.
        rho = np.array([0.4, 1.8, 2.3, 3.0, 3.7, 4.2, 10.0])
        k = 0.7
        step = 1e-5 * rho
        dp_drho = (
            material.pressure(rho + step, k, self.params)
            - material.pressure(rho - step, k, self.params)
        ) / (2 * step)
        np.testing.assert_allclose(
            material.sound_speed_squared(rho, k, self.params), dp_drho,
            rtol=2e-8, atol=2e-9,
        )

    def test_high_density_branch_is_exact_gamma_two(self):
        rho = np.array([4.0, 5.0, 20.0])
        k = np.array([0.2, 0.5, 0.8])
        np.testing.assert_array_equal(material.specific_energy(rho, k, self.params), k * rho)
        np.testing.assert_array_equal(material.pressure(rho, k, self.params), k * rho**2)
        np.testing.assert_array_equal(material.sound_speed_squared(rho, k, self.params), 2 * k * rho)

    def test_low_density_is_exactly_quiet_with_arbitrary_memory(self):
        rho = np.array([[0.1], [1.0], [1.999]])
        k = np.array([0.0, 1.0, 1e6])
        np.testing.assert_array_equal(material.pressure(rho, k, self.params), np.zeros((3, 3)))
        np.testing.assert_array_equal(material.sound_speed_squared(rho, k, self.params), np.zeros((3, 3)))
        q, dk = material.bulk_viscosity_source(rho, -1e4, self.params)
        np.testing.assert_array_equal(q, np.zeros((3, 1)))
        np.testing.assert_array_equal(dk, np.zeros((3, 1)))
        np.testing.assert_array_equal(
            material.specific_energy(rho, k, self.params), np.broadcast_to(3 * k, (3, 3))
        )

    def test_cold_memory_and_slow_compression_remain_unheated(self):
        rho = np.array([1.0, 3.0, 8.0])
        for theta in [2.0, 0.0, -3.0, -4.0]:
            q, dk = material.bulk_viscosity_source(rho, theta, self.params)
            np.testing.assert_array_equal(q, np.zeros(3))
            np.testing.assert_array_equal(dk, np.zeros(3))
        np.testing.assert_array_equal(material.pressure(rho, 0.0, self.params), np.zeros(3))

    def test_compression_converts_mechanical_work_into_memory_energy(self):
        # Independently differentiates e along continuity plus the memory source.
        rho = np.array([1.0, 2.4, 3.0, 4.5, 12.0])
        k = np.array([0.0, 0.2, 1.0, 0.0, 0.5])
        theta = -np.array([8.0, 5.0, 10.0, 6.0, 12.0])
        q, dk = material.bulk_viscosity_source(rho, theta, self.params)
        compression = -theta
        np.testing.assert_allclose(
            q * compression,
            rho * material.density_weight(rho, self.params) * dk,
            rtol=2e-15, atol=0,
        )
        dt = 1e-7
        rho_dot = -rho * theta
        # A forward directional derivative also covers parcels beginning at K=0.
        e_dot = (
            material.specific_energy(rho + dt * rho_dot, k + dt * dk, self.params)
            - material.specific_energy(rho, k, self.params)
        ) / dt
        np.testing.assert_allclose(
            rho * e_dot, -(material.pressure(rho, k, self.params) + q) * theta,
            rtol=4e-6, atol=2e-8,
        )

    def test_bulk_source_has_nonnegative_dissipation_and_exact_threshold(self):
        rho = np.array([[1.0], [2.5], [4.0], [8.0]])
        theta = np.array([1.0, 0.0, -3.999, -4.0, -4.001, -12.0])
        q, dk = material.bulk_viscosity_source(rho, theta, self.params)
        self.assertEqual(q.shape, (4, 6))
        self.assertTrue(np.all(q >= 0))
        self.assertTrue(np.all(dk >= 0))
        np.testing.assert_array_equal(q[:, :4], np.zeros((4, 4)))
        self.assertTrue(np.all(q[1:, 4:] > 0))
        self.assertTrue(np.all(q * np.maximum(-theta, 0) >= 0))

    def test_dimensionless_enthalpy_matches_pressure_integral(self):
        # Checks dH/dd=(1/d)d(P/(K*rho_q**2))/dd independently by quadrature.
        targets = [0.5, 1.0, 1.5, 2.0, 4.0]
        np.testing.assert_allclose(
            material.dimensionless_enthalpy(targets), [0.0, 0.0, 0.84375, 2.5, 6.5]
        )
        for upper in [1.2, 1.8, 2.0, 3.0]:
            d = np.linspace(1.0, upper, 12001)
            rho = self.params.rho_q * d
            integral = np.trapz(
                material.sound_speed_squared(rho, 1.0, self.params) / d,
                d,
            ) / self.params.rho_q
            self.assertAlmostEqual(float(material.dimensionless_enthalpy(upper)), float(integral), places=7)

    def test_entropy_energy_hessian_is_positive_semidefinite(self):
        # A removed latent offset makes the mixed entropy-volume Hessian fail.
        for sigma, v in [(0.3, 1.0), (0.5, 1 / 2.3), (1.0, 1 / 3), (2.0, 1 / 6)]:
            ds, dv = sigma * 1e-4, v * 1e-4

            def e(s, volume):
                return float(material.specific_energy(1 / volume, self.params.k_star * s**3, self.params))

            center = e(sigma, v)
            hss = (e(sigma + ds, v) - 2 * center + e(sigma - ds, v)) / ds**2
            hvv = (e(sigma, v + dv) - 2 * center + e(sigma, v - dv)) / dv**2
            hsv = (
                e(sigma + ds, v + dv) - e(sigma + ds, v - dv)
                - e(sigma - ds, v + dv) + e(sigma - ds, v - dv)
            ) / (4 * ds * dv)
            eig = np.linalg.eigvalsh([[hss, hsv], [hsv, hvv]])
            self.assertGreaterEqual(float(eig[0]), -1e-6 * max(1.0, float(eig[-1])))

    def test_invalid_parameters_are_rejected(self):
        for field in ["rho_q", "a0", "G", "tau"]:
            for bad in [0, -1, np.inf, np.nan]:
                args = dict(rho_q=2.0, a0=4.0, G=0.5, tau=0.25)
                args[field] = bad
                with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                    material.MaterialParameters(**args)

    def test_invalid_density_memory_or_divergence_is_rejected(self):
        for bad in [0, -1, np.inf, np.nan]:
            with self.subTest(rho=bad), self.assertRaises(ValueError):
                material.pressure(bad, 1.0, self.params)
        for bad in [-1, np.inf, np.nan]:
            with self.subTest(k=bad), self.assertRaises(ValueError):
                material.specific_energy(3.0, bad, self.params)
        for bad in [np.inf, np.nan]:
            with self.subTest(theta=bad), self.assertRaises(ValueError):
                material.bulk_viscosity_source(3.0, bad, self.params)
        for bad in [0, -1, np.inf, np.nan]:
            with self.subTest(d=bad), self.assertRaises(ValueError):
                material.activation(bad)


if __name__ == "__main__":
    unittest.main()
