#!/usr/bin/env python3
r"""Direct AQUAL Solar-System quadrupole for ``mu(x)=1-exp(-x)``.

This is deliberately not the algebraic RAR relation and not the QUMOND phantom-density
integral.  It solves, in units ``GM=a0=1``, the axisymmetric nonlinear equation

    div[mu(|grad phi|) grad phi] = 4*pi*delta^3(r),
    grad(phi) -> -eta*z_hat,

using the finite-volume implementation in ``theory_2026/aqual_solver_2026.py``.  The
regular unknown is ``u=phi+eta*z``.  The physical inner boundary ``phi=-1/r`` is
therefore ``u=-1/r+eta*r*cos(theta)``; the outer boundary is ``u=0``.
The angular domain uses cell-centred theta and regular (zero-flux) polar faces.

The near-origin correction is fitted as ``u+1/r = c2*r^2*P2(cos(theta))+...``.  Thus
``qzz=2*c2`` in the repository convention and the Blanchet--Novak coefficient is
``q2=3*c2=(3/2)*qzz``.  Consequently

    |Q2| = (3/2)|qzz| a0^(3/2)/sqrt(GM).

Scope: this is a bounded numerical audit of one weak-field AQUAL boundary-value problem.
It is not evidence for a relativistic completion and it is not a novelty claim.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.util
import json
import math
from pathlib import Path
from typing import Callable, Iterable, Sequence

import numpy as np
from numpy.polynomial.legendre import legvander
from scipy.integrate import quad
from scipy.optimize import brentq


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE.parents[1] / "theory_2026" / "aqual_solver_2026.py"
_SPEC = importlib.util.spec_from_file_location("_aqual_solver_2026_core", CORE_PATH)
if _SPEC is None or _SPEC.loader is None:  # pragma: no cover - installation failure
    raise ImportError(f"cannot load AQUAL core from {CORE_PATH}")
CORE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(CORE)


G_SI = 6.67430e-11
M_SUN_SI = 1.98892e30
GM_SUN_SI = G_SI * M_SUN_SI
A0_FROZEN_SI = 9.3619e-11
G_EXT_CENTRAL_SI = 2.32e-10
G_EXT_SIGMA_SI = 0.16e-10
PARK_2026_CENTRAL_SI = 1.6e-27
PARK_2026_SIGMA_SI = 1.8e-27
PARK_2026_POSITIVE_95_SI = PARK_2026_CENTRAL_SI + 2.0 * PARK_2026_SIGMA_SI


def mu_exp(x):
    """Exact target kernel, evaluated without small-x cancellation."""
    arr = np.asarray(x, dtype=float)
    ans = -np.expm1(-arr)
    return float(ans) if ans.ndim == 0 else ans


def solve_true_field(y_newton: float) -> float:
    """Solve ``x*mu_exp(x)=y_newton`` on its unique nonnegative branch."""
    y_newton = float(y_newton)
    if y_newton < 0.0:
        raise ValueError("y_newton must be nonnegative")
    if y_newton == 0.0:
        return 0.0
    upper = y_newton + math.sqrt(y_newton) + 2.0
    return brentq(
        lambda x: x * mu_exp(x) - y_newton,
        0.0,
        upper,
        xtol=5e-15,
        rtol=9e-15,
    )


def nu_aqual_exp(y_newton):
    """Spherical inverse partner of ``mu_exp``; this is not ``nu_RAR``."""
    arr = np.asarray(y_newton, dtype=float)
    flat = arr.reshape(-1)
    out = np.empty_like(flat)
    for i, value in enumerate(flat):
        if value < 0.0:
            raise ValueError("y_newton must be nonnegative")
        out[i] = math.inf if value == 0.0 else solve_true_field(float(value)) / value
    out = out.reshape(arr.shape)
    return float(out) if out.ndim == 0 else out


def nu_rar(y_newton):
    r"""Empirical ``[1-exp(-sqrt(y_N))]^-1`` relation used by many RAR fits."""
    arr = np.asarray(y_newton, dtype=float)
    if np.any(arr < 0.0):
        raise ValueError("y_newton must be nonnegative")
    den = -np.expm1(-np.sqrt(arr))
    ans = np.divide(1.0, den, out=np.full_like(arr, np.inf), where=den != 0.0)
    return float(ans) if ans.ndim == 0 else ans


def inner_u_boundary(eta: float, radius: float, cosine: float) -> float:
    """Regular-variable value equivalent to the physical ``phi=-1/r`` boundary."""
    return -1.0 / float(radius) + float(eta) * float(radius) * float(cosine)


def classify_against_ceiling(
    values: Iterable[float], errors: Iterable[float], ceiling: float
) -> tuple[bool, str]:
    """Classify only if every conservative lower endpoint exceeds the ceiling."""
    values = tuple(float(value) for value in values)
    errors = tuple(abs(float(error)) for error in errors)
    if not values or len(values) != len(errors):
        raise ValueError("values and errors must be nonempty and have equal length")
    excluded = min(value - error for value, error in zip(values, errors)) > float(ceiling)
    label = (
        "EXACT_EXPONENTIAL_AQUAL_EXCLUDED_AT_TESTED_PARAMETERS"
        if excluded
        else "EXACT_EXPONENTIAL_AQUAL_NOT_RULED_OUT_BY_THIS_TEST"
    )
    return excluded, label


@dataclass(frozen=True)
class SolveResult:
    eta: float
    ns: int
    nt: int
    rmin: float
    rmax: float
    fit_min: float
    fit_max: float
    qzz: float
    qzz_abs: float
    q2_blanchet_novak: float
    iterations: int
    iterate_change: float
    discrete_relative_residual: float
    converged: bool


def _extract_qzz(grid, u: np.ndarray, fit_window=(1.0e-3, 1.0e-2)) -> float:
    """Extract ``2*c2`` with a discrete weighted Legendre least-squares projection.

    Solving for P0..P6 simultaneously prevents the huge spherical ``1/r`` piece and
    odd multipoles from leaking into P2 through finite angular quadrature error.
    """
    correction = u + 1.0 / grid.r[:, None]
    basis = legvander(grid.mu_c, 6)
    weight = grid.sin * grid.dt
    gram = basis.T @ (weight[:, None] * basis)
    coefficients = np.linalg.solve(gram, basis.T @ (weight[:, None] * correction.T)).T
    chosen = (grid.r > fit_window[0]) & (grid.r < fit_window[1])
    if np.count_nonzero(chosen) < 4:
        raise ValueError("fit window contains too few radial cells")
    c2 = np.polyfit(grid.r[chosen] ** 2, coefficients[chosen, 2], 1)[0]
    return float(2.0 * c2)


def _discrete_residual(grid, u, phi, eta: float) -> float:
    matrix, boundary_rhs = CORE.build(grid, mu_exp, phi, eta)
    external = -eta * grid.r[:, None] * grid.mu_c[None, :]
    rhs = -(matrix @ external.ravel())
    rhs[: grid.nt] = boundary_rhs[: grid.nt]
    rhs[-grid.nt :] = 0.0
    lhs = matrix @ u.ravel()
    residual = lhs - rhs
    interior = np.ones(residual.size, dtype=bool)
    interior[: grid.nt] = False
    interior[-grid.nt :] = False
    scale = max(np.linalg.norm(lhs[interior]), np.linalg.norm(rhs[interior]), 1e-300)
    return float(np.linalg.norm(residual[interior]) / scale)


def solve_dimensionless_qzz(
    eta: float,
    *,
    ns: int = 192,
    nt: int = 48,
    rmin: float = 1.0e-6,
    rmax: float = 1.0e4,
    fit_window=(1.0e-3, 1.0e-2),
    tolerance: float = 1.0e-12,
) -> SolveResult:
    """Run one nonlinear finite-volume solve and extract the central quadrupole."""
    grid = CORE.Grid(rmin=rmin, rmax=rmax, ns=ns, nt=nt)
    u, phi, iterations, change = CORE.solve(
        grid,
        mu_exp,
        float(eta),
        tol=tolerance,
        itmax=600,
        relax=0.4,
        verbose=False,
    )
    qzz = _extract_qzz(grid, u, fit_window=fit_window)
    residual = _discrete_residual(grid, u, phi, float(eta))
    converged = bool(
        np.isfinite(u).all()
        and change < tolerance
        and residual < 2.0e-5
    )
    return SolveResult(
        eta=float(eta),
        ns=ns,
        nt=nt,
        rmin=rmin,
        rmax=rmax,
        fit_min=float(fit_window[0]),
        fit_max=float(fit_window[1]),
        qzz=qzz,
        qzz_abs=abs(qzz),
        q2_blanchet_novak=1.5 * abs(qzz),
        iterations=int(iterations),
        iterate_change=float(change),
        discrete_relative_residual=residual,
        converged=converged,
    )


@dataclass(frozen=True)
class ContinuumEstimate:
    eta: float
    qzz_abs: float
    conservative_numerical_error: float
    q2_blanchet_novak: float
    fit_residual_max: float
    meshes: tuple[SolveResult, ...]


def continuum_estimate(
    eta: float,
    resolutions: Sequence[tuple[int, int]] = ((192, 48), (288, 72), (384, 96)),
    **solve_kwargs,
) -> ContinuumEstimate:
    """Extrapolate linearly in ``h^2`` and retain the full last correction as error."""
    meshes = tuple(
        solve_dimensionless_qzz(eta, ns=ns, nt=nt, **solve_kwargs)
        for ns, nt in resolutions
    )
    if not all(item.converged for item in meshes):
        raise RuntimeError("at least one nonlinear mesh solve did not converge")
    h2 = np.array([1.0 / item.ns**2 for item in meshes])
    values = np.array([item.qzz_abs for item in meshes])
    slope, intercept = np.polyfit(h2, values, 1)
    fitted = intercept + slope * h2
    fit_residual = float(np.max(np.abs(values - fitted)))
    # This deliberately exceeds the formal fit error: it keeps the whole distance from
    # the continuum intercept to the finest raw mesh as a one-sided discretisation budget.
    numerical_error = max(abs(values[-1] - intercept), fit_residual)
    return ContinuumEstimate(
        eta=float(eta),
        qzz_abs=float(intercept),
        conservative_numerical_error=float(numerical_error),
        q2_blanchet_novak=float(1.5 * intercept),
        fit_residual_max=fit_residual,
        meshes=meshes,
    )


def inner_boundary_sensitivity(eta: float) -> dict:
    """Move ``rmin`` by two decades at approximately fixed logarithmic spacing."""
    configurations = ((1.0e-5, 144), (1.0e-6, 160), (1.0e-7, 176))
    solves = tuple(
        solve_dimensionless_qzz(eta, ns=ns, nt=40, rmin=rmin)
        for rmin, ns in configurations
    )
    values = np.array([item.qzz_abs for item in solves])
    return {
        "solves": solves,
        "qzz_min": float(values.min()),
        "qzz_max": float(values.max()),
        "fractional_span": float(np.ptp(values) / np.mean(values)),
    }


def outer_boundary_sensitivity(eta: float) -> dict:
    """Move ``rmax`` by two decades at approximately fixed logarithmic spacing."""
    configurations = ((1.0e3, 144), (1.0e4, 160), (1.0e5, 176))
    solves = tuple(
        solve_dimensionless_qzz(eta, ns=ns, nt=40, rmax=rmax)
        for rmax, ns in configurations
    )
    values = np.array([item.qzz_abs for item in solves])
    return {
        "solves": solves,
        "qzz_min": float(values.min()),
        "qzz_max": float(values.max()),
        "fractional_span": float(np.ptp(values) / np.mean(values)),
    }


def q2_si_from_qzz(qzz_abs: float, a0_si: float, gm_si: float = GM_SUN_SI) -> float:
    return 1.5 * abs(float(qzz_abs)) * float(a0_si) ** 1.5 / math.sqrt(float(gm_si))


def _solve_external_newtonian(nu: Callable[[float], float], eta: float) -> float:
    return brentq(lambda e_n: e_n * float(nu(e_n)) - eta, 1e-14, eta + 2.0)


def qumond_q(nu: Callable[[float], float], eta: float, vmax: float = 20.0) -> float:
    """Milgrom's exact QUMOND integral; included only as an architecture control."""
    e_n = _solve_external_newtonian(nu, eta)

    def angular_integral(v: float) -> float:
        def integrand(xi: float) -> float:
            d2 = e_n * e_n + v**4 + 2.0 * e_n * v * v * xi
            value = float(nu(math.sqrt(max(d2, 1e-300))))
            shape = e_n * (3.0 * xi - 5.0 * xi**3) + v * v * (1.0 - 3.0 * xi**2)
            return (value - 1.0) * shape

        return quad(integrand, -1.0, 1.0, epsabs=2e-8, epsrel=2e-8, limit=200)[0]

    cusp = math.sqrt(e_n)
    left = quad(angular_integral, 0.0, cusp, epsabs=2e-8, epsrel=2e-8, limit=200)[0]
    right = quad(angular_integral, cusp, vmax, epsabs=2e-8, epsrel=2e-8, limit=200)[0]
    return abs(1.5 * (left + right))


def spherical_validation(ns: int = 192, nt: int = 32) -> float:
    """Maximum field error against ``x*mu(x)=r^-2`` on a broad interior annulus."""
    grid = CORE.Grid(rmin=1e-4, rmax=1e4, ns=ns, nt=nt)
    _, phi, _, _ = CORE.solve(grid, mu_exp, 0.0, tol=1e-12, itmax=600, relax=0.4)
    numeric = CORE.grads(grid, phi)[:, nt // 2]
    exact = np.array([solve_true_field(1.0 / radius**2) for radius in grid.r])
    interior = (grid.r > 2e-3) & (grid.r < 5e2)
    return float(np.max(np.abs(numeric[interior] / exact[interior] - 1.0)))


def _estimate_for_eta_fast(eta: float) -> ContinuumEstimate:
    return continuum_estimate(
        eta,
        resolutions=((128, 32), (192, 48), (288, 72)),
    )


def run_audit() -> dict:
    anchor_eta = 1.9 / 1.2
    anchor = continuum_estimate(anchor_eta)
    frozen_eta = G_EXT_CENTRAL_SI / A0_FROZEN_SI
    frozen = continuum_estimate(frozen_eta)

    # A modest three-mesh bracket isolates sensitivity to the quoted Galactic-field
    # uncertainty.  This is parametric sensitivity, not folded into the numerical error.
    eta_low = (G_EXT_CENTRAL_SI - G_EXT_SIGMA_SI) / A0_FROZEN_SI
    eta_high = (G_EXT_CENTRAL_SI + G_EXT_SIGMA_SI) / A0_FROZEN_SI
    low = _estimate_for_eta_fast(eta_low)
    high = _estimate_for_eta_fast(eta_high)

    q2_value = q2_si_from_qzz(frozen.qzz_abs, A0_FROZEN_SI)
    q2_num_error = q2_si_from_qzz(frozen.conservative_numerical_error, A0_FROZEN_SI)
    q2_low = q2_si_from_qzz(low.qzz_abs, A0_FROZEN_SI)
    q2_high = q2_si_from_qzz(high.qzz_abs, A0_FROZEN_SI)
    q2_low_error = q2_si_from_qzz(low.conservative_numerical_error, A0_FROZEN_SI)
    q2_high_error = q2_si_from_qzz(high.conservative_numerical_error, A0_FROZEN_SI)
    tested_values = (q2_value, q2_low, q2_high)
    tested_errors = (q2_num_error, q2_low_error, q2_high_error)
    excluded, classification = classify_against_ceiling(
        tested_values, tested_errors, PARK_2026_POSITIVE_95_SI
    )
    robust_lower_q2 = min(
        value - error for value, error in zip(tested_values, tested_errors)
    )

    q_qumond_partner = qumond_q(nu_aqual_exp, frozen_eta)
    q_qumond_rar = qumond_q(nu_rar, frozen_eta)
    q2_qumond_partner = q2_si_from_qzz(q_qumond_partner, A0_FROZEN_SI)
    inner_boundary = inner_boundary_sensitivity(frozen_eta)
    outer_boundary = outer_boundary_sensitivity(frozen_eta)

    result = {
        "method": {
            "equation": "div[(1-exp(-|grad phi|))*grad phi]=4*pi*delta^3(r)",
            "units": "GM=a0=1",
            "boundary_conditions": "grad(phi)->-eta*z_hat; u=phi+eta*z; phi(rmin)=-1/rmin so u(rmin,theta)=-1/rmin+eta*rmin*cos(theta); u(rmax)=0",
            "quadrupole_convention": "u+1/r=c2*r^2*P2+...; qzz=2*c2; q2_BN=3*c2=1.5*qzz",
            "core_reused": str(CORE_PATH.relative_to(HERE.parents[2])),
        },
        "spherical_max_relative_error": spherical_validation(),
        "published_anchor": {
            "eta": anchor_eta,
            "published_q2_BN": 0.26,
            "computed": {
                "qzz_abs": anchor.qzz_abs,
                "q2_BN": anchor.q2_blanchet_novak,
                "numerical_error_qzz": anchor.conservative_numerical_error,
                "fractional_anchor_difference": anchor.q2_blanchet_novak / 0.26 - 1.0,
                "meshes": [asdict(item) for item in anchor.meshes],
            },
        },
        "frozen_parameters": {
            "a0_si": A0_FROZEN_SI,
            "g_ext_si": G_EXT_CENTRAL_SI,
            "g_ext_sigma_si": G_EXT_SIGMA_SI,
            "eta": frozen_eta,
            "qzz_abs": frozen.qzz_abs,
            "numerical_error_qzz": frozen.conservative_numerical_error,
            "q2_BN": frozen.q2_blanchet_novak,
            "Q2_si": q2_value,
            "Q2_numerical_error_si": q2_num_error,
            "Q2_over_positive_95_limit": q2_value / PARK_2026_POSITIVE_95_SI,
            "meshes": [asdict(item) for item in frozen.meshes],
        },
        "external_field_one_sigma_sensitivity": {
            "eta_low": eta_low,
            "eta_high": eta_high,
            "Q2_low_si": min(q2_low, q2_high),
            "Q2_high_si": max(q2_low, q2_high),
            "Q2_low_numerical_error_si": q2_low_error,
            "Q2_high_numerical_error_si": q2_high_error,
        },
        "inner_boundary_location_sensitivity": {
            "strategy": "rmin shifted by two decades at approximately matched ds=d(log r)",
            "qzz_min": inner_boundary["qzz_min"],
            "qzz_max": inner_boundary["qzz_max"],
            "fractional_span": inner_boundary["fractional_span"],
            "solves": [asdict(item) for item in inner_boundary["solves"]],
        },
        "outer_boundary_location_sensitivity": {
            "strategy": "rmax shifted by two decades at approximately matched ds=d(log r)",
            "qzz_min": outer_boundary["qzz_min"],
            "qzz_max": outer_boundary["qzz_max"],
            "fractional_span": outer_boundary["fractional_span"],
            "solves": [asdict(item) for item in outer_boundary["solves"]],
        },
        "architecture_controls": {
            "QUMOND_q_same_spherical_mu": q_qumond_partner,
            "QUMOND_Q2_same_spherical_mu_si": q2_qumond_partner,
            "AQUAL_over_QUMOND_same_spherical_mu": q2_value / q2_qumond_partner,
            "QUMOND_q_empirical_nu_RAR": q_qumond_rar,
            "nu_AQUAL_at_yN_1": nu_aqual_exp(1.0),
            "nu_RAR_at_yN_1": nu_rar(1.0),
        },
        "observation": {
            "Park_2026_central_si": PARK_2026_CENTRAL_SI,
            "Park_2026_sigma_si": PARK_2026_SIGMA_SI,
            "positive_two_sigma_ceiling_si": PARK_2026_POSITIVE_95_SI,
        },
        "exclusion_test": {
            "derived_excluded": excluded,
            "rule": "minimum over central and g_ext +/-1sigma of (Q2 - numerical_error) exceeds positive two-sigma ceiling",
            "robust_lower_Q2_si": robust_lower_q2,
            "robust_lower_over_ceiling": robust_lower_q2 / PARK_2026_POSITIVE_95_SI,
        },
        "classification": classification,
        "scope": "bounded finite-volume computation; no relativistic-completion or novelty claim",
    }
    return result


def _print_result(result: dict) -> None:
    anchor = result["published_anchor"]["computed"]
    frozen = result["frozen_parameters"]
    controls = result["architecture_controls"]
    sensitivity = result["external_field_one_sigma_sensitivity"]
    inner = result["inner_boundary_location_sensitivity"]
    outer = result["outer_boundary_location_sensitivity"]
    print("EXACT EXPONENTIAL AQUAL SOLAR-SYSTEM QUADRUPOLE AUDIT")
    print("=" * 72)
    print(f"spherical field validation max error: {result['spherical_max_relative_error']:.3e}")
    print(
        "BN2011 anchor (eta=1.9/1.2): "
        f"q2={anchor['q2_BN']:.6f} vs published 0.260000 "
        f"({anchor['fractional_anchor_difference']:+.3%})"
    )
    for mesh in result["published_anchor"]["computed"]["meshes"]:
        print(
            f"  anchor mesh {mesh['ns']}x{mesh['nt']}: |qzz|={mesh['qzz_abs']:.8f}, "
            f"residual={mesh['discrete_relative_residual']:.2e}"
        )
    print()
    print(
        f"frozen eta={frozen['eta']:.6f}: |qzz|={frozen['qzz_abs']:.6f} "
        f"+/- {frozen['numerical_error_qzz']:.6f} (conservative numerical budget)"
    )
    print(
        f"|Q2|={frozen['Q2_si']:.4e} +/- {frozen['Q2_numerical_error_si']:.1e} s^-2; "
        f"ratio to +2sigma ceiling={frozen['Q2_over_positive_95_limit']:.3f}"
    )
    print(
        "g_ext +/-1sigma sensitivity at fixed a0: "
        f"|Q2| in [{sensitivity['Q2_low_si']:.4e}, {sensitivity['Q2_high_si']:.4e}] s^-2"
    )
    print(
        "matched-resolution rmin sensitivity: "
        f"fractional |qzz| span={inner['fractional_span']:.3e}"
    )
    print(
        "matched-resolution rmax sensitivity: "
        f"fractional |qzz| span={outer['fractional_span']:.3e}"
    )
    print()
    print(
        "same spherical mu, QUMOND shortcut: "
        f"|Q2|={controls['QUMOND_Q2_same_spherical_mu_si']:.4e} s^-2; "
        f"direct AQUAL/QUMOND={controls['AQUAL_over_QUMOND_same_spherical_mu']:.4f}"
    )
    print(
        "at y_N=1: "
        f"nu_AQUAL-partner={controls['nu_AQUAL_at_yN_1']:.6f}, "
        f"empirical nu_RAR={controls['nu_RAR_at_yN_1']:.6f} (different functions)"
    )
    print(f"classification: {result['classification']}")


if __name__ == "__main__":
    audit = run_audit()
    _print_result(audit)
    output = HERE / "exact_exponential_aqual_q2_2026.json"
    output.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output.name}")
