import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest
import numpy as np

HERE=Path(__file__).resolve().parent
gate=None
if (HERE/'tidal_relation.py').exists():
    spec=importlib.util.spec_from_file_location('tidal_relation',HERE/'tidal_relation.py')
    gate=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)


class TidalTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gate,'tidal computation not implemented')

    def test_exact_angular_and_kernel_identities(self):
        self.assertTrue(all(v=='0' for v in gate.symbolic_checks().values()))

    def test_constitutive_jacobian_from_nonlinear_flux(self):
        # Wrong inverse kernel or derivative must fail the finite difference.
        for y in [0.03,0.5,1,2.5,5]:
            self.assertLess(gate.tangent_error(y),2e-7)

    def test_radial_normalization_against_exact_integrals(self):
        # Catches missing 2pi factors, an omitted outer filter, or wrong xi.
        for xi in [0.4,1,2.5]:
            self.assertAlmostEqual(gate.radial_factor('gaussian',xi,0)*8*np.pi**1.5*xi**3,1,delta=1e-11)
            self.assertAlmostEqual(gate.radial_factor('helmholtz',xi,0)*8*np.pi*xi**3,1,delta=1e-11)

    def test_independent_angular_hessian_and_rotation(self):
        e=np.array([1.,2.,3.]); e/=np.linalg.norm(e)
        for kernel in ['gaussian','helmholtz','quartic']:
            for y in [0.03,1,2.5,4]:
                H=gate.hessian_numeric(y,kernel,0.7,0.3,e)
                expected=gate.hessian_formula(y,kernel,0.7,0.3,e)
                self.assertLess(np.linalg.norm(H-expected)/np.linalg.norm(expected),2e-12)
                self.assertLess(gate.identity_error(H,y,e),2e-12)

    def test_ratio_limits_and_regular_trace_zero(self):
        # Catches treating the ratio pole as a divergent physical Hessian.
        H=gate.hessian_numeric(1e-7,'gaussian',1,0)
        self.assertAlmostEqual(gate.observables(H)[0]/np.trace(H),2/25,delta=1e-7)
        H=gate.hessian_numeric(1,'gaussian',1,0)
        self.assertAlmostEqual(gate.observables(H)[0]/np.trace(H),1/5,delta=1e-12)
        root=gate.thresholds()['trace_zero_y']
        H=gate.hessian_numeric(root,'gaussian',1,0)
        self.assertTrue(np.isfinite(H).all())
        self.assertLess(abs(np.trace(H))/np.linalg.norm(H),1e-10)
        self.assertLess(gate.identity_error(H,root),1e-11)

    def test_cli_serializes_all_results(self):
        # Catches numerical scalar types breaking the reproducibility outputs.
        result=subprocess.run([sys.executable,str(HERE/'tidal_relation.py')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__':
    unittest.main()
