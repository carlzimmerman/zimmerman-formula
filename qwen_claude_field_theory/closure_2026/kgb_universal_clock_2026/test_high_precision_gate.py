import unittest
import numpy as np
import mpmath as mp


class PrecisionTests(unittest.TestCase):
    def test_zero_next_control_sectors(self):
        import high_precision_gate as h
        zero=mp.matrix([0,0])
        j,err=h.next_control(zero,zero)
        self.assertEqual(j,0);self.assertEqual(mp.norm(err),0)
        j,err=h.next_control(mp.matrix([1,0]),zero)
        self.assertIsNone(j);self.assertEqual(mp.norm(err),1)
        j,err=h.next_control(zero,mp.matrix([0,1]))
        self.assertEqual(j,0);self.assertEqual(mp.norm(err),0)

    def test_zero_but_not_negative_field_determinant_rejected(self):
        import high_precision_gate as h
        with mp.workdps(40):
            with self.assertRaises(ValueError):h.check_map(mp.mpf('1.05'),mp.mpf('.525'),mp.mpf('.5'))
            h.check_map(mp.mpf('2'),mp.mpf('.525'),mp.mpf('.5'))

    def test_extrapolation_outside_coordinate_branch_rejected(self):
        import high_precision_gate as h
        with mp.workdps(40):
            theta=[mp.log(mp.mpf(x)) for x in ('4.3759759833e20','.1000309635','1.25e9')]
            with self.assertRaises(ValueError):h.pair(theta,mp.mpf('100'))

    def test_independent_closed_inverse(self):
        import high_precision_gate as h
        from structure import closed_inverse as c
        with mp.workdps(40):
            args=[mp.mpf(x) for x in ('1e-6','.1','.5','1.28e-7','-.0075','.525')]
            a=h.normalized(*args);b=c.normalized(*map(float,args))
            for key in ('P','kappa','gamma','W','H'):
                self.assertAlmostEqual(float(a[key])/b[key],1.,places=11)

    def test_first_curvature_parts(self):
        import high_precision_gate as h
        import reduced_match as r
        with mp.workdps(40):
            for a in r.pair(np.log([1.5,.15,.128])):
                args=[mp.mpf(str(a[k])) for k in ('eps','y','X','U','w','F')]
                A,B=h.parts(h.normalized(*args));A0,B0=r.curvature_parts(a)
                np.testing.assert_allclose(list(map(float,A)),A0,rtol=1e-10)
                np.testing.assert_allclose(list(map(float,B)),B0,rtol=1e-10)

    def test_shared_control_next_preservation(self):
        import high_precision_gate as h
        with mp.workdps(30):
            N=mp.matrix([2,4]);B=mp.matrix([-1,-2])
            j,res=h.next_control(N,B)
            self.assertEqual(j,2);self.assertEqual(mp.norm(res),0)
            _,res=h.next_control(mp.matrix([2,3]),B)
            self.assertGreater(mp.norm(res),mp.mpf('.1'))


if __name__=='__main__':unittest.main()
