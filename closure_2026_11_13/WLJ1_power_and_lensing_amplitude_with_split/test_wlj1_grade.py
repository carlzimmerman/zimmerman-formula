#!/usr/bin/env python3
"""Full-grader regressions; numerical stages are saved fixtures, never rerun.

Run with a Python environment containing NumPy and SciPy:
  python -I -B test_wlj1_grade.py -v
The optional --grader-script argument supports testing a scratch mutation.
Every grader execution copies its inputs to a temporary directory before the
script writes its outputs. The lane's historical files are read only.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
GRADER = HERE / "wlj1_grade.py"
INPUTS = (
    "wlj1_hm.json", "wlj1_hm_MUTATE.json",
    "wlj1_c4.json", "wlj1_c4_MUTATE.json",
    "wlj1_shear.json", "wlj1_shear_MUTATE.json",
    "wlj1_lwb_lwb1.json", "wlj1_lwb_lwb1r.json",
) + tuple(
    f"parts/wlj1_kl1bx1_{foot}_{group}.json"
    for foot in ("canonical", "alt")
    for group in ("legacy", "deskids", "polish")
)
OUTPUTS = (
    "wlj1_grade.json", "wlj1_grade.out",
    "wlj1_grade_MUTATE.json", "wlj1_grade_MUTATE.out",
    "wlj1_grade_asfrozen.json", "wlj1_grade_asfrozen.out",
)
CASES = ("REF", "ADOPT", "S1.25", "S2", "S3")
GUARDED = ("C4", "CO1", "HLF1")
HOLD = "ROW HOLDS WITH THE SPLIT"
NOV = "NO VERDICT"


def run_grader(*, as_frozen=False, c4=None, grader_script=None):
    """Execute the actual script, allowing only a C4 input fixture variation."""
    with tempfile.TemporaryDirectory(prefix="wlj1-grade-regression-") as name:
        scratch = Path(name)
        shutil.copyfile(grader_script or GRADER, scratch / "wlj1_grade.py")
        for relative in INPUTS:
            target = scratch / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE / relative, target)
        if c4 is not None:
            (scratch / "wlj1_c4.json").write_text(json.dumps(c4))
        env = os.environ.copy()
        for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
            env[key] = "1"
        command = [sys.executable, "-I", "-B", str(scratch / "wlj1_grade.py")]
        if as_frozen:
            command.append("--as-frozen")
        completed = subprocess.run(command, cwd=scratch, env=env,
                                   capture_output=True, text=True, timeout=30)
        if completed.returncode or completed.stderr:
            raise AssertionError(f"Grader failed: {completed.returncode}\n{completed.stderr}")
        files = {relative: (scratch / relative).read_bytes()
                 for relative in OUTPUTS if (scratch / relative).exists()}
        result = json.loads(files["wlj1_grade_asfrozen.json" if as_frozen
                                  else "wlj1_grade.json"])
        return result, files


class FootingIsolationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen, cls.frozen_files = run_grader(as_frozen=True)
        cls.amended, cls.amended_files = run_grader()

    def assert_guarded_words(self, result, footing, expected):
        for case in CASES:
            for gate in GUARDED:
                key = f"{gate}|{case}|{footing}"
                self.assertEqual(result["gates"][key]["word"], expected, key)
            key = f"24|{case}|{footing}"
            self.assertEqual(result["rows"][key]["word"], expected, key)

    def c4_fixture(self):
        return json.loads((HERE / "wlj1_c4.json").read_bytes())

    def test_frozen_canonical_roundoff_does_not_downgrade_alt(self):
        # This fails if a single shared C4 known-answer flag guards both feet.
        self.assert_guarded_words(self.frozen, "canonical", NOV)
        self.assert_guarded_words(self.frozen, "alt", HOLD)
        self.assertEqual(self.frozen["KA"]["C4"], {"canonical": False, "alt": True})

    def test_amendment_a1_restores_only_the_roundoff_blocked_labels(self):
        self.assertEqual(self.amended["KA"]["C4"], {"canonical": True, "alt": True})
        for footing in ("canonical", "alt"):
            self.assert_guarded_words(self.amended, footing, HOLD)
        for key, gate in self.amended["gates"].items():
            for field in ("s", "D", "gate_word"):
                self.assertEqual(gate[field], self.frozen["gates"][key][field],
                                 (key, field))

    def test_both_modes_reproduce_all_six_historical_outputs_byte_for_byte(self):
        generated = {**self.amended_files, **self.frozen_files}
        self.assertEqual(set(generated), set(OUTPUTS))
        for relative in OUTPUTS:
            with self.subTest(output=relative):
                self.assertEqual(generated[relative], (HERE / relative).read_bytes())

    def test_non_reference_known_answer_failure_blocks_only_its_footing(self):
        # A1 must not waive KA-G2 or pool either footing's failure.
        for bad, good in (("canonical", "alt"), ("alt", "canonical")):
            with self.subTest(failed_footing=bad):
                c4 = self.c4_fixture()
                c4["KA"][f"KA_G2_{bad}"]["pass_"] = False
                result, _ = run_grader(c4=c4)
                self.assert_guarded_words(result, bad, NOV)
                self.assert_guarded_words(result, good, HOLD)
                for key, entry in result["gates"].items():
                    original = self.amended["gates"][key]
                    if entry["foot"] == good or entry["gate"] not in GUARDED:
                        self.assertEqual(entry, original, key)
                    self.assertEqual(entry["s"], original["s"], key)

    def test_a1_rejects_reference_error_above_tolerance_on_either_footing(self):
        for bad, good in (("canonical", "alt"), ("alt", "canonical")):
            with self.subTest(failed_footing=bad):
                c4 = self.c4_fixture()
                c4["KA"][f"KA_R_{bad}"] = {"r_eff": 1.0 + 2e-12, "pass_": False}
                result, _ = run_grader(c4=c4)
                self.assert_guarded_words(result, bad, NOV)
                self.assert_guarded_words(result, good, HOLD)

    def test_a1_accepts_small_reference_roundoff_but_frozen_mode_does_not(self):
        c4 = self.c4_fixture()
        c4["KA"]["KA_R_alt"] = {"r_eff": 1.0 + 5e-13, "pass_": False}
        amended, _ = run_grader(c4=c4)
        frozen, _ = run_grader(c4=c4, as_frozen=True)
        self.assert_guarded_words(amended, "alt", HOLD)
        self.assert_guarded_words(frozen, "alt", NOV)

    def test_frozen_mode_reads_checks_instead_of_stale_global_summary(self):
        c4 = self.c4_fixture()
        c4["KA"]["KA_R_canonical"] = {"r_eff": 1.0, "pass_": True}
        self.assertFalse(c4["KA_ok"])  # Deliberately leave the cached summary stale.
        result, _ = run_grader(c4=c4, as_frozen=True)
        self.assert_guarded_words(result, "canonical", HOLD)
        self.assert_guarded_words(result, "alt", HOLD)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--grader-script", type=Path)
    options, remaining = parser.parse_known_args()
    if options.grader_script is not None:
        GRADER = options.grader_script.resolve()
    unittest.main(argv=[sys.argv[0], *remaining])
