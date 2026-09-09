"""Checks for the nonlinear two-phase evolution probe, not theory certificates."""
import importlib.util
import unittest
import numpy as np


class TwoPhaseEvolutionTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic46_two_phase_evolution'))
        import ic46_two_phase_evolution as module
        return module

    def test_collocation_differentiates_polynomials(self):
        x,D=self.module().grid(9,-1.,0.)
        self.assertLess(np.max(abs(D@(x**4)-4*x**3)),1e-11)
        self.assertLess(np.max(abs(D@np.ones(9))),1e-11)

    def test_physical_matter_frame_recovers_the_pinned_exact_solver(self):
        d=self.module().matter_control()
        self.assertLess(d,1e-12)

    def test_nonlinear_stage_solves_constraints_and_reports_unimposed_join(self):
        # The IC41 initial Taylor data lie only 5e-6 above a coefficient-cell
        # edge; choose a patch inside that declared analytic domain.
        result=self.module().experiment(nodes=7,width=3e-5,dt=1e-8,steps=1)
        self.assertTrue(result['completed'],result.get('reason'))
        self.assertGreater(result['rhs_calls'],1)
        self.assertEqual(result['completed_steps'],1)
        self.assertIn('w_r_interface',result['rows'][-1])
        self.assertFalse(result['junction_projected'])


if __name__=='__main__':unittest.main()
