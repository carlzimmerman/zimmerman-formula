#!/usr/bin/env python3
"""Independent endpoint, extremum and common-control tests."""
import math
import unittest
import sympy as s

try:
    import common_interval as h
except ImportError:
    h = None


class CommonIntervalTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(h, 'common interval implementation is required')

    def test_stationary_polynomial_and_factorization(self):
        t,I,R,c,beta,K=s.symbols('t I R c beta K', real=True)
        D=1+beta-beta*t*t
        L=(beta*I*(1-t*t)+2*c*t-R*t*t)/D
        S=beta*I+(1+beta)*R
        expected=2*(beta*c*t*t-S*t+(1+beta)*c)
        self.assertEqual(s.factor(s.diff(L,t)*D**2-expected),0)
        T=beta*(K-I)
        q=K+T-2*c*t+(R-T)*t*t
        self.assertEqual(s.factor(q-D*(K-L)),0)
        self.assertEqual(h.stationary_polynomial(t,I,R,c,beta),expected/2)

    def test_interior_exact_extremum_not_endpoint(self):
        out=h.lower_bound(s.Integer(10),s.Integer(-1),s.Integer(1),s.Integer(1),sqrt=s.sqrt)
        self.assertEqual(out['sector'],'interior')
        self.assertEqual(s.simplify(out['t']-(4-s.sqrt(14))),0)
        self.assertEqual(s.simplify(out['lower']-(7-s.sqrt(14)/2)),0)
        # A separate maximization via eliminating t gives the exact value.
        t=s.symbols('t');L=(10+2*t-9*t*t)/(2-t*t)
        self.assertEqual(s.simplify(s.diff(L,t).subs(t,out['t'])),0)
        self.assertGreater(float(out['lower']),5.)

    def test_endpoint_and_threshold_equality(self):
        for I in (1,5):
            out=h.lower_bound(I,-1,1,1)
            self.assertEqual(out['sector'],'endpoint_one')
            self.assertEqual(out['lower'],3)
            self.assertEqual(out['t'],1)

    def test_zero_cross_all_stationary_sectors(self):
        cases=((10,-1,'endpoint_zero',5),(1,-1,'endpoint_one',1),(2,-1,'constant',1))
        for I,R,sector,want in cases:
            out=h.lower_bound(I,R,0,1)
            self.assertEqual(out['sector'],sector)
            self.assertEqual(out['lower'],want)

    def test_common_open_interval_with_opposite_slopes(self):
        # Both have K in (1,2). Opposite slopes give j in (1,2) and (0,1): empty.
        p1=h.Pencil(0,1,2,-1,0,1)
        p2=h.Pencil(2,-1,2,-1,0,1)
        out=h.common_interval([p1,p2])
        self.assertEqual(out['status'],'empty')
        self.assertIsNone(out['witness'])
        # Moving only the test pencil offset yields strict intersection (1,2).
        p3=h.Pencil(3,-1,2,-1,0,1)
        out=h.common_interval([p1,p3])
        self.assertEqual(out['status'],'nonempty')
        self.assertEqual((out['lower'],out['upper'],out['witness']),(1,2,1.5))
        for p in (p1,p3):
            self.assertTrue(h.direct_health(p,out['witness'])['healthy'])

    def test_fixed_slope_healthy_and_unhealthy(self):
        good=h.Pencil(1.5,0,2,-1,0,1)
        bad=h.Pencil(1,0,2,-1,0,1)
        self.assertEqual(h.common_interval([good,good])['status'],'nonempty')
        self.assertEqual(h.common_interval([good,bad])['status'],'empty')
        self.assertFalse(h.direct_health(bad,0)['healthy'])

    def test_invalid_domain_and_empty_family_are_not_success(self):
        for beta,R in ((0,-1),(-1,-1),(1,0),(1,1)):
            with self.assertRaises(ValueError):h.lower_bound(10,R,1,beta)
        with self.assertRaises(ValueError):h.lower_bound(math.nan,-1,1,1)
        with self.assertRaises(ValueError):h.common_interval([])

    def test_interval_membership_matches_independent_quadratic_minimum(self):
        count=0
        for I in (1,3,10):
            for R in (-.5,-2):
                for b in (0,.25,1):
                    for beta in (.01,1,3):
                        p=h.Pencil(.3,-.7,I,R,b,beta)
                        out=h.common_interval([p])
                        for j in (-20,-10,-3,0,1,5):
                            belongs=out['status']=='nonempty' and out['lower']<j<out['upper']
                            self.assertEqual(belongs,h.direct_health(p,j)['healthy'])
                            count+=1
        self.assertEqual(count,324)

    def test_two_actual_inverse_pencils_share_one_curvature_control(self):
        try:
            import actual_pencils as actual
        except ImportError:
            actual=None
        self.assertIsNotNone(actual,'actual inverse adapter is required')
        out=actual.run_control_pair()
        self.assertEqual(out['common']['status'],'nonempty')
        self.assertFalse(out['common_action_demonstrated'])
        for row in out['states']:
            self.assertLess(row['correlation_residual'],2e-8)
            self.assertTrue(row['at_shared_j']['strict_EF'])
            self.assertLess(row['at_shared_j']['residual']['metric'],1e-8)


if __name__=='__main__':unittest.main(verbosity=2)
