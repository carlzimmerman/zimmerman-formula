import unittest
import numpy as np
import stress_audit as a


class StressTests(unittest.TestCase):
    def test_all_ten_inverse_metric_directions(self):
        result=a.derive()
        self.assertEqual(len(result['variations']),10)
        self.assertTrue(all(x['passed'] for x in result['variations']))
        self.assertEqual(sum(x['inverse_metric_multiplicity']==2 for x in result['variations']),6)

    def test_repeated_eigenvalues_and_proxy_identity(self):
        self.assertTrue(a.derive()['checks']['two_transverse_mixed_eigenvalues_L'])
        self.assertTrue(a.derive()['checks']['transverse_proxy_zero_adds_third_L_eigenvalue'])

    def test_frozen_reference_is_not_physical_velocity(self):
        j=a.action_jets(2.,.25,.1,1.,.8,.01)
        self.assertAlmostEqual(j['reference_margin'],1.5)
        self.assertNotAlmostEqual(j['P'],0.)
        self.assertEqual(a.action_jets(2.,.25,.1,1.,1.,0.)['P'],0.)

    def test_explicit_metric_density_checks_all_components(self):
        U,d,ell,qbar,Q,Y,s=2.,.25,.1,1.,.8,.01,1.2
        T,_=a.stress(a.action_jets(U,d,ell,qbar,Q,Y),Q,Y,s)
        numerical=a.finite_difference_stress(U,d,ell,qbar,Q,Y,s,1e-6)
        np.testing.assert_allclose(numerical,T,rtol=1e-7,atol=1e-8)

    def test_domain_boundary_is_rejected(self):
        with self.assertRaises(ValueError):a.action_jets(1.,1.,.1,1.,.8,.01)


if __name__=='__main__':unittest.main()
