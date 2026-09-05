"""Behavior tests: each checks a variation, limit, or independent integral."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

import numpy as np
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('onset_action_gate', HERE / 'onset_action_gate.py')
gate = None
if (HERE / 'onset_action_gate.py').exists():
    gate = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(gate)


class OnsetActionTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gate, 'the approved variational/onset computation is not implemented')

    def test_exact_inverse_not_rar(self):
        # Catches silently replacing the implicit exponential law with nu_RAR.
        for y in [1e-8, 0.02, 0.7, 1.0, 3.0, 30.0]:
            s = y * (-np.expm1(-y))
            self.assertAlmostEqual(gate.inverse_y(s) / y, 1.0, delta=3e-12)
        self.assertEqual(gate.inverse_y(0.0), 0.0)
        with self.assertRaises(ValueError):
            gate.inverse_y(-1.0)

    def test_dual_primitive_and_gaussian_coefficient_symbolically(self):
        # Catches wrong Legendre transform factors and central 1/3 factors.
        identities = gate.symbolic_checks()
        self.assertTrue(all(v == '0' for k, v in identities.items() if k.endswith('_residual')))
        self.assertEqual(identities['gaussian_central_coefficient'], '2/9')

    def test_action_variation_requires_adjoint_filter(self):
        # Removing outer S must fail the action gradient check.
        for kind in ['gaussian', 'helmholtz']:
            result = gate.variation_check(kind)
            self.assertLess(result['finite_difference_relative_error'], 2e-7)
            self.assertGreater(result['missing_adjoint_relative_error'], 1e-3)

    def test_source_response_reciprocity(self):
        # Catches claiming the one-filter law is a reciprocal energy response.
        for kind in ['gaussian', 'helmholtz']:
            result = gate.reciprocity_check(kind, 12)
            self.assertGreater(result['one_filter_relative_antisymmetry'], 1e-3)
            self.assertLess(result['action_relative_antisymmetry'], 1e-12)
            self.assertLess(result['finite_difference_response_error'], 2e-7)
            self.assertEqual(result['laplacian_nullity'], 1)

    def test_filter_mass_fractions_against_density_integrals(self):
        # Catches kernel normalization, Gaussian width, small-x cancellation.
        for x in [1e-6, 0.03, 0.8, 5.0]:
            g = quad(lambda t: np.sqrt(2/np.pi)*t*t*np.exp(-t*t/2), 0, x,
                     epsabs=1e-28, epsrel=2e-12)[0]
            h = quad(lambda t: t*np.exp(-t), 0, x, epsabs=1e-28, epsrel=2e-12)[0]
            self.assertAlmostEqual(gate.mass_fraction(x, 'gaussian') / g, 1, delta=3e-12)
            self.assertAlmostEqual(gate.mass_fraction(x, 'helmholtz') / h, 1, delta=3e-12)

    def test_one_filter_onset_against_original_force(self):
        # Tests the exact root against forces, not a second use of its equation.
        for kind in ['gaussian', 'helmholtz']:
            for eps in [1e-12, 1e-6, 1.0, 100.0]:
                x = gate.one_filter_onset(eps, kind)
                s = eps * gate.mass_fraction(x, kind) / x**2
                self.assertAlmostEqual(gate.phantom(s) / (eps/x**2), 1, delta=2e-10)

    def test_corrected_radial_integral_independent_angular_quadrature(self):
        # Catches a scalar-kernel convolution mistakenly used for a vector.
        for x, eps in [(0.04, 1e-8), (0.6, 1e-4), (3.0, 0.02)]:
            a = gate.filtered_phantom(x, eps)
            b = gate.filtered_phantom_angular(x, eps)
            self.assertAlmostEqual(a/b, 1, delta=2e-7)
            self.assertAlmostEqual(a/gate.filtered_phantom(x, eps, cutoff=12), 1, delta=2e-8)

    def test_sixth_power_small_mass_limit_not_fifth(self):
        # Catches retaining the phenomenological exponent after action variation.
        eps = 1e-12
        x = gate.action_onset(eps)
        self.assertAlmostEqual(x**6 / ((81/4)*eps), 1, delta=0.001)
        self.assertAlmostEqual(gate.filtered_phantom(x, eps)/(eps/x**2), 1, delta=2e-9)
        x2 = gate.action_onset(100*eps)
        self.assertAlmostEqual(x2/x, 100**(1/6), delta=0.003)

    def test_far_field_and_high_acceleration_recovery(self):
        # Catches smoothing the baryonic Newtonian field and failure of mu -> 1.
        for s in [30.0, 100.0]:
            self.assertLess(abs(gate.phantom(s)), 4e-12)
        x, eps = 100.0, 1e-4
        total = eps/x**2 + gate.filtered_phantom(x, eps)
        self.assertAlmostEqual(total*x/np.sqrt(eps), 1, delta=0.001)

    def test_full_run_serializes_reproducible_results(self):
        # Catches NumPy scalars leaking into JSON and CLI-only failures.
        result = subprocess.run([sys.executable,str(HERE/'onset_action_gate.py')],
                                capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        payload = json.loads((HERE/'results.json').read_text())
        self.assertEqual(len(payload['onset_rows']),9)
        self.assertTrue(all(payload['checks'].values()))


if __name__ == '__main__':
    unittest.main()
