"""Exact algebra checks for independently expanded physical-frame actions."""

import unittest

import sympy as s

from conformal_action import derive, derive_general_map, derive_gradient_map


class ConformalActionTests(unittest.TestCase):
    def test_static_source_comes_from_minimal_particle_action(self):
        result = derive()
        source = result["particle_source"]
        self.assertEqual(source["linear_lapse_source"], -source["mass"]*result["n"])
        self.assertEqual(source["linear_spatial_source"], 0)

    def test_raw_action_identities(self):
        result = derive()
        self.assertTrue(result["residuals"])
        for name, residual in result["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)

    def test_principal_action_structure(self):
        result = derive()
        m, k, alpha, eta, z, zd, n, nd, v = (
            result[key] for key in ("m", "k", "alpha", "eta", "z", "zd", "n", "nd", "v"))
        expected = m*(-3*(zd+eta*nd)**2+2*k*v*(zd+eta*nd)
                      + k**2*(z**2+2*(1+2*eta)*n*z
                              +(2*eta+3*eta**2+alpha)*n**2))
        self.assertEqual(s.expand(result["L"]-expected), 0)
        self.assertLessEqual(result["L"].free_symbols,
                             {m, k, alpha, eta, z, zd, n, nd, v})

    def test_lapse_velocity_and_untransformed_control(self):
        result = derive()
        m, k, alpha, eta, z, zd, n, nd, v = (
            result[key] for key in ("m", "k", "alpha", "eta", "z", "zd", "n", "nd", "v"))
        self.assertEqual(s.diff(result["L"], zd, nd), -6*m*eta)
        self.assertEqual(s.simplify(s.diff(result["L"], nd)
                                   - eta*s.diff(result["L"], zd)), 0)
        control = m*(-3*zd**2+2*k*v*zd+k**2*(z**2+2*n*z+alpha*n**2))
        self.assertEqual(s.expand(result["L"].subs(eta, 0)-control), 0)

    def test_general_map_static_and_physical_light_cone(self):
        result = derive_general_map()
        for name, residual in result["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)
        c, d, C, D = (result[key] for key in ("c", "d", "C", "D"))
        self.assertEqual(s.simplify(result["tensor_speed2"]-D**2/C), 0)
        self.assertEqual(s.simplify(result["newton_factor"]-(1+d)**2), 0)
        self.assertEqual(s.simplify(result["slip_coefficient"].subs(d, c/2)-(1+c)), 0)
        self.assertEqual(s.simplify(result["G_effective"]
                                   * 8*s.pi*result["m"]*D*s.sqrt(C)*(1+d)**2), 1)

    def test_derivative_map_retains_higher_spatial_operator(self):
        result = derive_gradient_map()
        cs, ds = result["cs"], result["ds"]
        self.assertEqual(s.simplify(result["gradient_squared_coefficient"]
                                   -(cs*ds+cs**2/4)), 0)
        self.assertEqual(s.simplify(result["luminal_gradient_squared_coefficient"]
                                   -3*cs**2/4), 0)
        self.assertEqual(result["residuals"]["integration_by_parts"], 0)
        self.assertEqual(s.simplify(result["fourier_fourth_order_term"]
                                   -3*cs**2*result["a_dot_k"]**2
                                   * result["k_squared"]*result["n"]**2), 0)


if __name__ == "__main__":
    unittest.main()
