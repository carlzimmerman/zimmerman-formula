"""Breaks caught: wrong variation, artificial ranks, missing source coupling."""
import importlib.util
import pathlib
import unittest

import mpmath as mp


class PinnedClockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = pathlib.Path(__file__).with_name('ic18_pinned_clock.py')
        cls.model = None
        if cls.path.exists():
            spec = importlib.util.spec_from_file_location('ic18', cls.path)
            cls.model = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.model)

    def require_model(self):
        self.assertIsNotNone(self.model, 'The action-derived IC18 computation is missing')
        mp.mp.dps = 60
        return self.model

    def test_exact_variations_and_canonical_schur(self):
        model = self.require_model()
        checks = model.identities()
        self.assertGreater(len(checks), 8)
        self.assertTrue(all(value == 0 for value in checks.values()), checks)

    def test_separation_does_not_hide_canonical_matter_superluminality(self):
        model = self.require_model()
        row = model.separation_control()
        self.assertAlmostEqual(float(row['canonical_speed_squared']), 9/7)
        self.assertEqual(row['canonical_superluminal'], True)
        self.assertTrue(row['dust_speed_squared'] > 0)

    def test_pin_bracket_does_not_depend_on_matter_stiffness(self):
        model = self.require_model()
        for curvature in (-1000, 0, 1000):
            row = model.pin_constraint(curvature)
            self.assertEqual(row['rank'], 4)
            self.assertAlmostEqual(float(row['determinant']), 1)
            self.assertTrue(all(v == 0 for v in row['preservation_residual']))

    def test_pole_background_is_positive_not_assigned(self):
        model = self.require_model()
        row = model.state('.1')
        self.assertTrue(0 < row['speed_squared'] < 1)
        self.assertTrue(row['energy'] > 0 and row['kinetic'] > 0)
        self.assertTrue(row['H_physical'] > 0)
        self.assertLess(abs(row['friedmann_residual']), mp.mpf('1e-50'))

    def test_relative_velocity_roots_check_direct_determinant(self):
        model = self.require_model()
        for velocity in ('0', '.1', '.9', '-.7'):
            row = model.characteristics('.1', velocity)
            self.assertTrue(row['kinetic_positive'])
            self.assertLess(row['maximum_root_residual'], mp.mpf('1e-50'))
            self.assertTrue(all(abs(mp.im(v)) < mp.mpf('1e-45') and abs(v) <= 1
                                for v in row['roots']))

    def test_pole_domain_is_not_silently_extended(self):
        model = self.require_model()
        for S in ('0', '.075', '-1'):
            with self.assertRaises(ValueError):
                model.state(S)
        with self.assertRaises(ValueError):
            model.characteristics('.1', '1')

    def test_charge_history_and_early_matter_scaling(self):
        model = self.require_model()
        result = model.history()
        self.assertLess(result['max_charge_residual'], mp.mpf('1e-45'))
        self.assertLess(abs(result['efolds_from_quadrature'] - 8), mp.mpf('1e-40'))
        self.assertGreater(result['initial_radiation_fraction'], mp.mpf('.5'))
        self.assertLess(abs(result['early_clock_dust_ratio'] - 1), mp.mpf('.01'))

    def test_strict_status_cannot_turn_local_pass_into_full_closure(self):
        model = self.require_model()
        self.assertEqual(model.completion_status({'checks': {'a': False}}, False), 1)
        self.assertEqual(model.completion_status({'checks': {'a': True}}, True), 2)

    def test_true_dust_transport_not_a_finite_pressure_substitute(self):
        model = self.require_model()
        self.assertTrue(hasattr(model, 'dust_characteristics'), 'Actual dust variation is missing')
        row = model.dust_characteristics('.1', '.1')
        self.assertEqual(row['dust_transport_factor'], 0)
        self.assertEqual(row['mixed_clock_dust_jet'], 0)
        self.assertLess(row['maximum_root_residual'], mp.mpf('1e-50'))

    def test_transition_constraint_is_varied_at_fixed_momentum(self):
        model = self.require_model()
        self.assertTrue(hasattr(model, 'transition_point'), 'Transition variation is missing')
        row = model.transition_point('.1', '.8')
        self.assertLess(abs(row['direct_derivative_residual']), mp.mpf('1e-45'))
        self.assertTrue(0 < row['eta'] < 1)

    def test_transition_rank_loss_requires_preservation_not_just_a_rank(self):
        model = self.require_model()
        self.assertTrue(hasattr(model, 'transition_fold'), 'Fold preservation is missing')
        row = model.transition_fold()
        self.assertLess(abs(row['constraint']), mp.mpf('1e-40'))
        self.assertLess(abs(row['lapse_second_derivative']), mp.mpf('1e-40'))
        self.assertGreater(abs(row['tertiary_preservation']), mp.mpf('1e-3'))


if __name__ == '__main__':
    unittest.main()
