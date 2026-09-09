"""Check nonzero evolved deviations; a frozen initial oracle must fail."""
import unittest
import numpy as np
from ic46_two_phase_evolution import grid
from ic49_deviation_evolution import Evolution


class DeviationTests(unittest.TestCase):
    def test_derivative_includes_nonzero_deviation_and_background(self):
        e=Evolution.__new__(Evolution)
        e.nodes=7;e.count=3;e.metric_deviations={}
        x,D=grid(7,0.,1.)
        e.offset=[x,x];e.D=[D,D]
        e.coeff=np.zeros((7,4));e.coeff[2]=[1.,2.,3.,4.]
        e.background=np.zeros((2,3,7))
        e.background[:,0]=1+2*x+3*x*x+4*x**3
        delta=np.zeros_like(e.background);delta[:,0]=.01*x**3
        fields,R=e.fields(np.r_[delta.ravel(),2.])
        self.assertEqual(R,2.)
        np.testing.assert_allclose(e.derivative(0,fields[0,0]),2+6*x+12.03*x*x,atol=1e-12)
        np.testing.assert_allclose(e.derivative(0,fields[0,0],2),6+24.06*x,atol=1e-11)
        np.testing.assert_allclose(e.derivative(0,x*x),2*x,atol=1e-12)


if __name__=='__main__':unittest.main()
