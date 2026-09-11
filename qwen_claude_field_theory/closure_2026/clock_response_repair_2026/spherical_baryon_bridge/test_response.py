"""Numerical infrastructure control, independent of a modified-gravity target."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np


class ResponseTests(unittest.TestCase):
    def test_radial_transform_recovers_gaussian_Newton_force(self):
        path=Path(__file__).with_name('response.py')
        self.assertTrue(path.exists(), 'missing sourced numerical response implementation')
        spec=importlib.util.spec_from_file_location('response_control',path)
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        k=np.geomspace(1e-5,300.,4097)
        # Independent Fourier Poisson solution for G=M=1 and sigma=.05.
        potential=-4*np.pi/k**2
        for radius in (.05,.15,.3):
            got=mod.radial_force(k,potential,radius,.05,1.)
            want=mod.gaussian_newton_force(radius,.05,1.,1.)
            self.assertAlmostEqual(got/want,1.,places=7)


if __name__=='__main__':unittest.main()
