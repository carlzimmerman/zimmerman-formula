from pathlib import Path
import unittest
import numpy as np


class DwarfTests(unittest.TestCase):
    def test_predictor_and_virial_checks(self):
        self.assertTrue(Path(__file__).with_name('isolated.py').exists(),'KT37 dwarf implementation absent')
        import isolated as m
        d=next(x for x in m.sample() if x['name']=='Fornax')
        row=m.predict(d,'canonical',.3,1000)
        self.assertEqual(len(row['sigma']),41)
        self.assertLess(row['checks']['maximum_virial_relative_difference'],1e-3)
        self.assertLess(row['checks']['newton_relative_error'],1e-3)
        plain=m.predict(d,'canonical',0.,1000)
        np.testing.assert_allclose(plain['sigma'],plain['plain_sigma'],rtol=2e-12)


if __name__=='__main__':unittest.main()
