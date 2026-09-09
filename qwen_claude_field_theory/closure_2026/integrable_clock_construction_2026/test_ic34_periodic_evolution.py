"""Many-step same-action flow, without projecting the momentum constraint."""
import importlib.util
import unittest
import numpy as np


class PeriodicEvolutionTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic34_periodic_evolution'))
        import ic34_periodic_evolution
        return ic34_periodic_evolution

    def test_independent_action_identities(self):
        for name,value in self.module().identities().items():
            self.assertEqual(value,0,name)

    def test_periodic_derivatives_and_zero_mode(self):
        m=self.module(); x,D,D2=m.grid(32)
        self.assertLess(np.max(abs(D@np.sin(3*x)-3*np.cos(3*x))),1e-12)
        self.assertLess(np.max(abs(D2@np.sin(3*x)+9*np.sin(3*x))),1e-11)
        self.assertLess(np.max(abs(D@np.ones(32))),1e-12)

    def test_many_steps_preserve_unprojected_momentum(self):
        out=self.module().experiment(nodes=32,dt=.002,end=.04,amplitude=.02)
        self.assertTrue(out['success'],out)
        self.assertEqual(out['steps'],20)
        self.assertLess(out['max_momentum_constraint'],1e-6)
        self.assertLess(out['max_lapse_constraint'],1e-8)
        self.assertLess(out['max_relative_matter_charge_drift'],1e-7)
        self.assertGreater(out['max_fluid_gradient'],0)


if __name__=='__main__':
    unittest.main()
