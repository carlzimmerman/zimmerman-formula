import unittest
from pathlib import Path
import importlib.util
import mpmath as mp
import numpy as np

class PressureTargetTests(unittest.TestCase):
    def module(self):
        path=Path(__file__).with_name('pressure_target.py')
        self.assertTrue(path.exists(),'new pressure-family implementation is absent')
        spec=importlib.util.spec_from_file_location('pressure_target_tests',path)
        model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
        return model

    def test_original_matrix_and_actual_derivatives(self):
        model=self.module()
        with mp.workdps(50):
            for eta in (-100,0,100):
                ref=model.reference(eta)
                args=list(map(mp.mpf,('1e-6','.1','.5','.00475','-1533','.525')))
                f=mp.mpf('3.3');j=mp.mpf('39')
                row=ref.normalized(*args);fast=model.single(*map(float,args),float(f),eta)
                np.testing.assert_allclose([fast[k] for k in ('P','K','Gamma','W')],
                    [float(row[k]) for k in ('P','kappa','gamma','W')],rtol=1e-9)
                np.testing.assert_allclose(fast['N']+float(j)*fast['B'],
                    list(map(float,ref.next_derivatives(row,f,j))),rtol=1e-8)

    def test_eta_zero_recovers_target(self):
        model=self.module()
        values=(1e-6,.1,.5,.00475,-1533,.525,3.3)
        a=model.single(*values,0);b=model.base.single(*values)
        for key in ('P','K','Gamma','W'):
            np.testing.assert_allclose(a[key],b[key],rtol=1e-9)

    def test_distinct_reference_instances_do_not_mutate(self):
        model=self.module()
        with mp.workdps(40):
            a=model.reference(0);before=a.geometry('1e-6','.1')['pr']
            b=model.reference(100)
            self.assertEqual(before,a.geometry('1e-6','.1')['pr'])
            self.assertNotEqual(before,b.geometry('1e-6','.1')['pr'])

if __name__=='__main__':unittest.main(verbosity=2)
