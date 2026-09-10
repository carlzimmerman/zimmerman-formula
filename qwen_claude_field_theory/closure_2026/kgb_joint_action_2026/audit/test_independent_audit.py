#!/usr/bin/env python3
"""Independent local audit; finite controls do not certify a complete theory.

Run with Python -B so importing the preserved legacy modules writes no cache.
The two counterexamples are exact rational constructions. The source-metric
comparison and slope checks use symbolic expressions, not fitted matrices.
"""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest

import sympy as s


CLOSURE = Path(__file__).resolve().parents[2]
LEGACY = CLOSURE / "kgb_shared_pressure_2026"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def classify_legacy_interval(result):
    """A positive computed gap rejected by the tolerance is unresolved."""
    if result["exists"]:
        return "numerically_resolved_nonempty"
    if result.get("upper", 0) > result.get("lower", 0):
        return "numerically_unresolved"
    return "no_positive_computed_gap"


class IndependentAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.steering = module("audit_legacy_steering", LEGACY / "jet_steering.py")
        cls.model = cls.steering.source.model

    def assertZeroMatrix(self, matrix):
        self.assertTrue(all(s.factor(entry) == 0 for entry in matrix), matrix)

    def test_exact_narrow_interval_is_not_empty_despite_legacy_rejection(self):
        delta = Q(1, 10**11)
        invariant, beta, cross = Q(1), Q(1), Q(0)
        radial = -1 + delta
        lower, upper = 1 - delta, invariant
        kinetic = (lower + upper) / 2
        angular = beta * (kinetic - invariant)
        self.assertLess(lower, kinetic)
        self.assertLess(kinetic, upper)
        self.assertGreater(kinetic, 0)
        self.assertLess(radial, 0)
        self.assertLess(angular, 0)
        self.assertGreater(cross**2 - kinetic * radial, 0)
        # With zero cross coefficient the all-direction speed squared is a
        # convex combination of these two exact values. Both are below one.
        self.assertTrue(0 < -radial / kinetic < 1)
        self.assertTrue(0 < -angular / kinetic < 1)
        result = self.steering.window(1.0, 0.0, float(radial), 1.0)
        self.assertFalse(result["exists"])
        self.assertGreater(result["upper"], result["lower"])
        self.assertEqual(classify_legacy_interval(result), "numerically_unresolved")
        print("EXACT_NARROW_INTERVAL", str(lower), str(upper),
              "legacy_classification=numerically_unresolved")

    def test_positive_radial_cone_has_unbounded_static_time_energy(self):
        kinetic, cross = s.Integer(1), s.Rational(1, 2)
        radial, angular = s.Rational(1, 10), -s.Rational(1, 10)
        invariant, beta = s.Rational(11, 10), s.Integer(1)
        self.assertEqual(angular, beta * (kinetic - invariant))
        self.assertEqual(cross**2 - kinetic * radial, s.Rational(3, 20))
        result = self.steering.window(float(invariant), float(cross), float(radial), 1.0)
        self.assertTrue(result["exists"])
        self.assertAlmostEqual(result["chosen_K"], 1.0)
        # For 0<=t<=1 the positive speed is t/2 + sqrt(1/10+3*t^2/20),
        # which increases with t. Its endpoint is strictly below one.
        max_speed = s.Rational(1, 2) + s.sqrt(s.Rational(3, 20))
        self.assertLess(max_speed, 1)
        velocity, gradient, transverse = s.symbols("velocity gradient transverse", real=True)
        lagrangian = (kinetic * velocity**2 + 2 * cross * velocity * gradient
                      + radial * gradient**2 + angular * transverse**2) / 2
        hamiltonian = s.expand(s.diff(lagrangian, velocity) * velocity - lagrangian)
        self.assertEqual(hamiltonian.subs({velocity: 0, transverse: 0}), -gradient**2 / 20)
        self.assertEqual(s.limit(-gradient**2 / 20, gradient, s.oo), -s.oo)
        print("POSITIVE_RADIAL_COUNTEREXAMPLE", "max_speed=" + str(max_speed),
              "static_energy=-gradient^2/20; not a kinetic-ghost claim")

    def test_primary_effective_metric_matches_all_principal_entries(self):
        # Deffayet et al. 1008.0048v2, equations 16--18, translated from
        # (+---), K+G box(phi) to (-+++), P-G box(phi); restore Planck m.
        a = self.model.principal_template()
        eta = s.diag(-1, 1, 1, 1)
        covector, hessian = a["v"], a["H"]
        vector = eta * covector
        x = -(covector.T * vector)[0] / 2
        dx = -hessian * vector
        dx_up = eta * dx
        vx = (vector.T * dx)[0]
        box = s.trace(eta * hessian)
        omega = a["P1"] - 2 * a["G1"] * box - a["G2"] * vx - 2 * x**2 * a["G1"]**2 / a["m"]
        theta = a["P2"] - a["G2"] * box + 4 * x * a["G1"]**2 / a["m"]
        independent = (-omega * eta + theta * vector * vector.T
                       - a["G2"] * (dx_up * vector.T + vector * dx_up.T)
                       - 2 * a["G1"] * eta * hessian * eta)
        self.assertZeroMatrix(independent - a["M"])

    def test_both_slopes_follow_directly_from_zero_current(self):
        v, w, chi, box, gx, p, ell = s.symbols("v w chi box gx p ell", nonzero=True)
        eta = s.diag(-1, 1, 1, 1)
        vector, dx_up = s.Matrix([v, w, 0, 0]), s.Matrix([0, chi, 0, 0])
        vv = vector * vector.T
        # Derivatives of the independently reconstructed effective metric.
        d_gxx = w * chi * eta - box * vv - dx_up * vector.T - vector * dx_up.T
        x = (v**2 - w**2) / 2
        beta = w**2 / (2 * x)
        px = gx * (box + chi / w)
        enthalpy = 2 * x * gx * chi / w
        target_shape = s.diag(1, 0, beta, beta)
        self.assertZeroMatrix(vv + gx / px * d_gxx - enthalpy / px * target_shape)
        # The regular expression contains no division by P_X or box+chi/w.
        regular = p * (box + chi / w) * vv + p * d_gxx
        regular_enthalpy = enthalpy.subs(gx, p * ell)
        self.assertZeroMatrix(regular - regular_enthalpy / ell * target_shape)
        self.assertZeroMatrix(regular.subs(box, -chi / w)
                              - regular_enthalpy / ell * target_shape)

    def test_exact_regular_zero_pressure_slope_control(self):
        # B=r=p=L=1, X=3/2, g=2/3: Z=0 and P_X=0 exactly.
        a = self.model.principal_template()
        vector = s.Matrix([-2, 1, 0, 0])
        hessian = s.Matrix([[-s.Rational(2, 3), s.Rational(4, 3), 0, 0],
                            [s.Rational(4, 3), 3, 0, 0],
                            [0, 0, 1, 0], [0, 0, 0, 1]])
        subs = {a["m"]: 1, a["G1"]: 1, a["G2"]: 0,
                a["P"]: 0, a["P1"]: 0, a["P2"]: 0}
        subs.update(zip(a["v"], vector))
        subs.update({a["H"][i, j]: hessian[i, j] for i in range(4) for j in range(i, 4)})
        slope = a["M"].diff(a["G2"]).subs(subs, simultaneous=True)
        stress = a["T"].subs(subs, simultaneous=True)
        self.assertEqual(stress[0, 0], -17)
        self.assertEqual(stress[0, 1], 0)
        self.assertEqual(stress[1, 1], 0)
        self.assertZeroMatrix(slope - s.diag(-17, 0, -s.Rational(17, 3), -s.Rational(17, 3)))

    def test_reported_repaired_jet_has_negative_radial_coefficient(self):
        precision = module("audit_legacy_precision", LEGACY / "precision_check.py")
        choice = self.steering.choose(1e-6, 20.0, 0.0, 0.5, 0.0, 1.0)
        self.assertIsNotNone(choice["selected"])
        row = precision.check("1e-6", "20", "0", ".5", "1", pressure="0",
                              pxx=str(choice["PXX"]), dps=60)
        self.assertGreater(row["kinetic"], 0)
        self.assertLess(row["radial"], 0)
        self.assertLess(row["angular"], 0)
        self.assertGreater(row["radial_discriminant"], 0)
        self.assertLess(float(row["relative_stress_error"]), 1e-45)
        print("REPAIRED_LOCAL_JET", "C11=" + str(row["radial"]),
              "stress_error=" + str(row["relative_stress_error"]), "dps=60")


if __name__ == "__main__":
    unittest.main(verbosity=2)
