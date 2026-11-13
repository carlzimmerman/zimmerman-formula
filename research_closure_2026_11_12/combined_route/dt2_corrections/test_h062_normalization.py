"""Test the physical acceleration scale of H062's production Mandel callback.

H062 is an executable with no main guard; load only its function definitions
to avoid launching its full data scan merely to test this local contract.
"""
import ast
import math
from pathlib import Path
import unittest
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "hy4_push/H062_exponent_gap.py"
tree = ast.parse(SOURCE.read_text())
definitions = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)
                               and n.name in {"mu_mand", "nu_of", "nu_mandel_mond"}],
                         type_ignores=[])
env = {"np": np, "math": math, "brentq": brentq}
exec(compile(definitions, str(SOURCE), "exec"), env)


class MandelNormalization(unittest.TestCase):
    def test_mond_normalization_has_unit_deep_acceleration_coefficient(self):
        self.assertIn("nu_mandel_mond", env,
                      "Cassini requires a callback in g_N/a0, not g_N/s")
        for n in (1, 2, 3, 5):
            with self.subTest(n=n):
                nu = env["nu_mandel_mond"](n)
                # g^2/(a0*g_N) must approach 1, not n or 1/n.
                y = 1e-10
                self.assertLess(abs(y*nu(y)**2-1), 5e-5)
                raw = env["nu_of"](env["mu_mand"], n)
                for y in (1e-5, .1, 2, 100):
                    self.assertLess(abs(nu(y)/raw(y/n)-1), 1e-8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
