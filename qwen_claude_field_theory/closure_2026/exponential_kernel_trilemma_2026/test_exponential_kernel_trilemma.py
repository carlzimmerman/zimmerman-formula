import contextlib
import io
import unittest

import exponential_kernel_trilemma as gate


class TestExponentialKernelTrilemma(unittest.TestCase):
    def test_exact_symbolic_trilemma(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = gate.main()
        self.assertEqual(rc, 0, buf.getvalue())
        out = buf.getvalue()
        self.assertIn("MOND Hessian vanishes", out)
        self.assertIn("STATUS: EXPONENTIAL_KERNEL_LOCAL_SINGLE_METRIC_TRILEMMA", out)


if __name__ == "__main__":
    unittest.main()
