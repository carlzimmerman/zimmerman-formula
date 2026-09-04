"""Provenance runner must preserve failure, not turn it into a physics PASS."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

MODULE = Path(__file__).with_name("run_audit.py")
runner = None
if MODULE.exists():
    spec = importlib.util.spec_from_file_location("run_audit", MODULE)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)


class AuditRunnerTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(runner, "provenance runner not implemented")

    def test_subprocess_output_and_nonzero_status_survive_recording(self):
        # A wrapper that normalizes every return code to zero must fail.
        with tempfile.TemporaryDirectory() as scratch:
            record = runner.record_job([sys.executable, "-c", "print('control'); raise SystemExit(7)"], scratch)
            self.assertEqual(record["exit_status"], 7)
            self.assertEqual(record["output"].strip(), "control")
            self.assertFalse(record["timed_out"])

    def test_timeout_is_recorded_as_unfinished_computation(self):
        # A timeout must not be interpreted as a negative mathematical result.
        with tempfile.TemporaryDirectory() as scratch:
            record = runner.record_job([sys.executable, "-c", "import time; time.sleep(1)"], scratch, timeout=0.02)
            self.assertTrue(record["timed_out"])
            self.assertNotEqual(record["exit_status"], 0)

    def test_missing_input_becomes_a_failed_record_not_a_stale_manifest(self):
        # A missing legacy input must not abort provenance before writing failure.
        missing = runner.HERE / "intentionally_absent_audit_fixture.py"
        self.assertFalse(missing.exists())
        try:
            record = runner.fingerprint(missing)
        except FileNotFoundError:
            self.fail("missing-input fingerprint aborts and can leave a stale PASS manifest")
        self.assertIsNone(record["sha256"])
        self.assertIn("error", record)


if __name__ == "__main__":
    unittest.main(verbosity=2)
