import unittest
import sympy as s
import vertices


class VertexTests(unittest.TestCase):
    def test_quartic_is_derived_by_expanding_action(self):
        result = vertices.symbolic_vertices()
        self.assertTrue(all(result['checks'].values()))
        self.assertEqual(len(result['checks']), 6)

    def test_quartic_moment_is_not_square_of_mean(self):
        row = vertices.symbolic_vertices()
        self.assertEqual(row['moment_ratio'], s.Rational(3, 2))

    def test_clock_and_P_vertices_are_both_retained(self):
        row = vertices.snapshot()
        self.assertLess(row['s_WYY'], 0)
        self.assertGreater(row['PXX_plus_sWYY'], 0)
        self.assertLess(row['jet_archive_max_error'], 1e-12)

    def test_exact_nonlinear_flux_converges_to_cubic_vertex(self):
        rows = vertices.flux_controls()
        self.assertLess(rows[-1]['relative_error'], 2e-4)
        self.assertLess(rows[-1]['relative_error'], rows[0]['relative_error']/10)
        self.assertLess(max(row['quadrature_difference'] for row in rows), 1e-9)

    def test_linear_control_has_no_third_harmonic(self):
        self.assertLess(abs(vertices.linear_flux_third()), 1e-14)


if __name__ == '__main__':
    unittest.main()
