import contextlib
import io
import unittest

import exact_exponential_scale_lock as gate


class TestExactExponentialScaleLock(unittest.TestCase):
    def test_scale_lock(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = gate.main()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("STATUS: EXACT_EXPONENTIAL_COEFFICIENT_DOOR_CLOSED", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
