#!/usr/bin/env python3
"""Exact compatibility algebra; no numerical mass scan or physical rank claim."""
import unittest
import sympy as s


class CompatibilityStructure(unittest.TestCase):
    def test_unsquared_h_matching_and_nonzero_U_derivative(self):
        alpha, U, V, k = s.symbols("alpha U V k", positive=True)
        h = alpha * s.sqrt(U) / (2 * (U - V))
        derivative = -(U + V) / (2 * U * (U - V))
        self.assertEqual(s.factor(s.diff(h, U) / h - derivative), 0)
        radical = s.sqrt(alpha**2 + 16 * k**2 * V)
        plus = (alpha + radical) / (4 * k)
        minus = 4 * k * V / (alpha + radical)
        for target, root in ((k, plus), (-k, minus)):
            # This is the unsquared equation in sqrt(U), including its sign.
            self.assertEqual(s.simplify(2 * target * (root**2 - V) - alpha * root), 0)

    def test_first_preservation_is_affine_collinearity(self):
        A2, A3, B2, B3 = s.symbols("A2 A3 B2 B3", nonzero=True)
        p = -A2 / B2
        K = A3 * B2 - A2 * B3
        self.assertEqual(s.factor(A3 + p * B3 - K / B2), 0)

    def test_preservation_determinant_tangency_identity(self):
        A2, A3, B2, B3 = s.symbols("A2 A3 B2 B3", nonzero=True)
        A2d, A3d, B2d, B3d = s.symbols("A2d A3d B2d B3d")
        p = -A2 / B2
        K = A3 * B2 - A2 * B3
        Kd = A3d * B2 + A3 * B2d - A2d * B3 - A2 * B3d
        Q = (A3d + p * B3d) * B2 - (A2d + p * B2d) * B3
        self.assertEqual(s.factor(Kd - Q - B2d * K / B2), 0)

    def test_next_preservation_uses_total_derivatives(self):
        p, k = s.symbols("p k")
        d0a, d1a, d0b, d1b, b = s.symbols("d0a d1a d0b d1b b")
        # D_p = D_0 + p D_1, with p held fixed inside D_p.
        c = d0a + p * (d1a + d0b) + p**2 * d1b
        direct = d0a + p * d1a + k * b + p * (d0b + p * d1b)
        self.assertEqual(s.expand(direct - c - k * b), 0)

    def test_implicit_matching_jacobian(self):
        Hy, HU, Fy, FU = s.symbols("Hy HU Fy FU", nonzero=True)
        reduced_y_derivative = Fy - FU * Hy / HU
        jacobian = Hy * FU - HU * Fy
        self.assertEqual(s.factor(jacobian + HU * reduced_y_derivative), 0)

    def test_action_jet_control_cancellation_at_arbitrary_tested_order(self):
        pjet = s.symbols("p0:7")
        h1 = s.symbols("h1_0:7")
        h3 = s.symbols("h3_0:7")
        for n in range(1, 7):
            # Leibniz: G^(n+1) = (p*h)^(n), with p=P_X.
            delta = sum(s.binomial(n, j) * pjet[j] * (h3[n-j] - h1[n-j])
                        for j in range(n+1))
            lower_matching = {h3[j]: h1[j] for j in range(n)}
            residual = delta.subs(lower_matching) - pjet[0] * (h3[n] - h1[n])
            self.assertEqual(s.expand(residual), 0)

    def test_finitely_many_seed_conditions_do_not_prove_invariance(self):
        X = s.symbols("X", real=True)
        # Abstract analytic preservation model, NOT a KGB/physical counterexample:
        # a1=b1=0, a2=-1,b2=1 force p=1; a3=-2+X^2,b3=2.
        # Then F1=F2=0, F3=X^2 and h3=exp(X^3/3), h1=h2=1.
        h3 = s.exp(X**3 / 3)
        self.assertEqual(h3.subs(X, 0), 1)
        self.assertEqual(s.diff(h3, X).subs(X, 0), 0)
        self.assertEqual(s.diff(h3, X, 2).subs(X, 0), 0)
        self.assertEqual(s.diff(h3, X, 3).subs(X, 0), 2)
        self.assertEqual(s.simplify(s.diff(h3, X) / h3), X**2)

    def test_continuum_affine_line_and_mass_curvature_identity(self):
        mass = s.symbols("mass", real=True)
        a, b = s.Function("a")(mass), s.Function("b")(mass)
        p = -s.diff(a, mass) / s.diff(b, mass)
        curvature = s.diff(a, mass, 2) * s.diff(b, mass) - s.diff(a, mass) * s.diff(b, mass, 2)
        self.assertEqual(s.factor(s.diff(p, mass) + curvature / s.diff(b, mass)**2), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
