"""Independent hand-derived geometry benchmarks and negative branch controls."""

import importlib.util
from pathlib import Path
import unittest

import sympy as sp


MODULE_PATH = Path(__file__).with_name("metric_branch_checks.py")
checks = None
if MODULE_PATH.exists():
    spec = importlib.util.spec_from_file_location("metric_branch_checks", MODULE_PATH)
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)


class MetricBranchTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(checks, "metric derivation is not implemented")

    def zero(self, expression):
        self.assertEqual(sp.simplify(expression), 0)

    def test_independent_potentials_have_distinct_density_and_slip_equations(self):
        # Catches a flipped Ricci sign, missing factor 2, or premature Phi=Psi.
        data = checks.static_geometry()
        r, phi, psi = data["r"], data["Phi"], data["Psi"]
        self.zero(data["G00"] - 2 * (sp.diff(psi, r, 2) + 2 * sp.diff(psi, r) / r))
        self.zero(data["Grr"] - 2 * sp.diff(phi - psi, r) / r)
        self.zero(data["Gtheta_over_r2"] - sp.diff(phi - psi, r, 2) - sp.diff(phi - psi, r) / r)
        self.zero(data["R00"] - sp.diff(phi, r, 2) - 2 * sp.diff(phi, r) / r)

    def test_schwarzschild_de_sitter_is_an_exact_einstein_metric(self):
        # Catches incorrect quadratic Christoffel contractions missed by a
        # linearized-flat benchmark; Lambda also fixes the curvature sign.
        t, r, theta, azimuth = sp.symbols("t r theta azimuth", real=True)
        mass, cosmological = sp.symbols("mass cosmological", real=True)
        lapse = 1 - 2 * mass / r - cosmological * r**2 / 3
        metric = sp.diag(-lapse, 1 / lapse, r**2, r**2 * sp.sin(theta)**2)
        ricci, scalar, einstein = checks.metric_curvature(metric, (t, r, theta, azimuth))
        for i in range(4):
            for j in range(4):
                self.zero(ricci[i, j] - cosmological * metric[i, j])
                self.zero(einstein[i, j] + cosmological * metric[i, j])
        self.zero(scalar - 4 * cosmological)

    def test_vacuum_integration_retains_constants_and_fixes_gamma(self):
        # Catches a discarded spatial integration constant or a claimed gamma
        # inserted independently of the integrated metric potentials.
        data = checks.static_exterior()
        r = data["r"]
        self.zero(data["Phi"] - data["C_phi"] + data["G_N"] * data["mass"] / r)
        self.zero(data["Psi"] - data["C_psi"] + data["G_N"] * data["mass"] / r)
        self.zero(data["G_N"] - data["kappa"] / (8 * sp.pi))
        self.zero(data["gamma"] - 1)
        for residual in data["vacuum_residuals"]:
            self.zero(residual)

    def test_exponential_mu_law_has_nonzero_exterior_ricci(self):
        # Catches use of the distinct explicit exponential-RAR interpolation,
        # or the false assumption that MOND obeys the GR vacuum equation.
        data = checks.mond_obstruction()
        y, r, a0 = data["y"], data["r"], data["a0"]
        self.zero(data["s"] - y * (1 - sp.exp(-y)))
        expected = 2 * a0 * y**2 / (r * (sp.exp(y) - 1 + y))
        self.zero(data["R00"] - expected)
        self.assertTrue(data["R00"].subs({y: 1, r: 1, a0: 1}).is_positive)
        self.zero(sp.limit(data["log_slope"], y, 0, dir="+") + 1)
        self.zero(sp.limit(data["log_slope"], y, sp.oo) + 2)

    def test_mond_and_nonconstant_lambda_fail_vacuum_acceptance(self):
        # Catches a vacuum gate that merely prints success or ignores the
        # proposed potential; exercises physical negative and positive cases.
        r = sp.symbols("r", positive=True)
        mass = sp.symbols("mass", positive=True)
        checks.assert_vacuum_potentials(-mass / r, -mass / r, r)
        with self.assertRaises(AssertionError):
            checks.assert_vacuum_potentials(sp.log(r), sp.log(r), r)
        with self.assertRaises(AssertionError):
            checks.assert_vacuum_potentials(-mass / r, -2 * mass / r, r)
        with self.assertRaises(AssertionError):
            checks.assert_zero(checks.mond_obstruction()["R00"], "MOND exterior")
        # A constant cosmological term cannot supply the varying MOND scalar.
        derivative = checks.mond_obstruction()["R00_derivative_along_branch"]
        self.assertNotEqual(sp.simplify(derivative), 0)

    def test_flrw_equations_come_from_curved_spatial_metric(self):
        # Catches lapse/sign/factor errors and omission of spatial curvature.
        data = checks.flrw_geometry()
        a, t, k = data["a"], data["t"], data["k"]
        h = sp.diff(a, t) / a
        self.zero(data["G00"] - 3 * (h**2 + k / a**2))
        self.zero(data["Gii_over_gii"] + 2 * sp.diff(a, t, 2) / a + h**2 + k / a**2)
        self.zero(data["rho_equation_lhs"] - 3 * (h**2 + k / a**2) + data["Lambda"])
        self.zero(data["p_equation_lhs"] + 2 * sp.diff(a, t, 2) / a + h**2 + k / a**2 - data["Lambda"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
