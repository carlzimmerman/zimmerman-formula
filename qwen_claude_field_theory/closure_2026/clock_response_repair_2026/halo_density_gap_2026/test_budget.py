"""Independent arithmetic fixtures for the density/radius screening budget."""
import importlib.util
from pathlib import Path
import unittest
import sympy as s


class BudgetTests(unittest.TestCase):
    def module(self):
        path=Path(__file__).with_name('density_gap.py')
        if not path.exists():self.fail('density-gap calculation not implemented')
        spec=importlib.util.spec_from_file_location('density_gap',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def test_radius_squared_and_density_normalization(self):
        value=self.module().budget(s.Integer(2),s.Integer(3),s.Rational(1,100),s.Integer(1),s.Rational(1,10))
        self.assertEqual(value,s.Rational(37,20000))

    def test_reject_degenerate_branch(self):
        for mass,ratio in ((0,1),(1,0),(1,-1)):
            with self.assertRaises(ValueError):
                self.module().budget(1,1,1,mass,ratio)


if __name__=='__main__':unittest.main()
