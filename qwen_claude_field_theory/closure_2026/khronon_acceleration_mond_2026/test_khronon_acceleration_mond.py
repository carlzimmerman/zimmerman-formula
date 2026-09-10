import contextlib
import importlib.util
import io
import pathlib
import unittest


HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("khronon_acceleration_mond_gate", HERE / "khronon_acceleration_mond_gate.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class KhrononAccelerationMondTests(unittest.TestCase):
    def test_gate(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            status = MOD.main()
        output = buf.getvalue()
        self.assertEqual(status, 0)
        self.assertIn("Checks completed: 12/12", output)
        self.assertIn("ACCELERATION_KHRONON_3D_SLIP_OBSTRUCTION", output)


if __name__ == "__main__":
    unittest.main()
