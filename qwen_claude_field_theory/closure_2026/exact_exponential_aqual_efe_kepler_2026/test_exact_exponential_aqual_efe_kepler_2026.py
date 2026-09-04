#!/usr/bin/env python3
"""Regression tests for the external-field AQUAL clock laws.

Every numerical target below is a hand-evaluated closed-form value, an
independently integrated Newtonian-ellipsoid coefficient, or an independently
integrated trajectory target.  The tests do not call the production formula
to manufacture their expected answers.
"""

import hashlib
import math
import json
import unittest
from pathlib import Path

from scipy.integrate import quad

from exact_exponential_aqual_efe_kepler_2026 import (
    action_primitive,
    build_certificate,
    core_clock_laws,
    depolarization_factors,
    external_field_parameters,
    point_mass_clock_laws,
    secular_node_law,
)
from independent_orbit_audit import measure_frequency_ratio, measure_node_advance, run_independent_audit
from symbolic_action_audit import run_symbolic_audit


class ExactExponentialAqualEfeKeplerTests(unittest.TestCase):
    def test_action_primitive_has_exact_exponential_constitutive_derivative(self):
        # G(1)=4/e-1 and G'(1)/2=1-1/e.
        self.assertAlmostEqual(action_primitive(1.0), 0.4715177646857693, places=14)
        h = 1.0e-6
        derivative = (action_primitive(1.0 + h) - action_primitive(1.0 - h)) / (2.0 * h)
        self.assertAlmostEqual(derivative / 2.0, 0.6321205588285577, places=9)

    def test_external_field_parameters_use_logarithmic_derivative_not_mu_prime(self):
        pars = external_field_parameters(1.0)
        self.assertAlmostEqual(pars.mu, 0.6321205588285577, places=15)
        self.assertAlmostEqual(pars.L, 0.5819767068693265, places=15)
        self.assertAlmostEqual(pars.q, 1.5819767068693265, places=15)

    def test_zero_field_limit_is_explicit_and_negative_eta_is_rejected(self):
        pars = external_field_parameters(0.0)
        self.assertEqual(pars.mu, 0.0)
        self.assertEqual(pars.L, 1.0)
        self.assertEqual(pars.q, 2.0)
        self.assertIsNone(point_mass_clock_laws(0.0).azimuthal_frequency_squared_coefficient)
        with self.assertRaises(ValueError):
            external_field_parameters(-1.0e-4)

    def test_zero_field_certificate_is_strict_json_not_nan_or_infinity(self):
        certificate = build_certificate([0.0])
        json.dumps(certificate, allow_nan=False)
        self.assertEqual(certificate["status"], "PASS_NONRELATIVISTIC_EFD_CALCULATION")
        self.assertTrue(certificate["checks"]["zero_field_degenerate_0"])
        self.assertNotIn("elliptic_0", certificate["checks"])

    def test_point_mass_nodal_clock_distinguishes_two_unambiguous_conventions(self):
        law = point_mass_clock_laws(2.47813)
        self.assertAlmostEqual(law.kepler_coefficient, 1.0147463885450525, places=14)
        self.assertAlmostEqual(law.vertical_to_azimuthal_frequency, 0.9027871775698558, places=14)
        self.assertAlmostEqual(law.node_shift_per_azimuth_period, 0.61080617756254, places=14)
        self.assertAlmostEqual(law.node_shift_per_vertical_period, 0.6765782597917736, places=14)

    def test_point_mass_deep_limit_gives_exact_sqrt_two_clock_split(self):
        law = point_mass_clock_laws(0.0)
        self.assertAlmostEqual(law.vertical_to_azimuthal_frequency, 1.0 / math.sqrt(2.0), places=15)
        self.assertAlmostEqual(
            law.node_shift_per_azimuth_period,
            2.0 * math.pi * (1.0 - 1.0 / math.sqrt(2.0)),
            places=15,
        )
        self.assertAlmostEqual(
            law.node_shift_per_vertical_period,
            2.0 * math.pi * (math.sqrt(2.0) - 1.0),
            places=15,
        )

    def test_closed_depolarization_factors_match_independent_integrals(self):
        # Physical sphere -> oblate ellipsoid (1,1,1/sqrt(q)) after z'=z/sqrt(q).
        q = 2.0
        c = 1.0 / math.sqrt(q)
        prefactor = c / 2.0
        n_perp_integral = quad(
            lambda s: prefactor / ((s + 1.0) ** 2 * math.sqrt(s + c * c)),
            0.0,
            math.inf,
            epsabs=2.0e-13,
        )[0]
        n_parallel_integral = quad(
            lambda s: prefactor / ((s + c * c) * (s + 1.0) * math.sqrt(s + c * c)),
            0.0,
            math.inf,
            epsabs=2.0e-13,
        )[0]
        factors = depolarization_factors(q)
        self.assertAlmostEqual(factors.perpendicular, n_perp_integral, places=12)
        self.assertAlmostEqual(factors.parallel, n_parallel_integral, places=12)
        self.assertAlmostEqual(2.0 * factors.perpendicular + factors.parallel, 1.0, places=14)

    def test_uniform_core_deep_clock_law_rejects_old_local_operator_shortcut(self):
        law = core_clock_laws(0.0)
        self.assertAlmostEqual(law.parallel_to_perpendicular_frequency_squared, 0.7519383938841087, places=15)
        self.assertAlmostEqual(law.parallel_to_perpendicular_period, 1.1532112482813996, places=15)
        # The old shortcut used 1/q=1/2; boundary matching changes the answer by O(1).
        self.assertGreater(abs(law.parallel_to_perpendicular_frequency_squared - 0.5), 0.25)

    def test_uniform_core_coefficients_obey_the_rescaled_poisson_trace(self):
        law = core_clock_laws(0.7)
        # Coefficients are normalized by 4*pi*G*rho/mu_e.
        self.assertAlmostEqual(
            2.0 * law.perpendicular_frequency_squared_coefficient
            + law.q * law.parallel_frequency_squared_coefficient,
            1.0,
            places=14,
        )

    def test_newtonian_limit_is_isotropic_for_both_sources(self):
        point = point_mass_clock_laws(50.0)
        core = core_clock_laws(50.0)
        self.assertAlmostEqual(point.vertical_to_azimuthal_frequency, 1.0, places=15)
        self.assertAlmostEqual(core.parallel_to_perpendicular_period, 1.0, places=14)

    def test_direct_3d_orbit_recovers_the_nodal_frequency_split(self):
        # This integrates the force rather than differentiating the production
        # frequency formula.  A swapped q, missing anisotropy, or wrong axis fails.
        measured = measure_frequency_ratio(eta=1.0, cycles=14, amplitude=2.0e-5)
        self.assertAlmostEqual(measured.measured_ratio, 0.7950600976206501, delta=2.0e-5)
        self.assertLess(measured.relative_error, 2.5e-5)

    def test_finite_e_secular_node_law_keeps_full_geometry_at_first_order(self):
        law = secular_node_law(
            eta=6.0,
            eccentricity=0.3,
            inclination=math.radians(20.0),
            argument_of_periapsis=math.radians(40.0),
        )
        self.assertAlmostEqual(math.degrees(law.node_shift_per_orbit), 2.59412624936494, places=12)
        self.assertGreater(law.geometry_bracket, 0.0)
        polar = secular_node_law(6.0, 0.3, math.pi / 2.0, math.radians(40.0))
        retrograde = secular_node_law(6.0, 0.3, math.radians(160.0), math.radians(40.0))
        self.assertAlmostEqual(polar.node_shift_per_orbit, 0.0, places=15)
        self.assertLess(retrograde.node_shift_per_orbit, 0.0)

    def test_unexpanded_3d_orbit_calibrates_first_periapsis_step_difference(self):
        audit = measure_node_advance(
            eta=6.0,
            eccentricity=0.3,
            inclination=math.radians(20.0),
            argument_of_periapsis=math.radians(40.0),
        )
        self.assertAlmostEqual(
            math.degrees(audit.first_periapsis_node_shift), 2.6037179649481, delta=2.0e-7
        )
        self.assertAlmostEqual(audit.first_step_relative_difference, 0.0036974744716, delta=2.0e-8)

    def test_orbit_certificate_includes_solver_convergence(self):
        audit = run_independent_audit()
        self.assertEqual(audit["status"], "PASS_NONRELATIVISTIC_EFD_ORBIT_AUDIT")
        self.assertTrue(audit["checks"]["node_step_size_convergence"])

    def test_symbolic_variation_and_orbit_average_are_live_computations(self):
        audit = run_symbolic_audit()
        self.assertTrue(audit["checks"]["constitutive_identity"])
        self.assertTrue(audit["checks"]["flux_hessian_eigenvalues"])
        self.assertTrue(audit["checks"]["eccentric_anomaly_average"])
        self.assertTrue(audit["checks"]["geometry_alpha_physical_range"])
        self.assertTrue(audit["checks"]["geometry_bracket_lower_bound"])
        self.assertTrue(audit["checks"]["geometry_bracket_positive"])

    def test_recorded_certificates_equal_fresh_computations(self):
        directory = Path(__file__).resolve().parent
        recorded_calculation = json.loads((directory / "calculation_results.json").read_text())
        recorded_orbit = json.loads((directory / "orbit_audit_results.json").read_text())
        recorded_symbolic = json.loads((directory / "symbolic_action_results.json").read_text())
        self.assertEqual(recorded_calculation, build_certificate([0.0, 0.1, 1.0, 2.47813, 10.0, 50.0]))
        self.assertEqual(recorded_orbit, run_independent_audit())
        self.assertEqual(recorded_symbolic, run_symbolic_audit())

    def test_manifest_hashes_pin_sources_and_outputs(self):
        directory = Path(__file__).resolve().parent
        repository = directory.parents[2]
        manifest = json.loads((directory / "computation_manifest.json").read_text())
        for record in manifest["sources"] + manifest["outputs"]:
            payload = (repository / record["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), record["sha256"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
