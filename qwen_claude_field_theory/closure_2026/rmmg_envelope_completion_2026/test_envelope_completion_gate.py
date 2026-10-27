from __future__ import annotations

import unittest

import envelope_completion_gate as gate


class EnvelopeCompletionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = gate.run()

    def test_all_constructive_checks_pass(self):
        self.assertTrue(all(self.result["checks"].values()))

    def test_strong_hda_identity_is_derived(self):
        self.assertEqual(self.result["envelope"]["hda_residual"], "0")

    def test_static_exponential_flux_is_recovered(self):
        self.assertTrue(self.result["envelope"]["static_flux_is_mu_s"])
        self.assertTrue(self.result["exponential"]["primitive_identity"])

    def test_local_and_homogeneous_sectors_are_separate(self):
        local = self.result["dirac_local"]
        homogeneous = self.result["dirac_homogeneous"]
        self.assertGreater(local["rank"], homogeneous["rank"])
        self.assertEqual(local["remaining_phase_dimension"], 0)
        self.assertEqual(homogeneous["remaining_phase_dimension"], 4)


if __name__ == "__main__":
    unittest.main()
