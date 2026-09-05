import importlib.util
from pathlib import Path
import unittest
import subprocess
import sys
import warnings
import numpy as np

HERE=Path(__file__).resolve().parent
gate=None
if (HERE/'binary_frequency.py').exists():
    spec=importlib.util.spec_from_file_location('binary_frequency',HERE/'binary_frequency.py')
    gate=importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)

class BinaryTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gate,'two-body implementation missing')

    def test_exact_vector_inverse(self):
        s=np.logspace(-14,4,70); y=gate.inverse_array(s)
        self.assertLess(np.max(abs(y*(-np.expm1(-y))/s-1)),2e-13)

    def test_filtered_newtonian_hessian_by_finite_difference(self):
        x=np.array([[.001,.002,.003],[.4,-.8,.2],[5.,2.,-1.]])
        p,H=gate.newton_kernel(x)
        for j in range(3):
            h=1e-6; dx=np.eye(3)[j]*h
            numerical=(gate.newton_kernel(x+dx)[0]-gate.newton_kernel(x-dx)[0])/(2*h)
            self.assertLess(np.linalg.norm(numerical-H[:,:,j])/np.linalg.norm(H[:,:,j]),2e-7)

    def test_filtered_newtonian_kernel_at_exact_center(self):
        with warnings.catch_warnings():
            warnings.simplefilter('error',RuntimeWarning)
            p,H=gate.newton_kernel(np.zeros((1,3)))
        np.testing.assert_allclose(p,0,atol=0)
        np.testing.assert_allclose(H[0],np.eye(3)*np.sqrt(2/np.pi)/3,rtol=1e-14)

    def test_two_position_variation_and_momentum(self):
        v=gate.force_check(.02,.3,.15,n=42)
        self.assertLess(v['energy_derivative_error'],2e-5)
        self.assertLess(v['momentum_error'],2e-5)

    def test_compact_pair_total_mass_coefficient(self):
        for fraction in [.1,.5,.9]:
            a=gate.binary_accelerations(1e-6,fraction,.03,n=42)
            h=-(a[1,2]-a[0,2])/.03
            self.assertLess(abs(h/((2/9)*1e-3)-1),.003)

    def test_frequency_symbolic_derivation(self):
        self.assertTrue(all(v=='0' for v in gate.symbolic_frequency().values()))

    def test_frequency_from_full_spectral_kernel(self):
        v=gate.frequency_observables(1.,.02)
        self.assertLess(v['identity_error'],.001)
        self.assertTrue(all(v[k]>0 for k in ['Omega2','kappa2','vertical2']))

    def test_both_forces_in_external_field(self):
        M=1e-4; fraction=.3; d=.03; s=1-np.exp(-1)
        A=1/(np.e-1); B=-A
        H=M/(30*np.sqrt(np.pi))*np.diag([5*A+B,5*A+B,5*A+3*B])
        for axis in [np.array([1.,0.,0.]),np.array([0.,0.,1.])]:
            a=gate.binary_accelerations(M,fraction,d,axis=axis,external=(0,0,s))
            self.assertLess(np.linalg.norm(a[1]-a[0]+d*H@axis)/np.linalg.norm(d*H@axis),.001)
            self.assertLess(np.linalg.norm(fraction*a[0]+(1-fraction)*a[1])/np.linalg.norm(a[1]-a[0]),2e-6)

    def test_cli_serialization(self):
        result=subprocess.run([sys.executable,str(HERE/'binary_frequency.py')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

if __name__=='__main__':
    unittest.main()
