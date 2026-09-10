"""Conditional algebra and actual static-inverse controls; no theory-fit test."""
import unittest
import mpmath as mp
import sympy as s
import zero_gamma as z


class ZeroBraidingTests(unittest.TestCase):
    def test_original_principal_identity(self):
        out=z.symbolic_principal_check()
        self.assertTrue(all(value==0 for value in out['matrix_residuals']))
        self.assertEqual(out['scalar_residual'],0)
        self.assertEqual(out['EF_ratio_residual'],0)

    def test_common_lower_jets_but_actual_second_jets(self):
        with mp.workdps(65):
            pair=z.pressure_pair('.1','.14')
            self.assertLess(abs(pair[0]['P']/pair[1]['P']-1),mp.mpf('1e-55'))
            for a in pair:
                f,j=mp.mpf('.05'),mp.mpf('7')
                jets=z.action_jets(a,f,j)
                self.assertLess(abs(a['gamma']),mp.mpf('1e-55'))
                expected=2*a['P']*j/a['F']+2*a['P']*f*f/a['F']**2+a['H']*jets[4]
                self.assertLess(abs((jets[3]-expected)/expected),mp.mpf('1e-55'))
                self.assertGreater(abs(jets[4]),1)
            self.assertGreater(abs(z.action_jets(pair[0],f,j)[4]-z.action_jets(pair[1],f,j)[4]),1)
            for index in range(3):
                left,right=(z.action_jets(a,f,j)[index] for a in pair)
                self.assertLess(abs(left-right)/max(abs(left),abs(right),1),mp.mpf('1e-55'))

    def test_actual_on_shell_matrix_and_j_independence(self):
        with mp.workdps(65):
            for y in ('.1','10'):
                a=z.zero_state('1e-6',y,U='1e-7')
                first=z.evaluate(a,mp.mpf('.05'),0)
                other=z.evaluate(a,mp.mpf('.05'),mp.mpf('1e10'))
                self.assertLess(first['Einstein_relative_error'],mp.mpf('1e-50'))
                self.assertLess(first['scalar_relative_error'],mp.mpf('1e-50'))
                self.assertLess(first['principal_identity_error'],mp.mpf('1e-50'))
                self.assertLess(first['current_scaled_error'],mp.mpf('1e-50'))
                self.assertLess(first['P_derivative_relative_error'],mp.mpf('1e-50'))
                self.assertFalse(first['strict_EF_scalar_cone'])
                self.assertFalse(first['bounded_EF_static_quadratic_energy'])
                for name in ('kinetic','cross','radial','angular'):
                    self.assertLess(abs(first[name]-other[name])/max(abs(first['kinetic']),1),mp.mpf('1e-45'))

    def test_next_control_coefficient(self):
        with mp.workdps(55):
            a=z.zero_state('1e-6','.1',U='1e-7');f=mp.mpf('.05')
            first=z.normalized_derivatives(a,f)
            n0=z.next_derivatives(a,f,0);n1=z.next_derivatives(a,f,1)
            for k in range(2):
                self.assertLess(abs((n1[k]-n0[k])-first[k]/f)/max(abs(first[k]/f),1),mp.mpf('1e-40'))

    def test_matching_polynomial_is_checked_unsquared(self):
        with mp.workdps(65):
            lower=z.curvature_matches(*z.pressure_pair('.1','.14'))
            upper=z.curvature_matches(*z.pressure_pair('1','3.8'))
            self.assertEqual(lower['sector'],'quadratic')
            self.assertEqual(lower['accepted'],[])
            self.assertTrue(all(not row['physical'] for row in lower['candidates']))
            # One squared root is physical but has opposite GXX signs.
            self.assertTrue(any(row['physical'] for row in upper['candidates']))
            self.assertEqual(upper['accepted'],[])
            self.assertFalse(upper['same_K_sign'])

    def test_matching_zero_coefficient_sector_and_map_guard(self):
        out=z.solve_matching_coefficients(0,0,0,0,0,0)
        self.assertEqual(out['sector'],'both_GXX_zero')
        self.assertEqual(out['accepted'],'all physical U pairs')
        with mp.workdps(30):
            a=z.zero_state('1e-6','.1')
            with self.assertRaises(ValueError):z.evaluate(a,a['F']/a['X'],0)
            with self.assertRaises(ValueError):z.evaluate(a,0,0)

    def test_identical_state_is_an_accepted_matching_control(self):
        with mp.workdps(40):
            a=z.zero_state('1e-6','.1')
            out=z.curvature_matches(a,a)
            self.assertEqual(out['sector'],'identity_polynomial')
            self.assertEqual(out['accepted'],'continuous physical intersection')
            self.assertEqual(out['open_x1_interval'],[0,1])

    def test_finite_curvature_reduction_not_projected_derivative(self):
        with mp.workdps(60):
            for U in ('1e-7','.2'):
                a=z.zero_state('1e-6','.1',U=U);f=mp.mpf('.07')
                K,t,v=z.matching_coefficients(a);x=a['U']/a['Q']
                gamma2=z.action_jets(a,f,mp.mpf('11'))[4]/(f*f)
                self.assertLess(abs(gamma2-K*mp.sqrt(a['U'])/a['Q'])/abs(gamma2),mp.mpf('1e-50'))
                self.assertLess(abs(a['H']*gamma2-t*x-v)/max(abs(t*x),abs(v),1),mp.mpf('1e-50'))
        K1,K2,u,v,x=s.symbols('K1 K2 u v x')
        polynomial=(-K1**2+K2**2*u**2)*x*x+(K1**2-K2**2*u*(1-2*v))*x-K2**2*v*(1-v)
        self.assertEqual(s.expand(polynomial-(K1*K1*x*(1-x)-K2*K2*(u*x+v)*(1-u*x-v))),0)


if __name__=='__main__':unittest.main()
