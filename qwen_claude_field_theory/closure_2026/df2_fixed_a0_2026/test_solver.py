"""Independent exact-limit controls for the finite-source variational solve."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

HERE=Path(__file__).resolve().parent


class SolverTests(unittest.TestCase):
    def solver(self):
        path=HERE/'solver.py'
        self.assertTrue(path.exists(), 'The action-derived finite-source solver is missing')
        spec=importlib.util.spec_from_file_location('df2_solver',path)
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        return mod

    def test_action_derivative(self):
        mod=self.solver()
        y=np.logspace(-4,2,61)
        step=1e-4*y
        numerical=(mod.primitive(y+step)-mod.primitive(y-step))/(2*step)
        np.testing.assert_allclose(numerical,2*y*mod.mu(y),rtol=2e-6,atol=2e-12)

    def test_isolated_first_integral(self):
        mod=self.solver()
        source=np.logspace(-12,3,101)
        g=mod.invert_mu(source)
        np.testing.assert_allclose(g*mod.mu(g),source,rtol=1e-11,atol=1e-15)

    def test_exact_newtonian_plummer_virial(self):
        mod=self.solver()
        eta=.06
        out=mod.spherical_virial(eta,newtonian=True)
        self.assertAlmostEqual(out/(np.pi*eta/32),1.,places=8)

    def test_variational_jacobian(self):
        mod=self.solver()
        out=mod.jacobian_check()
        self.assertLess(out['relative_error'],1e-6)
        self.assertLess(out['symmetry_error'],1e-12)

    def test_newtonian_pde(self):
        mod=self.solver()
        out=mod.solve(.06,.1,nr=25,nz=49,extent=20,newtonian=True)
        self.assertTrue(out['converged'])
        self.assertLess(abs(out['virial_trace']/ (3*np.pi*.06/32)-1),.03)
        self.assertLess(out['residual_relative'],1e-8)

    def test_small_source_external_field_convergence(self):
        mod=self.solver()
        out=mod.solve(1e-5,.5,nr=49,nz=97,extent=32)
        self.assertTrue(out['converged'], 'Subtract the uniform external flux analytically')


if __name__=='__main__': unittest.main()
