"""Dust is a conserved particle source, not canonical massless scalar matter."""
import importlib.util
import unittest
import mpmath as mp
import ic14_matter_square as original


class DustResponseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 50

    def model(self):
        self.assertIsNotNone(importlib.util.find_spec('ic15_dust_response'))
        return __import__('ic15_dust_response')

    def test_square_dust_fold_solves_both_equations_without_assuming_rank_loss(self):
        model = self.model()
        fold = model.square_dust_fold('.1')
        self.assertLess(abs(fold['constraint']), mp.mpf('1e-40'))
        self.assertLess(abs(fold['Lzz']), mp.mpf('1e-40'))
        self.assertGreater(abs(mp.det(fold['canonical_auxiliary_bracket'])), 1)
        self.assertLess(abs(fold['reduced_clock_momentum_hessian']), mp.mpf('1e-40'))
        self.assertFalse(fold['inside_original_chart'])

    def test_repaired_axes_have_regular_unique_positive_roots(self):
        model = self.model()
        for density in ('0', '.001', '.1', '1', '100', '1000000'):
            for source in ('b', 'Y'):
                bg = model.axis_state('.1', **{source:density})
                self.assertGreater(bg['z'], 0)
                self.assertLess(abs(bg['constraint']), mp.mpf('1e-30'))
                self.assertLess(bg['Lzz'], 0)

    def test_repair_preserves_vacuum_and_has_healthy_local_clock_samples(self):
        model = self.model()
        for S in ('.03', '.05', '.1', '.2'):
            zero = model.axis_state(S)
            ref = original.state(S, 0)
            self.assertLess(abs(zero['pressure']-ref['pressure']), mp.mpf('1e-40'))
            self.assertLess(abs(zero['K'][0,0]-ref['K'][0,0]), mp.mpf('1e-35'))
            for b in ('.001', '.01'):
                bg = model.axis_state(S, b=b)
                self.assertGreater(bg['M'][0,0], 0)
                self.assertGreater(bg['D'][0,0], 0)
                self.assertGreater(bg['K'][0,0], bg['D'][0,0])
                self.assertGreater(abs(mp.det(bg['canonical_auxiliary_bracket'])), 1)

    def test_implicit_clock_jets_match_raw_velocity_hessian(self):
        model = self.model()
        bg = model.axis_state('.1', b='.01')
        point = (mp.sqrt(2*bg['X']), bg['z'])
        density = lambda v,z:model.raw(-mp.log(v),z,b='.01')
        H = mp.matrix([[mp.diff(density,point,(2,0)),mp.diff(density,point,(1,1))],
                       [mp.diff(density,point,(1,1)),mp.diff(density,point,(0,2))]])
        self.assertLess(abs(bg['K'][0,0]-(H[0,0]-H[0,1]**2/H[1,1])), mp.mpf('1e-30'))

    def test_simultaneous_sources_are_a_separate_raw_root_obstruction(self):
        model = self.model()
        witness = model.mixed_degeneracy('.1')
        self.assertGreater(witness['b'], 0)
        self.assertGreater(witness['Y'], 0)
        self.assertLess(abs(witness['constraint']), mp.mpf('1e-40'))
        self.assertLess(abs(witness['Lzz']), mp.mpf('1e-40'))
        with self.assertRaises(ValueError):
            model.axis_state('.1', b=1, Y=1)

    def test_dust_root_regular_does_not_mean_high_density_clock_health(self):
        bg = self.model().axis_state('.1', b='100')
        self.assertLess(bg['Lzz'], 0)
        self.assertLess(bg['D'][0,0], 0)
        self.assertFalse(bg['healthy_clock_probe'])

    def test_covariant_source_and_potential_identities(self):
        model = self.model()
        self.assertTrue(all(v == 0 for v in model.identities().values()))
        with self.assertRaises(ValueError):model.axis_state('.1',b=-1)

    def test_failed_exact_identity_controls_exit_status_without_rejecting_negative_controls(self):
        model = self.model()
        self.assertTrue(hasattr(model, 'completion_status'))
        result = model.report()
        self.assertTrue(any(not row['healthy_clock_probe'] for row in result['repaired_axes']))
        self.assertEqual(model.completion_status(result), 0)
        self.assertEqual(model.completion_status(result, require_full_closure=True), 2)
        failed = dict(result, exact_checks=dict(result['exact_checks'], dust_monotonicity=False))
        self.assertEqual(model.completion_status(failed), 1)
        self.assertEqual(model.completion_status(failed, require_full_closure=True), 1)


if __name__ == '__main__':
    unittest.main()
