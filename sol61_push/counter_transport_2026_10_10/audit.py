"""Independent read-only audit of the saved 27 main counter-transport branches.

Uses fixed Gauss-Legendre quadrature and W=-integral M dM/r, independently
of checks.py's adaptive quadrature and cumulative-mass energy expansion.
Writes only audit_results.json beside this script.
"""
import hashlib
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[1]
data = json.loads((ROOT / "runs/main/results.json").read_text())
manifest = json.loads((ROOT / "runs/main/manifest.json").read_text())
assert data["mutate"] is False, "Only the main run is audited."

bands = data["bands"]
cuts = sorted({0.0, 1.0, *[value for band in bands for value in band]})
z, w = np.polynomial.legendre.leggauss(160)
r = np.concatenate([
    (a + b) / 2 + (b - a) * z / 2
    for a, b in zip(cuts[:-1], cuts[1:])
])
wg = np.concatenate([
    (b - a) * w / 2 for a, b in zip(cuts[:-1], cuts[1:])
])
worst = {"W": 0.0, "I2": 0.0, "U": 0.0, "ratio": 0.0, "mass": 0.0}
branch_count = 0
fourier_count = 0

for row in data["results"]:
    c = row["c_at_outer_radius"]
    norm = math.log1p(c) - c / (1 + c)

    def M(q):
        return (np.log1p(c * q) - c * q / (1 + c * q)) / norm

    dm = c * c * r / ((1 + c * r) ** 2 * norm)
    masses = [M(b) - M(a) for a, b in bands]
    F = [
        (M(np.clip(r, a, b)) - M(a)) / mass
        for (a, b), mass in zip(bands, masses)
    ]
    masks = [(r > a) & (r < b) for a, b in bands]
    W0 = -np.sum(wg * M(r) * dm / r)
    assert set(row["branches"]) == {
        "inward_only", "moment_neutral", "energy_neutral"
    }

    for branch, value in row["branches"].items():
        branch_count += 1
        mi = row["mi"]
        mo = value["mo"]
        donor = mi + mo
        mass = M(r) + mi * F[0] - donor * F[1] + mo * F[2]
        dnew = dm * (
            1 + mi / masses[0] * masks[0]
            - donor / masses[1] * masks[1]
            + mo / masses[2] * masks[2]
        )
        assert donor <= masses[1] + 1e-12 and np.min(dnew) >= 0
        W = -np.sum(wg * mass * dnew / r)
        worst["W"] = max(worst["W"], abs(W - W0 - value["delta_W"]))
        worst["I2"] = max(
            worst["I2"],
            abs(np.sum(wg * r * r * (dnew - dm)) - value["delta_I2"]),
        )
        worst["mass"] = max(worst["mass"], abs(np.sum(wg * dnew) - 1))
        for transform in value["transforms"]:
            fourier_count += 1
            k = transform["k_R"]
            j = np.sin(k * r) / (k * r)
            U0 = np.sum(wg * j * dm)
            U1 = np.sum(wg * j * dnew)
            worst["U"] = max(worst["U"], abs(U1 - U0 - transform["delta_U"]))
            worst["ratio"] = max(
                worst["ratio"],
                abs((U1 / U0) ** 2 - transform["halo_U_squared_ratio"]),
            )

hash_checks = []
for entry in manifest["input_artifacts"] + manifest["outputs"]:
    actual = hashlib.sha256((REPOSITORY / entry["path"]).read_bytes()).hexdigest()
    hash_checks.append({
        "path": entry["path"], "sha256": actual,
        "matches_manifest": actual == entry["sha256"],
    })

bounds = {
    "c": sorted({row["c_at_outer_radius"] for row in data["results"]}),
    "inward_fraction_of_donor_mass": sorted({
        row["donor_fraction_moved_in"] for row in data["results"]
    }),
    "radial_bands": bands,
    "kR": sorted({
        t["k_R"] for row in data["results"]
        for branch in row["branches"].values() for t in branch["transforms"]
    }),
}
expected = {
    "c": [5.0, 15.0, 40.0],
    "inward_fraction_of_donor_mass": [0.02, 0.1, 0.3],
    "radial_bands": [[0.05, 0.15], [0.25, 0.35], [0.7, 0.9]],
    "kR": [0.01, 0.1, 1.0, 3.0, 10.0],
}
tolerance = 1e-12
passed = (
    bounds == expected and len(data["results"]) == 9
    and branch_count == 27 and fourier_count == 135
    and all(error < tolerance for error in worst.values())
    and all(item["matches_manifest"] for item in hash_checks)
)
output = {
    "assertion": "Independent numerical verification of the saved main-run mass, binding-energy, second-moment and Fourier calculations",
    "passed": bool(passed),
    "method": "NumPy fixed Gauss-Legendre, 160 nodes per radial segment; direct W=-integral M dM/r and direct Fourier integration of changed density",
    "conventions": "G=M_initial=R_outer=1; isolated one-component truncated NFW; main branches only",
    "bounds": bounds,
    "branches_audited": branch_count,
    "fourier_points_audited": fourier_count,
    "absolute_tolerance": tolerance,
    "maximum_absolute_residuals": {key: float(value) for key, value in worst.items()},
    "input_and_output_hash_checks": hash_checks,
    "nonclaims": [
        "Floating-point quadrature agreement is not a certified error bound or a universal theorem.",
        "Equal gravitational binding energy does not establish a physical energy-conserving evolution; E=W/2 additionally requires isolated stationary endpoints without surface terms.",
        "Positive density is not a stationary phase-space distribution: upward density jumps at the band boundaries exclude an ordinary isotropic nonnegative f(E) equilibrium there; anisotropic support is untested.",
        "No RAR equilibrium, angular-momentum transport, entropy, stability or formation-timescale result.",
        "Individual-halo Fourier changes are not a cosmic-shear or observational prediction.",
    ],
}
(ROOT / "audit_results.json").write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps({"passed": bool(passed), "branches": branch_count, "maximum_absolute_residuals": output["maximum_absolute_residuals"]}))
raise SystemExit(0 if passed else 1)
