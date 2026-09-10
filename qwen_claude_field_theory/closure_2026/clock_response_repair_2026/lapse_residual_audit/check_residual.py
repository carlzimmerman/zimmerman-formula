#!/usr/bin/env python3
"""Compare matrix and differential lapse residuals without changing input code.

The differential check samples the trigonometric interpolants on the existing
mesh. It is a float64 consistency check, not a certified continuum norm.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / "dirac_operator"
EXPECTED = {
    "constraint_data.py": "0d31f01de91f92909612bf19b5095d3fd789e53816ede6b26d6733c284fd9397",
    "lapse_source.py": "2f8f72b343b346a2e5922c098ddb6bcd14824ce4a610558f41f34e85d945a3a8",
}


def capture_case(module, amplitude, modes, coefficients):
    """Observe the original function's return frame; never replace its code."""
    observed = {}
    wanted = ("a2", "volume", "mass", "lapse", "rhs", "matrix", "row")

    def capture(frame, event, arg):
        if event == "return" and frame.f_code is module.case.__code__:
            observed.update({key: frame.f_locals[key] for key in wanted})

    previous = sys.getprofile()
    try:
        sys.setprofile(capture)
        result = module.case(amplitude, modes, coefficients)
    finally:
        sys.setprofile(previous)
    if set(observed) != set(wanted):
        raise AssertionError("Original lapse function did not expose expected fields")
    return result, observed


def main():
    hashes = {name: hashlib.sha256((INPUT / name).read_bytes()).hexdigest()
              for name in EXPECTED}
    if hashes != EXPECTED:
        raise AssertionError("Audit input differs from the reviewed base; review before rerunning")
    sys.path.insert(0, str(INPUT))
    import lapse_source

    coefficients = lapse_source.source_coefficients()
    rows = []
    for modes in (8, 16, 32):
        original, data = capture_case(lapse_source, 0.05, modes, coefficients)
        count = original["mesh"]
        wave = np.fft.fftfreq(count, d=1 / count)

        def derivative(values):
            return np.fft.ifft(1j * wave * np.fft.fft(values)).real

        x = 2 * np.pi * np.arange(count) / count
        derivative_control = float(np.max(np.abs(
            derivative(np.sin(3*x) + np.cos(2*x))
            - (3*np.cos(3*x) - 2*np.sin(2*x)))))
        assert derivative_control < 1e-11
        lapse = data["lapse"]
        # -Delta N = -(a2 N')' + volume*mass*N = rhs.
        matrix_residual = data["matrix"] @ lapse - data["rhs"]
        spectral_residual = (-derivative(data["a2"] * derivative(lapse))
                             + data["volume"] * data["mass"] * lapse
                             - data["rhs"])
        matrix_max = float(np.max(np.abs(matrix_residual)))
        spectral_max = float(np.max(np.abs(spectral_residual)))
        rhs_max = float(np.max(np.abs(data["rhs"])))
        assert np.all(np.isfinite(spectral_residual))
        assert matrix_max < 1e-11
        assert spectral_max > 1000 * max(matrix_max, np.finfo(float).eps)
        assert original["positive_lapse"]
        row = dict(
            amplitude=0.05, modes=modes, mesh=count,
            matrix_residual_max=matrix_max,
            spectral_preservation_residual_max=spectral_max,
            spectral_preservation_residual_rms=float(np.sqrt(np.mean(spectral_residual**2))),
            spectral_residual_relative_to_rhs=spectral_max / rhs_max,
            lapse_min=float(lapse.min()), lapse_max=float(lapse.max()),
            source_min=original["min_source"],
            mass_min=float(data["mass"].min()),
            principal_density_min=float(data["a2"].min()),
            constraint_C_max=data["row"]["full_C_residual"],
            constraint_T_max=data["row"]["full_T_residual"],
            constraint_momentum_max=data["row"]["full_momentum_residual"],
            analytic_derivative_control_max=derivative_control,
        )
        if rows:
            row["observed_residual_order"] = math.log2(
                rows[-1]["spectral_preservation_residual_max"] / spectral_max)
        rows.append(row)
    assert all(1.9 < row["observed_residual_order"] < 2.1 for row in rows[1:])
    return {
        "base_revision": "81ef7508749fe36fcad8882ea494fe567d868e67",
        "input_sha256": hashes,
        "cases": rows,
        "finite_assertion": "Matrix residuals are at roundoff while sampled differential residuals converge at order approximately two in this family.",
        "limits": [
            "Three float64 solves at one clock epoch and one amplitude on periodic plane-symmetric data.",
            "Reuses the original constraint solver, source, coefficients, and matrix solution; does not independently validate them.",
            "Spectral residual is sampled on the existing mesh, not an interval-certified continuum norm or rigorous error bound.",
            "Resolution changes both the constraint Fourier truncation and the lapse finite-difference mesh.",
            "No finite-time evolution, unrestricted 3D inverse, positive-lapse theorem, or MOND coupling is established.",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-file", type=Path, required=True)
    args = parser.parse_args()
    result = main()
    args.result_file.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
