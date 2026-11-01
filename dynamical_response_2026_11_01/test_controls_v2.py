"""Analytic controls; scientific runs use the bounded runner separately."""
import unittest
import numpy as np
from response_v2 import pulse_integral, finite_hamiltonian, krylov

class Controls(unittest.TestCase):
    def test_zero_feedback_is_identity(self):
        H=finite_hamiltonian(np.zeros((2,3),complex),np.array([-1.,1.]))
        z=np.array([1.+1j,2.,3.])
        np.testing.assert_array_equal(H.sqrt(z),z)
        self.assertEqual(H.minimum,1.)
    def test_resonant_pulse(self):
        # Zero forcing frequency and zero oscillator: integral sin² is T/2.
        t=np.array([0.,2.])
        v=pulse_integral(np.array([0.]),t,0.,2.)
        self.assertAlmostEqual(v[0,0].real,0.)
        self.assertAlmostEqual(v[0,-1].imag,-1.,places=12)

    def test_positive_and_negative_feedback(self):
        V=np.array([[.2,.3j,0.],[0.,.1,.1j]])
        signs=np.array([-1.,1.])
        H=np.eye(3)+V.conj().T@np.diag(signs)@V
        op=finite_hamiltonian(V,signs)
        z=np.array([.1+1j,.2,.3j])
        np.testing.assert_allclose(op.sqrt(op.sqrt(z)),H@z,atol=1e-13)
        np.testing.assert_allclose(op.invsqrt(op.sqrt(z)),z,atol=1e-13)
        self.assertAlmostEqual(op.minimum,np.linalg.eigvalsh(H).min(),places=12)

    def test_krylov_against_exact_oscillators(self):
        M=np.array([[1.,.2j,0.],[-.2j,-2.,.1],[0.,.1,3.]])
        b=np.array([1.,.3j,.2])
        Q,T,err=krylov(lambda x:M@x,b,3)
        np.testing.assert_allclose(Q.conj().T@Q,np.eye(3),atol=1e-12)
        np.testing.assert_allclose(Q@T@Q.conj().T,M,atol=1e-12)

if __name__=='__main__':unittest.main()
