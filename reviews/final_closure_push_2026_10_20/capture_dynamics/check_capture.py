#!/usr/bin/env python3
"""Bounded checks for the capture-dynamics review; never imports a lane module.

Run from repository root:
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 reviews/final_closure_push_2026_10_20/capture_dynamics/check_capture.py

The analytic proofs are in RESULT.md. These checks verify the implemented toy
examples, the literal original capture map, and a conditional rate calculation.
They do not rerun or reclassify any CFG experiment.
"""
import ast
import hashlib
import json
import math
import platform
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BASE = "f659e6d8e1ee4cf2b756f091aff56b018da1fb1e"
started = datetime.now(timezone.utc).isoformat()
clock0 = time.monotonic()
sources = json.loads((OUT / "source_hashes.json").read_text())
input_paths = [ROOT / x["path"] for x in sources["artifacts"]]
input_paths += [Path(__file__).resolve(), OUT / "source_hashes.json"]
before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths}

# Extract the actual method body, without executing the lane's top-level code.
lane = ROOT / "campaign_fresh_gravity/CFG916_lock_and_release/cfg916.py"
tree = ast.parse(lane.read_text())
cls = next(x for x in tree.body if isinstance(x, ast.ClassDef) and x.name == "Run3")
method = next(x for x in cls.body if isinstance(x, ast.FunctionDef) and x.name == "capture")
namespace = {"np": np}
exec(compile(ast.Module(body=[method], type_ignores=[]), str(lane) + ":capture-only", "exec"), namespace)
capture = namespace["capture"]
class Cell:
    rf = np.array([0.0, 1.0])
    mph = np.array([1.0])
cell = Cell()
def original(t, f):
    a, b = capture(cell, np.array([float(t)]), np.array([float(f)]), 2.0, 1e-12, "c")
    return [float(a[0]), float(b[0])]

def exact_cap(t, f, c):
    delta = min(f, max(c - t, Fraction(0)))
    return t + delta, f - delta

pairs = [(Fraction(0), Fraction(2)), (Fraction(1, 2), Fraction(3, 2))]
projection_outputs = [original(*p) for p in pairs]
assert projection_outputs == [[1.0, 1.0], [1.0, 1.0]]
assert pairs[0] != pairs[1]
for p, o in zip(pairs, projection_outputs):
    assert tuple(Fraction(x) for x in o) == exact_cap(*p, Fraction(1))
assert original(Fraction(3, 2), Fraction(1, 2)) == [1.5, 0.5]
history = []
t, f = Fraction(0), Fraction(2)
for c in (Fraction(1, 2), Fraction(1), Fraction(1, 2)):
    t, f = exact_cap(t, f, c)
    history.append({"capacity": str(c), "t": str(t), "f": str(f)})
assert t == 1 and f == 1
assert exact_cap(Fraction(0), Fraction(2), Fraction(1, 2))[0] == Fraction(1, 2)

# Fixed-capacity reaction: f=N-t, s=C-t, R=a-b, F' R=-theta(a-b)log(a/b).
reaction = []
max_dissipation_residual = 0.0
for B in (-4.0, 0.0, 4.0):
    N, C, theta = 2.0, 1.0, 1.0
    kp, km = math.exp(B / 2), math.exp(-B / 2)
    S = N + C + km / kp
    teq = 2 * N * C / (S + math.sqrt(S * S - 4 * N * C))
    assert 0.0 < teq < min(N, C)
    for j in range(1, 102):
        t = j / 103.0
        f, s = N - t, C - t
        a, b = kp * f * s, km * t
        fp = theta * math.log(t / (f * s)) - B
        direct = fp * (a - b)
        entropy = -theta * (a - b) * math.log(a / b)
        assert direct <= 1e-12 and entropy <= 1e-12
        max_dissipation_residual = max(max_dissipation_residual, abs(direct - entropy))
    assert abs(kp * (N - teq) * (C - teq) - km * teq) < 1e-13
    reaction.append({"B_over_theta": B, "equilibrium_t": teq, "finite_capacity": C})

# Hill/Plummer counterexample: x=y=0 is an exact invariant subspace.
# Units Omega=1, r_J=1, a=1/2, GM=3(1+a^2)^(3/2).
a, omega, rj, amp = 0.5, 1.0, 1.0, 1.5
mu = 3 * (rj * rj + a * a) ** 1.5
def V(z):
    return 0.5 * omega * omega * z * z - mu / math.sqrt(z * z + a * a)
def acc(z):
    return -omega * omega * z - mu * z / (z * z + a * a) ** 1.5
Esaddle = -mu / math.sqrt(rj * rj + a * a) - 1.5 * omega * omega * rj * rj
E0 = V(amp)
assert amp > rj and E0 > Esaddle
assert abs(mu / (rj * rj + a * a) ** 1.5 - 3 * omega * omega) < 1e-14
orbits = []
for dt in (0.001, 0.0005):
    z, v = amp, 0.0
    maxerr = maxabsz = 0.0
    exterior = crosses = 0
    for j in range(round(8 / dt)):
        oldz = z
        kz1, kv1 = v, acc(z)
        kz2, kv2 = v + 0.5 * dt * kv1, acc(z + 0.5 * dt * kz1)
        kz3, kv3 = v + 0.5 * dt * kv2, acc(z + 0.5 * dt * kz2)
        kz4, kv4 = v + dt * kv3, acc(z + dt * kz3)
        z += dt * (kz1 + 2 * kz2 + 2 * kz3 + kz4) / 6
        v += dt * (kv1 + 2 * kv2 + 2 * kv3 + kv4) / 6
        maxerr = max(maxerr, abs(0.5 * v * v + V(z) - E0))
        maxabsz = max(maxabsz, abs(z))
        exterior += abs(z) > rj
        crosses += oldz * z < 0
    assert maxerr < 1e-6 and maxabsz <= amp + 1e-7 and exterior > 0 and crosses >= 2
    orbits.append({"dt": dt, "duration": 8.0, "max_energy_abs_error": maxerr,
                   "max_abs_z": maxabsz, "sample_fraction_outside_rJ": exterior / round(8 / dt),
                   "zero_crossings": crosses})

# Conditional two-stage release/drain calculation, using only CFG916 PH1.
result916 = json.loads((ROOT / "campaign_fresh_gravity/CFG916_lock_and_release/cfg916_results.json").read_text())
ph1 = result916["post_hoc"]["PH1_residual_tolerance"]
def residual(t, release, drain):
    if abs(release - drain) < 1e-12:
        return (1 + drain * t) * math.exp(-drain * t)
    return (drain * math.exp(-release * t) - release * math.exp(-drain * t)) / (drain - release)
def matched_time(q):
    lo, hi = 0.0, 100.0
    for _ in range(100):
        x = 0.5 * (lo + hi)
        if (1 + x) * math.exp(-x) > q:
            lo = x
        else:
            hi = x
    return 0.5 * (lo + hi)
k_dwarf_max = math.log(2) / 12
rate_table = []
for key, row in ph1.items():
    q = row["f_max"]
    for alpha, instant in row["dt_min_Gyr"].items():
        gamma_inv = instant / -math.log(q)
        gamma = 1 / gamma_inv
        finite = matched_time(q) * gamma_inv
        assert finite > instant
        assert abs(residual(finite, gamma, gamma) - q) < 1e-14
        # t=3 Gyr is an illustrative condition, not a measured merger age.
        contrast_min_3gyr = 12 * math.log(1 / q) / (3 * math.log(2))
        rate_table.append({"sample_footing": key, "alpha_f": float(alpha), "f_max": q,
                           "drain_time_Gyr": gamma_inv, "instant_release_min_Gyr": instant,
                           "release_equals_drain_min_Gyr": finite,
                           "release_dwarf_rate_max_per_Gyr": k_dwarf_max,
                           "necessary_release_rate_contrast_if_3Gyr": contrast_min_3gyr,
                           "residual_if_universal_dwarf_rate_at_3Gyr": residual(3, k_dwarf_max, gamma)})

after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths}
assert before == after
assert all(before[x["path"]] == x["sha256"] for x in sources["artifacts"])
checks = [
    {"name": "literal_LRc_noninjective_capture", "status": "pass", "states": 2},
    {"name": "rational_independent_capture_oracle_and_history", "status": "pass"},
    {"name": "finite_reaction_equilibria_and_entropy_identity", "status": "pass", "interior_states": 303,
     "max_dissipation_identity_abs_residual": max_dissipation_residual},
    {"name": "Hill_vertical_orbit_energy_and_refinement", "status": "pass", "runs": orbits},
    {"name": "sequential_release_drain_exact_formula", "status": "pass", "cases": len(rate_table)},
    {"name": "source_hashes_unchanged", "status": "pass"},
]
results = {"base_checkpoint": BASE, "observed_head_at_run": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
           "projection_outputs": projection_outputs, "history": history,
           "finite_site_reaction": reaction,
           "hill_counterexample": {"a": a, "Omega": omega, "rJ": rj, "GM": mu, "amplitude": amp,
                                   "Jacobi_energy": E0, "saddle_energy": Esaddle, "orbits": orbits},
           "rate_table": rate_table, "checks": checks}
result_path = OUT / "checks.json"
result_path.write_text(json.dumps(results, indent=2) + "\n")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes = rss if platform.system() == "Darwin" else rss * 1024
manifest = {
    "schema_version": 2, "claim_id": "capture-dynamics-2026-10-20-bounded-checks",
    "repository": {"commit": BASE, "dirty": True},
    "command": ["env", "OMP_NUM_THREADS=1", "OPENBLAS_NUM_THREADS=1", "MKL_NUM_THREADS=1", "python3", str(Path(__file__).relative_to(ROOT))],
    "environment": {"software": [{"name": "Python", "version": platform.python_version()}, {"name": "numpy", "version": np.__version__}],
                    "hardware": platform.platform() + "; observed peak RSS " + str(rss_bytes) + " bytes"},
    "mathematics": {
        "assertion_tested": "The original one-cell LR-c map identifies two distinct states; exact rational history retains a historical cap; 303 finite-site reaction states obey the dissipation identity; two scalar Hill-orbit discretizations conserve energy within 1e-6 over 8 normalized time units; eight PH1-derived rate examples obey the sequential formula.",
        "coefficient_domain": "Rational oracle; IEEE binary64 numerical checks",
        "conventions": "Cold labels are CFG915 t (alpha_t=0) and f (alpha_f>0), not canonical tether nomenclature. Hill model has Omega=rJ=1, a=1/2, vertical invariant subspace. Rate model is post-hoc, no recapture, one-way release and exponential drain.",
        "inputs": ["CFG916 capture method body", "CFG916 PH1 residual tolerances and median drain clocks"],
        "bounds": {"projection_states": 2, "reaction_interior_states": 303, "hill_duration": 8.0, "hill_dt": [0.001, 0.0005], "rate_cases": 8},
        "non_claims": ["No existing experiment rerun or classifier changed", "No universal orbit stability from numerical integration", "No fitted rate, measured release age, physical bath, or full carrier action derived", "No global physical impossibility of capture/release"]},
    "randomness": {"used": False, "generator": "none", "seed": None},
    "run": {"started_at": started, "runtime_seconds": time.monotonic() - clock0, "exit_status": 0, "status": "completed",
            "resource_limits": {"memory_bytes": None, "cpu_seconds": None, "max_cores": 1, "max_threads": 1}},
    "outputs": [{"path": str(result_path.relative_to(ROOT)), "sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(), "kind": "result"}],
    "checks": checks,
    "result": "implementation and finite assertion verified in the stated range",
    "residual_risks": ["Analytic proofs in RESULT.md are self-reviewed, not independently certified", "The Hill counterexample is in the circular-orbit Hill approximation, not a Bullet reconstruction", "Rate times inherit CFG916 PH1's linear median-clock approximation"],
    "input_artifacts": [{"path": p, "sha256": h, "sha256_after": after[p]} for p, h in before.items()],
    "declared_results": [str(result_path.relative_to(ROOT))],
}
(OUT / "computation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"checks": [{"name": x["name"], "status": x["status"]} for x in checks],
                  "runtime_seconds": manifest["run"]["runtime_seconds"], "observed_peak_RSS_bytes": rss_bytes,
                  "rate_table": rate_table}, indent=2))
