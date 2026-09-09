"""Same-action slow-clock evolution and observable propagation checks."""
import importlib.util
import unittest
import mpmath as mp
import numpy as np
import ic28_constant_tensor as base


class SlowClockTests(unittest.TestCase):
    def implementation(self):
        self.assertIsNotNone(importlib.util.find_spec('ic29_slow_clock'),
                             'Slow-clock evolution not implemented')
        import ic29_slow_clock
        return ic29_slow_clock

    def test_short_evolution_retains_actual_constraint_charge_and_schur(self):
        m=self.implementation()
        h=m.evolve(.001,max_step=.0001)
        self.assertTrue(h['success'],h['reason'])
        self.assertLess(h['maximum_charge_drift'],1e-9)
        self.assertLess(h['maximum_constraint_residual'],1e-20)
        for row in h['states']:
            self.assertAlmostEqual(row['M'],float(h['target_M']),places=8)

    def test_interpolated_state_uses_genuine_jets_and_physical_no_slip(self):
        m=self.implementation()
        h=m.evolve(.001,max_step=.0001)
        with mp.workdps(45):
            b=m.state_at(h,.0005)
            for value in base.integrability(b).values():
                self.assertLess(abs(value),mp.mpf('1e-30'))
            phase=mp.matrix([.2,.3,-.7,.11,-.23,.41])
            metric=base.physical_fields(b,mp.mpf('.1'),phase)
            self.assertLess(abs(metric['Phi']-metric['Psi']),mp.mpf('1e-30'))

    def test_tiny_positive_pin_not_misclassified_by_float_underflow(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'pin_info'),'Exact pin-domain check missing')
        with mp.workdps(40):
            b=m.initial();b['q']=mp.mpf('-1.9698610287519809')
            pin=m.pin_info(b)
            self.assertGreater(pin['eta'],0)
            self.assertEqual(float(pin['eta']),0)
            self.assertGreater(pin['domain_margin'],0)

    def test_full_propagator_volume_and_independent_metric_rows(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'transport'),'Physical propagation missing')
        h=m.evolve(.01,max_step=.001,pin_h0='.5')
        r=m.transport(h,.1,nodes=11)
        self.assertLess(r['relative_volume_error'],1e-8)
        phi=np.array(r['final_metric_map'])[0]
        psi=np.array(r['final_metric_map'])[1]
        self.assertLess(np.linalg.norm(phi-psi),1e-9)
        self.assertGreater(np.linalg.norm(phi),0)

    def test_frozen_polynomial_jets_are_derivatives_of_one_function(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'coefficient_table'),'Frozen coefficient table missing')
        h=m.evolve(.01,max_step=.001,pin_h0='.5')
        table=m.coefficient_table(h,11)
        with mp.workdps(45):
            S=mp.mpf(table.x[2])+mp.mpf('.37')*(mp.mpf(table.x[3])-mp.mpf(table.x[2]))
            jets=m.polynomial_jets(S,table)
            self.assertLess(abs(mp.diff(lambda x:m.polynomial_jets(x,table)[0],S)-jets[1]),mp.mpf('1e-32'))
            self.assertLess(abs(mp.diff(lambda x:m.polynomial_jets(x,table)[0],S,2)-jets[2]),mp.mpf('1e-30'))

    def test_changed_sources_solve_constraints_without_retuning_D(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'source_response'),'Fixed-action source test missing')
        h=m.evolve(.01,max_step=.001,pin_h0='.5')
        table=m.coefficient_table(h,11)
        with mp.workdps(40):
            r=m.source_response(h,table,2)
            self.assertLess(max(abs(x) for x in r['constraints']),mp.mpf('1e-25'))
            self.assertGreater(r['S'],mp.mpf(h['states'][0]['S']))


if __name__=='__main__':
    unittest.main()
