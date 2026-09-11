import unittest
from integration_precision_probe import run


class IntegrationPrecisionTests(unittest.TestCase):
    def test_records_refinement_without_assuming_convergence(self):
        result = run(steps=(.01, .005))
        self.assertEqual(len(result['rows']), 2)
        self.assertEqual(result['full_theory_status'], 'OPEN')
        for row in result['rows']:
            self.assertGreater(row['diagnostic']['max_scaled_euler'], 0)
            self.assertLess(row['max_background_constraint'], 1e-9)
            self.assertLess(row['max_endpoint_transfer_change'], 1e-6)


if __name__ == '__main__':
    unittest.main()
