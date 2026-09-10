import unittest
import mpmath as mp
import numpy as np
import fast
from reference import logslip_reference as ref


class FastTests(unittest.TestCase):
    def test_original_matrix_and_real_directional_derivatives(self):
        cases=[('1e-6','.1','.5','.004754976244','-1533.523854','.525','3.29992587867'),
               ('2e-6','.18','.5','.00611556537','-1720','.525','3.3'),
               ('1e-3','.8','.7','.002','.12','.8','-.07')]
        for values in cases:
            with self.subTest(values=values),mp.workdps(60):
                eps,y,X,U,w,F,f=map(mp.mpf,values)
                a=ref.normalized(eps,y,X,U,w,F);actual=fast.single(*map(float,values))
                np.testing.assert_allclose([actual[k] for k in ('P','K','Gamma','W')],
                    [float(a[k]) for k in ('P','kappa','gamma','W')],rtol=2e-10)
                np.testing.assert_allclose(actual['A']+float(f)*actual['B'],
                    list(map(float,ref.first_derivatives(a,f))),rtol=2e-9)
                np.testing.assert_allclose(actual['N'],list(map(float,ref.next_derivatives(a,f))),rtol=2e-8)
                self.assertLess(abs(float(a['pt']+a['pr'])),1e-40)

    def test_shared_curvature_enters_next_preservation(self):
        with mp.workdps(50):
            values=list(map(mp.mpf,('1e-6','.1','.5','.00475','-1533','.525','3.3')))
            eps,y,X,U,w,F,f=values;j=mp.mpf('39')
            a=ref.normalized(eps,y,X,U,w,F);out=fast.single(*map(float,values))
            np.testing.assert_allclose(out['N']+float(j)*out['B'],
                list(map(float,ref.next_derivatives(a,f,j))),rtol=2e-8)


if __name__=='__main__':unittest.main(verbosity=2)
