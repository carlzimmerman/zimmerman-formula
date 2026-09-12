#!/usr/bin/env python3
"""Independent symbolic and numerical checks for the static restriction."""
import unittest
import mpmath as mp
import sympy as sp
from clock_response import StaticClock


class ClockResponseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = StaticClock()

    def test_generic_quartic_stationary_elimination(self):
        u,z,Q,s0,W,W1,W2,P1,P2,A,B = sp.symbols("u z Q s W W1 W2 P1 P2 A B")
        F = W-2*Q*Q*W1
        Astar = -2*Q*W1/F
        r = 1-Q*Astar
        Bstar = (-W*Astar**3/2+W1*(Astar*r*r-Q*Astar*Astar*r)-2*Q*W2*r**3)/F
        v = u-Q*z
        L2 = -P1*u*u+s0*(W1*v*v-W*z*z/2)
        L4 = P2*u**4/2+s0*(-W*z**4/8+W1*z*z*v*v/2+W2*v**4/2)
        flux = sp.Poly(sp.diff(L2+L4,z).subs(z,A*u+B*u**3),u)
        self.assertEqual(sp.cancel(flux.coeff_monomial(u).subs(A,Astar)),0)
        self.assertEqual(sp.cancel(flux.coeff_monomial(u**3).subs({A:Astar,B:Bstar})),0)
        eff = sp.Poly((L2+L4).subs(z,A*u+B*u**3),u)
        c2 = -P1+s0*W1*W/F
        c4 = P2/2+s0*(-W*Astar**4/8+W1*Astar*Astar*r*r/2+W2*r**4/2)
        self.assertEqual(sp.cancel(eff.coeff_monomial(u**2).subs(A,Astar)-c2),0)
        # B drops out of the quartic coefficient because the quadratic is stationary.
        self.assertEqual(sp.cancel(eff.coeff_monomial(u**4).subs(A,Astar)-c4),0)

    def test_joint_expansion_comes_from_invariants(self):
        e,u,z,Q,s0,W,W1,W2,P1,P2=sp.symbols("e u z Q s W W1 W2 P1 P2")
        Y=(e*u-Q*e*z)**2/(1-e*e*z*z)
        full=-P1*e*e*u*u+P2*e**4*u**4/2+s0*sp.sqrt(1-e*e*z*z)*(W+W1*Y+W2*Y*Y/2)
        poly=sp.Poly(sp.series(full,e,0,5).removeO(),e)
        v=u-Q*z
        expected=P2*u**4/2+s0*(-W*z**4/8+W1*z*z*v*v/2+W2*v**4/2)
        self.assertEqual(sp.expand(poly.coeff_monomial(e**4)-expected),0)

    def test_archived_state_is_not_replaced_by_reference(self):
        m = self.model
        self.assertNotEqual(m.Q,m.bg["q"])
        for old,new in (("PX","P_X"),("PXX","P_XX"),("W","W"),("WY","W_Y"),("WYY","W_YY")):
            self.assertAlmostEqual(m.state["jets"][old],m.j0[new],places=14)

    def test_two_exact_derivative_routes_and_domain(self):
        m = self.model
        for u in (0,0.0001,0.001,0.003,0.01):
            for z in (m.solve(u),-0.02,0.015):
                a,b = m.evaluate(u,z),m.radical(u,z)
                self.assertAlmostEqual(a["Lz"],b["Lz"],places=15)
                self.assertAlmostEqual(a["Lzz"],b["Lzz"],places=14)
                P=m.model.jets(m.tau,a["X"],a["Y"])["P"]
                self.assertAlmostEqual(a["L"]-P,b["clock_lagrangian"],places=15)
                for key in ("clock_timelike_margin","P_log_numerator","P_log_denominator","W_sqrt_argument"):
                    self.assertGreater(a[key],0)

    def test_schur_from_differentiating_exact_eliminated_gradient(self):
        m = self.model
        for u in (0,0.0004,0.001,0.002,0.01):
            h=1e-7
            numerical=(m.row(u+h)["Lu"]-m.row(u-h)["Lu"])/(2*h)
            self.assertAlmostEqual(numerical,m.row(u)["schur"],delta=2e-10)

    def test_transverse_identity_on_eliminated_branch(self):
        for u in (0.0001,0.0004,0.001,0.0015398642948459,0.002,0.01):
            r=self.model.row(u)
            self.assertAlmostEqual(r["transverse_schur"],r["Lu"]/u,delta=1e-13)
            self.assertLess(r["transverse_clock"],0)

    def test_affine_einstein_gate_uses_high_precision_stationarity(self):
        result=self.model.high_precision_root("Lu",0.00154)
        gate=result["conditional_affine_transverse_principal"]
        self.assertLess(abs(mp.mpf(result["target_residual"])),mp.mpf("1e-60"))
        self.assertLess(abs(mp.mpf(gate["G_without_metric_feedback_evaluated"])),mp.mpf("1e-60"))
        self.assertLess(mp.mpf(gate["deltaG_metric"]),0)
        self.assertGreater(mp.mpf(gate["K_with_metric_feedback"]),0)
        self.assertLess(mp.mpf(gate["quarter_discriminant"]),0)
        self.assertLess(abs(mp.mpf(gate["float_gradient_error_against_high_precision"])),mp.mpf("1e-14"))
        self.assertTrue(all(gate["existing_covariant_symbolic_checks"].values()))

    def test_branch_clock_block_and_reversal(self):
        m=self.model
        self.assertGreater(m.F,0)
        self.assertGreater(m.C,0)
        self.assertGreater(m.Q*m.Q-m.bg["ell"],0)
        self.assertGreater(m.j0["P_XX"]+m.s*m.j0["W_YY"],0)
        self.assertLess(m.c4,0)
        self.assertGreater(m.row(0)["schur"],0)
        self.assertLess(m.row(0.002)["schur"],0)
        self.assertGreater(m.row(0.001)["Lu"],0)
        self.assertLess(m.row(0.002)["Lu"],0)
        for u in (0,0.0001,0.001,0.002,0.01):
            row=m.row(u)
            self.assertLessEqual(row["z"],0)
            self.assertLess(abs(row["Lz"]),1e-15)
            self.assertLessEqual(row["Lzz"],-m.s*m.F+1e-16)
            self.assertAlmostEqual(m.solve(-u),-row["z"],places=15)


if __name__ == "__main__":
    unittest.main(verbosity=2)
