#!/usr/bin/env python3
"""Independent numerical checks of the exterior HPI-Delta orbit law."""

from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
import math
from pathlib import Path
import unittest

import sympy as sp


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "hpi_delta_orbit_numeric_2026.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("hpi_delta_orbit_numeric_2026", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AnalyticOrbitLawTests(unittest.TestCase):
    def test_symbolic_derivation_closes_from_flux_slope_to_epicycle(self) -> None:
        """Catches printing a target formula without deriving its residual."""

        module = _load_module()
        derivation = module.derive_symbolic_orbit_law()
        self.assertEqual(derivation["log_mu_slope_residual"], 0)
        self.assertEqual(derivation["mass_slope_equation_residual"], 0)
        self.assertEqual(derivation["general_closed_form_residual"], 0)
        self.assertEqual(derivation["exterior_closed_form_residual"], 0)
        self.assertEqual(derivation["deep_exterior_ratio"], 2)
        self.assertEqual(derivation["newtonian_exterior_ratio"], 1)
        self.assertEqual(
            sp.simplify(
                derivation["deep_precession"]
                - sp.pi * (sp.sqrt(2) - 2)
            ),
            0,
        )

    def test_exponential_kernel_and_exterior_ratio_match_hand_values(self) -> None:
        """Catches a wrong exponential sign or a swapped epicyclic ratio."""

        module = _load_module()
        self.assertAlmostEqual(module.mu_exponential(1.0), 0.6321205588285577, 15)
        self.assertAlmostEqual(
            module.analytic_kappa_over_omega(1.0),
            1.3174820235368998,
            14,
        )
        self.assertAlmostEqual(
            module.analytic_kappa_over_omega(10.0),
            1.000453710942755,
            14,
        )

    def test_extended_mass_term_is_not_silently_dropped(self) -> None:
        """Catches applying the constant-mass exterior law inside matter."""

        module = _load_module()
        self.assertAlmostEqual(
            module.analytic_kappa2_over_omega2(1.0, mass_log_slope=1.0),
            2.3678794411714423,
            14,
        )
        self.assertAlmostEqual(
            module.analytic_kappa2_over_omega2(0.37, mass_log_slope=2.0),
            3.0,
            14,
        )


class ExteriorForceTests(unittest.TestCase):
    def test_implicit_force_is_solved_not_replaced_by_an_asymptote(self) -> None:
        """Catches using either g=g_N or g=sqrt(a0*g_N) at y=1."""

        module = _load_module()
        radius = 1.2577665549971213
        acceleration = module.solve_exterior_acceleration(radius, gm=1.0, a0=1.0)
        self.assertAlmostEqual(acceleration, 1.0, 13)
        self.assertLess(
            abs(
                acceleration * (1.0 - math.exp(-acceleration))
                - 1.0 / radius**2
            ),
            2.0e-14,
        )

    def test_circular_reference_orbit_is_fixed_by_target_y(self) -> None:
        """Catches losing a factor of r in Omega^2=g/r."""

        module = _load_module()
        orbit = module.circular_orbit_from_y(1.0, gm=1.0, a0=1.0)
        self.assertAlmostEqual(orbit["radius"], 1.2577665549971213, 14)
        self.assertAlmostEqual(orbit["acceleration"], 1.0, 14)
        self.assertAlmostEqual(orbit["omega"] ** 2, 1.0 / orbit["radius"], 14)
        self.assertAlmostEqual(
            orbit["angular_momentum"] ** 2,
            orbit["radius"] ** 3,
            13,
        )

    def test_zero_field_endpoint_is_explicitly_outside_numeric_audit(self) -> None:
        """Catches silently dividing by mu(0) in a claimed endpoint check."""

        module = _load_module()
        with self.assertRaises(ValueError):
            module.circular_orbit_from_y(0.0)


class NonlinearOrbitIntegrationTests(unittest.TestCase):
    def test_event_measured_frequency_ratio_matches_independent_literals(self) -> None:
        """Catches returning the analytic ratio instead of measuring orbit events."""

        module = _load_module()
        cases = (
            (0.1, 1.4052747141704525),
            (1.0, 1.3174820235368998),
            (10.0, 1.000453710942755),
        )
        for y, expected in cases:
            with self.subTest(y=y):
                result = module.integrate_near_circular_orbit(
                    y,
                    epsilon=1.0e-4,
                    requested_radial_cycles=5,
                    method="DOP853",
                    rtol=2.0e-11,
                    atol=2.0e-13,
                )
                self.assertGreaterEqual(result["measured_cycles"], 4)
                self.assertAlmostEqual(
                    result["measured_kappa_over_omega"], expected, delta=2.0e-7
                )
                self.assertLess(result["max_force_residual"], 3.0e-13)

    def test_measured_apsidal_shift_uses_pericenter_to_pericenter_convention(self) -> None:
        """Catches a degree/radian error or the inverse Omega/kappa convention."""

        module = _load_module()
        result = module.integrate_near_circular_orbit(
            1.0,
            epsilon=1.0e-4,
            requested_radial_cycles=5,
        )
        self.assertAlmostEqual(
            result["measured_precession_degrees"],
            -86.751489911,
            delta=2.0e-5,
        )
        self.assertLess(result["mean_azimuth_per_radial_cycle"], 2.0 * math.pi)


class NumericalAuditTests(unittest.TestCase):
    def test_near_circular_error_converges_quadratically_with_eccentricity(self) -> None:
        """Catches returning a copied analytic value instead of a nonlinear limit."""

        module = _load_module()
        audit = module.run_epsilon_convergence(
            1.0,
            epsilons=(1.0e-2, 1.0e-3, 1.0e-4),
            requested_radial_cycles=5,
        )
        errors = [item["absolute_relative_frequency_error"] for item in audit]
        self.assertGreater(errors[0], 50.0 * errors[1])
        self.assertGreater(errors[1], 50.0 * errors[2])
        self.assertLess(errors[2], 2.0e-8)

    def test_two_integrators_find_the_same_event_frequency(self) -> None:
        """Catches a DOP853-specific or loose-tolerance numerical artifact."""

        module = _load_module()
        comparison = module.compare_integrators(
            1.0,
            epsilon=1.0e-3,
            requested_radial_cycles=5,
            methods=("DOP853", "RK45"),
        )
        self.assertLess(comparison["fractional_disagreement"], 2.0e-8)
        self.assertAlmostEqual(
            comparison["measurements"]["DOP853"],
            1.3174821296,
            delta=3.0e-8,
        )

    def test_no_constitutive_slope_mutation_is_rejected_by_orbit_events(self) -> None:
        """Catches a dead numerical audit that cannot reject kappa=Omega."""

        module = _load_module()
        mutation = module.run_no_constitutive_slope_mutation(
            0.1,
            epsilon=1.0e-4,
            requested_radial_cycles=5,
        )
        self.assertLess(mutation["correct_relative_error"], 2.0e-7)
        self.assertGreater(mutation["mutated_relative_error"], 0.2)
        self.assertFalse(mutation["mutation_survives"])


class FullAuditTests(unittest.TestCase):
    def test_certificate_is_bounded_and_assembled_from_numeric_checks(self) -> None:
        """Catches promoting a finite orbit audit to novelty or theory closure."""

        module = _load_module()
        audit = module.run_full_audit()
        self.assertTrue(audit["passed"])
        self.assertTrue(all(audit["checks"].values()))
        self.assertEqual(len(audit["grid"]), 5)
        self.assertLess(audit["max_grid_relative_error"], 2.0e-7)
        self.assertFalse(audit["scope"]["proves_novelty"])
        self.assertFalse(audit["scope"]["proves_full_relativistic_theory"])
        self.assertTrue(audit["scope"]["exterior_constant_mass_only"])
        self.assertFalse(audit["scope"]["includes_exact_y_zero"])

    def test_command_line_report_exposes_machine_readable_bounded_verdict(self) -> None:
        """Catches a script that passes internally but emits no auditable result."""

        module = _load_module()
        stream = io.StringIO()
        with redirect_stdout(stream):
            exit_code = module.main()
        output = stream.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("PASS (BOUNDED NUMERICAL VALIDATION)", output)
        certificate_line = next(
            line for line in output.splitlines() if line.startswith("CERTIFICATE_JSON: ")
        )
        certificate = json.loads(certificate_line.removeprefix("CERTIFICATE_JSON: "))
        self.assertEqual(certificate["status"], "PASS_BOUNDED")
        self.assertEqual(certificate["grid_points"], 5)
        self.assertFalse(certificate["proves_novelty"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
