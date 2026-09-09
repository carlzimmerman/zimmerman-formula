"""Catch wrong conformal weights, frozen H, unsafe activation and fake history."""
import importlib.util
import unittest
import mpmath as mp
import ic11_clock_pressure as vacuum


class RadiationHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 50

    def model(self):
        self.assertIsNotNone(importlib.util.find_spec('ic16_radiation_history'))
        return __import__('ic16_radiation_history')

    def test_action_variation_and_radiation_conformal_weight(self):
        self.assertTrue(all(v == 0 for v in self.model().identities().values()))

    def test_radiation_changes_friedmann_not_the_auxiliary_root(self):
        model = self.model()
        for S in ('.03', '.1', '.2'):
            old = vacuum.state(S)
            bg = model.state(S, '.1')
            self.assertEqual(bg['w'], old['w'])
            self.assertLess(abs(3*mp.exp(-mp.mpf(1)/6)*bg['H']**2-old['energy']-mp.mpf('.1')), mp.mpf('1e-40'))
            self.assertLess(abs(bg['physical_H']/old['physical_H']-bg['H']/old['H']), mp.mpf('1e-40'))

    def test_compact_activation_has_a_real_density_cap(self):
        model = self.model()
        cap = model.radiation_cap('.1')
        below = model.state('.1', cap['radiation_cap']*mp.mpf('.99'))
        above = model.state('.1', cap['radiation_cap']*mp.mpf('1.01'))
        self.assertTrue(below['compact_plateau'])
        self.assertFalse(above['compact_plateau'])
        self.assertLess(cap['maximum_radiation_fraction'], mp.mpf('.4'))

    def test_one_sided_switch_does_not_switch_off_at_high_density(self):
        model = self.model()
        self.assertEqual(model.eta_up(0), 0)
        self.assertEqual(model.eta_up(mp.sqrt(mp.mpf('1.5'))), 1)
        self.assertEqual(model.eta_up(100), 1)
        self.assertEqual(model.eta_up(-100), 1)
        mid = model.eta_up(mp.sqrt(mp.mpf(5)/8))
        self.assertAlmostEqual(mid, mp.mpf('.5'))
        self.assertTrue(model.state('.1', 100)['up_plateau'])

    def test_sourced_history_conserves_two_charges_and_physical_radiation(self):
        model = self.model()
        history = model.history('.03', '1e16', 8, samples=17)
        self.assertGreater(history['physical_efolds'], 7)
        for row in history['rows']:
            self.assertLess(abs(row['clock_charge_ratio']-1), mp.mpf('1e-30'))
            self.assertLess(abs(row['physical_radiation_conservation_ratio']-1), mp.mpf('1e-40'))
            self.assertTrue(row['up_plateau'])
            self.assertTrue(row['clock_healthy'])
            self.assertGreater(row['radiation_fraction'], mp.mpf('.5'))
            self.assertGreater(row['physical_H'], 0)
        self.assertFalse(history['full_theory_closed'])

    def test_charge_history_matches_independent_quadrature(self):
        model = self.model()
        history = model.history('.03', 10, '.4', samples=5)
        end = history['rows'][-1]['S']
        quadrature = mp.quad(lambda S: 1/(3*vacuum.state(S)['speed_squared']), [mp.mpf('.03'), end])
        self.assertLess(abs(quadrature-mp.mpf('.4')), mp.mpf('1e-35'))

    def test_switch_change_is_not_a_global_stability_certificate(self):
        model = self.model()
        unsafe = model.state('.001', '1e16')
        self.assertTrue(unsafe['up_plateau'])
        self.assertFalse(unsafe['clock_healthy'])
        self.assertLess(unsafe['kinetic'], 0)
        for args in (('.1', -1), (0, 1)):
            with self.assertRaises(ValueError):
                model.state(*args)

    def test_independent_raychaudhuri_equation(self):
        model = self.model()
        N, h = mp.mpf('.2'), mp.mpf('1e-5')
        endpoint = lambda n: model.history('.03', 10, n, samples=2)['rows'][-1]
        H2 = lambda n: endpoint(n)['H']**2
        derivative = (-H2(N+2*h)+8*H2(N+h)-8*H2(N-h)+H2(N-2*h))/(12*h)
        row = endpoint(N)
        bg = vacuum.state(row['S'])
        expected = -(2*row['X']*bg['PX']+4*row['radiation']/3)/mp.exp(-mp.mpf(1)/6)
        self.assertLess(abs((derivative-expected)/expected), mp.mpf('1e-14'))


if __name__ == '__main__':
    unittest.main()
