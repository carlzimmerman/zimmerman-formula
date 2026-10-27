import math
import unittest
from atomic import Atom, HC, LIGHT, parcel


class AtomicTests(unittest.TestCase):
    def test_hydrogen_threshold(self):
        a = Atom(1/137.035999084, 510998.95, 938272088.16)
        self.assertAlmostEqual(a.binding, 13.5983, delta=.002)
        self.assertAlmostEqual(a.photo(a.binding)/1e-18, 6.30, delta=.02)
        self.assertEqual(a.photo(.99*a.binding), 0.)

    def test_milne_thermal_balance(self):
        a = Atom(.01, 1e6, 1e7)
        for theta in (.05, .1, .3, 1., 3., 10.):
            T=theta*a.binding
            rec=a.recombination(T, T)[0]
            reverse=a.photo_rate(T)[0]
            self.assertAlmostEqual(reverse/(rec*a.saha(T)), 1., delta=2e-7)

    def test_mass_scaling(self):
        a=Atom(.01,1e6,1e7); b=Atom(.01,1e7,1e8)
        self.assertAlmostEqual(b.binding/a.binding,10.)
        self.assertAlmostEqual(b.recombination(b.binding)[0]/a.recombination(a.binding)[0],.01,delta=1e-10)

    def test_closed_energy(self):
        r=parcel(Atom(.01,1e6,1e7),.1,3.,1e-9)
        self.assertLess(r['max_energy_error'],1e-7)
        self.assertTrue(0 < r['bound_fraction'] < 1)
        self.assertGreater(r['temperature_over_binding'],0.)

if __name__=='__main__':
    unittest.main()
