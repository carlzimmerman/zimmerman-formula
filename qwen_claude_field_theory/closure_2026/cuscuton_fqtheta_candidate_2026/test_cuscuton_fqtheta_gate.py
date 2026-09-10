import contextlib
import importlib.util
import io
import pathlib
import unittest


HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("cuscuton_fqtheta_gate", HERE / "cuscuton_fqtheta_gate.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class CuscutonFQThetaGateTests(unittest.TestCase):
    def test_action_gate(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            status = MOD.main()
        output = buf.getvalue()
        self.assertEqual(status, 0)
        self.assertIn("Checks completed: 11/11", output)
        self.assertIn("CUSCUTON_FQTHETA_NO_SLIP_OBSTRUCTION", output)


if __name__ == "__main__":
    unittest.main()
