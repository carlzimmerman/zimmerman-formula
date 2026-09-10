import unittest
import sympy as s
import conformal_dictionary as d


class DictionaryTests(unittest.TestCase):
    def test_radial_conformal_bridge(self):
        self.assertEqual(d.derive()['radial_variation_bridge_residual'],0)

    def test_scalar_mapping(self):
        a=d.derive()
        self.assertEqual(a['G_derivative_bridge'],0)
        self.assertEqual(a['linear_C_invertibility_numerator'],1)
        self.assertEqual(a['linear_inverse_residual'],0)

    def test_conformal_lensing_sum(self):
        self.assertEqual(d.derive()['EF_Weyl_residual'],0)

    def test_no_slip_requires_common_clock_radial_ratio(self):
        self.assertEqual(d.universal_condition()['residual'],0)

    def test_new_radial_equation_recovers_old_constant_F_case(self):
        a=d.derive();r,g,h,P,F=s.symbols('r g h P F',nonzero=True)
        self.assertEqual(s.factor(a['B'].subs(h,0)-(1+2*r*g)/(1+r*r*P/(2*F))),0)
        self.assertEqual(s.factor(a['weak_no_slip_pressure']-4*F*h/r),0)


if __name__=='__main__':unittest.main()
