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
if (HERE/'clock_caustic.py').exists():
    spec=importlib.util.spec_from_file_location('clock_caustic',HERE/'clock_caustic.py')
    gate=importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)


class CausticTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gate,'exact nonlinear clock evolution not implemented')

    def test_metric_curvature_and_geodesic_normal(self):
        # Wrong Christoffels, lapse or velocity normalization must fail.
        r=gate.symbolic_geometry()
        self.assertTrue(all(v==0 for v in r['Einstein_residuals']))
        self.assertEqual(r['normalization_residual'],0)
        self.assertTrue(all(v==0 for v in r['acceleration_residuals']))
        self.assertEqual(r['expansion_residual'],0)

    def test_actual_auxiliary_first_variation_at_zero(self):
        # Catches setting a singular q' to a guessed finite constant.
        r=gate.kernel_branch_check()
        self.assertEqual(r['q0'],0)
        self.assertEqual(r['composite_first_derivative_limit'],0)
        self.assertEqual(r['constitutive_tangent_limit'],sp.oo)

    def test_characteristic_derivatives_and_clock_reconstruction(self):
        # Wrong sign, missing gamma or clock integration constant must fail.
        r=gate.symbolic_characteristics()
        self.assertTrue(all(v==0 for key,v in r.items() if key.endswith('_residual')))
        for q in (0,.014,.07):
            r=gate.trajectory_check(q,1,.2,20,.2)
            self.assertLess(r['max_absolute_error'],2e-9)

    def test_caustic_time_matches_independent_jacobi_integration(self):
        # A preassigned time unrelated to geodesic evolution cannot pass.
        for H,p,k in ((1,.2,20),(.3,.1,30),(1,.05,100)):
            analytic=gate.caustic_time(H,p,k)
            numerical=gate.jacobi_event(H,p,k)
            self.assertAlmostEqual(analytic,numerical,delta=2e-9)

    def test_threshold_and_minkowski_limit(self):
        # Equality is not a finite-time caustic; H->0 must not divide by zero.
        self.assertIsNone(gate.caustic_time(1,.1,10))
        self.assertIsNone(gate.caustic_time(1,.1,20))
        self.assertAlmostEqual(gate.caustic_time(0,.1,20),.5,delta=1e-14)
        self.assertAlmostEqual(gate.caustic_time(1e-7,.1,20),.5,delta=1e-7)
        self.assertAlmostEqual(gate.center_invariants(2,1,.1,20)['K'],1,delta=2e-12)

    def test_invariant_clock_focusing_not_metric_curvature(self):
        # Catches merely testing a coordinate Jacobian with no scalar invariant.
        r=gate.symbolic_focusing()
        self.assertEqual(r['raychaudhuri_residual'],0)
        self.assertEqual(r['caustic_pole_residue'],-1)
        tc=gate.caustic_time(1,.1,30)
        a=gate.center_invariants(tc-.01,1,.1,30)
        b=gate.center_invariants(tc-.001,1,.1,30)
        self.assertLess(b['K'],a['K'])
        self.assertGreater(b['leaf_R'],a['leaf_R'])
        self.assertEqual(a['spacetime_R'],b['spacetime_R'])

    def test_global_jacobian_bound_and_compact_clock_caps(self):
        # Catches inspecting only q=0 or using a non-clock cap as the domain.
        r=gate.global_scan(1,.1,30)
        self.assertLess(r['minimum_bound_error'],2e-12)
        self.assertTrue(r['clock_cap_interval_nonempty'])
        self.assertTrue(r['cap_time_bounds_inside_regular_region'])

    def test_cli_refuses_full_theory_certificate(self):
        with tempfile.TemporaryDirectory() as folder:
            r=subprocess.run([sys.executable,'-B',str(HERE/'clock_caustic.py'),
                '--output-dir',folder,'--require-closed'],capture_output=True,text=True)
            self.assertEqual(r.returncode,2,r.stdout+r.stderr)
            data=json.loads((Path(folder)/'results.json').read_text())
            self.assertEqual(data['theory_status'],'OPEN')
            self.assertTrue(all(v['passed'] for v in data['checks']))


if __name__=='__main__':
    unittest.main()
