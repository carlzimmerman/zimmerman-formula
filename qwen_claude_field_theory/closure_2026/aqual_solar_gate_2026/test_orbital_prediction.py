import importlib.util
import sys
import unittest
from pathlib import Path
import sympy as s

sys.path.insert(0, str(Path(__file__).resolve().parent))
prediction = __import__("orbital_prediction") if importlib.util.find_spec("orbital_prediction") else None


class PredictionTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(prediction, "orbital prediction is not implemented")

    def test_force_sign_and_trace(self):
        d = prediction.derive()
        q = d["Q"]
        self.assertEqual(s.simplify(d["tidal"][0,0]+q/3), 0)
        self.assertEqual(s.simplify(d["tidal"][2,2]-2*q/3), 0)
        self.assertEqual(s.trace(d["tidal"]), 0)

    def test_orbit_average_derives_node_rate(self):
        d = prediction.derive()
        value = d["node_rate"].subs({d["Q"]:2, d["n"]:4, d["I"]:s.pi/3})
        self.assertEqual(s.simplify(value-s.Rational(1,8)), 0)
        self.assertEqual(s.simplify(d["node_rate"].subs(d["I"], s.pi/2)), 0)

    def test_zero_quadrupole_gives_no_precession(self):
        self.assertEqual(prediction.node_coefficient_mas_century(0., 30.), 0.)
        a = prediction.node_coefficient_mas_century(1e-26, 1.)
        b = prediction.node_coefficient_mas_century(1e-26, 2.)
        self.assertAlmostEqual(b, 2*a, places=14)


if __name__ == "__main__":
    unittest.main()
