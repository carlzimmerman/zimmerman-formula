#!/usr/bin/env python3
"""Adversarial tests for the HPI-Delta weak-static prediction audit."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

import sympy as sp


SCRIPT = Path(__file__).with_name("hpi_delta_predictions_2026.py")


def _load_module():
    """Load the real audit module and fail as an assertion while it is absent."""

    if not SCRIPT.exists():
        raise AssertionError(f"missing prediction audit: {SCRIPT.name}")
    spec = importlib.util.spec_from_file_location("hpi_delta_predictions_2026", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HpiDeltaKernelTests(unittest.TestCase):
    def test_action_primitive_derives_exponential_mu_and_both_limits(self) -> None:
        """Catches a wrong primitive sign/coefficient or an inserted mu."""

        result = _load_module().derive_predictions()["kernel"]
        self.assertEqual(result["primitive_residual"], 0)
        self.assertEqual(result["mu_residual"], 0)
        self.assertEqual(result["newtonian_limit"], 1)
        self.assertEqual(result["deep_ratio"], 1)
        self.assertEqual(result["zero_field_mu"], 0)


class HpiDeltaActionVariationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = _load_module().derive_predictions()

    def test_phi_and_psi_equations_are_independent_euler_lagrange_variations(self) -> None:
        """Catches an assigned slip equation or a wrong EH/MOND variation sign."""

        self.assertIn("weak_static_action", self.result)
        action = self.result["weak_static_action"]
        radial = action["radial"]
        symbols = radial["symbols"]
        r = symbols["r"]
        a0 = symbols["a0"]
        G = symbols["G"]
        Phi = symbols["Phi"]
        Psi = symbols["Psi"]
        rho = symbols["rho"]
        g = sp.diff(Phi, r)
        expected_phi = (
            2 * sp.diff(r**2 * (sp.diff(Psi, r) - sp.exp(-g / a0) * g), r)
            - 8 * sp.pi * G * r**2 * rho
        )
        expected_psi = 2 * sp.diff(r**2 * (g - sp.diff(Psi, r)), r)

        self.assertEqual(sp.simplify(radial["E_phi"] - expected_phi), 0)
        self.assertEqual(sp.simplify(radial["E_psi"] - expected_psi), 0)
        self.assertNotEqual(radial["E_phi"], radial["E_psi"])
        self.assertEqual(action["phi_flux_residuals"], (0, 0, 0))
        self.assertEqual(action["psi_flux_residuals"], (0, 0, 0))

    def test_trace_constraint_preservation_generates_the_psi_equation_for_k_nonzero(self) -> None:
        """Catches insertion of Phi=Psi instead of preserving C_pi."""

        self.assertIn("trace_preservation", self.result)
        result = self.result["trace_preservation"]
        symbols = result["symbols"]
        A = symbols["A"]
        k = symbols["k"]
        Phi = symbols["Phi"]
        Psi = symbols["Psi"]
        p_Psi = symbols["p_Psi"]

        self.assertEqual(result["secondary_C_pi"], -k**2 * p_Psi)
        self.assertEqual(result["preservation_residual"], 0)
        self.assertEqual(
            sp.simplify(result["dot_C_pi"] - 2 * A * k**4 * (Phi - Psi)),
            0,
        )
        self.assertEqual(result["weak_E_psi_relation_residual"], 0)
        self.assertEqual(result["derived_Psi_solution"], Phi)
        self.assertTrue(result["requires_k_nonzero"])

    def test_planck_normalization_maps_physical_dust_source_to_measured_G(self) -> None:
        """Catches silently identifying the conditional dust coefficient with G."""

        self.assertIn("source_normalization", self.result)
        normalization = self.result["source_normalization"]
        self.assertEqual(normalization["matter_rescaling_residual"], 0)
        self.assertEqual(normalization["high_acceleration_poisson_residual"], 0)
        self.assertEqual(normalization["measured_G_residual"], 0)


class HpiDeltaSphericalAndOrbitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = _load_module().derive_predictions()

    def test_derived_no_slip_turns_phi_equation_into_exact_aqual(self) -> None:
        """Catches using Poisson or imposing the MOND equation independently."""

        self.assertIn("aqual", self.result)
        aqual = self.result["aqual"]
        symbols = aqual["symbols"]
        r = symbols["r"]
        a0 = symbols["a0"]
        G = symbols["G"]
        Phi = symbols["Phi"]
        rho = symbols["rho"]
        g = sp.diff(Phi, r)
        expected = (
            2 * sp.diff(r**2 * (1 - sp.exp(-g / a0)) * g, r)
            - 8 * sp.pi * G * r**2 * rho
        )

        self.assertEqual(aqual["derived_slip_residual"], 0)
        self.assertEqual(sp.simplify(aqual["E_phi_on_slip"] - expected), 0)
        self.assertEqual(aqual["aqual_residual"], 0)

    def test_spherical_flux_law_has_exact_newton_and_deep_mond_limits(self) -> None:
        """Catches a wrong radial measure, source normalization, or asymptotic power."""

        self.assertIn("spherical", self.result)
        spherical = self.result["spherical"]
        symbols = spherical["symbols"]
        r = symbols["r"]
        g = symbols["g"]
        a0 = symbols["a0"]
        G = symbols["G"]
        M = symbols["M"]

        expected_flux = r**2 * g * (1 - sp.exp(-g / a0)) - G * M
        self.assertEqual(sp.simplify(spherical["integrated_flux"] - expected_flux), 0)
        self.assertEqual(spherical["spherical_law_residual"], 0)
        self.assertEqual(spherical["mass_source"]["mass_definition_residual"], 0)
        self.assertEqual(spherical["mass_source"]["flux_derivative_residual"], 0)
        self.assertEqual(spherical["mass_source"]["exterior_projection_residual"], 0)
        self.assertEqual(spherical["newtonian_mu_limit"], 1)
        self.assertEqual(spherical["deep_flux_ratio"], 1)
        self.assertEqual(
            spherical["deep_acceleration"], sp.sqrt(G * M * a0) / r
        )

    def test_generalized_kepler_law_and_btfr_are_consequences_of_spherical_flux(self) -> None:
        """Catches insertion of Kepler/BTFR without the exact exponential factor."""

        self.assertIn("orbit", self.result)
        orbit = self.result["orbit"]
        symbols = orbit["symbols"]
        r = symbols["r"]
        T = symbols["T"]
        a0 = symbols["a0"]
        G = symbols["G"]
        M = symbols["M"]
        expected = (
            4
            * sp.pi**2
            * r**3
            / T**2
            * (1 - sp.exp(-4 * sp.pi**2 * r / (a0 * T**2)))
            - G * M
        )

        self.assertEqual(sp.simplify(orbit["generalized_kepler_residual"]), 0)
        self.assertEqual(sp.simplify(orbit["generalized_kepler_law"] - expected), 0)
        self.assertEqual(orbit["newtonian_kepler_residual"], 0)
        self.assertEqual(orbit["deep_period_residual"], 0)
        self.assertEqual(orbit["btfr_residual"], 0)

    def test_epicyclic_ratio_and_apsidal_precession_follow_from_same_mu(self) -> None:
        """Catches a missing constitutive derivative or inverted frequency ratio."""

        self.assertIn("epicycle", self.result)
        epicycle = self.result["epicycle"]
        y = epicycle["y"]
        L_expected = y / (sp.exp(y) - 1)
        ratio_expected = (1 + 3 * L_expected) / (1 + L_expected)
        precession_expected = 2 * sp.pi * (
            sp.sqrt((1 + L_expected) / (1 + 3 * L_expected)) - 1
        )

        self.assertEqual(sp.simplify(epicycle["L"] - L_expected), 0)
        self.assertEqual(epicycle["L_from_mu_residual"], 0)
        self.assertEqual(epicycle["log_slope_residual"], 0)
        self.assertEqual(sp.simplify(epicycle["kappa2_over_omega2"] - ratio_expected), 0)
        self.assertEqual(sp.simplify(epicycle["precession"] - precession_expected), 0)
        self.assertEqual(epicycle["newtonian_kappa2_over_omega2"], 1)
        self.assertEqual(epicycle["deep_kappa2_over_omega2"], 2)
        self.assertEqual(epicycle["newtonian_precession"], 0)
        self.assertEqual(
            sp.simplify(
                epicycle["deep_precession"]
                - 2 * sp.pi * (1 / sp.sqrt(2) - 1)
            ),
            0,
        )

    def test_extended_mass_epicycle_and_exterior_rotation_slope_are_derived(self) -> None:
        """Catches silently assuming constant mass or assigning the logarithmic slope."""

        epicycle = self.result["epicycle"]
        self.assertIn("mass_log_slope", epicycle)
        y = epicycle["y"]
        m = epicycle["mass_log_slope"]
        L = y / (sp.exp(y) - 1)
        general_slope = (m - 2) / (1 + L)
        general_ratio = (1 + 3 * L + m) / (1 + L)
        exterior_rotation_slope = (1 + y - sp.exp(y)) / (
            2 * (sp.exp(y) - 1 + y)
        )

        self.assertEqual(epicycle["differentiated_flux_residual"], 0)
        self.assertEqual(
            sp.simplify(epicycle["general_log_g_slope"] - general_slope), 0
        )
        self.assertEqual(
            sp.simplify(epicycle["general_kappa2_over_omega2"] - general_ratio),
            0,
        )
        self.assertEqual(
            sp.simplify(epicycle["exterior_log_g_slope"] + 2 / (1 + L)), 0
        )
        self.assertEqual(
            sp.simplify(epicycle["exterior_rotation_log_slope"] - exterior_rotation_slope),
            0,
        )
        self.assertEqual(epicycle["newtonian_rotation_log_slope"], -sp.Rational(1, 2))
        self.assertEqual(epicycle["deep_rotation_log_slope"], 0)


class HpiDeltaLensingAndMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = _load_module().derive_predictions()

    def test_null_geodesic_integral_has_full_newtonian_and_deep_mond_factors(self) -> None:
        """Catches losing Psi, a line-of-sight factor, or the impact-parameter factor."""

        self.assertIn("lensing", self.result)
        lensing = self.result["lensing"]
        symbols = lensing["symbols"]
        b = symbols["b"]
        a0 = symbols["a0"]
        G = symbols["G"]
        M = symbols["M"]
        c = symbols["c"]
        r_M = sp.sqrt(G * M / a0)

        self.assertEqual(lensing["gamma"], 1)
        self.assertEqual(lensing["metric_sum_factor"], 2)
        self.assertEqual(lensing["newtonian_single_potential_integral"], 2 * G * M / b)
        self.assertEqual(lensing["newtonian_deflection"], 4 * G * M / (b * c**2))
        self.assertEqual(
            lensing["deep_single_potential_integral"],
            sp.pi * sp.sqrt(G * M * a0),
        )
        self.assertEqual(
            lensing["deep_deflection"],
            2 * sp.pi * sp.sqrt(G * M * a0) / c**2,
        )
        self.assertEqual(lensing["no_slip_to_one_potential_factor"], 2)
        self.assertEqual(
            sp.simplify(
                lensing["deep_to_baryon_newtonian_ratio"]
                - sp.pi * b / (2 * r_M)
            ),
            0,
        )

    def test_mutations_change_the_physical_outputs_instead_of_self_reporting(self) -> None:
        """Catches dead controls and hard-coded MOND/slip/lensing/epicycle outputs."""

        self.assertIn("mutations", self.result)
        mutations = self.result["mutations"]
        y = self.result["kernel"]["y"]

        self.assertEqual(mutations["remove_F_exp"]["effective_mu"], 1)
        self.assertEqual(
            sp.simplify(
                mutations["remove_F_exp"]["mu_residual"] - sp.exp(-y)
            ),
            0,
        )
        self.assertEqual(mutations["wrong_EH_psi_coefficient"]["gamma"], sp.Rational(1, 2))
        self.assertEqual(
            mutations["wrong_EH_psi_coefficient"]["mond_modulus_residual"],
            -sp.Rational(1, 2),
        )
        self.assertEqual(mutations["drop_Psi_from_lensing"]["deep_factor"], 1)
        self.assertEqual(
            mutations["drop_Psi_from_lensing"]["relative_to_no_slip"],
            sp.Rational(1, 2),
        )
        self.assertEqual(
            mutations["ignore_constitutive_slope"]["deep_kappa2_over_omega2"],
            1,
        )
        self.assertNotEqual(
            mutations["ignore_constitutive_slope"]["deep_kappa2_over_omega2"],
            self.result["epicycle"]["deep_kappa2_over_omega2"],
        )

    def test_certificate_is_bounded_and_all_checks_depend_on_computed_outputs(self) -> None:
        """Catches promoting this prediction audit to PPN, closure, or novelty evidence."""

        module = _load_module()
        self.assertIn("scope", self.result)
        scope = self.result["scope"]
        self.assertTrue(scope["leading_weak_static_gamma_only"])
        self.assertTrue(scope["deep_scale_free_lensing_requires_cutoff"])
        self.assertTrue(scope["source_normalization_bridge_is_explicit"])
        self.assertTrue(scope["source_normalization_conditional_on_reduced_action"])
        self.assertFalse(scope["explicit_dust_action_varied"])
        self.assertFalse(scope["full_ppn_certified"])
        self.assertFalse(scope["full_nonlinear_dirac_certified"])
        self.assertFalse(scope["novelty_claimed"])
        self.assertEqual(scope["candidate_status"], "OPEN")

        checks = module.evaluate_checks(self.result)
        self.assertTrue(checks)
        self.assertTrue(all(checks.values()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
