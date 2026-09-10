import unittest
import mpmath as mp
import sector


class ConstantSectorTests(unittest.TestCase):
    def test_exact_original_principal_homogeneity(self):
        self.assertTrue(all(value==0 for value in sector.symbolic_scaling()))
        self.assertEqual(sector.symbolic_angular_identity(),0)

    def test_numeric_normalizations_do_not_change_signs(self):
        with mp.workdps(55):
            base=sector.model.evaluate('1e-6','3','.5','.525')
            scaled=sector.model.evaluate('1e-6','3','2','2.1')
            for key in sector.PRINCIPAL_KEYS:
                self.assertLess(abs(4*scaled[key]-base[key])/max(abs(base[key]),1),mp.mpf('1e-35'))

    def test_independent_angular_condition(self):
        with mp.workdps(60):
            for y in ('.03','1','3','10'):
                condition=sector.angular_condition('1e-6',y)
                row=sector.model.evaluate('1e-6',y)
                self.assertLess(abs(condition-mp.mpf('.5')*row['angular'])/max(abs(condition),1),mp.mpf('1e-40'))
                self.assertGreater(condition,0)

    def test_true_inverse_boundaries_bracketed(self):
        with mp.workdps(50):
            roots=sector.boundaries()
            delta=mp.mpf('1e-4')
            self.assertLess(sector.zshape('1e-6',roots['zero_z']-delta),0)
            self.assertGreater(sector.zshape('1e-6',roots['zero_z']+delta),0)
            self.assertGreater(sector.enthalpy('1e-6',roots['zero_enthalpy']-delta),0)
            self.assertLess(sector.enthalpy('1e-6',roots['zero_enthalpy']+delta),0)


if __name__=='__main__':unittest.main()
