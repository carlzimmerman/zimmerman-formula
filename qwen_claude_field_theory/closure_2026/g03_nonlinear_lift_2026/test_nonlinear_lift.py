import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import sympy as sp

HERE=Path(__file__).resolve().parent
gate=None
if (HERE/'nonlinear_lift.py').exists():
    spec=importlib.util.spec_from_file_location('nonlinear_lift',HERE/'nonlinear_lift.py')
    gate=importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)


class LiftTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gate,'nonlinear lift calculation is not implemented')

    def test_kernel_limit_from_exact_primitive(self):
        # Catches a changed kernel or wrong power/factor in the first variation.
        r=gate.symbolic_checks()
        self.assertEqual(r['flux_identity_residual'],0)
        self.assertEqual(r['flux_small_s_coefficient'],1)
        self.assertEqual(r['q_small_s_coefficient'],sp.Rational(4,3))
        self.assertEqual(r['cusp_second_derivative_jump'],4)

    def test_fourier_coefficients_against_independent_quadrature(self):
        # Wrong normalization, parity or denominator must fail.
        for n in range(1,18):
            self.assertAlmostEqual(gate.cusp_coefficient(n),gate.quadrature_coefficient(n),delta=2e-12)

    def test_exact_flux_semiconvexity_certificate(self):
        # Catches a wrong lower Hessian bound and a spurious no-solution claim.
        r=gate.symbolic_checks()
        self.assertIn('flux_derivative_minimum',r)
        self.assertEqual(sp.simplify(r['flux_derivative_minimum']+1/(1+sp.exp(2))),0)
        for amplitude in (.01,.5,1):
            self.assertGreater(np.exp(-amplitude)+float(r['flux_derivative_minimum'])*np.exp(amplitude),0)

    def test_finite_mode_cubic_target_is_not_continuum_minimum(self):
        # Catches confusing fixed-resolution epsilon limits with continuum ones.
        self.assertTrue(hasattr(gate,'leading_minimum'),'finite-mode cubic minimization missing')
        coarse=gate.leading_minimum(.5,8,2048)
        fine=gate.leading_minimum(.5,16,4096)
        self.assertLess(coarse['gradient_norm'],3e-6)
        self.assertLess(fine['gradient_norm'],3e-6)
        self.assertGreater(coarse['value'],fine['value'])
        self.assertGreater(fine['value'],gate.cubic_infimum(.5))
        exact=gate.solve_auxiliary(1e-8,.5,8,2048)
        self.assertLess(abs(exact['energy_correction']-coarse['value']),2e-6)

    def test_identity_filter_parseval_control(self):
        # Catches mistaking every filter for the Gaussian obstruction.
        r=gate.spectral_norm(0,101,'gaussian')
        self.assertAlmostEqual(10**(2*r['log10_gradient_rms']),3/8,delta=1e-9)

    def test_inverse_heat_growth_and_algebraic_control(self):
        # Catches forgetting that the required inverse filter grows, not decays.
        low=gate.spectral_norm(.5,21,'gaussian')
        high=gate.spectral_norm(.5,41,'gaussian')
        self.assertGreater(high['log10_gradient_rms']-low['log10_gradient_rms'],50)
        a=gate.spectral_norm(.5,101,'helmholtz')
        b=gate.spectral_norm(.5,201,'helmholtz')
        self.assertLess(abs(a['log10_gradient_rms']-b['log10_gradient_rms']),.002)

    def test_weighted_exact_functional_gradient(self):
        # Catches dropping lapse weights, adjoint filter or preconditioner.
        self.assertLess(gate.gradient_check()['relative_error'],2e-6)

    def test_joint_high_frequency_trial_breaks_uniform_quadratic_limit(self):
        # Catches silently treating fixed-k expansion as a uniform Hessian.
        self.assertTrue(hasattr(gate,'nonuniform_trial'),'exact variational trial missing')
        a=gate.nonuniform_trial(8,.5)
        b=gate.nonuniform_trial(20,.5)
        self.assertEqual(a['squared_gradient_term'],0)
        self.assertLess(b['log_lapse_H1_norm'],a['log_lapse_H1_norm'])
        self.assertLess(b['minimum_ratio_upper_bound'],1e-9)
        self.assertLess(abs(b['minimum_ratio_upper_bound']/b['asymptotic_upper_bound']-1),1e-8)

    def test_nonlinear_solution_has_nonzero_auxiliary_and_small_residual(self):
        # A prescribed U=0 and fake optimizer success cannot pass.
        r=gate.solve_auxiliary(.001,.5,16,1024)
        self.assertLess(r['scaled_gradient_norm'],3e-6)
        self.assertGreater(r['scaled_gradient_rms'],.5)
        self.assertLess(r['energy_correction'],0)
        self.assertLess(r['projected_flux_residual_rms'],3e-7)

    def test_cubic_energy_has_independent_variational_bounds(self):
        # Wrong Legendre coefficient or assumed minimizer fails.
        r=gate.solve_auxiliary(.0001,.5,24,2048)
        self.assertGreater(r['energy_correction'],gate.cubic_infimum(.5))
        self.assertLess(abs(r['energy_correction']/gate.cubic_infimum(.5)-1),.02)

    def test_cli_cannot_certify_full_theory(self):
        with tempfile.TemporaryDirectory() as folder:
            r=subprocess.run([sys.executable,'-B',str(HERE/'nonlinear_lift.py'),
                '--output-dir',folder,'--require-closed'],capture_output=True,text=True)
            self.assertEqual(r.returncode,2,r.stdout+r.stderr)
            data=json.loads((Path(folder)/'results.json').read_text())
            self.assertTrue(all(c['passed'] for c in data['checks']))
            self.assertEqual(data['theory_status'],'OPEN')


if __name__=='__main__':
    unittest.main()
