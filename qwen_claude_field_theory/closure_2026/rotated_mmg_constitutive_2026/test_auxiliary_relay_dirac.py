import unittest

from auxiliary_relay_dirac import relay_dirac


class AuxiliaryRelayDiracTests(unittest.TestCase):
    def test_primary_secondary_chain_closes_locally(self):
        nz = relay_dirac(1.0, 2.0, 1.0)
        z = relay_dirac(0.0, 2.0, 1.0)
        self.assertEqual(nz["dirac_rank"], len(nz["dirac_matrix"]))
        self.assertEqual(nz["remaining_scalar_phase_dimension"], 0)
        self.assertEqual(nz["preservation_status"], "uniquely_fixed")
        self.assertLess(z["dirac_rank"], nz["dirac_rank"])
        self.assertEqual(z["preservation_status"], "rank_deficient")


if __name__ == "__main__":
    unittest.main(verbosity=2)
