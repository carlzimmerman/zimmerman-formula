import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
gate = None
if (HERE / 'flrw_gate.py').exists():
    spec = importlib.util.spec_from_file_location('flrw_gate', HERE / 'flrw_gate.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)


class FLRWTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gate, 'FLRW calculation not implemented')

    def test_background_from_lapse_and_scale_variation(self):
        # Catches deleting the lapse variation or a wrong Lambda sign.
        r = gate.background_check()
        self.assertTrue(all(v == 0 for v in r['residuals']))
        self.assertNotEqual(r['wrong_hubble_residual'], 0)
        self.assertIn('aux_first_variation_limit',r)
        self.assertEqual(r['aux_first_variation_limit'],0)
        self.assertEqual(r['aux_tangent_limit'],sp.oo)
        self.assertEqual(r['q_power_limit'],sp.Rational(4,3))

    def test_adm_shift_and_time_boundary(self):
        # Catches freezing the shift, lapse or background volume factor.
        r = gate.scalar_action()
        A,H,k,z,n,b,d = [r[key] for key in ('A','H','k','z','n','b','d')]
        self.assertEqual(sp.simplify(r['raw']-r['boundary_dt']-r['L']), 0)
        self.assertEqual(sp.simplify(sp.diff(r['L'],b)-2*A**3*k*(d-H*n)),0)
        self.assertEqual(sp.simplify(sp.diff(r['L'],n,2)+6*A**3*H**2-2*A*k**2),0)

    def test_dirac_brackets_and_full_preservation(self):
        # Catches an omitted constraint, wrong PB sign or skipped multiplier.
        r = gate.dirac_sector()
        self.assertEqual(r['PB']+r['PB'].T, sp.zeros(len(r['constraints'])))
        self.assertTrue(all(v == 0 for v in r['preservation_residuals']))
        self.assertEqual(r['dof'], r['reduced_kinetic_hessian'].rank())
        for values in ((1,1,1),(2,sp.Rational(1,3),3)):
            mat = np.array(r['PB'].subs(dict(zip(r['parameters'],values))),float)
            self.assertEqual(np.linalg.matrix_rank(mat),r['second_class'])

    def test_scalar_dynamics_and_clock_density(self):
        # Catches losing the time-dependent boundary or H factors.
        r = gate.dirac_sector()
        self.assertEqual(r['reduced_eom_residual'],0)
        self.assertEqual(r['clock_conservation_residual'],0)
        self.assertTrue(r['reduced_kinetic_hessian'][0,0].is_positive)
        self.assertIn('gr_reduced_action',r)
        self.assertEqual(r['gr_reduced_action'],0)

    def test_homogeneous_chain_is_restarted(self):
        # Catches treating sine-shift variables as physical at k=0.
        r = gate.homogeneous_sector()
        self.assertTrue(all(v == 0 for v in r['preservation_residuals']))
        self.assertIn('reduced_action',r)
        self.assertEqual(r['dof'], sp.hessian(r['reduced_action'],[r['velocity']]).rank())

    def test_tensor_from_curvature(self):
        # Catches sign/normalization errors in the tensor gradient sector.
        r = gate.tensor_sector()
        self.assertEqual(sp.simplify(r['speed_squared']-1),0)
        self.assertTrue(r['kinetic'].is_positive)

    def test_vector_constraint_preservation(self):
        r = gate.vector_sector()
        self.assertTrue(all(v == 0 for v in r['preservation_residuals']))
        self.assertIn('reduced_action',r)
        self.assertEqual(r['dof'], sp.hessian(r['reduced_action'],[r['velocity']]).rank())

    def test_exact_auxiliary_variation(self):
        # Finite differences, not a Hessian assigned at the singular point.
        r = gate.auxiliary_gradient_check()
        self.assertLess(r['relative_error'],2e-6)

    def test_nonlinear_auxiliary_zero_field_limit(self):
        # Catches replacing the minimization by U=0 or a preset coefficient.
        large = gate.auxiliary_minimum(.01,.2,4,192)
        small = gate.auxiliary_minimum(.005,.2,4,192)
        for r in (large,small):
            self.assertLess(r['scaled_gradient_norm'],2e-5)
            self.assertTrue(0 < r['value_ratio'] < 1)
        self.assertLess(abs(small['value_ratio']-1),abs(large['value_ratio']-1))

    def test_cli_outputs_and_strict_status(self):
        # Catches serialization failures and accidental certification.
        with tempfile.TemporaryDirectory() as folder:
            p = subprocess.run([sys.executable,'-B',str(HERE/'flrw_gate.py'),
                                '--output-dir',folder,'--require-closed'],
                               capture_output=True,text=True)
            self.assertEqual(p.returncode,2,p.stdout+p.stderr)
            r = json.loads((Path(folder)/'results.json').read_text())
            self.assertTrue(all(row['passed'] for row in r['checks']))
            self.assertEqual(r['theory_status'],'OPEN')


if __name__ == '__main__':
    unittest.main()
