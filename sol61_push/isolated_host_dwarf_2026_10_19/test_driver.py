"""Orthogonal bookkeeping tests, written before the experiment driver."""
import unittest
import numpy as np


class DriverTests(unittest.TestCase):
    def test_energy_and_vector_J_partition_are_galilean_invariant(self):
        from run_dwarf import ledger
        x=np.array([[1.,0.,0.],[-1.,0.,0.],[0.,2.,0.]])
        v=np.array([[0.,2.,0.],[0.,-1.,0.],[.5,0.,0.]])
        m=np.array([2.,2.,1.]); cold=np.array([True,True,False])
        a=ledger(x,v,m,cold,0.2,False)
        b=ledger(x+np.array([100.,-20.,3.]),v+np.array([12.,4.,-2.]),m,cold,0.2,False)
        self.assertAlmostEqual(a['Eint'],b['Eint'],places=11)
        np.testing.assert_allclose(a['Jint'],b['Jint'],atol=1e-11)
        self.assertAlmostEqual(a['Eint'],a['Ecold']+a['Estars'],places=12)
        np.testing.assert_allclose(np.array(a['Jcold'])+a['Jstars'],a['Jint'],atol=1e-12)
        np.testing.assert_allclose(np.array(a['Jint'])+a['Jorb'],a['Jtotal'],atol=1e-12)
        self.assertAlmostEqual(a['Etotal'],a['Eint']+a['Eorb']+a['Uhost'],places=12)

    def test_initial_dwarf_is_identical_before_host_translation(self):
        from run_dwarf import initial_conditions
        a=initial_conditions(64,16,87319,40.)
        b=initial_conditions(64,16,87319,40.)
        for i in range(4):
            np.testing.assert_array_equal(a[i],b[i])
        x,v,m,c=a[:4]
        np.testing.assert_allclose(np.average(x,axis=0,weights=m),0,atol=1e-10)
        np.testing.assert_allclose(np.average(v,axis=0,weights=m),0,atol=1e-12)
        self.assertLess(np.count_nonzero(np.linalg.norm(x[c],axis=1)<300),8)


if __name__=='__main__':
    unittest.main()
