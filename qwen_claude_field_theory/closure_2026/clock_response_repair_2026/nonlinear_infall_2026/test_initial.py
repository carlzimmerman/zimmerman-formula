#!/usr/bin/env python3
"""Initial-slice tests: no MOND/PPN/DOF answers are supplied to the solver."""
import unittest

import numpy as np

from initial import coefficients, geometry, solve_slice, independent_fd, force_bound


class InitialTests(unittest.TestCase):
    def test_background_preservation_and_zero_source(self):
        for gamma in (0.0, 1e-6):
            c = coefficients(gamma)
            self.assertLess(abs(c["F0"]-c["lambda0"]), 1e-13)
            out = solve_slice(0., .2, gamma=gamma)
            self.assertLess(np.max(abs(out["delta"])), 1e-13)
            self.assertLess(np.max(abs(out["Qdot"]-c["qdot"])), 1e-13)
            self.assertLess(np.max(abs(out["Kdot"]-3*c["Hdot"])), 1e-12)
            self.assertLess(np.max(abs(out["g_areal"])), 1e-13)

    def test_hamiltonian_geometry_and_regular_center(self):
        r = np.linspace(0, 5, 20001)
        rho, f, fp, enclosed = geometry(r, .03, .7, 1.)
        self.assertEqual(f[0], 1.)
        self.assertEqual(fp[0], 0.)
        residual = 1-f[1:]-r[1:]*fp[1:]-rho[1:]*r[1:]**2
        self.assertLess(np.max(abs(residual)), 1e-15)
        np.testing.assert_allclose(np.gradient(f, r)[10:-10], fp[10:-10],
                                   rtol=2e-5, atol=2e-9)
        self.assertTrue(np.all(np.diff(enclosed) >= -1e-15))

    def test_lapse_independent_solver_and_negative_control(self):
        out = solve_slice(.04, .5, outer=12., points=501)
        self.assertGreater(np.min(out["N"]), 0.)
        self.assertLessEqual(np.max(out["N"]), 1.+1e-12)
        self.assertLess(out["equation_relative_residual"], 1e-8)
        self.assertLess(out["offgrid_equation_relative_residual"], 1e-6)
        self.assertGreater(out["unit_lapse_relative_residual"], .99)
        errors = []
        for nodes in (1001, 2001, 4001):
            r, delta = independent_fd(.04, .5, 12., nodes, out["coefficients"])
            errors.append(np.max(abs(delta-out["solution"].sol(r)[0])))
        self.assertLess(errors[-1], errors[0]/10)
        self.assertLess(errors[-1], 2e-7)

    def test_domain_refinement_and_initial_evolution_equations(self):
        a = solve_slice(.05, .3, outer=10.)
        b = solve_slice(.05, .3, outer=16.)
        self.assertLess(np.max(abs(a["delta"]-b["solution"].sol(a["r"])[0])), 1e-9)
        for key, error in a["time_equation_absolute_residuals"].items():
            self.assertLess(error, 1e-10, key)
        self.assertGreater(np.max(abs(a["chi_gradient_dot"])), 0.)
        self.assertGreater(np.max(abs(a["dust_gradient_dot"])), 0.)

    def test_small_source_response_not_inserted_mond(self):
        a = solve_slice(1e-3, .3)
        b = solve_slice(1e-5, .3)
        r = .9
        ga, gb = (np.interp(r, x["r"], x["g_areal"]) for x in (a,b))
        slope = np.log(ga/gb)/np.log(100.)
        self.assertLess(abs(slope-1.), .003)
        # This checks measured perturbative scaling, not a universal no-go.
        self.assertGreater(abs(slope-.5), .4)

    def test_invalid_coordinate_patch_is_rejected(self):
        with self.assertRaises(ValueError):
            solve_slice(100., 1.)

    def test_maximum_principle_force_bound(self):
        for gamma in (0.,1e-6):
            out = solve_slice(.1,.4,gamma=gamma)
            bound = force_bound(out,.1,.4)
            self.assertTrue(bound["hypotheses"])
            self.assertLess(np.max(-out["delta"])-bound["d"]*.1, 1e-12)
            self.assertGreaterEqual(np.min(out["g_areal"]), -1e-12)
            self.assertLess(np.max(out["g_areal"]-.1*bound["C"]), 1e-12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
