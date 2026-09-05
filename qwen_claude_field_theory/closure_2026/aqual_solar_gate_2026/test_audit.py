"""Independent fixtures: reject monopole leakage, sign errors and false convergence."""
import importlib.util
import sys
import unittest
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "theory_2026"))
from aqual_solver_2026 import Grid, multipoles
audit = __import__("audit") if importlib.util.find_spec("audit") else None


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(audit, "the new bounded audit is not implemented yet")
        self.grid = Grid(1e-4, 1e4, 128, 32)

    def test_pure_monopole_has_zero_quadrupole(self):
        g = self.grid
        u = (-1 / g.r[:, None] + .001 / g.r[:, None]) * np.ones((1, g.nt))
        self.assertGreater(abs(2 * multipoles(g, u, 0)[2]), .01)
        self.assertLess(abs(audit.extract(g, u)["c2"]), 1e-7)

    def test_mixed_angular_modes_and_inner_boundary_tail(self):
        g = self.grid
        r, x = g.r[:, None], g.mu_c[None, :]
        p2 = (3*x*x-1)/2
        u = -1/r + .007/r + .17*r*r*p2 + 2e-12/r**3*p2 + .02*r*x
        self.assertAlmostEqual(audit.extract(g, u)["c2"], .17, places=7)

    def test_physical_quadrupole_sign_and_units(self):
        # Phi_2 = -Q2/3 * r^2 P2. a0=4, GM=16 -> a0/rM=2.
        self.assertAlmostEqual(audit.physical_Q2(-.2, 4, 16), 1.2)

    def test_extraction_requires_resolved_fit_window(self):
        with self.assertRaises(ValueError):
            audit.extract(self.grid, np.zeros((128, 32)), window=(1e-4, 1.01e-4))

    def test_exact_exponential_zero_and_deep_limit(self):
        self.assertEqual(audit.mu_exp(0.), 0.)
        self.assertAlmostEqual(audit.mu_exp(1e-15)/1e-15, 1., places=14)

    def test_newtonian_field_has_no_quadrupole(self):
        g = Grid(1e-3, 1e3, 64, 24)
        u, diagnostics = audit.solve_checked(g, lambda x: np.ones_like(x), 2., outer="asymptotic")
        self.assertLess(abs(audit.extract(g, u, window=(.02,.2))["c2"]), 1e-7)
        self.assertTrue(diagnostics["converged"])

    def test_iteration_exhaustion_is_not_convergence(self):
        with self.assertRaises(RuntimeError) as caught:
            audit.solve_checked(self.grid, audit.mu_exp, 2., maxiter=1)
        self.assertTrue(hasattr(caught.exception, "diagnostics"), "failure must retain convergence evidence")
        self.assertGreater(caught.exception.diagnostics["last_update"], 1e-9)

    def test_invalid_boundary_rejected(self):
        with self.assertRaises(ValueError):
            audit.solve_checked(self.grid, audit.mu_exp, 2., outer="unknown")


if __name__ == "__main__":
    unittest.main()
