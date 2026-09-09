#!/usr/bin/env python3
"""Constructive repair identities and independent UV kinetic audit."""
import unittest
import mpmath as mp
import ic10_transition as original
import ic11_transition_completion as trial


class CompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 60
        cls.states = list(original.continuation(500))

    def test_symbolic_action_identities(self):
        self.assertTrue(all(value == 0 for value in trial.symbolic_identities().values()))

    def test_plateau_and_static_correction_first_jets(self):
        # At eta=1, C=J=A^-1. At p=0, Z=0 and dZ/dp=0.
        for point in (self.states[0]["point"], [mp.mpf(0),mp.mpf("0.2"),mp.mpf("0.6")]):
            for R, dx, du in (("1","0","0"),("0","1","2")):
                f = lambda rho,xi,u: trial.correction_density([rho,xi,u],mp.mpf(R),mp.mpf(dx),mp.mpf(du))
                self.assertLess(abs(f(*point)),mp.mpf("1e-45"))
                for i in range(3):
                    self.assertLess(abs(mp.diff(f,tuple(point),tuple(int(j==i) for j in range(3)))),mp.mpf("1e-40"))

    def test_trial_has_positive_W_and_no_auxiliary_poles_in_active_window(self):
        checked = 0
        for bg in self.states:
            if mp.mpf("0.5") < bg["eta"] < 1:
                fixed = trial.at_background(bg)
                self.assertGreater(min(mp.eigsy(fixed["W"],eigvals_only=True)),0)
                self.assertFalse(fixed["positive_auxiliary_poles"])
                self.assertLess(abs(fixed["tensor_speed_squared"]-1),mp.mpf("1e-45"))
                checked += 1
        self.assertGreater(checked, 10)

    def test_UV_identity_and_actual_sign_change(self):
        values = []
        for n in (200,220):
            bg = self.states[n]
            fixed = trial.at_background(bg)
            rho,xi,u = bg["point"]
            direct = (bg["E"]*bg["A"]/6
                      +mp.diff(lambda v: original.raw_density(v,xi,u),rho,2)/4)
            self.assertLess(abs(fixed["scalar_UV_kinetic"]-direct),mp.mpf("1e-42"))
            self.assertLess(abs(fixed["scalar_UV_kinetic"]-fixed["scalar_UV_switch_identity"]),mp.mpf("1e-42"))
            values.append(direct)
        self.assertGreater(values[0],0)
        self.assertLess(values[1],0)

    def test_high_frequency_schur_kinetic_converges_to_negative_limit(self):
        bg = self.states[220]
        fixed = trial.at_background(bg)
        mixing = bg["hessian"][1:3,0]/2
        errors = []
        for k2 in (mp.mpf("1e12"),mp.mpf("1e16")):
            Q = bg["auxiliary"]+k2*fixed["G"]
            kinetic = fixed["scalar_UV_kinetic"]-(mixing.T*(Q**-1)*mixing)[0]
            self.assertLess(kinetic,0)
            errors.append(abs(kinetic-fixed["scalar_UV_kinetic"]))
        self.assertLess(errors[1], errors[0]/1000)


if __name__ == "__main__":
    unittest.main()
