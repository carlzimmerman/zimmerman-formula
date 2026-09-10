import contextlib
import io
import importlib.util
import pathlib
import unittest


HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "fqtheta_regulator_trilemma_gate", HERE / "fqtheta_regulator_trilemma_gate.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class FQThetaRegulatorTrilemmaTests(unittest.TestCase):
    def test_gate_exits_zero_and_reports_all_checks(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            status = MOD.main()
        output = stream.getvalue()
        self.assertEqual(status, 0)
        self.assertIn("Checks completed: 12/12", output)
        self.assertIn("FQTHETA_REGULATOR_TRILEMMA", output)

    def test_symbolic_reduced_residue(self):
        # Re-run the gate and retain the action-level output as an executable
        # regression check rather than asserting a desired sign by hand.
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            MOD.main()
        self.assertIn("K_red = -Unz**2*k**2/(2*Q0**2*Upp)", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
