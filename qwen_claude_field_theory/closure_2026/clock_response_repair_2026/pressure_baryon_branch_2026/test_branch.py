#!/usr/bin/env python3
import unittest
import numpy as np
from solve import solve


class SupportedInitialBranch(unittest.TestCase):
    def test_coupled_solution_refinement_and_exterior(self):
        coarse=solve(points=300,tolerance=5e-7)
        fine=solve(points=800,tolerance=1e-8)
        larger=solve(points=900,outer=6.,tolerance=1e-8)
        for out in (coarse,fine,larger):
            self.assertEqual(out['status'],'initial_bvp_solved',out)
            self.assertLess(max(out['max_offgrid_relative']),1e-4)
            self.assertLess(out['max_boundary_residual'],1e-8)
        for key in ('omega','surface','total_areal_mass','areal_force'):
            np.testing.assert_allclose(coarse[key],fine[key],rtol=1e-4,atol=1e-9)
            np.testing.assert_allclose(fine[key],larger[key],rtol=1e-4,atol=1e-9)

    def test_dilute_configuration_excluded_analytically(self):
        out=solve(hc=1e-6,lam=50.)
        self.assertEqual(out['status'],'excluded_by_necessary_binding_bound')
        self.assertLess(out['binding_ratio'],1)

    def test_pressure_support_is_not_stationarity(self):
        out=solve()
        self.assertLess(out['expanding_density_rate_at_center'],0)

    def test_rejected_exterior_never_extrapolates_force(self):
        out=solve(hc=1e-4,lam=50.)
        self.assertEqual(out['status'],'physical_or_residual_gate_failed')
        self.assertFalse(out['vacuum_exterior'])
        self.assertIsNone(out['areal_force'])
        self.assertIsNone(out['force_radius'])

    def test_invalid_matter_domain_rejected(self):
        with self.assertRaises(ValueError):solve(hc=-.1)

if __name__=='__main__':unittest.main(verbosity=2)
