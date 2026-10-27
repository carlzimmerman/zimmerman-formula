"""Regression for the separately pinned generic-vector constructor fix."""
import os
from pathlib import Path
import unittest
import numpy as np
import falcon_native
from benchmark_falcon import direct_gravity,HERE

LIBRARY=HERE.parent/'vendor'/'falcon_double_order5_fix_build_001'/'libfalcon.dylib'


class FixedOrder5Tests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(LIBRARY.is_file(), 'patched order5 library has not been built')
        os.environ['FALCON_NATIVE_LIBRARY']=str(LIBRARY)

    def test_binary64_order5_and_hardcoded_P0(self):
        info=falcon_native.backend_metadata()
        self.assertEqual(info['real_bytes'],8)
        self.assertEqual(info['expansion_order'],5)
        self.assertEqual(info['kernel'],'P0 Plummer, hardcoded')

    def test_evolved_full3D_Plummer_accuracy_and_momentum_torque_refine(self):
        state=np.load(HERE.parent/'run_pilot_gpu8k_iso'/'final.npz')
        x,m=state['x'],state['m']; ar,Ur,pr=direct_gravity(x,m,10.,threads=1)
        errors=[]
        for theta in (.3,.2,.1):
            a,U,phi=falcon_native.gravity(x,m,10.,theta=theta)
            errors.append(np.linalg.norm(a-ar)/np.linalg.norm(ar))
            self.assertLess(np.linalg.norm(phi-pr)/np.linalg.norm(pr),1.e-4)
            self.assertLess(abs(U/Ur-1.),1.e-4)
            F=m[:,None]*a
            self.assertLess(np.linalg.norm(F.sum(axis=0))/np.linalg.norm(F,axis=1).sum(),1.e-13)
            normalized_torque=np.linalg.norm(np.cross(x,F).sum(axis=0))/np.sum(np.linalg.norm(x,axis=1)*np.linalg.norm(F,axis=1))
            self.assertLess(normalized_torque,1.e-6)
        self.assertLess(errors[-1],errors[0])
        self.assertLess(errors[-1],1.e-5)


if __name__=='__main__':unittest.main()
