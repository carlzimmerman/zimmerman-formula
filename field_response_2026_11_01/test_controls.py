"""Small independent controls for FR01 variational calculations."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np


class VariationalControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = Path(__file__).with_name('radial_stability_v2.py')
        assert p.exists(), 'radial variational implementation is not yet present'
        spec = importlib.util.spec_from_file_location('radial_stability', p)
        cls.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.m)

    def test_numpy_scalars_roundtrip_and_nonfinite_rejected(self):
        import json
        self.assertTrue(hasattr(self.m, 'json_default'), 'NumPy serialization adapter missing')
        encoded=json.dumps({'ok':np.bool_(True),'n':np.int64(6),'x':np.float64(.5)},
                           default=self.m.json_default,allow_nan=False)
        self.assertEqual(json.loads(encoded),{'ok':True,'n':6,'x':.5})
        with self.assertRaises(ValueError):
            json.dumps({'x':float('nan')},default=self.m.json_default,allow_nan=False)

    def test_local_hessian_from_energy_differences(self):
        for n, s in [(.2,.1), (2.,.4), (20.,1.)]:
            a,b,c = self.m.local_hessian(n,s)
            for dn,ds in [(1.,0.), (0.,1.), (.7,-.3)]:
                h = 2e-4
                f = self.m.local_energy
                fd = (f(n+h*dn,s+h*ds)-2*f(n,s)+f(n-h*dn,s-h*ds))/h**2
                expected = a*dn**2+2*b*dn*ds+c*ds**2
                self.assertAlmostEqual(fd/expected, 1., delta=3e-6)

    def test_reciprocal_term_mutation_is_detected(self):
        n,s,dn,ds,h = 2.,.4,.7,-.3,2e-4
        f = self.m.local_energy
        fd=(f(n+h*dn,s+h*ds)-2*f(n,s)+f(n-h*dn,s-h*ds))/h**2
        a,b,c=self.m.local_hessian(n,s)
        mutated=a*dn**2+c*ds**2
        self.assertGreater(abs(fd-mutated)/abs(fd), .1)

    def test_radial_gravity_from_enclosed_mass(self):
        from scipy.integrate import cumulative_trapezoid, simpson
        r=np.linspace(0.,1.,20001)
        n=(1-r*r)**2
        xi=r*(1+.3*r*r)
        np_=-4*r*(1-r*r)
        xip=1+.9*r*r
        q=-(np_*xi+n*(xip+2*(1+.3*r*r)))
        dm=cumulative_trapezoid(q*r*r,r,initial=0.)
        safe=np.where(r>0,r,1.)
        integral=-2.5*simpson(dm*dm/safe**2,x=r)
        local=-2.5*simpson(n*n*xi*xi*r*r,x=r)
        self.assertAlmostEqual(integral/local,1.,delta=2e-7)
        self.assertLess(abs(dm[-1]),2e-8)


if __name__ == '__main__':
    unittest.main()
