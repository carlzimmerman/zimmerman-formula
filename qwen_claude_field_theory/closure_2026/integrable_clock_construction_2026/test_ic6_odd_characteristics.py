#!/usr/bin/env python3
"""Mutation-sensitive checks of IC6 odd characteristics and their scope."""
import importlib.util
import json
from pathlib import Path
import unittest

import sympy as s

SOURCE = Path(__file__).with_name("ic6_odd_characteristics.py")
SPEC = importlib.util.spec_from_file_location("ic6_odd_checked", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class IC6OddTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = MODULE.derive()

    def assertZero(self, value):
        self.assertTrue(MODULE.is_zero(value), str(value))

    def test_actual_inverse_volume_and_ricci_jets(self):
        g = self.d["geometry"]
        for key in ("inverse_second_jet", "determinant_second_jet", "R_first_jet", "R_second_jet"):
            self.assertZero(g["residuals"][key])
        self.assertZero(g["R2"]+(g["gamma_z"]**2+(g["L"][0]-g["L"][1])**2*g["gamma"]**2)/(2*g["A"][2]**2))
        self.assertFalse(g["R2"].has(g["gamma_zz"]))

    def test_finite_temporal_anisotropy_is_retained(self):
        g = self.d["geometry"]
        self.assertZero(g["QTF1"])
        self.assertZero(g["QTF2"]-(g["gamma_t"]**2+(g["H"][0]-g["H"][1])**2*g["gamma"]**2)/(2*g["N"]**2))
        example = g["QTF2"].subs(dict(zip(g["H"], (1, 2, 4)))).subs({g["gamma_t"]: 0, g["gamma"]: 1, g["N"]: 1})
        self.assertEqual(example, s.Rational(1, 2))

    def test_spatial_anisotropy_is_not_silently_set_to_zero(self):
        g = self.d["geometry"]
        example = g["R2"].subs(dict(zip(g["L"], (1, 3, 2)))).subs({g["gamma_z"]: 0, g["gamma"]: 1, g["A"][2]: 1})
        self.assertEqual(example, -2)

    def test_clock_conformal_curvature_uses_actual_hatted_R(self):
        g = self.d["geometry"]
        difference = g["Rhat"]-g["curvature"]
        self.assertZero(s.diff(difference, g["eps"]))
        self.assertTrue(difference.has(g["wz"]))
        self.assertTrue(difference.has(g["wzz"]))

    def test_phase_momenta_are_varied_and_trace_responds_at_second_order(self):
        p = self.d["phase"]
        for key in ("five_momentum_EL", "TF_elimination", "p_EL", "envelope_p", "trace_second_jet_EL"):
            self.assertZero(p["residuals"][key])
        self.assertZero(p["p_solution"]+p["m"]*p["Q"]/p["K"])
        self.assertZero(p["p_second"]-3*p["m"]*p["Q"]*p["F"]*p["Y2"]/(2*p["a02"]*p["K"]**2))

    def test_odd_momentum_has_no_linear_scalar_or_other_momentum_mixing(self):
        self.assertZero(self.d["phase"]["residuals"]["odd_momentum_mixed_Hessian"])

    def test_independent_local_phase_benchmark_and_mutation(self):
        balanced = MODULE.odd_phase_coefficients()
        unbalanced = MODULE.odd_phase_coefficients(balance=False)
        self.assertZero(balanced["EL_residual"])
        self.assertZero(balanced["physical_speed_squared"]-1)
        # Removing precisely the H6 reciprocal tensor coefficient recovers H5.
        # A test suite that merely hard-codes c_T=1 would miss this mutation.
        self.assertZero(unbalanced["physical_speed_squared"]-unbalanced["J"])
        self.assertEqual(unbalanced["physical_speed_squared"].subs(unbalanced["J"], 2), 2)

    def test_physical_lapse_and_directional_scale_are_in_characteristic(self):
        g = self.d["geometry"]
        omega, k = s.symbols("omega k_z", real=True)
        symbol = self.d["characteristic"]
        self.assertZero(symbol.subs(omega, g["N"]*k/g["A"][2]))
        self.assertNotEqual(s.simplify(symbol.subs({omega: k, g["N"]: 2, g["A"][2]: 3})), 0)

    def test_positive_branch_and_isotropic_limit(self):
        self.assertTrue(self.d["kinetic"].is_positive)
        self.assertTrue(self.d["gradient"].is_positive)
        g = self.d["geometry"]
        common_H, common_A = s.symbols("H A", positive=True)
        replacements = dict.fromkeys(g["H"], common_H)
        replacements.update(dict.fromkeys(g["A"], common_A))
        replacements.update(dict.fromkeys(g["L"], 0))
        expected = self.d["phase"]["m"]*g["N"]*common_A**3*self.d["J"]*(g["gamma_t"]**2/g["N"]**2-g["gamma_z"]**2/common_A**2)/4
        self.assertZero(self.d["L2"].subs(replacements)-expected)

    def test_even_rank_one_square_is_not_discarded(self):
        p = self.d["phase"]
        self.assertZero(p["hessian"].det())
        self.assertZero(p["residuals"]["rank_one_square"])
        values = {p["m"]: 1, p["a02"]: 1, p["F"]: 1, p["Q"]: 1, p["Y"]: 0}
        self.assertEqual(p["hessian"][0, 0].subs(values), -s.Rational(3, 2))
        self.assertEqual(p["hessian"][0, 1].subs(values), 1)

    def test_varying_F_retains_extra_auxiliary_curvature_cross_term(self):
        p = self.d["phase"]
        self.assertZero(p["residuals"]["full_F_Hessian_square_and_cross_term"])
        self.assertZero(p["full_F_quadratic"].subs(p["delta_F"], 0)-p["rank_one_square"])
        # At Y=0, delta_K has no delta_F. The nonzero delta_F delta_Y term
        # therefore cannot be hidden in the rank-one square or set to zero.
        mixed = s.diff(p["full_F_quadratic"], p["delta_F"], p["delta_Y"])
        self.assertZero(mixed.subs(p["Y"], 0)-p["m"]*p["Q"]**2/(2*p["a02"]))

    def test_genuine_nearby_bianchi_branch_has_nonsingular_auxiliaries(self):
        h = self.d["homogeneous"]
        for value in h["residuals"].values():
            self.assertZero(value)
        self.assertGreater(h["determinant_numeric"], 0)
        self.assertGreater(float(h["shear_second_at_witness"]), 0)

    def test_json_and_scope_do_not_promote_odd_result_to_all_modes(self):
        result = MODULE.run()
        json.dumps(result)
        self.assertTrue(result["exact_checks_passed"])
        self.assertEqual(result["base_commit"], "0b75e72bf5797e451beb258847ade528cd9c4551")
        for key in ("full_all_background_causality_proved", "even_physical_characteristics_eliminated", "nonlinear_inhomogeneous_solution_existence_proved"):
            self.assertFalse(result[key])


if __name__ == "__main__":
    unittest.main()
