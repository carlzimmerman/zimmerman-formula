import importlib.util
import unittest


class WeightedMultiplierTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic43_weighted_multiplier'))
        return __import__('ic43_weighted_multiplier')

    def test_actual_pin_variation_and_bulk_dirac_reduction(self):
        out=self.module().bulk()
        for key in ['physical_bracket_error','reduced_H_error','preservation_error']:
            self.assertEqual(out[key],0)
        self.assertEqual(self.module().repo_pin_identity(),0)

    def test_singular_multiplier_can_have_regular_positive_physical_hamiltonian(self):
        out=self.module().example()
        self.assertEqual(out['weighted_multiplier_error'],0)
        self.assertEqual(out['crossing_force_jump'],0)
        self.assertEqual(out['energy_flow_error'],0)
        self.assertTrue(out['positive_Hpp_both_sides'])

    def test_global_replacement_does_not_silently_pin_the_off_phase(self):
        out=self.module().example()
        self.assertNotEqual(out['global_replacement_error'],0)
        self.assertEqual(out['zero_phase_preservation_error'],0)

    def test_reduced_action_evolves_through_the_phase_boundary(self):
        out=self.module().orbit()
        self.assertTrue(out['solver_success'])
        self.assertGreater(len(out['crossing_times']),0)
        self.assertLess(out['relative_energy_drift'],1e-9)


if __name__=='__main__':unittest.main()
