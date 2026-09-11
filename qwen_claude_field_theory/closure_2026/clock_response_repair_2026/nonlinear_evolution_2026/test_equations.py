#!/usr/bin/env python3
"""Reject omitted gradient terms and changed action-variation conventions."""
import importlib.util
from pathlib import Path
import unittest

import sympy as s

HERE = Path(__file__).resolve().parent


class EquationsTest(unittest.TestCase):
    def test_unrestricted_equations_and_initial_restriction(self):
        path = HERE/"equations.py"
        self.assertTrue(path.exists(), "full-gradient equations are not implemented")
        spec = importlib.util.spec_from_file_location("evolution_equations",path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.derive()
        self.assertTrue(all(result["checks"].values()))
        self.assertGreater(len(result["checks"]), 5)
        # Exact zero-gradient principal coefficient comes from previous action
        # variation. Dropping generated chi gradients changes this coefficient.
        sy = result["symbols"]
        M = result["matrix"].subs({sy["u"]:0,sy["ur"]:0,sy["Qr"]:0})
        self.assertFalse(s.cancel(M.det()) == 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
