#!/usr/bin/env python3
"""Fix-forward check of P1D1's real shape/GLS kernels; no data fit or output overwrite.

The six-bin positive injection is independent of candidate SIGN. Only the two
specified Setup methods are compiled from the historical script; none of its
top-level statements, data loads, fits or writes executes. Controlled spectra
are supplied at that kernel's boundary. This is an implementation sign check,
not validation of a cosmological flux response or observational sensitivity.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from scipy.optimize import minimize_scalar

SOURCE = Path(__file__).with_name("p1d1_m6_boera.py")


def positive_injection(adiabatic, isocurvature, tilt, bias_squared, noise):
    """Plant the declared +isocurvature convention without calling the candidate.

No candidate sign, fit object or fitted model callable is accepted. Inputs are
already evaluated spectra; this function does not certify their physics.
"""
    ad, iso, tilt, noise = np.broadcast_arrays(
        np.asarray(adiabatic, float), np.asarray(isocurvature, float),
        np.asarray(tilt, float), np.asarray(noise, float))
    if (not np.isfinite(bias_squared) or bias_squared <= 0 or
            not all(np.all(np.isfinite(a)) for a in (ad, iso, tilt, noise)) or
            np.any(ad < 0) or np.any(iso < 0) or np.any(tilt <= 0)):
        raise ValueError("Positive injection requires finite nonnegative spectra and positive bias/tilt")
    return bias_squared * tilt * (ad + iso) + noise


def run_regression():
    source = SOURCE.read_text()
    tree = ast.parse(source)
    setup = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Setup")
    methods = [n for n in setup.body if isinstance(n, ast.FunctionDef) and n.name in ("model_shape", "gls")]
    if {m.name for m in methods} != {"model_shape", "gls"}:
        raise RuntimeError("Historical candidate kernel has changed; review extraction")
    extracted = ast.Module(body=[ast.ClassDef(name="Candidate", bases=[], keywords=[], body=methods,
                                             decorator_list=[])], type_ignores=[])
    ast.fix_missing_locations(extracted)
    # Six literal controlled spectra. The planted vector below is independently
    # written, so reusing SIGN in the injection cannot silently pass the check.
    ad = np.ones(6)
    iso = np.array([0.2, 0.4, 1.0, 0.8, 0.3, 0.1])
    truth_literal = np.array([1.2, 1.4, 2.0, 1.8, 1.3, 1.1])
    truth = positive_injection(ad, iso, np.ones(6), 1.0, np.zeros(6))
    np.testing.assert_allclose(truth, truth_literal, atol=0, rtol=0)
    covariance_inverse = np.eye(6) * 100.0  # fixed synthetic sigma=0.1, not Boera covariance
    namespace = {"np": np, "KP": 0.03, "SIGN": 1.0,
                 "spectra": lambda bg, A, z, kh, RJ: (ad.copy(), iso.copy())}
    exec(compile(extracted, str(SOURCE), "exec"), namespace)
    candidate_type = namespace["Candidate"]
    candidate = candidate_type()
    candidate.bg, candidate.A = None, 1.0
    candidate.z = {"4.2": {"kv": np.full(6, 0.03), "kh": np.arange(6)}}

    def fit(sign, planted):
        namespace["SIGN"] = sign
        def score(mu):
            shape = candidate.model_shape("4.2", mu, 0.1, 0.0)
            return candidate.gls(shape, planted, covariance_inverse)[1]
        search = minimize_scalar(score, bounds=(0, 3), method="bounded", options={"xatol": 1e-12})
        mu, chi = min(((float(search.x), float(search.fun)), (0.0, score(0)), (3.0, score(3))),
                      key=lambda pair: pair[1])
        return {"mu_hat": mu, "chi2": chi,
                "accepted": bool(abs(mu - 1) < 1e-6 and chi < 1e-12)}

    positive = fit(1.0, truth)
    negative = fit(-1.0, truth)
    # Demonstrate the historical failure mode separately: changing the truth's
    # sign together with the model restores perfect recovery of the wrong sign.
    legacy = fit(-1.0, ad - iso)
    passed = positive["accepted"] and not negative["accepted"] and negative["chi2"] > 25 and legacy["accepted"]
    return {"check": "independent fixed-nuisance synthetic sign regression", "pass": bool(passed),
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "candidate_methods": ["Setup.model_shape", "Setup.gls"],
            "positive_candidate": positive, "negative_candidate": negative,
            "legacy_correlated_negative_injection": legacy,
            "historical_data_verdict": "NOT DIAGNOSTIC; unchanged; no physical F_b upper limit",
            "non_claims": ["No Boera refit", "No nuisance-marginalized sensitivity test",
                           "No gas-to-flux calibration", "No physical M6 exclusion"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_regression()
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["pass"] else 1)
