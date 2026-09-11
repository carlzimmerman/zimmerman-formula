#!/usr/bin/env python3
"""Bounded checks of action coefficients, independent of the infall constraints.

These tests catch a total derivative substituted for a fixed-X time partial,
an omitted cubic repair, and an incorrect second background time derivative.
They do not establish nonlinear solutions or a complete gravitational theory.
"""
import importlib.util
from functools import lru_cache
import math
from pathlib import Path
import unittest

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent


@lru_cache(maxsize=None)
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BackgroundTests(unittest.TestCase):
    def coefficients(self, gamma):
        path = HERE / "background.py"
        self.assertTrue(path.is_file(), "the action-derived background module is missing")
        return load("infall_background_test", path).background(gamma=gamma)

    def close(self, actual, expected, *, atol=2e-13, rtol=2e-12):
        self.assertTrue(math.isclose(actual, expected, abs_tol=atol, rel_tol=rtol),
                        f"{actual!r} != {expected!r}")

    def test_repaired_action_preserves_charge_energy_and_pressure(self):
        # Removing the cubic P or W counterterm breaks these invariants.
        required = {"M2", "Lambda", "H", "q", "A", "U", "d", "W0", "WY",
                    "P", "PX", "PXX", "Pt", "PXt", "Ptt", "Vt", "Vtt",
                    "Wt", "qdot", "Hdot", "gamma"}
        for gamma in (0.0, 1e-6):
            c = self.coefficients(gamma)
            self.assertTrue(required <= c.keys())
            self.assertTrue(all(math.isfinite(value) for value in c.values()))
            q, H, A, U, M = (c[k] for k in ("q", "H", "A", "U", "M2"))
            self.close(q, 10 / 11)
            self.close(A, 0.1)
            self.close(U, 1 / 110)
            self.close(c["d"], 0.005)
            self.close(c["WY"], 0.005)
            self.close(H, math.sqrt(4 / 15))
            self.close(c["Hdot"], -0.05)
            self.close(c["P"], 0.0)
            self.close(2*q*c["PX"] - 6*gamma*H*q*q, A)
            rho = 2*q*q*c["PX"] - c["P"] + U - 6*gamma*H*q**3
            pressure = c["P"] - U + c["W0"] + 2*gamma*q*q*c["qdot"]
            self.close(rho, q*A + U)
            self.close(3*M*H*H, rho + M*c["Lambda"])
            self.close(pressure, 0.0)

    def test_fixed_x_partials_match_independent_cubic_background_jets(self):
        # A total time derivative of P on the branch is zero; Pt must not be.
        for gamma in (0.0, 1e-6):
            c = self.coefficients(gamma)
            q, H, A, U, qd, hd = (c[k] for k in ("q", "H", "A", "U", "qdot", "Hdot"))
            B0 = A/q + 2*A*A/U
            self.close(qd, -3*A*H*0.5/B0 - q*U/(2*H))
            self.close(c["PXX"], (B0 - A/q)/(4*q*q))
            self.close(c["Pt"], -A*qd - 6*gamma*q*q*H*qd)
            self.close(c["PXt"], (-3*H*A - B0*qd)/(2*q)
                       + 3*gamma*(H*qd + q*hd))
            self.close(c["Vt"], -A*qd - 3*H*U)
            self.close(c["Vt"] - c["Pt"] + 3*H*c["W0"], 0.0)
            self.assertGreater(abs(c["Pt"]), 1e-3)

    def test_time_partials_against_independently_evolved_action(self):
        # Uses the original stationary ODE and finite differences of the action,
        # not any derivative helper or symbolic expression from background.py.
        self.coefficients(0.0)
        stationary = load("infall_stationary_control", HERE.parent / "nonlinear_transport/stationary.py")
        _, rhs = stationary.symbolic()
        h = 1e-3

        def flow(t, state):
            a, m, v = state
            H = math.sqrt((0.7 + 0.1/a**3)/3)
            lm, lv = rhs(m, v, 1/(1 + 7*a**3))
            return [a*H, m*H*lm, v*(1-v)*H*lv]

        points = {0: np.array([1.0, 0.1, 0.5])}
        for sign in (-1, 1):
            solution = solve_ivp(flow, (0, sign*2*h), points[0],
                                 method="DOP853", rtol=3e-13, atol=3e-15,
                                 dense_output=True)
            self.assertTrue(solution.success, solution.message)
            for multiple in (sign, 2*sign):
                points[multiple] = solution.sol(multiple*h)

        for gamma in (0.0, 1e-6):
            c = self.coefficients(gamma)
            fixed_x = c["q"]**2

            def action_at(state):
                a, m, v = state
                A = 0.1/a**3
                q = 1/(1+m)
                U = m*q*A
                d = A*U/(2*q*(q*A+U))
                H = math.sqrt((0.7+A)/3)
                B0 = A/q + 2*A*A/U
                qdot = -3*A*H*v/B0 - q*U/(2*H)
                numerator = U - 2*d*fixed_x
                denominator = U - 2*d*q*q
                P = -U*math.log(numerator/denominator)/2 + 3*gamma*q*H*(fixed_x-q*q)
                PX = d*U/numerator + 3*gamma*q*H
                W = U - 2*gamma*q*q*qdot
                return np.array([P, PX, U, W, q, qdot])

            f = {i: action_at(state) for i, state in points.items()}
            first = (f[-2] - 8*f[-1] + 8*f[1] - f[2])/(12*h)
            second = (-f[2] + 16*f[1] - 30*f[0] + 16*f[-1] - f[-2])/(12*h*h)
            for key, expected in (("Pt", first[0]), ("PXt", first[1]),
                                  ("Vt", first[2]), ("Wt", first[3]),
                                  ("Ptt", second[0]), ("Vtt", second[2]),
                                  ("qdot", first[4])):
                self.close(c[key], expected, atol=5e-10, rtol=5e-8)
            self.close(c["qddot"], first[5], atol=5e-11, rtol=5e-9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
