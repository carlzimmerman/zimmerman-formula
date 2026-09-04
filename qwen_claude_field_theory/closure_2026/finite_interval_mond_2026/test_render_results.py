"""Keep scientific plot inputs tied to measured rather than predicted values."""
import importlib.util
from pathlib import Path
import unittest


class PlotInputTests(unittest.TestCase):
    def test_payload_preserves_empirical_prediction_difference(self):
        path = Path(__file__).with_name('render_results.py')
        self.assertTrue(path.exists(), 'plot implementation missing')
        spec = importlib.util.spec_from_file_location('render_results', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sample = {'scenarios': {'primary': {'rows': [
            {'observed_D_J_dex': [.2, .1], 'predicted_D_J_dex': {'mu_exp': [.7, -.2]},
             'covariance_D_J_dex2': [[.04, 0], [0, .01]]}], 'summary': {'galaxies': 1}}}}
        x, y, error, summary = module.plot_payload(sample)
        self.assertEqual(x.tolist(), [[.7, -.2]])
        self.assertEqual(y.tolist(), [[.2, .1]])
        self.assertEqual(error.tolist(), [[.2, .1]])
        self.assertEqual(summary['galaxies'], 1)
        sample['scenarios']['primary']['rows'] = []
        with self.assertRaises(ValueError):
            module.plot_payload(sample)


if __name__ == '__main__':
    unittest.main()
