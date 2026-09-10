import unittest
from pathlib import Path
import importlib.util
import numpy as np

class SearchTests(unittest.TestCase):
    def model(self):
        path=Path(__file__).with_name('search.py')
        self.assertTrue(path.exists(),'pressure search not implemented')
        spec=importlib.util.spec_from_file_location('tested_pressure_search',path)
        model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
        return model

    def test_zero_pressure_change_reproduces_actual_joint(self):
        m=self.model();row=m.solve(m.SEED,0)
        self.assertLess(max(abs(np.asarray(row['matching_relative']))),1e-7)
        health=m.health(row)
        self.assertFalse(health['promote'])
        self.assertTrue(all(value<0 for value in health['angular_speed_squared']))

    def test_same_pressure_not_omitted_from_elimination(self):
        m=self.model();a,b=m.pair(np.log(m.SEED),100)
        self.assertLess(abs(a['P']-b['P'])/max(abs(a['P']),1),1e-10)
        self.assertNotEqual(a['geometry']['eta'],0)

if __name__=='__main__':unittest.main(verbosity=2)
