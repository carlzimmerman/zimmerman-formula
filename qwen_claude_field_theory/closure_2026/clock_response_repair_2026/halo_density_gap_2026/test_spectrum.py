"""Known flat-ball eigenvalue and refinement, not an assigned matrix rank."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np


class SpectrumTests(unittest.TestCase):
    def test_flat_ball_benchmark(self):
        path=Path(__file__).with_name('spectrum.py')
        if not path.exists():self.fail('constrained lapse spectrum not implemented')
        spec=importlib.util.spec_from_file_location('spectrum',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        errors=[]
        for n in (32,64):
            result=module.spectrum(0.,.03,n)
            expected=np.pi**2/100
            errors.append(abs(result['shifted_scaled_eigenvalues'][0]-expected))
        self.assertLess(errors[1],1e-4)
        self.assertGreater(errors[0]/errors[1],3.5)
        self.assertLess(errors[0]/errors[1],4.5)


if __name__=='__main__':unittest.main()
