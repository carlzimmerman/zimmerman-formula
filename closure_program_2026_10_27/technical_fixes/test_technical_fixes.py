"""Bounded regression suite; never imports the executable research scripts."""
import importlib.util
import ast
import copy
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
P1 = ROOT / "rebuild_2026_10_22/P1D1_m6_boera_high_z_forest/p1d1_independent_sign_check.py"
X48 = ROOT / "rebuild_2026_10_22/X48_native_cf_zoom/x48_common_modes.py"
LAUNCHER = X48.with_name("x48_zoom_common.py")


def load_file(test, path):
    test.assertTrue(path.is_file(), "Missing opt-in correction: " + str(path))
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class IndependentInjection(unittest.TestCase):
    def test_literal_positive_injection_has_no_candidate_sign(self):
        # Break caught: using the candidate's sign/model to generate truth.
        mod = load_file(self, P1)
        got = mod.positive_injection([1, 1], [0.2, 0.8], [2, 3], 4, [0.1, -0.1])
        np.testing.assert_allclose(got, [9.7, 21.5], rtol=0, atol=1e-14)

    def test_sign_mutation_is_rejected_even_without_a_data_power_gate(self):
        # Break caught: both sides sharing SIGN, or vacuous passing on failed G1.
        mod = load_file(self, P1)
        result = mod.run_regression()
        self.assertTrue(result["positive_candidate"]["accepted"])
        self.assertFalse(result["negative_candidate"]["accepted"])
        self.assertGreater(result["negative_candidate"]["chi2"], 25)
        self.assertTrue(result["legacy_correlated_negative_injection"]["accepted"])


class CommonFourierModes(unittest.TestCase):
    def test_actual_hr_correction_preserves_support_and_covariance(self):
        # Break caught: dk is band-limited but HR uses the old unmasked Pk.
        # Execute the actual transformed draw, xi, CC and correction. Replace
        # only the astrophysical target solve with a fixed synthetic target.
        mod = load_file(self, LAUNCHER)
        helper = load_file(self, X48)
        source = X48.with_name("x48_zoom.py").read_text()
        function = copy.deepcopy(mod.transformed_initial_conditions(source))
        def assigns(node, name):
            return isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets)
        end = next(i for i, node in enumerate(function.body) if assigns(node, "c2r"))
        correction = [copy.deepcopy(n) for n in function.body
                      if assigns(n, "delta") or (assigns(n, "w") and "rvec" in ast.unparse(n))]
        self.assertEqual(len(correction), 2)
        function.body = (function.body[:end + 1] + ast.parse(
            "CCi = np.linalg.inv(CC)\ncvec = np.array([1., -2.])\nrvec = np.array([c1r, c2r])"
        ).body + correction + ast.parse("return locals()").body)
        herm = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == "_herm")
        tree = ast.Module(body=[herm, function], type_ignores=[])
        ast.fix_missing_locations(tree)
        # The requested box is 2pi, so full-grid physical wavevectors are integers.
        C = {"rhom": 3 * 5 / (4 * math.pi * (math.pi / 2) ** 3),
             "K": np.geomspace(1e-4, 100, 1001)}
        C["PK"] = np.exp(-C["K"] ** 2 / 4)
        for cutoff in (1.5, 10.0):  # test radial cutoff and excluded Nyquist planes
            namespace = {"np": np, "math": math, "lacey_cole_zf": lambda C, M: (1., .5),
                         "_common_gaussian": helper.gaussian_rfft,
                         "_common_support": getattr(helper, "support_mask", None),
                         "_common_kmax": cutoff}
            exec(compile(tree, "<actual-X48-HR-fixed-target>", "exec"), namespace)
            state = namespace["constrained_field"](C, 10., 11, 8, 1.5)
            # Independent full complex-grid oracle, not the helper support mask.
            axis = np.fft.fftfreq(8) * 8
            kx, ky, kz = np.meshgrid(axis, axis, axis, indexing="ij")
            kk = np.sqrt(kx ** 2 + ky ** 2 + kz ** 2)
            support = ((kk > 0) & (kk <= cutoff) & (abs(kx) != 4)
                       & (abs(ky) != 4) & (abs(kz) != 4))
            expected_pk = np.interp(np.log(np.maximum(kk, 1e-30)), np.log(C["K"]), C["PK"], left=0, right=0)
            expected_pk[~support] = 0
            dk_full = np.fft.fftn(state["delta"]) / 8 ** 3
            self.assertLess(float(np.max(abs(dk_full[~support]))), 2e-14)
            np.testing.assert_allclose(state["Pk"], expected_pk[:, :, :5], rtol=3e-15, atol=1e-16)
            window = np.exp(-(kk * state["RG"]) ** 2 / 2)
            vectors = np.stack([window, -kk ** 2 * window])
            oracle_cc = np.einsum("axyz,bxyz,xyz->ab", vectors, vectors, expected_pk) / state["V"]
            np.testing.assert_allclose(state["CC"], oracle_cc, rtol=4e-15, atol=1e-17)
            # Independent spectral covariance between delta(x) and both constraints.
            for a, name in enumerate(("xi1", "xi2")):
                oracle_xi = np.fft.ifftn(expected_pk * vectors[a]).real * 8 ** 3 / state["V"]
                np.testing.assert_allclose(state[name], oracle_xi, rtol=2e-14, atol=2e-17)
            constrained = np.array([np.sum(dk_full * vectors[a]).real for a in range(2)])
            np.testing.assert_allclose(constrained, [1, -2], rtol=0, atol=3e-14)

    def test_opt_in_launcher_wires_common_coefficients_and_dry_run_has_no_writes(self):
        # Break caught: launcher still using old array RNG, or starting a job in dry-run.
        mod = load_file(self, LAUNCHER)
        source = X48.with_name("x48_zoom.py").read_text()
        function = copy.deepcopy(mod.transformed_initial_conditions(source))
        end = next(i for i, node in enumerate(function.body) if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "d_r" for t in node.targets))
        function.body = function.body[:end + 1] + [ast.Return(value=ast.Name(id="dk", ctx=ast.Load()))]
        tree = ast.Module(body=[function], type_ignores=[])
        ast.fix_missing_locations(tree)
        helper = load_file(self, X48)
        namespace = {"np": np, "math": math, "lacey_cole_zf": lambda C, M: (1.0, 0.5),
                     "_common_gaussian": helper.gaussian_rfft,
                     "_common_support": getattr(helper, "support_mask", None), "_common_kmax": 4.0}
        exec(compile(tree, "<test-actual-patched-random-prefix>", "exec"), namespace)
        C = {"rhom": 1.0, "K": np.array([1e-4, 100.0]), "PK": np.ones(2)}
        L = 4 * (3 * 5 / (4 * math.pi)) ** (1 / 3)
        got = namespace["constrained_field"](C, 10.0, 9, 8, 1.5)
        want = helper.gaussian_rfft(8, L, 9, lambda k: np.ones_like(k), kmax=4.0)
        np.testing.assert_allclose(got, want, rtol=0, atol=0)
        with tempfile.TemporaryDirectory() as td:
            new_work = Path(td) / "future-common-job"
            cmd = [sys.executable, str(LAUNCHER), "--common-kmax", "4", "--work", str(new_work),
                   "--dry-run", "--mass", "1e12", "--ng", "48"]
            result = subprocess.run(cmd, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["mode"], "dry-run: no simulation started")
            self.assertFalse(new_work.exists())
            new_work.mkdir()
            refused = subprocess.run(cmd, text=True, capture_output=True)
            self.assertNotEqual(refused.returncode, 0)
            self.assertEqual(list(new_work.iterdir()), [])

    def test_shared_physical_modes_are_equal_after_fft_normalization(self):
        # Break caught: array-order RNG dependence on ng, or missing ng**3 factor.
        mod = load_file(self, X48)
        grids = {n: mod.gaussian_rfft(n, 7.0, 19, lambda k: 1 / (1 + k * k))
                 for n in (8, 12, 16)}
        for mx in range(-3, 4):
            for my in range(-3, 4):
                for mz in range(4):
                    vals = [g[mx % n, my % n, mz] / n ** 3 for n, g in grids.items()]
                    np.testing.assert_allclose(vals, [vals[0]] * 3, rtol=2e-15, atol=2e-15)
        other = mod.gaussian_rfft(8, 7.0, 20, lambda k: 1 / (1 + k * k))
        self.assertNotEqual(grids[8][1, 2, 1], other[1, 2, 1])

    def test_real_field_round_trip_and_parseval_even_and_odd(self):
        # Break caught: independent random draws on the kz=0 plane or bad Nyquist modes.
        mod = load_file(self, X48)
        for n in (7, 8, 12):
            dk = mod.gaussian_rfft(n, 5.0, 3, lambda k: np.ones_like(k))
            field = np.fft.irfftn(dk, s=(n, n, n))
            np.testing.assert_allclose(np.fft.rfftn(field), dk, atol=3e-13, rtol=2e-14)
            weights = np.full(dk.shape[-1], 2.0)
            weights[0] = 1.0
            if n % 2 == 0:
                weights[-1] = 1.0
                self.assertTrue(np.all(dk[n // 2, :, :] == 0))
                self.assertTrue(np.all(dk[:, n // 2, :] == 0))
                self.assertTrue(np.all(dk[:, :, -1] == 0))
            expected_var = np.sum(abs(dk) ** 2 * weights[None, None, :]) / n ** 6
            self.assertAlmostEqual(float(np.mean(field ** 2)), float(expected_var), places=12)
            self.assertEqual(dk[0, 0, 0], 0)

    def test_ensemble_power_and_independent_mode_covariance(self):
        # Break caught: wrong complex-Gaussian variance or correlated mode hashes.
        mod = load_file(self, X48)
        modes = [(1, 0, 0), (0, 1, 1), (1, 2, 1), (-2, 1, 2)]
        sample = []
        for seed in range(256):
            dk = mod.gaussian_rfft(8, 3.0, seed, lambda k: np.ones_like(k))
            sample.append([dk[x % 8, y % 8, z] / 8 ** 3 * np.sqrt(27)
                           for x, y, z in modes])
        z = np.asarray(sample)
        self.assertLess(float(np.max(abs(z.mean(axis=0)))), 0.17)
        self.assertLess(float(np.max(abs(np.mean(abs(z) ** 2, axis=0) - 1))), 0.25)
        self.assertLess(float(np.max(abs(np.mean(z.real ** 2, axis=0) - 0.5))), 0.15)
        self.assertLess(float(np.max(abs(np.mean(z.imag ** 2, axis=0) - 0.5))), 0.15)
        cross = z.conj().T @ z / len(z)
        cross[np.diag_indices(4)] = 0
        self.assertLess(float(np.max(abs(cross))), 0.20)

    def test_common_bandlimit_and_invalid_inputs(self):
        # Break caught: silently admitting unsupported or nonphysical input power.
        mod = load_file(self, X48)
        dk = mod.gaussian_rfft(8, 2 * np.pi, 1, lambda k: np.ones_like(k), kmax=1.1)
        self.assertEqual(np.count_nonzero(dk), 5)  # +/-x, +/-y and +z in rfft storage.
        for n, box, seed, power in ((2, 1, 0, lambda k: k * 0 + 1),
                                    (8, -1, 0, lambda k: k * 0 + 1),
                                    (8, 1, -1, lambda k: k * 0 + 1),
                                    (8, 1, 0, lambda k: k * 0 - 1)):
            with self.assertRaises(ValueError):
                mod.gaussian_rfft(n, box, seed, power)


if __name__ == "__main__":
    unittest.main(verbosity=2)
