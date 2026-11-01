"""Thermodynamic and gravitational checks for the thermal branch discriminator."""

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
    import thermal_branch
except ModuleNotFoundError:
    thermal_branch = None


class ThermalBranchTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(thermal_branch, "thermal branch implementation is absent")
        self.params = material.MaterialParameters(rho_q=1, G=1,
                                                  a0=np.sqrt(8 * np.pi), tau=0.5)

    def test_thermal_enthalpy_uses_isothermal_pressure_derivative(self):
        # Catches the adiabatic enthalpy being used after thermal relaxation.
        for d in [1.1, 1.5, 1.9, 2.5, 5.0]:
            delta = 1e-5
            derivative = (thermal_branch.thermal_enthalpy(d + delta) -
                          thermal_branch.thermal_enthalpy(d - delta)) / (2 * delta)
            p_derivative = (thermal_branch.thermal_pressure_shape(d + delta) -
                            thermal_branch.thermal_pressure_shape(d - delta)) / (2 * delta)
            self.assertAlmostEqual(derivative, p_derivative / d, delta=1e-8)
        self.assertEqual(thermal_branch.thermal_enthalpy(0.5), 0)
        self.assertAlmostEqual(thermal_branch.thermal_enthalpy(4),
                               2 / np.sqrt(1.5) - 0.5, places=14)

    def test_density_inverse_resolves_gate_and_finite_enthalpy_limit(self):
        # Catches choosing a dormant density or extending the inverse past H_infinity.
        densities = np.array([1, 1.0001, 1.1, 1.5, 2, 3, 100, 1e5])
        recovered = thermal_branch.density_from_thermal_enthalpy(
            thermal_branch.thermal_enthalpy(densities))
        np.testing.assert_allclose(recovered, densities, rtol=1e-10, atol=1e-11)
        with self.assertRaises(ValueError):
            thermal_branch.density_from_thermal_enthalpy(2 / np.sqrt(1.5))
        with self.assertRaises(ValueError):
            thermal_branch.density_from_thermal_enthalpy(-1e-6)

    def test_fixed_mass_branch_satisfies_virial_and_thermal_identity(self):
        # Catches omitted 4*pi, rho_q, or a wrong internal-energy weight.
        mass = np.pi / 3
        branch = thermal_branch.fixed_mass_branch(20, mass, self.params)
        self.assertAlmostEqual(branch["mass"], mass, places=12)
        self.assertGreater(branch["central_K"], 0)
        self.assertGreater(branch["radius"], 0)
        self.assertLess(abs(branch["virial_relative_residual"]), 2e-7)
        self.assertAlmostEqual(branch["total_energy"],
                               branch["internal_energy"] + branch["gravitational_energy"],
                               places=13)
        self.assertAlmostEqual(branch["temperature"] * branch["entropy"],
                               3 * branch["internal_energy"], places=12)

    def test_physical_scales_are_not_silently_normalized_to_one(self):
        # Catches accidental use of unit G, rho_q, or Kstar in dimensionalization.
        reference = thermal_branch.fixed_mass_branch(5, 1, self.params)
        rhoq, gravity, kstar = 7, 3, 5
        params = material.MaterialParameters(rho_q=rhoq, G=gravity,
                                             a0=np.sqrt(8*np.pi*gravity*kstar*rhoq**2), tau=1)
        mass_factor = rhoq * (kstar / gravity)**1.5
        changed = thermal_branch.fixed_mass_branch(5, mass_factor, params)
        self.assertAlmostEqual(changed["psi"], reference["psi"], places=12)
        self.assertAlmostEqual(changed["radius"] / reference["radius"],
                               np.sqrt(kstar / gravity), places=12)
        self.assertAlmostEqual(changed["internal_energy"] / reference["internal_energy"],
                               kstar * rhoq * mass_factor, places=10)
        self.assertAlmostEqual(changed["entropy"] / reference["entropy"], mass_factor, places=10)

    def test_cli_emits_finite_case_table_and_energy_offsets(self):
        # Catches a nonreviewable CLI result or comparison with the wrong energy.
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "branch.json"
            result = subprocess.run(
                [sys.executable, str(HERE / "thermal_branch.py"), "--central-densities",
                 "2", "20", "--initial-energy", "-0.6381918589", "--output", str(output)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text())
            self.assertEqual(len(report["branches"]), 2)
            for branch in report["branches"]:
                self.assertAlmostEqual(branch["energy_minus_initial"],
                                       branch["total_energy"] + 0.6381918589, places=13)
            json.dumps(report, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
