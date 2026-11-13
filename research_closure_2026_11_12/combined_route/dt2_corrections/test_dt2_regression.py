"""Independent analytic benchmarks for DT2's time coordinate and dust limit.

These fail if an extra 1/a enters dt/dln(a), or 3 replaces 2 in the
ln(a)-coordinate growth friction. They do not certify nonlinear formation.
"""
import sys
from pathlib import Path
import unittest
import numpy as np

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "hy4_preview_push/CLOSE-1_DT2"))
import dt2_linear as L
import dt2_form as F
import dt2_reach as R


class CosmologicalBenchmarks(unittest.TestCase):
    def test_cosmic_elapsed_time_matches_exact_flat_lcdm_age(self):
        # Integral of dt=da/(aH) has this independent closed-form primitive.
        om = 0.31
        h0 = 70e3 / F.D.MPC
        age = lambda a: 2 / (3*h0*np.sqrt(1-om)) * np.arcsinh(
            np.sqrt((1-om)/om) * a**1.5)
        expected = age(1.0) - age(1/11)
        for module in (F, R):
            with self.subTest(module=module.__name__):
                actual = float(module.T_OF_A(1.0)-module.T_OF_A(1/11))
                self.assertLess(abs(actual/expected-1), 2e-6)

    def test_eds_pressureless_growing_mode_is_delta_proportional_to_a(self):
        old = L.OM_M, L.OM_L
        try:
            L.OM_M, L.OM_L = 1.0, 0.0
            # Exact EdS solution delta(a)=a, initialized with ddelta/dln(a)=delta.
            actual = L.growth_factor(0.0, 1/7, 1.0, dt2=False)
            self.assertAlmostEqual(actual, 7.0, places=7)
        finally:
            L.OM_M, L.OM_L = old

    def test_truncated_formation_cannot_report_present_day_settling(self):
        result = F.run(10.45, F.D.A0_CANON, N=40, max_steps=1, absorb=False)
        self.assertIn("reached_z0", result)
        self.assertFalse(result["reached_z0"])
        self.assertEqual(result["termination_reason"], "max_steps")
        with self.assertRaises(ValueError):
            F.settled_radius(result, F.D.A0_CANON)


if __name__ == "__main__":
    unittest.main(verbosity=2)
