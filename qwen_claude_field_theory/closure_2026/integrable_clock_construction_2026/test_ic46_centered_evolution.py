"""A known zero-reaction initial slice must not acquire a roundoff-scale source."""
import importlib.util
import unittest


class CenteredEvolutionTests(unittest.TestCase):
    def test_centering_reduces_initial_constraint_error_without_changing_equations(self):
        self.assertIsNotNone(importlib.util.find_spec('ic46_centered_evolution'))
        import ic46_centered_evolution as module
        d=module.experiment(nodes=7,width=3e-5,dt=1e-8,steps=1)
        self.assertTrue(d['completed'],d.get('reason'))
        self.assertLess(d['rows'][0]['lapse_max'],1e-7)
        self.assertLess(d['rows'][0]['inactive_clock_max'],1e-7)
        self.assertLess(abs(d['rows'][0]['active_clock_reaction']),1e-7)
        self.assertFalse(d['junction_projected'])


if __name__=='__main__':unittest.main()
