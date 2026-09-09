#!/usr/bin/env python3
import unittest
import mpmath as mp


class PoleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps=80

    def model(self):
        return __import__('ic17_pole_clock')

    def test_exact_pole_identities(self):
        self.assertTrue(all(v==0 for v in self.model().identities().values()))

    def test_static_zero_jet_defined_before_pole_evaluation(self):
        m=self.model()
        point=(mp.mpf('.6'),mp.mpf('.1'),mp.mpf(0))
        self.assertEqual(m.phase_delta(*point),0)
        for i in range(3):
            self.assertEqual(mp.diff(m.phase_delta,point,tuple(int(k==i) for k in range(3))),0)

    def test_invalid_active_pole_and_excluded_boundary(self):
        m=self.model()
        with self.assertRaises(ValueError):m.phase_delta(mp.mpf('.5'),0,1)
        with self.assertRaises(ValueError):m.phase_delta(mp.mpf('.6'),0,1)
        with self.assertRaises(ValueError):m.phase_delta(mp.mpf('.5'),0,mp.sqrt(mp.mpf('.5')))
        self.assertEqual(m.phase_delta(mp.mpf('.5'),0,0),0)

    def test_failed_checks_cannot_be_reported_as_success(self):
        m=self.model()
        sample=dict(exact_checks={'identity':'0'},scan={'unhealthy_samples':0},late_scan={'unhealthy_samples':0},
                    radiation_history={'unhealthy_samples':0,'quadrature_minus_charge':'0',
                                       'max_charge_error':'0','max_radiation_charge_error':'0'})
        self.assertTrue(m.verification_ok(sample))
        sample['scan']['unhealthy_samples']=1
        self.assertFalse(m.verification_ok(sample))
        sample['scan']['unhealthy_samples']=0
        sample['exact_checks']['identity']='1'
        self.assertFalse(m.verification_ok(sample))

    def test_finite_late_branch_before_condensate(self):
        condensate,rows=self.model().late_scan()
        self.assertTrue(all(b['admissible'] for b in rows))
        self.assertGreater(condensate,rows[-1]['S'])

    def test_pressure_derivatives_and_actual_auxiliary_root(self):
        m=self.model()
        S=mp.mpf('.002')
        b=m.state(S)
        step=mp.mpf('1e-15')
        left,right=m.state(S-step),m.state(S+step)
        self.assertLess(abs((right['P']-left['P'])/(2*step)-b['PS']),mp.mpf('1e-19'))
        self.assertLess(abs((right['PS']-left['PS'])/(2*step)-b['PSS_effective']),mp.mpf('1e-16'))
        self.assertLess(abs(b['constraint']),mp.mpf('1e-60'))
        self.assertLess(abs(b['canonical_identity_residual']),mp.mpf('1e-60'))

    def test_requested_loggrid_health_and_dust_limit(self):
        m=self.model()
        rows=m.scan()
        self.assertEqual(len(rows),241)
        self.assertTrue(all(b['admissible'] for b in rows))
        for b in rows:
            self.assertEqual(b['auxiliary_rank'],2)
        b=rows[0]
        self.assertLess(abs(b['speed_squared']/(b['delta']/4)-1),mp.mpf('1e-6'))
        self.assertLess(abs(b['energy']/b['clock_charge_density']-1),mp.mpf('1e-6'))

    def test_backward_radiation_history_and_charge_conservation(self):
        m=self.model()
        history=m.history(samples=41)
        self.assertLess(abs(history['physical_efolds']-8),mp.mpf('1e-55'))
        self.assertLess(abs(history['physical_efolds_quadrature']-history['physical_efolds']),mp.mpf('1e-55'))
        self.assertTrue(all(b['admissible'] for b in history['states']))
        self.assertGreater(history['states'][0]['radiation_fraction'],mp.mpf('.5'))
        for b in history['states']:
            self.assertLess(abs(b['charge_ratio']-1),mp.mpf('1e-55'))
            self.assertLess(abs(b['radiation_charge_ratio']-1),mp.mpf('1e-55'))


if __name__=='__main__':
    unittest.main()
