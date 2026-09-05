#!/usr/bin/env python3
"""Bounded AQUAL convergence audit; no fitted/assumed quadrupoles or theory PASS.

Reuses the committed finite-volume operator, independently extracts multipoles,
and strengthens iteration stopping. This is not an independent PDE discretization.
"""
from __future__ import annotations
import os
for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
import numpy as np
import scipy
from numpy.polynomial.legendre import legvander
from scipy.sparse.linalg import spsolve

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOLVER = ROOT / "qwen_claude_field_theory/theory_2026/aqual_solver_2026.py"
sys.path.insert(0, str(SOLVER.parent))
from aqual_solver_2026 import Grid, build, multipoles

A0 = 9.3619e-11
GM_SUN = 1.32712440018e20
GEXT = 2.32e-10
PARK_MEAN, PARK_SIGMA = 1.6e-27, 1.8e-27


def mu_exp(x):
    return -np.expm1(-np.asarray(x, dtype=float))


def physical_Q2(c2, a0=A0, gm=GM_SUN):
    """Phi_2=c2*r^2*P2; Park Phi_2=-Q2*r_phys^2*P2/3."""
    return float(-3*c2*a0**1.5/np.sqrt(gm))


def extract(grid, u, window=(.003, .03), lmax=6):
    selected = (grid.r > window[0]) & (grid.r < window[1])
    if selected.sum() < 6 or lmax < 2 or lmax >= grid.nt:
        raise ValueError("unresolved extraction window or angular basis")
    # Fit all angular modes together: sampled Legendre functions are not orthogonal.
    r = grid.r[selected]
    f = u[selected] + 1/r[:, None]
    p = legvander(grid.mu_c, lmax)
    w = np.sqrt(grid.sin*grid.dt)
    coefficients, _, rank, _ = np.linalg.lstsq(p*w[:, None], f.T*w[:, None], rcond=None)
    if rank != lmax+1:
        raise ValueError("angular fit lost rank")
    # Include the decaying harmonic induced by a finite inner Dirichlet boundary.
    scale = np.sqrt(window[0]*window[1])
    radial = np.column_stack(((r/scale)**2, np.ones_like(r), (scale/r)**3))
    fit, _, rank, _ = np.linalg.lstsq(radial, coefficients[2], rcond=None)
    if rank != 3:
        raise ValueError("radial fit lost rank")
    residual = coefficients[2]-radial@fit
    return {"c2": float(fit[0]/scale**2), "decaying_l2": float(fit[2]*scale**3),
            "constant_l2": float(fit[1]), "radial_fit_rms": float(np.sqrt(np.mean(residual**2))),
            "window": list(window), "lmax": lmax, "points": int(selected.sum())}


def solve_checked(grid, mufun, eta, outer="zero", inner="total_spherical",
                  tol=1e-9, maxiter=160, seconds=120):
    if outer not in ("zero", "asymptotic") or inner not in ("total_spherical", "perturbation_spherical"):
        raise ValueError("unknown boundary prescription")
    start = time.monotonic()
    r, x = grid.r[:, None], grid.mu_c[None, :]
    external = -eta*r*x
    u = -np.ones((grid.ns, grid.nt))/r
    inner_u = -1/grid.r[0] + (eta*grid.r[0]*grid.mu_c if inner == "total_spherical" else np.zeros(grid.nt))
    outer_u = np.zeros(grid.nt)
    if outer == "asymptotic":
        if eta <= 0:
            raise ValueError("external-field asymptotic boundary requires eta>0")
        m = float(mufun(eta))
        eps = 1e-5
        slope = float((mufun(eta*(1+eps))-mufun(eta*(1-eps)))/(2*eps*m))
        outer_u = -1/(m*grid.r[-1]*np.sqrt(1+slope*(1-grid.mu_c**2)))
    updates, last_coefficients = [], []
    for iteration in range(maxiter):
        if time.monotonic()-start > seconds:
            raise TimeoutError("case resource cap exceeded")
        matrix, _ = build(grid, mufun, u+external, eta)
        rhs = -matrix@external.ravel()
        rhs[:grid.nt] = inner_u
        rhs[-grid.nt:] = outer_u
        proposed = spsolve(matrix, rhs).reshape(u.shape)
        # Unlike legacy stopping, inner |Phi|~1/rmin cannot dilute transition errors.
        update = float(np.max(np.abs(proposed[1:-1]-u[1:-1])/(1+np.abs(proposed[1:-1]))))
        if not np.isfinite(update):
            raise RuntimeError("nonfinite nonlinear update")
        updates.append(update)
        u = .5*(u+proposed)
        if iteration >= maxiter-8:
            last_coefficients.append(extract(grid, u)["c2"])
        if update < tol:
            break
    else:
        error = RuntimeError("nonlinear iteration exhausted without convergence")
        error.diagnostics = {"last_update": updates[-1], "minimum_update": min(updates),
                             "last_eight_updates": updates[-8:], "last_eight_c2": last_coefficients}
        raise error
    matrix, _ = build(grid, mufun, u+external, eta)
    coo = matrix.tocoo()
    off = coo.row != coo.col
    rr, cc, vv = coo.row[off], coo.col[off], coo.data[off]
    potential = (u+external).ravel()
    flux = vv*(potential[cc]-potential[rr])
    signed = np.bincount(rr, weights=flux, minlength=potential.size)
    absolute = np.bincount(rr, weights=abs(flux), minlength=potential.size)
    bulk = slice(grid.nt, -grid.nt)
    relative = abs(signed[bulk])/np.maximum(absolute[bulk], 1e-14*max(absolute))
    return u, {"iterations": iteration+1, "relative_update": update, "converged": True,
               "max_cell_relative_flux_imbalance": float(max(relative)),
               "p99_cell_relative_flux_imbalance": float(np.quantile(relative, .99)),
               "runtime_seconds": time.monotonic()-start}


def cases():
    common = dict(rmin=1e-4, rmax=1e4, ns=512, nt=128, a0=A0, gext=GEXT,
                  outer="zero", inner="total_spherical", tol=1e-9)
    variants = [
        ("coarse", dict(ns=256, nt=64)), ("baseline", {}),
        ("fine", dict(ns=768, nt=192)),
        ("outer_near", dict(rmax=1e3, ns=448)),
        ("outer_far", dict(rmax=1e5, ns=576)),
        ("inner_smaller", dict(rmin=3e-5, ns=545)),
        ("inner_larger", dict(rmin=3e-4, ns=482)),
        ("outer_asymptotic", dict(outer="asymptotic")),
        ("inner_perturbation", dict(inner="perturbation_spherical")),
        ("tighter_iteration", dict(tol=1e-11)),
        ("gext_minus_2sigma", dict(gext=2e-10)),
        ("gext_plus_2sigma", dict(gext=2.64e-10)),
        ("alternative_a0", dict(a0=1.1279e-10)),
        ("BN2011_exponential_anchor", dict(a0=1.2e-10, gext=1.9e-10)),
    ]
    return [dict(common, **{"name": name}, **changes) for name, changes in variants]


def run_case(case):
    grid = Grid(case["rmin"], case["rmax"], case["ns"], case["nt"])
    eta = case["gext"]/case["a0"]
    u, diagnostics = solve_checked(grid, mu_exp, eta, outer=case["outer"],
                                  inner=case["inner"], tol=case["tol"])
    fits = []
    for window in ((.003, .03), (.0015, .015), (.006, .06)):
        for order in (4, 6, 8):
            fit = extract(grid, u, window, order)
            fit["Q2_si"] = physical_Q2(fit["c2"], case["a0"])
            fits.append(fit)
    central = fits[1]
    q2 = central["Q2_si"]
    return {"case": case, "diagnostics": diagnostics, "fits": fits,
            "qzz": 2*central["c2"], "Q2_si": q2,
            "Q2_over_Park_upper_2sigma": q2/(PARK_MEAN+2*PARK_SIGMA),
            "legacy_qzz_same_solution": float(2*multipoles(grid, u, eta)[2])}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=[c["name"] for c in cases()])
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    inputs = [SOLVER, *sorted(HERE.glob("*.py")), *sorted(HERE.glob("*.md"))]
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    git = lambda *a: subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()
    commit, dirty = git("rev-parse", "HEAD"), bool(git("status", "--porcelain"))
    results, failures = [], []
    for case in cases():
        if args.case and args.case != case["name"]:
            continue
        try:
            record = run_case(case)
            results.append(record)
            print(f"{case['name']}: Q2={record['Q2_si']:.9e}; ratio={record['Q2_over_Park_upper_2sigma']:.5f}; "
                  f"iters={record['diagnostics']['iterations']}; "
                  f"flux={record['diagnostics']['max_cell_relative_flux_imbalance']:.2e}", flush=True)
        except Exception as exc:
            failures.append({"case": case, "error": repr(exc), "traceback": traceback.format_exc(),
                             "diagnostics": getattr(exc, "diagnostics", None)})
            print(f"FAILED {case['name']}: {exc}", flush=True)
    changed = [p for p, h in hashes.items() if digest(ROOT/p) != h]
    exit_code = int(bool(failures or changed))
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    result_path = output/"results.json"
    result_path.write_text(json.dumps({"results": results, "failures": failures,
                                      "changed_inputs": changed}, indent=2, allow_nan=False)+"\n")
    manifest = {
        "schema_version": 1, "claim_id": "fixed-exponential-AQUAL-solar-gate-2026-09-04",
        "repository": {"commit": commit, "dirty": dirty, "ending_commit": git("rev-parse", "HEAD")},
        "command": "PYTHONDONTWRITEBYTECODE=1 "+sys.executable+" "+" ".join(sys.argv),
        "environment": {"software": [sys.version, "numpy "+np.__version__, "scipy "+scipy.__version__],
                        "hardware": platform.platform(), "threads": 1},
        "mathematics": {
            "assertion_tested": "Numerical quadrupole sensitivity for exact mu=1-exp(-g/a0) AQUAL, not QUMOND",
            "coefficient_domain": "IEEE binary64; sparse nonlinear finite-volume solves",
            "conventions": "GM=a0=1 in PDE; Phi_N=-1/r; Park Q2=-3*c2*a0^(3/2)/sqrt(GM_Sun)",
            "inputs": [{"path": p, "sha256": h} for p, h in hashes.items()],
            "bounds": {"cases": [r["case"] for r in results], "case_cap_seconds": 120,
                       "max_iterations": 160, "random_sampling": False},
            "non_claims": ["No continuum error bound", "No independent PDE discretization",
                           "No reanalysis of raw Cassini data", "No relativistic closure or novelty proof"]},
        "randomness": {"used": False, "generator": "", "seed": None},
        "run": {"started_at": started, "runtime_seconds": time.monotonic()-start, "exit_status": exit_code},
        "outputs": [{"path": str(result_path.resolve()), "sha256": digest(result_path)}],
        "checks": [{"name": "all_requested_cases_completed", "passed": not failures},
                   {"name": "inputs_unchanged", "passed": not changed}],
        "result": "bounded numerical evidence; interpret with REPORT.md; execution status is not a theory verdict",
        "residual_risks": ["finite boundaries and mesh; no certified truncation bound",
                           "constant external field and point-Sun approximation",
                           "phenomenological fixed a0 and external-field inputs"]}
    (output/"computation_manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
