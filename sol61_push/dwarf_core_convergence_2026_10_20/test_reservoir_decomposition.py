import importlib.util,unittest
from pathlib import Path
import numpy as np
p=Path(__file__).with_name('reservoir_decomposition.py')
if p.exists():
    spec=importlib.util.spec_from_file_location('reservoirs',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
else:module=None

class ReservoirTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(module,'reservoir decomposition missing')

    def test_group_orbital_motion_is_not_called_spin(self):
        x=np.array([[9.,0,0],[11.,0,0],[-9.,0,0],[-11.,0,0]])
        v=np.array([[0.,4,0],[0.,4,0],[0.,-4,0],[0.,-4,0]])
        m=np.ones(4);phi=-np.arange(1.,5.)
        out=module.decompose(x,v,m,phi,dict(right=np.array([1,1,0,0],bool),left=np.array([0,0,1,1],bool)))
        self.assertAlmostEqual(out['groups']['right']['Jspin'][2],0)
        self.assertAlmostEqual(out['groups']['right']['Jcentre'][2],80)
        self.assertAlmostEqual(out['global']['Jinternal'][2],160)
        self.assertLess(out['closure']['J_norm'],1e-12)
        self.assertLess(abs(out['closure']['energy']),1e-12)

    def test_translation_and_boost_preserve_internal_partition(self):
        rng=np.random.default_rng(918);x=rng.normal(size=(17,3));v=rng.normal(size=(17,3));m=rng.uniform(.2,4,17);phi=-rng.uniform(2,5,17)
        groups=dict(a=np.arange(17)<8,b=np.arange(17)>=8)
        a=module.decompose(x,v,m,phi,groups);b=module.decompose(x+[1e4,-2e4,3e4],v+[100,-200,300],m,phi,groups)
        for name in groups:
            for key in ('Jspin','Jcentre','Kwithin','Kcentre','Uallocated'):
                np.testing.assert_allclose(a['groups'][name][key],b['groups'][name][key],rtol=1e-10,atol=1e-9)

if __name__=='__main__':unittest.main()
