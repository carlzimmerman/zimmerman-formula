import unittest
from fractions import Fraction as Q
import sympy as s

try:
    import cutoff_counterexample as c
except ImportError:
    c=None


class CutoffTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(c,'cutoff counterexample implementation is required')

    def test_ordered_sets_do_not_force_a_different_mode(self):
        result=c.ordered_counterexample()
        self.assertEqual(result['values'],dict(k_cmb=Q(1,10),early=Q(1,5),late=Q(1),k_gal=Q(10)))
        self.assertTrue(result['ordered_cutoffs'])
        self.assertTrue(result['cmb_early'])
        self.assertTrue(result['cmb_late'])
        self.assertFalse(result['galaxy_late'])
        self.assertEqual(result['strict_margin'],Q(1,10))

    def test_counterexample_even_with_L125_literal_cutoff_law(self):
        result=c.literal_law_counterexample()
        self.assertEqual(result['early'],Q(1000000,1091))
        self.assertEqual(result['late'],Q(1000000))
        self.assertTrue(result['same_mode_transfer'])
        self.assertFalse(result['galaxy_late'])

    def test_same_mode_transfer_with_finite_exact_controls(self):
        for early,late in ((Q(1),Q(2)),(Q(1,100),Q(3,100)),(Q(5),Q(7))):
            for k in (early/10,early/2,early*Q(99,100)):
                self.assertTrue(c.cluster_proxy(k,early))
                self.assertTrue(c.cluster_proxy(k,late))
        with self.assertRaises(ValueError):c.cluster_proxy(1,0)

    def test_expansion_factor_changes_cutoff_scaling(self):
        a,v0,H0=s.symbols('a v0 H0',positive=True)
        rad=c.instantaneous_cutoff(a,H0/a**2,v0/a)
        matter=c.instantaneous_cutoff(a,H0/a**s.Rational(3,2),v0/a)
        self.assertEqual(s.simplify(rad-H0/v0),0)
        self.assertEqual(s.simplify(matter-H0*s.sqrt(a)/v0),0)
        self.assertEqual(s.simplify(s.diff(s.log(matter),a)*a),s.Rational(1,2))


if __name__=='__main__':unittest.main(verbosity=2)
