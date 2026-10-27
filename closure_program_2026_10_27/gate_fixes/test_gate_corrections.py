"""Targeted behavioral regressions; --historical must fail before correction.

Run only this file, not repository-wide test discovery: research scripts write outputs.
"""
import argparse
import ast
import importlib.util
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
RB = ROOT / "rebuild_2026_10_22"
HISTORICAL = "--historical" in sys.argv
sys.argv = [a for a in sys.argv if a != "--historical"]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def historical_need(cells):
    tree = ast.parse((RB / "X57_exclusion_mechanism/x57_exclusion.py").read_text())
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "need" for t in n.targets))
    return eval(compile(ast.Expression(node.value), "historical_X57_need", "eval"), {"c": cells})


def historical_c6(mass, radius, a0):
    path = RB / "X64_oblique_object_keys/x64_oblique_keys.py"
    tree = ast.parse(path.read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "cand_values")
    # Execute the actual historical function, stopping via its sigma=NaN branch.
    ns = dict(math=math, G=1.0, MSUN=1.0, CL=1.0, NU1=(1+math.sqrt(5))/2,
              CAND=["vesc_vc"], CAND_REP=[], A0={"f": a0}, SIGA0={"f": a0/(2*math.pi)},
              nu=lambda y: 0.5+math.sqrt(0.25+1/y))
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(path), "exec"), ns)
    m = dict(sigma=float("nan"), r=radius, Mr=mass, Mb=mass,
             x=mass/radius**2/a0, f_b=1.0, phi_int=mass/radius)
    return ns["cand_values"]("f", "point", m)["vesc_vc"]


if not HISTORICAL:
    R4 = load(RB / "X57_exclusion_mechanism/x57_r4b_correction.py", "r4")
    C6 = load(RB / "X64_oblique_object_keys/x64_c6_correction.py", "c6")


class GateRegressions(unittest.TestCase):
    def test_band_entry_uses_upper_allowed_edge(self):
        cell = dict(pred=1.0, meas=0.7, s=0.1)
        actual = historical_need({"h0672": cell}) if HISTORICAL else R4.band_entry(cell)["absolute_drop"]
        self.assertAlmostEqual(actual, 0.1, places=14)

    def test_prediction_inside_band_needs_no_downward_repair(self):
        cell = dict(pred=0.85, meas=0.7, s=0.1)
        actual = historical_need({"h0672": cell}) if HISTORICAL else R4.band_entry(cell)["absolute_drop"]
        self.assertEqual(actual, 0.0)

    def test_point_mass_ratio_independent_of_catalogue_radius(self):
        expected = math.sqrt(2 / ((1+math.sqrt(5))/2))
        for radius in (0.1, 1.0, 25.0):
            if HISTORICAL:
                actual = historical_c6(1.0, radius, 1.0)
            else:
                actual = C6.binding_ratio(1.0, 1.0, "point", G=1.0)[0]
            self.assertAlmostEqual(actual, expected, places=14)

    @unittest.skipIf(HISTORICAL, "new correction-domain checks")
    def test_fractional_budget_converts_to_same_units(self):
        cell = dict(pred=2.0, meas=1.4, s=0.1)
        self.assertAlmostEqual(R4.band_entry(cell)["fractional_drop"], 0.2)
        self.assertEqual(R4.repair_bound_status(cell, 0.2), "BOUND DOES NOT EXCLUDE")
        self.assertEqual(R4.repair_bound_status(cell, 0.19), "INSUFFICIENT UNDER STATED BOUND")

    @unittest.skipIf(HISTORICAL, "new correction-domain checks")
    def test_below_band_cannot_be_repaired_by_downward_change(self):
        self.assertEqual(R4.repair_bound_status(dict(pred=0.3, meas=0.7, s=0.1), 0.5),
                         "DOWNWARD CHANGE CANNOT REPAIR UNDERPREDICTION")

    @unittest.skipIf(HISTORICAL, "new correction-domain checks")
    def test_positive_shell_has_negative_interior_shear(self):
        self.assertAlmostEqual(R4.shell_delta_sigma(0.5, 1.0, math.pi), -0.04145188432738028)
        self.assertGreater(R4.shell_delta_sigma(2.0, 1.0, math.pi), 0.0)

    @unittest.skipIf(HISTORICAL, "new correction-domain checks")
    def test_plummer_uses_enclosed_mass_at_common_radius(self):
        ratio, r, phi, menc = C6.binding_ratio(1.0, 1.0, "plummer", G=1.0, scale=2.0)
        self.assertEqual(r, 1.0)
        self.assertAlmostEqual(phi, 1/math.sqrt(5))
        self.assertAlmostEqual(menc, 1/(5**1.5))
        self.assertAlmostEqual(ratio**2, 2*phi/(0.5*(menc+math.sqrt(menc*menc+4*menc))))

    @unittest.skipIf(HISTORICAL, "new correction-domain checks")
    def test_uniform_gas_potential_is_continuous_at_edge(self):
        for r in (0.999999, 1.0, 1.000001):
            phi, mass = C6.lens_potential_mass(r, 2.0, 3.0, 1.0, G=1.0)
            self.assertAlmostEqual(phi, 5.0, places=4)
            self.assertAlmostEqual(mass, 5.0, places=4)

    @unittest.skipIf(HISTORICAL, "new correction-domain checks")
    def test_truncated_beta_potential_derivative_and_exterior(self):
        r, h = 1.0, 1e-5
        phi, mass = C6.beta_potential_mass(r, 0.2, 5.0, 3.0, G=1.0)
        pp = C6.beta_potential_mass(r+h, 0.2, 5.0, 3.0, G=1.0)[0]
        pm = C6.beta_potential_mass(r-h, 0.2, 5.0, 3.0, G=1.0)[0]
        self.assertAlmostEqual(-(pp-pm)/(2*h), mass/r**2, places=9)
        phi_out, mass_out = C6.beta_potential_mass(4.0, 0.2, 5.0, 3.0, G=1.0)
        self.assertAlmostEqual(phi_out, mass_out/4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
