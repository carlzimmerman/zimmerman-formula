import importlib.util
import unittest


class SourcedBackground(unittest.TestCase):
    def test_frozen_coefficients_preserve_constraints_with_matter(self):
        self.assertIsNotNone(importlib.util.find_spec('background_evolve'),
                             'missing sourced background evolution')
        from background_evolve import evolve
        result=evolve(.002)
        self.assertLess(result['max_friedmann_residual'],1e-9)
        self.assertLess(result['max_clock_residual'],1e-9)
        self.assertLess(result['max_relative_dust_charge_drift'],1e-9)
        self.assertLess(result['max_relative_radiation_charge_drift'],1e-9)
        self.assertGreater(result['min_clock_rate'],0.)
        self.assertGreater(result['min_H'],0.)


if __name__=='__main__':unittest.main()
