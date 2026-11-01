"""Independent energy and envelope checks for the isentropic limit calculation."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))
import material

try:
    import isentropic_limit
except ModuleNotFoundError:
    isentropic_limit = None


class IsentropicLimitTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(isentropic_limit, "isentropic limit implementation is absent")
        self.params = material.MaterialParameters(rho_q=1, G=1,
                                                  a0=np.sqrt(8*np.pi), tau=0.5)
        self.mass = np.pi/3

    def test_initial_energy_is_the_uniform_sphere_continuum_integral(self):
        # Catches importing a finite-shell gravitational energy as the continuum value.
        result = isentropic_limit.initial_uniform_sphere_energy(self.mass, 1, -0.25, 1)
        self.assertAlmostEqual(result, -0.6383386726543543, places=12)

    def test_equilibrium_energy_agrees_with_independent_virial_integral(self):
        # Catches a missing latent-energy contribution or wrong gravitational measure.
        branch = isentropic_limit.isentropic_equilibrium(2.5, self.mass, self.params)
        self.assertAlmostEqual(branch["mass"], self.mass, places=12)
        self.assertLess(abs(branch["virial_relative_residual"]), 2e-7)
        self.assertLess(abs(branch["direct_minus_virial_energy"]), 2e-7)
        self.assertGreater(branch["half_mass_radius"], 0)
        self.assertLess(branch["half_mass_radius"], branch["radius"])

    def test_stationary_fixed_mass_envelope_includes_dormant_energy_offset(self):
        # Catches differentiating only pressure energy rather than the full material energy.
        # Differencing close equilibrium solves needs tighter ODE errors than
        # predicting the endpoint itself; otherwise solver noise is amplified.
        options = dict(rtol=1e-12, quadrature_rtol=1e-11, max_step=0.005)
        lower = isentropic_limit.isentropic_equilibrium(2.4-1e-4, self.mass, self.params, **options)
        upper = isentropic_limit.isentropic_equilibrium(2.4+1e-4, self.mass, self.params, **options)
        center = isentropic_limit.isentropic_equilibrium(2.4, self.mass, self.params, **options)
        slope = ((upper["total_energy"]-lower["total_energy"]) /
                 (upper["K"]-lower["K"]))
        self.assertAlmostEqual(slope/center["energy_derivative_wrt_K"], 1, delta=2e-5)

    def test_dense_branch_approaches_the_analytic_n_one_energy(self):
        # Catches the length or mass normalization in the high-density limit.
        branch = isentropic_limit.isentropic_equilibrium(1000, self.mass, self.params)
        n_one_radius = np.sqrt(np.pi*branch["K"]/2)
        n_one_energy = -self.mass**2/(2*n_one_radius)
        self.assertAlmostEqual(branch["radius"]/n_one_radius, 1, delta=0.003)
        self.assertAlmostEqual(branch["total_energy"]/n_one_energy, 1, delta=0.003)

    def test_energy_selected_endpoint_is_not_fitted_to_an_observed_entropy(self):
        # Catches solving for a preset K or matching total energy without latent energy.
        target = isentropic_limit.initial_uniform_sphere_energy(self.mass, 1, -0.25, 1)
        result = isentropic_limit.solve_energy_limit(target, self.mass, self.params)
        self.assertGreater(result["K"], 0)
        self.assertLess(abs(result["energy_residual"]), 2e-8)
        self.assertGreater(result["energy_derivative_wrt_K"], 0)
        self.assertAlmostEqual(result["entropy"],
                               self.mass*np.cbrt(result["K"]/self.params.k_star), places=12)

    def test_cli_writes_finite_reviewable_prediction(self):
        # Catches a CLI that omits its physical assumptions or selected endpoint.
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/"limit.json"
            run = subprocess.run([sys.executable, str(HERE/"isentropic_limit.py"),
                                  "--initial-energy", "-0.6383386726543543",
                                  "--output", str(output)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            report = json.loads(output.read_text())
            self.assertIn("conditional", report["scope"])
            self.assertLess(abs(report["endpoint"]["energy_residual"]), 2e-8)
            json.dumps(report, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
