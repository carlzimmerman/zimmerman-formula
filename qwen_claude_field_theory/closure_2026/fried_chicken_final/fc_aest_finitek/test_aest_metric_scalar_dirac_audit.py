import contextlib
import io
import unittest

import aest_metric_scalar_dirac_audit as audit
import verify_aest_source_lagrangian as source_check


class TestAestMetricScalarDiracAudit(unittest.TestCase):
    def test_exact_reduction(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = audit.main()
        self.assertEqual(rc, 0, buf.getvalue())
        out = buf.getvalue()
        self.assertIn("STATUS: HOST_SCALAR_CONSTRAINT_CLAIM_REFUTED", out)
        self.assertIn("scalar_DOF=1", out)
        self.assertIn("omega^2=", out)

    def test_compact_lagrangian_matches_covariant_route(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = source_check.main()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("SOURCE_MATCH_STATUS= PASS", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
