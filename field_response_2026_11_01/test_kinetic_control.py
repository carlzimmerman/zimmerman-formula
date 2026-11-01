import importlib.util
from pathlib import Path
import unittest


class KineticControl(unittest.TestCase):
    def test_exact_stretch_hessian_at_prescribed_steps(self):
        p=Path(__file__).with_name('kinetic_screen_v2.py')
        s=importlib.util.spec_from_file_location('kinetic_v2',p)
        m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
        result=m.stretch_controls()
        self.assertTrue(result['passed'],str(result))


if __name__=='__main__':unittest.main()
