"""Independent controls for the same-action two-field dust principal symbol."""
import importlib
import importlib.util
import unittest
import mpmath as mp


class DustPrincipalTests(unittest.TestCase):
    def setUp(self):
        mp.mp.dps=70
        self.assertIsNotNone(importlib.util.find_spec('ic17_dust_principal'),
                             'Missing same-action dust principal derivation')
        self.m=importlib.import_module('ic17_dust_principal')

    def test_raw_velocity_and_auxiliary_schur_identities(self):
        self.assertTrue(all(value==0 for value in self.m.identities().values()))

    def test_direct_reduced_pressure_velocity_hessian(self):
        b=self.m.state('.1')
        v,t=mp.sqrt(2*b['X']),mp.sqrt(2*b['Y'])
        def lagrangian(v,t):
            return self.m.background.action.build()['evaluate'](-mp.log(v),mp.log(t),mp.mpf('1e-5'))[0]
        for i,j in ((0,0),(0,1),(1,1)):
            orders=tuple(int(k==i)+int(k==j) for k in range(2))
            actual=mp.diff(lagrangian,(v,t),orders)
            self.assertLess(abs(actual-b['K'][i,j])/(1+abs(actual)),mp.mpf('1e-55'))

    def test_two_sound_speeds_not_single_clock_probe(self):
        b=self.m.state('.1')
        speeds=b['speed_squared']
        self.assertEqual(len(speeds),2)
        self.assertAlmostEqual(float(speeds[0]),.00015738275,places=10)
        self.assertAlmostEqual(float(speeds[1]),.22114548,places=7)
        self.assertTrue(b['admissible'])
        self.assertEqual(b['auxiliary_rank'],4)

    def test_requested_51_state_grid(self):
        result=self.m.report()
        self.assertEqual(result['scan']['samples'],51)
        self.assertEqual(result['scan']['failed_samples'],0)
        self.assertTrue(all(result['checks'].values()))
        self.assertEqual(self.m.completion_status(result),0)
        self.assertEqual(self.m.completion_status(result,True),2)

    def test_failed_checks_cannot_claim_success(self):
        sample={'checks':{'symbolic':True},'scan':{'failed_samples':0}}
        self.assertEqual(self.m.completion_status(sample,True),2)
        sample['checks']['symbolic']=False
        self.assertEqual(self.m.completion_status(sample),1)
        self.assertEqual(self.m.completion_status(sample,True),1)
        sample['checks']['symbolic']=True
        sample['scan']['failed_samples']=1
        self.assertEqual(self.m.completion_status(sample),1)

    def test_relative_flow_has_complex_pair_not_a_health_pass(self):
        self.assertTrue(hasattr(self.m,'relative_flow'), 'Missing relative-flow principal falsification')
        row=self.m.relative_flow('.1','.1')
        self.assertEqual(row['complex_root_count'],2)
        self.assertFalse(row['hyperbolic'])
        self.assertTrue(row['time_kinetic_positive'])
        self.assertLess(row['maximum_normalized_determinant_residual'],mp.mpf('1e-55'))
        self.assertEqual(self.m.relative_flow('.1','0')['complex_root_count'],0)

    def test_bad_principal_has_regular_local_adm_constraint_patch(self):
        self.assertTrue(hasattr(self.m,'local_constraint_witness'), 'Missing ADM constraint embedding')
        row=self.m.local_constraint_witness()
        self.assertTrue(row['local_patch_regular'])
        self.assertAlmostEqual(float(row['rho']),3.0147594526108043,places=12)
        self.assertAlmostEqual(float(row['rho_X']),-531.5105429344,places=7)
        for key in ('hamiltonian_residual','momentum_residual','differentiated_hamiltonian_residual'):
            self.assertLess(abs(row[key]),mp.mpf('1e-55'))


if __name__=='__main__':
    unittest.main()
