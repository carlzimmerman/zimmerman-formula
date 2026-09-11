#!/usr/bin/env python3
"""Independent potential tests; manufactured jets do not solve the action."""
import unittest

import numpy as np


def implementation():
    try:
        from potentials import from_time_jets, reconstruct
    except ModuleNotFoundError as error:
        raise AssertionError("independent metric-potential reconstruction is missing") from error
    return from_time_jets, reconstruct


class PotentialTests(unittest.TestCase):
    def test_independent_nonzero_slip_manufactured_jets(self):
        # Catches imposing Phi=Psi, losing shear's sign, and using lapse alone.
        from_time_jets, _ = implementation()
        r = np.linspace(0., 6., 3001)
        mass, core, beta_amplitude = .002, .7, .003
        radial_metric_perturbation = mass*r*r/(r*r+core*core)**1.5
        f = (1+radial_metric_perturbation)**-2
        beta = beta_amplitude*np.exp(-r*r)
        shear = -4*beta_amplitude*r*r*np.exp(-r*r)
        lapse = .001*np.exp(-2*r*r)
        out = from_time_jets(
            r, f, lapse, np.zeros_like(r), -shear/3,
            psi_outer=-mass/np.sqrt(r[-1]**2+core**2),
            beta_outer=beta[-1], beta_prime_outer=-2*r[-1]*beta[-1])
        np.testing.assert_allclose(out["Psi"], -mass/np.sqrt(r*r+core*core),
                                   rtol=0., atol=2e-11)
        np.testing.assert_allclose(out["beta_dot"], beta, rtol=0., atol=2e-11)
        np.testing.assert_allclose(out["Phi"], lapse+beta, rtol=0., atol=2e-11)
        self.assertGreater(np.max(abs(out["slip"])), .005)

    def test_nonpositive_spatial_metric_is_rejected(self):
        from_time_jets, _ = implementation()
        r = np.linspace(0., 1., 11)
        with self.assertRaises(ValueError):
            from_time_jets(r, np.zeros_like(r), r*0, r*0, r*0,
                           psi_outer=0., beta_outer=0., beta_prime_outer=0.)

    def test_zero_source_and_quadratic_initial_slip(self):
        _, reconstruct = implementation()
        from initial import solve_slice
        zero = reconstruct(solve_slice(0., .3, outer=20., points=1601))
        self.assertLess(np.max(abs(zero["Phi"])), 2e-11)
        self.assertLess(np.max(abs(zero["Psi"])), 2e-11)
        self.assertIsNone(zero["relative_slip"])
        amplitudes = (2e-3, 1e-3, 5e-4)
        outputs = [reconstruct(solve_slice(a, .3, outer=20., points=2401))
                   for a in amplitudes]
        errors = [np.max(abs(out["slip"])) for out in outputs]
        for index in range(2):
            # Halving the source must suppress slip faster than a linear term.
            self.assertLess(errors[index+1], .30*errors[index])
        self.assertGreater(np.max(abs(outputs[-1]["Phi"])), 1e-6)
        self.assertGreater(np.max(abs(outputs[-1]["beta_dot"])), 1e-6)

    def test_exterior_tail_and_resolution_control(self):
        _, reconstruct = implementation()
        from initial import solve_slice
        short = reconstruct(solve_slice(1e-3, .3, outer=16., points=2401))
        long = reconstruct(solve_slice(1e-3, .3, outer=24., points=3601))
        for key in ("Phi", "Psi"):
            sampled = np.interp(short["r"], long["r"], long[key])
            self.assertLess(np.max(abs(short[key]-sampled)), 2e-10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
