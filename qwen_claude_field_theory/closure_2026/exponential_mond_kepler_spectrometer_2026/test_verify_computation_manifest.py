#!/usr/bin/env python3
"""Tests for byte-level computation-manifest verification."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
PATH = HERE / "verify_computation_manifest.py"
SPEC = importlib.util.spec_from_file_location("manifest_verifier", PATH)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


class ComputationManifestVerificationTests(unittest.TestCase):
    def test_current_manifest_hashes_match_working_tree(self) -> None:
        result = VERIFY.verify_manifest(
            HERE / "computation_manifest.json",
            repository_root=HERE.parents[2],
            require_tracked=False,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["files_verified"], result["files_declared"])

    def test_hash_mutation_is_rejected(self) -> None:
        manifest = VERIFY.load_strict_json(HERE / "computation_manifest.json")
        mutated = copy.deepcopy(manifest)
        mutated["sources"][0]["sha256"] = "0" * 64
        with self.assertRaises(VERIFY.ManifestVerificationError):
            VERIFY.verify_manifest_data(
                mutated,
                repository_root=HERE.parents[2],
                require_tracked=False,
            )

    def test_duplicate_and_parent_paths_are_rejected(self) -> None:
        manifest = VERIFY.load_strict_json(HERE / "computation_manifest.json")
        duplicate = copy.deepcopy(manifest)
        duplicate["outputs"].append(copy.deepcopy(duplicate["sources"][0]))
        with self.assertRaises(VERIFY.ManifestVerificationError):
            VERIFY.verify_manifest_data(
                duplicate,
                repository_root=HERE.parents[2],
                require_tracked=False,
            )
        unsafe = copy.deepcopy(manifest)
        unsafe["sources"][0]["path"] = "../escape.py"
        with self.assertRaises(VERIFY.ManifestVerificationError):
            VERIFY.verify_manifest_data(
                unsafe,
                repository_root=HERE.parents[2],
                require_tracked=False,
            )

    def test_nonfinite_json_constant_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text('{"value": NaN}\n', encoding="utf-8")
            with self.assertRaises(VERIFY.ManifestVerificationError):
                VERIFY.load_strict_json(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
