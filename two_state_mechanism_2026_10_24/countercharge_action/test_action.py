import unittest
import numpy as np
from field import energy_density,lagrangian,displacement,Field
from response import oscillation,rar_limit

class ActionTests(unittest.TestCase):
    def test_legendre(self):
        for e in (.001,.1,1.,10.):
            d=displacement(np.array([e,0.,0.]))[0]
            self.assertAlmostEqual(e*d-lagrangian(e),energy_density(d),places=11)

    def test_neutral_field(self):
        f=Field(17,24.,1.5)
        r=f.solve([[-2.,0.,0.],[2.,0.,0.]],[10.,-10.])
        self.assertLess(r['gauss_relative'],2e-6)
        self.assertLess(abs(r['total_charge']),1e-10)
        self.assertGreater(r['forces'][0][0],0.)

    def test_response_energy(self):
        r=oscillation(.3,.1,10.,1e-9)
        self.assertLess(r['relative_energy_error'],1e-7)
        self.assertLess(r['min_displacement'],0.)

    def test_countercharge_limit(self):
        self.assertEqual(rar_limit(.1,.1,0.),0.)
        self.assertTrue(0<rar_limit(.1,.1,.05)<1)

if __name__=='__main__':unittest.main()
