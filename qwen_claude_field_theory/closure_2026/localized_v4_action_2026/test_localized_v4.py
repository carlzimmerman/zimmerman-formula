import unittest

from localized_action import action_data, localized_static_variation
from eliminate_localizers import eliminate_localizers
from localized_dirac import flat_scalar_blocks, dirac_report
from metric_variation_gate import metric_variation_gate
from causal_response_gate import causal_response_gate
from york_variation_gate import york_variation_gate
from curved_york_variation_gate import curved_york_variation_gate
from curved_localizer_dirac import curved_localizer_dirac_gate
from physical_causality_gate import physical_causality_gate
from retarded_carrier_pincer import retarded_carrier_pincer
from flrw_ward_gate import flrw_ward_gate


class LocalizedV4ContractTests(unittest.TestCase):
    def test_localizer_equations_are_present(self):
        data = action_data()
        constraints = data["constraints"]
        self.assertIn("Delta_h chi - D_iD_j K^ij", constraints)
        self.assertIn("H1 A - P_T div K", constraints)
        self.assertIn("H_TT Q - P_TT(3Ric)", constraints)

    def test_nonzero_and_zero_mode_cases_are_not_merged(self):
        blocks = flat_scalar_blocks()
        self.assertNotEqual(
            blocks["k_nonzero"]["kernel_dimension"],
            blocks["k_zero"]["kernel_dimension"],
        )

    def test_elimination_identity_is_not_assumed(self):
        result = eliminate_localizers()
        self.assertTrue(result["scalar_identity"])
        self.assertTrue(result["vector_identity"])
        self.assertTrue(result["tt_identity"])

    def test_static_potentials_are_varied_independently(self):
        result = localized_static_variation()
        self.assertTrue(result["psi_equation_is_slip_laplacian"])
        self.assertTrue(result["phi_equation_is_exponential_aqual"])

    def test_dirac_report_exposes_actual_matrices(self):
        for mode in ("k_nonzero", "k_zero"):
            result = dirac_report(mode)
            self.assertIn("poisson_matrix", result)
            self.assertIn("rank", result)
            self.assertIn("closure", result)

    def test_metric_variation_includes_inverse_and_projector_terms(self):
        result = metric_variation_gate()
        self.assertLess(result["max_finite_difference_error"], 2e-7)
        self.assertGreater(result["max_omitted_inverse_error"], 1e-4)
        self.assertGreater(result["max_omitted_projector_error"], 1e-4)

    def test_causal_gate_rechecks_all_six_source_polarizations(self):
        result = causal_response_gate()
        self.assertEqual(result["v3_spatial_pole_count"], 0)
        self.assertEqual(result["v3_factor_failure_count"], 0)
        self.assertGreater(result["v2_spatial_pole_count"], 0)

    def test_york_tt_projector_variation_is_metric_consistent(self):
        result = york_variation_gate()
        self.assertLess(result["projector_finite_difference_error"], 1e-7)
        self.assertLess(result["action_finite_difference_error"], 1e-7)
        self.assertLess(result["constraint_residual"], 1e-10)
        self.assertGreater(result["tt_dimension"], 0)

    def test_flrw_and_matter_ward_identity_are_derived(self):
        result = flrw_ward_gate()
        self.assertTrue(result["localizers_vanish_on_flrw"])
        self.assertTrue(result["lapse_equation_matches_friedmann"])
        self.assertTrue(result["continuity_implies_acceleration"])

    def test_curved_york_connection_terms_are_metric_consistent(self):
        result = curved_york_variation_gate()
        self.assertLess(result["projector_finite_difference_error"], 1e-7)
        self.assertLess(result["action_finite_difference_error"], 1e-7)
        self.assertLess(result["constraint_residual"], 1e-10)
        self.assertEqual(result["constraint_rank"], 4)
        self.assertEqual(result["tt_dimension"], 2)

    def test_full_tt_localizer_dirac_chain_closes_in_both_modes(self):
        result = curved_localizer_dirac_gate()
        for name in ("k_nonzero", "k_zero_raw", "k_zero_kernel_removed"):
            sector = result[name]
            self.assertEqual(
                sector["first_class_count"] + sector["second_class_count"],
                sector["independent_constraint_count"],
            )
            self.assertEqual(sector["auxiliary_configuration_dof"], 0)
            self.assertEqual(sector["preservation_residual"], 0.0)
            self.assertEqual(
                tuple(sector["poisson_matrix_shape"]),
                (sector["independent_constraint_count"],) * 2,
            )

    def test_exponential_physical_channel_is_separated_from_gr_control(self):
        result = physical_causality_gate()
        checks = result["checks"]
        self.assertTrue(all(checks.values()))
        self.assertIn("FAILS_STRICT_CAUSAL_GATE", result["status"])

    def test_retarded_carrier_pincer_is_derived(self):
        result = retarded_carrier_pincer()
        self.assertTrue(all(result["checks"].values()))
        self.assertIn("PINCER", result["status"])


if __name__ == "__main__":
    unittest.main()
