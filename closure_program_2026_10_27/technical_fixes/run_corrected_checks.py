#!/usr/bin/env python3
"""Run only the bounded correction suite and emit separately named evidence."""
import argparse
import ast
import importlib.util
import io
import json
import math
from pathlib import Path
import resource
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
P1 = ROOT / "rebuild_2026_10_22/P1D1_m6_boera_high_z_forest"
X48 = ROOT / "rebuild_2026_10_22/X48_native_cf_zoom"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    tests = load(Path(__file__).with_name("test_technical_fixes.py"))
    stream = io.StringIO()
    report = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
    print(stream.getvalue())
    sign = load(P1 / "p1d1_independent_sign_check.py").run_regression()
    helper = load(X48 / "x48_common_modes.py")
    # Reproduce the historical defect from the actual selected source AST.
    original = next(n for n in ast.parse((X48 / "x48_zoom.py").read_text()).body
                    if isinstance(n, ast.FunctionDef) and n.name == "constrained_field")
    prefix = [n for n in original.body if 74 <= n.lineno <= 78]
    code = compile(ast.Module(body=prefix, type_ignores=[]), "<historical-X48-random-block>", "exec")
    old = {}
    for n in (8, 16):
        namespace = {"np": np, "L": 7.0, "seed": 19, "ng": n,
                     "Pk": np.ones((n, n, n // 2 + 1)), "KK": np.ones((n, n, n // 2 + 1))}
        exec(code, namespace)
        old[n] = namespace["dk"]
    old_mismatch = abs(old[8][1, 2, 1] / 8 ** 3 - old[16][1, 2, 1] / 16 ** 3)
    old_roundtrip = np.max(abs(np.fft.rfftn(np.fft.irfftn(old[8], s=(8, 8, 8))) - old[8]))
    new = {n: helper.gaussian_rfft(n, 7, 19, lambda k: np.ones_like(k)) for n in (8, 12, 16)}
    shared_error = max(abs(new[n][x % n, y % n, z] / n ** 3 - new[8][x % 8, y % 8, z] / 8 ** 3)
                       for n in (12, 16) for x in range(-3, 4) for y in range(-3, 4) for z in range(4))
    modes = [(1, 0, 0), (0, 1, 1), (1, 2, 1), (-2, 1, 2)]
    sample = []
    for seed in range(256):
        dk = helper.gaussian_rfft(8, 3, seed, lambda k: np.ones_like(k))
        sample.append([dk[x % 8, y % 8, z] / 8 ** 3 * math.sqrt(27) for x, y, z in modes])
    z = np.asarray(sample)
    covariance = z.conj().T @ z / len(z)
    covariance[np.diag_indices(4)] = 0
    historical = json.loads((P1 / "p1d1_m6_boera_results.json").read_text())["footings"]["canonical"]["primary"]
    result = {"pass": bool(report.wasSuccessful() and sign["pass"] and old_mismatch > 1e-3 and old_roundtrip > 1e-3),
              "tests_run": report.testsRun, "failures": len(report.failures), "errors": len(report.errors),
              "historical_P1D1": {"class": historical["class"], "G0": historical["G0"], "G1": historical["G1"]},
              "P1D1_sign": sign,
              "X48": {"legacy_shared_mode_abs_mismatch": float(old_mismatch),
                       "legacy_rfft_roundtrip_max_abs_error": float(old_roundtrip),
                       "corrected_shared_modes_max_abs_error": float(shared_error),
                       "whitened_power_by_mode": np.mean(abs(z) ** 2, axis=0).tolist(),
                       "whitened_mean_max_abs": float(np.max(abs(z.mean(axis=0)))),
                       "cross_mode_covariance_max_abs": float(np.max(abs(covariance))),
                       "seeds": "0 through 255", "ng_covariance": 8,
                       "ng_shared_modes": [8, 12, 16], "ng_real_roundtrip": [7, 8, 12]},
              "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024),
              "non_claims": ["No observational refit or M6 exclusion", "No post-constraint common-mode guarantee",
                             "No halo simulation or convergence certification"]}
    with (args.output_dir / "corrected_checks_results.json").open("x") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    with (args.output_dir / "p1d1_sign_CORRECTED.json").open("x") as output:
        json.dump(sign, output, indent=2)
        output.write("\n")
    print(json.dumps({"pass": result["pass"], "tests_run": result["tests_run"], "X48": result["X48"],
                      "P1D1_positive": sign["positive_candidate"], "P1D1_negative": sign["negative_candidate"],
                      "historical_verdict": historical["class"], "peak_rss_bytes": result["peak_rss_bytes"]}, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
