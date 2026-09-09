"""Tests of action-function integrability, not full-theory certification."""
import importlib.util
import unittest
import mpmath as mp


class PotentialTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic24_potential'), 'Integrated coefficient implementation missing')
        import ic24_potential
        return ic24_potential

    def test_constraints_and_computed_schur(self):
        m=self.module()
        with mp.workdps(40):
            b=m.initial();r=m.reconstruct(b['S'],b['q'],b['z'],b['Q'],b['parameters'],b['fluids'])
            self.assertLess(max(map(abs,r['constraints'])),mp.mpf('1e-30'))
            self.assertLess(abs(r['M']+3),mp.mpf('1e-30'))

    def test_total_derivatives_integrate_one_function(self):
        m=self.module()
        with mp.workdps(40):
            b=m.initial();r=m.reconstruct(b['S'],b['q'],b['z'],b['Q'],b['parameters'],b['fluids'])
            errors=m.integrability(r)
            self.assertLess(max(abs(x) for x in errors.values()),mp.mpf('1e-28'))

    def test_preservation_is_variation_with_fixed_jets(self):
        m=self.module()
        with mp.workdps(40):
            b=m.initial();r=m.reconstruct(b['S'],b['q'],b['z'],b['Q'],b['parameters'],b['fluids'])
            self.assertLess(max(map(abs,r['preservation'])),mp.mpf('1e-30'))
            self.assertGreater(r['principal']['gradient_margin'],0)
            self.assertGreater(r['principal']['lightcone_margin'],0)

    def test_integrated_branch_past_old_crossing(self):
        m=self.module()
        self.assertTrue(hasattr(m,'evolve'),'Background integrator missing')
        result=m.evolve(target_Q=.005)
        self.assertTrue(result['solver_success'])
        self.assertAlmostEqual(result['states'][-1]['Q'],.005,places=10)
        self.assertLess(result['maximum_charge_drift'],1e-8)
        self.assertGreater(result['minimum_lightcone_margin'],0)
        self.assertGreater(result['minimum_gradient_margin'],0)

    def test_fixed_action_quadratic_agrees_with_parent(self):
        m=self.module()
        self.assertTrue(hasattr(m,'quadratic'),'Reconstructed quadratic action missing')
        with mp.workdps(40):
            b=m.initial();jets=m.model.coefficient_jets(b['S'],b['parameters'])
            r=m.fixed_state(b['S'],b['q'],b['z'],b['Q'],b['parameters'],b['fluids'],jets)
            actual=m.quadratic(r,7);parent=m.mixture.quadratic(b,7)
            for key in ('K','L','W','A','B','potential'):
                self.assertLess(mp.norm(actual[key]-parent[key]),mp.mpf('1e-28'))

    def test_full_roots_follow_reconstructed_action_jets(self):
        m=self.module()
        self.assertTrue(hasattr(m,'frequencies'),'Full time-dependent equations missing')
        with mp.workdps(60):
            b=m.initial();r=m.reconstruct(b['S'],b['q'],b['z'],b['Q'],b['parameters'],b['fluids'])
            f=m.frequencies(r,mp.mpf('1e14'))
            expected=sorted(mp.re(x) for x in mp.eig(r['principal']['symbol'],left=False,right=False))
            actual=sorted(mp.im(x)**2/(mp.exp(2*r['S'])*mp.mpf('1e14')) for x in f['roots'] if mp.im(x)>0)
            self.assertEqual(len(actual),3)
            self.assertLess(max(abs(x-y) for x,y in zip(expected,actual)),mp.mpf('1e-7'))
            self.assertLess(f['residual'],mp.mpf('1e-40'))

    def test_auxiliary_brackets_both_sectors(self):
        m=self.module()
        self.assertTrue(hasattr(m,'brackets'),'Actual auxiliary brackets missing')
        with mp.workdps(40):
            b=m.initial();r=m.reconstruct(b['S'],b['q'],b['z'],b['Q'],b['parameters'],b['fluids'])
            for k2 in (0,1,10000):
                pb=m.brackets(r,k2)
                self.assertLess(mp.norm(pb['matrix']+pb['matrix'].T),mp.mpf('1e-30'))
                self.assertEqual(pb['rank'],4)
                self.assertNotEqual(pb['determinant'],0)


if __name__=='__main__':unittest.main()
