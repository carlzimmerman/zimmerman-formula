import unittest
import sympy as s
try:
    import metric_principal as target
except ModuleNotFoundError:
    target = None


class MetricPrincipalTests(unittest.TestCase):
    def require_module(self):
        self.assertIsNotNone(target, "metric principal implementation is missing")

    def test_linearized_einstein_annihilates_coordinate_variations(self):
        self.require_module()
        r=target.einstein()
        self.assertEqual(r['gauge_identity'], s.zeros(10,4))

    def test_computed_metric_kernel_has_only_tensor_waves(self):
        self.require_module()
        samples=target.metric_ranks()
        self.assertEqual(samples['null']['kernel_minus_gauge'],2)
        self.assertEqual(samples['timelike']['kernel_minus_gauge'],0)
        self.assertEqual(samples['spacelike']['kernel_minus_gauge'],0)

    def test_harmonic_reduction_is_trace_reversed_wave_operator(self):
        self.require_module()
        self.assertEqual(target.einstein()['harmonic_identity'],s.zeros(4))

    def test_matter_metric_couplings_are_lower_differential_order(self):
        self.require_module()
        r=target.matter()
        self.assertEqual(r['block_degrees'],{'metric':0,'mixed':1,'scalar':2})
        self.assertTrue(r['leading_metric_free'])
        self.assertEqual(r['scalar_difference'],s.zeros(2))


if __name__=='__main__':
    unittest.main()
