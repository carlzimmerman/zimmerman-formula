#!/usr/bin/env python3
"""Independent controls for the new IC-6 tensor-balance revision."""
import importlib.util
import json
from pathlib import Path
import unittest

import sympy as s

SOURCE = Path(__file__).with_name("tensor_balance_completion.py")
MODULE = None
if SOURCE.exists():
    spec = importlib.util.spec_from_file_location("tensor_balance_tested", SOURCE)
    MODULE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(MODULE)


class TensorBalanceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(MODULE, "The tensor phase-action derivation is not implemented")
        self.d = MODULE.derive()

    def assertZero(self, expr):
        values = list(expr) if isinstance(expr,s.MatrixBase) else [expr]
        self.assertTrue(all(s.simplify(v)==0 for v in values),str(expr))

    def test_actual_connection_curvature_and_tracefree_velocity(self):
        # Catches an assumed Ricci coefficient or missing physical scale/lapse.
        d = self.d
        self.assertZero(d["R2"]+d["k"]**2*d["gamma"]**2*s.sin(d["k"]*d["coord"])**2/(2*d["A"]**2))
        self.assertZero(d["QTF2"]-d["eps"]**2*d["gammadot"]**2*s.cos(d["k"]*d["coord"])**2/(2*d["N"]**2))
        self.assertZero(d["R1"])
        self.assertZero(d["determinant"]-d["A"]**6)

    def test_trace_momentum_el_is_used_before_quadratic_reduction(self):
        # Catches incorrectly freezing a nonstationary trace momentum.
        d = self.d
        self.assertZero(d["p0"]+d["m"]*d["Q"])
        for branch in d["branches"].values():
            self.assertZero(branch["p_linear"])
            self.assertZero(branch["p_preservation_residual"])
            self.assertZero(branch["p_second_order_action_residual"])
            self.assertZero(branch["PTF_EL_residual"])

    def test_old_and_new_tensor_coefficients_from_phase_elimination(self):
        # Catches balancing only the gradient or taking an inverted speed ratio.
        d = self.d
        J = 1+d["Q"]**2*d["F"] / d["a02"]
        old,new = d["branches"]["IC5"],d["branches"]["IC6"]
        self.assertZero(old["K_T"]-1)
        self.assertZero(old["G_T"]-J)
        self.assertZero(old["physical_speed_squared"]-J)
        self.assertZero(new["K_T"]-J)
        self.assertZero(new["G_T"]-J)
        self.assertZero(new["physical_speed_squared"]-1)

    def test_positive_tensor_branch_is_explicit(self):
        # Catches a ghost branch being certified merely because c_T^2=1.
        d = self.d
        Jpos=s.Symbol("J_positive",positive=True)
        replace={d["F"]:(Jpos-1)*d["a02"]/d["Q"]**2}
        for key in ("K_T","G_T"):
            value=s.simplify(d["branches"]["IC6"][key].subs(replace))
            self.assertEqual(value,Jpos)
            self.assertTrue(value.is_positive)

    def test_time_dependent_measure_enters_tensor_equation(self):
        # Catches freezing the expanding measure or omitting J_T damping.
        d = self.d
        self.assertZero(d["wave_equation_residual"])
        self.assertZero(d["balanced_damping"]-(3*d["A_rate"]-d["N_rate"]+d["J_rate"]))

    def test_nearby_homogeneous_constraint_branch_reaches_nonzero_F(self):
        # Catches substituting arbitrary off-shell xi,u as an on-shell claim.
        d = self.d
        T,ell=d["T"],d["ell"]
        self.assertZero(d["homogeneous_secondary_at_witness"])
        self.assertZero(d["homogeneous_tangent_residual"])
        self.assertZero(d["dF_dj"]+(5*T-27)/(2*ell**2*(4*T-27)))
        self.assertZero(d["dJT_dj"]+4*(5*T-27)/(3*(4*T-27)))
        self.assertLess(float(d["dJT_dj"].subs(T,9)),0)

    def test_static_first_jets_and_isotropic_homogeneous_action_transfer(self):
        # Catches silently changing the stationary or isotropic FLRW equations.
        self.assertZero(self.d["static_first_jets"])
        self.assertZero(self.d["isotropic_difference"])
        self.assertZero(self.d["isotropic_first_jets"])

    def test_no_bianchi_I_transfer_and_no_witness_quadratic_change(self):
        # Catches extending an isotropic bridge to finite homogeneous shear.
        d = self.d
        self.assertZero(d["witness_second_jet"])
        self.assertEqual(d["hamiltonian_change"].subs({d["m"]:1,d["a02"]:1,
            d["p"]:1,d["F"]:1,d["PTF_squared"]:1}),-1)

    def test_auxiliary_gradient_square_is_unchanged_at_fixed_momenta(self):
        # Catches calling a lower-order change a new principal-gradient term.
        self.assertZero(self.d["gradient_change_hessian"])

    def test_json_scope_and_computed_residuals(self):
        result=MODULE.run()
        json.dumps(result)
        self.assertTrue(result["exact_checks_passed"])
        self.assertTrue(result["input_hashes_match"])
        self.assertFalse(result["full_all_background_causality_proved"])
        self.assertGreaterEqual(len(result["exact_residuals"]),15)

    def test_actual_IC6_auxiliary_density_converges_on_positive_tensor_branch(self):
        # Catches relabeling H5's numerical result instead of solving IC6.
        self.assertTrue(callable(getattr(MODULE,"numerical",None)),
                        "The IC6 density has not been sent to the auxiliary solver")
        result=MODULE.numerical()
        self.assertTrue(result["density_bridge_passed"])
        self.assertTrue(result["all_converged"])
        self.assertLess(result["maximum_residual"],1e-10)
        self.assertGreater(result["minimum_JT_lower_bound"],0)
        self.assertLess(result["refinement_difference_32_64"],result["refinement_difference_16_32"])

    def test_full_plateau_momentum_elimination_includes_JT_trace_dependence(self):
        # Catches omitting d(JT)/dp after eliminating all five tensor components.
        self.assertIn("plateau",self.d,"The full plateau phase action has not been eliminated")
        d=self.d["plateau"]
        self.assertZero(d["tensor_EL_residuals"])
        self.assertZero(d["envelope_residual"])
        self.assertZero(d["trace_EL_residual"])
        self.assertZero(d["compact_lagrangian_residual"])
        self.assertZero(d["p_solution"]+self.d["m"]*self.d["Q"]/d["K6"])


if __name__ == "__main__":
    unittest.main()
