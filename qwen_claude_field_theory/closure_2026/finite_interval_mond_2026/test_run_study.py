"""Failure preservation and provenance tests; never mutate research inputs."""

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest


def runner():
    path = Path(__file__).with_name("run_study.py")
    spec = importlib.util.spec_from_file_location("finite_interval_runner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RunnerTests(unittest.TestCase):
    def test_success_records_output_and_required_environment(self):
        module = runner()
        with tempfile.TemporaryDirectory() as scratch:
            code = "import os,json; print(json.dumps({k:os.environ[k] for k in " + repr(list(module.ENVIRONMENT)) + "}))"
            result = module.record_job([sys.executable, "-c", code], scratch)
        self.assertEqual(result["exit_status"], 0)
        self.assertFalse(result["timed_out"])
        self.assertEqual(json.loads(result["output"]), module.ENVIRONMENT)
        self.assertGreaterEqual(result["runtime_seconds"], 0)
        self.assertIn("started_at", result)
        self.assertIn("ended_at", result)

    def test_nonzero_and_timeout_preserve_stdout_and_status(self):
        module = runner()
        with tempfile.TemporaryDirectory() as scratch:
            failed = module.record_job([sys.executable, "-c", "print('failure evidence', flush=True); raise SystemExit(7)"], scratch)
            timed = module.record_job([sys.executable, "-c", "import time; print('before timeout', flush=True); time.sleep(5)"], scratch, timeout=0.3)
        self.assertEqual(failed["exit_status"], 7)
        self.assertIn("failure evidence", failed["output"])
        self.assertEqual(timed["exit_status"], 124)
        self.assertTrue(timed["timed_out"])
        self.assertIn("before timeout", timed["output"])

    def test_missing_executable_is_recorded_and_timeout_is_bounded(self):
        module = runner()
        with tempfile.TemporaryDirectory() as scratch:
            missing = module.record_job([str(Path(scratch)/"absent-executable")], scratch)
            for timeout in (0, -1, 181, float("nan")):
                with self.assertRaises(ValueError):
                    module.record_job([sys.executable, "-c", "pass"], scratch, timeout=timeout)
        self.assertEqual(missing["exit_status"], 127)
        self.assertIn("FileNotFoundError", missing["output"])
        self.assertFalse(missing["timed_out"])

    def test_fingerprints_record_missing_and_detect_content_change(self):
        module = runner()
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            path = root/"input.txt"
            self.assertIsNone(module.fingerprint(path, root)["sha256"])
            path.write_text("first")
            first = module.fingerprint(path, root)
            self.assertEqual(first["path"], "input.txt")
            self.assertEqual(len(first["sha256"]), 64)
            path.write_text("second")
            self.assertNotEqual(first, module.fingerprint(path, root))

    def test_source_inventory_includes_new_docs_and_requires_full_catalog(self):
        module = runner()
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            here = root/"qwen_claude_field_theory/closure_2026/finite_interval_mond_2026"
            here.mkdir(parents=True)
            data = root/"real_research/data/sparc_data"
            data.mkdir(parents=True)
            (data/"one_rotmod.dat").write_text("synthetic")
            first_paths, first_errors = module.source_inventory(here, root)
            self.assertTrue(any("175" in error for error in first_errors))
            self.assertIn(here/"response_math.py", first_paths)
            self.assertIn(root/"hunt_2026/hunt_lib.py", first_paths)
            self.assertIn(root/"real_research/data/SPARC_Lelli2016c.mrt", first_paths)
            doc = here/"EXTRA.md"
            doc.write_text("new source")
            second_paths, _ = module.source_inventory(here, root)
            self.assertIn(doc, second_paths)
            self.assertNotEqual(first_paths, second_paths)

    def test_verdict_is_execution_only_and_detects_provenance_drift(self):
        module = runner()
        source = [{"path": "test.py", "sha256": "a"*64}]
        jobs = [{"exit_status": 0, "timed_out": False,
                 "output": '{"scientific_verdict":"rejected"}'}]
        self.assertEqual(module.failure_reasons(jobs, source, source, "abc", "abc", []), [])
        self.assertTrue(module.failure_reasons(jobs, source, source, "abc", "def", []))
        self.assertTrue(module.failure_reasons(jobs, source, [], "abc", "abc", []))
        self.assertTrue(module.failure_reasons(jobs, [{"path": "absent", "sha256": None}], [], "abc", "abc", []))
        self.assertTrue(module.failure_reasons([{ "exit_status": 4, "timed_out": False}], source, source, "abc", "abc", []))
        self.assertTrue(module.failure_reasons(jobs, source, source, "abc", "abc", ["missing required output"]))

    def test_job_plan_covers_both_suites_math_empirical_plot_and_old_cli(self):
        module = runner()
        with tempfile.TemporaryDirectory() as scratch:
            jobs = module.job_plan(module.HERE, module.ROOT, Path(scratch))
        self.assertEqual(len(jobs), 6)
        joined = "\n".join(" ".join(str(value) for value in job["argv"]) for job in jobs)
        for expected in ("response_math.py", "empirical.py", "render_results.py", "orbit_shape.py"):
            self.assertIn(expected, joined)
        self.assertEqual(joined.count("unittest discover"), 2)
        plot = next(job for job in jobs if job["name"] == "render_results")
        self.assertIn("MPLCONFIGDIR", plot["environment"])
        self.assertIn("XDG_CACHE_HOME", plot["environment"])


if __name__ == "__main__":
    unittest.main()
