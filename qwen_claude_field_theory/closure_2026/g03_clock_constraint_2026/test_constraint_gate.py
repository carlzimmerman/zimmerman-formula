import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import sympy as sp

HERE=Path(__file__).resolve().parent
gate=None
if (HERE/'constraint_gate.py').exists():
    spec=importlib.util.spec_from_file_location('constraint_gate',HERE/'constraint_gate.py')
    gate=importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)


class ConstraintTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gate,'same-action constraint admission not implemented')

    def test_exact_legendre_identity_and_zero_field_derivatives(self):
        # Wrong factors of two or a changed kernel must fail.
        r=gate.legendre_identity()
        self.assertEqual(r['stationarity_residual'],0)
        self.assertEqual(r['on_shell_identity_residual'],0)
        self.assertEqual(r['primitive_hessian_zero'],0)
        self.assertEqual(r['eliminated_hessian_limit'],sp.oo)
        self.assertEqual(r['inverse_holder_limit'],1)

    def test_adm_legendre_transform_before_branch_substitution(self):
        # Reversing the ADM kinetic sign must fail.
        r=gate.adm_kinetic()
        self.assertTrue(all(v==0 for v in r['momentum_residuals']))
        self.assertEqual(r['Hamiltonian_residual'],0)
        self.assertEqual(r['lapse_primary'],0)
        self.assertEqual(r['lapse_equation_residual'],0)

    def test_lifted_scalar_brackets_are_derived_and_preserved(self):
        # A guessed rank, omitted p_v, or dropped preservation equation fails.
        r=gate.lifted_scalar()
        self.assertEqual(r['PB']+r['PB'].T,sp.zeros(len(r['constraints'])))
        self.assertEqual(r['PB'].rank(),r['second_class'])
        self.assertTrue(all(v==0 for v in r['preservation_residuals']))
        self.assertEqual(r['scalar_dof'],r['parent_scalar_dof'])
        self.assertEqual(r['reduced_action_residual'],0)
        self.assertEqual(r['v_constraint_residual'],0)
        self.assertEqual(r['u_constraint_residual'],0)

    def test_filter_inverse_and_zero_gain_are_not_silently_identified(self):
        # Gaussian gain is positive, not an exactly truncated zero mode.
        r=gate.lifted_scalar()
        self.assertEqual(r['flux_solution_residual'],0)
        self.assertGreater(r['second_class'],r['zero_gain_PB_rank'])
        self.assertTrue(all(v==0 for v in r['multiplier_substitution_residuals']))

    def test_nonzero_constraint_pairing_has_an_exact_determinant(self):
        # Missing u/v cross-pairing or a sign error changes this determinant.
        r=gate.lifted_scalar()
        self.assertIn('constraint_pairing_det',r)
        A,k,sigma=sp.symbols('A k sigma',positive=True)
        self.assertEqual(sp.simplify(r['constraint_pairing_det']-8*A**3*k**4*sigma**2),0)

    def test_homogeneous_irregular_constraint_is_not_a_gauge_generator(self):
        # Null linearization cannot certify a nonlinear gauge orbit.
        r=gate.homogeneous_flux()
        self.assertEqual(r['constraint_jacobian_at_zero'],0)
        self.assertEqual(r['constraint_over_v2_limit'],1)
        self.assertEqual(r['primitive_over_v3_limit'],sp.Rational(2,3))
        self.assertEqual(r['GR_homogeneous_dof'],0)
        self.assertIsNone(r['full_homogeneous_flux_Dirac_count'])

    def test_clock_cap_constraints_and_normal_derivative_are_satisfied(self):
        # Hamiltonian sign or an assumed K=0 restriction must fail.
        r=gate.branch_admission()
        self.assertEqual(r['Hamiltonian_constraint'],0)
        self.assertEqual(r['Hamiltonian_preservation'],0)
        self.assertEqual(r['momentum_constraint'],0)
        self.assertTrue(all(v==0 for v in r['ADM_evolution_residuals']))
        self.assertTrue(all(v==0 for v in r['auxiliary_equation_residuals']))
        self.assertNotEqual(r['expansion'],0)

    def test_clock_only_refoliation_changes_the_off_shell_action(self):
        # a_mu=0 along solutions is not arbitrary refoliation invariance.
        r=gate.refoliation_check()
        self.assertEqual(r['acceleration_residual'],0)
        self.assertEqual(r['action_coefficient_residual'],0)
        self.assertEqual(r['stationary_refoliation_coefficient'],0)
        self.assertGreater(float(r['time_varying_refoliation_example']),0)

    def test_cli_does_not_certify_full_geometric_closure(self):
        with tempfile.TemporaryDirectory() as folder:
            r=subprocess.run([sys.executable,'-B',str(HERE/'constraint_gate.py'),
                '--output-dir',folder,'--require-closed'],capture_output=True,text=True)
            self.assertEqual(r.returncode,2,r.stdout+r.stderr)
            result=json.loads((Path(folder)/'results.json').read_text())
            self.assertEqual(result['theory_status'],'OPEN')
            self.assertTrue(all(c['passed'] for c in result['checks']))


if __name__=='__main__':
    unittest.main()
