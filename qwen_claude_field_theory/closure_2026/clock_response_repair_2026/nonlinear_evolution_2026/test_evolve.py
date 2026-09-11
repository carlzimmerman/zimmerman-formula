#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest
import numpy as np

HERE=Path(__file__).resolve().parent


class EvolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=HERE/"evolve.py"

    def load(self):
        self.assertTrue(self.path.exists(),"full-gradient evolution is not implemented")
        spec=importlib.util.spec_from_file_location("clock_evolve",self.path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def test_zero_source_evolves_original_background(self):
        m=self.load();run=m.evolve(0.,.3,tend=.005,dt=.001,points=65,outer=3.)
        end=run["state"];bg=run["model"].background(.005)
        for index,target in ((0,bg["a"]),(1,bg["a"]),(2,bg["H"]),(3,bg["H"]),(4,bg["q"])):
            np.testing.assert_allclose(end[index],target,rtol=2e-8,atol=2e-9)
        self.assertLess(run["snapshots"][-1]["max_clock_constraint"],1e-8)

    def test_nonzero_source_generates_clock_gradient_and_conserves_dust(self):
        m=self.load();run=m.evolve(.02,.3,tend=.005,dt=.001,points=129,outer=3.)
        self.assertGreater(np.max(abs(run["state"][5])),1e-8)
        self.assertGreater(np.max(abs(run["state"][6])),1e-8)
        self.assertLess(abs(run["snapshots"][-1]["mass_balance_relative_error"]),1e-9)
        self.assertGreater(run["snapshots"][-1]["shell_jacobian_min"],.9)

    def test_constraint_residuals_decrease_under_spatial_refinement(self):
        m=self.load();errors=[]
        for n in (129,257):
            run=m.evolve(.02,.3,tend=.02,dt=.00025,points=n,outer=3.)
            last=run["snapshots"][-1]
            errors.append([last["max_hamiltonian_constraint"],last["max_momentum_constraint"]])
        self.assertTrue(np.all(np.array(errors[1]) < .6*np.array(errors[0])),errors)

    def test_negative_dust_density_rejected(self):
        m=self.load();system=m.Evolution(.02,.3,65,3.,.01,1e-6)
        bad=system.initial.copy();bad[7,10]=-.001
        with self.assertRaises(ValueError):system.fields(0.,bad)


if __name__=="__main__":unittest.main(verbosity=2)
